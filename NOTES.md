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
