import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'fs';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage(); await pg.goto('about:blank');
const b64 = readFileSync('pumpe.png').toString('base64');

const mach = async (zuschnitt, size) => await pg.evaluate(async ({ b64, zuschnitt, size }) => {
  const img = new Image();
  await new Promise(r => { img.onload = r; img.src = 'data:image/png;base64,' + b64; });
  const c = document.createElement('canvas'); c.width = c.height = size;
  const x = c.getContext('2d');
  x.fillStyle = '#fff'; x.fillRect(0, 0, size, size);
  if (zuschnitt) {
    const [sx, sy, sw, sh] = zuschnitt;
    const s = Math.min(size / sw, size / sh) * 0.96;
    x.drawImage(img, sx, sy, sw, sh, (size - sw * s) / 2, (size - sh * s) / 2, sw * s, sh * s);
  } else {
    const s = Math.min(size / img.width, size / img.height) * 0.98;
    x.drawImage(img, (size - img.width * s) / 2, (size - img.height * s) / 2,
                img.width * s, img.height * s);
  }
  // Fast-weisse Pixel auf reines Weiss, damit multiply keine Kante stehen laesst
  const d = x.getImageData(0, 0, size, size), p = d.data;
  for (let i = 0; i < p.length; i += 4)
    if (p[i] > 240 && p[i+1] > 240 && p[i+2] > 240) { p[i] = p[i+1] = p[i+2] = 255; }
  x.putImageData(d, 0, 0);
  return c.toDataURL('image/webp', 0.9);
}, { b64, zuschnitt, size });

const out = {};
out.hand = await mach([150, 10, 650, 1330], 900);   // nur Gerät in der Hand
out.set  = await mach(null, 940);                    // komplettes Set
for (const [k, v] of Object.entries(out)) console.log(k, Math.round(v.length / 1024) + ' KB');
writeFileSync('pumpe-bilder.json', JSON.stringify(out));
await b.close();
