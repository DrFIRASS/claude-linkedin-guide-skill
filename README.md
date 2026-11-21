# Claude LinkedIn Guide Skill

**Un post LinkedIn par jour, sans rien écrire.** Ce skill Claude crée un guide PDF gratuit (lead magnet), l'image du post,
le texte du post au format « Accès GRATUIT 👇 », puis le publie ou le programme sur LinkedIn avec
[Blotato](https://blotato.com/?ref=firas).

Avec une base Notion et une tâche planifiée, Claude prend chaque nuit un sujet dans ta liste et programme le post pour
le lendemain matin.

👉 **Crée ton compte Blotato ici : [blotato.com/?ref=firas](https://blotato.com/?ref=firas)**

<p align="center">
  <img src="docs/exemple-post-linkedin.png" alt="Post LinkedIn créé et publié avec Claude : 10 206 impressions, 256 commentaires" width="560">
</p>

## Le résultat

Ce post a été **créé et publié à 100 % par Claude** avec ce skill : le guide de 35 pages, l'image, le texte et la
publication.

- **10 206 impressions, 256 commentaires, 128 réactions**
- Le post : [voir sur LinkedIn](https://lnkd.in/p/e9wrSjkV)
- Le PDF produit : [`docs/exemple-guide-marketing-claude-2026.pdf`](docs/exemple-guide-marketing-claude-2026.pdf)

Tous les posts publiés avec ce système sont sur mon profil :
**[linkedin.com/in/doctor-firass](https://www.linkedin.com/in/doctor-firass/)**. Abonne-toi pour voir ceux qui sortent chaque matin.

## Ce que fait le skill

| Étape | Ce que Claude fait | Ce que tu obtiens |
|---|---|---|
| 1. Plan | 8 à 10 chapitres et un mot-clé (ex. `MARKETING`) | Le plan du guide |
| 2. Rédaction | Deux agents écrivent les chapitres en parallèle, puis un script contrôle tout | Le contenu en JSON |
| 3. PDF | Mise en page paysage, couverture, sommaire, méthodes, prompts, workflows, checklists, plan sur 30 jours | Le PDF dans ton dossier local |
| 4. Image | La couverture dans un lecteur PDF, les miniatures, le bloc « COMMENTE « MOT-CLÉ » POUR UN ACCÈS GRATUIT → » | `image-post-linkedin.png` |
| 5. Post | Texte « Accès GRATUIT 👇 », sans demander de commenter (LinkedIn réduit la portée de ces posts) | `post-linkedin.md` |
| 6. Publication | Envoi de l'image et du texte à Blotato, publication ou programmation | Le post en ligne |

Chaque guide contient, pour 10 chapitres : 35 pages, 42 prompts prêts à copier, 10 méthodes, 10 workflows et 60 points
de contrôle. Les chiffres de la couverture sont calculés par le script : ils sont toujours vrais.

<p align="center">
  <img src="docs/image-post-exemple.png" alt="Image du post générée par le skill" width="640">
</p>

## Ce dont tu as besoin

| Outil | Pourquoi | Lien |
|---|---|---|
| **Claude Code** (terminal ou onglet Code de l'app Claude Desktop) | Le skill lance des scripts Python sur ton ordinateur | [claude.com/claude-code](https://claude.com/claude-code) |
| **Blotato** | Publie et programme le post sur LinkedIn | [blotato.com/?ref=firas](https://blotato.com/?ref=firas) |
| **Google Chrome** (ou Chromium, Edge) | Transforme la mise en page en PDF et en image | [google.com/chrome](https://www.google.com/chrome/) |
| **Python 3** | Les scripts du skill | [python.org](https://www.python.org/downloads/) |
| **Poppler** (`pdftoppm`, `pdfinfo`) | Les miniatures des pages dans l'image | voir ci-dessous |
| **Notion** (facultatif) | La file des sujets pour le mode automatique | [notion.com](https://www.notion.com/) |

Installer Poppler :

```bash
brew install poppler
```

Sur Linux : `sudo apt install poppler-utils`. Sur Windows : télécharge
[poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases) et ajoute son dossier `bin` au PATH.

## Installation

**1. Récupère le skill et copie-le dans tes skills Claude**

```bash
git clone https://github.com/DrFIRASS/claude-linkedin-guide-skill.git
```

```bash
cp -R claude-linkedin-guide-skill/post-linkedin-guide ~/.claude/skills/
```

**2. Connecte Blotato à Claude**

Crée ton compte sur [blotato.com](https://blotato.com/?ref=firas) et connecte ton compte LinkedIn dans les réglages de
Blotato. Puis, dans Claude Code :

```bash
claude mcp add --transport http Blotato https://mcp.blotato.com/mcp
```

Lance `/mcp` dans Claude Code, choisis Blotato puis « Authenticate », et redémarre Claude Code.

Dans l'app Claude Desktop, tu peux aussi l'ajouter comme connecteur personnalisé avec la même URL
`https://mcp.blotato.com/mcp` (guide officiel : [help.blotato.com/api/mcp/setup](https://help.blotato.com/api/mcp/setup)).

**3. (Facultatif) Connecte Notion** pour le mode automatique

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

**4. Lance ton premier guide**

Dans Claude Code, écris par exemple :

```text
Fais-moi un guide PDF + le post LinkedIn sur « l'automatisation avec n8n pour les débutants »
```

Au premier lancement, Claude te pose 4 questions (ton nom, ta signature, ton dossier, ta mascotte) et trouve ton compte
LinkedIn dans Blotato. Il enregistre tout dans `~/.claude/skills/post-linkedin-guide/config.json`. Ensuite, il ne
demande plus rien.

Avant de publier, Claude te montre le texte et l'image et attend ton « go ». Si tu écris « publie-le » ou
« programme-le demain à 8 h » dans ta demande, il le fait directement.

## Le système automatique : un post par jour avec Notion

C'est ce que j'utilise tous les jours. Tu ajoutes des sujets dans Notion, Claude fait le reste chaque nuit.

### 1. Duplique le modèle Notion

👉 **[Dupliquer la base « File des guides LinkedIn »](https://www.notion.so/41f3d6550fd981a88ff8cad28d66e31e)**
(bouton « Dupliquer » en haut à droite de la page)

Les colonnes de la base :

| Colonne | Type | Rempli par | Rôle |
|---|---|---|---|
| `Sujet` | Titre | Toi | Le sujet du guide, ex. « Le guide de l'automatisation avec n8n » |
| `Source` | URL | Toi (facultatif) | Un post LinkedIn ou un article qui t'inspire |
| `Consignes` | Texte | Toi (facultatif) | Public, nombre de chapitres, angle, mot-clé souhaité |
| `Statut` | Sélection | Toi, puis Claude | `À traiter` → `En cours` → `Traité` ou `Erreur` |
| `Mot-clé` | Texte | Claude | Le mot-clé choisi, ex. `N8N` |
| `Fichier PDF` | Texte | Claude | Le chemin du PDF sur ton ordinateur |
| `Lien du post` | URL | Claude | Le lien LinkedIn, ajouté après la publication |
| `Date de publication` | Date et heure | Claude | L'heure à laquelle le post est programmé |
| `ID Blotato` | Texte | Claude | L'identifiant du post programmé dans Blotato |
| `Message d'erreur` | Texte | Claude | La cause, si un sujet n'a pas pu être traité |
| `Ajouté le` | Date de création | Notion | Sert à traiter les sujets dans l'ordre |

Pour ajouter un sujet : une nouvelle ligne, un `Sujet`, le `Statut` sur `À traiter`. C'est tout.

### 2. Donne ta copie à Claude

Dans Claude Code :

```text
Configure le mode automatique du skill post-linkedin-guide avec ma base Notion : <lien de ta copie>
```

Claude enregistre la base, ton heure de publication (8 h par défaut) et ton fuseau horaire dans `config.json`.

### 3. Crée les tâches planifiées

Dans l'app Claude Desktop (onglet Code, « Tâches planifiées ») ou avec `/schedule` dans Claude Code, crée :

| Tâche | Quand | Texte à copier |
|---|---|---|
| Guide + post LinkedIn de la nuit | Chaque jour à 00 h 05 | [`taches-planifiees/guide-linkedin-de-la-nuit.md`](taches-planifiees/guide-linkedin-de-la-nuit.md) |
| Liens des posts LinkedIn (facultatif) | Chaque jour à 08 h 30 | [`taches-planifiees/liens-posts-linkedin.md`](taches-planifiees/liens-posts-linkedin.md) |

Chaque nuit, Claude prend le plus ancien sujet `À traiter`, crée le guide, l'image et le post, programme le post à 8 h
et met la ligne Notion à jour. L'ordinateur doit être allumé et l'app Claude ouverte à l'heure de la tâche.

## Envoyer le guide aux personnes qui commentent

Le PDF est enregistré dans ton dossier local (`~/Documents/guides-linkedin/<mot-clé>/` par défaut). Quand quelqu'un
commente le mot-clé, envoie-lui le PDF en pièce jointe dans un message LinkedIn, ou un lien (Google Drive, Notion,
Dropbox, ton site). Claude te donne le message tout prêt à la fin de chaque guide.

## Personnaliser

| Quoi | Où |
|---|---|
| Ton nom, ta signature, ton site | `config.json` (créé au premier lancement) |
| Ta mascotte | Remplace les 3 PNG de `post-linkedin-guide/assets/mascotte/` (mêmes noms, fond transparent) et mets `"mascotte": true` dans `config.json` |
| Les couleurs | Les variables en haut de `post-linkedin-guide/scripts/style.css` |
| Le format du post | `post-linkedin-guide/references/post-linkedin.md` |
| Le ton et les règles d'écriture | `post-linkedin-guide/references/contenu-schema.md` |

Sans mascotte, le guide reste complet : la couverture et la page de fin s'affichent sans personnage.

## Contenu du repository

```text
claude-linkedin-guide-skill/
├── README.md
├── LICENSE
├── docs/                          Exemple : capture du post, image générée, PDF complet
├── taches-planifiees/             Les textes des 2 tâches planifiées
└── post-linkedin-guide/           Le skill, à copier dans ~/.claude/skills/
    ├── SKILL.md                   Les instructions que Claude suit
    ├── config.exemple.json        Le modèle de configuration
    ├── references/                Configuration, contenu, post, publication Blotato, mode automatique
    ├── scripts/                   check_contenu.py, build_guide.py, build_image.py, commun.py, style.css
    └── assets/
        ├── exemple-marketing/     Le guide MARKETING complet (contenu JSON + post publié)
        └── mascotte/              La mascotte de l'exemple (à remplacer par la tienne)
```

## Questions fréquentes

**Ça marche sur claude.ai dans le navigateur ?** Non. Le skill lance Chrome et Python sur ton ordinateur : il faut Claude
Code (dans le terminal ou dans l'onglet Code de l'app Claude Desktop).

**Ça marche sur Windows ?** Oui : les scripts trouvent Chrome ou Edge tout seuls. Si Chrome est installé ailleurs, mets son
chemin dans la variable `CHROME_PATH`.

**Claude invente des chiffres ?** Non. Les règles du skill interdisent toute statistique ou tout résultat inventé, et un
script vérifie le contenu avant de créer le PDF. Relis quand même chaque guide avant de le partager.

**Il existe une version en anglais ?** Oui, avec le post LinkedIn en anglais : [github.com/DrFIRASS/claude-linkedin-guide-skill-en](https://github.com/DrFIRASS/claude-linkedin-guide-skill-en).

**Le post demande de commenter ?** Seulement dans l'image. Le texte ne contient jamais « commente » : LinkedIn réduit la
portée des posts qui le demandent.

## Auteur

**Dr. Firas**, IA, automatisation et contenu, expliqués simplement.

- LinkedIn : [linkedin.com/in/doctor-firass](https://www.linkedin.com/in/doctor-firass/)
- Les guides : [guide.dr-firas.vip](https://guide.dr-firas.vip)
- Blotato (lien affilié) : [blotato.com/?ref=firas](https://blotato.com/?ref=firas)

Le lien Blotato est un lien d'affiliation : si tu prends un abonnement, je touche une commission, sans surcoût pour toi.

## Licence

Code sous licence [MIT](LICENSE). La mascotte de `assets/mascotte/` appartient à Dr. Firas et n'est pas couverte par la
licence : elle sert uniquement à l'exemple.
