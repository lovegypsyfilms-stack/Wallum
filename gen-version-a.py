#!/usr/bin/env python3
"""Generate src/their-copy.html — Version A, CLAI's copy in the Wallum identity.

CLAI's site is ~6,500 words across six pages. Pasted into one column it reads
as an unbroken wall. This breaks it at the headings their own content already
has — Koala, Glossy Black Cockatoos, Wallum Froglet and so on — gives each
section a photographic header, and puts a clickable index above them so a
reader can go straight to what they came for.

Source text: source-copy/clai.json, scraped from clai.au on 14 Sep 2026.
Not rewritten — that is the whole point of Version A.

    python3 gen-version-a.py && python3 build.py
"""
import html, json, pathlib, re

root = pathlib.Path(__file__).parent
P = json.loads((root / "clai.json").read_text(encoding="utf-8"))

ECO = "ecology-cultural-heritage"

# Grouped so the index reads as an argument rather than a list of links.
# (group title, [(id, label, image class, [(page, lo, hi), ...]), ...])
GROUPS = [
    ("Why we are here", [
        ("vision",   "Vision and mission",     "img-girl",     [("about-us", 1, 14)]),
        ("land",     "The land",               "img-land",     [("wallum", 0, None)]),
        ("culture",  "Cultural significance",  "img-heath",    [(ECO, 1, 4)]),
    ]),
    ("The living world", [
        ("biodiv",   "Biodiversity",           "img-hero",      [(ECO, 5, 44)]),
        ("koala",    "Koala",                  "img-trees",    [(ECO, 45, 52)]),
        ("cockatoo", "Glossy black-cockatoo",  "img-cockatoo", [(ECO, 53, 56)]),
        ("water",    "Water and the froglet",  "img-frog",     [(ECO, 57, None)]),
    ]),
    ("Taking part", [
        ("donate",   "Donate",                 "img-flower",   [("pledge", 0, 8)]),
        ("pledge",   "Pledge and endorsements","img-dusk",     [("pledge", 9, None)]),
        ("member",   "Membership and contact", "img-gather",   [("membership", 0, None),
                                                                ("contact-us", 0, None)]),
        ("team",     "Team and advisors",      "img-canopy",    [("about-us", 15, None)]),
    ]),
]
SECTIONS = [sec for _t, secs in GROUPS for sec in secs]

# Facts worth catching the eye on a page this long. Bolded on first appearance
# within a section only — these are CLAI's own words, not added emphasis.
KEY = [
    "9 EPBC Federally-listed Threatened Species", "12 NSW listed Threatened Species",
    "9 Federal EPBC listed Threatened Species", "last 1% of Wallum heathland",
    "124 residential lots", "Target: $35m in currency funds and Biodiversity Credits",
    "Lot 13 DP1251383", "Conservation Land Trust", "in perpetuity",
    "fully tax deductible", "Registered Charity",
    "THIS IS NATIONAL HERITAGE; it is no place for bulldozers.",
]
LABEL = re.compile(r"^([A-Z][A-Za-z'&/,\- ]{2,46}):$")
# "Bob Brown: I wholeheartedly endorse ..." — a name and its statement sharing
# one paragraph. Split so the name becomes a heading you can scan for.
INLINE = re.compile(r"^([A-Z][A-Za-z'&/,\- ]{2,46}):\s+(\S.*)$", re.S)
SHOUT = re.compile(r"^[A-Z][A-Z '&\-]{3,46}$")

DROP = {"about us", "contact us", "wallum heathland", "cultural heritage biodiversity",
        "read more", "home", "pledge", "membership", "donate", "join clai", "scroll to top"}
FORMY = re.compile(r"(?i)fields marked with|your name \*|your email \*|phone number \*|"
                   r"subject \*|message \*|residential address \*|membership contributed")


