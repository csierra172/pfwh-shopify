# Primavera Flowers Paid Traffic & SEO Strategy (synthesized)

Source: `PFWH_Paid_Traffic_SEO_Strategy.docx` (May 2026). Synthesized into actionable runbook for the pfwh-v2 repo. Cross-references the more detailed `docs/meta-catalog-setup.md` and `docs/google-pla-setup.md` runbooks already in this repo.

---

## What's been applied to the codebase from this strategy

This section tracks what's already shipped vs. what's manual / in admin only.

### Shipped to the repo
- **Header logo asset fallback** in `blocks/_header-logo.liquid`. Top-left now renders `assets/primavera-logo.svg` by default until a real upload happens in Theme Editor.
- **Subscription PDP funnel** at `/pages/subscriptions` with full hero, trust strip, this-week's-bench preview, three tiers, roses cross-sell, how-it-works, photo guarantee, delivery zones, FAQ, final CTA.
- **/pages/roses** SEO landing for "roses delivery NYC" intent. Cross-links to subscriptions.
- **/pages/flower-delivery-washington-heights** P0 landing (per SEO playbook). Targets `washington heights flower delivery`, `florist 10033`, `florist 10032`, `florist 10034`, `florist 10040`.
- **/pages/columbia-presbyterian-hospital-flowers** P0 hospital page. Targets `flower delivery columbia presbyterian`, `NYP flower delivery 168th`. Hospital-specific etiquette section (no scent for ICU, NICU policies).
- **/pages/quinceanera** Latino-occasion white space. Bilingual copy. Targets `quinceanera flowers nyc` (zero national competition per strategy doc).
- **/pages/dia-de-las-madres** Spanish-first occasion landing. Pairs with English homepage. Targets `flores dia de las madres nyc`.
- **products.csv catalog expanded** to 35 SKUs (60 variants) with WaHi-localized titles + tags including `bestseller`, `same-day`, occasion tags.
- **Google Maps embed** on the homepage coverage section.
- **Same-day cutoff sticky bar** wired in `snippets/sameday-countdown.liquid`.
- **Welcome popup** wired in `snippets/welcome-popup.liquid` (15% off lead magnet).
- **JSON-LD LocalBusiness/Florist schema** in `snippets/seo-schema.liquid`.
- **Meta + Google ad setup runbooks** at `docs/meta-catalog-setup.md` and `docs/google-pla-setup.md`.

### Still manual / Shopify admin only

These cannot be done in code. They have to be done by Chris in the Shopify or Google or Meta admin.

1. **Publish the Savor theme.** DEPLOY.md flags this as the single highest-leverage action. Until clicked, customers still see the Teleflora franchise template at primaveraflowersnyc.com.
2. **Create the new pages in admin.** For each `templates/page.{handle}.json` we shipped, a Page resource has to exist in admin pointing to the template. See "New pages to create in admin" below.
3. **Upload the brand logo via Theme Editor → Header → Logo** to replace the asset-fallback rendering with a customer-uploaded version (cleaner control over height/width).
4. **Install the Facebook & Instagram + Google & YouTube channels** in admin. Sync catalogs. See `docs/meta-catalog-setup.md` and `docs/google-pla-setup.md`.
5. **Verify domain in Meta Business Manager.** Brand Safety → Domains.
6. **Optimize Google Business Profile** (highest-ROI action per strategy doc). Add all SKUs as products, post weekly, seed Q&A, request reviews via post-purchase email/SMS.
7. **Install Klaviyo.** Welcome series, post-purchase, abandoned checkout. See `clients/Primavera/emails/KLAVIYO-FLOWS.md` for flow specs.
8. **Install Judge.me** ($0 free tier). Import existing Google reviews. PDP review block. Target 20 reviews in 30 days.
9. **Install Pickeasy** ($9.99/mo). Same-day cutoff configuration, blackout dates, delivery slots.
10. **Install AfterSell** ($34.99/mo). Post-purchase upsell for vase/chocolates/balloons/teddy.
11. **Install Smile.io** (free tier). Loyalty + referrals.
12. **Add `/pages/subscriptions`, `/pages/roses`, `/pages/flower-delivery-washington-heights` to the main nav** in admin → Navigation → Main menu.

---

## Quick wins from the strategy doc (30 days)

If we do nothing else in the first 30 days, these 4 actions should drive measurable revenue:

1. **Claim and fully optimize Google Business Profile.** Free, highest ROI. Add all products with photos. Post weekly. Seed Q&A.
2. **Install the Google & YouTube channel** to get products into free Google Shopping listings.
3. **Install the Facebook & Instagram channel** + launch $30/day DPA retargeting on existing traffic.
4. **The new `/pages/flower-delivery-washington-heights` page is now live** in the repo. Once Savor is published, this page targets the highest-intent local SEO keyword.

---

## New pages to create in admin

Each of these requires creating a Page resource in **Shopify Admin → Online Store → Pages → Add page** pointing to the matching template. The template files are already in the repo.

