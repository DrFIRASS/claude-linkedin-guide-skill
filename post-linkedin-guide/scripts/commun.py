"""Fonctions partagées par build_guide.py et build_image.py.

- lire_config() : lit config.json à la racine du skill (créé au premier lancement à partir de config.exemple.json).
- trouver_chrome() : trouve Chrome, Chromium ou Edge sur macOS, Windows ou Linux (ou la variable CHROME_PATH).
- uri() : transforme un chemin local en adresse file:// valable sur tous les systèmes.
"""
import json, os, shutil
from pathlib import Path

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHEMINS_CHROME = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
NOMS_CHROME = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"]


def lire_config():
    for nom in ("config.json", "config.exemple.json"):
        f = os.path.join(SKILL, nom)
        if os.path.exists(f):
            return json.load(open(f, encoding="utf-8"))
    return {}


def trouver_chrome():
    env = os.environ.get("CHROME_PATH")
    if env and os.path.exists(env):
        return env
    for p in CHEMINS_CHROME:
        if os.path.exists(p):
            return p
    for nom in NOMS_CHROME:
        p = shutil.which(nom)
        if p:
            return p
    raise SystemExit("Chrome introuvable. Installe Google Chrome, ou indique son chemin dans la variable CHROME_PATH.")


def uri(chemin):
    return Path(chemin).resolve().as_uri()


def reglages(meta):
    """Auteur et mascotte : meta.json d'abord, puis config.json."""
    config = lire_config()
    auteur = meta.get("auteur") or config.get("auteur") or "Ton nom"
    mascotte = meta.get("mascotte", config.get("mascotte", False))
    dossier = os.path.join(SKILL, "assets", "mascotte")
    if mascotte and not all(os.path.exists(os.path.join(dossier, f"{n}.png"))
                            for n in ("presente-joyeux", "index-conseil", "deux-pouces")):
        mascotte = False
    return auteur, bool(mascotte), dossier
