// Liste des personnes affichées dans le menu « Changer de personne » (en haut à droite).
// Pour ajouter quelqu'un : crée sa page dans chaque langue (par ex. macron.html, en/macron.html…) puis ajoute une entrée ici.
// La page d'accueil (index.html) affiche automatiquement toutes les personnes de cette liste.
// "categorie" : "personnalites", "jeux" ou "sport" (voir window.CATEGORIES en bas).
// "recherche" (facultatif) : mots cherchés pour les actualités automatiques ; sinon le nom.
// "sigle" (facultatif) : texte court affiché dans le rond quand il n'y a pas de photo.
// "photo" (facultatif) : image carrée dans le dossier images/ ; sinon les initiales s'affichent.
window.PERSONNES = [
  {
    nom: "Benjamin Netanyahou", categorie: "personnalites", page: "netanyahou.html", photo: "images/netanyahou.jpg", recherche: "Netanyahu OR Netanyahou OR Netanjahu",
    noms: { en: "Benjamin Netanyahu", de: "Benjamin Netanjahu", it: "Benjamin Netanyahu", es: "Benjamín Netanyahu" },
    description: { fr: "Premier ministre d'Israël", en: "Prime Minister of Israel", de: "Ministerpräsident Israels", it: "Primo ministro d'Israele", es: "Primer ministro de Israel" }
  },
  {
    nom: "Donald Trump", categorie: "personnalites", page: "trump.html", photo: "images/trump.jpg",
    description: { fr: "Président des États-Unis", en: "President of the United States", de: "Präsident der USA", it: "Presidente degli Stati Uniti", es: "Presidente de Estados Unidos" }
  },
  {
    nom: "Jeffrey Epstein", categorie: "personnalites", page: "epstein.html", photo: "images/epstein.jpg",
    description: { fr: "Financier, condamné pour crimes sexuels", en: "Financier, convicted sex offender", de: "Finanzier, verurteilter Sexualstraftäter", it: "Finanziere, condannato per reati sessuali", es: "Financiero, condenado por delitos sexuales" }
  },
  {
    nom: "GTA 6", categorie: "jeux", page: "gta6.html", sigle: "VI", recherche: "\"GTA 6\" OR \"GTA VI\"",
    description: { fr: "Rockstar Games · sortie le 19 novembre 2026", en: "Rockstar Games · out 19 November 2026", de: "Rockstar Games · erscheint am 19. November 2026", it: "Rockstar Games · esce il 19 novembre 2026", es: "Rockstar Games · sale el 19 de noviembre de 2026" }
  },
  {
    nom: "EA Sports FC 27", categorie: "jeux", page: "fc27.html", sigle: "FC", recherche: "\"EA Sports FC\" OR \"FC 27\"",
    description: { fr: "Jeu de football d'EA Sports · sorti en septembre 2026", en: "EA Sports football game · out September 2026", de: "Fußballspiel von EA Sports · erschienen im September 2026", it: "Gioco di calcio di EA Sports · uscito a settembre 2026", es: "Juego de fútbol de EA Sports · salió en septiembre de 2026" }
  },
];

// Catégories affichées sur la page d'accueil (dans cet ordre).
window.CATEGORIES = [
  { id: "personnalites", icone: "👤", noms: { fr: "Personnalités", en: "Public figures", de: "Persönlichkeiten", it: "Personalità", es: "Personalidades" } },
  { id: "jeux",          icone: "🎮", noms: { fr: "Jeux", en: "Games", de: "Spiele", it: "Giochi", es: "Juegos" } },
  { id: "sport",         icone: "⚽", noms: { fr: "Sport", en: "Sports", de: "Sport", it: "Sport", es: "Deportes" } },
];
