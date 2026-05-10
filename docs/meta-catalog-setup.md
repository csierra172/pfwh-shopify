# Primavera × Meta Dynamic Catalog Ads — Setup Guide

Last verified: May 2026. Store: `pfwh-2.myshopify.com` (Savor theme). Brand: Primavera Flowers Washington Heights. Budget: $500–$1,000/mo.

> **Naming note (2024-2025 rebrands still in flux in 2026 UI):**
> - "Dynamic Product Ads (DPA)" is now **Advantage+ Catalog Ads**.
> - "Advantage+ Shopping Campaigns (ASC)" was renamed **Advantage+ Sales Campaigns** in 2025.
> - Both names still appear in Ads Manager menus depending on rollout.

---

## Step 1 — Install Meta Pixel + Conversions API on Shopify

Recommendation: start with the **native Shopify "Facebook & Instagram" sales channel** (free, dedupes automatically). Only graduate to Stape ($10/mo) or Elevar ($50/mo) if (a) you add Recharge or a 3rd-party checkout, (b) Events Manager shows match quality < 6.0, or (c) deduplication rate drops < 90%. For Primavera at $500–$1k/mo, native is correct. Confidence: high.

1. Shopify admin → **Settings → Apps and sales channels → Add sales channel** → install **Facebook & Instagram by Meta**.
2. Open the channel → **Set up to start selling → Start setup** under "Marketing on Facebook and Instagram."
3. Connect the Facebook account that owns the **Primavera Business Manager / Meta Business Suite**. If a BM doesn't exist, create one at business.facebook.com first.
4. Connect the **Ad Account**, the **Facebook Page** (Primavera Flowers WaHi), and the **Instagram Business account** (@primaveraflowersnyc).
5. Under **Data sharing settings**, choose **Maximum**. This enables Pixel + Conversions API together with automatic event_id deduplication. Do not pick "Standard" or "Enhanced."
6. Under **Customer data sharing**, accept Meta's terms.
7. Select the **Pixel** (or create one named `primavera-pfwh-pixel`).
8. Finish onboarding. Verify in Meta **Events Manager → Data Sources → [your pixel] → Overview**:
   - Events firing: `PageView`, `ViewContent`, `AddToCart`, `InitiateCheckout`, `Purchase`, `Search`.
   - Each shows "1 event from 2 sources" (Pixel + CAPI). If you see "1 event from 1 source," dedupe is broken — open a Shopify support ticket.
   - **Event Match Quality** target ≥ 6.5/10 per event.
   - **Deduplication rate** target ≥ 90%.
9. Default params Shopify sends automatically: `content_ids` (variant ID), `content_type` (`product` or `product_group`), `value`, `currency: USD`, `contents` (array with id/quantity/item_price), plus customer params (em, ph, fbp, fbc, client_ip_address, client_user_agent) for matching. **You do not need to manually configure event_id** — Shopify generates and matches it across browser + server.
10. Configure **Aggregated Event Measurement** (Events Manager → Settings → Web Events): rank Purchase #1, InitiateCheckout #2, AddToCart #3, ViewContent #4. Verify the production domain under **Brand Safety → Domains**.

---

## Step 2 — Connect the Shopify catalog to Meta Commerce Manager

The native sales channel auto-creates a catalog and pushes products. Sync is incremental and runs in minutes, not 24 hours — sufficient for same-day florist inventory. Confidence: high.

1. Open **Commerce Manager → Catalogs**. There should be a catalog named `Shopify – pfwh-2` already created by the sales channel.
2. Confirm catalog type = **E-commerce**, product source = **Shopify**, item count > 0.
3. **Catalog → Settings → Data Sources** — confirm "Shopify" is connected and "Last sync" is recent (< 60 min).
4. **When to override with a manual feed**: build a separate scheduled XML/CSV feed only if you need to (a) rewrite titles to bake in occasion, (b) split SKUs that share a Shopify product but should be distinct catalog items, or (c) inject `custom_label_*` fields the native sync doesn't expose. For v1, skip this — use native sync and inject metadata via tags + metafields (Step 3).

---

## Step 3 — Configure the catalog feed for florist data

Required: `id`, `title`, `description`, `availability`, `condition`, `price`, `link`, `image_link`, `brand`. Recommended: `product_type`, `google_product_category`, `custom_label_0..4`, `additional_image_link`, `sale_price`, `item_group_id`.

