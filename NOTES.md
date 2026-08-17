# Working notes

Decisions and findings that aren't obvious from the code. Keep short.

## Email signup — parked, and here's why (Aug 2026)

The handoff listed this as "awaiting an answer from Wix support." It's resolved:
**there is no client-side-only path into Wix Contacts.**

Both candidate endpoints require an admin-level scope:

| Endpoint | Permission | Scope |
|---|---|---|
| `POST /email-marketing/v1/email-subscriptions` | `EMAIL_SUBSCRIPTIONS.MODIFY` | admin |
| `POST /v4/submissions` (Wix Forms) | `WIX_FORMS.SUBMISSION_CREATE` | `SCOPE.DC-FORMS.MANAGE-SUBMISSIONS` |

A static site on GitHub Pages cannot hold a secret — anything in the page source
is public. So any route into Wix needs something server-side in front of it.

Options, if this is ever picked back up:

1. **Cloudflare Worker proxy** (recommended). ~30 lines, free tier. Form stays in
   our design and posts to the Worker; the Worker holds the API key and writes
   the contact. The key is pasted into Cloudflare's dashboard by the owner —
   it should never be sent through chat or committed here.
2. **Wix form embed.** No code, no secret, but an iframe with foreign styling.
3. **Formspree/Basin + Zapier.** No code, two more subscriptions.

Parked in Aug 2026: the business doesn't send many campaigns, so a signup form
feeding a rarely-mailed list wasn't worth the moving parts.

## Photos are now served by the site itself (Aug 2026)

All 29 photos were pulled out of the Wix CDN, resized to 1200px max and
converted to WebP, and committed to `assets/photos/`. 8.6 MB of originals became
2.4 MB. Several were 3264px originals the browser was shrinking on every visit.

**The originals were not touched.** They're still in the Wix Media Manager;
these are resized copies. Nothing there was moved or deleted.

Filenames are the Wix media hash — `photo_id()` in `build.py` derives it, so a
`PHOTOS` entry still reads as its Wix name and the local file is found from it.
To add a photo: upload to Wix as usual, then pull it down the same way (there's
a one-off script in the session scratchpad, easy to rewrite) or drop the file
straight into `assets/photos/` named after its hash.

`build.py` reads each WebP's real dimensions at build time via `webp_size()`, a
hand-rolled header parser, so every `<img>` carries width and height and the
page doesn't jump as photos load. No image library needed on CI — see below for
where the resizing actually happens.

## Adding photos without touching code

This is the route a non-technical person uses, and it is the one to keep
working. Upload a photo to `assets/photos/pages/<page-slug>/` on github.com and
it appears on that page. No build.py edit, nothing installed, works from a phone
browser. `assets/photos/pages/README.md` is written for that person — keep it in
plain language.

Three pieces make it work:

- **`dropped_photos()`** scans the folder at build time. Files with `@` in the
  stem are skipped, because those are the responsive versions of a photo already
  in the list — without that guard they render as duplicate cards.
- **The filename is the alt text.** `alt_from_filename()` strips a leading `01-`
  ordering prefix, swaps dashes and underscores for spaces, and capitalises.
  This is the load-bearing trick: it gets real alt text out of somebody who will
  never fill in an alt-text field.
- **`.github/workflows/optimize-photos.yml`** runs `tools/optimize_dropped.py`
  on any push touching that folder: Pillow converts to WebP, caps at 1200px,
  writes `@800`/`@400`, deletes the original and commits back. It skips its own
  commits (`github.actor != 'github-actions[bot]'`) or it would loop forever.

**The build never depends on that Action having run.** `image_size()` reads
JPEG and PNG headers as well as WebP, so a raw phone photo builds correctly —
just heavier for the minute before the optimised version lands. Verified by
building with a 249 KB JPEG in place, then again after conversion.

Paths are percent-encoded in `photo_tag()`. Dropped filenames contain spaces,
and a raw space in a `srcset` is not merely untidy — the spec splits candidates
on whitespace, so it breaks the entire set.

## Adding a photo — tools/prep_photos.py (curated photos)

The site build stays dependency-free on purpose. All resizing happens in
`tools/prep_photos.py`, which runs **locally, never on CI**, and commits its
output:

