# Where things stand — plain English

Written for Lyle, August 2026. No jargon. Read top to bottom.

---

## First: your backlinks, traffic and site history are not at risk

This is the thing you said you were worried about, so it goes first.

**You are not migrating the site. You are changing which computer answers the
phone.** Everything that makes Google trust discountokc.com is attached to the
*domain name* and to the *page addresses*, and neither of those changes.

Here is exactly why nothing is lost:

**Your page addresses stay identical.** All fifteen pages keep the same web
addresses they have now — `/flooring/`, `/vanities/`, `/rubbermulchokc/` and so
on. They were deliberately copied from your live Wix sitemap when the rebuild
started, character for character. When a link on somebody else's website points
at `discountokc.com/flooring/`, it still lands on a real page afterwards. No
broken links, no redirects needed, no "page not found."

**Your domain name stays the same.** Backlinks point at `discountokc.com`. That
does not change, so every link you have ever earned still points at you. Domain
age and history live with the domain, not with Wix.

**Your Google Search Console history stays.** Verification for discountokc.com
is done through a DNS record, not through anything on the Wix site. That record
is not being touched, so your years of search history and data stay in the same
Search Console property. Nothing resets.

**Your Google Business Profile is untouched.** It is not part of this at all.
Reviews, photos, map placement — all unaffected.

**Your email keeps working.** Your email runs on Google Workspace through
records that live in the same DNS panel. The cutover plan changes exactly two
things and leaves email alone. This is the one genuine danger in the whole
project, and the plan is written specifically to avoid it — see the warning in
CUTOVER.md about never changing nameservers.

**The Wix site is never deleted.** It stays published the whole time. If
anything looks wrong, putting two DNS records back returns you to exactly where
you are today, within about an hour.

**The one rule that protects all of this: nobody changes a page address.** If a
slug changes, that page's links and rankings break. That is the only way to lose
what you have, and it is entirely within our control.

Realistically, expect a small wobble in rankings for a week or two after any host
change — that is normal and it settles. The site will also be substantially
faster, which helps.

---

## What you need to do to move the site

Four steps. Two are mine, two are yours. **Do them in this order.**

### Step 1 — You: look at the test site and approve it

The site is built and running at a temporary address. Click through it on your
phone, since that is where most of your traffic is. Check the prices, the phone
numbers, the hours, and that the Yukon store appears nowhere.

**Nothing else happens until you say yes.** This is the last easy moment to
change anything.

### Step 2 — Me: flip two settings

In the deploy workflow I change `BASE` and `WRITE_CNAME`, commit, and wait for
the build to go green. Takes minutes.

**Expect this:** the moment it deploys, the temporary test address stops
working. That is normal and it is why you approve first. Visitors see nothing —
discountokc.com still shows the Wix site until step 4.

### Step 3 — You: point GitHub at your domain

In the repository: **Settings → Pages → Custom domain** → type
`www.discountokc.com` → Save.

### Step 4 — You: change two DNS records at Wix

In the Wix domain DNS panel. Wix may ask you to disconnect the domain from the
Wix *site* first — that is fine, your Wix account, Media Manager and 4,000
contacts are unaffected.

Replace the three apex A records with these four:

```
@   A   185.199.108.153
@   A   185.199.109.153
@   A   185.199.110.153
@   A   185.199.111.153
```

Repoint www:

```
www  CNAME  yamakessense.github.io
```

**Do not touch anything else in that panel.** Specifically: leave every MX
record and every TXT record exactly as they are. Those are your email and your
Google verification. Changing the nameservers would take them with it and break
email — do not change nameservers.

### Then, within a few hours

- **Settings → Pages → Enforce HTTPS** — tick it once the box is no longer
  greyed out. Can take a few minutes to a few hours.
- **Search Console** — resubmit the sitemap: `https://www.discountokc.com/sitemap.xml`

### If anything goes wrong

Put the old records back: apex A to `185.230.63.107`, `.171`, `.186` and www
CNAME to `cdn1.wixdns.net`. Back to normal within an hour. The Wix site was
never unpublished, so nothing is unrecoverable.

Full detail is in CUTOVER.md.

---

## What I need from you

Small things, none of them blocking the move.

**1. Two photos at full size.** Two of the three you sent came through as
thumbnails and look soft on a phone:

- The south OKC / Santa Fe storefront (came through 188 pixels wide)
- The ceiling fan aisle (188 pixels wide)

The Midwest City storefront was the same problem until you re-sent it at 1206
pixels, and that one now looks correct — so the fix works, I just need the
originals. Download them from the Google Business Profile dashboard **on a
computer**, or email them to yourself first and attach from there. Attaching
straight from a phone photo viewer is what shrinks them.

**2. A photo of the Visions Workhorse paint.** You asked for product images. The
paint product listing currently reuses a general paint shelf photo. A clear
shot of a Workhorse bucket and a gallon can — label readable — would be much
better, and paint is one of only four things on the site eligible for product
listings in search.

**3. Confirm the military discount detail.** I wrote it as 10% off the
already-discounted running-line vinyl plank price. Tell me if that is wrong.

**4. From Jessica, when she has time.** Still outstanding from the video notes:
unlist the Yukon video, retitle the videos whose names do not say what is in
them, and send TikTok / Facebook / Google Business Profile links.