### Florist-specific field guidance

- **`title`** (max 200 chars, ~65 displayed): formula `[Occasion] [Flower/Style] — [Size] | Same-Day NYC Delivery`. Examples:
  - `Sympathy White Roses Bouquet — Premium | Same-Day NYC Delivery`
  - `Mother's Day Pink Peonies — Standard | Same-Day Delivery WaHi`
  Bake the occasion into the title; Meta's relevance ranker reads it heavily.
- **`description`** (max 9999, ~150 useful): lead with delivery zone + cutoff time. "Hand-arranged in Washington Heights NYC. Order by 2 PM for same-day."
- **`condition`**: `new` for all SKUs.
- **`availability`**: `in stock`. For sold-out same-day items, use `out of stock` so Meta auto-pauses the ad rather than showing a dead SKU.
- **`brand`**: `Primavera Flowers WaHi` (consistent string — used by some product sets).
- **`google_product_category`**: `2802` (Home & Garden > Plants > Flowers). For plants/houseplants: `985`.
- **`product_type`** (your taxonomy, free text): use Shopify product type. Examples: `Flowers > Bouquets > Roses`, `Flowers > Sympathy`, `Subscriptions`, `Add-ons`.

### Custom labels for Primavera

| Label | Use for | Values |
|---|---|---|
| `custom_label_0` | Occasion | `birthday \| sympathy \| anniversary \| just-because \| get-well \| new-baby \| quinceanera \| dia-de-las-madres \| mothers-day \| bestseller` |
| `custom_label_1` | Price tier | `under-60 \| 60-100 \| 100-150 \| 150-plus` |
| `custom_label_2` | SKU type | `arrangement \| subscription \| addon \| plant` |
| `custom_label_3` | Season | `evergreen \| spring \| mothers-day \| valentines \| holiday` |
| `custom_label_4` | Margin tier | `high \| mid \| low` (set later from your COGS sheet) |

### How to populate `custom_label_*` with native Shopify sync

Shopify's Facebook channel doesn't expose all five custom labels directly. Two options:

- **Option A (simplest)**: rely on Shopify **tags** + **product type**. Then in Commerce Manager, build product sets using filters on `Product Type Contains` and `Description Contains` and tag-equivalent fields. Works for occasion segmentation without metafields.
- **Option B (cleaner)**: install a feed enrichment app — **Flexify** or **Socialhead** — and map Shopify metafields in namespace `facebook` (keys `custom_label_0..4`) onto Meta catalog fields. Pick this if you need labels 1–4 above.

### Product Sets to build now

Build these in **Commerce Manager → Catalog → Sets → Create Set**. They become the targeting unit for ad sets:

1. **All Bouquets** — Product type contains `Bouquet`, exclude `subscription` and `addon`.
2. **Bestsellers** — tag/`custom_label_0` = `bestseller`.
3. **Sympathy** — `custom_label_0` = `sympathy`.
4. **Birthday** — `custom_label_0` = `birthday`.
5. **Anniversary** — `custom_label_0` = `anniversary`.
6. **Mother's Day** (seasonal) — `custom_label_0` = `mothers-day` OR `dia-de-las-madres`.
7. **Roses** — `custom_label_0` = `roses` OR title contains "Roses".
8. **Subscriptions** — `custom_label_2` = `subscription`.

---

## Step 4 — Build retargeting + prospecting audiences

In **Audiences → Create Audience → Custom Audience → Website**. Source = the Pixel from Step 1.

Florist-gifting tip: shorter windows than typical e-commerce. Buying intent is event-driven (birthday, condolence) and decays in days, not months.

| Audience | Definition | Use for |
|---|---|---|
| **VC-7** | `ViewContent` last 7 days, exclude Purchasers-30 | Hot retarget |
| **VC-30** | `ViewContent` last 30 days, exclude Purchasers-30 | Mid retarget |
| **ATC-14** | `AddToCart` last 14 days, exclude `Purchase` last 14 | High-intent abandoners |
| **IC-7** | `InitiateCheckout` last 7 days, exclude `Purchase` last 7 | Hottest abandoners |
| **Purchasers-180** | `Purchase` last 180 days | Exclusion + LAL seed |
| **IG/FB Engagers-90** | Engaged with IG account or FB Page last 90 days | Soft retarget / warm prospecting |
| **LAL 1% Purchasers** | Lookalike (US, 1%) off Purchasers-180 | Build only when seed has ≥ 100 records (≥ 500 ideal) |

