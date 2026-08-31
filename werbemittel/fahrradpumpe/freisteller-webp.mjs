import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'fs';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage(); await pg.goto('about:blank');
const frei = JSON.parse(readFileSync('pumpe-frei.json', 'utf8')).frei;
const webp = await pg.evaluate(async ({ src }) => {
  const img = new Image();
  await new Promise(r => { img.onload = r; img.src = src; });
  // Quadratische Leinwand mit Alpha, Produkt zentriert
  const size = 900;
  const c = document.createElement('canvas'); c.width = c.height = size;
  const x = c.getContext('2d');
  const s = Math.min(size / img.width, size / img.height) * 0.94;
  const w = img.width * s, h = img.height * s;
  x.drawImage(img, (size - w) / 2, (size - h) / 2, w, h);
  return c.toDataURL('image/webp', 0.92);
}, { src: frei });
writeFileSync('pumpe-bilder.json', JSON.stringify({ hand: webp, set: webp }));
console.log('Freisteller als WebP:', Math.round(webp.length / 1024), 'KB');
await b.close();
