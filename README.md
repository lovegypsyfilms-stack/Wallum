# Wallum — Be Here

Campaign site for the acquisition and permanent protection of Wallum, a coastal
wetland on Bundjalung country in northern New South Wales.

## The two versions

- **`index.html`** — Version B. The reduced, brand-aligned site. ~616 words.
- **`their-copy.html`** — Version A. CLAI's existing website copy, verbatim,
  inside the same identity. ~6,509 words.

A switcher pinned to the bottom of both flips between them. It is pitch
scaffolding — delete `<nav class="vswitch">` from `src/` before launch.

## Editing it

`brand.css` is the single source of truth for the identity, shared by both
versions. The page bodies live in `src/`. After changing either, run:

```bash
python3 build.py
```

That inlines `brand.css` into `src/index.html` and `src/their-copy.html` and
writes the two files at the repo root, which are what actually get served.

**Edit `brand.css` and `src/`, never the root HTML files** — the build
overwrites them.

Why inline rather than `<link>`: preview sandboxes do not reliably apply an
external stylesheet, and when they don't the site renders as raw unstyled
HTML. Inlining removes that failure mode. There are no other dependencies and
no bundler.

## Deploying

GitHub Pages serves the default branch. Settings → Pages → Deploy from branch →
`main` / root. `.nojekyll` is present so Pages serves the files as-is rather
than running them through Jekyll.

Pages takes about a minute after a push.

## Before this goes live

Four things are deliberately unset. Search `index.html` for `TODO`.

1. **`DONATE_URL`** — the Donate and Give now buttons currently scroll to the
   donation panel. No money can be taken until this points at a real platform.
2. **`SIGNUP_URL`** — the "I am here" form. While it's empty the form thanks
   people and stores nothing, which is honest but useless. Point it at your
   list provider.
3. **The raised total** — currently `$0`, in two places that must agree: the
   `--pct` on `.meter-fill` and the figure in `.meter-raised`.
4. **The claims.** The species counts (9 / 12 / 3) came from the design comp
   and have not been verified against any source. The four items under
   "Mythology above. Institutional credibility underneath." describe what those
   commitments mean, with no registration number, ABN or board named. Confirm
   the counts against an ecological report and fill in the entity details from
   real documents before publishing. This is a page asking people for money;
   everything factual on it needs to survive being checked.

## Photography

There are no photographs in this repo yet. Every image slot falls back to a
painted gradient so the site holds together without them. See
[`photos/README.md`](photos/README.md) for the shot list and how to drop one in.

## Type

Fraunces for display and numerals, Archivo for everything else. Both are
self-hosted from `fonts/` — no Google Fonts request, so there's no third-party
dependency and nothing to load before first paint. Both are SIL Open Font
License 1.1; the licences are in `fonts/`.
