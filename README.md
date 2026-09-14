# Wallum — Be Here

Campaign site for the acquisition and permanent protection of Wallum, a coastal
wetland on Bundjalung country in northern New South Wales.

## Running it

Open `index.html` in a browser. That's it — there's no build step, no bundler,
no dependencies. `index.html` is the whole app: CSS in one `<style>`, a short
`<script>` at the bottom.

The only other files that ship are the fonts and (once they exist) the photos.

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
