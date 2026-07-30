# Repository Setup Guide

This guide walks through pushing this repository to GitHub and enabling the documentation site. Do this once.

## 1. Push to your repository

```bash
cd geoai-repo

git init
git add .
git commit -m "Add GeoAI planning intelligence framework and documentation"
git branch -M main
git remote add origin https://github.com/desmond-lartey/Knowledge-Management-Informatics.git
git push -u origin main
```

If the repository already has content, either merge or force-push a fresh history:

```bash
git push -u origin main --force   # only if you intend to replace existing content
```

## 2. Enable GitHub Pages

Two options — the workflow-based build (recommended) or the simple branch-folder build.

### Option A — Automatic build via Actions (recommended)

The included workflow at `.github/workflows/pages.yml` builds the Jekyll site from `docs/` on every push.

1. Go to your repository on GitHub.
2. **Settings → Pages**.
3. Under **Build and deployment → Source**, select **GitHub Actions**.
4. Push any change to `docs/` (or trigger the workflow manually from the Actions tab).
5. The site publishes to `https://desmond-lartey.github.io/Knowledge-Management-Informatics/`.

### Option B — Serve directly from the docs folder

1. **Settings → Pages**.
2. Under **Source**, select **Deploy from a branch**.
3. Branch: `main`, folder: `/docs`.
4. Save. The site builds automatically.

If you use Option B, GitHub Pages reads `docs/_config.yml` directly — no Actions workflow needed. You can delete `.github/workflows/pages.yml` in that case.

## 3. Verify the math renders

The documentation uses MathJax for equations (configured in `docs/_config.yml` via the kramdown `math_engine: mathjax` setting). After the site builds, open the [Indicators](https://desmond-lartey.github.io/Knowledge-Management-Informatics/indicators) page and confirm the formulas render as typeset mathematics rather than raw LaTeX.

If equations show as raw `$$...$$`, add this to the top of each docs page's front matter or include a MathJax script in the theme layout. The Cayman theme used here supports kramdown-mathjax out of the box for most content.

## 4. Link from the paper

In the published article, cite the repository and documentation site:

> Code and documentation: https://github.com/desmond-lartey/Knowledge-Management-Informatics
> Documentation: https://desmond-lartey.github.io/Knowledge-Management-Informatics/

Add these to a **Data and Code Availability** statement, for example:

> The complete pipeline, indicator formulas, recommendation logic, validation
> procedures, and reproduction guide are openly available at
> https://github.com/desmond-lartey/Knowledge-Management-Informatics, with
> browsable documentation at
> https://desmond-lartey.github.io/Knowledge-Management-Informatics/.

## 5. Add the sample data

To let readers run the lightweight stages without the full national datasets, export a subset of your Alabama diagnostic output and commit it:

```bash
# From your machine, copy a sample of the diagnostic CSV
cp AL_urban_grid_results.csv data/sample/AL_urban_grid_results_sample.csv
git add data/sample/AL_urban_grid_results_sample.csv
git commit -m "Add sample diagnostic data for lightweight reproduction"
git push
```

Readers can then run `src/sensitivity.py` and the recommendation logic directly against the sample.
