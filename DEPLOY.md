# Primavera Flowers — Deploy Guide

This repository contains the Savor-based Shopify theme for **primaveraflowersnyc.com** (store handle in dev: `pfwh-2.myshopify.com`).

## What's in this repo

```
assets/        Theme JS/CSS/SVG (113 files, untouched from Savor 3.5.1)
blocks/        Block components (93)
config/        settings_data.json — palette + typography customized for Primavera
layout/        theme.liquid + password.liquid
locales/       51 languages
sections/      41 section types
snippets/      103 snippets
templates/     Page templates — homepage rebuilt; new: page.delivery, page.story, page.sympathy, page.faq, page.es
data/          products.csv — 23 SKUs / 39 variants ready for Shopify import
```

## Step 1 — Connect this repo to Shopify

Your Themes → Connect theme dialog said "No accounts found." That's the Shopify GitHub app missing on your `netizenof` account. Fix:

1. Open `https://github.com/apps/shopify/installations/new`
2. Pick the **netizenof** account
3. Grant access to **`pfwh`** (or "All repositories")
4. Back in Shopify Admin → Online Store → Themes → **Connect theme**
5. Account: **netizenof**, Repository: **pfwh**, Branch: **main** (or `claude/install-pfwh-1r346` while the PR is open)
6. Click **Connect** — Shopify imports the theme as a new, unpublished theme

Your store is currently on **Horizon 3.5.1**. Connecting the repo does NOT replace Horizon. It adds Savor as a separate theme. Preview, then click **Publish** when ready.

## Step 2 — Import products

In Shopify Admin → **Products → Import** → upload `data/products.csv`.

Tags drive smart collections. Create these collections (Products → Collections → Create collection → Smart collection → match tag):

| Collection handle | Tag |
|---|---|
| bestsellers | bestseller |
| same-day | same-day |
| roses | roses |
| sympathy | sympathy |
| birthday | birthday |
| anniversary | anniversary |
| just-because | just-because |
| get-well | get-well |
| new-baby | new-baby |
| quinceanera | quinceanera |
| dia-de-las-madres | dia-de-las-madres |

After import, replace the placeholder image fields (currently empty) with real photos — either restock from `primaveraflowersnyc.com`, the Instagram feed, or new shoots.

## Step 3 — Map page templates

Create these pages (Online Store → Pages → Add page) and pick the matching template suffix:

| Page title | Handle | Template |
|---|---|---|
| Delivery | delivery | page.delivery |
| Our Story | our-story | page.story |
| Sympathy Concierge | sympathy | page.sympathy |
| FAQ | faq | page.faq |
| Florista Washington Heights | florista-washington-heights | page.es |

## Step 4 — App stack (cost-prioritized)

Native first (no fees):
- **Shopify Subscriptions** — runs the three subscription SKUs
- **Translate & Adapt** — feeds the `page.es.json` template + product translations
- **Search & Discovery** — synonyms, boosts (set "roses" ≈ "rosas")
- **Meta Pixel + Conversions API** — server-side tracking
- **Google & YouTube** — Merchant Center sync for Shopping/PMax
- **Shopify Inbox** — chat

Paid (~$110/mo total):
- **Zapiet — Pickup + Delivery** ($30) — 2pm cutoff, zone gating, Roadie/Skipcart fallback
- **Klaviyo** ($45 at first volume tier) — welcome, abandoned cart, post-purchase, Mother's Day cohort
- **Loox** ($15) — photo reviews
- **Nuflorist** ($20) — florist-specific add-ons + holiday rules

## Step 5 — Pre-publish checklist

- [ ] Logo uploaded (header.logo setting)
- [ ] Real address verified: 463 Fort Washington Ave, NY 10033 — phone (917) 770-1684
- [ ] Year founded confirmed for "since [year]" copy in homepage and story page
- [ ] Same-day cutoff confirmed (theme defaults to 2pm; bumping to 3pm differentiates from Ode à la Rose)
- [ ] Photo placeholders replaced for hero, occasion tiles, story section
- [ ] At least 5 Google reviews surfaced via Loox or static
- [ ] Sympathy / funeral home partner contacts confirmed (Ortiz, Schwartz Brothers)
- [ ] Klaviyo welcome flow live before paid traffic begins
- [ ] Meta Pixel + CAPI firing (use the Meta Pixel Helper extension to verify)
- [ ] Google Merchant Center feed approved (no disapproved products)
- [ ] Tax + shipping zones configured for 10032/10033/10034/10040 + Bronx ZIPs

## Step 6 — Publish

Online Store → Themes → Savor (the connected one) → **Publish**.

Then immediately: Settings → Sales channels → **Online Store** → remove the password protection.

## Customizing & deploying further

**Editing locally:**
```
git checkout main
git pull
# edit files
git add .
git commit -m "..."
git push origin main
```
GitHub-connected themes auto-pull from `main` on every push (you'll see updates in the Shopify Admin under Themes → version history).

**Editing in the Shopify theme editor:**
Theme editor changes are auto-committed back to `main` by the Shopify GitHub integration. Pull before editing locally to avoid conflicts.

**CLI fallback (if needed):**
```
shopify auth login --store=pfwh-2.myshopify.com
shopify theme dev   # local preview
shopify theme push  # push current dir to a theme
```

## Branch state

- `main` — production
- `claude/install-pfwh-1r346` — initial install + customizations PR