```
pip install pillow
python3 tools/prep_photos.py add ~/Downloads/IMG_1234.jpg storefront-yukon
python3 tools/prep_photos.py derive     # rebuild derivatives for everything
```

For each photo it writes `<name>.webp` capped at 1200px, plus `<name>@800.webp`
and `<name>@400.webp`. `photo_tag()` looks for those two on disk and emits a
`srcset` when they exist, so a phone downloads the 400px file to fill a 356px
card instead of a 1200px one. Measured over five pages: 1407 KB before, 991 KB
on a retina phone, 410 KB on a standard-density one.

**It never upscales.** A source narrower than a derivative width is skipped, and
a photo with no derivatives gets a plain `src` — so the srcset path and the
no-srcset path are both correct and CI still needs no image library.

Source resolution is the one thing the tool can't fix. `storefront-south-okc`
(188×314) and `ceiling-fans-aisle` (188×189) came in as thumbnails and look soft
on a high-DPI phone. If full-size originals ever turn up, `prep_photos.py add`
over the same name is the whole job — that is exactly how
`storefront-midwest-city` was fixed in Aug 2026, going from a 600×338 screenshot
to a 1206×677 original. It gained an `@800` derivative it could not previously
produce, and the phone file got *smaller* (17 KB → 15 KB) because the resize now
starts from real detail instead of an already-compressed thumbnail.

The Wix CDN resize transforms do work (`/v1/fill/w_800,h_600,q_80/` appended to
a media URL) if this is ever reversed.

**What Wix is still needed for:** the 4,000 contacts and email campaigns, and
hosting the live discountokc.com until DNS cutover. The website itself no longer
depends on it at all.

## Mobile is the primary surface (Aug 2026)

Phones are the biggest traffic source, so the site is measured at 390×844
before anything ships. Four things were fixed:

**The category strip was hiding seven of ten departments.** Ten categories need
1075px; a phone gives them 358px. Vanities, Flooring and Bath showed; Kitchen,
Patio, Lights & Fans, Tools, Other, Deals and Mulch sat off the right edge with
no fade, arrow or peeking chip to say the strip swipes. A phone visitor read the
store as a three-department shop. `.catnav::before/::after` are now edge fades,
toggled by `nav_script()` — `.catnav-more` while there is travel to the right,
`.catnav-less` to the left. Neither ever shows on desktop, where all ten fit.
`nav_script()` also centres the active pill, so deep categories like Mulch open
with their pill in view.

**Tap targets.** Category links were 37px, the top-bar links 20px, the masthead
Call button 42px — all under the 44px floor. All three are now 44px minimum. The
top bar grew ~48px doing it, which is acceptable because it is *not* sticky
(only `.masthead` is), so that cost lands once on the first screen.

**Type.** The top-bar links went 13px → 14px. The tagline beside them stays 13px
on purpose: at 14px "Tue–Sat 9–6, Sun 10–6" wraps and orphans the final "6".

**Breadcrumbs.** On a category page the current crumb repeated the H1 word for
word — up to 70 characters over two lines directly above the same words. It is
still in the DOM for crawlers, now clamped to one line with an ellipsis.

Use `padding-block`, not the `padding` shorthand, on anything inside `.wrap` —
the shorthand wipes `.wrap`'s `padding-inline: var(--gutter)` and the content
goes edge to edge on a phone.

## Still loaded from third parties

Nothing comes from Wix — all 29 photos are local and verified (29 referenced,
29 on disk, 0 HTTP failures, zero `wixstatic`/`wix.com` references in `build.py`
or in the build output). Two non-Wix dependencies remain:

| What | Where | Cost |
|---|---|---|
| Google Fonts CSS (Archivo, Public Sans, Spline Sans Mono) | every page | render-blocking third-party request before text paints |
| YouTube thumbnails (`i.ytimg.com`) | 16 images across 9 pages | a separate connection per thumbnail |

Self-hosting the three fonts into `assets/` is the higher-value of the two and
would make the site fully self-contained.

## AEO / GEO structure — the point of the whole site

The business ranks for its own name and almost nothing else. That is the
problem this structure exists to fix: somebody typing *how can I save money on
flooring* or *where do I buy discount ceiling fans in OKC* should land here, and
an answer engine asked the same thing should quote this site.

