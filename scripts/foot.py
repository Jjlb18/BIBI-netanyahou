"""Met à jour data/foot.json : matchs (résultats, en direct, à venir) et classements
des grandes compétitions européennes de football.

Lancé automatiquement par GitHub Actions (.github/workflows/actualites.yml).
Source : l'API publique de scores d'ESPN. Si une compétition ne répond pas,
ses anciennes données sont gardées.
"""
import json, os, sys, urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHIER = os.path.join(ROOT, 'data', 'foot.json')

# id sur le site : code ESPN
COMPETITIONS = {
    'ucl': 'uefa.champions',
    'uel': 'uefa.europa',
    'uecl': 'uefa.europa.conf',
    'eng': 'eng.1',
    'esp': 'esp.1',
    'ita': 'ita.1',
    'ger': 'ger.1',
    'fra': 'fra.1',
}
JOURS_AVANT, JOURS_APRES = 10, 21


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (foot-bot)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def matchs(code):
    now = datetime.now(timezone.utc)
    debut = (now - timedelta(days=JOURS_AVANT)).strftime('%Y%m%d')
    fin = (now + timedelta(days=JOURS_APRES)).strftime('%Y%m%d')
    data = get(f'https://site.api.espn.com/apis/site/v2/sports/soccer/{code}/scoreboard?dates={debut}-{fin}&limit=300')
    out = []
    for ev in data.get('events', []):
        comp = (ev.get('competitions') or [{}])[0]
        teams = {c.get('homeAway'): c for c in comp.get('competitors', [])}
        if 'home' not in teams or 'away' not in teams:
            continue
        st = ((comp.get('status') or ev.get('status') or {}).get('type') or {})
        state = st.get('state', 'pre')  # pre / in / post
        m = {
            'd': ev.get('date') or comp.get('date'),
            'dom': teams['home']['team'].get('displayName', '?'),
            'ext': teams['away']['team'].get('displayName', '?'),
            'st': state,
        }
        if st.get('name') in ('STATUS_POSTPONED', 'STATUS_CANCELED'):
            m['st'] = 'annule'
        if state in ('in', 'post'):
            try:
                m['sd'] = int(float(teams['home'].get('score', 0)))
                m['se'] = int(float(teams['away'].get('score', 0)))
            except (TypeError, ValueError):
                pass
        if state == 'in':
            m['min'] = (comp.get('status') or {}).get('displayClock') or st.get('shortDetail', '')
        out.append(m)
    out.sort(key=lambda x: x['d'] or '')
    return out


def classement(code):
    data = get(f'https://site.api.espn.com/apis/v2/sports/soccer/{code}/standings')
    groupes = data.get('children') or [data]
    entries = []
    for g in groupes:
        entries += (g.get('standings') or {}).get('entries', [])
    out = []
    for e in entries:
        s = {x.get('name'): x.get('value') for x in e.get('stats', [])}
        def v(k):
            try:
                return int(float(s.get(k) or 0))
            except (TypeError, ValueError):
                return 0
        out.append({'r': v('rank'), 'eq': (e.get('team') or {}).get('displayName', '?'),
                    'j': v('gamesPlayed'), 'g': v('wins'), 'n': v('ties'), 'p': v('losses'), 'pts': v('points')})
    out.sort(key=lambda x: (x['r'] or 999, -x['pts']))
    return out


def main():
    try:
        ancien = json.load(open(FICHIER, encoding='utf8'))
    except Exception:
        ancien = {'competitions': {}}
    nouveau = {'maj': ancien.get('maj'), 'competitions': {}}
    change = False
    for cid, code in COMPETITIONS.items():
        avant = ancien.get('competitions', {}).get(cid, {'matchs': [], 'classement': []})
        apres = dict(avant)
        try:
            ms = matchs(code)
            if ms:
                apres['matchs'] = ms
        except Exception as ex:
            print(f'! {cid} matchs : {ex}', file=sys.stderr)
        try:
            cl = classement(code)
            if cl:
                apres['classement'] = cl
        except Exception as ex:
            print(f'! {cid} classement : {ex}', file=sys.stderr)
        if apres != avant:
            change = True
            print(f'✓ {cid} : {len(apres.get("matchs", []))} matchs, {len(apres.get("classement", []))} équipes')
        nouveau['competitions'][cid] = apres
    if change:
        nouveau['maj'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
        os.makedirs(os.path.dirname(FICHIER), exist_ok=True)
        json.dump(nouveau, open(FICHIER, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('foot.json', 'mis à jour' if change else 'inchangé')


if __name__ == '__main__':
    main()
