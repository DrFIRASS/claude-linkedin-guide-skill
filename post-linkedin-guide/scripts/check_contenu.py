#!/usr/bin/env python3
"""Contrôle le contenu du guide avant de générer le PDF.

Usage : python3 check_contenu.py <dossier_projet>

Vérifie le schéma (références/contenu-schema.md), les longueurs qui conditionnent la mise en page,
et les règles d'écriture du skill. Sort avec le code 1 et la liste des problèmes s'il y en a.
"""
import json, glob, os, re, sys

if len(sys.argv) != 2:
    sys.exit("Usage : python3 check_contenu.py <dossier_projet>")
C = os.path.join(os.path.abspath(sys.argv[1]), "contenu")
pb = []

# Mots et signes refusés. « [À COMPLÉTER] » est refusé : une marque oubliée dans un prompt fait brouillon.
# Pour une info manquante dans un prompt, écrire [INFO MANQUANTE].
INTERDITS = [("—", "tiret long"), ("–", "demi-cadratin"), ("À COMPLÉTER", "marque [À COMPLÉTER]")]
MOTS = r"\b(vous|incroyable|révolutionnaire|ultime|booster|scaler|synergie|game changer)\b"


def texte(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x:
            yield from texte(y)
    elif isinstance(x, dict):
        for y in x.values():
            yield from texte(y)


def regles(nom, obj):
    for s in texte(obj):
        for car, lib in INTERDITS:
            if car in s:
                pb.append(f"{nom} : {lib} dans « {s[:60]}… »")
        m = re.search(MOTS, s, re.I)
        if m:
            pb.append(f"{nom} : mot refusé « {m.group(0)} » dans « {s[:60]}… »")


def borne(nom, s, mini, maxi):
    if not (mini <= len(s) <= maxi):
        pb.append(f"{nom} : {len(s)} caractères (attendu {mini} à {maxi})")


for f in ("meta.json", "extra.json"):
    if not os.path.exists(os.path.join(C, f)):
        pb.append(f"{f} manquant")
if pb:
    sys.exit("\n".join(pb))

meta = json.load(open(os.path.join(C, "meta.json"), encoding="utf-8"))
extra = json.load(open(os.path.join(C, "extra.json"), encoding="utf-8"))
regles("meta.json", meta)
regles("extra.json", extra)
for l in meta["titre_couverture"]:
    # au-delà, la ligne déborde sur la forme rose de la couverture
    if len(l.replace("*", "")) > 17:
        pb.append(f"meta.titre_couverture : « {l} » dépasse 17 caractères")
if len(meta["titre_couverture"]) != 4:
    pb.append("meta.titre_couverture : 4 lignes attendues")
if not re.fullmatch(r"[A-Z0-9]{2,30}", meta["mot_cle"]):
    pb.append("meta.mot_cle : 2 à 30 majuscules ou chiffres, sans accent ni espace")
if len(extra["setup_steps"]) != 3 or len(extra["setup_prompts"]) != 2:
    pb.append("extra : 3 setup_steps et 2 setup_prompts attendus")
if len(extra["plan30"]) != 4 or any(len(w["actions"]) != 4 for w in extra["plan30"]):
    pb.append("extra.plan30 : 4 semaines de 4 actions attendues")
for sp in extra["setup_prompts"]:
    borne("extra.setup_prompts.prompt", sp["prompt"], 250, 560)

chs = sorted(glob.glob(os.path.join(C, "ch*.json")))
if not 6 <= len(chs) <= 10:
    pb.append(f"{len(chs)} chapitres : la mise en page est prévue pour 6 à 10")
nums = []
for f in chs:
    nom = os.path.basename(f)
    try:
        c = json.load(open(f, encoding="utf-8"))
    except json.JSONDecodeError as err:
        pb.append(f"{nom} : JSON invalide ({err})")
        continue
    regles(nom, c)
    nums.append(c["num"])
    borne(f"{nom}.title", c["title"], 5, 42)
    borne(f"{nom}.intro", c["intro"], 220, 400)
    if len(c["framework"]["steps"]) != 4:
        pb.append(f"{nom} : 4 étapes de méthode attendues")
    for s in c["framework"]["steps"]:
        borne(f"{nom}.framework.d", s["d"], 60, 145)
    if len(c["prompts"]) != 4:
        pb.append(f"{nom} : 4 prompts attendus")
    for p in c["prompts"]:
        borne(f"{nom}.prompt « {p['title']} »", p["prompt"], 300, 620)
    if len(c["workflow"]["steps"]) != 5:
        pb.append(f"{nom} : 5 étapes de workflow attendues")
    if len(c["checklist"]) != 6:
        pb.append(f"{nom} : 6 points de checklist attendus")
    for s in c["checklist"]:
        borne(f"{nom}.checklist", s, 15, 95)
    borne(f"{nom}.mistake", c["mistake"], 60, 240)
    borne(f"{nom}.tip", c["tip"], 60, 240)
if nums != list(range(1, len(nums) + 1)):
    pb.append(f"numéros de chapitres non consécutifs : {nums}")

if pb:
    print("Contenu à corriger :")
    print("\n".join(f"- {x}" for x in pb))
    sys.exit(1)
print(f"Contenu valide : {len(chs)} chapitres.")
