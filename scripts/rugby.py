"""Met à jour data/rugby.json : derniers résultats et prochains matchs des grandes compétitions de rugby.

Lancé par GitHub Actions (.github/workflows/actualites.yml), mais ne contacte la source
qu'une fois par heure (la clé gratuite est partagée entre tous ses utilisateurs).
Source : TheSportsDB (clé publique gratuite « 123 », ou une clé personnelle dans le
secret THESPORTSDB_KEY). Avec la clé gratuite, les classements de rugby ne sont pas fournis :
seuls les matchs sont mis à jour. Les anciennes données sont gardées en cas d'erreur.
"""
import json, os, sys, time, urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHIER = os.path.join(ROOT, 'data', 'rugby.json')
KEY = os.environ.get('THESPORTSDB_KEY', '').strip() or '123'
API = f'https://www.thesportsdb.com/api/v1/json/{KEY}'
INTERVALLE = timedelta(minutes=55)

# id sur le site : identifiant de la compétition chez TheSportsDB
COMPETITIONS = {
    'top14': 4430,   # French Top 14
    'prem': 4414,    # English Premiership Rugby
    'urc': 4446,     # United Rugby Championship
    'ercc': 4550,    # European Rugby Champions Cup
    'six': 4714,     # Six Nations Championship
}


def get(path):
    req = urllib.request.Request(API + path, headers={'User-Agent': 'BIBI-netanyahou-site/1.0 (github.com/Jjlb18/BIBI-netanyahou)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    time.sleep(2.5)  # reste sous 30 requêtes par minute
    return data or {}


def quand(e):
    ts = e.get('strTimestamp')
    if ts:
        try:
            d = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(f"{e.get('dateEvent')}T{(e.get('strTime') or '00:00:00')[:8]}").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def conv(e, passe):
    d = quand(e)
    if not d:
        return None
    sd, se = e.get('intHomeScore'), e.get('intAwayScore')
    statut = (e.get('strStatus') or '').lower()
    if 'postpon' in statut or 'cancel' in statut:
        st = 'annule'
    elif passe and sd not in (None, '') and se not in (None, ''):
        st = 'post'
    elif passe:
        return None
    else:
        st = 'pre'
    m = {'d': d.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z'),
         'dom': e.get('strHomeTeam') or '?', 'ext': e.get('strAwayTeam') or '?', 'st': st}
    if st == 'post':
        m['sd'], m['se'] = int(sd), int(se)
    return m


def matchs(lid):
    out = []
    for path, passe in ((f'/eventspastleague.php?id={lid}', True), (f'/eventsnextleague.php?id={lid}', False)):
        for e in (get(path).get('events') or []):
            m = conv(e, passe)
            if m:
                out.append(m)
    seen, uniq = set(), []
    for m in sorted(out, key=lambda x: x['d']):
        k = (m['d'], m['dom'], m['ext'])
        if k not in seen:
            seen.add(k); uniq.append(m)
    return uniq


def classement(lid):
    out = []
    for e in (get(f'/lookuptable.php?l={lid}').get('table') or []):
        try:
            out.append({'r': int(e.get('intRank') or 0), 'eq': e.get('strTeam') or '?', 'j': int(e.get('intPlayed') or 0),
                        'g': int(e.get('intWin') or 0), 'n': int(e.get('intDraw') or 0), 'p': int(e.get('intLoss') or 0),
                        'pts': int(e.get('intPoints') or 0)})
        except (TypeError, ValueError):
            continue
    return out


def main():
    try:
        ancien = json.load(open(FICHIER, encoding='utf8'))
    except Exception:
        ancien = {'competitions': {}}
    now = datetime.now(timezone.utc)
    dernier = ancien.get('essai')
    if dernier and now - datetime.fromisoformat(dernier) < INTERVALLE and os.environ.get('FORCER') != '1':
        print('Rugby : mis à jour il y a moins d\'une heure, rien à faire.')
        return
    nouveau = {'maj': ancien.get('maj'), 'essai': now.isoformat(timespec='seconds'), 'source': 'thesportsdb',
               'competitions': dict(ancien.get('competitions', {}))}
    change = False
    for cid, lid in COMPETITIONS.items():
        avant = ancien.get('competitions', {}).get(cid, {'matchs': [], 'classement': []})
        apres = dict(avant)
        for cle, f in (('matchs', matchs), ('classement', classement)):
            try:
                v = f(lid)
                if v:
                    apres[cle] = v
            except Exception as ex:
                print(f'! {cid} {cle} : {ex}', file=sys.stderr)
        if apres != avant:
            change = True
        print(f'{cid} : {len(apres.get("matchs", []))} matchs, {len(apres.get("classement", []))} équipes')
        nouveau['competitions'][cid] = apres
    if change:
        nouveau['maj'] = now.isoformat(timespec='seconds')
    json.dump(nouveau, open(FICHIER, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('rugby.json', 'mis à jour' if change else 'inchangé')


if __name__ == '__main__':
    main()
