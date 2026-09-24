/* PULSE Service Worker — macht die App installierbar & offline-fähig.
   Strategie: App-Shell vorab cachen; same-origin-Anfragen stale-while-revalidate
   (sofort aus dem Cache, im Hintergrund aktualisieren); API-Calls zu fremden
   Hosts laufen normal übers Netz und werden nicht gecacht. */
const CACHE = 'pulse-v3';
const SHELL = [
  './info-hub.html',
  './pulse.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      /* Einzeln statt addAll: fehlt eine Datei oder liefert sie kurzzeitig
         einen Fehler, scheiterte sonst die ganze Installation still — die
         App galt als installierbar, startete offline aber nicht. */
      .then(c => Promise.all(SHELL.map(u => c.add(u).catch(() => {}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // APIs: immer live

  /* Die Seite selbst netz-zuerst. Mit stale-while-revalidate sah man nach
     jeder Aenderung beim Start noch die vorherige Fassung — dauerhaft eine
     Veroeffentlichung hinterher. */
  if (req.mode === 'navigate' || url.pathname.endsWith('.html')) {
    e.respondWith(
      fetch(req).then(res => {
        if (res && res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req, copy));
        }
        return res;
      }).catch(() => caches.match(req).then(t => t || caches.match('./info-hub.html')))
    );
    return;
  }

  e.respondWith(
    caches.match(req).then(cached => {
      const fresh = fetch(req).then(res => {
        if (res && res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req, copy));
        }
        return res;
      }).catch(() => cached);
      return cached || fresh;
    })
  );
});
