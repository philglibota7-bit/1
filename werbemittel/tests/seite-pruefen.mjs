import { chromium } from 'playwright';
const errs = [];
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const step = async (n, f) => { try { await f(); console.log('✓', n); }
  catch (e) { console.log('✗', n, '—', e.message.split('\n')[0]); errs.push(n); } };

const pg = await b.newPage({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 2 });
pg.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
pg.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });

// --- Direkter Aufruf ohne Kampagne ---
await pg.goto('file:///home/user/1/squelly.html');
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(700);
/* Die Zahl der Produkte wächst; die Prüfungen zählen deshalb selbst nach,
   statt eine feste Zahl zu erwarten. */
const kuerzel = await pg.evaluate(() => PRODUKTE.map(p => p.kuerzel));
await step('Jedes Produkt hat eine Karte', async () => {
  const n = await pg.evaluate(() => document.querySelectorAll('.card').length);
  if (n !== kuerzel.length) throw new Error(n + ' Karten zu ' + kuerzel.length + ' Produkten');
  if (n < 4) throw new Error('nur ' + n + ' Karten');
});
await step('Ohne Kampagne: SubID sagt "direkt"', async () => {
  const l = await pg.evaluate(() => [...document.querySelectorAll('.cta')].map(a => a.href));
  const sub = decodeURIComponent(l[0]).match(/ascsubtag=([^&]+)/)[1];
  if (sub !== 'sq-direkt-ohne-seite-' + kuerzel[0]) throw new Error(sub);
  if (l.length !== kuerzel.length) throw new Error(l.length + ' Links');
});
await step('Wirkzeichen auf den Karten', async () => {
  const ohne = await pg.evaluate(() => [...document.querySelectorAll('.card')]
    .filter(c => !c.querySelector('.photo .fx') && !c.querySelector('.photo .glow'))
    .map(c => c.querySelector('.cname').textContent));
  if (ohne.length) throw new Error('ohne Zeichen: ' + ohne.join(', '));
});
await pg.screenshot({ path: 'sq3-desktop.png' });

// --- Aufruf über eine Anzeige ---
await pg.goto('file:///home/user/1/squelly.html?utm_source=instagram&utm_medium=paid&utm_campaign=Herbst%20Start&utm_content=lampe-hoch');
await pg.waitForTimeout(700);
await step('Mit Kampagne: Herkunft landet in der SubID', async () => {
  const l = await pg.evaluate(() => [...document.querySelectorAll('.cta')].map(a => decodeURIComponent(a.href)));
  const subs = l.map(u => u.match(/ascsubtag=([^&]+)/)[1]);
  const soll = kuerzel.map(k => 'sq-instagram-herbststart-lampehoch-' + k);
  if (JSON.stringify(subs) !== JSON.stringify(soll)) throw new Error(JSON.stringify(subs));
});
await step('Herkunft übersteht Navigation ohne Parameter', async () => {
  await pg.goto('file:///home/user/1/squelly.html');
  await pg.waitForTimeout(600);
  const u = decodeURIComponent(await pg.evaluate(() => document.querySelector('.cta').href));
  if (!/sq-instagram-herbststart/.test(u)) throw new Error(u.slice(0, 120));
});
await step('Partner-Tag weiterhin an jedem Link', async () => {
  const l = await pg.evaluate(() => [...document.querySelectorAll('.cta')].map(a => a.href));
  if (!l.every(u => /tag=squelly-21/.test(u))) throw new Error('Tag fehlt');
});
await step('Datenschutztext nennt die Herkunftsspeicherung', async () => {
  await pg.evaluate(() => sheet('datenschutz'));
  await pg.waitForTimeout(300);
  const t = await pg.locator('#shBody').innerText();
  if (!/sessionStorage/i.test(t) || !/utm_source/i.test(t)) throw new Error('Text unvollständig');
  await pg.keyboard.press('Escape');
});

const m = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true });
m.on('pageerror', e => errs.push('MOBIL: ' + e.message));
await m.goto('file:///home/user/1/squelly.html');
await m.evaluate(() => document.fonts.ready);
await m.waitForTimeout(800);
const ovf = await m.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
console.log(ovf > 2 ? '✗ mobiler Überlauf ' + ovf : '✓ kein mobiler Überlauf');
if (ovf > 2) errs.push('Überlauf');
await m.screenshot({ path: 'sq3-mobil.png', fullPage: true });

await b.close();
console.log('\n' + (errs.length ? 'FEHLER: ' + errs.join(', ') : 'Alles bestanden, keine JS-Fehler.'));
process.exit(errs.length ? 1 : 0);
