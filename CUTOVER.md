# DNS cutover — discountokc.com

Current state, looked up Aug 2026. Do not start until the test URL has been
clicked through and approved.

## What's there now

```
Nameservers   ns6.wixdns.net, ns7.wixdns.net      <- DNS is hosted AT WIX
Apex (@)      A  185.230.63.107 / .171 / .186     <- Wix web servers  [CHANGE]
www           CNAME  cdn1.wixdns.net              <- Wix CDN          [CHANGE]
MX            aspmx.l.google.com + 4 more         <- Google Workspace [DO NOT TOUCH]
TXT           google-site-verification=4B9OT32... <- Search Console   [DO NOT TOUCH]
TXT           google._domainkey  v=DKIM1;...      <- email signing    [DO NOT TOUCH]
TTL           3600 (1 hour)
```

**The email warning.** Mail for this domain runs on Google Workspace, and those
MX/DKIM records live in the same Wix DNS zone as the website records. Changing
the *nameservers* away from Wix would take the MX and TXT records with them and
break email and Search Console verification until they were recreated by hand.

**So: do not change nameservers.** Leave DNS hosted at Wix and edit only two
things inside the Wix DNS panel — the apex A records and the www CNAME.
Everything else in the zone stays exactly as it is.

## Steps, in order

### 1. Flip the workflow — Claude does this

In `.github/workflows/deploy.yml`:

```yaml
BASE: ""
WRITE_CNAME: "1"
```

Commit, push, wait for green.

**Expect this:** the moment it deploys, `yamakessense.github.io/discountokc/`
stops working — GitHub redirects it to www.discountokc.com, which is still Wix.
That is why the test URL gets approved *before* this step, not after. Visitors
see no downtime; discountokc.com keeps serving the Wix site until step 3.

### 2. Set the custom domain — you, in GitHub

Repo → **Settings → Pages → Custom domain** → `www.discountokc.com` → Save.

### 3. Change two records — you, in Wix

Wix domain DNS panel. Wix may make you disconnect the domain from the Wix *site*
first; the Wix account, the Media Manager and the contacts are unaffected.

Replace the three apex A records with GitHub's four:

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

Leave MX and every TXT record alone.

### 4. HTTPS — you, in GitHub

Wait for propagation (TTL is 1 hour). Then Settings → Pages → tick
**Enforce HTTPS** once the certificate has provisioned. It can take a few
minutes to a few hours; the box is greyed out until it's ready.

### 5. Search Console

Resubmit the sitemap: `https://www.discountokc.com/sitemap.xml`

## Rollback

Put the Wix records back — apex A to 185.230.63.107/.171/.186 and www CNAME to
cdn1.wixdns.net. Back to normal within the 1-hour TTL. The Wix site stays
published throughout, so nothing is ever deleted and nothing is unrecoverable.

## Why the slugs matter here

All 15 URLs match the live Wix sitemap exactly, so this is a host change, not a
migration. No redirects are needed and existing rankings carry over. That only
holds as long as nobody changes a slug.
