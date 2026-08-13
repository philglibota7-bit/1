import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'fs';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage(); await pg.goto('about:blank');
const b64 = readFileSync('pumpe-neu.jpg').toString('base64');

const res = await pg.evaluate(async ({ b64 }) => {
  const img = new Image();
  await new Promise(r => { img.onload = r; img.src = 'data:image/jpeg;base64,' + b64; });
  // Nur die Pumpe: Ausschnitt in Originalkoordinaten
  const sx = 372, sy = 1112, sw = 626, sh = 1152;
  const c = document.createElement('canvas'); c.width = sw; c.height = sh;
  const x = c.getContext('2d');
  x.drawImage(img, sx, sy, sw, sh, 0, 0, sw, sh);
  const d = x.getImageData(0, 0, sw, sh), p = d.data;

  // Der Hintergrund ist blaustichig, das Gerät neutral. Blaustich -> transparent.
  let weg = 0;
  for (let i = 0; i < p.length; i += 4) {
    const r = p[i], g = p[i+1], bl = p[i+2];
    const blaustich = bl - r;
    const hell = (r + g + bl) / 3;
    if (blaustich > 14 && hell > 26) { p[i+3] = 0; weg++; }
  }
  // Verbliebene Inseln entfernen: was vom Rand aus erreichbar und dunkel ist,
  // gehört nicht zum Produkt (Bemaßungslinien, Kanten des Telefons).
  const undurch = new Uint8Array(sw * sh);
  for (let i = 0, k = 0; i < p.length; i += 4, k++) undurch[k] = p[i+3] > 0 ? 1 : 0;
  const stapel = [];
  for (let px = 0; px < sw; px++){ stapel.push(px); stapel.push((sh-1)*sw + px); }
  for (let py = 0; py < sh; py++){ stapel.push(py*sw); stapel.push(py*sw + sw-1); }
  const gesehen = new Uint8Array(sw * sh);
  while (stapel.length){
    const k = stapel.pop();
    if (gesehen[k] || !undurch[k]) continue;
    gesehen[k] = 1;
    const px = k % sw, py = (k / sw) | 0;
    if (px > 0) stapel.push(k-1);
    if (px < sw-1) stapel.push(k+1);
    if (py > 0) stapel.push(k-sw);
    if (py < sh-1) stapel.push(k+sw);
  }
  // Nur Ränder säubern, das Produkt in der Mitte bleibt unangetastet
  for (let k = 0; k < sw*sh; k++){
    if (!gesehen[k]) continue;
    const px = k % sw, py = (k / sw) | 0;
    if (px < 40 || px > sw-40 || py < 40 || py > sh-40){ p[k*4+3] = 0; weg++; }
  }
  x.putImageData(d, 0, 0);
  return { bild: c.toDataURL('image/png'), weg, gesamt: sw * sh };
}, { b64 });

console.log('entfernte Pixel:', res.weg, 'von', res.gesamt,
            '(' + Math.round(res.weg / res.gesamt * 100) + ' %)');
writeFileSync('pumpe-frei.json', JSON.stringify({ frei: res.bild }));

// Kontrollansicht auf kariertem Grund
const pg2 = await b.newPage({ viewport: { width: 500, height: 900 } });
await pg2.setContent(`<body style="margin:0;background:
  repeating-conic-gradient(#ddd 0 25%, #fff 0 50%) 0 0/24px 24px">
  <img src="${res.bild}" style="width:500px;height:900px;object-fit:contain"></body>`);
await pg2.waitForTimeout(600);
await pg2.screenshot({ path: 'freisteller-test.png' });
await b.close();
