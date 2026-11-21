# Contenu du guide : schémas et brief des rédacteurs

Le dossier `contenu/` du projet contient trois sortes de fichiers. Les exemples complets sont dans
`assets/exemple-marketing/contenu/`. Copiez-les comme point de départ.

## Règles d'écriture (pour tous les fichiers)

- Tutoiement. Jamais « vous ».
- Aucun tiret long (—) ni demi-cadratin (–) : virgule, deux-points ou nouvelle phrase.
- Guillemets « » avec espaces. Espace avant : ; ? ! (le script les rend insécables).
- Aucun mot creux : incroyable, révolutionnaire, ultime, game changer, booster, scaler, synergie.
- Phrases courtes et concrètes. Chaque élément s'applique aujourd'hui, sans théorie.
- Aucune statistique, aucun résultat client, aucun chiffre d'étude inventés.
- Ne citer que des fonctions d'outils qui existent vraiment. Pour Claude (novembre 2026) : Projets (instructions et fichiers partagés par les conversations du Projet), Artifacts, recherche web et Recherche approfondie, analyse de fichiers (PDF, CSV, Excel), Skills, connecteurs (Google Drive, Gmail, Google Agenda, Notion, HubSpot, Slack…), Claude Code, tâches planifiées. Pas de nom de menu inventé.
- Jamais « [À COMPLÉTER] » : écrire `[INFO MANQUANTE]`.

## meta.json

```json
{
  "auteur": "Dr. Firas",
  "mascotte": true,
  "titre_court": "Le guide du marketing avec Claude 2026",
  "fichier_pdf": "Le guide du marketing avec Claude 2026 - Dr Firas.pdf",
  "mot_cle": "MARKETING",
  "edition": "ÉDITION 2026",
  "titre_couverture": ["Le guide complet", "du marketing", "avec *Claude*", "2026"],
  "accroche": "Méthodes, prompts prêts à copier et workflows pour faire tourner ton marketing avec Claude.",
  "mots_cote": ["STRATÉGIE", "PROMPTS", "WORKFLOWS", "CHECKLISTS"],
  "bandeau": ["Guide gratuit · par Dr. Firas", "IA, automatisation et contenu, expliqués simplement"]
}
```

- `auteur`, `mascotte` : repris de `config.json` (le nom affiché sur le guide, et `true` seulement si `assets/mascotte/` contient les 3 images de l'utilisateur).
- `titre_court` : pied de page et titre du PDF.
- `fichier_pdf` : le nom affiché en haut de l'image du post. Sans caractère spécial autre que tiret et espaces.
- `titre_couverture` : 4 lignes de 17 caractères au plus. `*mot*` passe le mot en magenta (un seul par titre).
- `accroche` : une phrase de 80 à 110 caractères.
- `mots_cote` : 4 mots courts en capitales, en haut à droite de la couverture.

## extra.json

Clés, dans l'ordre : `sommaire_00`, `sommaire_plan`, `setup_kicker`, `setup_titre`, `setup_intro`, `setup_steps`,
`setup_prompts`, `features_titre`, `features`, `plan_titre`, `plan_intro`, `plan30`, `fin_titre`, `fin_paras`,
`fin_signature`, `fin_url`, `legal`.

- **Chapitre 00 « Avant de commencer »** : la page la plus utile du guide. Elle prépare l'outil une fois pour toutes
  (pour Claude : un Projet, une fiche marque, des instructions). `setup_titre` en 2 lignes (la 2e en magenta),
  `setup_intro` en 2 ou 3 phrases, exactement 3 `setup_steps` `{t, d}`, exactement 2 `setup_prompts`
  `{title, use, prompt}` (250 à 560 caractères), 4 ou 5 `features` `{t, d}` qui expliquent les fonctions citées dans le guide.
- **Plan sur 30 jours** : `plan_titre` en 2 lignes, `plan_intro`, et `plan30` = 4 semaines
  `{t, chapitres: "Chapitres 00, 01, 02", actions: [4 actions courtes]}`. `sommaire_plan` = `{t, st}` pour la ligne du sommaire.
- **Page de fin** : `fin_titre` court (« À toi de jouer »), 3 `fin_paras`, `fin_signature` (la `signature` de `config.json`), `fin_url` (le `site` de `config.json`, ou une chaîne vide),
  `legal` : guide indépendant et gratuit, non validé par l'éditeur de l'outil, marque déposée, fonctions datées du mois en cours.

## ch01.json … chNN.json

```json
{
  "num": 1,
  "title": "Stratégie marketing",
  "subtitle": "Un plan clair sur 90 jours avant d'écrire la moindre ligne",
  "intro": "2 ou 3 phrases, 280 à 380 caractères.",
  "framework": {
    "name": "La méthode CAP 90",
    "steps": [ { "t": "Faire le constat", "d": "1 phrase, 90 à 140 caractères." } ]
  },
  "prompts": [
    { "title": "Le diagnostic express", "use": "Quand l'utiliser, moins de 90 caractères.", "prompt": "350 à 600 caractères, avec des [VARIABLES], un rôle, le contexte, le format de sortie." }
  ],
  "workflow": {
    "title": "Workflow : ton plan 90 jours dans un Projet Claude",
    "where": "Un Projet Claude + un Artifact",
    "steps": ["5 étapes, une phrase chacune, moins de 130 caractères"]
  },
  "checklist": ["6 points de contrôle, moins de 90 caractères, formulés comme des vérifications"],
  "mistake": "Erreur fréquente : 1 ou 2 phrases, moins de 220 caractères.",
  "tip": "Astuce <auteur> : 1 ou 2 phrases concrètes, moins de 220 caractères."
}
```

Quantités exactes : 4 étapes de méthode, 4 prompts, 5 étapes de workflow, 6 points de checklist.
`title` : 2 à 5 mots (il s'affiche en très gros sur 2 lignes au plus). Les longueurs comptent : au-delà, une carte déborde.

## Brief type pour un agent rédacteur

Lancez deux agents `general-purpose` en arrière-plan, dans le même message. Adaptez les crochets :

```text
Tu rédiges le contenu de 5 chapitres d'un guide PDF en français : « [TITRE DU GUIDE] », signé [AUTEUR]
([CE QUE FAIT L'AUTEUR], public de débutants curieux, entrepreneurs, freelances). Le guide est gratuit, distribué sur LinkedIn.

Tes chapitres :
[N]. [Titre] ([ce qu'il couvre, en quelques mots])
… (5 chapitres)

Écris UN fichier JSON par chapitre : [DOSSIER]/contenu/chNN.json, avec EXACTEMENT ce schéma :
[coller le schéma « ch01.json » ci-dessus, avec les quantités et les longueurs]

Règles de style (impératives) :
[coller la section « Règles d'écriture » ci-dessus]
- Varie les prompts : certains demandent à l'outil de poser d'abord des questions, d'autres de critiquer, d'autres de produire un tableau.
- JSON valide, vérifié avec python3 -c "import json;json.load(open(...))". Pas de commentaires dans le JSON.

Un autre rédacteur fait les chapitres [liste des autres chapitres et de leurs sujets] : n'empiète pas sur ces sujets.

Quand c'est fini, réponds juste avec la liste des fichiers écrits et le nom de la méthode de chacun.
```

Pour un guide en 8 chapitres, faites 2 agents de 4 chapitres. Après leur retour, lancez `check_contenu.py`.
