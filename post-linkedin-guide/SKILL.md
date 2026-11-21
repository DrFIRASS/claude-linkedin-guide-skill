---
name: post-linkedin-guide
description: "Post LinkedIn Guide : crée de bout en bout un guide PDF gratuit (lead magnet) de 8 à 10 chapitres, choisit un mot-clé, fabrique l'image du post (couverture dans un lecteur PDF, miniatures des pages, bloc « COMMENTE « MOT-CLÉ » POUR UN ACCÈS GRATUIT → »), rédige le post LinkedIn au format « Accès GRATUIT 👇 » et le publie ou le programme sur LinkedIn avec Blotato. Le PDF est enregistré dans un dossier local. Utilise ce skill dès que l'utilisateur veut un guide PDF à offrir sur LinkedIn, un lead magnet, refaire un post comme celui d'un créateur qui offre un guide en commentaire, ou dit « fais-moi un guide + le post LinkedIn », « même chose que le guide MARKETING sur un autre sujet », « traite le prochain sujet de la file Notion », même sans citer le skill."
---

# Post LinkedIn Guide

Le principe : un créateur publie « J'ai rassemblé dans un seul guide… Accès GRATUIT 👇 » avec l'aperçu d'un PDF, et envoie le
guide à chaque personne qui commente le mot-clé. Ce skill fait tout le travail, dans cet ordre :

1. le contenu du guide (8 à 10 chapitres) ;
2. le PDF, enregistré dans le dossier local du guide ;
3. l'image du post ;
4. le texte du post LinkedIn ;
5. la publication (ou la programmation) sur LinkedIn avec Blotato.

Le guide de référence est le guide **MARKETING** (« Le guide complet du marketing avec Claude 2026 », 35 pages,
10 chapitres, 42 prompts), dans `assets/exemple-marketing/`. C'est la référence de qualité et de ton.

## Avant tout : la configuration

Lisez `config.json` à la racine de ce skill. S'il n'existe pas, c'est le premier lancement : suivez
`references/premiere-configuration.md` (4 questions, puis création de `config.json`). En mode automatique, ne posez
aucune question : si `config.json` manque, arrêtez-vous et dites-le.

Valeurs utilisées partout :
- `auteur` : le nom affiché sur le guide (couverture, pied de page, « Astuce <auteur> », signature) ;
- `signature`, `site` : la page de fin du PDF (`site` peut rester vide) ;
- `mascotte` : `true` seulement si l'utilisateur a mis ses 3 images dans `assets/mascotte/` (voir la configuration) ;
- `dossier_guides` : où ranger chaque guide ;
- `blotato_linkedin_account_id` : le compte LinkedIn à utiliser dans Blotato ;
- `notion_data_source`, `heure_publication`, `fuseau` : le mode automatique.

## Règles d'écriture

- Ton direct. Jamais de tiret long (—) ni de demi-cadratin (–), ni de formule creuse.
- Le PDF et le post **tutoient** le lecteur.
- Rien d'inventé : aucune statistique, aucun résultat client, aucun « +230 % ». Les chiffres de la couverture sont
  calculés par le script, donc toujours vrais. Une fonction d'un outil n'est citée que si elle existe ; vérifiez ce qui
  peut vieillir (offres, menus, prix).
- Pas de logo ni de marque d'un tiers (Anthropic, OpenAI…) en couverture : le guide est signé par l'auteur. La dernière
  page dit que le guide est indépendant.
- Préférer les agents en parallèle pour rédiger les chapitres.
- Ne jamais écrire « [À COMPLÉTER] » : pour une info manquante dans un prompt, écrire `[INFO MANQUANTE]`.

## Déroulé

### 0. Cadrer (une seule question si besoin)

Il faut : le **sujet** (ex. « le marketing avec Claude »), le **public** (par défaut : débutants curieux, entrepreneurs,
freelances) et, s'il y en a un, le **post de référence** à imiter. Si le sujet est clair, ne demandez rien.