For prospecting at this budget, **broad Advantage+ audience with location restriction** beats interest-stacking. Lookalikes are a fallback only after the purchase audience matures. Interest layering (e.g. "Florist," "Anniversary," "1-800-Flowers") is no longer recommended at this spend level after Meta's June 2025 detailed-targeting consolidation.

---

## Step 5 — Launch Advantage+ Catalog Ads campaign

Use **two campaigns** at this budget — one prospecting, one retargeting. A single Advantage+ Sales campaign with broad targeting can work but at $500–$1k/mo it under-spends retargeting where ROAS is best for a local florist.

### Campaign A — Catalog Retargeting (Advantage+ Catalog Ads)

1. **Campaign objective**: Sales.
2. **Buying type**: Auction.
3. Toggle **"Use a catalog"** ON. Choose `Shopify – pfwh-2`.
4. Campaign name: `PFWH | Retargeting | Catalog | YYYY-MM`.
5. **Campaign budget**: ABO (Ad Set Budget) so you can split across two retargeting ad sets.
6. **Ad sets** (two):
   - **AS1 — Hot Abandoners**. Budget $7/day. Product set: **All Bouquets**. Audience: ATC-14 ∪ IC-7, exclude Purchasers-30. Location: United States (do not narrow — this audience is already pre-qualified). Optimization: **Conversions → Purchase**. Attribution: 7-day click / 1-day view.
   - **AS2 — Browsers**. Budget $5/day. Product set: **All Bouquets**. Audience: VC-30, exclude ATC-14, exclude Purchasers-30. Same location/optimization as AS1.
7. **Ad level**: Format = **Carousel** with **"Use info from your catalog"** ON. Meta auto-pulls images, names, prices. Add 1 manual creative card at position 1 (lifestyle hero) — Meta lets you pin a fixed card; the rest are dynamic.

### Campaign B — Catalog Prospecting (Advantage+ Sales Campaign)

1. **Campaign objective**: Sales.
2. Toggle **Advantage+ Sales Campaign** ON (formerly ASC). Select the catalog.
3. Campaign name: `PFWH | Prospecting | Adv+Sales | YYYY-MM`.
4. **Campaign budget (CBO)**: $15–$25/day to start.
5. **Audience controls** (the new 2025 ASC fields): age 28–65, gender all, **language English + Spanish** (WaHi is heavily Spanish-speaking — Día de las Madres / quinceañera SKUs depend on this).
6. **Existing-customer budget cap**: 15% so most spend goes to prospecting.
7. **Location**: see geo section below.
8. **Ad set**: only one is allowed in Advantage+ Sales. Product set: **Bestsellers** OR **All Bouquets** (start with Bestsellers — narrower set converges faster on small budgets).
9. **Placements**: Advantage+ Placements ON.
10. **Ad level**: Carousel from catalog + 1 vertical Reel-format video card if available.

### Geographic targeting (applies to both campaigns)

- **Recommended**: pin-drop on `463 Fort Washington Ave, New York, NY 10033` with a **10-mile radius**, **People living in or recently in this location**. Covers the 5-borough core + Northern NJ commuters who buy for NYC recipients.
- **Why not 5 miles**: at 5 miles around 463 FWA you cover WaHi/Inwood/Harlem/parts of Bronx/Englewood — too small for Advantage+ to find 50 conversions/week to exit learning. Algorithm starves.
- **Why not "NYC metro"**: bleeds into Long Island / Westchester where you can't deliver same-day, wastes spend.
- **Advantage+ caveat**: Advantage+ Sales **honors location restrictions** but de-prioritizes other signals. The 10-mile radius is respected.

---

## Step 6 — Creative requirements

### Specs (2026)

- **Square 1:1**: 1080×1080, JPG/PNG, < 30MB. Default for Feed catalog cards.
- **Vertical 9:16**: 1080×1920 for Reels/Stories. Leave ~250px top/bottom safe zone for UI chrome (profile, CTA bar). Avoid copy in those bands.
- **Carousel**: all cards must share aspect ratio. 1:1 is the safest cross-placement default.
- **Min image res**: 600×600; Meta will throttle delivery on smaller. Aim 1080×1080 minimum.
- **Format choice**: **Carousel auto-generated from catalog** is current best practice for DPA — single-image DPA is deprecated in practice.

