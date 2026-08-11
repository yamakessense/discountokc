#!/usr/bin/env python3
"""discountokc.com static site generator.

Run:  python3 build.py
Out:  _site/   (the whole website: 15 pages, same slugs as the Wix site)

Edit the words in the PAGE CONTENT section, run this, commit. GitHub Actions
also runs it automatically on every push and publishes the result.
"""
import json, os, re, shutil, html


# ===================== DESIGN & LAYOUT =====================
BIZ = "Jameson's Discount Home Improvement Warehouse"
SHORT = "Jameson's"
SITE = "https://www.discountokc.com"

CSS = r"""
:root{
  --royal:#3D4E9E; --deep:#2C3A78; --ink:#161B33; --red:#C94A3F;
  --cream:#F7F3EC; --white:#fff; --line:#E4DED1; --muted:#5C6070;
  --green:#2E7D4F;
  --pad:clamp(1.1rem,4vw,2rem);
  --maxw:1140px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:'Public Sans',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  background:var(--cream);color:var(--ink);line-height:1.6;font-size:17px;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:var(--royal);text-decoration:none}
a:hover{text-decoration:underline}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.wrap{width:min(var(--maxw),100% - 2rem);margin-inline:auto}
h1,h2,h3,h4,.display{font-family:'Archivo',system-ui,sans-serif;font-weight:800;line-height:1.08;letter-spacing:-.02em}
h1{font-size:clamp(2rem,5.6vw,3.35rem);text-transform:uppercase;letter-spacing:-.015em}
h2{font-size:clamp(1.5rem,3.6vw,2.25rem);margin-bottom:.6rem}
h3{font-size:1.18rem;margin-bottom:.35rem}
p{margin-bottom:1rem;max-width:70ch}
.eyebrow{font-family:'Spline Sans Mono',ui-monospace,monospace;font-size:.75rem;letter-spacing:.18em;
  text-transform:uppercase;color:var(--red);font-weight:600;display:block;margin-bottom:.7rem}
.mono{font-family:'Spline Sans Mono',ui-monospace,monospace}

/* ---------- top info bar ---------- */
.topbar{background:var(--deep);color:#fff;font-size:.86rem}
.topbar .wrap{display:flex;gap:.4rem 1.6rem;flex-wrap:wrap;justify-content:center;
  align-items:center;padding:.5rem 0;text-align:center}
.topbar a{color:#fff;font-weight:700;text-decoration:none}
.topbar a:hover{text-decoration:underline}
.topbar .sep{opacity:.45}
@media(max-width:640px){.topbar .sep{display:none}.topbar .wrap{gap:.15rem .9rem}}

/* ---------- header ---------- */
.masthead{background:var(--royal);color:#fff}
.masthead .wrap{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.85rem 0}
.brand{display:flex;align-items:center;gap:.65rem;color:#fff;text-decoration:none}
.brand:hover{text-decoration:none}
.mark{width:44px;height:44px;flex:0 0 44px;background:var(--red);color:#fff;display:grid;place-items:center;
  font-family:'Archivo';font-weight:800;font-size:1.35rem;border-radius:4px;box-shadow:0 0 0 3px rgba(255,255,255,.22)}
.brand .nm{font-family:'Archivo';font-weight:800;font-size:1.12rem;line-height:1.05;text-transform:uppercase;letter-spacing:-.01em}
.brand .nm span{display:block;font-family:'Spline Sans Mono',monospace;font-size:.6rem;font-weight:400;
  letter-spacing:.2em;opacity:.85;margin-top:.22rem;text-transform:uppercase}
.callbtn{background:#fff;color:var(--deep);font-weight:800;padding:.6rem 1rem;border-radius:3px;
  display:inline-flex;align-items:center;gap:.45rem;white-space:nowrap;font-size:.95rem}
.callbtn:hover{background:var(--cream);text-decoration:none}
@media(max-width:520px){.callbtn .lbl{display:none}}

/* ---------- category nav ---------- */
.catnav{background:var(--deep);position:sticky;top:0;z-index:60}
.catnav ul{display:flex;list-style:none;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.catnav ul::-webkit-scrollbar{display:none}
.catnav a{color:#fff;font-weight:600;font-size:.94rem;padding:.75rem 1.05rem;display:block;white-space:nowrap;
  border-bottom:3px solid transparent}
.catnav a:hover{background:rgba(255,255,255,.12);text-decoration:none}
.catnav a.on{border-bottom-color:var(--red);background:rgba(255,255,255,.09)}
.catnav a.hot{background:var(--red)}

/* ---------- ticket strip (signature) ---------- */
.ticket{background:var(--red);color:#fff}
.ticket .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:.5rem 1rem;
  padding:.7rem 0;text-align:center;font-weight:600;font-size:.97rem}
.ticket b{font-family:'Archivo';font-weight:800;text-transform:uppercase;letter-spacing:.03em}
.ticket .tag{font-family:'Spline Sans Mono',monospace;font-weight:600;background:#fff;color:var(--red);
  padding:.12rem .6rem;border-radius:2px;position:relative}
.ticket a{color:#fff;text-decoration:underline;text-underline-offset:3px;font-weight:700}

/* ---------- sections ---------- */
main section{padding:clamp(2.2rem,5vw,3.6rem) 0}
main section.tight{padding-top:0}
.sechead{max-width:60ch;margin-bottom:1.6rem}
.sechead p{color:var(--muted)}
.rule{height:6px;background:repeating-linear-gradient(135deg,var(--royal) 0 10px,transparent 10px 20px);opacity:.5}

/* ---------- hero ---------- */
.hero{background:var(--royal);color:#fff;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;inset:0;
  background:repeating-linear-gradient(135deg,rgba(255,255,255,.05) 0 18px,transparent 18px 36px);pointer-events:none}
.hero .wrap{position:relative;z-index:1;padding:clamp(2.4rem,6vw,4.2rem) 0}
.hero .eyebrow{color:#fff;opacity:.85}
.hero h1{max-width:16ch}
.hero h1 em{font-style:normal;color:#FFD9D3;display:block}
.hero .lead{font-size:clamp(1.02rem,2.3vw,1.22rem);max-width:52ch;margin-top:1rem;color:#EAECF7}
.hero .fine{font-size:.88rem;color:#C6CCE8;max-width:56ch;margin-top:1.3rem;margin-bottom:0}
.btnrow{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:1.5rem}
.btn{display:inline-flex;align-items:center;gap:.5rem;font-weight:800;font-size:1rem;padding:.85rem 1.3rem;
  border-radius:3px;border:2px solid transparent;cursor:pointer;font-family:'Public Sans',sans-serif}
.btn:hover{text-decoration:none}
.btn-red{background:var(--red);color:#fff}
.btn-red:hover{background:#b23f35}
.btn-white{background:#fff;color:var(--deep)}
.btn-white:hover{background:var(--cream)}
.btn-out{border-color:currentColor;color:inherit;background:transparent}
.btn-out:hover{background:rgba(255,255,255,.14)}
.btn-ink{background:var(--deep);color:#fff}
.btn-ink:hover{background:var(--royal)}

/* ---------- page head (interior) ---------- */
.pagehead{background:var(--white);border-bottom:1px solid var(--line)}
.pagehead .wrap{padding:clamp(1.6rem,4vw,2.6rem) 0}
.crumbs{font-family:'Spline Sans Mono',monospace;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);margin-bottom:.8rem}
.crumbs a{color:var(--muted)}
.pagehead .lead{font-size:1.08rem;color:var(--muted);max-width:62ch;margin-top:.9rem;margin-bottom:0}

/* ---------- category grid ---------- */
.grid{display:grid;gap:.9rem;grid-template-columns:repeat(auto-fill,minmax(158px,1fr))}
.tile{background:#fff;border:1px solid var(--line);border-radius:4px;padding:1.1rem;display:block;color:var(--ink);
  transition:transform .16s ease,box-shadow .16s ease,border-color .16s}
.tile:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(22,27,51,.10);border-color:var(--royal);text-decoration:none}
.tile svg{color:var(--royal);margin-bottom:.6rem}
.tile h3{font-size:1.02rem;margin-bottom:.15rem}
.tile span{font-size:.85rem;color:var(--muted)}

/* ---------- cards / split ---------- */
.split{display:grid;gap:1.2rem;grid-template-columns:repeat(auto-fit,minmax(290px,1fr))}
.card{background:#fff;border:1px solid var(--line);border-radius:4px;padding:1.5rem}
.card.dark{background:var(--deep);color:#fff;border-color:transparent}
.card.dark p{color:#D5DAEE}
.card.dark .eyebrow{color:#FFC9C2}
.card ul{list-style:none;display:flex;flex-direction:column;gap:.6rem;margin-top:.9rem}
.card li{position:relative;padding-left:1.5rem;font-size:.96rem}
.card li::before{content:"";position:absolute;left:0;top:.55em;width:9px;height:9px;background:var(--red)}
.card.dark li::before{background:#FFC9C2}

/* ---------- price chips ---------- */
.prices{display:flex;flex-wrap:wrap;gap:.6rem;margin:1.1rem 0}
.chip{font-family:'Spline Sans Mono',monospace;background:#fff;border:1px solid var(--line);
  border-left:4px solid var(--red);padding:.55rem .8rem;font-size:.9rem;border-radius:2px}
.chip b{display:block;font-size:1.15rem;color:var(--deep);font-weight:600}
.card.dark .chip{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.18);border-left-color:#FFC9C2;color:#fff}
.card.dark .chip b{color:#fff}

/* ---------- FAQ ---------- */
.faq{max-width:70ch}
.faq details{background:#fff;border:1px solid var(--line);border-radius:3px;margin-bottom:.6rem}
.faq summary{cursor:pointer;list-style:none;padding:.95rem 1.1rem;font-weight:700;font-family:'Archivo';
  display:flex;justify-content:space-between;gap:1rem;align-items:flex-start}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-family:'Spline Sans Mono',monospace;color:var(--red);font-size:1.3rem;line-height:1}
.faq details[open] summary::after{content:"–"}
.faq .ans{padding:0 1.1rem 1.05rem;color:var(--muted)}
.faq .ans p:last-child{margin-bottom:0}

/* ---------- video slot ---------- */
.vslot{border:2px dashed var(--line);background:#fff;border-radius:4px;padding:1.4rem;color:var(--muted);
  display:flex;gap:1rem;align-items:center}
.vslot svg{flex:0 0 auto;color:var(--red)}
.vslot p{margin:0;font-size:.94rem}

/* ---------- locations ---------- */
.locs{background:var(--deep);color:#fff}
.locs h2{color:#fff}
.locgrid{display:grid;gap:1.1rem;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));margin-top:1.3rem}
.loc{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);border-radius:4px;padding:1.4rem}
.loc h3{font-size:1.25rem}
.loc .addr{color:#D5DAEE;margin-bottom:.5rem}
.loc .tel{font-family:'Spline Sans Mono',monospace;font-size:1.22rem;color:#fff;font-weight:600;display:inline-block;margin:.3rem 0 .7rem}
.loc a.dir{display:inline-block;color:#fff;font-weight:700;border-bottom:2px solid var(--red);padding-bottom:2px}
.hours{margin-top:1.2rem;font-family:'Spline Sans Mono',monospace;font-size:.9rem;color:#D5DAEE}

/* ---------- CTA strip ---------- */
.ctastrip{background:var(--red);color:#fff;text-align:center}
.ctastrip h2{color:#fff}
.ctastrip p{margin-inline:auto;color:#FFE7E3}
.ctastrip .btnrow{justify-content:center}

/* ---------- footer ---------- */
footer{background:var(--ink);color:#B9BDD0;font-size:.92rem;padding:2.4rem 0 2.6rem}
footer h4{color:#fff;font-family:'Archivo';font-weight:800;font-size:.95rem;margin-bottom:.7rem;text-transform:uppercase;letter-spacing:.04em}
footer a{color:#B9BDD0;display:block;margin-bottom:.3rem}
footer a:hover{color:#fff}
.footgrid{display:grid;gap:1.6rem;grid-template-columns:2fr 1fr 1fr 1fr}
@media(max-width:760px){.footgrid{grid-template-columns:1fr 1fr}}
@media(max-width:480px){.footgrid{grid-template-columns:1fr}}
.footbot{margin-top:2rem;padding-top:1.1rem;border-top:1px solid rgba(255,255,255,.12);
  display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem;font-size:.82rem}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}html{scroll-behavior:auto}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&'
         'family=Public+Sans:wght@400;600;700&family=Spline+Sans+Mono:wght@400;600&display=swap" rel="stylesheet">')

# Lucide-style stroke icons (no emoji)
def icon(name, size=26):
    P = {
      "layers": '<path d="M12 2 2 7l10 5 10-5-10-5Z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
      "vanity": '<rect x="3" y="4" width="18" height="9" rx="1"/><path d="M7 13v7M17 13v7M3 17h18"/>',
      "droplet": '<path d="M12 2.7 6.9 8.2a7.2 7.2 0 1 0 10.2 0Z"/>',
      "kitchen": '<path d="M4 3v18M4 8h6M14 3v7a3 3 0 0 0 3 3v8"/><path d="M20 3v7a3 3 0 0 1-3 3"/>',
      "bulb": '<path d="M9 18h6M10 22h4"/><path d="M12 2a6 6 0 0 0-3.5 10.9c.6.5.9 1.2 1 1.9l.1 1.2h4.8l.1-1.2c.1-.7.4-1.4 1-1.9A6 6 0 0 0 12 2Z"/>',
      "tool": '<path d="M14.7 6.3a4 4 0 0 0 5 5l-9.6 9.6a2.1 2.1 0 0 1-3-3Z"/><path d="m14.7 6.3 3-3 3 3-3 3"/>',
      "umbrella": '<path d="M12 2a10 10 0 0 1 10 10H2A10 10 0 0 1 12 2Z"/><path d="M12 12v7a3 3 0 0 0 6 0"/>',
      "truck": '<path d="M2 6h11v11H2z"/><path d="M13 10h4l4 4v3h-8"/><circle cx="7" cy="19" r="2"/><circle cx="17" cy="19" r="2"/>',
      "tag": '<path d="M3 3h8l10 10-8 8L3 11Z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
      "boxes": '<rect x="3" y="3" width="8" height="8"/><rect x="13" y="3" width="8" height="8"/><rect x="3" y="13" width="8" height="8"/><rect x="13" y="13" width="8" height="8"/>',
      "phone": '<path d="M6 3h4l2 5-2.5 1.5a12 12 0 0 0 5 5L16 12l5 2v4a2 2 0 0 1-2.2 2A17 17 0 0 1 4 5.2 2 2 0 0 1 6 3Z"/>',
      "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/>',
      "play": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m10 9 5 3-5 3Z"/>',
      "roller": '<rect x="3" y="4" width="13" height="5" rx="1"/><path d="M16 6.5h4V12h-8v3"/><rect x="10" y="15" width="4" height="6" rx="1"/>',
      "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    }
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>')

NAV = [
    ("vanities", "Vanities"), ("flooring", "Flooring"), ("bath", "Bath"), ("kitchen", "Kitchen"),
    ("patio", "Patio"), ("lighting", "Lights &amp; Fans"), ("tools", "Tools"),
    ("rubbermulchokc", "Rubber Mulch"), ("bulk-rubber-mulch", "Bulk Mulch"),
    ("inventory", "Inventory"), ("about", "About"), ("location", "Locations"),
    ("contact", "Contact"), ("deals", "Deals"),
]

def topbar(L):
    return f'''<div class="topbar"><div class="wrap">
<a href="{L('location')}">Two stores in the OKC metro</a><span class="sep">·</span>
<span>Tue&ndash;Sat 9&ndash;6 &middot; Sun 10&ndash;6 &middot; Closed Monday</span><span class="sep">·</span>
<a href="tel:+14052068111">Midwest City (405) 206-8111</a><span class="sep">·</span>
<a href="tel:+14054797918">South OKC (405) 479-7918</a>
</div></div>'''

def masthead(L):
    return f'''<header class="masthead"><div class="wrap">
<a class="brand" href="{L('')}"><span class="mark">J</span>
<span class="nm">Jameson's<span>Discount Home Improvement</span></span></a>
<a class="callbtn" href="tel:+14052068111">{icon('phone',18)}<span class="lbl">Call</span> 405-206-8111</a>
</div></header>'''

def catnav(L, current):
    items = "".join(
        f'<li><a href="{L(s)}" class="{"hot " if s=="deals" else ""}{"on" if s==current else ""}">{t}</a></li>'
        for s, t in NAV)
    return f'<nav class="catnav" aria-label="Product categories"><div class="wrap"><ul>{items}</ul></div></nav>'

def ticket():
    return ('<div class="ticket"><div class="wrap"><b>Summer special</b>'
            '<span>IPEMA-certified chunk rubber nuggets</span>'
            '<span class="tag">$500 / supersack</span>'
            '<span>pickup only &middot; in stock now</span>'
            '<a href="tel:+14052068111">Call 405-206-8111</a></div></div>')

def locations_block(heading="Two stores across the OKC metro"):
    return f'''<section class="locs"><div class="wrap">
<span class="eyebrow" style="color:#FFC9C2">Come see us</span>
<h2>{heading}</h2>
<div class="locgrid">
  <div class="loc">
    <h3>Midwest City</h3>
    <p class="addr">7010 SE 15th Street<br>Midwest City, OK 73110</p>
    <a class="tel" href="tel:+14052068111">405-206-8111</a><br>
    <a class="dir" href="https://www.google.com/maps/search/?api=1&amp;query=7010+SE+15th+Street+Midwest+City+OK+73110">Get directions</a>
  </div>
  <div class="loc">
    <h3>South OKC <span class="mono" style="font-size:.72rem;opacity:.8">NEAR I-240</span></h3>
    <p class="addr">8100 S. Santa Fe Ave<br>Oklahoma City, OK 73139</p>
    <a class="tel" href="tel:+14054797918">405-479-7918</a><br>
    <a class="dir" href="https://www.google.com/maps/search/?api=1&amp;query=8100+S+Santa+Fe+Ave+Oklahoma+City+OK+73139">Get directions</a>
  </div>
</div>
<p class="hours">HOURS &nbsp;Tue&ndash;Sat 9:00&ndash;6:00 &middot; Sun 10:00&ndash;6:00 &middot; Closed Monday</p>
</div></section>'''

def footer(L):
    cats = "".join(f'<a href="{L(s)}">{t}</a>' for s, t in NAV[:7])
    return f'''<footer><div class="wrap">
<div class="footgrid">
  <div>
    <h4>{BIZ}</h4>
    <p style="max-width:40ch">Closeout home improvement warehouse serving the Oklahoma City metro &mdash;
    name-brand flooring, vanities, bath, kitchen, lighting, tools and patio at up to 50% off retail,
    plus playground-certified rubber mulch.</p>
    <a href="mailto:save@discountokc.com">save@discountokc.com</a>
  </div>
  <div><h4>Shop</h4>{cats}</div>
  <div><h4>Stores</h4>
    <a href="tel:+14052068111">Midwest City &middot; 405-206-8111</a>
    <a href="tel:+14054797918">South OKC &middot; 405-479-7918</a>
    <a href="{L('location')}">Hours &amp; directions</a>
    <a href="{L('contact')}">Contact</a>
  </div>
  <div><h4>More</h4>
    <a href="{L('about')}">About Jameson's</a>
    <a href="{L('deals')}">This week's deals</a>
    <a href="https://405rubbermulch.com">405RubberMulch.com &mdash; wholesale</a>
  </div>
</div>
<div class="footbot"><span>&copy; {BIZ} &middot; Midwest City &amp; South OKC</span>
<span class="mono">Tue&ndash;Sat 9&ndash;6 &middot; Sun 10&ndash;6 &middot; Closed Mon</span></div>
</div></footer>'''

# ===================== PAGE CONTENT =====================


VSLOT = ('<div class="vslot">' + icon('play', 30) +
         '<p><b>Video slot &mdash; reserved.</b> Three to five of your YouTube videos drop in here, each with a '
         'short written summary and VideoObject schema, once the channels are tagged and sorted.</p></div>')

CATS = [
    ("flooring", "layers", "Flooring", "Waterproof LVP &amp; tile"),
    ("vanities", "vanity", "Vanities", "Single &amp; double, all styles"),
    ("bath", "droplet", "Bath", "Toilets, tubs, faucets"),
    ("kitchen", "kitchen", "Kitchen", "Sinks, faucets, fixtures"),
    ("lighting", "bulb", "Lights &amp; Fans", "Fixtures &amp; ceiling fans"),
    ("tools", "tool", "Tools", "Name-brand power &amp; hand"),
    ("patio", "umbrella", "Patio", "Outdoor furniture &amp; decor"),
    ("rubbermulchokc", "truck", "Rubber Mulch", "Playground certified"),
]


def cat_grid(L):
    tiles = "".join(
        f'<a class="tile" href="{L(s)}">{icon(ic)}<h3>{t}</h3><span>{d}</span></a>'
        for s, ic, t, d in CATS)
    return f'<div class="grid">{tiles}</div>'


def faq_html(items):
    out = ['<div class="faq">']
    for q, a in items:
        out.append(f'<details><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>')
    out.append('</div>')
    return "".join(out)


def build_pages(L):
    """Return list of page dicts. L(slug) -> link href."""
    P = []

    # ---------------------------------------------------------------- HOME
    P.append(dict(
        slug="", nav="", kind="home",
        title=f"{BIZ} | Name-Brand Closeout Prices &mdash; OKC &amp; Midwest City",
        desc=("Closeout home improvement warehouse in the OKC metro. Name-brand flooring, vanities, bath, "
              "kitchen, lighting, tools, patio and playground-certified rubber mulch at up to 50% off retail. "
              "Two stores: Midwest City and South OKC."),
        h1="Name-brand home improvement at closeout prices",
        body=f'''
<section class="hero"><div class="wrap">
  <span class="eyebrow">Midwest City &amp; South OKC &middot; Two stores</span>
  <h1>Name-brand home improvement at closeout prices <em>Because retail prices suck.</em></h1>
  <p class="lead">Flooring, vanities, kitchen, bath, lighting, tools, patio and more &mdash; up to half off retail.
  New truckloads land every week.</p>
  <div class="btnrow">
    <a class="btn btn-red" href="{L('inventory')}">See what's in stock</a>
    <a class="btn btn-out" href="{L('location')}">Hours &amp; directions</a>
  </div>
  <p class="fine">Inventory moves faster than the website &mdash; items pictured are examples, and we'll always
  have something similar on the floor.</p>
</div></section>
{ticket()}
<section><div class="wrap">
  <div class="sechead"><span class="eyebrow">Under one roof</span>
    <h2>Everything for the remodel, half off retail</h2>
    <p>Toilets, tubs, vanities, faucets, ceiling fans, light fixtures, patio furniture, flooring, tools and more &mdash;
    bought as closeout, overstock and end-of-line lots, sold in the box.</p></div>
  {cat_grid(L)}
</div></section>
<section class="tight"><div class="wrap"><div class="split">
  <div class="card dark">
    <span class="eyebrow">Retail &amp; wholesale &middot; one company</span>
    <h2 style="color:#fff">405RubberMulch.com &mdash; our regional wholesale arm serving Oklahoma, Kansas, Missouri &amp; Arkansas</h2>
    <p>Jameson's is the retail home of 405RubberMulch.com. Schools, cities and contractors across four states get
    flatbed truckload delivery of IPEMA-certified playground rubber mulch through 405RubberMulch. Need bags or a
    supersack today? Pick it up at either Jameson's store.</p>
    <div class="prices">
      <div class="chip"><b>$8</b>24-lb bag</div>
      <div class="chip"><b>$601</b>2,000-lb supersack</div>
      <div class="chip"><b>$500</b>summer special, pickup</div>
    </div>
    <div class="btnrow">
      <a class="btn btn-white" href="https://405rubbermulch.com">Regional truckload delivery &mdash; 405RubberMulch.com</a>
      <a class="btn btn-out" href="{L('rubbermulchokc')}">Buy mulch in store</a>
    </div>
  </div>
  <div class="card">
    <span class="eyebrow">On the shelf now</span>
    <h2>Visions Quality Coatings paint &mdash; $21.99 a gallon</h2>
    <p>High-performance Workhorse interior and exterior latex, in 1-gallon and 5-gallon buckets.</p>
    <ul>
      <li><b>Premium performance, warehouse prices.</b> Workhorse blends deliver national-brand durability, hide and
      coverage at a closeout discount &mdash; smooth for DIY, consistent for pros.</li>
      <li><b>Leaders in the circular economy.</b> Visions is a major innovator in remanufactured paint, rescuing
      premium post-consumer material.</li>
      <li><b>A truly sustainable choice.</b> Keeps thousands of gallons out of local waste streams.</li>
    </ul>
  </div>
</div></div></section>
<section class="tight"><div class="wrap">
  <div class="sechead"><span class="eyebrow">Why Jameson's</span>
  <h2>A closeout warehouse, not a salvage yard</h2></div>
  <div class="split">
    <div class="card"><h3>Running-line, in the box</h3>
      <p>Our flooring, paint and fixtures are name-brand, running-line product &mdash; not seconds, not returns.
      We buy closeouts, overstock and end-of-line lots, so you get what the big stores sell for up to half the price.</p></div>
    <div class="card"><h3>Truckloads, weekly</h3>
      <p>New lots land every week and sell fast. What's here today may be gone next Saturday &mdash; which is exactly
      why the prices are what they are.</p></div>
    <div class="card"><h3>Two stores, one phone call</h3>
      <p>Midwest City and South OKC near I-240. Call either store and staff will tell you what's actually on the floor
      right now before you drive out.</p></div>
  </div>
</div></section>
<section class="tight"><div class="wrap">
  <div class="sechead"><span class="eyebrow">Good to know</span><h2>Frequently asked questions</h2></div>
  {faq_html([
    ("What is Jameson's Discount Home Improvement Warehouse?",
     "A closeout home improvement retail warehouse with two Oklahoma City metro stores &mdash; 7010 SE 15th Street in "
     "Midwest City and 8100 S. Santa Fe Ave in south OKC near I-240. We sell name-brand flooring, vanities, bath, "
     "kitchen, lighting, tools and patio at up to 50% off retail."),
    ("Is your rubber mulch playground certified?",
     "Yes &mdash; IPEMA-certified chunk rubber nuggets, in stock for pickup at Jameson's."),
    ("Do you deliver truckloads of rubber mulch?",
     "Yes &mdash; our wholesale arm, 405RubberMulch.com, delivers flatbed truckloads to schools, cities and "
     "contractors across Oklahoma, Kansas, Missouri and Arkansas."),
    ("What does rubber mulch cost?",
     "$8 per 24-lb bag and $601 per 2,000-lb supersack. All summer: IPEMA-certified chunk rubber nuggets at "
     "$500 per supersack, pickup only. Volume discounts available."),
    ("Do you carry paint?",
     "Yes &mdash; Visions Quality Coatings Workhorse interior and exterior latex at $21.99 a gallon, in 1-gallon "
     "and 5-gallon buckets."),
    ("What are your hours?",
     "Both stores: Tuesday through Saturday 9:00 AM to 6:00 PM, Sunday 10:00 AM to 6:00 PM, closed Monday."),
    ("Can I order online or have it shipped?",
     "Sales are in-store. Inventory is closeout-driven and changes daily, so call ahead and staff will check the "
     "floor for you: 405-206-8111 in Midwest City, 405-479-7918 in South OKC."),
  ])}
</div></section>
{locations_block()}
<section class="ctastrip"><div class="wrap">
  <h2>New deals hit the floor every week</h2>
  <p style="max-width:52ch">Come by and see what landed &mdash; or call first and we'll tell you what's on the floor.</p>
  <div class="btnrow">
    <a class="btn btn-white" href="tel:+14052068111">Call Midwest City</a>
    <a class="btn btn-white" href="tel:+14054797918">Call South OKC</a>
  </div>
</div></section>
''',
        faq=[
            ("Is your rubber mulch playground certified?",
             "Yes — IPEMA-certified chunk rubber nuggets, in stock for pickup at Jameson's."),
            ("Do you deliver truckloads of rubber mulch?",
             "Yes — our wholesale arm, 405RubberMulch.com, delivers flatbed truckloads to schools, cities and "
             "contractors across Oklahoma, Kansas, Missouri and Arkansas."),
            ("What does rubber mulch cost?",
             "$8 per 24-lb bag and $601 per 2,000-lb supersack. All summer: IPEMA-certified chunk rubber nuggets at "
             "$500 per supersack, pickup only. Volume discounts available."),
            ("Do you carry paint?",
             "Yes — Visions Quality Coatings Workhorse interior and exterior latex at $21.99 a gallon, in 1-gallon "
             "and 5-gallon buckets."),
            ("What are your hours?",
             "Both stores: Tuesday through Saturday 9:00 AM to 6:00 PM, Sunday 10:00 AM to 6:00 PM, closed Monday."),
        ]))

    # ------------------------------------------------------- category pages
    cat = []

    cat.append(dict(
        slug="vanities", nav="vanities",
        title="Discount Bathroom Vanities OKC | Vanity Art &amp; Wyndham Up to 50% Off | Jameson's",
        desc=("Name-brand bathroom vanities at closeout prices in Midwest City and South OKC &mdash; single and double "
              "vanities including Vanity Art and Wyndham Collection. Stock changes weekly; call or visit."),
        h1="Discount bathroom vanities in OKC &mdash; up to 50% off Vanity Art, Wyndham &amp; more",
        lead="Single and double vanities, tops and mirrors from closeout and overstock lots &mdash; in the box, not seconds.",
        paras=[
            "Jameson's Discount Home Improvement Warehouse carries name-brand bathroom vanities at closeout prices, "
            "including Vanity Art and Wyndham Collection pieces. Sizes run from compact single vanities for a half "
            "bath up to 72-inch doubles, in finishes that rotate as new lots arrive. Many arrive as complete units "
            "with tops and hardware.",
            "A vanity swap is the single highest-impact change you can make in a bathroom, and it sits right on the "
            "line between DIY and pro work. If your new vanity matches the footprint of the old one and the supply "
            "lines and drain line up, most handy homeowners can do the swap in an afternoon. Moving plumbing, cutting "
            "into a stone top, or going from a 30-inch to a 60-inch cabinet is where a licensed plumber earns the fee.",
            "Because vanities come in as closeout lots, what's on the floor is what's available &mdash; there's no "
            "back room and no reorder. If you see the one you want at the price you want, that's the day to buy it. "
            "Call either store and staff will walk the floor and tell you what's actually there before you drive out.",
        ],
        faq=[
            ("Where can I buy a discount bathroom vanity in the Oklahoma City metro?",
             "Jameson's Discount Home Improvement Warehouse — 7010 SE 15th Street in Midwest City and 8100 S. Santa Fe "
             "Ave in south OKC near I-240. Name-brand vanities at up to 50% off retail."),
            ("What brands of vanities do you carry?",
             "Brands rotate with the lots, but Vanity Art and Wyndham Collection pieces come through regularly. "
             "Call ahead and staff will tell you what's on the floor today."),
            ("Can I install a bathroom vanity myself?",
             "If the new vanity matches the old footprint and the plumbing lines up, it's a common DIY job. Moving "
             "supply or drain lines, or changing cabinet size, is worth a licensed plumber."),
            ("Do vanities come with tops?",
             "Many closeout vanities arrive as complete units with tops; some are cabinet-only. It depends on the lot, "
             "so call 405-206-8111 or 405-479-7918 to confirm before you make the drive."),
        ]))

    cat.append(dict(
        slug="flooring", nav="flooring",
        title="Discount Flooring OKC | Waterproof LVP $2.19&ndash;$2.69/sf | Jameson's",
        desc=("Waterproof rigid-core LVP with manufacturer warranty, averaging $2.19&ndash;$2.69/sf, plus porcelain "
              "tile. Closeout lots arrive weekly in Midwest City &amp; South OKC &mdash; call or visit."),
        h1="Discount flooring in OKC &mdash; waterproof LVP &amp; tile up to 50% off",
        lead="Rigid-core waterproof plank and porcelain tile, bought by the truckload and priced to move.",
        chips=[("$2.19&ndash;$2.69", "per sq ft, waterproof LVP"), ("12&ndash;20 mil", "wear layer, warrantied")],
        paras=[
            "Jameson's Discount Home Improvement carries waterproof luxury vinyl plank (LVP) and porcelain tile at "
            "closeout prices &mdash; the same rigid-core, name-brand product big-box stores sell, at a fraction of the "
            "price. We regularly stock 12-mil and 20-mil wear-layer waterproof LVP backed by manufacturer warranty, "
            "with prices that fluctuate by lot but currently average $2.19 to $2.69 per square foot. Select styles of "
            "porcelain tile round out the selection.",
            "Flooring is one of the highest-impact upgrades you can make on a budget. Click-lock LVP is a genuinely "
            "DIY-friendly install &mdash; it floats over most existing floors with no glue or nails, and a weekend and "
            "a tapping block will carry most rooms. Large-format tile, wet areas, and subfloor repair are where a "
            "professional installer earns their fee. Either way, the flooring itself is where the savings live: "
            "material bought at closeout costs the same to install as material bought at full retail.",
            "Because our inventory comes from truckload closeouts, surplus lots arrive continuously and sell fast. If "
            "you're calculating square footage for a project, call ahead or stop by &mdash; staff can tell you what's "
            "on the floor and how much of it is left.",
        ],
        faq=[
            ("Is there LVP flooring under $2.50 a square foot in Oklahoma City?",
             "Yes — our waterproof rigid-core LVP averages $2.19–$2.69/sf depending on the current lot, with a "
             "manufacturer warranty. Stock changes weekly."),
            ("Can I install LVP myself?",
             "Click-lock floating LVP is one of the most DIY-friendly floors made. If your subfloor is flat and dry, "
             "most rooms are a weekend project. Tile and subfloor repair are better left to a pro."),
            ("How much should I buy?",
             "Measure your square footage and add roughly 10% for cuts and waste. Staff at either store can help you "
             "check the math against what's in stock."),
            ("What if the style I want sells out mid-project?",
             "Closeout lots are finite — buy the full quantity for your project up front. Call Midwest City at "
             "405-206-8111 or South OKC at 405-479-7918 to confirm current pallet quantities."),
        ]))

    cat.append(dict(
        slug="bath", nav="bath",
        title="Discount Bath OKC | Toilets, Tubs &amp; Faucets Up to 50% Off | Jameson's",
        desc=("Name-brand toilets, tubs and faucets at closeout prices in Midwest City &amp; South OKC. Inventory "
              "changes weekly &mdash; call or visit to see what's in stock."),
        h1="Discount bath &mdash; toilets, tubs &amp; faucets in OKC up to 50% off",
        lead="Name-brand bath fixtures from closeout and overstock lots &mdash; not seconds, not returns.",
        paras=[
            "Jameson's carries name-brand toilets, bathtubs, faucets, and bath fixtures at up to 50% off big-box "
            "retail &mdash; brands like Kohler and Moen from closeout and overstock lots, not seconds or returns. The "
            "exact models rotate week to week, but toilets, tubs, and faucets are core stock at both stores year-round.",
            "A bathroom refresh is one of the best returns on a remodel dollar, and much of it is DIY territory: "
            "swapping a faucet or installing a new toilet takes basic tools and an afternoon. Replacing a bathtub or "
            "moving supply lines is where a licensed plumber is the right call. The math works the same either way "
            "&mdash; labor costs what it costs, so buying the fixture at closeout price is where you win.",
            "Selection changes fast. Call either store and staff will tell you what's on the floor right now.",
        ],
        faq=[
            ("Where can I buy a discount toilet or bathtub in the OKC metro?",
             "Jameson's Discount Home Improvement — 7010 SE 15th Street in Midwest City and 8100 S. Santa Fe Ave in "
             "south OKC near I-240. Name-brand bath fixtures at up to 50% off retail."),
            ("Are these seconds or damaged units?",
             "No — closeout, overstock, and liquidation inventory. Name-brand, running-line product in the box."),
            ("Can I replace a faucet or toilet myself?",
             "Both are common DIY jobs with basic tools. Tub replacement or plumbing relocation is worth hiring a "
             "licensed plumber."),
            ("Do you match a specific model I found online?",
             "Inventory is closeout-driven, so we can't order specific models — but comparable name-brand units are "
             "usually on the floor for far less. Call ahead to check."),
        ]))

    cat.append(dict(
        slug="kitchen", nav="kitchen",
        title="Discount Kitchen OKC | Sinks, Faucets &amp; Fixtures | Jameson's",
        desc=("Name-brand kitchen sinks, faucets and fixtures at up to 50% off retail. Closeout inventory in "
              "Midwest City &amp; South OKC &mdash; call or visit for current stock."),
        h1="Discount kitchen &mdash; sinks, faucets &amp; fixtures in OKC up to 50% off",
        lead="The cheapest way to make a kitchen read \u201cupdated\u201d without touching the cabinets.",
        paras=[
            "Kitchen upgrades don't need a full remodel budget. Jameson's stocks kitchen sinks, faucets, and fixtures "
            "from name brands at closeout pricing &mdash; up to 50% off what the same class of product runs at big-box "
            "retail. Because stock comes in by the truckload from closeouts and overstock, the mix changes constantly, "
            "which is exactly why the prices are what they are.",
            "A faucet swap is a first-timer's DIY job; an undermount sink in a stone counter is a job for a pro. In "
            "both cases the fixture is the cost you control &mdash; get it at closeout and the project math changes "
            "fast. If you're doing a rental-property refresh, this is the cheapest way to make a kitchen read "
            "\u201cupdated\u201d without touching cabinets.",
        ],
        faq=[
            ("Where can I find discount kitchen sinks and faucets near Oklahoma City?",
             "Jameson's Discount Home Improvement, with stores in Midwest City (7010 SE 15th Street) and south OKC "
             "(8100 S. Santa Fe Ave near I-240). Closeout name-brand stock at up to 50% off."),
            ("Is this good enough quality for a rental or a flip?",
             "It's the same name-brand, in-box product sold at national retailers — bought as closeout lots, which is "
             "where the discount comes from."),
            ("Can I install a kitchen faucet myself?",
             "Usually yes — basic tools, shutoff valves, and an hour or two. Undermount sink installs and counter "
             "modifications are pro territory."),
            ("What's in stock right now?",
             "It changes weekly. Call 405-206-8111 (Midwest City) or 405-479-7918 (South OKC) and staff will check "
             "the floor."),
        ]))

    cat.append(dict(
        slug="lighting", nav="lighting",
        title="Discount Lighting &amp; Ceiling Fans OKC | Up to 50% Off | Jameson's",
        desc=("Name-brand light fixtures and ceiling fans at closeout prices in Midwest City &amp; South OKC. "
              "Stock rotates weekly &mdash; call or visit."),
        h1="Discount lighting &amp; ceiling fans in OKC &mdash; up to 50% off name brands",
        lead="Chandeliers, vanity bars, flush mounts, LED and fans &mdash; the fastest way to modernize a room.",
        paras=[
            "Lighting is the fastest way to modernize a room, and Jameson's makes it cheap: name-brand light fixtures, "
            "ceiling fans, and LED lighting at closeout prices, up to 50% off retail. Chandeliers, vanity bars, flush "
            "mounts, and fans move through both stores continuously as closeout lots arrive.",
            "Swapping a light fixture or ceiling fan is a classic DIY job &mdash; kill the breaker, match the wires, "
            "mount the bracket. If a room needs new circuits or you're not comfortable at the panel, a licensed "
            "electrician is the right call. Fixture-for-fixture swaps at closeout prices are how a whole house gets a "
            "lighting refresh for the cost of two or three fixtures at full retail.",
        ],
        faq=[
            ("Where can I buy discount ceiling fans and light fixtures in the OKC metro?",
             "Jameson's Discount Home Improvement — Midwest City and south OKC near I-240. Name-brand fixtures and "
             "fans at up to 50% off retail."),
            ("Are these current styles or old stock?",
             "Closeout lots are typically running-line or recent-line product from national brands — the discount "
             "comes from how we buy, not from age or damage."),
            ("Can I replace a light fixture myself?",
             "Like-for-like swaps are common DIY with the breaker off. New circuits or panel work call for a licensed "
             "electrician."),
            ("Do you stock LED?",
             "Yes — LED fixtures and lighting regularly come through both stores."),
        ]))

    cat.append(dict(
        slug="tools", nav="tools",
        title="Discount Tools OKC | Name-Brand Power &amp; Hand Tools | Jameson's",
        desc=("Name-brand power and hand tools at closeout prices in Midwest City &amp; South OKC. Lots move fast "
              "&mdash; call or stop by for today's stock."),
        h1="Discount name-brand tools in OKC &mdash; closeout prices at Jameson's",
        lead="The fastest-moving category in the store. Lots land, get priced to move, and go.",
        paras=[
            "Jameson's carries name-brand power tools and hand tools &mdash; brands like Milwaukee among them &mdash; "
            "at closeout prices well below big-box retail. Tool inventory is the most fast-moving category in the "
            "store: closeout lots land, get priced to move, and go. That's good news if you check in regularly and "
            "bad news if you wait a week on the drill you saw.",
            "For DIYers gearing up for the projects on our other pages &mdash; flooring installs, faucet swaps, vanity "
            "replacements &mdash; this is the cheapest way to build the kit. Contractors grabbing backup or crew tools "
            "do well here too.",
        ],
        faq=[
            ("Is there a discount tool outlet in the OKC metro?",
             "Yes — Jameson's Discount Home Improvement in Midwest City (7010 SE 15th Street) and south OKC "
             "(8100 S. Santa Fe Ave). Name-brand tools at closeout prices."),
            ("Are the tools new?",
             "Closeout and overstock inventory — new, in-box, name-brand product."),
            ("What brands do you carry?",
             "It depends on the current lots — name brands rotate through constantly. Call either store for what's on "
             "the shelf today."),
            ("Do you get repeat stock?",
             "Closeout lots are one-time buys. If you see a tool you need at the price you want, that's the day to "
             "buy it."),
        ]))

    cat.append(dict(
        slug="patio", nav="patio",
        title="Discount Patio Furniture OKC | Up to 50% Off | Jameson's",
        desc=("Closeout patio sets, outdoor furniture and decor at up to 50% off retail in Midwest City &amp; "
              "South OKC. New lots arrive through the season."),
        h1="Discount patio furniture &amp; outdoor living in OKC &mdash; up to 50% off",
        lead="Where retail markup runs highest, and closeout buying saves the most.",
        paras=[
            "Outdoor living is where retail markup runs highest &mdash; and where closeout buying saves the most. "
            "Jameson's stocks patio sets, outdoor furniture, and decor at up to 50% off retail, with new lots arriving "
            "through the season. Because it's closeout inventory, the styles change constantly: what's on the floor in "
            "April won't be what's on the floor in July, and the best pieces go early.",
            "If you're staging a home for sale, a clean patio setup is one of the cheapest square-footage upgrades "
            "there is &mdash; it turns a bare slab into an extra \u201croom\u201d in listing photos for a few hundred "
            "dollars instead of a few thousand.",
        ],
        faq=[
            ("Where can I buy discount patio furniture in Oklahoma City?",
             "Jameson's Discount Home Improvement — Midwest City (7010 SE 15th Street) and south OKC (8100 S. Santa Fe "
             "Ave near I-240). Closeout patio sets and outdoor decor at up to 50% off."),
            ("When is the best selection?",
             "Early in the season, as lots arrive — but closeouts show up year-round. Call ahead for what's currently "
             "on the floor."),
            ("Do you deliver patio furniture?",
             "Sales are in-store; most sets load straight into a pickup. Call either store with questions about a "
             "specific piece."),
            ("Is it name-brand product?",
             "Yes — closeout and overstock lots from national brands, new in box or floor-ready."),
        ]))

    cat.append(dict(
        slug="rubbermulchokc", nav="rubbermulchokc",
        title="Playground Certified Bulk Rubber Mulch in Stock &mdash; OKC | Jameson's",
        desc=("IPEMA-certified playground rubber mulch in stock in the OKC metro: $8 per 24-lb bag, $601 per "
              "2,000-lb supersack, summer special $500 per supersack, pickup only."),
        h1="Playground certified bulk rubber mulch in stock &mdash; OKC",
        lead="IPEMA-certified chunk rubber nuggets, bagged or by the supersack, for pickup at either store.",
        chips=[("$8", "24-lb bag"), ("$601", "2,000-lb supersack"), ("$500", "summer special, pickup only")],
        paras=[
            "Jameson's stocks IPEMA-certified chunk rubber nuggets for playgrounds, landscape beds and play areas at "
            "both OKC-metro stores. Buy it by the 24-lb bag at $8, or by the 2,000-lb supersack at $601. All summer "
            "long, IPEMA-certified chunk rubber nuggets are $500 per supersack, pickup only. Volume discounts are "
            "available &mdash; ask at the counter.",
            "Rubber mulch is the low-maintenance choice for play areas: it doesn't decompose, doesn't need topping off "
            "every spring, and holds its fall-height rating far longer than wood chips. For playground use, depth is "
            "what matters &mdash; check the fall height of your equipment and buy to that depth, and add a bit for "
            "settling and displacement under swings and slides.",
            "Buying for a school, city park or a big install? That's what our wholesale arm is for. "
            "405RubberMulch.com delivers flatbed truckloads across Oklahoma, Kansas, Missouri and Arkansas.",
        ],
        faq=[
            ("Is your rubber mulch playground certified?",
             "Yes — IPEMA-certified chunk rubber nuggets, in stock for pickup at Jameson's."),
            ("What does rubber mulch cost in Oklahoma City?",
             "$8 per 24-lb bag and $601 per 2,000-lb supersack at Jameson's. All summer: IPEMA-certified chunk rubber "
             "nuggets at $500 per supersack, pickup only. Volume discounts available."),
            ("Do you deliver, or is it pickup only?",
             "In-store purchases are pickup. For truckload quantities delivered to schools, cities and contractors, "
             "our wholesale arm 405RubberMulch.com covers Oklahoma, Kansas, Missouri and Arkansas."),
            ("How much rubber mulch do I need?",
             "It depends on the area and the fall height your playground equipment requires. Bring your square footage "
             "and required depth to either store, or call 405-206-8111, and staff will run the numbers with you."),
        ]))

    cat.append(dict(
        slug="bulk-rubber-mulch", nav="bulk-rubber-mulch",
        title="Bulk Rubber Mulch &mdash; Supersacks &amp; Truckloads | OKC | Jameson's",
        desc=("Bulk IPEMA-certified rubber mulch in the OKC metro: $601 per 2,000-lb supersack, $500 summer special, "
              "pickup only. Flatbed truckload delivery through 405RubberMulch.com."),
        h1="Bulk rubber mulch &mdash; supersacks &amp; truckloads",
        lead="Supersacks for pickup at either store; flatbed truckloads delivered across four states.",
        chips=[("$601", "2,000-lb supersack"), ("$500", "summer special, pickup only"), ("4 states", "truckload delivery")],
        paras=[
            "For anything bigger than a few bags, the 2,000-lb supersack is the way to buy. Supersacks are $601 each, "
            "and all summer long IPEMA-certified chunk rubber nuggets are $500 per supersack, pickup only. Bring a "
            "truck or trailer rated for the load &mdash; a supersack weighs a ton, literally.",
            "405RubberMulch.com &mdash; our regional wholesale arm serving Oklahoma, Kansas, Missouri &amp; Arkansas "
            "&mdash; handles the volume side. Schools, municipalities, parks departments and contractors get flatbed "
            "truckload delivery of IPEMA-certified playground rubber mulch, quoted by the load.",
            "Not sure whether you need a supersack or a truckload? Call the Midwest City store at 405-206-8111 with "
            "your square footage and required depth and we'll tell you straight.",
        ],
        faq=[
            ("How much does a supersack of rubber mulch cost?",
             "$601 per 2,000-lb supersack. All summer, IPEMA-certified chunk rubber nuggets are $500 per supersack, "
             "pickup only. Volume discounts available."),
            ("Do you deliver truckloads?",
             "Yes — 405RubberMulch.com delivers flatbed truckloads to schools, cities and contractors across Oklahoma, "
             "Kansas, Missouri and Arkansas."),
            ("Is the bulk mulch the same certified product?",
             "Yes — IPEMA-certified chunk rubber nuggets, the same product sold in bags."),
            ("What do I need to pick up a supersack?",
             "A truck or trailer that can carry a full ton, and a way to unload it at the other end. Call ahead so we "
             "have it ready: 405-206-8111 Midwest City, 405-479-7918 South OKC."),
        ]))

    cat.append(dict(
        slug="inventory", nav="inventory",
        title="What's In Stock | Closeout Home Improvement Inventory | Jameson's OKC",
        desc=("What Jameson's stocks across both OKC-metro stores: flooring, vanities, bath, kitchen, lighting, "
              "tools, patio, paint and playground-certified rubber mulch. Inventory changes daily."),
        h1="What's in stock at Jameson's",
        lead="Inventory changes daily. Here's what's always in the building, and what to call about.",
        paras=[
            "Everything on our floor is closeout, overstock or end-of-line inventory bought by the truckload, so the "
            "specific models rotate constantly &mdash; but the categories below are core stock at both stores "
            "year-round. If you want to know whether a particular kind of item is on the floor today, calling is "
            "faster than driving: 405-206-8111 in Midwest City, 405-479-7918 in South OKC.",
        ],
        extra=lambda L: f'<div style="margin:1.4rem 0">{cat_grid(L)}</div>' + f'''
<div class="split" style="margin-top:1.2rem">
  <div class="card"><span class="eyebrow">Also always here</span><h3>Paint</h3>
  <p>Visions Quality Coatings Workhorse interior and exterior latex, $21.99 a gallon, in 1-gallon and 5-gallon buckets.</p></div>
  <div class="card"><span class="eyebrow">Also always here</span><h3>Rubber mulch</h3>
  <p>IPEMA-certified chunk rubber nuggets: $8 per 24-lb bag, $601 per 2,000-lb supersack, $500 summer special, pickup only.
  <a href="{L('rubbermulchokc')}">See mulch details</a>.</p></div>
</div>''',
        faq=[
            ("Can I see your inventory online?",
             "Not item by item — stock turns too fast for a live catalog. The category pages describe what's always in "
             "the building, and a phone call gets you today's floor: 405-206-8111 or 405-479-7918."),
            ("How often does new inventory arrive?",
             "New closeout lots land weekly. Popular items sell within days."),
            ("Do you hold items?",
             "Call the store and ask — it depends on the item and how much of the lot is left."),
            ("Do you buy or take trade-ins?",
             "We buy closeout, overstock and end-of-line lots from manufacturers and distributors. Call the Midwest "
             "City store at 405-206-8111 if you have a lot to move."),
        ]))

    cat.append(dict(
        slug="deals", nav="deals",
        title="This Week's Deals | Closeout Prices in OKC &amp; Midwest City | Jameson's",
        desc=("Current specials at Jameson's: IPEMA-certified rubber mulch $500 per supersack, Visions paint $21.99 "
              "a gallon, waterproof LVP from $2.19/sf. Two OKC-metro stores."),
        h1="Deals on the floor right now",
        lead="Standing prices that beat retail, plus whatever landed this week.",
        chips=[("$500", "supersack, summer special"), ("$21.99", "Visions paint, per gallon"),
               ("$2.19+", "waterproof LVP, per sq ft")],
        paras=[
            "Closeout pricing isn't a sale that ends Sunday &mdash; it's how the whole store is bought. Below are the "
            "standing prices worth planning around. Everything else is whatever came off the truck this week, which "
            "is why it pays to stop in regularly or follow us on Facebook and Instagram.",
        ],
        extra=lambda L: f'''
<div class="split" style="margin:1.3rem 0">
  <div class="card"><span class="eyebrow">Summer special</span><h3>Rubber mulch &mdash; $500 per supersack</h3>
  <p>IPEMA-certified chunk rubber nuggets, 2,000-lb supersack, pickup only. Regular price $601; bags are $8 for 24 lb.
  <a href="{L('bulk-rubber-mulch')}">Bulk details</a>.</p></div>
  <div class="card"><span class="eyebrow">Every day</span><h3>Visions paint &mdash; $21.99 a gallon</h3>
  <p>Workhorse interior and exterior latex in 1-gallon and 5-gallon buckets. Remanufactured premium paint,
  national-brand performance.</p></div>
  <div class="card"><span class="eyebrow">Every day</span><h3>Waterproof LVP &mdash; from $2.19/sf</h3>
  <p>Rigid-core, 12&ndash;20 mil wear layer, manufacturer warranty. Lot pricing runs $2.19&ndash;$2.69/sf.
  <a href="{L('flooring')}">Flooring details</a>.</p></div>
</div>''',
        faq=[
            ("Do you run weekly sales?",
             "The whole store is priced off closeout buying, so there's no weekly sale cycle. New lots arrive weekly "
             "and are priced to move when they hit the floor."),
            ("How do I find out what just came in?",
             "Follow us on Facebook and Instagram, or call the store: 405-206-8111 Midwest City, 405-479-7918 South OKC."),
            ("Are the specials at both stores?",
             "Pricing is the same at both, but the actual stock differs by store because lots get split. Call the one "
             "you plan to visit."),
            ("Do you price match?",
             "Our prices are already built off closeout buying rather than retail margins, so they're typically well "
             "under matched pricing to begin with."),
        ]))

    cat.append(dict(
        slug="about", nav="about",
        title="About Jameson's Discount Home Improvement Warehouse | OKC &amp; Midwest City",
        desc=("Who Jameson's is: a closeout home improvement warehouse with two Oklahoma City metro stores and a "
              "four-state rubber mulch wholesale arm, 405RubberMulch.com."),
        h1="About Jameson's",
        lead="A closeout warehouse with two OKC-metro stores and a four-state wholesale arm.",
        paras=[
            "Jameson's Discount Home Improvement Warehouse buys closeout, overstock and end-of-line inventory by the "
            "truckload from manufacturers and distributors, and sells it out of two Oklahoma City metro stores at up "
            "to half of what the same product costs at retail. The product is name-brand, running-line and in the box "
            "&mdash; the discount comes from how we buy, not from what it is.",
            "That's also why the floor changes constantly. There's no catalog and no back stock: when a lot is gone, "
            "it's gone, and something else is in its place. Customers who check in regularly do the best.",
            "The mulch side of the business scales all the way up. 405RubberMulch.com is our regional wholesale arm, "
            "delivering flatbed truckloads of IPEMA-certified playground rubber mulch to schools, cities and "
            "contractors across Oklahoma, Kansas, Missouri and Arkansas &mdash; while the retail stores keep bags and "
            "supersacks on hand for homeowners.",
        ],
        faq=[
            ("Where is Jameson's located?",
             "Two Oklahoma City metro stores: 7010 SE 15th Street, Midwest City, OK 73110 and 8100 S. Santa Fe Ave, "
             "Oklahoma City, OK 73139, near I-240."),
            ("What are your hours?",
             "Tuesday through Saturday 9:00 AM to 6:00 PM, Sunday 10:00 AM to 6:00 PM, closed Monday, at both stores."),
            ("Why are the prices so much lower than big-box stores?",
             "We buy closeout, overstock and end-of-line lots by the truckload rather than ordering from a catalog at "
             "wholesale list. The savings pass straight through."),
            ("Are you related to 405RubberMulch.com?",
             "Yes — 405RubberMulch.com is our regional wholesale arm for rubber mulch, serving Oklahoma, Kansas, "
             "Missouri and Arkansas."),
        ]))

    cat.append(dict(
        slug="location", nav="location",
        title="Hours &amp; Locations | Midwest City &amp; South OKC | Jameson's",
        desc=("Jameson's store hours and directions: 7010 SE 15th Street, Midwest City (405-206-8111) and 8100 S. "
              "Santa Fe Ave, Oklahoma City near I-240 (405-479-7918). Tue&ndash;Sat 9&ndash;6, Sun 10&ndash;6, closed Monday."),
        h1="Hours &amp; locations",
        lead="Two stores in the OKC metro. Same hours, same pricing, different floor stock.",
        paras=[
            "Both stores are open Tuesday through Saturday from 9:00 AM to 6:00 PM and Sunday from 10:00 AM to 6:00 "
            "PM, and both are closed on Monday. Sales are in-store, and because inventory is closeout-driven, calling "
            "the specific store before you drive out is the fastest way to know what's actually on the floor.",
        ],
        faq=[
            ("What are Jameson's hours?",
             "Tuesday through Saturday 9:00 AM to 6:00 PM, Sunday 10:00 AM to 6:00 PM, closed Monday — both locations."),
            ("Where is the Midwest City store?",
             "7010 SE 15th Street, Midwest City, OK 73110. Phone 405-206-8111."),
            ("Where is the South OKC store?",
             "8100 S. Santa Fe Ave, Oklahoma City, OK 73139, near I-240. Phone 405-479-7918."),
            ("Do both stores carry the same items?",
             "Same categories and same pricing, but closeout lots get split between stores, so specific items differ. "
             "Call the store you plan to visit."),
        ]))

    cat.append(dict(
        slug="contact", nav="contact",
        title="Contact Jameson's | Midwest City 405-206-8111 &middot; South OKC 405-479-7918",
        desc=("Contact Jameson's Discount Home Improvement Warehouse: Midwest City 405-206-8111, South OKC "
              "405-479-7918, save@discountokc.com. Tue&ndash;Sat 9&ndash;6, Sun 10&ndash;6, closed Monday."),
        h1="Contact us",
        lead="Call the store you plan to visit &mdash; staff will walk the floor and tell you what's there.",
        paras=[
            "The fastest answer to \u201cdo you have it?\u201d is a phone call to the specific store, because closeout "
            "stock differs between locations and turns over weekly. For wholesale rubber mulch truckloads, go through "
            "405RubberMulch.com.",
        ],
        extra=lambda L: '''
<div class="split" style="margin:1.3rem 0">
  <div class="card"><span class="eyebrow">Midwest City</span><h3>405-206-8111</h3>
  <p>7010 SE 15th Street, Midwest City, OK 73110</p>
  <div class="btnrow"><a class="btn btn-ink" href="tel:+14052068111">Call this store</a></div></div>
  <div class="card"><span class="eyebrow">South OKC &middot; near I-240</span><h3>405-479-7918</h3>
  <p>8100 S. Santa Fe Ave, Oklahoma City, OK 73139</p>
  <div class="btnrow"><a class="btn btn-ink" href="tel:+14054797918">Call this store</a></div></div>
  <div class="card"><span class="eyebrow">Email &amp; wholesale</span><h3>save@discountokc.com</h3>
  <p>General questions by email. Truckload rubber mulch quotes: <a href="https://405rubbermulch.com">405RubberMulch.com</a>.</p></div>
</div>''',
        faq=[
            ("What's the best way to reach Jameson's?",
             "Call the store directly: 405-206-8111 for Midwest City, 405-479-7918 for South OKC. Email is "
             "save@discountokc.com."),
            ("Can I order over the phone?",
             "Sales are in-store, but staff will happily check whether something is on the floor before you drive out."),
            ("Who do I contact about truckload rubber mulch?",
             "405RubberMulch.com, our regional wholesale arm serving Oklahoma, Kansas, Missouri and Arkansas."),
        ]))

    P.extend(cat)
    return P

# ===================== BUILD =====================
import json, os, re, shutil, html


OUT = os.path.dirname(os.path.abspath(__file__))

# BASE = "" for the real domain. On GitHub's temporary test URL the site lives
# under /discountokc/, so the workflow sets BASE=/discountokc while testing.
BASE = os.environ.get("BASE", "").rstrip("/")
# CNAME tells GitHub which custom domain to serve. Leave off until DNS cutover,
# otherwise the temporary test URL redirects to the domain (still on Wix).
WRITE_CNAME = os.environ.get("WRITE_CNAME", "") == "1"
SITEDIR = os.path.join(OUT, "_site")


def strip(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html.unescape(t))).strip()


# ----------------------------------------------------------------- schema
STORES = [
    dict(_id="#midwest-city", tel="+1-405-206-8111", street="7010 SE 15th Street",
         city="Midwest City", zipc="73110",
         desc="Closeout home improvement warehouse with name-brand products up to 50% off retail. "
              "Vanities, flooring, bath, kitchen, lighting, tools, patio and more.",
         area=["Midwest City", "Del City", "Oklahoma City", "Choctaw", "Nicoma Park", "Harrah"]),
    dict(_id="#south-okc", tel="+1-405-479-7918", street="8100 S. Santa Fe Ave",
         city="Oklahoma City", zipc="73139",
         desc="Closeout home improvement warehouse near I-240 with name-brand products up to 50% off retail.",
         area=["Oklahoma City", "Moore", "Norman", "Del City", "Newcastle"]),
]
HOURS = [
    {"@type": "OpeningHoursSpecification",
     "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
     "opens": "09:00", "closes": "18:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday"], "opens": "10:00", "closes": "18:00"},
]


def store_nodes():
    out = []
    for s in STORES:
        out.append({
            "@type": "HardwareStore", "@id": SITE + "/" + s["_id"], "name": BIZ, "url": SITE,
            "telephone": s["tel"], "priceRange": "$$", "description": s["desc"],
            "address": {"@type": "PostalAddress", "streetAddress": s["street"], "addressLocality": s["city"],
                        "addressRegion": "OK", "postalCode": s["zipc"], "addressCountry": "US"},
            "openingHoursSpecification": HOURS, "areaServed": s["area"], "email": "save@discountokc.com",
            "sameAs": ["https://www.instagram.com/discountokc/",
                       "https://www.instagram.com/jamesons_discount_mwc/"],
        })
    out.append({
        "@type": "Organization", "@id": "https://405rubbermulch.com/#org", "name": "405RubberMulch.com",
        "url": "https://405rubbermulch.com",
        "description": "Regional wholesale arm of Jameson's Discount Home Improvement Warehouse, delivering flatbed "
                       "truckloads of IPEMA-certified playground rubber mulch across Oklahoma, Kansas, Missouri and Arkansas.",
        "areaServed": ["Oklahoma", "Kansas", "Missouri", "Arkansas"],
        "parentOrganization": {"@id": SITE + "/#midwest-city"},
    })
    return out


def faq_node(pid, faq):
    return {"@type": "FAQPage", "@id": pid + "#faq",
            "mainEntity": [{"@type": "Question", "name": strip(q),
                            "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]}


def page_schema(p):
    url = SITE + "/" + (p["slug"] + "/" if p["slug"] else "")
    if p["slug"] == "":
        graph = store_nodes() + [faq_node(url, p["faq"])]
    else:
        graph = [
            {"@type": "WebPage", "@id": url, "url": url, "name": strip(p["title"]),
             "description": strip(p["desc"]), "isPartOf": {"@id": SITE + "/#midwest-city"}},
            {"@type": "BreadcrumbList", "@id": url + "#crumbs", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": strip(p["h1"]), "item": url}]},
            faq_node(url, p["faq"]),
        ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


# ------------------------------------------------------------ page bodies
def interior_body(p, L):
    chips = ""
    if p.get("chips"):
        chips = '<div class="prices">' + "".join(
            f'<div class="chip"><b>{v}</b>{lbl}</div>' for v, lbl in p["chips"]) + "</div>"
    paras = "".join(f"<p>{t}</p>" for t in p.get("paras", []))
    extra = p["extra"](L) if p.get("extra") else ""
    return f'''
<div class="pagehead"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{L('')}">Home</a> / {strip(p['h1'])}</nav>
  <h1>{p['h1']}</h1>
  {f'<p class="lead">{p["lead"]}</p>' if p.get("lead") else ''}
</div></div>
<section><div class="wrap">
  {chips}
  {paras}
  {extra}
  <div style="margin-top:1.6rem">{VSLOT}</div>
</div></section>
<section class="tight"><div class="wrap">
  <div class="sechead"><span class="eyebrow">Answers</span><h2>Questions, answered</h2></div>
  {faq_html([(q, a) for q, a in p['faq']])}
</div></section>
{locations_block("Come see it in person")}
'''


def render_body(p, L):
    return p["body"] if p.get("kind") == "home" else interior_body(p, L)


# ------------------------------------------------------------- deploy tree
def dep_link(slug):
    return (BASE + "/") if slug == "" else f"{BASE}/{slug}/"


def full_page(p, body, L):
    url = SITE + "/" + (p["slug"] + "/" if p["slug"] else "")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{p['title']}</title>
<meta name="description" content="{strip(p['desc'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="{'website' if p['slug']=='' else 'article'}">
<meta property="og:title" content="{strip(p['title'])}">
<meta property="og:description" content="{strip(p['desc'])}">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#3D4E9E">
{FONTS}
<link rel="stylesheet" href="{BASE}/assets/site.css">
<script type="application/ld+json">
{page_schema(p)}
</script>
</head>
<body>
{topbar(L)}
{masthead(L)}
{catnav(L, p['nav'])}
<main>
{body}
</main>
{footer(L)}
</body>
</html>
'''


def build_deploy():
    if os.path.isdir(SITEDIR):
        shutil.rmtree(SITEDIR)
    os.makedirs(os.path.join(SITEDIR, "assets"), exist_ok=True)
    with open(os.path.join(SITEDIR, "assets", "site.css"), "w") as f:
        f.write(CSS)
    pages = build_pages(dep_link)
    urls = []
    for p in pages:
        body = render_body(p, dep_link)
        d = SITEDIR if p["slug"] == "" else os.path.join(SITEDIR, p["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w") as f:
            f.write(full_page(p, body, dep_link))
        urls.append(SITE + "/" + (p["slug"] + "/" if p["slug"] else ""))

    # 404
    nf = dict(slug="404", nav="", title="Page not found | " + BIZ, desc="Page not found.",
              h1="That page isn't here", lead="It may have moved. Try a category below, or call the store.",
              paras=["If you were looking for something specific, call Midwest City at 405-206-8111 or South OKC at "
                     "405-479-7918 and we'll point you the right way."],
              extra=lambda L: cat_grid(L), faq=[])
    body404 = f'''<div class="pagehead"><div class="wrap"><h1>{nf['h1']}</h1>
<p class="lead">{nf['lead']}</p></div></div>
<section><div class="wrap"><p>{nf['paras'][0]}</p>{cat_grid(dep_link)}</div></section>'''
    with open(os.path.join(SITEDIR, "404.html"), "w") as f:
        f.write(f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{nf['title']}</title>
<meta name="robots" content="noindex">{FONTS}<link rel="stylesheet" href="{BASE}/assets/site.css"></head><body>
{topbar(dep_link)}{masthead(dep_link)}{catnav(dep_link,'')}<main>{body404}</main>{footer(dep_link)}</body></html>''')

    with open(os.path.join(SITEDIR, "sitemap.xml"), "w") as f:
        items = "".join(f"<url><loc>{u}</loc><changefreq>weekly</changefreq></url>" for u in urls)
        f.write('<?xml version="1.0" encoding="UTF-8"?>'
                f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>')
    with open(os.path.join(SITEDIR, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    if WRITE_CNAME:
        with open(os.path.join(SITEDIR, "CNAME"), "w") as f:
            f.write("www.discountokc.com\n")
    return pages


# ------------------------------------------------------------ preview file
def prev_link(slug):
    return "#/" if slug == "" else f"#/{slug}"


def build_preview():
    pages = build_pages(prev_link)
    data = {}
    for p in pages:
        data[p["slug"]] = {"t": strip(p["title"]), "nav": p["nav"], "html": render_body(p, prev_link)}
    js = json.dumps(data, ensure_ascii=False)
    home = pages[0]
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{home['title']}</title>
<meta name="description" content="{strip(home['desc'])}">
<meta name="theme-color" content="#3D4E9E">
{FONTS}
<style>{CSS}</style>
<script type="application/ld+json">
{page_schema(home)}
</script>
</head>
<body>
{topbar(prev_link)}
{masthead(prev_link)}
{catnav(prev_link, "")}
<main id="app"></main>
{footer(prev_link)}
<script>
const PAGES = {js};
function route(){{
  var s = (location.hash || '#/').replace(/^#\\/?/,'').replace(/\\/$/,'');
  var p = PAGES[s] || PAGES[''];
  document.getElementById('app').innerHTML = p.html;
  document.title = p.t;
  document.querySelectorAll('.catnav a').forEach(function(a){{
    a.classList.toggle('on', a.getAttribute('href') === (s ? '#/'+s : '#/'));
  }});
  window.scrollTo(0,0);
}}
window.addEventListener('hashchange', route);
route();
</script>
</body>
</html>
'''


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pages = build_deploy()
    with open(os.path.join(SITEDIR, "preview.html"), "w") as f:
        f.write(build_preview())
    print("pages:", len(pages), [p["slug"] or "(home)" for p in pages])
