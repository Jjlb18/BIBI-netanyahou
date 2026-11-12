// Liste des personnes affichées dans le menu « Changer de personne » (en haut à droite).
// Pour ajouter quelqu'un : crée sa page dans chaque langue (par ex. macron.html, en/macron.html…) puis ajoute une entrée ici.
// La page d'accueil (index.html) affiche automatiquement toutes les personnes de cette liste.
// "categorie" : "personnalites", "jeux" ou "sport" (voir window.CATEGORIES en bas).
// "type" (pour les personnalités) : "politique", "sport", "richesse" ou "historique" (voir window.TYPES en bas).
// "recherche" (facultatif) : mots cherchés pour les actualités automatiques ; sinon le nom.
// "sigle" (facultatif) : texte court affiché dans le rond quand il n'y a pas de photo.
// "photo" (facultatif) : image carrée dans le dossier images/ ; sinon les initiales s'affichent.
window.PERSONNES = [
  {
    nom: "Benjamin Netanyahou", categorie: "personnalites", type: "politique", page: "netanyahou.html", photo: "images/netanyahou.jpg", recherche: "Netanyahu OR Netanyahou OR Netanjahu",
    noms: { en: "Benjamin Netanyahu", de: "Benjamin Netanjahu", it: "Benjamin Netanyahu", es: "Benjamín Netanyahu" },
    description: { fr: "Premier ministre d'Israël", en: "Prime Minister of Israel", de: "Ministerpräsident Israels", it: "Primo ministro d'Israele", es: "Primer ministro de Israel" }
  },
  {
    nom: "Donald Trump", categorie: "personnalites", type: "politique", page: "trump.html", photo: "images/trump.jpg",
    description: { fr: "Président des États-Unis", en: "President of the United States", de: "Präsident der USA", it: "Presidente degli Stati Uniti", es: "Presidente de Estados Unidos" }
  },
  {
    nom: "Jeffrey Epstein", categorie: "personnalites", type: "politique", page: "epstein.html", photo: "images/epstein.jpg",
    description: { fr: "Financier, condamné pour crimes sexuels", en: "Financier, convicted sex offender", de: "Finanzier, verurteilter Sexualstraftäter", it: "Finanziere, condannato per reati sessuali", es: "Financiero, condenado por delitos sexuales" }
  },
  {
    nom: "Elon Musk", categorie: "personnalites", type: "richesse", page: "musk.html", photo: "images/musk.jpg", recherche: "\"Elon Musk\"",
    description: { fr: "Patron de Tesla et SpaceX, homme le plus riche du monde", en: "Head of Tesla and SpaceX, world's richest person", de: "Chef von Tesla und SpaceX, reichster Mensch der Welt", it: "Capo di Tesla e SpaceX, l'uomo più ricco del mondo", es: "Jefe de Tesla y SpaceX, la persona más rica del mundo" }
  },
  {
    nom: "Jeff Bezos", categorie: "personnalites", type: "richesse", page: "bezos.html", photo: "images/bezos.jpg", recherche: "\"Jeff Bezos\"",
    description: { fr: "Fondateur d'Amazon et de Blue Origin", en: "Founder of Amazon and Blue Origin", de: "Gründer von Amazon und Blue Origin", it: "Fondatore di Amazon e Blue Origin", es: "Fundador de Amazon y Blue Origin" }
  },
  {
    nom: "Bernard Arnault", categorie: "personnalites", type: "richesse", page: "arnault.html", photo: "images/arnault.jpg", recherche: "\"Bernard Arnault\"",
    description: { fr: "PDG de LVMH, numéro un mondial du luxe", en: "CEO of LVMH, the world's largest luxury group", de: "Chef von LVMH, größter Luxuskonzern der Welt", it: "AD di LVMH, primo gruppo del lusso al mondo", es: "Director general de LVMH, líder mundial del lujo" }
  },
  {
    nom: "Adolf Hitler", categorie: "personnalites", type: "historique", page: "hitler.html", photo: "images/hitler.jpg", recherche: "Hitler",
    description: { fr: "Dictateur de l'Allemagne nazie (1933-1945)", en: "Dictator of Nazi Germany (1933-1945)", de: "Diktator des nationalsozialistischen Deutschlands (1933-1945)", it: "Dittatore della Germania nazista (1933-1945)", es: "Dictador de la Alemania nazi (1933-1945)" }
  },
  {
    nom: "Joseph Staline", categorie: "personnalites", type: "historique", page: "staline.html", photo: "images/staline.jpg", recherche: "Staline OR Stalin OR Stalín",
    noms: { en: "Joseph Stalin", de: "Josef Stalin", it: "Iosif Stalin", es: "Iósif Stalin" },
    description: { fr: "Dictateur de l'Union soviétique (1924-1953)", en: "Dictator of the Soviet Union (1924-1953)", de: "Diktator der Sowjetunion (1924-1953)", it: "Dittatore dell'Unione Sovietica (1924-1953)", es: "Dictador de la Unión Soviética (1924-1953)" }
  },
  {
    nom: "Benito Mussolini", categorie: "personnalites", type: "historique", page: "mussolini.html", photo: "images/mussolini.jpg", recherche: "Mussolini",
    description: { fr: "Dictateur fasciste de l'Italie (1922-1943)", en: "Fascist dictator of Italy (1922-1943)", de: "Faschistischer Diktator Italiens (1922-1943)", it: "Dittatore fascista dell'Italia (1922-1943)", es: "Dictador fascista de Italia (1922-1943)" }
  },
  {
    nom: "GTA", categorie: "jeux", page: "gta.html", sigle: "GTA", recherche: "\"GTA 6\" OR \"GTA VI\"",
    description: { fr: "Dernière version : GTA V · prochaine : GTA VI (19 novembre 2026)", en: "Latest: GTA V · next: GTA VI (19 November 2026)", de: "Neueste: GTA V · nächste: GTA VI (19. November 2026)", it: "Ultima: GTA V · prossima: GTA VI (19 novembre 2026)", es: "Última: GTA V · próxima: GTA VI (19 de noviembre de 2026)" }
  },
  {
    nom: "EA Sports FC", categorie: "jeux", page: "fc.html", sigle: "FC", recherche: "\"EA Sports FC\" OR \"FC 27\"",
    description: { fr: "Dernière version : FC 27 · prochaine : FC 28 (date ???)", en: "Latest: FC 27 · next: FC 28 (date ???)", de: "Neueste: FC 27 · nächste: FC 28 (Termin ???)", it: "Ultima: FC 27 · prossima: FC 28 (data ???)", es: "Última: FC 27 · próxima: FC 28 (fecha ???)" }
  },
  {
    nom: "Football", categorie: "sport", page: "foot.html", sigle: "⚽", recherche: "Champions League OR Premier League OR LaLiga OR Bundesliga OR Serie A OR Ligue 1",
    noms: { de: "Fußball", it: "Calcio", es: "Fútbol" },
    description: { fr: "Ligue des champions, Premier League, LaLiga, Serie A… : matchs et classements", en: "Champions League, Premier League, LaLiga, Serie A…: matches and standings", de: "Champions League, Premier League, LaLiga, Serie A …: Spiele und Tabellen", it: "Champions League, Premier League, LaLiga, Serie A…: partite e classifiche", es: "Liga de Campeones, Premier League, LaLiga, Serie A…: partidos y clasificaciones" }
  },
];

