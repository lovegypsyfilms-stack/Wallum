#!/usr/bin/env python3
"""Build the Wallum site into one self-contained HTML file.

Sources of truth:
    brand.css              the identity, shared by both versions
    src/index.html         Version B — reduced, brand-aligned copy
    src/their-copy.html    Version A — CLAI's existing copy, verbatim
    fonts/  photos/        assets

Everything is folded into a single index.html: the stylesheet inlined, the
fonts and photographs embedded as data: URIs, and both versions in the one
document toggled by the switcher.

It is built this way because preview sandboxes do not reliably serve a page's
sub-resources — an external stylesheet renders as unstyled HTML, missing
images render as blank panels, and a link to a second HTML file goes nowhere.
A single file with nothing external has none of those failure modes.

    python3 build.py
"""
import base64, pathlib, re

root = pathlib.Path(__file__).parent
MIME = {".woff2": "font/woff2", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


def embed(css: str) -> str:
    """Replace every url("fonts/…") / url("photos/…") with a data: URI."""
    def sub(m):
        rel = m.group(1).strip()
        p = root / rel
        if not p.exists():
            raise SystemExit(f"brand.css references {rel}, which does not exist")
        b64 = base64.b64encode(p.read_bytes()).decode("ascii")
        return f'url("data:{MIME[p.suffix.lower()]};base64,{b64}")'
    return re.sub(r'url\(\s*["\']?((?:fonts|photos)/[^"\')]+)["\']?\s*\)', sub, css)


def body(name: str) -> str:
    """Everything after the <!--BRAND--> marker, minus the old switcher."""
    src = (root / "src" / name).read_text(encoding="utf-8")
    if "<!--BRAND-->" not in src:
        raise SystemExit(f"src/{name} is missing the <!--BRAND--> marker")
    out = src.split("<!--BRAND-->", 1)[1]
    return re.sub(r'(?s)<nav class="vswitch".*?</nav>', "", out).strip()


css = embed((root / "brand.css").read_text(encoding="utf-8"))

page = f"""<meta charset="utf-8">
<title>Wallum Be Here</title>
<style>
{css}
</style>

<div class="ver" id="ver-b">
{body("index.html")}
</div>

<div class="ver" id="ver-a" hidden>
{body("their-copy.html")}
</div>

<div class="ver" id="ver-s" hidden>
{(root / "src" / "stewardship.html").read_text(encoding="utf-8").strip()}
</div>

<nav class="vswitch" aria-label="Pitch version">
  <b>Version</b>
  <button type="button" id="to-b" aria-current="page">B &middot; Reduced</button>
  <button type="button" id="to-a">A &middot; Full CLAI copy</button>
  <span class="sep" aria-hidden="true"></span>
  <b>Hero</b>
  <button type="button" class="hero-pick" data-hero="">1</button>
  <button type="button" class="hero-pick" data-hero="hero--dawn">2</button>
  <button type="button" class="hero-pick" data-hero="hero--frog" aria-current="page">3</button>
</nav>

<script>
  (function () {{
    var views = {{ b: document.getElementById("ver-b"),
                   a: document.getElementById("ver-a"),
                   s: document.getElementById("ver-s") }};
    var tabs = {{ b: document.getElementById("to-b"), a: document.getElementById("to-a") }};
    function show(which) {{
      Object.keys(views).forEach(function (k) {{ views[k].hidden = k !== which; }});
      // stewardship lives under version B, so B stays marked while it is open
      var lit = which === "s" ? "b" : which;
      Object.keys(tabs).forEach(function (k) {{
        if (k === lit) tabs[k].setAttribute("aria-current", "page");
        else tabs[k].removeAttribute("aria-current");
      }});
      window.scrollTo(0, 0);
    }}
    tabs.b.addEventListener("click", function () {{ show("b"); }});
    tabs.a.addEventListener("click", function () {{ show("a"); }});
    // any link carrying data-view switches instead of navigating
    document.addEventListener("click", function (e) {{
      var el = e.target.closest("[data-view]");
      if (!el) return;
      e.preventDefault();
      show(el.getAttribute("data-view"));
    }});
    // hero picker — swaps the first frame in place
    var picks = document.querySelectorAll(".hero-pick");
    picks.forEach(function (btn) {{
      btn.addEventListener("click", function () {{
        var hero = document.querySelector("#ver-b .hero");
        if (!hero) return;
        hero.classList.remove("hero--dawn", "hero--frog");
        var v = btn.getAttribute("data-hero");
        if (v) hero.classList.add(v);
        picks.forEach(function (o) {{
          if (o === btn) o.setAttribute("aria-current", "page");
          else o.removeAttribute("aria-current");
        }});
        show("b");
      }});
    }});
  }})();
</script>
"""
out = root / "index.html"
out.write_text(page, encoding="utf-8")
(root / "their-copy.html").unlink(missing_ok=True)
print(f"built index.html  ({len(page):,} bytes, {len(page)/1048576:.2f} MB) — one file, nothing external")
