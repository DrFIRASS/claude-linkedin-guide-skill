#!/usr/bin/env python3
"""Génère le guide PDF (charte magenta et violet, nom de l'auteur pris dans meta.json ou config.json).

Usage : python3 build_guide.py <dossier_projet>

Le dossier projet contient contenu/meta.json, contenu/extra.json et contenu/ch01.json … chNN.json
(schéma : references/contenu-schema.md). Le script écrit <dossier>/guide.html puis le PDF
<dossier>/<meta.fichier_pdf>, au format 1280 x 960 px par page, avec Chrome headless.
Les chiffres de la couverture (chapitres, prompts, méthodes, workflows, points de contrôle)
sont calculés à partir du contenu : ils sont toujours vrais.
"""
import json, glob, html, re, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import SKILL, trouver_chrome, uri, reglages

if len(sys.argv) != 2:
    sys.exit("Usage : python3 build_guide.py <dossier_projet>")
ICI = os.path.abspath(sys.argv[1])
C = os.path.join(ICI, "contenu")

meta = json.load(open(os.path.join(C, "meta.json"), encoding="utf-8"))
extra = json.load(open(os.path.join(C, "extra.json"), encoding="utf-8"))
chapitres = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(C, "ch*.json")))]
chapitres.sort(key=lambda c: c["num"])
TITRE_GUIDE = meta["titre_court"]
AUTEUR, MASCOTTE_ON, MASCOTTE = reglages(meta)


def e(s):
    return html.escape(s, quote=False)


def nbsp(s):
    # typographie française : espace insécable avant : ; ? ! et dans « »
    s = re.sub(r" ([:;?!»])", " \\1", s)
    return s.replace("« ", "« ")


def t(s):
    return nbsp(e(s))


def accent(s):
    # *mot* devient le mot en magenta
    return re.sub(r"\*([^*]+)\*", r'<span class="grad">\1</span>', t(s))


def prompt_html(p):
    s = re.sub(r"(\[[^\]]+\])", r'<span class="var">\1</span>', t(p))
    return s.replace("\n", "<br>")


def masc(nom, classe=""):
    # sans mascotte (mascotte: false), l'image est simplement absente
    if not MASCOTTE_ON:
        return ""
    c = f' class="{classe}"' if classe else ""
    return f'<img{c} src="{uri(os.path.join(MASCOTTE, nom + ".png"))}">'


def deux_lignes(lignes):
    return f'{t(lignes[0])}<br><span class="grad">{t(lignes[1])}</span>'


pages, num_page = [], [0]


def footer(chap=None):
    num_page[0] += 1
    gauche = f"Chapitre {chap:02d}" if chap else t(AUTEUR)
    return f"""<div class="foot"><span class="fl"><b>{gauche}</b> · {t(TITRE_GUIDE)}</span>
<span class="fr">{num_page[0]:02d}</span></div>"""


# ---------- Couverture ----------
nb_prompts = sum(len(c["prompts"]) for c in chapitres) + len(extra["setup_prompts"])
nb_check = sum(len(c["checklist"]) for c in chapitres)
moitie = (len(chapitres) + 1) // 2
li = lambda cs: "".join(f'<li><span class="n">{c["num"]:02d}</span><span class="tt">{t(c["title"])}</span></li>' for c in cs)
num_page[0] += 1
pages.append(f"""
<section class="page cover">
  <div class="blob"></div>
  {masc('presente-joyeux', 'masc')}
  <div class="brand"><span class="dot"></span>{t(AUTEUR)}</div>
  <div class="side">{'<br>'.join(t(m) for m in meta['mots_cote'])}</div>
  <div class="pill">{t(meta['edition'])}</div>
  <h1>{'<br>'.join(accent(l) for l in meta['titre_couverture'])}</h1>
  <div class="rule"></div>
  <p class="lead">{t(meta['accroche'])}</p>
  <div class="stats">
    <div><b>{len(chapitres)}</b><span>chapitres</span></div>
    <div><b>{nb_prompts}</b><span>prompts</span></div>
    <div><b>{len(chapitres)}</b><span>méthodes</span></div>
    <div><b>{len(chapitres)}</b><span>workflows</span></div>
    <div><b>{nb_check}</b><span>points de contrôle</span></div>
  </div>
  <div class="toc"><ol>{li(chapitres[:moitie])}</ol><ol>{li(chapitres[moitie:])}</ol></div>
  <div class="band"><span>{t(meta['bandeau'][0])}</span><span>{t(meta['bandeau'][1])}</span></div>
</section>""")

