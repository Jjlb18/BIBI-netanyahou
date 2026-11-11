// Liste des personnes affichées dans le menu « Changer de personne » (en haut à droite).
// Pour ajouter quelqu'un : crée sa page dans chaque langue (par ex. macron.html, en/macron.html…) puis ajoute une entrée ici.
// La page d'accueil (index.html) affiche automatiquement toutes les personnes de cette liste.
// "recherche" (facultatif) : mots cherchés pour les actualités automatiques ; sinon le nom.
// "photo" (facultatif) : image carrée dans le dossier images/ ; sinon les initiales s'affichent.
window.PERSONNES = [
  {
    nom: "Benjamin Netanyahou", page: "netanyahou.html", photo: "images/netanyahou.jpg", recherche: "Netanyahu OR Netanyahou OR Netanjahu",
    noms: { en: "Benjamin Netanyahu", de: "Benjamin Netanjahu", it: "Benjamin Netanyahu", es: "Benjamín Netanyahu" },
    description: { fr: "Premier ministre d'Israël", en: "Prime Minister of Israel", de: "Ministerpräsident Israels", it: "Primo ministro d'Israele", es: "Primer ministro de Israel" }
  },
  {
    nom: "Donald Trump", page: "trump.html", photo: "images/trump.jpg",
    description: { fr: "Président des États-Unis", en: "President of the United States", de: "Präsident der USA", it: "Presidente degli Stati Uniti", es: "Presidente de Estados Unidos" }
  },
  {
    nom: "Jeffrey Epstein", page: "epstein.html", photo: "images/epstein.jpg",
    description: { fr: "Financier, condamné pour crimes sexuels", en: "Financier, convicted sex offender", de: "Finanzier, verurteilter Sexualstraftäter", it: "Finanziere, condannato per reati sessuali", es: "Financiero, condenado por delitos sexuales" }
  },
];
