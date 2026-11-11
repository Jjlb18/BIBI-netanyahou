"""Met à jour la section « En ce moment » de chaque page avec les derniers titres de presse.

Lancé automatiquement par GitHub Actions (.github/workflows/actualites.yml).
Pour chaque personne de personnes.js et chaque langue, il lit le flux Google News
et remplace le contenu entre <!--NEWS-START--> et <!--NEWS-END-->.
"""
import html, os, re, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_ITEMS = 6
ZURICH = ZoneInfo('Europe/Zurich')

LANGS = {
    # langue : (dossier, paramètres Google News)
    'fr': ('', 'hl=fr&gl=CH&ceid=CH:fr'),
    'en': ('en', 'hl=en-US&gl=US&ceid=US:en'),
    'de': ('de', 'hl=de&gl=CH&ceid=CH:de'),
    'it': ('it', 'hl=it&gl=CH&ceid=CH:it'),
    'es': ('es', 'hl=es&gl=ES&ceid=ES:es'),
}
UPDATED = {
    'fr': 'Dernière mise à jour : {} (heure de Zurich) · titres de presse sélectionnés automatiquement',
    'en': 'Last updated: {} (Zurich time) · headlines selected automatically',
    'de': 'Zuletzt aktualisiert: {} (Zürcher Zeit) · Schlagzeilen automatisch ausgewählt',
    'it': 'Ultimo aggiornamento: {} (ora di Zurigo) · titoli selezionati automaticamente',
    'es': 'Última actualización: {} (hora de Zúrich) · titulares seleccionados automáticamente',
}
MONTHS = {
    'fr': ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'],
    'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'de': ['Jan.', 'Feb.', 'März', 'Apr.', 'Mai', 'Juni', 'Juli', 'Aug.', 'Sep.', 'Okt.', 'Nov.', 'Dez.'],
    'it': ['gen.', 'feb.', 'mar.', 'apr.', 'mag.', 'giu.', 'lug.', 'ago.', 'set.', 'ott.', 'nov.', 'dic.'],
    'es': ['ene.', 'feb.', 'mar.', 'abr.', 'may.', 'jun.', 'jul.', 'ago.', 'sept.', 'oct.', 'nov.', 'dic.'],
}


def short_date(dt, lang):
    m = MONTHS[lang][dt.month - 1]
    if lang == 'de':
        return f'{dt.day}. {m} {dt.year}'
    if lang == 'en':
        return f'{dt.day} {m} {dt.year}'
    return f'{dt.day} {m} {dt.year}'


def stamp(dt, lang):
    return f'{short_date(dt, lang)}, {dt:%H:%M}'


def personnes():
    """Lit personnes.js : nom, page et (facultatif) recherche de chaque personne."""
    src = open(os.path.join(ROOT, 'personnes.js'), encoding='utf8').read()
    out = []
    for block in re.findall(r'\{[^{}]*?(?:\{[^{}]*\}[^{}]*?)*\}', src.split('window.PERSONNES', 1)[1]):
        nom = re.search(r'\bnom:\s*"([^"]+)"', block)
        page = re.search(r'\bpage:\s*"([^"]+)"', block)
        q = re.search(r'\brecherche:\s*"([^"]+)"', block)
        if nom and page:
            out.append({'nom': nom.group(1), 'page': page.group(1),
                        'recherche': q.group(1) if q else nom.group(1)})
    return out


def fetch(query, params):
    url = ('https://news.google.com/rss/search?q=' +
           urllib.parse.quote(f'{query} when:3d') + '&' + params)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (actualites-bot)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def parse(xml_bytes):
    items = []
    for it in ET.fromstring(xml_bytes).iter('item'):
        title = (it.findtext('title') or '').strip()
        link = (it.findtext('link') or '').strip()
        source = (it.findtext('source') or '').strip()
        try:
            date = parsedate_to_datetime(it.findtext('pubDate') or '')
        except (TypeError, ValueError):
            continue
        if source and title.endswith(' - ' + source):
            title = title[: -len(' - ' + source)]
        if title and link:
            items.append({'title': title, 'link': link, 'source': source or 'Google News', 'date': date})
    items.sort(key=lambda x: x['date'], reverse=True)
    # pas deux fois le même titre
    seen, unique = set(), []
    for x in items:
        key = re.sub(r'\W+', '', x['title'].lower())[:60]
        if key not in seen:
            seen.add(key)
            unique.append(x)
    return unique[:MAX_ITEMS]


def render(items, lang, now):
    e = html.escape
    rows = '\n'.join(
        f'    <div class="item"><span class="d">{short_date(x["date"].astimezone(ZURICH), lang)}</span>'
        f'<div><p>{e(x["title"])}</p><a href="{e(x["link"])}" rel="noopener">{e(x["source"])}</a></div></div>'
        for x in items)
    return (f'<!--NEWS-START-->\n  <p class="updated">{UPDATED[lang].format(stamp(now, lang))}</p>\n'
            f'  <div class="news">\n{rows}\n  </div>\n  <!--NEWS-END-->')


def main():
    now = datetime.now(timezone.utc).astimezone(ZURICH)
    changed = errors = 0
    for p in personnes():
        for lang, (folder, params) in LANGS.items():
            path = os.path.join(ROOT, folder, p['page'])
            if not os.path.exists(path):
                continue
            try:
                items = parse(fetch(p['recherche'], params))
            except Exception as ex:  # réseau, flux vide…
                print(f'! {p["nom"]} [{lang}] : {ex}', file=sys.stderr)
                errors += 1
                continue
            if len(items) < 2:
                print(f'- {p["nom"]} [{lang}] : pas assez de titres, page inchangée')
                continue
            page = open(path, encoding='utf8').read()
            old = re.search(r'<!--NEWS-START-->.*?<!--NEWS-END-->', page, re.S)
            if not old:
                continue
            # rien de nouveau ? (on compare les liens, pas l'heure)
            if all(html.escape(x['link']) in old.group(0) for x in items):
                continue
            page = page[:old.start()] + render(items, lang, now) + page[old.end():]
            open(path, 'w', encoding='utf8').write(page)
            changed += 1
            print(f'✓ {p["nom"]} [{lang}] : {len(items)} titres')
    print(f'{changed} page(s) mise(s) à jour, {errors} erreur(s)')


if __name__ == '__main__':
    main()