### Dynamic copy templates

Use the `{{product.name}}` / `{{product.price}}` macros in primary text:

- **Retargeting**: *"Still thinking about {{product.name}}? Same-day NYC delivery if you order by 2pm. From {{product.price}}."*
- **Prospecting**: *"Hand-arranged in Washington Heights. {{product.name}} — {{product.price}}. Same-day delivery across NYC."*
- **Sympathy set** (separate ad): *"Thoughtful arrangements, delivered same-day in NYC. {{product.name}} from {{product.price}}."* — keep tone restrained, no urgency CTAs.
- **Mother's Day**: *"For Mom — {{product.name}}. Order by Saturday for Sunday delivery."*

CTA button: **Shop Now** (default). For Sympathy, **Learn More** is gentler and tests better in some accounts.

---

## Initial test plan ($500–$1,000/mo)

Assume $1,000/mo = ~$33/day total.

| Week | Action |
|---|---|
| **Week 1 (learning)** | 70/30 prospecting/retargeting → Retargeting $10/day ($7 + $3), Prospecting $23/day. Do not change anything for 7 days unless spend < 50% of budget or no impressions in 24h. |
| **Week 2** | Review. If retargeting CPA is materially below prospecting (likely), shift to 60/40 prospecting/retargeting. If retargeting volume is choked (audience < 1k), keep 70/30. |
| **Week 3** | Introduce **Sympathy** ad set in retargeting (separate creative, separate copy). Add **Mother's Day** product set if within 30 days of holiday. |
| **Week 4** | If Purchasers-180 ≥ 100, build LAL 1% and add as 3rd prospecting ad set at $5/day. Evaluate after 7 days. |

**At $500/mo**: collapse to one retargeting ad set (combined ATC ∪ IC ∪ VC-7) and one Advantage+ Sales prospecting campaign. Same logic, smaller surface.

### Benchmarks (goalposts, not contracts)

Florist-specific public data is thin — confidence: low.

