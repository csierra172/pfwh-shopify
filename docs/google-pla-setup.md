# Primavera × Google Shopping (PLA / PMax) — Setup Guide

Last verified: May 2026. Store: `pfwh-2.myshopify.com` (Savor theme). Brand: Primavera Flowers Washington Heights. Budget: $500–$1,000/mo.

> **2026 context that frames everything below:**
> - **Merchant Center Next** is the only UI as of Jan 1, 2026. Old "Classic" GMC is dead — menu paths in this doc reflect MC Next.
> - **Content API → Merchant API** migration: beta cutoff Feb 28, 2026, Content API cutoff Aug 18, 2026. The Shopify Google channel handles this for you. Do not roll your own feed integration without Merchant API support.
> - **Smart Shopping is gone** (migrated to PMax in 2022–23). PMax is the default Shopping campaign type.
> - **Consent Mode v2** required for any EU/UK traffic. PFWH is NYC-local so this is not blocking, but enable it anyway via Shopify Customer Privacy.

---

## Step 1 — Connect Shopify to Google Merchant Center

**Use the native Google & YouTube channel.** For a $500–$1,000/mo florist, third-party feed managers (Feedonomics, DataFeedWatch, Channable) are overkill — you'd burn $50–$200/mo of the test budget on feed plumbing. Reserve those for $10K+/mo accounts where field-level overrides drive measurable lift. The native channel handles ~90% of what's needed and is already Merchant-API-compatible.

**Steps:**
1. Shopify admin → **Sales channels** → **+** → search "Google & YouTube" → **Add channel**.
2. Open the channel → **Connect Google account** → sign in with the Google account that owns/will own the GMC + Google Ads accounts. Use a `@primaveraflowers.com` Google Workspace account if one exists; avoid personal Gmail.
3. Accept the Google Merchant Center linking prompt. If no GMC exists, the flow creates one and auto-claims `primaveraflowers.com` (or whatever the storefront domain is) via Shopify's auto-verification handshake.
4. Confirm shipping zones in Shopify match where you actually deliver (10032/10033/10034/10040 + any wider NYC). GMC pulls these.
5. Confirm tax settings (NY sales tax) — required for US shopping ads.
6. Wait 1–24 hours for first feed sync. Initial GMC review of products takes 3–5 business days; expect some disapprovals.

**Pre-reqs that block sync** (Shopify-side checklist before connecting):
- Storefront not password-protected
- Refund policy + Terms of Service published (footer links auto-detected by GMC)
- Contact page with physical address (463 Fort Washington Ave) + phone — GMC verifies business identity from this
- Valid payment provider live (Shopify Payments fine)

**What native sync handles automatically:** id, title (from product title), description, link, image_link, price, sale_price, availability, condition (set to `new`), brand (from Shopify vendor field), product_type (from Shopify product type), shipping (from Shopify shipping zones).

