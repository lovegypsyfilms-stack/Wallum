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
<!-- DRAFT. Remove the robots line below — and robots.txt — at launch, or the
     finished site stays invisible to search engines. -->
<meta name="robots" content="noindex, nofollow">
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

<nav class="vswitch" aria-label="Version">
  <button type="button" id="to-b" aria-current="page">Version 1</button>
  <button type="button" id="to-a">Version 2 &middot; CLAI copy</button>
</nav>

<script>
  (function () {{
    // Fit "The last one per cent" to the exact width of WALLUM above it.
    // Letter-spacing is the only lever that does not alter cap height, so the
    // two lines stay locked to the same left and right edges. Trailing spacing
    // is compensated with a matching text-indent, and the result is measured
    // and corrected rather than trusted — rounding leaves a few pixels.
    function fitLockup() {{
      document.querySelectorAll(".hero .wordmark").forEach(function (mark) {{
        var sub = mark.parentNode.querySelector(".hero-onepc");
        if (!sub) return;
        var target = mark.getBoundingClientRect().width;
        // the rule and the sign-up form lock to this same measure
        var hero = mark.closest(".hero");
        if (hero && target) hero.style.setProperty("--lockup-w", target + "px");
        var n = (sub.textContent || "").trim().length;
        if (!target || n < 2) return;
        sub.style.letterSpacing = "0px";
        sub.style.textIndent = "0px";
        var ls = (target - sub.getBoundingClientRect().width) / n;
        for (var pass = 0; pass < 4; pass++) {{
          sub.style.letterSpacing = ls + "px";
          sub.style.textIndent = ls + "px";
          var diff = target - sub.getBoundingClientRect().width;
          if (Math.abs(diff) < 0.4) break;
          ls += diff / n;
        }}

        // The explainer under it fits the same measure, but by scale rather
        // than by tracking: it is a sentence in mixed case, and the spacing
        // it would take to stretch 335px to 484px would read as a caption
        // pulled apart. Sized to fit, it simply sets to the width. Below a
        // legible floor — a narrow phone — it gives up and wraps instead.
        var exp = mark.parentNode.querySelector(".hero-onepc-sub");
        if (!exp) return;
        exp.style.whiteSpace = "nowrap";
        exp.style.maxWidth = "none";
        exp.style.fontSize = "";
        var size = parseFloat(getComputedStyle(exp).fontSize);
        var w = exp.getBoundingClientRect().width;
        if (!w) return;
        size *= target / w;
        for (var p2 = 0; p2 < 4; p2++) {{
          exp.style.fontSize = size + "px";
          var d2 = target - exp.getBoundingClientRect().width;
          if (Math.abs(d2) < 0.4) break;
          size *= target / (target - d2);
        }}
        // A phone's lockup is only ~287px wide, and fitting the sentence into
        // that drives it to ~12px — smaller than the size the phone deliberately
        // scales everything up to. There it wraps at its own size instead.
        if (size < 14) {{
          exp.style.whiteSpace = ""; exp.style.maxWidth = ""; exp.style.fontSize = "";
        }}
      }});
    }}
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitLockup);
    window.addEventListener("resize", fitLockup);
    setTimeout(fitLockup, 0); setTimeout(fitLockup, 400);

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
      fitLockup();   // a hidden view measures zero, so fit it once it is shown
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
  }})();
</script>
"""
out = root / "index.html"
out.write_text(page, encoding="utf-8")
(root / "their-copy.html").unlink(missing_ok=True)
print(f"built index.html  ({len(page):,} bytes, {len(page)/1048576:.2f} MB) — one file, nothing external")
