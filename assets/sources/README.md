# Editable image sources

[Português](README.pt-br.md) · [Images](../README.md)

These sources were introduced with Alpha-v0.2.0-Alkimim and also describe Stable-v1.0.0. Diagram geometry, labels, palette, and PNGs are unchanged; only current SVG title metadata is updated.

| Illustration | English SVG | Portuguese SVG | PNG canvas |
| --- | --- | --- | --- |
| Banner | [English](oal-banner-en.svg) | [Portuguese](oal-banner-pt-br.svg) | 1766 × 776 |
| Layers | [English](oal-layers-en.svg) | [Portuguese](oal-layers-pt-br.svg) | 1284 × 1020 |
| Case cardinalities | [English](oal-map-en.svg) | [Portuguese](oal-map-pt-br.svg) | 1427 × 1058 |

The SVGs are self-contained and keep their text, icons, panels and connectors editable. The banner embeds the original OAL mark and the restored decorative background. The original mark and both logo PNGs remain unchanged in the parent directory.

## Update the two languages

Edit the corresponding entries in [labels.json](labels.json), then regenerate with [render_images.py](render_images.py). The rendering script controls the geometry shared by both languages. It writes the six SVGs here and the six PNGs in the parent directory.

```sh
python -m pip install cairosvg==2.9.1
python assets/sources/render_images.py
```

Run the last command from the repository root. CairoSVG requires Cairo on the host. Typography uses Arial/Helvetica/Nimbus Sans with a sans-serif fallback; the delivered PNGs were rendered with Nimbus Sans. Inspect both languages after changing text or geometry, particularly the longest Portuguese labels. The included PNGs can be used directly without installing rendering dependencies.

## Meaning of the drawings

- The layer diagram has one ADMV group containing ADPM and ADVS, and one L1–L2 engine.
- The cardinality map retains one UCS case identity, one ADPM identity, one directly linked ADVS behavioral test, and one ADI identity. Its two lower identity links are not derivation engines.
- The ADI–ADIB mapping is recorded in both directions and may be many-to-many.
- The banner's dashed arrow points from ADIB toward versioned UCS as an optional additional source during derivation; it is not a runtime dependency or a canonical L1–L4 engine.

## Artwork production

The decorative banner background was restored from the supplied English banner using image editing: all foreground lettering, diagrams, icons, cards and logos were removed while retaining the pale blue/white waves, gradients and rounded corners. The resulting art is [banner-background.png](banner-background.png). No technical relationship or label is encoded in that generated background. All labels and diagram geometry are explicit in the SVG sources and rendering script. The original OAL mark is reused directly.

The production instruction was: preserve only the original pale white/ice-blue/cyan abstract background, flowing translucent bottom waves, upper corner sweeps, wide composition and transparent outside corners; remove all text, logos, cards, icons, connectors and symbols. The final six diagrams were inspected for labels, accents, arrows, grouping, legibility and EN/PT parity.
