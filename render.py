"""Render the preliminary learning book in all languages.

For each language (Quarto profiles en, fr and pt) this renders the HTML book and the
Word version into _book/<language>/, and writes _book/index.html, a page linking to
the three versions. It also renders, for internal use only, a short Word version of
each language (text, equations and figures, without code and exercises; see
short-docx.lua) into _internal/<language>/, which is not published.

Usage:  py render.py [en fr pt]
"""
import glob
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
QUARTO = shutil.which("quarto") or r"C:\Program Files\RStudio\resources\app\bin\quarto\bin\quarto.exe"
NAMES = {"en": "English", "fr": "Français", "pt": "Português"}


def main():
    languages = [a for a in sys.argv[1:] if a in NAMES] or list(NAMES)
    for lang in languages:
        subprocess.run([QUARTO, "render", "--profile", lang], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "render-short-docx.py", "--profile", lang], cwd=ROOT, check=True)

    rows = []
    for lang, name in NAMES.items():
        folder = os.path.join(ROOT, "_book", lang)
        if not os.path.exists(os.path.join(folder, "index.html")):
            continue
        docs = sorted(os.path.basename(f) for f in glob.glob(os.path.join(folder, "*.docx")))
        links = " · ".join('<a href="%s/%s">Word</a>' % (lang, d) for d in docs)
        rows.append('<li><a href="%s/index.html">%s</a> — %s</li>' % (lang, name, links))
    with open(os.path.join(ROOT, "_book", "index.html"), "w", encoding="utf8") as f:
        f.write("""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>TIMERA — Preliminary learning</title>
<style>body{font-family:system-ui,sans-serif;max-width:40rem;margin:3rem auto;padding:0 1rem;line-height:1.6}</style>
</head><body>
<h1>TIMERA — Preliminary learning</h1>
<p>Training Initiative for Modelling Epidemic Response in Africa</p>
<ul>
%s
</ul>
</body></html>
""" % "\n".join(rows))
    print("Written", os.path.join(ROOT, "_book", "index.html"))


if __name__ == "__main__":
    main()
