"""Met à jour data/hockey.json : matchs (résultats, en direct, à venir) et classement de la NHL.

Lancé automatiquement par GitHub Actions (.github/workflows/actualites.yml).
Source : l'API publique de la NHL (api-web.nhle.com), gratuite et sans clé.
Si l'API ne répond pas, les anciennes données sont gardées.
"""
import json, os, sys, time, urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHIER = os.path.join(ROOT, 'data', 'hockey.json')
API = 'https://api-web.nhle.com/v1'
UA = 'PortraitsEnDirect/1.0 (+https://github.com/Jjlb18/BIBI-netanyahou)'

ETATS = {'FUT': 'pre', 'PRE': 'pre', 'LIVE': 'in', 'CRIT': 'in', 'FINAL': 'post', 'OFF': 'post'}


def get(path):
    req = urllib.request.Request(API + path, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    time.sleep(1)
    return data


def txt(v):
    if isinstance(v, dict):
        return v.get('fr') or v.get('default') or ''
    return v or ''


def equipe(t):
    nom = ' '.join(x for x in (txt(t.get('placeName')), txt(t.get('commonName'))) if x) or txt(t.get('name')) or t.get('abbrev', '')
    return {'nom': nom, 'abrev': t.get('abbrev', ''), 'logo': t.get('logo', ''), 'score': t.get('score')}


def matchs(date):
    out = []
    for jour in get(f'/schedule/{date}').get('gameWeek', []):
        for g in jour.get('games', []):
            if g.get('gameType') not in (1, 2, 3):
                continue
            etat = ETATS.get(g.get('gameState'), 'pre')
            if g.get('gameScheduleState') in ('PPD', 'CNCL', 'SUSP'):
                etat = 'annule'
            fin = (g.get('periodDescriptor') or {}).get('periodType', '')
            out.append({'id': g.get('id'), 'date': g.get('startTimeUTC'), 'etat': etat,
                        'dom': equipe(g.get('homeTeam', {})), 'ext': equipe(g.get('awayTeam', {})),
                        'fin': fin if fin in ('OT', 'SO') else ''})
    return out


def main():
    try:
        ancien = json.load(open(FICHIER, encoding='utf8'))
    except Exception:
        ancien = {}
    maint = datetime.now(timezone.utc)
    try:
        jeux = {}
        for d in (maint - timedelta(days=7), maint):
            for m in matchs(d.strftime('%Y-%m-%d')):
                jeux[m['id']] = m
        jeux = sorted(jeux.values(), key=lambda m: m['date'] or '')
        recents = [m for m in jeux if m['etat'] in ('post', 'in')][-10:][::-1]
        avenir = [m for m in jeux if m['etat'] == 'pre'][:10]
        classement = []
        for i, t in enumerate(get('/standings/now').get('standings', []), 1):
            classement.append({'nom': txt(t.get('teamName')), 'abrev': txt(t.get('teamAbbrev')), 'logo': t.get('teamLogo', ''),
                               'conf': t.get('conferenceName', ''), 'div': t.get('divisionName', ''),
                               'mj': t.get('gamesPlayed', 0), 'v': t.get('wins', 0), 'd': t.get('losses', 0),
                               'dp': t.get('otLosses', 0), 'pts': t.get('points', 0),
                               'bp': t.get('goalFor', 0), 'bc': t.get('goalAgainst', 0)})
        if not classement and not jeux:
            raise ValueError('réponse vide')
        data = {'maj': maint.isoformat(timespec='seconds'), 'recents': recents, 'avenir': avenir, 'classement': classement}
    except Exception as e:  # on garde les anciennes données
        print('Hockey : erreur, anciennes données gardées :', e, file=sys.stderr)
        return
    # on n'écrit que si le contenu a changé (hors date de mise à jour)
    if {k: v for k, v in ancien.items() if k != 'maj'} == {k: v for k, v in data.items() if k != 'maj'}:
        print('Hockey : rien de nouveau.')
        return
    os.makedirs(os.path.dirname(FICHIER), exist_ok=True)
    json.dump(data, open(FICHIER, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'Hockey : {len(recents)} résultats, {len(avenir)} à venir, {len(classement)} équipes.')


if __name__ == '__main__':
    main()
