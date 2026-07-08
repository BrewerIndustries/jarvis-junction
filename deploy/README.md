# Deploy — Jarvis's Junction

Static site hosted on **GitHub Pages** (same model as Stellar Ascent / Space Base Race).

## Model

- One Pages site serves both environments from one repo:
  - `main` branch → `/` (prod) → **https://jarvis-junction.dabrewer.dev/**
  - `dev` branch → `/dev/` (dev) → **https://jarvis-junction.dabrewer.dev/dev/**
- `.github/workflows/pages.yml` lives on **`dev`** and checks out both branches
  itself, writing the `CNAME`. It triggers on **push to `dev`** (and manual
  `workflow_dispatch`). **Pushing to `main` does NOT auto-redeploy** — re-run the
  Action ("Run workflow") or push `dev`.

## Update

```bash
# dev site: just push dev — the Action rebuilds both / and /dev/
git push origin dev

# prod: promote via an approved PR (dev -> main), then trigger a rebuild
#   gh workflow run pages.yml   (or push an empty commit to dev)
```

## One-time setup (already done at repo creation)

```bash
# enable Pages via Actions
gh api -X POST repos/BrewerIndustries/jarvis-junction/pages -f build_type=workflow
# allow the dev branch to deploy to the github-pages environment
gh api -X POST repos/BrewerIndustries/jarvis-junction/environments/github-pages/deployment-branch-policies -f name=dev
# custom domain + HTTPS (set AFTER the DNS CNAME resolves, else the cert stalls)
gh api -X PUT repos/BrewerIndustries/jarvis-junction/pages -f cname=jarvis-junction.dabrewer.dev
gh api -X PUT repos/BrewerIndustries/jarvis-junction/pages -F https_enforced=true
```

## DNS (Cloudflare, done by the owner)

No wildcard on `dabrewer.dev`, so prod needs its own record:

```
CNAME  jarvis-junction  ->  brewerindustries.github.io   (DNS-only / not proxied)
```

Dev shares the same Pages host at `/dev/`, so it needs no separate record.

## Registry / launcher / dashboard

- `.jarvis.json` (repo root) declares the app to the dashboard + launcher cron.
- Dashboard: `jarvis-dashboard/scripts/sync-registry.mjs` — `REPOS` + `DEFAULTS`.
- Launcher: `jarvis-launcher/src/lib/apps.ts` — `DEFAULT_APPS` (Games, explicit
  `prodUrl`/`devUrl`).
