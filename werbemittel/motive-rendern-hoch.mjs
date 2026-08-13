import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage({ viewport: { width: 1200, height: 1200 } });
const errs = []; pg.on('pageerror', e => errs.push(e.message));
await pg.goto('file:///tmp/claude-0/-home-user-1/d9dd5cf6-a597-547e-95fb-a98c3cc3ca25/scratchpad/ads4-hoch.html');
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(800);

// Produktkante im Bild messen und den Aufsetzschatten exakt daruntersetzen
const mass = await pg.evaluate(() => {
  const out = [];
  for (const ad of document.querySelectorAll('.ad')) {
    const img = ad.querySelector('.stage img');
    const stage = ad.querySelector('.stage');
    const schatten = ad.querySelector('.contact');

    // Nicht-weisse Pixel einsammeln
    const n = 300;
    const c = document.createElement('canvas'); c.width = c.height = n;
    const x = c.getContext('2d');
    x.fillStyle = '#fff'; x.fillRect(0, 0, n, n);
    x.drawImage(img, 0, 0, n, n);
    const d = x.getImageData(0, 0, n, n).data;
    let minX = n, maxX = 0, maxY = 0;
    for (let py = 0; py < n; py++) for (let px = 0; px < n; px++) {
      const i = (py * n + px) * 4;
      if (d[i] < 238 || d[i+1] < 238 || d[i+2] < 238) {
        if (px < minX) minX = px; if (px > maxX) maxX = px; if (py > maxY) maxY = py;
      }
    }
    // object-fit: contain -> gerendertes Rechteck im Stage-Kasten
    const sw = stage.offsetWidth, sh = stage.offsetHeight;
    const s = Math.min(sw / img.naturalWidth, sh / img.naturalHeight);
    const rw = img.naturalWidth * s, rh = img.naturalHeight * s;
    const ox = (sw - rw) / 2, oy = (sh - rh) / 2;

    const basisY = oy + (maxY + 1) / n * rh;              // Unterkante des Produkts
    const mitteX = ox + ((minX + maxX) / 2) / n * rw;     // horizontale Mitte
    const breite = (maxX - minX + 1) / n * rw;

    const w = Math.max(150, breite * 1.12), h = Math.max(38, breite * 0.16);
    schatten.style.left = (stage.offsetLeft + mitteX - w / 2) + 'px';
    schatten.style.top  = (stage.offsetTop + basisY - h * 0.52) + 'px';
    schatten.style.width = w + 'px';
    schatten.style.height = h + 'px';
    schatten.style.right = 'auto'; schatten.style.bottom = 'auto';
    out.push({ id: ad.id, basisY: Math.round(basisY), breite: Math.round(breite) });
  }
  return out;
});
console.log('Gemessen:', JSON.stringify(mass));
await pg.waitForTimeout(300);

const namen = { ad1: 'vakuumierer', ad2: 'massagepistole', ad3: 'sunset-lampe' };
for (const [id, name] of Object.entries(namen)) {
  await pg.locator('#' + id).screenshot({ path: `hoch-${name}.png` });
}
console.log(errs.length ? 'FEHLER: ' + errs.join('; ') : 'ok');
await b.close();
