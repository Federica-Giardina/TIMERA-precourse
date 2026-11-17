"""Render the preliminary learning book in all languages, ready for publication.

For each language (Quarto profiles en, fr and pt) this renders the HTML book into
docs/<language>/, then writes docs/index.html, a start page linking to the three
versions. The folder docs/ is published with GitHub Pages (Settings -> Pages ->
Deploy from a branch -> main, /docs) at
https://federica-giardina.github.io/TIMERA-precourse/.

The datasets of Module 1 are not published here: this book's chapters do not use
them, and the full set (which grows as the main course adds material) is shared
through the main course repository instead, to avoid suggesting participants need
to download data for this book.

For internal use only (sharing and feedback), it also renders the Word versions of
each language, complete and short (text, equations and figures, without code and
exercises; see short-docx.lua), into _internal/<language>/, which is not published.

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
ACKNOWLEDGEMENT = (
    "TIMERA is supported by the Global Health EDCTP3 Joint Undertaking and its members under grant "
    "agreement No&nbsp;101249114, and co-funded by the European Union and the Coalition for Epidemic "
    "Preparedness Innovations (CEPI). Views and opinions expressed are however those of the author(s) only "
    "and do not necessarily reflect those of the European Union, the Global Health EDCTP3 Joint Undertaking "
    "or CEPI. Neither the European Union nor the granting authority can be held "
    "responsible for them.")

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>TIMERA — Preliminary learning</title>
<link rel="icon" href="timera-icon.png">
<style>
body{font-family:system-ui,sans-serif;max-width:42rem;margin:3rem auto;padding:0 1rem;line-height:1.6;color:#212529;background:#fff}
a{color:#2780e3}
.languages{list-style:none;padding:0;display:flex;gap:1rem;flex-wrap:wrap;font-size:1.15rem}
.languages a{display:inline-block;padding:.4rem 1rem;border:1px solid #2780e3;border-radius:6px;text-decoration:none}
.languages a:hover{background:#2780e3;color:#fff}
footer{margin-top:3rem;padding-top:1rem;border-top:1px solid #dee2e6;font-size:.85rem;color:#495057}
footer img{max-width:100%%;width:25rem}
</style>
</head><body>
<p><img src="timera-logo.png" alt="TIMERA — Training Initiative for Modelling Epidemic Response in Africa" style="max-width:100%%;width:26rem"></p>
<h1>Preliminary learning</h1>
<ul class="languages">
%s
</ul>
<footer>
<p><img src="funder-logos.png" alt="Global Health EDCTP3, Co-funded by the European Union and CEPI"></p>
<p>%s</p>
</footer>
</body></html>
"""


def main():
    languages = [a for a in sys.argv[1:] if a in NAMES] or list(NAMES)
    for lang in languages:
        subprocess.run([QUARTO, "render", "--profile", lang, "--to", "html"], cwd=ROOT, check=True)
        # Word versions: internal only, not published
        for f in glob.glob(os.path.join(SITE, lang, "*.docx")):
            os.remove(f)
        subprocess.run([sys.executable, "render-short-docx.py", "--full", "--profile", lang], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "render-short-docx.py", "--profile", lang], cwd=ROOT, check=True)

    # images, and a marker that tells GitHub Pages to serve the files as they are
    open(os.path.join(SITE, ".nojekyll"), "w").close()
    for name in ["timera-logo.png", "timera-icon.png", "funder-logos.png"]:
        shutil.copy2(os.path.join(ROOT, "images", name), os.path.join(SITE, name))

    rows = ['<li><a href="%s/index.html" lang="%s">%s</a></li>' % (lang, lang, name)
            for lang, name in NAMES.items() if os.path.exists(os.path.join(SITE, lang, "index.html"))]
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf8") as f:
        f.write(PAGE % ("\n".join(rows), ACKNOWLEDGEMENT))
    print("Written", os.path.join(SITE, "index.html"))


if __name__ == "__main__":
    main()
