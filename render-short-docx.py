"""Render the short Word version of the book, for internal use (sharing and feedback):
the text, equations and figures of the lectures, without R code, output, practical
sessions, exercises or solutions (see short-docx.lua).

Usage, from the root of the project, after the normal render (`quarto render`):
    py render-short-docx.py [--profile NAME]

The short version is rendered in a temporary folder (a render of the whole project
empties its output folder) and saved, with the suffix "-short", in _internal/ (or
_internal/<profile>/), which is not published. Quarto is taken from the PATH, or from the copy bundled with RStudio.
"""
import glob
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
QUARTO = shutil.which("quarto") or r"C:\Program Files\RStudio\resources\app\bin\quarto\bin\quarto.exe"
TMP = "_book-short-tmp"
INTERNAL = "_internal"


def main():
    profile = sys.argv[sys.argv.index("--profile") + 1] if "--profile" in sys.argv else None
    out = os.path.join(ROOT, INTERNAL, profile) if profile else os.path.join(ROOT, INTERNAL)
    tmp = os.path.join(ROOT, TMP)
    existing = set(glob.glob(os.path.join(ROOT, "*_files")))
    cmd = [QUARTO, "render", "--to", "docx", "-M", "short-version:true", "--output-dir", TMP]
    if profile:
        cmd += ["--profile", profile]
    try:
        subprocess.run(cmd, cwd=ROOT, check=True)
        os.makedirs(out, exist_ok=True)
        for f in glob.glob(os.path.join(tmp, "*.docx")):
            short = os.path.join(out, os.path.basename(f)[:-5] + "-short.docx")
            shutil.copy2(f, short)
            print("Short version:", short)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        # figure folders that this render left next to the chapters
        for d in set(glob.glob(os.path.join(ROOT, "*_files"))) - existing:
            if os.path.isdir(d) and os.path.exists(d[:-6] + ".qmd"):
                shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    main()
