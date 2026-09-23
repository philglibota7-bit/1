/* ORBIT Service Worker — macht die App installierbar und offline-fähig.
   Die Seite selbst kommt bevorzugt frisch aus dem Netz (sonst sieht man
   nach einer Änderung noch einmal die alte Fassung), alles andere
   sofort aus dem Cache mit Nachladen im Hintergrund.
   Fremde Hosts — api.anthropic.com, api.github.com — laufen immer live
   und landen nie im Cache. */
const CACHE = 'orbit-v1';
const SHELL = [
  './orbit.html',
  './orbit.webmanifest',
  './orbit-icon-192.png',
  './orbit-icon-512.png',
  './orbit-icon-maskable.png',
  './orbit-apple-touch-icon.png',
  /* Die echte Erde: Tag, Wolken, Stadtlichter — zusammen 1,4 MB. Ohne
     sie zeichnet die Seite die gerechnete Erde, also laeuft sie auch,
     wenn eine davon fehlt. */
  './orbit-erde-tag.jpg',
  './orbit-erde-wolken.jpg',
  './orbit-erde-lichter.jpg',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      /* Einzeln statt addAll: fehlt eine Datei, soll nicht die ganze
         Installation scheitern. */
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
  if (url.origin !== self.location.origin) return;   // APIs: immer live

  const istSeite = req.mode === 'navigate' || url.pathname.endsWith('.html');

  if (istSeite) {
    /* Netz zuerst, Cache als Rückfalllinie — so ist eine neue Fassung
       sofort da und die App startet trotzdem ohne Verbindung. */
    e.respondWith(
      fetch(req).then(res => {
        if (res && res.ok) {
          const kopie = res.clone();
          caches.open(CACHE).then(c => c.put(req, kopie));
        }
        return res;
      }).catch(() => caches.match(req).then(t => t || caches.match('./orbit.html')))
    );
    return;
  }

  e.respondWith(
    caches.match(req).then(cached => {
      const frisch = fetch(req).then(res => {
        if (res && res.ok) {
          const kopie = res.clone();
          caches.open(CACHE).then(c => c.put(req, kopie));
        }
        return res;
      }).catch(() => cached);
      return cached || frisch;
    })
  );
});
