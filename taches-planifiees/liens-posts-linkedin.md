# Tâche planifiée : « Liens des posts LinkedIn »

Facultative. Elle remplit la colonne « Lien du post » de Notion une fois le post publié.

- **Nom** : Liens des posts LinkedIn
- **Fréquence** : tous les jours, 30 minutes après ton heure de publication (ex. 08 h 30)
- **Texte de la tâche** :

```text
Tâche courte et sans question.

1. Lis le config.json du skill post-linkedin-guide (dans ~/.claude/skills/post-linkedin-guide/). Charge avec ToolSearch les outils Notion (notion-query-data-sources, notion-update-page) et Blotato (blotato_get_post_status).
2. Dans la source Notion notion_data_source de config.json, trouve les lignes dont « Statut » = « Traité », « ID Blotato » non vide et « Lien du post » vide.
3. Pour chacune, appelle blotato_get_post_status avec postSubmissionId = « ID Blotato » (10 secondes au moins entre deux appels) :
   - statut « published » : mets « Lien du post » = le publicUrl renvoyé ;
   - statut « scheduled » ou « in-progress » : ne change rien ;
   - statut « failed » : mets « Statut » = « Erreur » et « Message d'erreur » = « Publication LinkedIn échouée : » suivi du message de Blotato.
4. Ne publie, ne programme et ne supprime aucun post. Ne touche à aucune autre colonne.

Termine par un compte rendu d'une à trois lignes : liens ajoutés, posts encore programmés, échecs.
```