Créez le dossier projet `<dossier_guides>/<mot-clé en minuscules>/` (développez le `~`), avec un sous-dossier `contenu/`.

### 1. Plan et mot-clé

Choisissez 8 à 10 chapitres qui couvrent le sujet sans se recouper, et le **mot-clé** : un mot court, facile à dire et à
taper, 2 à 30 majuscules ou chiffres, sans accent (ex. `MARKETING`). Vérifiez qu'il n'existe pas déjà un dossier de ce
nom dans `dossier_guides`.

Rédigez vous-même `contenu/meta.json` (avec `auteur` et `mascotte` repris de `config.json`) et `contenu/extra.json`
(chapitre 00, plan sur 30 jours, page de fin). Schémas et exemple : `references/contenu-schema.md`.

### 2. Rédiger les chapitres en parallèle

Lancez **deux agents en arrière-plan** (chapitres 1 à 5, puis 6 à 10), chacun avec le brief type de
`references/contenu-schema.md`. Pendant ce temps, écrivez `meta.json` et `extra.json`. Ensuite :

```bash
python3 <skill>/scripts/check_contenu.py <dossier_projet>
```

Corrigez chaque problème signalé (dans les JSON), puis relancez jusqu'à « Contenu valide ».

### 3. Générer le PDF

```bash
python3 <skill>/scripts/build_guide.py <dossier_projet>
```

Il écrit `guide.html` et le PDF (nom dans `meta.fichier_pdf`) dans le dossier projet, au format paysage 1280 × 960 :
couverture, sommaire, chapitre 00, 3 pages par chapitre (méthode, 4 prompts, workflow + checklist), plan sur 30 jours,
page de fin. Avec 10 chapitres : 35 pages.

**Regardez le résultat** avant d'aller plus loin. Rendez les pages en PNG (`pdftoppm -r 60 -png <pdf> <dossier>/apercu/p`)
et regardez-les. Points à contrôler : titre de couverture qui ne touche pas la forme rose, aucune carte de prompt qui
déborde, aucun texte en minuscule après « Erreur fréquente » ou « Workflow ». Corrigez le contenu plutôt que la feuille
de style quand c'est possible.

Le PDF reste dans le dossier projet : c'est le fichier que l'utilisateur enverra (ou déposera sur Google Drive, Notion,
son site…) aux personnes qui commentent.

### 4. Fabriquer l'image du post

```bash
python3 <skill>/scripts/build_image.py <dossier_projet>
```

Elle écrit `image-post-linkedin.png` (2560 × 1920) : un lecteur PDF (barre avec le nom du fichier, « 1 / N », zoom,
icônes), la colonne de miniatures des pages 1 à 7, la couverture au centre, et tout en bas le bloc dégradé
« COMMENTE « MOT-CLÉ » POUR UN ACCÈS GRATUIT → » sur une seule ligne.

Ouvrez l'image et vérifiez que le texte du bloc tient sur une ligne. Pour un mot-clé long, le script réduit la police ;
si ça ne suffit pas, raccourcissez le mot-clé plutôt que de couper la phrase.

Le mot « commente » ne doit figurer **que dans l'image**, jamais dans le texte du post : LinkedIn réduit la portée des
posts qui demandent de commenter.

### 5. Rédiger le post LinkedIn

Format « Accès GRATUIT 👇 », règles complètes et exemple validé dans `references/post-linkedin.md`. Visez 900 à 1 500
caractères (comptez-les). Enregistrez-le dans `<dossier_projet>/post-linkedin.md`.

### 6. Publier sur LinkedIn avec Blotato

Procédure exacte dans `references/publication-linkedin.md` : compte `blotato_linkedin_account_id`, image envoyée par URL
présignée, `blotato_create_post`, puis lien du post.

