# TIMERA — Preliminary learning

Self-study material for participants of **TIMERA** (Training Initiative for Modelling Epidemic Response in Africa), to be completed before the first face-to-face module, in English, French and Portuguese:

- **P1** Introduction to R
- **P2** Statistical and epidemiological concepts
- **P3** Mathematical background

**Read online:** <https://federica-giardina.github.io/TIMERA-precourse/>. The datasets used in Module 1 can be downloaded from the same page.

## Rendering

Requires R (≥ 4.4) with `tidyverse`, `readxl`, `patchwork`, `knitr` and `rmarkdown`, Quarto (bundled with RStudio) and Python 3. In a terminal:

```
py render.py
```

renders the three languages into `docs/en`, `docs/fr` and `docs/pt`, copies the datasets to `docs/datasets` and writes the start page `docs/index.html`. For internal use only (sharing drafts and requesting feedback), it also produces Word versions of each language, complete and short, in `_internal/`, which is not published. `quarto render --to html` alone renders the English version only.

## Publishing

The website is the folder `docs/`, served by GitHub Pages. After rendering, commit and push the changes (including `docs/` and `_freeze/`); the website is updated within a few minutes. GitHub Pages is enabled once, in the repository settings: *Settings → Pages → Build and deployment → Deploy from a branch → `main`, folder `/docs`*.

## Source

This repository is **generated** from the main course repository, <https://github.com/Federica-Giardina/TIMERA>, where the same chapters form the *Preliminary learning* part of the course book and the translations are maintained. Changes should be made there and exported with `py precourse/export.py` (see `precourse/README.md` in the main repository); edits made directly in this repository will be overwritten.

## Licence

TIMERA is supported by the Global Health EDCTP3 Joint Undertaking and its members under grant agreement No 101249114, and co-funded by the European Union and the Coalition for Epidemic Preparedness Innovations (CEPI).

CC BY-NC-SA 4.0. The datasets retain the licences of their original sources (see `datasets/README.md`).
