# Repository Setup Guide

This guide walks through pushing this repository to GitHub and publishing the MkDocs Material documentation site. Do this once.

## 1. Push to your repository

```bash
cd geoai-repo

git init
git add .
git commit -m "Add GeoAI planning intelligence framework and MkDocs documentation"
git branch -M main
git remote add origin https://github.com/desmond-lartey/Knowledge-Management-Informatics.git
git push -u origin main
```

If the repository already has content and you intend to replace it:

```bash
git push -u origin main --force
```

## 2. Enable GitHub Pages via Actions

The documentation is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and deployed automatically by the workflow at `.github/workflows/deploy-docs.yml`.

1. Go to your repository on GitHub.
2. **Settings -> Pages**.
3. Under **Build and deployment -> Source**, select **GitHub Actions**.
4. Push any change to `docs/` or `mkdocs.yml` — or trigger the workflow manually from the **Actions** tab.
5. The site publishes to:
   `https://desmond-lartey.github.io/Knowledge-Management-Informatics/`

The first deployment takes two to three minutes. Subsequent pushes rebuild automatically.

## 3. Preview locally before pushing (optional)

```bash
pip install mkdocs-material
mkdocs serve
```

Open `http://127.0.0.1:8000` to preview. Live-reloads as you edit. The site was verified to build cleanly in `--strict` mode, so `mkdocs build --strict` should pass without warnings.

## 4. What the site includes

The MkDocs Material configuration (`mkdocs.yml`) enables:

- **Light and dark mode** with a toggle (teal primary, deep-orange accent).
- **Instant navigation** and top-level tabs across the seven documentation pages.
- **Full-text search** with suggestions and highlighting.
- **Code copy buttons** on every code block.
- **MathJax equation rendering** — every indicator formula renders as typeset mathematics (configured via `pymdownx.arithmatex` and `docs/javascripts/mathjax.js`).
- **Edit-on-GitHub** links on each page.

## 5. Link from the paper

In the published article, cite the repository and documentation site. A ready-to-use **Data and Code Availability** statement:

> The complete pipeline, indicator formulas, recommendation logic, validation
> procedures, and reproduction guide are openly available at
> https://github.com/desmond-lartey/Knowledge-Management-Informatics, with
> browsable documentation at
> https://desmond-lartey.github.io/Knowledge-Management-Informatics/.

## 6. Add the sample data

To let readers run the lightweight stages without the full national datasets, export a subset of your Alabama diagnostic output and commit it:

```bash
cp AL_urban_grid_results.csv data/sample/AL_urban_grid_results_sample.csv
git add data/sample/AL_urban_grid_results_sample.csv
git commit -m "Add sample diagnostic data for lightweight reproduction"
git push
```

Readers can then run `src/sensitivity.py` and the recommendation logic directly against the sample.

## Documentation structure

```
mkdocs.yml                       <- site configuration (repo root)
docs/
- index.md                       <- home
- methodology.md                 <- five-stage pipeline
- indicators.md                  <- every formula, disclosed
- recommendation-logic.md        <- rule-based decision table
- validation.md                  <- expert validation & reliability
- sensitivity.md                 <- PQI weighting robustness
- reproducibility.md             <- step-by-step reproduction
- javascripts/mathjax.js         <- equation rendering config
```

To add a new page, create the markdown file in `docs/` and add it to the `nav:` block in `mkdocs.yml`.