**Answer-first (BLUF) blocks are the unit of content.** A `sections` entry on a
page dict is `(question, bluf, [supporting])` and renders through
`sections_html()` as:

```
<div class="qa" id="…"><h2>the question somebody actually types</h2>
  <p class="bluf">the answer, 40–60 words, in the first sentence or two</p>
  …supporting detail…
</div>
```

Rules that matter, and why:

- **The H2 is the query, verbatim-ish.** Not "Flooring costs" but "How much does
  it cost to floor a house in Oklahoma City?" The old pages had no body headings
  at all — the only H2s on the entire site were "Questions, answered" and "Come
  see it in person", which is exactly why nothing but the brand name ranked.
- **Answer in the first 40–60 words, then context.** Never build up to it.
- **Entity-rich, not pronoun-rich.** Write "Jameson's Discount Home Improvement
  Warehouse stocks…" rather than "we stock…", and name Oklahoma City, the
  street addresses, the brands and the prices. A retrieval engine lifting one
  block has to get a complete answer with no antecedents to resolve.
- **Break out lists and tables.** `.qa` styles `<ol>` and `<table>`; wrap tables
  in `<div class="tablewrap">` so they scroll on a phone instead of pushing the
  page sideways.
- **Visible text first, schema second.** `faq_node()` builds FAQPage from the
  section questions *and* the FAQ accordion, and every entry is on the page as
  an `<h2>` or `<summary>`. `howto_nodes()` emits HowTo only where a numbered
  procedure is genuinely visible. Never add a schema answer with no visible
  counterpart — a build-time check for that is worth writing if this grows.

`robots.txt` names GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User,
Claude-SearchBot, PerplexityBot, Perplexity-User, Google-Extended, Applebot,
Applebot-Extended, Bingbot, CCBot, Amazonbot and meta-externalagent explicitly.
`User-agent: *` already allowed them; naming them is unambiguous to an auditor
and survives a future tightening of the wildcard.

**Done so far:** flooring, lighting and vanities carry answer-first sections.
**Still to do:** bath, kitchen, patio, tools, rubbermulchokc, bulk-rubber-mulch,
inventory, deals and the home page, which should become the pillar that links
down to each cluster.

## How the site talks

Humble and hard-working. State the thing and stop.

The failure mode to watch for is the clever summing-up clause — the sentence
that lands a point and then explains why it was a good point. "That's what
makes the math work." "That's what squares it." "Which is why X." "That's good
news if you do A and bad news if you do B." "That is the whole reason X beats
Y." None of that is how the owner talks, and it reads as AI filler. A pass in
Aug 2026 removed six of them.

Rewrite by saying the plain version: not "that is the whole reason LVP beats
tile on a budget: the material is cheaper here and the labor is you," but "on a
budget, LVP usually comes out ahead of tile: the material costs less and you
are not paying anyone to install it."

## Pricing model

The discounts are up front. The tag price is the low price — there is no sale
cycle to wait for and no coupon. A single item may go on sale in a given month,
but our prices are our prices. Don't write copy implying a weekly or seasonal
sale rhythm.

Two things that do move below the tag, both worth stating plainly and neither
advertised week to week:

- **10% military discount on brand-new running-line vinyl plank.** Current
  product, not closeout overage. Do not widen this to the whole store.
- **Take-all deals on the last of a line**, which on flooring can mean pallet
  pricing on a style or two.

**They do not stack.** Take-all and pallet prices are already cut well past 10%,
so the military discount does not come off on top of one. Every page that names
both has to say so, and both category FAQs carry the question outright, because
"can I combine these" is exactly the kind of thing a customer asks at the
counter after reading only one of them.

## Buying inventory — the B2B side

Half the business is buying, and the site says so on `about` and `contact`.
The facts, so nobody softens them into vagueness later:

- **Most inventory is bought outright and up front** — one price, one pickup.
  That is what a seller usually wants and it should stay the headline.
- **Consignment is the exception, not the pitch.** On specialty equipment,
  surplus construction material and job-site leftovers we will take goods on
  consignment and let the market set the price, because the value isn't clear
  until it's in front of buyers.
- **RTV and reverse logistics loads are routine.** Routing goods back up the
  supply chain is slow and expensive and product sits waiting its turn. We are
  the local infrastructure that clears the bottleneck. Big-box stores,
  manufacturers and distribution centers are the audience for that sentence.