# ---------- Sommaire ----------
p = 3
lignes = [("00", extra["sommaire_00"]["t"], extra["sommaire_00"]["st"], p)]
p += 1
for c in chapitres:
    lignes.append((f'{c["num"]:02d}', c["title"], c["subtitle"], p))
    p += 3
lignes.append(("+", extra["sommaire_plan"]["t"], extra["sommaire_plan"]["st"], p))
somm = "".join(
    f'<div class="sl"><span class="sn">{n}</span><div><b>{t(ti)}</b><small>{t(st)}</small></div><span class="dots"></span><span class="sp">{pg:02d}</span></div>'
    for n, ti, st, pg in lignes)
pages.append(f"""
<section class="page sommaire">
  <div class="kick">SOMMAIRE</div>
  <h2>Ce que tu vas<br><span class="grad">mettre en place</span></h2>
  <div class="slist">{somm}</div>
  <div class="howto">
    <div class="ht"><b>Comment lire ce guide</b>Chaque chapitre tient en 3 pages : une méthode, 4 prompts prêts à copier, un workflow et sa checklist.</div>
    <div class="ht"><b>Les [CROCHETS]</b>Dans chaque prompt, remplace le texte entre crochets par tes informations avant de l'envoyer.</div>
    <div class="ht"><b>Dans l'ordre ou pas</b>Commence par la page 03, puis va directement au chapitre qui règle ton problème du moment.</div>
  </div>
  {footer()}
</section>""")

# ---------- Chapitre 00 : préparation ----------
setup_steps = "".join(
    f'<div class="ss"><span class="num">{i+1}</span><div><b>{t(s["t"])}</b><p>{t(s["d"])}</p></div></div>'
    for i, s in enumerate(extra["setup_steps"]))
setup_prompts = "".join(
    f'<div class="pcard"><div class="ph"><b>{t(sp["title"])}</b><small>{t(sp["use"])}</small></div><div class="pbody">{prompt_html(sp["prompt"])}</div></div>'
    for sp in extra["setup_prompts"])
feats = "".join(f'<div class="feat"><b>{t(f["t"])}</b><span>{t(f["d"])}</span></div>' for f in extra["features"])
pages.append(f"""
<section class="page setup">
  <div class="kick">{t(extra['setup_kicker'])}</div>
  <h2>{deux_lignes(extra['setup_titre'])}</h2>
  <p class="intro">{t(extra["setup_intro"])}</p>
  <div class="setgrid">
    <div class="steps3">{setup_steps}<div class="feats"><div class="fk">{t(extra['features_titre'])}</div>{feats}</div></div>
    <div class="sprompts">{setup_prompts}</div>
  </div>
  {footer()}
</section>""")

