// Vercel edge version of the proxy in server.py. Streams the FIRMS CSV through
// (edge runtime has no response size cap; the file is ~8.5 MB, gzips to ~2 MB)
// and lets the CDN cache it, so NASA sees one fetch per half hour, not one per
// visitor.
export const config = { runtime: 'edge' };

const FIRMS_URL = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/'
  + 'modis-c6.1/csv/MODIS_C6_1_Global_7d.csv';

export default async function handler() {
  const upstream = await fetch(FIRMS_URL, { headers: { 'User-Agent': 'worldburn' } });
  if (!upstream.ok) return new Response('FIRMS fetch failed: ' + upstream.status, { status: 502 });
  return new Response(upstream.body, {
    headers: {
      'Content-Type': 'text/csv',
      'Cache-Control': 'public, s-maxage=1800, stale-while-revalidate=3600',
    },
  });
}