**5. Nothing about the $500 rubber mulch summer special is in the product
listings**, on purpose — it will expire. Tell me when it ends and I will make
sure the site says the right thing.

---

## What is left on my side

Ordered by what will actually move the needle.

**1. Add an email signup that works.** Currently parked. A static site cannot
safely hold a password, so a signup form needs a small piece of middleware —
about thirty lines on Cloudflare's free tier. Only worth doing if you actually
want to grow the mailing list.

**2. Sort out the Google tags on 405rubbermulch.com.** Not this site, and not
something I can fix from here — that site's code is in a different repository I
can't push to, and the answer isn't in the code anyway. Four Google tag IDs are
firing on it, including **two different Google Ads accounts**, and you told me
tags there are reporting into analytics accounts for both businesses. If one of
those Ads accounts is discountokc's, then every 405rubbermulch visitor is being
counted in discountokc's ad data and both accounts are optimising on the wrong
traffic. Worth checking before more ad money goes through either one. Open
Google Ads → account switcher and GA4 → Admin → Property and write down which
business owns each ID. **Don't delete any tag before that** — a deleted
conversion tag loses its history silently. Details are in NOTES.md.

**3. The one small fix on 405rubbermulch.com.** Its thank-you page — the
conversion page — is the only page on that site with no canonical tag. It should
have one. Same repository problem: I can tell you, I can't do it from here.

---

## Things that must not change, ever

Short list. Everything else is fair game.

- **The fifteen page addresses.** This is what protects your rankings and links.
- **The FAQ wording**, which is mirrored word-for-word into the code that AI
  assistants read. Both come from one source in the build — keep it that way.
- **The name, address, phone and hours block.**
- **The old Yukon phone number, 405-494-0355, must never appear anywhere.** That
  store is permanently closed.
- **Google verification records and any tracking tags** — do not delete.

---

## What changed while you were away

For your own record. Everything is committed and pushed to the branch
`claude/yamakessense-discountokc-review-vp4nqs`.

- **Mobile fixes.** Seven of your ten departments were invisible on a phone —
  the category bar scrolled sideways with nothing showing there was more. Fixed.
  Buttons and phone links were too small to tap reliably. Fixed.
- **Photos load properly.** Phones now download a phone-sized image instead of a
  full-size one. Across five pages that went from 1,407 KB to 410 KB on an
  ordinary phone.
- **Both storefronts are on the home page and the locations page**, described by
  landmark, since that is how people actually find you.
- **Ceiling fans** got the full story: the brands, the honest condition
  disclosure, why working fans get returned, and a six-step troubleshooting
  checklist a customer can run before giving up on one.
- **The buying side of the business is finally on the site** — bought outright,
  consignment where it fits, return-to-vendor and reverse logistics loads,
  trailer clear-outs. That section did not exist before.
- **Pricing is stated the way you actually run it:** discounts up front, no sale
  cycle, plus the military discount and take-all/pallet pricing, and the fact
  that those two do not stack.
- **Search visibility plumbing:** the answer-first structure described above,
  product listings for paint, mulch and flooring, and a robots file that
  explicitly welcomes ChatGPT, Claude, Perplexity and Google's AI crawlers.
- **The answer-first rewrite is finished.** This was the big one and the thing
  you were frustrated about. Your pages used to have no headings matching
  anything a person types — the only two headings on the whole site were
  "Questions, answered" and "Come see it in person," which is why you only came
  up for "Jameson's." Every page now leads with real questions and answers each
  one in its first two sentences: *"How much does it cost to floor a house in
  Oklahoma City?"*, *"Are scratch-and-dent bathtubs worth buying?"*, *"When is
  the best time to buy patio furniture in Oklahoma?"*, *"Is rubber mulch cheaper
  than wood mulch over time?"*, *"Can I haul a 2,000-pound supersack in a pickup
  truck?"* — thirty-seven of them across the site. The home page is now the hub
  and links down into each department, and the department pages link across to
  each other, so somebody who lands on tools finds the flooring they need the
  tools for.
- **The site no longer waits on Google to show text.** The three fonts were
  being fetched from Google on every page load, and nothing could paint until
  that finished. They now live in the site itself. A page with no video on it
  reaches out to nobody.
- **Two things I put on the site that you should read and correct me on if I
  have them wrong:** a five-step method for repairing a chip in an acrylic tub
  (on the bath page), and a table of the standing prices (on the deals page).
  The table says plainly that $601 is the standing supersack price and the $500
  summer special is not one of the standing numbers.
- **You can now throw up a campaign page** with its own Google tag or Meta
  pixel by adding one block to the build file. It stays off the main navigation
  and can be kept out of search.

---

## One thing worth knowing about tracking

You asked whether GA4 covers everything. For *measuring* traffic, yes — it will
tell you where every visitor came from, including AI assistants.

What it cannot do is feed Facebook. The Meta pixel is not a reporting tool; it
sends conversion signal back to Meta so their ad system learns who to show your
ads to. If you are not running Meta ads, you do not need it and should not carry
it. If you start running them, the support is built and it is one line to turn
on.

The site currently loads **no** analytics, no pixel and no tag manager. That is
deliberate — it keeps the site fast and keeps you out of cookie-consent
territory until you actually want tracking.
