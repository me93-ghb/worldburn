# worldburn design system

The chrome is the annotation layer of a satellite image.
Everything on screen should read like the metadata strip on an acquisition frame, quiet and instrument-true, so the globe stays the only loud thing on the page.

## Tokens

| token | value | use |
|---|---|---|
| `--space` | `#04060a` | page background, space |
| `--ink` | `#0d1420` | control fills, panels |
| `--hairline` | `#24303c` | borders, rules, neatline corners |
| `--label` | `#6b7c88` | secondary text, tick labels |
| `--text` | `#c8d2d9` | primary UI text |
| `--fire` | `#e08a3c` | accent: links, units, focus rings |
| `--paper` | `#e8ddcf` | title, the big number |

## Type

One family, on purpose: `ui-monospace, "SF Mono", Menlo, monospace`.
Satellite annotation strips are single-typeface; hierarchy comes from scale and weight, not a second font.

- Display: 34px / weight 300, the total-fire-power figure only. One big moment per page.
- Title: 15px / 500, uppercase, `.32em` tracking.
- Label: 11px, uppercase, `.10em` to `.14em` tracking.
- Body (about panel): 12.5px / 1.7, sentence case.

## Rules

- Separators are `·`, never em dashes, in all UI copy.
- Lowercase-feel labels, uppercase rendered via CSS, sentence case only in about-panel prose.
- Every inferred data label says so ("presumed", "likely"); measured things get stated plainly.
- Corners: 3px radius on controls, none on panels. No pills.
- The signature elements are the four neatline corner brackets and the FRP colorbar. Don't add more decoration; if something new competes with them, cut it.
- The colorbar is log-scaled 10 MW to 1 GW+ and must keep matching the dot-size mapping in `index.html` (`3.5 + log10(1+frp) * 4`).

## Directions considered and dropped

- Unified top instrument bar (title, controls, stats in one strip): cleaner app, but loses the looking-through-an-instrument feel.
- Documentary lower-third caption with the GW figure as a broadcast overlay: drifts cinematic, fights the globe.

## Quality floor

Focus-visible rings on all controls, `prefers-reduced-motion` stops the auto-spin, mobile collapses stats to the headline figure bottom-right.
