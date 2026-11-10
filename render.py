"""Render the preliminary learning book in all languages, ready for publication.

For each language (Quarto profiles en, fr and pt) this renders the HTML book into
docs/<language>/. It then copies the datasets to docs/datasets/ and writes
docs/index.html, a start page linking to the three versions. The folder docs/ is
published with GitHub Pages (Settings -> Pages -> Deploy from a branch -> main, /docs)
at https://federica-giardina.github.io/TIMERA-precourse/.

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
DATASETS = {"en": "Datasets", "fr": "Jeux de données", "pt": "Conjuntos de dados"}
DATASETS_NOTE = "CSV files used in Module 1, with descriptions · fichiers CSV du module 1 · ficheiros CSV do Módulo 1"
DOWNLOAD_ICON = ('<svg aria-hidden="true" width="18" height="18" viewBox="0 0 16 16" fill="currentColor">'
                 '<path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5'
                 'a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0'
                 'l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg>')
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
.download{display:inline-flex;align-items:center;gap:.4rem;font-weight:600;text-decoration:none}
.note{font-size:.85rem;color:#6c757d}
footer{margin-top:3rem;padding-top:1rem;border-top:1px solid #dee2e6;font-size:.85rem;color:#495057}
footer img{max-width:100%%;width:16rem}
</style>
</head><body>
<p><img src="timera-logo.png" alt="TIMERA — Training Initiative for Modelling Epidemic Response in Africa" style="max-width:100%%;width:26rem"></p>
<h1>Preliminary learning</h1>
<ul class="languages">
%s
</ul>
<p><a class="download" href="datasets/TIMERA-datasets.zip" download>%s %s</a><br><span class="note">%s</span></p>
<footer>
<p><img src="funder-logos.png" alt="Global Health EDCTP3 and Co-funded by the European Union"></p>
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

    # datasets, images, and a marker that tells GitHub Pages to serve the files as they are
    shutil.copytree(os.path.join(ROOT, "datasets"), os.path.join(SITE, "datasets"), dirs_exist_ok=True)
    open(os.path.join(SITE, ".nojekyll"), "w").close()
    for name in ["timera-logo.png", "timera-icon.png", "funder-logos.png"]:
        shutil.copy2(os.path.join(ROOT, "images", name), os.path.join(SITE, name))

    rows = ['<li><a href="%s/index.html" lang="%s">%s</a></li>' % (lang, lang, name)
            for lang, name in NAMES.items() if os.path.exists(os.path.join(SITE, lang, "index.html"))]
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf8") as f:
        f.write(PAGE % ("\n".join(rows), DOWNLOAD_ICON, " · ".join(DATASETS.values()), DATASETS_NOTE,
                        ACKNOWLEDGEMENT))
    print("Written", os.path.join(SITE, "index.html"))


if __name__ == "__main__":
    main()
