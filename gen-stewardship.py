#!/usr/bin/env python3
"""Generate src/stewardship.html — the page behind "Permanent stewardship".

The front page used to carry four small credibility tiles whose text was mine.
They are now one heading on the front page and four sections here, and the
text is CLAI's own, pulled from source-copy/clai.json so every claim is
traceable to something they published rather than to something I wrote.

    python3 gen-stewardship.py && python3 build.py
"""
import html, json, pathlib

root = pathlib.Path(__file__).parent
P = json.loads((root / "clai.json").read_text(encoding="utf-8"))

def block(page, i):
    return P[page][i]["text"].strip()

# (id, title, image class, lead, [(page, index), ...])
SECTIONS = [
    ("s-charity", "A registered charity", "img-flower",
     "Who receives the money, and what happens to it if the purchase fails.",
     [("pledge", 3), ("pledge", 6)]),
    ("s-gov", "Transparent governance", "img-land",
     "The accounts are published, and the purpose is written into the constitution.",
     [("pledge", 5), ("pledge", 8)]),
    ("s-trust", "Held in perpetuity", "img-hero",
     "Ownership is the point. A trust, not a covenant on somebody else's title.",
     [("about-us", 8), ("about-us", 10)]),
    ("s-plan", "A management plan", "img-ground",
     "Written with ecological and cultural advisers, and with Bundjalung Traditional Owners.",
     [("about-us", 9), ("about-us", 7)]),
]

secs = []
for i, (sid, title, img, lead, refs) in enumerate(SECTIONS, 1):
    paras = "\n".join(
        f"        <p>{html.escape(block(pg, ix), quote=False)}</p>" for pg, ix in refs)
    srcs = " &middot; ".join(sorted({f"clai.au/{pg}" for pg, _ix in refs}))
    secs.append(f"""  <section class="sechead {img}" id="{sid}">
    <div class="sechead-in">
      <span class="num">{i:02d} &middot; Permanent stewardship</span>
      <h2>{html.escape(title)}</h2>
    </div>
  </section>
  <section class="band doc">
    <div class="inner stack">
      <div class="sec">
        <p class="lead">{html.escape(lead)}</p>
{paras}
        <p class="wordcount">{srcs}</p>
      </div>
    </div>
  </section>""")

MARK = """<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true">
        <circle cx="24" cy="24" r="22"/><circle cx="24" cy="24" r="16.5"/><circle cx="24" cy="24" r="11"/>
        <path d="M24 34V17" stroke-linecap="round"/>
        <path d="M24 23c-4.2 0-6.6-2.6-6.6-6.4 3.9 0 6.6 2.4 6.6 6.4Z"/>
        <path d="M24 20.5c4.2 0 6.6-2.6 6.6-6.4-3.9 0-6.6 2.4-6.6 6.4Z"/>
      </svg>"""

page = f"""<header class="nav">
  <div class="nav-in">
    <a class="mark" href="#top" data-view="b" style="color:var(--brass-lt)">{MARK}
      <span><span class="mark-name">WALLUM</span><span class="mark-sub" style="display:block">HUMANITY REMEMBERS</span></span>
    </a>
    <ul class="nav-links">
      <li><a href="#s-charity">Charity</a></li>
      <li><a href="#s-gov">Governance</a></li>
      <li><a href="#s-trust">The trust</a></li>
      <li><a href="#s-plan">Management</a></li>
    </ul>
    <a class="btn btn--ghost" href="#top" data-view="b">&larr; Back</a>
  </div>
</header>

<main id="steward-page">
  <section class="band groupband steward-top">
    <div class="inner">
      <span class="group-num">Permanent stewardship</span>
      <h2>How Wallum is held</h2>
      <p>Bought outright and placed in a Conservation Land Trust, where it cannot be sold again.
        Four things make that binding rather than hopeful.</p>
    </div>
  </section>

{chr(10).join(secs)}

  <section class="band doc">
    <div class="inner stack" style="text-align:center">
      <a class="btn btn--solid" href="#top" data-view="b">&larr; Back to Wallum</a>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="inner">
    <a class="mark" href="#top" data-view="b">{MARK}
      <span><span class="mark-name">WALLUM</span><span class="mark-sub" style="display:block">HUMANITY REMEMBERS</span></span>
    </a>
    <p class="foot-ack">We acknowledge the Bundjalung people as the Traditional Owners of the land
      and waters of Wallum, and pay respect to Elders past and present.</p>
    <p class="foot-tag">Land &middot; People &middot; A shared tomorrow</p>
  </div>
</footer>
"""
(root / "src" / "stewardship.html").write_text(page, encoding="utf-8")
print(f"src/stewardship.html — {len(SECTIONS)} sections, {len(page):,} bytes")
