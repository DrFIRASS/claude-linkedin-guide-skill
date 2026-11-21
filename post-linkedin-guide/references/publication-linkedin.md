# Publier le post sur LinkedIn avec Blotato

Outils du connecteur Blotato (à charger avec ToolSearch s'ils sont différés) : `blotato_list_accounts`,
`blotato_create_presigned_upload_url`, `blotato_create_post`, `blotato_get_post_status`.

Pas de compte Blotato ? Il se crée ici : https://blotato.com/?ref=firas. Le connecteur s'ajoute à Claude avec l'URL
`https://mcp.blotato.com/mcp` (détails dans le README).

## 1. Le bon compte

```
blotato_list_accounts(platform: "linkedin")
```

Utilisez `blotato_linkedin_account_id` de `config.json`, et `blotato_linkedin_page_id` s'il existe (post publié sur une
page entreprise). Si cet id n'est plus dans la liste, ne devinez pas : en mode normal, demandez lequel prendre ; en mode
automatique, arrêtez-vous avec une erreur.

## 2. Envoyer l'image

```
blotato_create_presigned_upload_url(filename: "<mot-clé>.png")
```

Puis envoyez les octets bruts du PNG (pas de JSON, pas de multipart) :

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X PUT -H "Content-Type: image/png" \
  --data-binary "@<dossier_projet>/image-post-linkedin.png" "<presignedUrl>"
curl -sI "<publicUrl>" | grep -iE "^(HTTP|content-type)"
```

Attendu : `200`, puis `200` et `image/png` sur l'URL publique.

## 3. Publier ou programmer

```
blotato_create_post(
  accountId: "<blotato_linkedin_account_id>",
  platform: "linkedin",
  text: "<texte exact de post-linkedin.md, sans la ligne de titre>",
  mediaUrls: ["<publicUrl>"]
)
```

Ajoutez `pageId` seulement si `config.json` en donne un. Sans `scheduledTime`, le post part tout de suite. Pour
programmer, passez `scheduledTime` (ISO 8601 avec le décalage horaire, ex. `2026-11-22T08:00:00+01:00`).

La réponse donne `status` et `publicUrl`. Si le statut est `in-progress`, appelez `blotato_get_post_status` (10 secondes
au moins entre deux appels) jusqu'à `published` ou `failed`. Ne relancez pas une publication qui a échoué sans comprendre
l'erreur : un second envoi risque un doublon.

## 4. Rendre compte

| Réseau | Compte | Statut | ID |
|---|---|---|---|
| LinkedIn | <nom du compte> (<id>) | Publié / Programmé à <heure> | `<postSubmissionId>` |

Donnez le `publicUrl`. Le navigateur affiche souvent la page de connexion de LinkedIn sur ce lien : dites que le statut
vient de Blotato et invitez l'utilisateur à regarder le rendu de l'image dans son fil.
