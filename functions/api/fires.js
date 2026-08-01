// Cloudflare Pages version of the FIRMS proxy (Vercel version: /api/fires.js,
// local dev: server.py). The cf block caches the upstream fetch at Cloudflare's
// edge for 30 minutes, so NASA sees one fetch per half hour, not one per visitor.
const FIRMS_URL = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/'
  + 'modis-c6.1/csv/MODIS_C6_1_Global_7d.csv';

export async function onRequest() {
  const upstream = await fetch(FIRMS_URL, {
    headers: { 'User-Agent': 'worldburn' },
    cf: { cacheTtl: 1800, cacheEverything: true },
  });
  if (!upstream.ok) return new Response('FIRMS fetch failed: ' + upstream.status, { status: 502 });
  return new Response(upstream.body, {
    headers: {
      'Content-Type': 'text/csv',
      'Cache-Control': 'public, s-maxage=1800, stale-while-revalidate=3600',
    },
  });
}
