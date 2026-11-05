# TIMERA — Preliminary learning

Self-study material for participants of **TIMERA** (Training Initiative for Modelling Epidemic Response in Africa), to be completed before the first face-to-face module, in English, French and Portuguese:

- **P1** Introduction to R
- **P2** Statistical and epidemiological concepts
- **P3** Mathematical background

**Read online:** <https://federica-giardina.github.io/TIMERA-preparatory/> — each language version can also be downloaded as a Word document, together with the datasets used in Module 1 (`datasets/TIMERA-datasets.zip`).

## Rendering

Requires R (≥ 4.4) with `tidyverse`, `readxl`, `patchwork`, `knitr` and `rmarkdown`, Quarto (bundled with RStudio) and Python 3. In a terminal:

```
py render.py
```

renders the three languages (HTML and Word) into `docs/en`, `docs/fr` and `docs/pt`, copies the datasets to `docs/datasets` and writes the language page `docs/index.html`. `quarto render` alone renders the English version only.

## Publishing

The website is the folder `docs/`, served by GitHub Pages. After rendering, commit and push the changes (including `docs/` and `_freeze/`); the website is updated within a few minutes. GitHub Pages is enabled once, in the repository settings: *Settings → Pages → Build and deployment → Deploy from a branch → `main`, folder `/docs`*.

## Source

This repository is **generated** from the main course repository, <https://github.com/Federica-Giardina/TIMERA>, where the same chapters form the *Preliminary learning* part of the course book and the translations are maintained. Changes should be made there and exported with `py preparatory/export.py` (see `preparatory/README.md` in the main repository); edits made directly in this repository will be overwritten.

## Licence

CC BY-NC-SA 4.0. The datasets retain the licences of their original sources (see `datasets/README.md`).
