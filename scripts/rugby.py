"""Met à jour data/rugby.json : matchs et classements des grandes compétitions de rugby.

Lancé par GitHub Actions (.github/workflows/actualites.yml), mais ne contacte la source
qu'une fois toutes les 3 heures (l'offre gratuite autorise 100 requêtes par jour).
Source : api-sports.io (API Rugby). La clé doit être enregistrée dans le dépôt GitHub
comme secret nommé RUGBY_API_KEY (Settings → Secrets and variables → Actions).
Si la clé manque ou qu'une compétition ne répond pas, les anciennes données sont gardées.
"""
import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHIER = os.path.join(ROOT, 'data', 'rugby.json')
API = 'https://v1.rugby.api-sports.io'
KEY = os.environ.get('RUGBY_API_KEY', '').strip()
INTERVALLE = timedelta(hours=3)
JOURS_AVANT, JOURS_APRES = 14, 28

# id sur le site : (mots cherchés, pays attendu ou None)
COMPETITIONS = {
    'top14': ('Top 14', 'France'),
    'prem': ('Premiership Rugby', 'England'),
    'urc': ('United Rugby Championship', None),
    'ercc': ('Champions Cup', None),
    'six': ('Six Nations', None),
}

ETATS_FIN = {'FT', 'AET', 'AW', 'AOT'}
ETATS_LIVE = {'1H', '2H', 'HT', 'ET', 'BT', 'PT', 'LIVE'}
ETATS_ANNULE = {'PST', 'CANC', 'ABD', 'INTR', 'SUSP'}


def get(path, **params):
    url = API + path + ('?' + urllib.parse.urlencode(params) if params else '')
    req = urllib.request.Request(url, headers={'x-apisports-key': KEY})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get('errors'):
        raise RuntimeError(data['errors'])
    time.sleep(2)
    return data.get('response', [])


def trouver(nom, pays):
    """Trouve l'identifiant de la compétition et sa saison en cours."""
    res = get('/leagues', search=nom)
    def score(l):
        n = (l.get('name') or '').lower()
        c = ((l.get('country') or {}).get('name') or '')
        return (n == nom.lower(), nom.lower() in n, pays is None or c == pays)
    res.sort(key=score, reverse=True)
    if not res:
        raise RuntimeError(f'compétition introuvable : {nom}')
    l = res[0]
    saisons = l.get('seasons') or []
    cur = [s for s in saisons if s.get('current')] or saisons[-1:]
    return {'id': l.get('id'), 'saison': (cur[0] if cur else {}).get('season')}


def matchs(info):
    now = datetime.now(timezone.utc)
    out = []
    for g in get('/games', league=info['id'], season=info['saison']):
        try:
            d = datetime.fromisoformat((g.get('date') or '').replace('Z', '+00:00'))
        except ValueError:
            continue
        if not (now - timedelta(days=JOURS_AVANT) <= d <= now + timedelta(days=JOURS_APRES)):
            continue
        st = ((g.get('status') or {}).get('short') or 'NS').upper()
        etat = 'post' if st in ETATS_FIN else 'in' if st in ETATS_LIVE else 'annule' if st in ETATS_ANNULE else 'pre'
        t = g.get('teams') or {}
        sc = g.get('scores') or {}
        m = {'d': d.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z'),
             'dom': (t.get('home') or {}).get('name', '?'), 'ext': (t.get('away') or {}).get('name', '?'), 'st': etat}
        if etat in ('in', 'post') and sc.get('home') is not None:
            m['sd'], m['se'] = sc.get('home'), sc.get('away')
        if etat == 'in':
            m['min'] = st
        out.append(m)
    out.sort(key=lambda x: x['d'])
    return out


def classement(info):
    res = get('/standings', league=info['id'], season=info['saison'])
    groupes = res if (res and isinstance(res[0], list)) else [res]
    out = []
    for grp in groupes:
        for e in grp:
            g = e.get('games') or {}
            v = lambda k: ((g.get(k) or {}).get('total') or 0)
            x = {'r': e.get('position'), 'eq': (e.get('team') or {}).get('name', '?'), 'j': g.get('played', 0),
                 'g': v('win'), 'n': v('draw'), 'p': v('lose'), 'pts': e.get('points', 0)}
            if len(groupes) > 1:
                x['grp'] = e.get('group', {}).get('name') if isinstance(e.get('group'), dict) else e.get('group')
            out.append(x)
    return out


def main():
    if not KEY:
        print('Pas de clé RUGBY_API_KEY : les données rugby ne sont pas mises à jour.')
        return
    try:
        ancien = json.load(open(FICHIER, encoding='utf8'))
    except Exception:
        ancien = {'competitions': {}}
    now = datetime.now(timezone.utc)
    dernier = ancien.get('essai')
    if dernier and now - datetime.fromisoformat(dernier) < INTERVALLE and os.environ.get('FORCER') != '1':
        print('Rugby : dernière mise à jour il y a moins de 3 h, rien à faire.')
        return
    nouveau = {'maj': ancien.get('maj'), 'essai': now.isoformat(timespec='seconds'),
               'ids': ancien.get('ids', {}), 'competitions': dict(ancien.get('competitions', {}))}
    change = False
    for cid, (nom, pays) in COMPETITIONS.items():
        avant = ancien.get('competitions', {}).get(cid, {'matchs': [], 'classement': []})
        apres = dict(avant)
        try:
            info = nouveau['ids'].get(cid)
            if not info or not info.get('saison') or now.weekday() == 0 and now.hour < 3:
                info = trouver(nom, pays)  # recherché au début et chaque lundi (changement de saison)
                nouveau['ids'][cid] = info
            for cle, f in (('matchs', matchs), ('classement', classement)):
                try:
                    v = f(info)
                    if v or cle == 'matchs':
                        apres[cle] = v
                except Exception as ex:
                    print(f'! {cid} {cle} : {ex}', file=sys.stderr)
        except Exception as ex:
            print(f'! {cid} : {ex}', file=sys.stderr)
        if apres != avant:
            change = True
            print(f'✓ {cid} : {len(apres.get("matchs", []))} matchs, {len(apres.get("classement", []))} équipes')
        nouveau['competitions'][cid] = apres
    if change:
        nouveau['maj'] = now.isoformat(timespec='seconds')
    json.dump(nouveau, open(FICHIER, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('rugby.json', 'mis à jour' if change else 'inchangé')


if __name__ == '__main__':
    main()
