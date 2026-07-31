# Deployment — Read This

The documentation deploys to a `gh-pages` branch using `mkdocs gh-deploy`.
This bypasses Jekyll completely.

## One-time setup (do these in order)

### Step 1 — Delete any old Jekyll workflow

On GitHub, check `.github/workflows/` in your repo for any file OTHER than
`deploy-docs.yml` — for example `jekyll-gh-pages.yml`, `pages.yml`, or
`static.yml`. **Delete them.** They are what keep running Jekyll and causing
the `include-markdown` error. Only `deploy-docs.yml` should remain.

### Step 2 — Push this repository

```bash
git add .
git commit -m "Switch to mkdocs gh-deploy"
git push origin main
```

This triggers the workflow, which builds the site and creates a `gh-pages`
branch automatically.

### Step 3 — Wait for the Action to finish

Go to the **Actions** tab. Watch "Deploy MkDocs to gh-pages" run. It should
finish in 1-2 minutes and show green. If it's the first run, it creates the
`gh-pages` branch.

### Step 4 — Point Pages at the gh-pages branch

**Settings -> Pages -> Build and deployment:**
- Source: **Deploy from a branch**
- Branch: **gh-pages**  /  **(root)**
- Save

(Yes — "Deploy from a branch" this time, NOT "GitHub Actions". Because the
branch now contains pre-built static HTML, Jekyll can't break it, and the
`.nojekyll` file stops Jekyll from trying.)

### Step 5 — Visit the site

After ~1 minute:
`https://desmond-lartey.github.io/Knowledge-Management-Informatics/`

## Why this works when the other way didn't

The GitHub-Actions-native Pages deployment kept falling back to Jekyll because
a leftover Jekyll workflow was still present and processing your markdown —
including the `{% include-markdown %}` tag, which Jekyll doesn't understand.

`mkdocs gh-deploy` sidesteps all of that: MkDocs builds the HTML itself inside
the Action, then pushes finished HTML to `gh-pages`. GitHub just serves those
static files. Nothing re-processes your markdown, so nothing can choke on the
include tag.

## Updating the site later

Just push to `main`. The workflow rebuilds and force-updates `gh-pages`
automatically. You never touch the `gh-pages` branch by hand.
