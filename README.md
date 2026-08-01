# watch the world burn

![one full rotation, live data](demo.gif)

A dark 3D globe of every fire NASA's satellites can currently see.
The last 24 hours burn as live embers, the rest of the week lingers as char.
One dropdown filters what kind of burning you're looking at, the other switches rendering styles (embers is the best one).

Not a science tool.
NASA's own [FIRMS fire map](https://firms.modaps.eosdis.nasa.gov/map/) does that properly.
This exists because I had no idea how much of the planet is burning on an ordinary day, or that most of it is on purpose.

Pair-built with Claude, credited as co-author in the commits. The idea and the picking-at-the-data were mine. Most of the code wasn't.

## Running it

```bash
python3 server.py
```

Then open <http://localhost:8123>.
Python 3 and a browser, that's the whole stack.

If the FIRMS feed is unreachable the page falls back to sample data and says so under the title.

## Deploying

The repo carries both proxy variants, same 30 minute CDN cache either way:

- Cloudflare Pages: `npx wrangler pages deploy . --project-name worldburn` (uses `functions/api/fires.js`).
- Vercel: `vercel` (uses `api/fires.js`).

After the first deploy, update the `og:image` URL in `index.html` to the real domain.
`og.png` is the link preview image.

## Data

- Fires: [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/), the keyless rolling `MODIS_C6_1_Global_7d.csv` (about 110k detections). `server.py` proxies and caches it for 30 minutes so one NASA fetch serves every visitor.
- Coastlines and borders: [Natural Earth](https://www.naturalearthdata.com/) via [world-atlas](https://github.com/topojson/world-atlas), pulled from CDN.
- Volcano markers are a hardcoded list of usually-active volcanoes, not live eruption status.

## How the fire typing works

Satellites measure where a fire is, how hot it burns and for how long.
They can't see who lit it.

An earlier version here labeled the split "likely wildfire" vs "likely agricultural".
The data disagreed: 46% of the African savanna belt classified as "wildfire".
So the split is now behavior, which is actually measurable:

- Persistent: a 0.1° cell hot on 3+ consecutive days, or peaking over 150 MW.
- Brief: everything else on land.
- Over water: presumed gas flare. Same assumption NASA's own archive type field makes. Could just as well be a rig accident or a ship on fire.

Consecutive days matter: the first behavior version counted any 3 detection days in the week, and in dense burning regions a cell collects several unrelated one-day burns, so 60% of the belt's "persistent" fires weren't persistent at all.
With the consecutive rule the belt sits around 19% persistent while the boreal north stays around 81%, which matches how those regions actually burn: above 50°N persistent nearly always means a real wildfire, in the belt it means a big front burn that held its ground for days.
A brand-new wildfire also reads "brief" on day one until it persists.

## Field notes

Things that bit me, written down so they only bite once:

- Sprites on a globe want `depthTest: false` plus a horizon fade in the vertex shader. Depth-tested quads get sliced by the sphere into arc artifacts at glancing angles. Start the fade well before the geometric horizon and shrink the quad too, or big soft sprites overhang the limb and look like fire shining through the planet.
- Force sprite alpha to zero before the quad edge or the square shows up when you zoom in.
- Don't hand-roll geo polygon rasterization. Fiji crosses the antimeridian and drags a fill-inverting sliver across the whole equirectangular canvas. Russia too. Use d3-geo's `geoPath`, and fill with `'evenodd'`, because at 110m resolution the Mediterranean, Black Sea, Caspian and Persian Gulf are hole rings whose winding the nonzero rule ignores.
- You can't multiply an orange flame ramp into blue. Flare tinting blends toward the tint color by luminance instead.
- Stacked additive radial gradients band into visible rings at 8 bits. Dither the alpha.