// Catégories affichées sur la page d'accueil (dans cet ordre).
window.CATEGORIES = [
  { id: "personnalites", icone: "👤", noms: { fr: "Personnalités", en: "Public figures", de: "Persönlichkeiten", it: "Personalità", es: "Personalidades" } },
  { id: "jeux",          icone: "🎮", noms: { fr: "Jeux", en: "Games", de: "Spiele", it: "Giochi", es: "Juegos" } },
  { id: "sport",         icone: "⚽", noms: { fr: "Sport", en: "Sports", de: "Sport", it: "Sport", es: "Deportes" } },
];

// Types de personnalités (sous-catégories de « Personnalités »).
window.TYPES = [
  { id: "politique",  icone: "🏛️", noms: { fr: "Politique", en: "Politics", de: "Politik", it: "Politica", es: "Política" } },
  { id: "sport",      icone: "🏅", noms: { fr: "Sport", en: "Sports", de: "Sport", it: "Sport", es: "Deporte" } },
  { id: "richesse",   icone: "💰", noms: { fr: "Richesse", en: "Wealth", de: "Reichtum", it: "Ricchezza", es: "Riqueza" } },
  { id: "historique", icone: "📜", noms: { fr: "Historique", en: "Historical", de: "Historisch", it: "Storici", es: "Históricos" } },
];