**What it does NOT handle well for a florist** (we'll fix in Step 2):
- `google_product_category` — defaults to whatever auto-mapping picks; almost always wrong for cut flowers
- `gtin` / `identifier_exists` — handmade bouquets need explicit `identifier_exists = no`
- Custom labels (occasion, price tier, bestseller) — must be set via metafields
- Title formula — defaults to raw Shopify product title, which is usually short and brand-less

---

## Step 2 — Configure the product feed for florist data

### 2a. Title formula

Google weights the **first 70 characters** of `title` heaviest for query matching. Practitioner consensus title pattern for occasion-driven local commerce:

```
[Brand] [Color/Variety] [Product Type] | [Occasion] | [Delivery Promise] [City]
```

Examples for PFWH:
- `Primavera Flowers Pink Garden Roses Bouquet | Birthday Flowers | Same-Day NYC Delivery`
- `Primavera Flowers White Lilies Sympathy Arrangement | Funeral Flowers | Same-Day Manhattan Delivery`
- `Primavera Flowers Mixed Tulips | Just Because Bouquet | Washington Heights Same-Day`

Hard rules:
- Front-load the keyword the buyer types ("birthday flowers," "sympathy arrangement," "roses bouquet"). Brand name is not the highest-volume search term — but keep it for trust + brand-search overlap.
- Stay under **150 chars** (Google truncates at 150, displays ~70).
- No ALL CAPS, no promo language ("BEST!", "$10 off"), no emojis — these trigger automated disapproval as "promotional text in title."
- Variant-level titles should include the differentiator (size, color) — Shopify variants do this natively if your product titles are good.

**Implementation:** Use the Google & YouTube channel's "Title customization" rules (admin → Google & YouTube → Settings → Product feed → Title format), OR set per-product overrides via Shopify metafields (`google.custom_label_*` and `google.title`). Confidence: medium — the in-app title rule editor is limited; for nuanced concatenation many shops still hand-edit titles or use a metafield + Liquid override.

### 2b. Custom labels (`custom_label_0` through `custom_label_4`)

PMax/Shopping listing groups can only segment by feed attributes. Custom labels are how you slice the catalog for budget control. Recommended PFWH mapping:

| Label | Purpose | Values |
|---|---|---|
| `custom_label_0` | **Occasion** | `birthday`, `sympathy`, `anniversary`, `just-because`, `get-well`, `new-baby`, `quinceanera`, `dia-de-las-madres`, `everyday` |
| `custom_label_1` | **Price tier** | `under-50`, `50-99`, `100-149`, `150-plus` |
| `custom_label_2` | **Margin tier** | `high`, `mid`, `low` (subscriptions = high, add-ons = low) |
| `custom_label_3` | **Bestseller flag** | `bestseller`, `regular`, `new`, `clearance` |
| `custom_label_4` | **Seasonality** | `evergreen`, `valentines`, `mothers-day`, `dia-de-madres`, `holiday`, `spring`, `summer`, `fall`, `winter` |

**How to populate:** map your existing Shopify product tags (`bestseller`, `roses`, `sympathy`, `birthday`, etc.) into these labels. The Google & YouTube channel exposes a metafield mapping UI under **Product feed → Metafields**, OR set `custom_label_0`-`4` directly per product as metafields under namespace `google` (key `custom_label_0`, type `single_line_text_field`). Bulk-edit via Shopify CSV export → re-import.

### 2c. `google_product_category`

Set to `Arts & Entertainment > Party & Celebration > Gift Giving > Fresh Cut Flowers` — taxonomy ID **2899** — for all bouquets and arrangements.

For non-flower products:
- Plants/potted: `Home & Garden > Plants > Plants` (taxonomy 985)
- Subscription boxes containing flowers: still use 2899
- Add-ons (vases, cards, chocolates): use the actual product category (e.g., `Home & Garden > Decor > Vases` = 602)

Set globally via Shopify product type → metafield mapping, with per-product overrides in metafield `mm-google-shopping.google_product_category` or `google.google_product_category` (the channel reads either; confidence: medium on which key wins — verify in GMC diagnostics after first sync).

### 2d. `identifier_exists` and GTIN

Cut-flower bouquets are handmade and have **no GTIN**. Per Google's policy:
- Set `identifier_exists = no` (or `false`) on every bouquet/arrangement SKU.
- Optionally provide `brand = Primavera Flowers` and a unique `mpn` (your Shopify SKU works) — improves trust signals without faking a GTIN.

**Do not** invent UPC codes. GMC catches GTIN mismatches with the GS1 database and suspends accounts for invalid identifiers.

For resold add-ons that DO have GTINs (boxed chocolates, branded vases) — provide the real GTIN. Mixing handmade + branded products under one account is fine as long as each row declares correctly.

### 2e. Image requirements (2026)

- **Minimum** 800×800 px (will sync but barely). **Recommended** 1500×1500 px or larger — Google's 2026 documentation now explicitly recommends 1500×1500 for Shopping/PMax to support high-density displays and product image experiments.
- Max 64 MP, max 16 MB.
- **Background:** white, off-white, or transparent for the **primary** `image_link`. Lifestyle backgrounds are fine for `additional_image_link` (up to 10).
- **`lifestyle_image_link`:** add at least one — products with lifestyle imagery see ~27% higher CTR per Google's own data.
- For a florist, the practical setup: primary image on white seamless (the bouquet alone), 2–4 additional images showing scale (held by hand, in the recipient's home, on a table). Avoid heavy filters or overlay text — overlay text is a disapproval trigger.

---

## Step 3 — Verify GMC + set shipping/tax

In Merchant Center Next (`merchants.google.com`):

1. **Settings → Business information** → confirm legal name, address (463 Fort Washington Ave, New York, NY 10033), phone, customer service email.
2. **Settings → Website** → verify `primaveraflowers.com` (or current storefront domain). Shopify auto-verifies via OAuth handshake; if it fails, fall back to HTML tag (paste into theme.liquid `<head>`) or DNS TXT record.
3. **Settings → Shipping and returns → Shipping services** — confirm Shopify-imported zones are correct. For same-day delivery, set a flat rate or free-over-threshold rule that mirrors Shopify checkout exactly. **Mismatched shipping is the #1 cause of GMC suspensions for florists.**
4. **Settings → Shipping and returns → Return policy** — must match Shopify's published policy. For perishables, "no returns; replacement within 24h on quality issues" is acceptable.
5. **Settings → Tax** (US) — leave on "automatic"; Shopify passes tax through.
6. New 2026 requirement: GMC may trigger **video verification** at signup or post-suspension. You record a short walkthrough showing the storefront, products, and packing. Only 3 attempts allowed before permanent suspension — read the prompt carefully if it appears.

---

## Step 4 — Local inventory feed: skip for now

**Recommendation: do NOT set up the local inventory feed in the first 60 days.**

Reasoning:
- LIA's value prop is "Pickup today / In stock nearby" surfaces. PFWH has 1 storefront and most flowers are made-to-order — pickup-today inventory is fuzzy.
- LIA setup requires: separate local inventory feed, in-store availability data, store code, and (for "Pickup today") an order-ahead mechanism. Real cost: 5–10 hours of setup + ongoing inventory accuracy work.
- At $500–$1,000/mo, marginal LIA lift ≠ worth the lift. The same impressions are reachable through a well-tuned Google Business Profile + standard PMax with location-targeting.

**What to do instead:**
- Make sure the **Google Business Profile** for 463 Fort Washington Ave is claimed, fully filled out, has products listed, and is linked to GMC (Settings → Linked accounts → Google Business Profile). This unlocks the "available at this location" annotation on your shopping ads for local searchers — most of the LIA-style benefit at zero ongoing maintenance.
- Revisit LIA at $3K+/mo or after launching a real walk-in / pickup-today merchandising program.

Confidence: high on skip recommendation for this budget tier.

---

## Step 5 — Launch Performance Max campaign(s)

### Campaign architecture for $500–$1,000/mo

Three-campaign hybrid is the 2026 practitioner consensus, even at low budget:

1. **Brand Search** (exact + phrase match on "primavera flowers", "primavera washington heights", etc.) — $3–$5/day. Defensive; keeps competitors off your name.
2. **Performance Max — All Products** — $20–$25/day (~70–75% of total). One PMax campaign, single product feed (no listing-group splits to start), 2–3 asset groups by occasion theme.
3. *(Optional, only if budget = $1,000)* **Non-brand Search** on high-intent occasion terms ("birthday flowers nyc", "same day flower delivery washington heights") — $5/day. Skip at $500/mo.

**Why not all-PMax?** PMax cannibalizes brand search and reports inflated ROAS by claiming brand conversions. With a separate brand campaign + brand exclusions on PMax, you keep clean attribution and still let PMax hunt non-brand demand.

### Brand exclusions on PMax

Critical step. In Google Ads:
1. **Tools → Shared library → Brand lists** → create list `Primavera brand` containing "Primavera Flowers", "Primavera Flowers Washington Heights", "primaveraflowers.com", common misspellings.
2. On the PMax campaign: **Settings → Brand exclusions** → add the brand list. This routes brand queries to your dedicated Brand Search campaign.

### PMax exact settings

- **Campaign objective:** Sales
- **Conversion goal:** Purchase (account-default), with Purchase value as the primary signal
- **Bid strategy:** **Maximize Conversions** for the first 3–4 weeks (until ~30 conversions logged), then switch to **Target ROAS** at a target slightly below your observed ROAS (e.g., if achieving 3.0 ROAS, set tROAS = 250%). Do NOT start with tROAS — you'll starve volume.
- **Budget:** $25/day on $750/mo plan; $20/day on $500/mo. PMax penalizes mid-flight budget changes >20%, so set the right number from day 1.
- **Locations:** Target by ZIP — 10032, 10033, 10034, 10040 + adjacent (10031, 10039, 10025, 10027, 07024 Fort Lee). Use **"Presence: People in or regularly in your targeted locations"** — NOT "interest in" (too broad, wastes budget).
- **Languages:** English + Spanish (Washington Heights is heavily Dominican; dia-de-las-madres products earn this).
- **Final URL expansion:** OFF for the first 30 days. Forces PMax to send traffic only to the URLs in your asset groups, prevents random product/blog page targeting.
- **Customer acquisition:** ON, "Bid for new customers only" OFF (you want both new + returning). Set new-customer value at ~$15–$25 (rough LTV-AOV delta).
- **Ad schedule:** All day; let the algorithm learn. Florist demand spikes Thu–Sat and pre-occasion windows; don't dayparting at this scale.
- **Devices:** All. Mobile dominates floral (~75%).

**Will PMax exit learning at this budget?** Threshold cited as ~30 conversions/30 days at campaign level. AOV ~$80, target CPA ~$25 → ~30 conv = ~$750 spend. **Just barely workable at $750/mo, tight at $500/mo.** Confidence: medium. Plan for a 6–8 week learning window, not the quoted 2–4. If after week 6 you have <20 conversions, the budget is the constraint, not the campaign — increase or pause non-PMax spend.

---

## Step 6 — Asset groups + creative requirements

Three asset groups in the single PMax campaign, each tied to an occasion cluster + listing-group filter on `custom_label_0`:

| Asset Group | Listing filter | Theme |
|---|---|---|
| **Everyday & Romance** | `custom_label_0 IN [birthday, anniversary, just-because, everyday]` | "Make their day. Hand-arranged in Washington Heights." |
| **Sympathy & Get Well** | `custom_label_0 IN [sympathy, get-well]` | "Thoughtful arrangements, delivered with care." Softer tone, no urgency-promo language. |
| **Cultural & Seasonal** | `custom_label_0 IN [quinceanera, dia-de-las-madres, new-baby]` | Bilingual headlines; lean on Washington Heights / Dominican community signals. |

**Creative minimums per asset group** (Google's required asset counts):
- 5 headlines (30 char), at least 1 ≤15 char ("Same-Day Flowers")
- 5 long headlines (90 char)
- 5 descriptions (90 char), at least 1 short
- 1 business name
- 4 logos (1:1 + 4:1)
- 20 images: 1.91:1 landscape, 1:1 square, 4:5 portrait — mix product-on-white + lifestyle
- **At least 1 video.** If you don't have one, Google auto-generates from images, but a real 6–15 second vertical video of an arrangement being assembled outperforms auto-gen meaningfully. New 2026: Asset Studio (Imagen 4 / Veo 3) can generate one inside Google Ads — acceptable as a starter, replace with real footage by week 4.

**Audience signals** (NOT targeting, just hints to the algorithm):
- Custom segment: people who searched "flower delivery nyc", "florist near me", "sympathy flowers manhattan"
- Your customer list (upload Shopify customer email export — needs ~1,000+ to be usable; confidence: low at PFWH's likely list size, can skip)
- Detailed demographics: parents, in a relationship — lightly weighted

---

## Initial test plan ($500–$1,000/mo)

### Week 0 (setup, no spend)
- Steps 1–4 complete
- Feed clean in GMC (zero red errors; warnings OK)
- Brand exclusions list built
- 3 asset groups built with all required assets
- Conversion tracking firing (see Tracking section below)

### Week 1–2 (learning)
- PMax live at $20–$25/day, Brand Search at $3–$5/day
- **Do not touch settings.** Budget changes >20% reset learning. No bid strategy changes. No asset edits beyond replacing a flat-out broken asset.
- Watch GMC daily for disapprovals — fix as they arrive.
- Expect: 0–10 conversions, CPA possibly 2–3× steady state.

### Week 3–4 (early signal)
- Look at search terms via the Insights tab (PMax doesn't show full search terms, but "search categories" and "search themes" surface).
- Add **negative keywords at account level** (Shared library → Negatives): `wholesale`, `silk flowers`, `artificial`, `1800flowers`, `teleflora`, `from from` (typo bots), `free`, `cheap` — competitor brands and low-intent.
- If ≥30 conversions logged, switch PMax bid strategy to Target ROAS at 80% of observed ROAS.

### Week 5–8 (optimize)
- Asset-level reporting: kill any image/headline marked "Low" if its sibling assets are "Good"/"Best."
- Search-theme refinement: add 3–5 search themes per asset group to push the algorithm toward your priority queries.
- Consider Merchant Promotions (next section) if you're running any first-purchase or "free vase with $75+" offers.

### Budget split snapshot
| Budget | PMax | Brand Search | Non-brand Search |
|---|---|---|---|
| $500/mo | $400 ($13/day) | $100 ($3/day) | — |
| $750/mo | $600 ($20/day) | $100 ($3/day) | $50 ($2/day) |
| $1,000/mo | $750 ($25/day) | $100 ($3/day) | $150 ($5/day) |

---

## Optimization checklist (week 2–4)

- [ ] All products in feed `Approved` (not just `Pending`)
- [ ] Top 10 bestsellers have ≥1500×1500 hero image + lifestyle image
- [ ] `google_product_category = 2899` on all bouquets/arrangements
- [ ] `identifier_exists = no` on all handmade SKUs
- [ ] All 5 custom labels populated on every product
- [ ] Brand exclusion list active on PMax
- [ ] At least 1 conversion firing per day on average
- [ ] Negatives added: competitor brands + "wholesale" + "silk" + "artificial" + "DIY"
- [ ] **Merchant Promotions** feed enabled if running discounts (Discounts → Manage → Google & YouTube channel toggle on the discount). Eligible promos: % off, fixed amount off, free shipping over threshold. PFWH first-time-buyer discount is a fit.
- [ ] **Sitelink extensions** (campaign-level) for: Birthday Flowers, Sympathy Arrangements, Same-Day Delivery, Subscription Service
- [ ] **Seller ratings**: requires 100+ verified reviews in past 12 months and ≥3.5★. PFWH likely doesn't qualify yet; install a verified review collector (Yotpo, Okendo, Judge.me with Google Reviews integration) and seed reviews from existing customers. Don't expect seller ratings to show until ~month 3.

---

## Common pitfalls (florist-specific)

1. **Sympathy/funeral disapprovals** — Google has stricter content policies for ads targeting bereaved users ("personal hardships" policy). Avoid pressure language ("Don't miss the funeral!", "Last chance"). Use respectful copy ("Thoughtfully arranged," "Delivered with care"). Sympathy products themselves are allowed; the ad copy is what gets flagged. Confidence: medium on exact triggers — Google doesn't publish a florist-specific list.
2. **"Same-day" as a claim** — Allowed if you can actually deliver same-day for orders placed before a cutoff. Put the cutoff in the description, not the title ("Order by 1 PM for same-day NYC delivery"). Untrue same-day claims = misleading-ad disapproval.
3. **"Local" / "near me" in titles** — Fine if true. Avoid "#1 florist in NYC" / "best florist" superlatives without third-party citation — "unsupported claims" disapproval.
4. **"Starting at $X" in titles** — Disapproval for "promotional text in title." Use the actual product price; let Google show sale_price natively.
5. **Shipping mismatch suspensions** — Shopify zones must equal GMC shipping rules. Check after every shipping change in Shopify.
6. **Subscription SKUs** — Google Shopping doesn't natively handle recurring; submit the first delivery as a one-time price. Use `subscription_cost` attribute if you want to advertise the recurring nature (optional, advanced).
7. **Add-on products in the feed** — Either exclude (`excluded_destination = Shopping_ads`) so $5 cards don't waste impressions, or assign to a low-priority listing group.
8. **Spanish-language landing pages** — If you run bilingual asset groups but the storefront is English-only, you'll see a mismatch in PMax reporting. Either localize key landing pages or note this as an expected drag.

---

## Tracking + measurement

**Recommended stack (one of two paths):**

**Path A — Native (simplest, recommended for $500–$1,000/mo):**
- Shopify Google & YouTube channel handles Google Ads conversion tag (purchase event with value, currency, transaction_id) and GA4 ecommerce events automatically.
- Enable enhanced conversions in Google Ads → Tools → Conversions → enhanced conversions ON. Lifts attributed conversions ~5–15%.
- Don't run a parallel GTM-based GA4 setup at the same time — duplicate events ruin reporting.

**Path B — GTM server-side (only if migrating to a real measurement stack):**
- Install GA4 + Google Ads via GTM Web container, disable the Shopify Google channel's GA4 toggle to prevent duplication.
- Use Shopify's Customer Events + Pixels API for checkout-extensibility-compatible events.
- Server-side container via Stape or self-hosted for iOS/cookie loss recovery. Overkill for $500/mo budget; revisit at $5K+/mo.

**Must-fire events:**
- `purchase` (with value, currency, items[], transaction_id) — primary conversion
- `begin_checkout`, `add_to_cart` — secondary signals (PMax uses these for audience optimization even when they're not the primary conversion goal)
- `view_item` — for cart-abandoner remarketing

**Conversion windows (2026 defaults):** click-through 30 days, view-through 1 day for Display/YouTube. Leave default unless you have a specific reason to change.

---

## Sources

- [Shopify Help: Set up Google & YouTube channel](https://help.shopify.com/en/manual/online-sales-channels/google/getting-setup/connect)
- [Shopify Help: Google & YouTube channel requirements](https://help.shopify.com/en/manual/online-sales-channels/google/requirements)
- [Shopify Help: Syncing your products](https://help.shopify.com/en/manual/online-sales-channels/google/getting-setup/syncing-products)
- [Google Merchant Center Help: identifier_exists](https://support.google.com/merchants/answer/6324478?hl=en)
- [Google Merchant Center Help: GTIN](https://support.google.com/merchants/answer/6324461?hl=en)
- [Google Merchant Center Help: google_product_category](https://support.google.com/merchants/answer/6324436?hl=en)
- [Google Merchant Center Help: image_link](https://support.google.com/merchants/answer/6324350?hl=en)
- [Google Merchant Center Help: lifestyle_image_link](https://support.google.com/merchants/answer/9103186?hl=en)
- [Google Merchant Center Help: Sale price and promotions for Shopify](https://support.google.com/merchants/answer/14232690?hl=en)
- [Google Ads Help: Apply brand exclusions to Performance Max](https://support.google.com/google-ads/answer/14505308?hl=en)
- [Google Ads Help: Custom labels for Shopping ads](https://support.google.com/google-ads/answer/6275295?hl=en)
- [Search Engine Journal: Performance Max for Ecommerce — Hybrid Strategy](https://www.searchenginejournal.com/performance-max-for-ecommerce-the-hybrid-strategy-thats-actually-working/571885/)
- [Search Engine Land: Top Performance Max optimization tips for 2026](https://searchengineland.com/top-performance-max-optimization-tips-461913)
- [Store Growers: Performance Max Campaigns Ultimate Ecommerce Guide 2026](https://www.storegrowers.com/performance-max-campaigns/)
- [Channable: PMax Best Practices 2026](https://www.channable.com/blog/performance-max-campaigns-best-practices)
- [Optmyzr: How to Optimize Performance Max in 2026](https://www.optmyzr.com/guide/performance-max/)
- [PPC Mastery: Brand Exclusions in PMax](https://www.ppcmastery.com/blog/tpe-49-brand-exclusions-how-to-exclude-brand-from-pmax)
- [ALM Corp: Google 1500×1500 Image Recommendation Guide 2026](https://almcorp.com/blog/google-1500x1500-image-recommendation-product-feeds/)
- [ALM Corp: Google Shopping API Migration Deadlines 2026](https://almcorp.com/blog/google-shopping-api-migration-deadline-2026/)
- [Productcategory.net: Fresh Cut Flowers (2899)](https://productcategory.net/finder/arts-and-entertainment/party-and-celebration/gift-giving/fresh-cut-flowers/)
- [Wiserreview: Google Seller Ratings 2026](https://wiserreview.com/blog/google-seller-ratings/)
- [COREPPC: GA4 Conversion Tracking for Shopify 2026](https://coreppc.com/blog/ga4-conversion-tracking-shopify-2026/)
- [Feedonomics: Google Local Inventory Ads Setup](https://feedonomics.com/blog/local-inventory-ads/)