- **Trailer clear-outs** — scratch-and-dent, **vendor buybacks** and the rest.
  It is *vendor*, never "bender". An autocorrect put "bender buybacks" on the
  page in Aug 2026 and it survived a round of review because it reads like trade
  slang. It isn't a term. The trade audience this paragraph is written for would
  have spotted it immediately.

Everything routes to `b2b@discountokc.com`. Keep that address on both pages.

## Campaign pages and per-page Google tags

Drop a dict into `CAMPAIGN_PAGES` near the top of `build.py` and the page
builds — masthead, category nav, footer, store schema and the mobile treatment
all come with it. Nothing else needs editing. A slug that collides with an
existing page fails the build rather than shadowing it.

```python
CAMPAIGN_PAGES = [dict(
  slug="fall-flooring-sale", title="…", desc="…", h1="…",
  paras=["…"], sections=[(q, bluf, [detail])], faq=[(q, a)],
  gtag=dict(ids=["AW-1234567890"], send_to="AW-1234567890/AbC_dEfGhIjK"),
  noindex=True,     # paid lander: built and reachable, kept out of the sitemap
)]
```

`gtag` also accepts a bare list — `gtag=["G-XXXXXXXXXX", "AW-1234567890"]` — for
measurement with no conversion event. The tag is emitted **only** on pages that
ask for it. The site carries no analytics by default and that is on purpose:
nothing to consent to, nothing blocking first paint.

### GA4 vs the Meta pixel — they are not alternatives

GA4 does capture every traffic source, so as *measurement* it is the right and
sufficient tool: it will tell you a visitor arrived from Facebook, from Google
organic, from an AI assistant, or direct. Nothing else is needed to answer
"where is traffic coming from".

What GA4 cannot do is talk back to Meta. The pixel exists to send conversion
signal into Meta's ad auction so delivery optimises toward people who convert,
and to build retargeting audiences. GA4 has no path into that system, and
Google's own tags have no path into it either.

So the rule is simple:

- **Not running Meta ads?** No pixel. GA4 already tells you what Facebook
  traffic did, and an unused pixel is a third-party script and a consent
  liability for nothing.
- **Running Meta ads?** Add `pixel=` to the pages in that campaign's path.
  Delivery optimisation is the entire reason, and it needs the signal.

```python
pixel="1234567890123456"
pixel=dict(id="1234567890123456", event="Lead")   # PageView always fires too
```

Same opt-in shape as `gtag`, same isolation — emitted only on pages that ask.
Meta's `<noscript>` fallback pixel is included.

The IDs are written into public page source, so only ever put real measurement
IDs in that field. This repo is public.

## Product snippets — what qualifies and what must not

Google splits product structured data in two. *Merchant listings* are for pages
a customer can buy from directly; *product snippets* are for pages they cannot.
Jameson's sells in store, so **product snippets are the correct class and
merchant listings are not** — do not add `priceValidUntil`, shipping or return
policy nodes trying to qualify for the merchant experience.

Two rules gate anything added to a page's `products`:

1. **The price must be visible on that same page.** Structured data has to match
   what the customer is shown. Every price below sits in a `.chip` at the top of
   its own page.
2. **The price must be standing, not a rotating lot.** A closeout vanity that
   sells on Saturday leaves stale markup behind.

That excludes most of the floor, correctly — there is no catalog and stock turns
weekly. Currently marked up:

| Page | Product | Offer |
|---|---|---|
| flooring | Waterproof rigid-core LVP | AggregateOffer $2.19–$2.69 |
| rubbermulchokc | Playground rubber mulch, 24-lb bag | $8.00 |
| rubbermulchokc | Bulk rubber mulch supersack, 2,000 lb | $601.00 |
| deals | Visions Workhorse latex paint, per gallon | $21.99 |

**The supersack is marked at its standing $601, not the $500 summer special.**
The special will lapse and stale markup on an expired price is worse than no
markup. Same reasoning for the $629 vanity on the deals page — a one-off
closeout, so no Product node.

## OPEN ISSUE — 405rubbermulch tags and Search Console duplicates

