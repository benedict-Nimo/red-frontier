// Red Frontier offline support: keeps the game, its data and its libraries on the device.
const CACHE = 'rf-5cbe968e6f';
const SHELL = ["./", "index.html", "manager.html", "manifest.webmanifest", "icons/apple-touch-icon.png", "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-512.png", "nasa/PIA10651.jpg", "nasa/PIA10906.jpg", "nasa/PIA10959.jpg", "nasa/PIA12120.jpg", "nasa/PIA12338.jpg", "nasa/PIA16938.jpg", "nasa/PIA19400.jpg", "nasa/PIA22521.jpg", "nasa/PIA24203.jpg", "nasa/PIA26302.jpg", "nasa/RASSOR.jpg", "nasa/VEGGIE.jpg", "nasa/donki-snapshot-2026-11-14.json", "nasa/phoenix-weather-daily.json", "vendor/three.min.js", "fonts/atkinson-hyperlegible-latin-400-normal.woff2", "fonts/atkinson-hyperlegible-latin-700-normal.woff2", "fonts/chakra-petch-latin-500-normal.woff2", "fonts/chakra-petch-latin-600-normal.woff2", "fonts/chakra-petch-latin-700-normal.woff2", "fonts/jetbrains-mono-latin-400-normal.woff2", "fonts/jetbrains-mono-latin-600-normal.woff2"];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.hostname === 'api.nasa.gov') return; // live NASA data always comes from the network
  // Serve from the device first, refresh in the background (works offline after the first visit).
  e.respondWith(caches.open(CACHE).then(cache => cache.match(req, {ignoreSearch: true}).then(hit => {
    const net = fetch(req).then(res => {
      if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone());
      return res;
    }).catch(() => hit || (req.mode === 'navigate' ? cache.match('index.html') : undefined));
    return hit || net;
  })));
});
