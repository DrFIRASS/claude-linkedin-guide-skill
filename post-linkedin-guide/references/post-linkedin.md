# Le post LinkedIn « Accès GRATUIT 👇 »

## Pourquoi ce format

LinkedIn réduit la diffusion des posts qui demandent de commenter (« commente », « écris en commentaire », « tape le
mot-clé »). Le texte ne demande donc jamais de commenter : il montre la valeur, liste ce que l'on reçoit, puis finit sur
« Accès GRATUIT ! 👇 ». L'appel « COMMENTE « MOT-CLÉ » » n'apparaît que **dans l'image**, que LinkedIn ne lit pas comme du
texte.

## Structure, dans cet ordre

1. **Hook** (2 lignes) : une action concrète à la première personne, puis le résultat chiffré, avec les vrais chiffres
   du PDF. « J'ai rassemblé dans un seul guide tout ce que je fais faire à Claude en marketing. / 10 chapitres, 42 prompts
   prêts à copier, 35 pages. »
2. **Le problème du lecteur** en 2 ou 3 lignes très courtes, puis le recadrage « Le problème n'est pas X. / C'est Y. » et
   une phrase en contraste.
3. **« Ce qui change concrètement : »** puis 4 ou 5 lignes « → », chacune avec le vrai nom d'une fonction ou d'une étape.
4. **« Ce que tu reçois : »** puis 3 ou 4 lignes « → ». La dernière est la note d'honnêteté (une limite, ce que le guide
   ne promet pas).
5. **Avant / Après** en une ligne chacun. Pas de chiffre inventé : si aucune mesure réelle n'existe, rester qualitatif.
6. **Chute** d'une ou deux lignes qui résume l'idée.
7. **Fin, toujours :**
   ```
   Accès GRATUIT ! 👇
   Reposts priorisés en priorité absolue. ♻️
   ```

## Règles

- Jamais les mots « commente », « commentaire », « écris », « tape », « like », « partage » dans le texte, ni de mot-clé
  à poster.
- Aucun lien dans le post, aucun premier commentaire : l'accès part en message privé.
- Listes « → » de 5 lignes au plus. Pas de question finale. Aucun hashtag, ou 2 au plus juste avant « Accès GRATUIT ».
- Tutoiement, phrases courtes, une idée par ligne, aucun tiret long, aucun mot marketing creux.
- Les chiffres (chapitres, prompts, pages, points de contrôle) sont ceux que renvoie `build_guide.py`.
- Longueur : 900 à 1 500 caractères. Comptez : `sed -n '3,$p' post-linkedin.md | wc -m`.

## Exemple validé et publié (guide MARKETING)

Le texte complet est dans `assets/exemple-marketing/post-linkedin.md` (1 497 caractères). Il a été publié tel quel avec
l'image du lecteur PDF, entièrement créé et publié par Claude : plus de 10 000 impressions.

## Message privé à envoyer à chaque personne qui commente

Le PDF est dans le dossier local du guide. L'utilisateur choisit comment le partager : pièce jointe dans le message
LinkedIn, ou lien (Google Drive, Notion, Dropbox, son site). Proposez les deux versions :

```text
Voici ton accès au [titre court du guide] : [lien du PDF]
Commence par le chapitre 00, il prend 10 minutes.
```

```text
Voici le [titre court du guide] en pièce jointe 👆
Commence par le chapitre 00, il prend 10 minutes.
```
