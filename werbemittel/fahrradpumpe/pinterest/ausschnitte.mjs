// Schneidet die echten Anwendungsfotos aus der A+-Tafel des Herstellers.
// Kein Nachbau, keine Montage — nur Ausschnitt, damit auf dem Pin zu sehen
// ist, was das Geraet im Alltag tut.
import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'fs';

const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage(); await pg.goto('about:blank');
const quelle = 'data:image/jpeg;base64,' + readFileSync('pumpe-neu.jpg').toString('base64');

// Bildkoordinaten in der Tafel (1969 x 2560).
const felder = {
  rahmen:  [1300, 564, 542, 549],   // Pumpe am Fahrradrahmen
  tasche:  [1300, 1172, 542, 549],  // Pumpe wandert in die Satteltasche
  rucksack:[1300, 1776, 542, 553],  // Pumpe wandert in den Rucksack
  groesse: [102, 954, 896, 1312],   // Groeszenvergleich neben dem Handy
};

const raus = await pg.evaluate(async ({ src, felder }) => {
  const img = new Image();
  await new Promise(r => { img.onload = r; img.src = src; });
  const erg = { masze: [img.width, img.height] };
  for (const [name, [x, y, w, h]] of Object.entries(felder)) {
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    c.getContext('2d').drawImage(img, x, y, w, h, 0, 0, w, h);
    erg[name] = c.toDataURL('image/webp', 0.9);
  }
  return erg;
}, { src: quelle, felder });

console.log('Tafel:', raus.masze.join('x'));
const { masze, ...bilder } = raus;
writeFileSync('pumpe-nutzung.json', JSON.stringify(bilder));
for (const [name, uri] of Object.entries(bilder)) {
  writeFileSync(`nutz-${name}.webp`, Buffer.from(uri.split(',')[1], 'base64'));
  console.log(name, Math.round(uri.length / 1024), 'KB');
}
await b.close();