def render(page, lo, hi):
    """Blocks lo..hi of a page as HTML. The section's own heading is dropped —
    it has been promoted into the photographic header above it."""
    blocks = P[page][lo: (hi + 1) if hi is not None else None]
    out, first, seen_keys = [], True, set()
    for b in blocks:
        t = b["text"].strip()
        if first and b["tag"] in ("h2", "h3"):
            first = False
            continue
        first = False
        if b["tag"] == "li" and t.lower() in DROP:
            continue
        if FORMY.search(t):
            continue
        e = html.escape(t, quote=False)
        if b["tag"] == "li":
            out.append(f"        <li>{e}</li>"); continue
        if b["tag"] in ("h2", "h3"):
            out.append(f"        <h3>{e}</h3>"); continue
        m = LABEL.match(t)
        if m:                      # "Endorsements:" — a heading in disguise
            out.append(f"        <h3>{html.escape(m.group(1), quote=False)}</h3>"); continue
        if SHOUT.match(t):         # "PLEDGE OF SUPPORT"
            out.append(f"        <h3>{e}</h3>"); continue
        m = INLINE.match(t)
        if m:
            out.append(f"        <h3>{html.escape(m.group(1), quote=False)}</h3>")
            t, e = m.group(2), html.escape(m.group(2), quote=False)
        for phrase in KEY:
            p = html.escape(phrase, quote=False)
            if p in e and p not in seen_keys:
                e = e.replace(p, f"<strong>{p}</strong>", 1); seen_keys.add(p); break
        cls = ' class="lead"' if not out else ""
        out.append(f"        <p{cls}>{e}</p>")
    res, inlist = [], False
    for line in out:
        li = "<li>" in line
        if li and not inlist:
            res.append("        <ul>"); inlist = True
        if not li and inlist:
            res.append("        </ul>"); inlist = False
        res.append(line)
    if inlist:
        res.append("        </ul>")
    return "\n".join(res)


def words(page, lo, hi):
    b = P[page][lo: (hi + 1) if hi is not None else None]
    return sum(len(x["text"].split()) for x in b)


n = 0
index_groups, secs = [], []
for gi, (gtitle, gsecs) in enumerate(GROUPS, 1):
    row = []
    for sid, label, img, parts in gsecs:
        n += 1
        row.append(f'          <a class="tile {img}" href="#{sid}">'
                   f'<b>{n:02d}</b><span>{html.escape(label)}</span></a>')
    index_groups.append(f"""      <div class="group">
        <div class="group-head">
          <span class="group-num">{gi:02d}</span>
          <h3>{html.escape(gtitle)}</h3>
        </div>
        <div class="tiles tiles--{len(gsecs)}">
{chr(10).join(row)}
        </div>
      </div>""")

    secs.append(f"""  <section class="band groupband" id="g{gi}">
    <div class="inner">
      <span class="group-num">{gi:02d}</span>
      <h2>{html.escape(gtitle)}</h2>
    </div>
  </section>""")

    for k, (sid, label, img, parts) in enumerate(gsecs, 1):
        body = "\n".join(render(pg, lo, hi) for pg, lo, hi in parts)
        wc = sum(words(pg, lo, hi) for pg, lo, hi in parts)
        srcs = " &middot; ".join(f"clai.au/{pg}" for pg, _l, _h in parts)
        idx = sum(len(g[1]) for g in GROUPS[:gi-1]) + k
        secs.append(f"""  <section class="sechead {img}" id="{sid}">
    <div class="sechead-in">
      <span class="num">{idx:02d} &middot; {html.escape(gtitle)}</span>
      <h2>{html.escape(label)}</h2>
    </div>
  </section>
  <section class="band doc">
    <div class="inner stack">
      <div class="sec">
{body}
        <p class="wordcount">{wc} words &middot; {srcs}</p>
        <a class="backtop" href="#a-index">&uarr; All sections</a>
      </div>
    </div>
  </section>""")

