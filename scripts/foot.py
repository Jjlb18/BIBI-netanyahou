"""Met à jour data/foot.json : matchs (résultats, en direct, à venir) et classements
des grandes compétitions européennes de football.

Lancé automatiquement par GitHub Actions (.github/workflows/actualites.yml).
Source : football-data.org (gratuit, nécessite une clé).
La clé doit être enregistrée dans le dépôt GitHub comme secret nommé FOOTBALL_DATA_TOKEN
(Settings → Secrets and variables → Actions → New repository secret).
Si la clé manque ou qu'une compétition ne répond pas, les anciennes données sont gardées.
"""
import json, os, sys, time, urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHIER = os.path.join(ROOT, 'data', 'foot.json')
API = 'https://api.football-data.org/v4'
TOKEN = os.environ.get('FOOTBALL_DATA_TOKEN', '').strip()

# id sur le site : code football-data.org (offre gratuite)
COMPETITIONS = {
    'ucl': 'CL',
    'eng': 'PL',
    'esp': 'PD',
    'ita': 'SA',
    'ger': 'BL1',
    'fra': 'FL1',
}
JOURS_AVANT, JOURS_APRES = 10, 21
PAUSE = 6.5  # l'offre gratuite autorise 10 requêtes par minute

ETATS = {'SCHEDULED': 'pre', 'TIMED': 'pre', 'IN_PLAY': 'in', 'PAUSED': 'in', 'LIVE': 'in',
         'FINISHED': 'post', 'AWARDED': 'post', 'POSTPONED': 'annule', 'CANCELLED': 'annule', 'SUSPENDED': 'annule'}


def get(path):
    req = urllib.request.Request(API + path, headers={'X-Auth-Token': TOKEN})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    time.sleep(PAUSE)
    return data


def nom(team):
    return (team or {}).get('shortName') or (team or {}).get('name') or '?'


def matchs(code):
    now = datetime.now(timezone.utc)
    debut = (now - timedelta(days=JOURS_AVANT)).strftime('%Y-%m-%d')
    fin = (now + timedelta(days=JOURS_APRES)).strftime('%Y-%m-%d')
    data = get(f'/competitions/{code}/matches?dateFrom={debut}&dateTo={fin}')
    out = []
    for m in data.get('matches', []):
        st = ETATS.get(m.get('status'), 'pre')
        x = {'d': m.get('utcDate'), 'dom': nom(m.get('homeTeam')), 'ext': nom(m.get('awayTeam')), 'st': st}
        ft = ((m.get('score') or {}).get('fullTime') or {})
        if st in ('in', 'post') and ft.get('home') is not None:
            x['sd'], x['se'] = ft.get('home'), ft.get('away')
        if st == 'in' and m.get('minute'):
            x['min'] = f"{m['minute']}'"
        out.append(x)
    out.sort(key=lambda x: x['d'] or '')
    return out


def classement(code):
    data = get(f'/competitions/{code}/standings')
    tables = [s for s in data.get('standings', []) if s.get('type') == 'TOTAL'] or data.get('standings', [])
    out = []
    for t in tables[:1]:
        for e in t.get('table', []):
            out.append({'r': e.get('position'), 'eq': nom(e.get('team')), 'j': e.get('playedGames', 0),
                        'g': e.get('won', 0), 'n': e.get('draw', 0), 'p': e.get('lost', 0), 'pts': e.get('points', 0)})
    return out


def main():
    if not TOKEN:
        print('Pas de clé FOOTBALL_DATA_TOKEN : les données foot ne sont pas mises à jour.')
        return
    try:
        ancien = json.load(open(FICHIER, encoding='utf8'))
    except Exception:
        ancien = {'competitions': {}}
    nouveau = {'maj': ancien.get('maj'), 'competitions': dict(ancien.get('competitions', {}))}
    change = False
    for cid, code in COMPETITIONS.items():
        avant = ancien.get('competitions', {}).get(cid, {'matchs': [], 'classement': []})
        apres = dict(avant)
        for cle, f in (('matchs', matchs), ('classement', classement)):
            try:
                v = f(code)
                if v:
                    apres[cle] = v
            except Exception as ex:
                print(f'! {cid} {cle} : {ex}', file=sys.stderr)
        if apres != avant:
            change = True
            print(f'✓ {cid} : {len(apres.get("matchs", []))} matchs, {len(apres.get("classement", []))} équipes')
        nouveau['competitions'][cid] = apres
    if change:
        nouveau['maj'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
        json.dump(nouveau, open(FICHIER, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('foot.json', 'mis à jour' if change else 'inchangé')


if __name__ == '__main__':
    main()
