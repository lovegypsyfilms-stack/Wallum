#!/usr/bin/env python3
"""Build the VOICES comp — a layout study, not a page of the site.

The question this answers is "what does a layer of public voices look like
above the supporter wall". The answer here is that it does not need a badge
to separate it from the wall: a voice is someone who said something, so the
band carries words, and the size and the quote do the work a label was being
asked to do.

Nobody real appears here. The portraits are the same invented, generated
faces already standing in on the wall, and every name, role and line of
quoted speech is lorem — marked as such on the page itself. This page is a
frame to drop real endorsers into once they have agreed, and it is built
outside the site so it cannot be mistaken for part of it.

    python3 gen-voices-comp.py        ->  preview-voices.html
"""
import base64, pathlib, re

root = pathlib.Path(__file__).parent
MIME = {".woff2": "font/woff2", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


def embed(css: str) -> str:
    def sub(m):
        rel = m.group(1).strip()
        p = root / rel
        if not p.exists():
            raise SystemExit(f"references {rel}, which does not exist")
        b64 = base64.b64encode(p.read_bytes()).decode("ascii")
        return f'url("data:{MIME[p.suffix.lower()]};base64,{b64}")'
    return re.sub(r'url\(\s*["\']?((?:fonts|photos)/[^"\')]+)["\']?\s*\)', sub, css)


css = embed((root / "brand.css").read_text(encoding="utf-8"))

# Placeholder only. Slot, role, and the shape of a usable line — no real person.
VOICES = [
    ("marlya", "Placeholder name",  "Role or standing, one line",
     "One sentence in their own words about why this place matters."),
    ("hugh",   "Placeholder name",  "Role or standing, one line",
     "A second voice runs a little longer, because real speech does not come to length."),
    ("ros",    "Placeholder name",  "Role or standing, one line",
     "A third, shorter."),
    ("nia",    "Placeholder name",  "Role or standing, one line",
     "And a fourth, to show the row reflowing when the quotes are uneven."),
]

WALL = [
    ("tessa","Tessa","Byron Bay, NSW"), ("kai","Kai","Sunshine Coast, QLD"),
    ("mara","Mara","Noosa, QLD"), ("amara","Amara","Gold Coast, QLD"),
    ("tom","Tom","Grampians, VIC"), ("ravi","Ravi","Margaret River, WA"),
    ("hugh","Hugh","Tasman Peninsula, TAS"), ("lily","Lily","Wollongong, NSW"),
    ("ros","Ros","Eden, NSW"), ("noah","Noah","Torquay, VIC"),
    ("marlya","Marlya","Arrernte Country, NT"), ("leilani","Leilani","Garry Beach, NSW"),
    ("nia","Nia","Bundjalung Country, NSW"), ("mei","Mei","Kiama, NSW"),
    ("sophie","Sophie","Bellingen, NSW"),
]

voices = "\n".join(
    '      <li class="voice">\n'
    '        <div class="voice-face w-%s"></div>\n'
    '        <blockquote class="voice-said"><p>%s</p></blockquote>\n'
    '        <p class="voice-who"><b>%s</b><span>%s</span></p>\n'
    '      </li>' % (slug, said, name, role)
    for slug, name, role, said in VOICES)

wall = "\n".join(
    '        <li class="wtile w-%s"><span class="wname">%s</span>'
    '<span class="wplace">%s</span></li>' % (slug, name, place)
    for slug, name, place in WALL)

page = """<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<title>Wallum &middot; voices band, layout comp</title>
<style>
%s

  /* ================= COMP CHROME ================= */
  .comp-note{
    background:#2A1E10; color:#F3E6CE; border-bottom:1px solid rgba(217,188,130,.35);
  }
  .comp-note .inner{ padding-block:18px; }
  .comp-note h1{
    font-family:var(--body); font-weight:800; font-size:.72rem;
    letter-spacing:.16em; text-transform:uppercase; color:var(--brass-lt); margin:0 0 8px;
  }
  .comp-note p{ margin:0 0 6px; font-size:.9rem; line-height:1.5; max-width:74ch; }
  .comp-note p:last-child{ margin-bottom:0; }
  .comp-note b{ color:#FFF3DC; font-weight:700; }

  /* ================= VOICES ================= */
  /* No badge. A voice is someone who said something, so this band carries
     speech and the wall below carries faces — the difference in kind is
     what separates them, and it needs no label to be read. */
  .voices{ background:var(--ink); color:#EFEADC; }
  .voices .inner{ padding-block:clamp(48px,6vw,84px); }
  .voices .section-title{ color:#F6F2E7; }
  .voices-lede{
    max-width:52ch; margin:10px auto 0; text-align:center;
    font-size:clamp(.95rem,1.3vw,1.08rem); line-height:1.55;
    color:rgba(239,234,220,.72);
  }
  .voice-row{
    list-style:none; margin:clamp(30px,4vw,48px) 0 0; padding:0;
    display:grid; gap:clamp(20px,2.6vw,34px);
    grid-template-columns:repeat(auto-fit,minmax(215px,1fr));
  }
  /* the quote row absorbs the slack so the names sit on one baseline
     however unevenly real speech falls */
  .voice{
    display:grid; gap:14px; justify-items:center; text-align:center;
    grid-template-rows:auto 1fr auto; align-content:start;
  }
  .voices .section-title{ text-align:center; }
  .voice-face{
    width:clamp(96px,10vw,128px); aspect-ratio:1; border-radius:50%%;
    background-size:cover; background-position:center 20%%;
    box-shadow:0 0 0 1px rgba(217,188,130,.34), 0 8px 26px rgba(0,0,0,.5);
  }
  .voice-said{ margin:0; align-self:center; }
  .voice-said p{
    margin:0; font-family:var(--display); font-weight:600;
    font-size:clamp(1rem,1.5vw,1.16rem); line-height:1.4;
    letter-spacing:-.012em; color:#F6F2E7;
  }
  .voice-said p::before{ content:"\\201C"; }
  .voice-said p::after{ content:"\\201D"; }
  .voice-who{ margin:0; display:grid; gap:2px; }
  .voice-who b{
    font-family:var(--body); font-weight:700; font-size:.82rem;
    letter-spacing:.01em; color:var(--brass-lt);
  }
  .voice-who span{
    font-family:var(--body); font-weight:500; font-size:.72rem;
    line-height:1.35; color:rgba(239,234,220,.6);
  }
  .voices-rule{
    width:min(100%%,120px); height:1px; margin:clamp(42px,5vw,66px) auto 0;
    background:linear-gradient(90deg,rgba(217,188,130,0),rgba(217,188,130,.5),rgba(217,188,130,0));
  }
  @media(max-width:700px){
    :root{ font-size:150%%; }
    .voice-row{ grid-template-columns:1fr; }
    .voice-face{ width:104px; }
  }
</style>

<section class="band comp-note">
  <div class="inner">
    <h1>Layout comp &mdash; not part of the site</h1>
    <p>This is the voices band as a <b>frame</b>, shown above the supporter wall so the two
       can be judged together. Every name, role and quoted line below is <b>placeholder text</b>,
       and the portraits are the same <b>invented, generated faces</b> already standing in on the
       wall. No real person appears on this page.</p>
    <p>The band takes a real name only once that person has agreed, in writing, to be shown
       supporting the campaign &mdash; and it holds the sentence they actually gave.</p>
  </div>
</section>

<section class="band grain voices">
  <div class="inner">
    <h2 class="section-title">Voices</h2>
    <p class="voices-lede">A few people say why, in their own words.</p>
    <ul class="voice-row">
%s
    </ul>
    <div class="voices-rule"></div>
  </div>
</section>

<section class="band grain gather">
  <div class="gather-globe"></div>
  <div class="inner">
    <div class="gather-copy">
      <h2>Come together.</h2>
      <p class="big-idea">Wallum becomes a place humanity gathers around.</p>
    </div>
    <ul class="wall" aria-label="People who are here">
%s
    </ul>
    <p class="wall-note">Every person who joins appears here.</p>
  </div>
</section>
""" % (css, voices, wall)

out = root / "preview-voices.html"
out.write_text(page, encoding="utf-8")
print("built %s  (%s bytes)" % (out.name, format(len(page.encode()), ",")))
