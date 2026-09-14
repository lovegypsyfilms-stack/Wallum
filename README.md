# Wallum — Be Here

Campaign site for the acquisition and permanent protection of Wallum, a coastal
wetland on Bundjalung country in northern New South Wales.

## The two versions

Both live in the one built page, toggled by the switcher pinned to the bottom
of the screen:

- **Version B** — the reduced, brand-aligned site. ~616 words.
- **Version A** — CLAI's existing website copy, verbatim, inside the same
  identity. ~6,509 words.

The switcher is pitch scaffolding. Delete the `<nav class="vswitch">` block
and the `ver-a` wrapper from `build.py` before launch.

## Editing it

Edit these, never the built file:

    brand.css              the identity, shared by both versions
    src/index.html         Version B body
    src/their-copy.html    Version A body
    photos/  fonts/        assets

Then:

```bash
python3 build.py
```

That writes `index.html` at the repo root — **build output, do not edit it.**

The build inlines `brand.css` and embeds every font and photograph as a
`data:` URI, producing one self-contained file of about 1 MB.

That seems heavy-handed, and it is deliberate. Preview sandboxes do not
reliably serve a page's sub-resources: an external stylesheet can be ignored
(the site renders as raw unstyled HTML), images can fail to load, and a link
to a second HTML file can go nowhere. All three happened here. A single file
with nothing external has none of those failure modes, and it still works
opened straight off disk with no server.

The cost is that the page is ~1 MB instead of ~45 KB. Once the real
photography lands, revisit this: served over HTTPS from Pages with proper
caching, separate files are the better trade.

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
