#!/usr/bin/env python3
"""Inline brand.css into each page.

brand.css is the single source of truth for the identity. Both versions share
it, so a change to the brand is one edit here and a re-run of this script.

It is inlined rather than linked because the sandboxes these pages get previewed
in do not always apply an external stylesheet, which renders the site as raw
unstyled HTML. Inlining removes that failure mode everywhere.

    python3 build.py
"""
import pathlib

root = pathlib.Path(__file__).parent
css = (root / "brand.css").read_text(encoding="utf-8")

for name in ("index.html", "their-copy.html"):
    src = (root / "src" / name).read_text(encoding="utf-8")
    if "<!--BRAND-->" not in src:
        raise SystemExit(f"src/{name} is missing the <!--BRAND--> marker")
    out = src.replace("<!--BRAND-->", "<style>\n" + css + "\n</style>", 1)
    (root / name).write_text(out, encoding="utf-8")
    print(f"built {name}  ({len(out):,} bytes)")