| Page title | Handle | Template suffix |
|---|---|---|
| Subscriptions | `subscriptions` | `subscriptions` |
| Roses | `roses` | `roses` |
| Flower Delivery Washington Heights | `flower-delivery-washington-heights` | `flower-delivery-washington-heights` |
| Columbia Presbyterian Hospital Flowers | `columbia-presbyterian-hospital-flowers` | `columbia-presbyterian-hospital-flowers` |
| Quinceañera Flowers | `quinceanera` | `quinceanera` |
| Día de las Madres | `dia-de-las-madres` | `dia-de-las-madres` |

---

## Title formula for product feed (Meta + Google)

Per the strategy doc, every product title in `data/products.csv` should follow this structure:

```
[Flower Type] + [Color/Style] + [Product Type] + [Occasion] + [Delivery Speed] + "NYC" or "Washington Heights"
```

Examples to retitle existing SKUs:
- `Classic Red Roses` → `Red Roses Bouquet | Same-Day Delivery NYC | Classic Arrangement`
- `Pink Garden Roses` → `Pink Garden Roses Wrapped Bouquet | Birthday Flowers Manhattan`
- `White Roses & Eucalyptus` → `White Roses & Eucalyptus Arrangement | Same-Day NYC Delivery`
- `Rainbow Long-Stem Roses` → `Rainbow Long-Stem Roses Bouquet | Anniversary Flowers NYC`
- `Quinceañera Centerpiece` → `Quinceañera Flower Centerpiece | Washington Heights Florist`
- `Sympathy Standing Spray` → `Sympathy Standing Spray | Same-Day Flower Delivery Manhattan`

Apply via Shopify product editor or by re-importing the CSV with updated titles.

---

## Meta campaign structure ($500 to $1k/mo test)

- **Campaign 1: Prospecting** (Advantage+ Shopping). All SKUs in catalog. 60% of Meta budget.
- **Campaign 2: Retargeting** (Manual DPA). 7/14/30-day windows. 40% of Meta budget.
- **Audience exclusion:** existing purchasers (180 days) excluded from cold campaigns.
- **Creative:** 1:1 square for feed, 9:16 vertical for Reels/Stories. Min 3 variants per ad set.
- **Pixel events** (priority order): Purchase → InitiateCheckout → AddToCart → ViewContent → Lead.

Detailed setup: `docs/meta-catalog-setup.md`.

---

## Google PMax + PLA structure

- **Campaign 1: Brand Search** (manual CPC). Protect brand terms. Small budget.
- **Campaign 2: Performance Max** (PMax). All products. 60% of Google budget.
- **Campaign 3: Standard Shopping** for high-margin SKUs (Quinceañera, Sympathy, Subscriptions, Orchids). Manual bid control.
- **Radius targeting:** 5-10 miles from Washington Heights for all campaigns.

Detailed setup: `docs/google-pla-setup.md`.

---

## App stack ($100-150/mo lean setup)

| Function | App | Cost | Notes |
|---|---|---|---|
| Subscriptions | Appstle | $10/mo | No transaction fees at entry. Florist-friendly. |
| Delivery date picker | Pickeasy | $9.99-24.99/mo | Built for perishables. Cutoff times, blackouts, delivery slots. |
| Post-purchase upsell | AfterSell | $34.99/mo | One-click upsell for vase/chocolates/balloons/teddy. |
| SEO | SEO Manager by Venntov | $20/mo | Meta tags, sitemap, structured data. |
| Email + SMS | Klaviyo | Free → $20+15/mo | Best Shopify integration. Welcome, abandoned cart, post-purchase. |
| Reviews | Judge.me | Free → $15/mo | Best free tier. Photo reviews. Google Shopping integration. |
| Loyalty | Smile.io | Free → $49/mo | Points, referrals, review incentives. |
| Meta channel | Facebook & Instagram | Free | Required. Auto-syncs catalog. |
| Google channel | Google & YouTube | Free | Required. Auto-syncs to Merchant Center. |

---

## SEO pages priority (90 days)

| Priority | Page | Status |
|---|---|---|
| P0 | `/pages/flower-delivery-washington-heights` | ✅ shipped in repo |
| P0 | `/pages/roses` | ✅ shipped in repo |
| P0 | `/pages/columbia-presbyterian-hospital-flowers` | ✅ shipped in repo |
| P0 | `/pages/quinceanera` | ✅ shipped in repo |
| P0 | `/pages/dia-de-las-madres` | ✅ shipped in repo |
| P0 | `/pages/florista-washington-heights` (Spanish hub) | ✅ existing |
| P0 | `/pages/subscriptions` | ✅ rebuilt as PDP funnel |
| P0 | `/pages/sympathy` | ✅ existing |
| P1 | `/pages/inwood-flower-delivery` | ⏳ pending |
| P1 | `/pages/hudson-heights-florist` | ⏳ pending |
| P1 | `/pages/allen-hospital-flowers-inwood` | ⏳ pending |
| P1 | `/pages/marble-hill-flower-delivery` | ⏳ pending |
| P1 | `/pages/riverdale-flower-delivery` | ⏳ pending |

---

## Source

Synthesized from `PFWH_Paid_Traffic_SEO_Strategy.docx` (Local Agent Mode session output, May 2026). Cross-references `clients/Primavera/seo/SEO-PLAYBOOK.md`, `clients/Primavera/funnel/FUNNEL-ANALYSIS.md`, and `clients/Primavera/competitors/COMPETITOR-REPORT.md`.
