"""Render the preliminary learning book in all languages, ready for publication.

For each language (Quarto profiles en, fr and pt) this renders the HTML book and the
Word version into docs/<language>/. It then copies the datasets archive to
docs/datasets/ and writes docs/index.html, a page linking to the three versions.
The folder docs/ is published with GitHub Pages (Settings → Pages → Deploy from a
branch → main, /docs) at https://federica-giardina.github.io/TIMERA-preparatory/.

It also renders, for internal use only, a short Word version of each language (text,
equations and figures, without code and exercises; see short-docx.lua) into
_internal/<language>/, which is not published.

Usage:  py render.py [en fr pt]
"""
import glob
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
QUARTO = shutil.which("quarto") or r"C:\Program Files\RStudio\resources\app\bin\quarto\bin\quarto.exe"
SITE = os.path.join(ROOT, "docs")
NAMES = {"en": "English", "fr": "Français", "pt": "Português"}
DATASETS = {"en": "Datasets used in Module 1 (CSV files, with descriptions)",
            "fr": "Jeux de données utilisés dans le module 1 (fichiers CSV, avec descriptions)",
            "pt": "Conjuntos de dados utilizados no Módulo 1 (ficheiros CSV, com descrições)"}


def main():
    languages = [a for a in sys.argv[1:] if a in NAMES] or list(NAMES)
    for lang in languages:
        subprocess.run([QUARTO, "render", "--profile", lang], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "render-short-docx.py", "--profile", lang], cwd=ROOT, check=True)

    # datasets, and a marker that tells GitHub Pages to serve the files as they are
    shutil.copytree(os.path.join(ROOT, "datasets"), os.path.join(SITE, "datasets"), dirs_exist_ok=True)
    open(os.path.join(SITE, ".nojekyll"), "w").close()

    rows = []
    for lang, name in NAMES.items():
        folder = os.path.join(SITE, lang)
        if not os.path.exists(os.path.join(folder, "index.html")):
            continue
        docs = sorted(os.path.basename(f) for f in glob.glob(os.path.join(folder, "*.docx")))
        links = " · ".join('<a href="%s/%s">Word</a>' % (lang, d) for d in docs)
        rows.append('<li><a href="%s/index.html">%s</a> — %s</li>' % (lang, name, links))
    data = " / ".join(DATASETS.values())
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf8") as f:
        f.write("""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>TIMERA — Preliminary learning</title>
<style>body{font-family:system-ui,sans-serif;max-width:42rem;margin:3rem auto;padding:0 1rem;line-height:1.6}</style>
</head><body>
<h1>TIMERA — Preliminary learning</h1>
<p>Training Initiative for Modelling Epidemic Response in Africa</p>
<ul>
%s
</ul>
<p><a href="datasets/TIMERA-datasets.zip">TIMERA-datasets.zip</a> — %s</p>
</body></html>
""" % ("\n".join(rows), data))
    print("Written", os.path.join(SITE, "index.html"))


if __name__ == "__main__":
    main()