Raised Aug 2026, not yet resolved. This concerns the **other** repo
(`yamakessense/405rubbermulch-site`, the Hostinger-hosted 405rubbermulch.com),
but it is written here because that repo is push-disabled from this session and
because the two properties may be contaminating each other's data.

### Four Google tag IDs are firing on 405rubbermulch.com

Counted across its 13 HTML pages:

| ID | Type | On how many pages |
|---|---|---|
| `GT-WB72BHMG` | Google tag / container | 26 references |
| `AW-998556622` | Google **Ads** conversion account | 17 |
| `AW-18336005673` | Google **Ads** conversion account, a second one | 17 |
| `G-F6P1TCFK29` | GA4 property | 13 |

**Two separate Google Ads accounts are configured on one site.** The owner
reports that tags on 405rubbermulch are reporting into analytics accounts
belonging to *both* 405rubbermulch.com and discountokc.com.

If one of those AW accounts belongs to discountokc, then every 405rubbermulch
visitor is being counted in discountokc's Ads data, and conversion optimisation
on both accounts is learning from the wrong traffic. That is worth checking
before any more ad spend goes through either account.

**This cannot be settled from the code.** The HTML shows which IDs fire; only
the Google Ads and GA4 admin screens show which business each ID belongs to.
First step is to open Google Ads → account switcher and GA4 → Admin → Property,
and write down which of `AW-998556622`, `AW-18336005673`, `G-F6P1TCFK29` and
`GT-WB72BHMG` belongs to which domain. Then remove from each site the tags that
are not its own.

Note `AW-998556622` also appears in the discountokc-side history for a Google
Ads conversion tag task, which is a further reason to check it carefully.

Do not delete any tag until that mapping is confirmed. A deleted conversion tag
loses history silently.

### The Search Console "duplicate, not indexed" pages

Partly expected, partly a real gap.

**Expected, leave alone.** `.htaccess` on 405rubbermulch 301-redirects twelve
old area-code pages (`/405-area.html`, `/918-area.html`, …) into four state
pages. Those will always report as "Page with redirect". That is the redirect
working, not a fault.

**Also expected.** `.htaccess` has no www-vs-non-www or http-vs-https
canonicalisation rule, so Hostinger may answer on up to four URL variants per
page. Twelve of thirteen pages do carry `rel="canonical"` pointing at
`https://405rubbermulch.com`, so Google should fold the variants together and
report them as "Alternate page with proper canonical tag" — benign. Adding a
single 301 to the canonical host in `.htaccess` would tidy it up.

**A real gap.** `thank-you/index.html` is the **only page with no canonical
tag** — and it is the conversion page, the one carrying the Ads conversion
event. It should get one.

None of this affects discountokc.com. Its 15 pages each carry a canonical, and
the cutover keeps every URL identical.

## Never strip the head

Do not remove Google verification tags, tracking scripts, or meta tags when
editing `full_page()` or the 404/preview templates. Search Console for
discountokc.com is verified by **DNS TXT record**, not by an HTML tag (see
CUTOVER.md), so there is no verification meta tag in the markup today — but that
can change the moment somebody adds a second property or a tag manager, and a
verification tag deleted by accident is silent until rankings move.

Current head, per built page: 19 `<meta>` tags (viewport, description, robots,
Open Graph, Twitter card, theme-color) and 3–4 `<script>` tags (JSON-LD, search,
nav cue, and the video script on pages that carry one). No analytics or tag
manager is installed on this site at present.

## Condition language

The site used to claim inventory was "not seconds, not returns." It isn't — the
floor is a mix of closeout, overstock and scratch-and-dent, and the owner's
position is that everything has a place and a price. Don't reintroduce blanket
"all our product is X" claims; say most/some and disclose.

Never describe the business as a salvage yard or junkyard. It's a DIY closeout
store: running-line product, paint, rubber mulch, LVP, overstock and open-box.

## Things that must not change

15 URL slugs, FAQ wording (mirrored word-for-word into JSON-LD — `build.py`
generates both from one source, keep it that way), the NAP block, hours, and the
verified prices. The Yukon store is permanently closed and its old number,
405-494-0355, must never appear.

`BASE=/discountokc` and `WRITE_CNAME=""` stay as they are until DNS cutover. A
CNAME written while the site is on the temporary URL breaks the test URL.