# ---------- Chapitres : ouverture, prompts, workflow ----------
cap = lambda s: s[:1].upper() + s[1:]
for c in chapitres:
    n = c["num"]
    steps = "".join(
        f'<div class="fs"><span class="num">{i+1}</span><b>{t(s["t"])}</b><p>{t(s["d"])}</p></div>'
        for i, s in enumerate(c["framework"]["steps"]))
    mistake = cap(re.sub(r"^Erreur fréquente\s*:\s*", "", c["mistake"]))
    tip = cap(re.sub(r"^Astuce[^:]{0,40}:\s*", "", c["tip"]))
    pages.append(f"""
<section class="page chap">
  <div class="hero">
    <div class="bignum">{n:02d}</div>
    <div class="htxt"><div class="kick w">CHAPITRE {n:02d}</div>
    <h2>{t(c["title"])}</h2><p class="sub">{t(c["subtitle"])}</p></div>
  </div>
  <p class="intro">{t(c["intro"])}</p>
  <div class="fwname"><span class="kick">LA MÉTHODE</span><h3>{t(c["framework"]["name"])}</h3></div>
  <div class="fsteps">{steps}</div>
  <div class="duo">
    <div class="warn"><div class="tag r">ERREUR FRÉQUENTE</div><p>{t(mistake)}</p></div>
    <div class="tip{'' if MASCOTTE_ON else ' nomasc'}">{masc('index-conseil')}<div><div class="tag v">ASTUCE {t(AUTEUR).upper()}</div><p>{t(tip)}</p></div></div>
  </div>
  {footer(n)}
</section>""")

    cards = "".join(
        f'<div class="pcard"><div class="ph"><span class="pn">P{n}.{i+1}</span><div><b>{t(pr["title"])}</b><small>{t(pr["use"])}</small></div></div><div class="pbody">{prompt_html(pr["prompt"])}</div></div>'
        for i, pr in enumerate(c["prompts"]))
    pages.append(f"""
<section class="page prompts">
  <div class="phead"><div class="kick">CHAPITRE {n:02d} · {t(c["title"]).upper()}</div>
  <h2>{len(c["prompts"])} prompts <span class="grad">prêts à copier</span></h2></div>
  <div class="pgrid">{cards}</div>
  {footer(n)}
</section>""")

    wsteps = "".join(f'<li><span class="num">{i+1}</span><p>{t(s)}</p></li>' for i, s in enumerate(c["workflow"]["steps"]))
    checks = "".join(f'<li><span class="box"></span><p>{t(s)}</p></li>' for s in c["checklist"])
    wtitle = cap(re.sub(r"^Workflow\s*:\s*", "", c["workflow"]["title"]))
    suivant = next((x for x in chapitres if x["num"] == n + 1), None)
    nxt = (f'Chapitre suivant : <b>{t(suivant["title"])}</b> →' if suivant
           else f"Dernière étape : <b>{t(extra['sommaire_plan']['t'][:1].lower() + extra['sommaire_plan']['t'][1:])}</b> →")
    pages.append(f"""
<section class="page wf">
  <div class="phead"><div class="kick">CHAPITRE {n:02d} · WORKFLOW ET CHECKLIST</div>
  <h2>Passe <span class="grad">à l'action</span></h2></div>
  <div class="wgrid">
    <div class="wcard"><div class="tag v">WORKFLOW</div><h3>{t(wtitle)}</h3>
      <div class="where"><span>OÙ</span>{t(c["workflow"]["where"])}</div>
      <ol class="wsteps">{wsteps}</ol></div>
    <div class="ccard"><div class="tag g">CHECKLIST</div><h3>Avant de valider</h3><ul class="checks">{checks}</ul>
      <div class="next">{nxt}</div></div>
  </div>
  {footer(n)}
</section>""")

# ---------- Plan d'action ----------
weeks = "".join(
    f'<div class="week"><div class="wk">SEMAINE {i+1}</div><h3>{t(w["t"])}</h3><p class="wch">{t(w["chapitres"])}</p><ul>' +
    "".join(f"<li>{t(x)}</li>" for x in w["actions"]) + "</ul></div>"
    for i, w in enumerate(extra["plan30"]))
pages.append(f"""
<section class="page plan">
  <div class="kick">TON PLAN D'ACTION</div>
  <h2>{deux_lignes(extra['plan_titre'])}</h2>
  <p class="intro">{t(extra["plan_intro"])}</p>
  <div class="weeks">{weeks}</div>
  {footer()}
</section>""")

# ---------- Fin ----------
num_page[0] += 1
pages.append(f"""
<section class="page fin">
  <div class="blob"></div>
  {masc('deux-pouces', 'masc')}
  <div class="brand w"><span class="dot"></span>{t(AUTEUR)}</div>
  <div class="fintxt">
    <div class="kick w">ET MAINTENANT ?</div>
    <h2>{t(extra["fin_titre"])}</h2>
    {"".join(f"<p>{t(x)}</p>" for x in extra["fin_paras"])}
    <div class="sig"><b>{t(AUTEUR)}</b><span>{t(extra['fin_signature'])}</span><span class="url">{t(extra['fin_url'])}</span></div>
  </div>
  <p class="legal">{t(extra["legal"])}</p>
</section>""")

css = open(os.path.join(SKILL, "scripts", "style.css"), encoding="utf-8").read()
doc = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{t(TITRE_GUIDE)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&family=IBM+Plex+Mono:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=block" rel="stylesheet">
<style>{css}</style></head><body>{''.join(pages)}</body></html>"""
out = os.path.join(ICI, "guide.html")
open(out, "w", encoding="utf-8").write(doc)

pdf = os.path.join(ICI, meta["fichier_pdf"])
subprocess.run([trouver_chrome(), "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                "--no-pdf-header-footer", "--virtual-time-budget=15000", f"--print-to-pdf={pdf}", uri(out)],
               check=True, capture_output=True)
print(json.dumps({"pdf": pdf, "pages": len(pages), "chapitres": len(chapitres), "prompts": nb_prompts,
                  "points_de_controle": nb_check}, ensure_ascii=False))