- **Target ROAS**: 2.5–3.5x blended. Retargeting will run 5–8x, prospecting 1.5–2.5x.
- **Target CPA**: $20–$35 against AOV $80.
- **Min data threshold to exit learning phase**: 50 optimized events per ad set per week (Meta's stated floor). At $33/day this is achievable only on the retargeting side; prospecting will likely stay in extended learning — accept that.

---

## Optimization checklist (week 2–4)

- [ ] Events Manager: dedupe rate ≥ 90%, EMQ ≥ 6.5 on Purchase. Fix CAPI before tuning ads.
- [ ] Catalog: 0 disapproved items. Check **Commerce Manager → Catalog → Issues** weekly.
- [ ] Frequency: retargeting < 4/week. If higher, rotate creative or widen window.
- [ ] Creative fatigue: CTR drops > 25% week-over-week → swap top card.
- [ ] Audience overlap: prospecting ↔ retargeting overlap < 20% (Audiences → Show Audience Overlap).
- [ ] Don't kill ad sets before 50 conversions or 7 days, whichever later.
- [ ] Don't edit budgets > 20% in a single change — resets learning.

---

## Common pitfalls (florist-specific)

- **Mother's Day spike eats learning.** The week before Mother's Day is 5–10x normal volume. If you launch a fresh campaign 7 days out, learning won't finish before the spike. **Fix:** launch the Mother's Day product set as a *new ad set inside the existing campaign* (inherits CBO learning), not a new campaign. Pre-warm 14 days out.
- **Sympathy ads disapproved or throttled.** Meta's classifiers occasionally flag funeral/sympathy creative under "personal attributes" or sensitive content. Avoid words like "loss" / "grief" in primary text; use "in remembrance" / "thoughtful." Keep imagery white/cream tones, no caskets/cemeteries. (A wedding florist had wedding floral content mis-flagged as child exploitation in Oct 2025 — appeals work but slowly.)
- **Wedding/quinceañera SKUs flagged for "personal attributes."** Don't write "Are you getting married?" / "Is your daughter turning 15?" — use third-person ("Quinceañera bouquets, hand-arranged in NYC").
- **Native Shopify CAPI dedupe failure.** If Events Manager shows 1-of-1 instead of 1-of-2, reconnect the Facebook channel. Don't layer Stape on top — you'll double-fire.
- **Same-day inventory mismatch.** If you sell out at 1pm, Meta's catalog needs `availability: out of stock` to stop showing the ad. Native sync is "few minutes" — mostly fine, but on Mother's Day weekend consider manually pausing the affected product set when bestsellers go OOS.
- **Geo too tight.** 5-mile radius around 463 FWA starves Advantage+. Use 10 miles minimum.
- **Spanish-language audience missed.** WaHi/Inwood is bilingual — set ad set Language to English + Spanish, and have at least one Spanish creative for `dia-de-las-madres` and `quinceanera` sets.
- **Detailed-targeting nostalgia.** Don't try to layer 5+ florist/wedding/anniversary interests post-June 2025 — Meta consolidated those categories and the ad set will under-deliver.

---

## Sources

- [Meta Conversions API setup, complete 2026 guide — DataAlly](https://www.dataally.ai/blog/how-to-set-up-meta-conversions-api)
- [Shopify Meta CAPI Setup, 2026 — PantoSource](https://pantosource.com/blog/shopify-meta-conversions-api)
- [Stape — Facebook Conversions API and Shopify](https://stape.io/blog/facebook-conversion-api-and-shopify)
- [Elevar — Meta CAPI for Shopify, 3 options](https://getelevar.com/shopify/implement-facebook-conversion-api/)
- [Meta Pixel deduplication with event_id explained — Conversios](https://www.conversios.io/blog/pixel-firing-no-conversions-fix/)
- [Event Deduplication for Meta Conversions — Analyzify](https://analyzify.com/hub/event-deduplication-for-meta-conversions)
- [Advantage+ Catalog Ads — Accelerated Digital Media](https://www.accelerateddigitalmedia.com/insights/what-are-meta-advantage-catalog-ads/)
- [About the Advantage+ Campaign Experience — Meta Business Help](https://www.facebook.com/business/help/1292656978738967)
- [Meta Advantage+ Shopping Campaigns Guide 2026 — Adligator](https://adligator.com/blog/meta-advantage-plus-shopping-campaigns-guide)
- [83 Changes to Meta Advertising in 2025 — Jon Loomer](https://www.jonloomer.com/meta-advertising-changes-2025/)
- [Facebook Product Feed Specifications 2026 — Adnabu](https://blog.adnabu.com/facebook/facebook-product-feed-specifications/)
- [Flexify — Custom Labels for Facebook product feed](https://www.flexify.net/help/custom-labels-premium-feature)
- [Flexify — Internal Labels and Product Sets on Meta](https://www.flexify.net/help/using-internal-labels-to-create-product-sets-on-meta)
- [Shopify Help — Publishing products on Facebook and Instagram by Meta](https://help.shopify.com/en/manual/online-sales-channels/facebook-instagram-by-meta/publishing-products)
- [Meta Carousel Ad Specs 2026 — AdManage.ai](https://admanage.ai/blog/meta-carousel-ad-specs)
- [Meta Ad Specs 2026 — Vizup](https://www.tryvizup.com/blog/meta-ad-specs-2026-every-dimension-size-you-need)
- [Prospecting vs Retargeting Budget Allocation — Adtriba](https://www.adtriba.com/blog/retargeting-prospecting-budget-allocation)
- [Meta Ads Retargeting Strategy Guide 2026 — Benly](https://benly.ai/learn/meta-ads/retargeting-strategies)
- [Meta Sensitivity Category Restrictions — Northbeam](https://www.northbeam.io/blog/meta-sensitivity-category-restrictions)
- [Geotargeting Strategies for Local Businesses — TheAdSpend](https://theadspend.com/resources/in-depth-analysis-geotargeting-strategies-for-local-businesses-on-facebook-google-and-linkedin-ads)

---

**Confidence notes:**
- Florist-specific CPA/ROAS benchmarks (Section: Initial test plan) — confidence low, no public data. Treat as hypotheses; validate on first 30 days.
- Sympathy/quinceañera classifier behavior — anecdotal post-Oct 2025 incidents only.
- Native CAPI dedupe via the Shopify channel — confidence high, well-documented.
- 10-mile geo radius vs 5-mile starvation — confidence medium-high; Meta docs are explicit on location as a hard constraint, but exact "starvation" thresholds are practitioner consensus, not Meta-published.
