# Photography

Nothing in this folder yet. **The site works without it** — every image slot
falls back to a painted gradient — but the photographs are what will carry it.

## How to add one

1. Drop the file in this folder.
2. Open `index.html`, find the **PHOTOGRAPHY SWITCHBOARD** at the top of the
   `<style>` block, and uncomment the matching line.

That's the whole job. The gradient steps aside on its own.

```css
/* --photo-hero:      url("photos/hero-dawn.jpg"); */   ← before
   --photo-hero:      url("photos/hero-dawn.jpg");      ← after
```

## Shot list

| Variable | Filename | Shot | Ratio / size |
|---|---|---|---|
| `--photo-hero` | `hero-dawn.jpg` | Dawn over the wetland. Mist on water, low sun, depth. The one image the whole site rests on. | Wide, ~2400×1400 |
| `--photo-frog` | `frog.jpg` | Wallum sedge frog at the waterline, tannin-dark water. | ~1200×1600 portrait |
| `--photo-cockatoo` | `cockatoo.jpg` | Black-cockatoo in banksia or she-oak. | ~1200×1600 portrait |
| `--photo-heath` | `heath.jpg` | Flowering heath, backlit, shallow depth of field. | ~1200×1600 portrait |
| `--photo-gather` | `gathering.jpg` | The "come together" image — a crowd, a map, a connected world. Dark enough to hold white text. | Wide, ~2000×1200 |
| `--photo-land` | `land-aerial.jpg` | Aerial of the property at dusk. Should read as *scale* — this is what $60m buys. | ~1600×1200 |
| `--photo-flower` | `swamp-orchid.jpg` | Swamp orchid or similar, close, pale against dark. | Wide, ~2000×900 |
| `--photo-ground` | `bark.jpg` | Bark or canopy texture. Sits behind dark text panels — keep it quiet. | Wide, ~2000×1000 |
| `--photo-canopy` | `canopy.jpg` | Canopy at golden hour. Light section, dark text over it. | Wide, ~2400×1000 |
| `--photo-closing` | `heath-dusk.jpg` | Heath at last light. The final image anyone sees. | Wide, ~2400×1200 |
| `--photo-face-1/2/3` | `face-1.jpg` … | Three portraits, "before us / us / after us". Crop to 3:4. | ~600×800 each |

## Before you commit them

- **Compress.** Target under 400 KB each; the hero can go to ~600 KB. Every
  one of these loads on first paint, and a lot of people will open this on
  phone data. Export at 2× the display size, not camera-native.
- **Check the dark overlays.** The stat cards and the hero lay text over the
  image. Busy or bright-at-the-bottom frames will fight the type.
- **Know the provenance.** Species photographs in particular: either shoot
  them, licence them, or credit them. A donation page is exactly the wrong
  place to be loose about image rights.
