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
page doesn't jump as photos load. No image library needed on CI.

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
