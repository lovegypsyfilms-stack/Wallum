# preview/

The latest draft, served at `/Wallum/preview/` while `/Wallum/` stays frozen
at whatever the client was last sent.

GitHub Pages serves one branch, so a second branch cannot have its own URL.
This folder is the workaround: work happens on `draft`, and the built page is
copied here on `main` so it has a link of its own without moving the client's.

`preview/index.html` is build output. Do not edit it — edit `brand.css` and
`src/` on `draft`, run `python3 build.py`, and copy the result here.

Delete this folder at launch.
