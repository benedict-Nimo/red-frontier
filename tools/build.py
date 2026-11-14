"""Builds the GitHub Pages / installable-app version of Red Frontier from the source page.

Usage: python3 tools/build.py /path/to/source/index.html
Writes index.html, manifest.webmanifest and sw.js next to this repo's root.
"""
import json, os, sys, hashlib, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(sys.argv[1], encoding='utf-8').read()

head = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Red Frontier: a free Mars survival game for kids. Help Astro survive a crash on Mars by solving real Martian problems. NASA Space Apps 2026.">
<meta name="theme-color" content="#140D0B">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Red Frontier">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<style>html,body{margin:0}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}[hidden]{display:none!important}</style>
</head>
<body>
"""
import re
FONTCSS = ''.join("@font-face{font-family:'%s';font-weight:%d;font-display:swap;src:url(fonts/%s.woff2) format('woff2')}" % (fam, w, f) for fam, w, f in [
    ('Chakra Petch', 500, 'chakra-petch-latin-500-normal'), ('Chakra Petch', 600, 'chakra-petch-latin-600-normal'), ('Chakra Petch', 700, 'chakra-petch-latin-700-normal'),
    ('Atkinson Hyperlegible', 400, 'atkinson-hyperlegible-latin-400-normal'), ('Atkinson Hyperlegible', 700, 'atkinson-hyperlegible-latin-700-normal'),
    ('JetBrains Mono', 400, 'jetbrains-mono-latin-400-normal'), ('JetBrains Mono', 600, 'jetbrains-mono-latin-600-normal')])
# self-host the 3D engine and fonts so the app loads fast and works offline
src = src.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js', 'vendor/three.min.js')
src = re.sub(r'<link rel="preconnect"[^>]*>\n?', '', src)
src = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n?', '', src)
cut = src.index('<style>')
pre, body = src[:cut], src[cut:]
head = head.replace('<style>html,body', pre + '<style>' + FONTCSS + 'html,body', 1)
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(head + body + "\n</body>\n</html>\n")

manifest = {
    "name": "Red Frontier: Junior Astronaut Mission Trainer",
    "short_name": "Red Frontier",
    "description": "Help Astro survive a crash on Mars by solving real Martian problems, with real NASA data.",
    "id": "./",
    "start_url": "./",
    "scope": "./",
    "display": "fullscreen",
    "display_override": ["fullscreen", "standalone"],
    "orientation": "any",
    "background_color": "#140D0B",
    "theme_color": "#140D0B",
    "categories": ["education", "games", "kids"],
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
json.dump(manifest, open(os.path.join(ROOT, 'manifest.webmanifest'), 'w'), indent=2)

shell = ['./', 'index.html', 'manager.html', 'manifest.webmanifest'] + \
        sorted('icons/' + os.path.basename(p) for p in glob.glob(os.path.join(ROOT, 'icons', '*.png'))) + \
        sorted('nasa/' + os.path.basename(p) for p in glob.glob(os.path.join(ROOT, 'nasa', '*'))) + \
        ['vendor/three.min.js'] + sorted('fonts/' + os.path.basename(p) for p in glob.glob(os.path.join(ROOT, 'fonts', '*.woff2')))
h = hashlib.sha256()
for f in shell[1:]:
    h.update(open(os.path.join(ROOT, f), 'rb').read())
version = 'rf-' + h.hexdigest()[:10]
sw = f"""// Red Frontier offline support: keeps the game, its data and its libraries on the device.
const CACHE = '{version}';
const SHELL = {json.dumps(shell)};
self.addEventListener('install', e => {{
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
}});
self.addEventListener('activate', e => {{
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
}});
self.addEventListener('fetch', e => {{
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.hostname === 'api.nasa.gov') return; // live NASA data always comes from the network
  // Serve from the device first, refresh in the background (works offline after the first visit).
  e.respondWith(caches.open(CACHE).then(cache => cache.match(req, {{ignoreSearch: true}}).then(hit => {{
    const net = fetch(req).then(res => {{
      if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone());
      return res;
    }}).catch(() => hit || (req.mode === 'navigate' ? cache.match('index.html') : undefined));
    return hit || net;
  }})));
}});
"""
open(os.path.join(ROOT, 'sw.js'), 'w').write(sw)
print('built', version, len(shell), 'files cached')