total = sum(len(b["text"].split()) for pg in P for b in P[pg])
MARK = """<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true">
        <circle cx="24" cy="24" r="22"/><circle cx="24" cy="24" r="16.5"/><circle cx="24" cy="24" r="11"/>
        <path d="M24 34V17" stroke-linecap="round"/>
        <path d="M24 23c-4.2 0-6.6-2.6-6.6-6.4 3.9 0 6.6 2.4 6.6 6.4Z"/>
        <path d="M24 20.5c4.2 0 6.6-2.6 6.6-6.4-3.9 0-6.6 2.4-6.6 6.4Z"/>
      </svg>"""

page_html = f"""<!--BRAND-->

<header class="nav">
  <div class="nav-in">
    <a class="mark" href="#a-top" style="color:var(--brass-lt)">{MARK}
      <span><span class="mark-name">WALLUM</span><span class="mark-sub" style="display:block">HUMANITY REMEMBERS</span></span>
    </a>
    <ul class="nav-links">
      <li><a href="#a-index">All sections</a></li>
      <li><a href="#land">The land</a></li>
      <li><a href="#biodiv">Biodiversity</a></li>
      <li><a href="#donate">Donate</a></li>
    </ul>
    <a class="btn btn--solid" href="#donate">Donate</a>
  </div>
</header>

<main id="a-top">
  <section class="band grain hero">
    <div class="hero-sky"></div>
    <div class="hero-mist"></div>
    <div class="inner">
      <svg class="emblem rise" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width=".9" aria-hidden="true" style="color:var(--brass)">
        <circle cx="24" cy="24" r="22"/><circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="12"/><circle cx="24" cy="24" r="7"/>
        <path d="M24 36V15" stroke-linecap="round"/>
        <path d="M24 22c-4.6 0-7.2-2.9-7.2-7 4.3 0 7.2 2.6 7.2 7Z"/>
        <path d="M24 19.5c4.6 0 7.2-2.9 7.2-7-4.3 0-7.2 2.6-7.2 7Z"/>
      </svg>
      <h1 class="wordmark rise">Wallum</h1>
      <div class="hero-rule rise" aria-hidden="true"><i></i><b></b><i></i></div>
      <p class="behere rise">Help buy wallum</p>
      <p class="hero-lede rise hero-q">Join us to protect the Wallum Heathland at Brunswick Heads,
        NSW, preserving the natural ecology and indigenous cultural values in perpetuity for the
        benefit of all.</p>
      <p class="hero-what rise">Version A &mdash; CLAI's existing website copy, unedited, inside the
        Wallum identity. {total:,} words across {len(SECTIONS)} sections.</p>
      <div class="hero-cta rise">
        <span class="cta-pair">
          <a class="btn btn--solid" href="#a-index">Browse the sections</a>
          <span class="cta-note">Jump straight to what you want</span>
        </span>
        <span class="cta-pair">
          <a class="btn btn--ghost" href="#donate">Donate</a>
          <span class="cta-note">Accounts and pledge details</span>
        </span>
      </div>
    </div>
  </section>

  <section class="band index" id="a-index">
    <div class="inner">
      <div class="index-head">
        <p class="eyebrow">Contents</p>
        <h2>Everything on this page</h2>
        <p>CLAI's {total:,} words, grouped into {len(SECTIONS)} sections. Tap any one to go
          straight to it.</p>
      </div>
{chr(10).join(index_groups)}
    </div>
  </section>

{chr(10).join(secs)}
</main>

<footer class="foot">
  <div class="inner">
    <a class="mark" href="#a-top">{MARK}
      <span><span class="mark-name">WALLUM</span><span class="mark-sub" style="display:block">HUMANITY REMEMBERS</span></span>
    </a>
    <p class="foot-ack">We acknowledge the Bundjalung people as the Traditional Owners of the land
      and waters of Wallum, and pay respect to Elders past and present.</p>
    <p class="foot-tag">Land &middot; People &middot; A shared tomorrow</p>
  </div>
</footer>
"""
(root / "src" / "their-copy.html").write_text(page_html, encoding="utf-8")
print(f"src/their-copy.html — {len(SECTIONS)} sections, {total:,} words, {len(page_html):,} bytes")