Publier sur LinkedIn est public et difficile à rattraper. Si la demande de l'utilisateur dit déjà de publier
(« poste-le maintenant », « publie-le », « programme-le demain à 8 h »), faites-le. Sinon, montrez le texte final et
l'image, et demandez un seul « go ».

### Mode automatique (tâche planifiée et file Notion)

Quand le skill est lancé par une tâche planifiée, ou quand l'utilisateur demande de « traiter la file » ou « le prochain
sujet de la liste », lisez `references/mode-automatique.md` : le sujet vient de la base Notion (`notion_data_source`),
rien n'est demandé, le post est **programmé** à `heure_publication` (pas publié tout de suite), et la ligne Notion passe
en « Traité » avec le mot-clé, le chemin du PDF et la date, ou en « Erreur » avec la raison.

### 7. Conclure

Donnez à l'utilisateur :
- le chemin du PDF et de l'image (envoyez-les avec SendUserFile si l'outil existe) ;
- le mot-clé ;
- le texte du post et le lien LinkedIn s'il est publié ;
- le **message privé** à envoyer à chaque personne qui commente (modèle dans `references/post-linkedin.md`) ;
- ce qui n'a pas pu être vérifié (une fonction d'outil, un chiffre).

## Fichiers du skill

| Fichier | Rôle |
|---|---|
| `config.exemple.json` | Modèle de configuration, copié en `config.json` au premier lancement |
| `scripts/check_contenu.py` | Valide les JSON : schéma, longueurs qui tiennent dans la mise en page, mots et signes interdits |
| `scripts/build_guide.py` | Génère `guide.html` puis le PDF avec Chrome headless |
| `scripts/build_image.py` | Génère l'image du post (lecteur PDF + bloc « Commente ») |
| `scripts/commun.py` | Configuration, recherche de Chrome (macOS, Windows, Linux) |
| `scripts/style.css` | La charte : magenta `#CB3672`, violet `#8747A1`, corail `#EEA39C`, encre `#131325`, Archivo + IBM Plex |
| `assets/mascotte/` | 3 images de mascotte (celles de Dr. Firas pour l'exemple ; à remplacer par les tiennes) |
| `assets/exemple-marketing/` | Le guide MARKETING complet : `contenu/*.json` et `post-linkedin.md` |
| `references/premiere-configuration.md` | Premier lancement : questions et création de `config.json` |
| `references/contenu-schema.md` | Schémas JSON, règles d'écriture, brief des agents rédacteurs |
| `references/post-linkedin.md` | Format du post, exemple validé, message privé |
| `references/publication-linkedin.md` | Publication Blotato pas à pas |
| `references/mode-automatique.md` | File Notion, tâche planifiée, programmation, gestion des erreurs |

Outils nécessaires : Google Chrome (ou Chromium, Edge), `pdftoppm` et `pdfinfo` (paquet poppler), Python 3.

## Pièges déjà rencontrés

- **Texte en dégradé** (`background-clip: text`) : Chrome dessine un cadre parasite autour dans le PDF. La charte utilise
  du magenta plein pour les mots mis en avant.
- **Titre de couverture** trop long : il déborde sur la forme rose. 17 caractères au plus par ligne, 4 lignes (le
  contrôle le vérifie).
- **Classes CSS** : l'image réutilise `style.css`, qui définit déjà `.side` et `.next`. Les classes du lecteur commencent
  donc par `v` (`.vside`, `.vnext`…). À garder si vous modifiez le script.
- **Polices** : elles viennent de Google Fonts. Sans connexion internet, Chrome prend une police de secours et la mise en
  page bouge.
- **Commande `rm` avec une variable** : écrire `"${VAR:?}"/*.png`, jamais `$VAR/*.png`.
- **LinkedIn** : la page du post demande une connexion dans le navigateur. Le statut « published » et le `publicUrl`
  renvoyés par Blotato font foi ; dites-le à l'utilisateur.
