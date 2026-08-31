import { chromium } from 'playwright';
const errs = [];
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage({ viewport: { width: 1280, height: 1000 }, deviceScaleFactor: 2 });
pg.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
pg.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });
const step = async (n, f) => { try { await f(); console.log('✓', n); }
  catch (e) { console.log('✗', n, '—', e.message.split('\n')[0]); errs.push(n); } };

await pg.goto('file:///home/user/1/squelly-v2.html');
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(1400);

await step('Vier Karten mit Bild, Preis und Wirkzeichen', async () => {
  const d = await pg.evaluate(() => [...document.querySelectorAll('.karte')].map(k => ({
    name: k.querySelector('.name')?.textContent,
    preis: k.querySelector('.preis')?.textContent,
    fx: !!k.querySelector('.fx svg'),
    bild: k.querySelector('.bild img')?.naturalWidth || 0,
    beispiel: !!k.querySelector('.beispiel')
  })));
  if (d.length !== 4) throw new Error(d.length + ' Karten');
  d.forEach(x => {
    if (!/€/.test(x.preis || '')) throw new Error('kein Preis: ' + x.name);
    if (!x.fx) throw new Error('kein Wirkzeichen: ' + x.name);
    if (!x.bild) throw new Error('Bild leer: ' + x.name);
    if (!x.beispiel) throw new Error('Beispiel-Kennzeichnung fehlt: ' + x.name);
  });
  console.log('   ', d.map(x => x.preis).join(' | '));
});
await step('Jedes Produkt hat seine eigene Akzentfarbe', async () => {
  const f = await pg.evaluate(() => [...document.querySelectorAll('.karte')]
    .map(k => getComputedStyle(k).getPropertyValue('--akzent').trim()));
  if (new Set(f).size !== 4) throw new Error(f.join(', '));
});
await step('Tiefpreis-Marke nur, wo der Wert auch das Tief ist', async () => {
  const m = await pg.evaluate(() => [...document.querySelectorAll('.karte')].map(k => ({
    k: k.dataset.kuerzel, marke: !!k.querySelector('.marker') })));
  const soll = { vakuumierer: true, massagepistole: false, lampe: true, pumpe: true };
  m.forEach(x => { if (x.marke !== soll[x.k]) throw new Error(x.k + ' = ' + x.marke); });
});
await step('Kategorien filtern', async () => {
  await pg.click('#fach button[data-kat="Fahrrad"]');
  await pg.waitForTimeout(200);
  const n = await pg.evaluate(() => document.querySelectorAll('.karte:not(.weg)').length);
  if (n !== 1) throw new Error(n + ' sichtbar');
  const t = await pg.textContent('#treffer');
  if (!/1 Produkt/.test(t)) throw new Error(t);
  await pg.click('#fach button[data-kat="Alle"]');
  await pg.waitForTimeout(200);
});
await step('Suche greift auf Merkmale, nicht nur auf den Namen', async () => {
  await pg.fill('#suchfeld', 'usb-c');
  await pg.waitForTimeout(200);
  const n = await pg.evaluate(() => document.querySelectorAll('.karte:not(.weg)').length);
  if (n !== 2) throw new Error(n + ' Treffer für usb-c');
  await pg.fill('#suchfeld', 'zzz');
  await pg.waitForTimeout(200);
  const leer = await pg.evaluate(() => document.getElementById('leer').classList.contains('an'));
  if (!leer) throw new Error('Leermeldung fehlt');
  await pg.fill('#suchfeld', '');
  await pg.waitForTimeout(200);
});
await step('Amazon-Link trägt Partner-Kürzel und Zuordnung', async () => {
  const l = await pg.evaluate(() => [...document.querySelectorAll('.cta')].map(a => a.href));
  if (l.length !== 4) throw new Error(l.length + ' Links');
  if (!l.every(u => /tag=squelly-21/.test(u))) throw new Error('Tag fehlt');
  const s = decodeURIComponent(l[0]).match(/ascsubtag=([^&]+)/)[1];
  if (s !== 'sq-direkt-ohne-seite-vakuumierer') throw new Error(s);
  const rel = await pg.evaluate(() => document.querySelector('.cta').rel);
  if (!/sponsored/.test(rel) || !/nofollow/.test(rel)) throw new Error(rel);
});
await step('Herkunft aus der Anzeige landet in der SubID', async () => {
  await pg.goto('file:///home/user/1/squelly-v2.html?utm_source=pinterest&utm_medium=pin&utm_campaign=Herbst%20Start&utm_content=pumpe-pin-8-szene');
  await pg.waitForTimeout(900);
  const s = decodeURIComponent(await pg.evaluate(() => document.querySelector('.cta').href));
  if (!/sq-pinterest-herbststart-pumpepin8szene-vakuumierer/.test(s)) throw new Error(s.slice(0, 140));
});
await step('Wunschpreis setzen, merken, entfernen', async () => {
  await pg.evaluate(() => alarmUmschalten('lampe'));
  await pg.waitForTimeout(150);
  await pg.fill('#ziel-lampe', '19.50');
  await pg.evaluate(() => alarmSpeichern('lampe'));
  await pg.waitForTimeout(300);
  const t = await pg.evaluate(() => document.querySelector('[data-kuerzel="lampe"] .wecker').textContent);
  if (!/19,50/.test(t)) throw new Error(t);
  await pg.reload(); await pg.waitForTimeout(900);
  const t2 = await pg.evaluate(() => document.querySelector('[data-kuerzel="lampe"] .wecker').textContent);
  if (!/19,50/.test(t2)) throw new Error('nach Neuladen: ' + t2);
  await pg.evaluate(() => alarmLoeschen('lampe'));
  await pg.waitForTimeout(250);
});
await step('Ziel über dem Preis wird abgelehnt', async () => {
  await pg.evaluate(() => alarmUmschalten('pumpe'));
  await pg.fill('#ziel-pumpe', '99');
  await pg.evaluate(() => alarmSpeichern('pumpe'));
  await pg.waitForTimeout(250);
  const m = await pg.textContent('#meldungen');
  if (!/zu hoch/.test(m)) throw new Error(m);
});
await step('Rechtstexte öffnen sich', async () => {
  await pg.evaluate(() => blatt('datenschutz'));
  await pg.waitForTimeout(250);
  const t = await pg.textContent('#dlgText');
  if (!/sessionStorage/.test(t) || !/localStorage/.test(t)) throw new Error('unvollständig');
  await pg.keyboard.press('Escape');
});
await pg.evaluate(() => window.scrollTo(0, 400));
await pg.waitForTimeout(1400);
await pg.screenshot({ path: 'v2-desktop.png', fullPage: false });
await pg.screenshot({ path: 'v2-lang.png', fullPage: true });

const m = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true });
m.on('pageerror', e => errs.push('MOBIL: ' + e.message));
await m.goto('file:///home/user/1/squelly-v2.html');
await m.evaluate(() => document.fonts.ready);
await m.waitForTimeout(1200);
const ovf = await m.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
console.log(ovf > 2 ? '✗ mobiler Überlauf ' + ovf : '✓ kein mobiler Überlauf');
if (ovf > 2) errs.push('Überlauf');
await m.screenshot({ path: 'v2-mobil.png', fullPage: true });

await b.close();
console.log('\n' + (errs.length ? 'FEHLER: ' + errs.join(', ') : 'Alles bestanden, keine JS-Fehler.'));
