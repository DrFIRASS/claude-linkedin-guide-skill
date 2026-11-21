# Premier lancement : créer config.json

Ce fichier n'est lu que si `config.json` n'existe pas à la racine du skill. Posez les questions en une seule fois
(AskUserQuestion si l'outil existe, sinon un seul message), puis écrivez `config.json` à partir de `config.exemple.json`.

## Les questions

1. **Ton nom**, tel qu'il doit apparaître sur le guide (ex. « Marie Dupont ») → `auteur`.
2. **Ce que tu fais, en une ligne** (ex. « Marketing et IA pour les indépendants ») → `signature`.
   Facultatif : ton site ou ta page (ex. `mariedupont.fr`) → `site`, sinon chaîne vide.
3. **Où ranger les guides** sur l'ordinateur. Par défaut `~/Documents/guides-linkedin` → `dossier_guides`.
4. **La mascotte** : le skill est livré avec la mascotte de Dr. Firas, qui sert uniquement à l'exemple. Deux choix :
   - pas de mascotte (par défaut) → `mascotte: false`. Le guide reste complet, sans personnage ;
   - ta propre mascotte → l'utilisateur remplace les 3 images de `assets/mascotte/` par les siennes, PNG à fond
     transparent, avec les **mêmes noms** : `presente-joyeux.png` (couverture, personnage qui présente),
     `index-conseil.png` (encadré « Astuce », personnage qui montre du doigt), `deux-pouces.png` (page de fin) →
     `mascotte: true`. Vérifiez que les 3 fichiers sont bien remplacés avant de mettre `true`.

## Le compte Blotato

Pas de question à poser : chargez les outils Blotato avec ToolSearch, puis `blotato_list_accounts(platform: "linkedin")`.

- Aucun outil Blotato : le connecteur n'est pas installé. Donnez le lien d'installation du README
  (`https://mcp.blotato.com/mcp`) et continuez sans publication : le skill produira quand même le PDF, l'image et le texte.
- Un seul compte LinkedIn : prenez son `id`.
- Plusieurs comptes : demandez lequel (nom affiché et id). Si le compte a des pages entreprise, demandez aussi si le
  post part sur le profil ou sur une page (`pageId`), et notez-le dans `config.json` sous `blotato_linkedin_page_id`.

→ `blotato_linkedin_account_id`.

## Le mode automatique (facultatif)

Si l'utilisateur veut un post par jour sans rien faire, il duplique le modèle Notion « File des guides LinkedIn »
(lien dans le README du repository). Demandez-lui le lien de **sa copie**, faites `notion-fetch` dessus et notez l'URL
`collection://…` de la source de données → `notion_data_source`. Demandez l'heure de publication (par défaut `08:00`) et
le fuseau (par défaut `Europe/Paris`).

Ensuite, proposez de créer la tâche planifiée avec le texte de `taches-planifiees/guide-linkedin-de-la-nuit.md` du
repository (outil `create_scheduled_task` dans l'app Claude, ou commande `/schedule`).

## Exemple de config.json rempli

```json
{
  "auteur": "Marie Dupont",
  "signature": "Marketing et IA pour les indépendants",
  "site": "mariedupont.fr",
  "mascotte": false,
  "dossier_guides": "~/Documents/guides-linkedin",
  "blotato_linkedin_account_id": "12345",
  "notion_data_source": "collection://xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "heure_publication": "08:00",
  "fuseau": "Europe/Paris"
}
```

Montrez le fichier final à l'utilisateur en une ligne par valeur, puis reprenez la demande de départ.
