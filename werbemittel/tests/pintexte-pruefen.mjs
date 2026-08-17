import { chromium } from 'playwright';
import { existsSync } from 'fs';
const errs = [];
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage({ viewport: { width: 980, height: 1200 }, deviceScaleFactor: 2 });
pg.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
pg.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });
await pg.goto('file:///home/user/1/werbemittel/fahrradpumpe/pinterest/pin-texte.html');
await pg.waitForTimeout(600);

const step = async (n, f) => { try { await f(); console.log('✓', n); }
  catch (e) { console.log('✗', n, '—', e.message.split('\n')[0]); errs.push(n); } };

await step('Neun Pins mit allen vier Feldern', async () => {
  const n = await pg.evaluate(() => document.querySelectorAll('#pins .pin').length);
  if (n !== 9) throw new Error(n + ' Pins');
  const f = await pg.evaluate(() =>
    [...document.querySelectorAll('#pins .pin')].map(p => p.querySelectorAll('.feld').length));
  if (f.some(x => x !== 4)) throw new Error('Felder je Pin: ' + f.join(','));
});
await step('Titel, Beschreibung und Alt bleiben unter Pinterests Grenzen', async () => {
  const lang = await pg.evaluate(() => {
    const raus = [];
    document.querySelectorAll('#pins .zaehler').forEach(z => {
      const [ist, max] = z.textContent.split('/').map(s => parseInt(s.trim(), 10));
      if (ist > max) raus.push(z.textContent);
    });
    return raus;
  });
  if (lang.length) throw new Error(lang.join(' | '));
  const t = await pg.evaluate(() => document.getElementById('zahl').textContent);
  if (!/alle innerhalb/.test(t)) throw new Error(t);
});
await step('Jede Beschreibung ist als Anzeige gekennzeichnet', async () => {
  const ohne = await pg.evaluate(() =>
    [...document.querySelectorAll('#pins .pin')]
      .map(p => p.querySelectorAll('.feld')[1].querySelector('.text').textContent)
      .filter(t => t.indexOf('Anzeige') === -1).length);
  if (ohne) throw new Error(ohne + ' ohne Kennzeichnung');
});
await step('Jeder Pin trägt seine eigene Zieladresse', async () => {
  const u = await pg.evaluate(() =>
    [...document.querySelectorAll('#pins .url')].map(x => x.textContent));
  if (u.length !== 9) throw new Error(u.length + ' Adressen');
  if (new Set(u).size !== 9) throw new Error('Adressen doppelt');
  if (!u.every(x => /utm_source=pinterest&utm_medium=pin/.test(x))) throw new Error('Kanal fehlt');
  if (!/utm_content=pumpe-pin-1-nachtfahrt/.test(u[0])) throw new Error(u[0]);
});
await step('Kampagne schlägt auf alle Adressen durch', async () => {
  await pg.fill('#kampagne', 'Winter');
  await pg.waitForTimeout(200);
  const u = await pg.evaluate(() =>
    [...document.querySelectorAll('#pins .url')].map(x => x.textContent));
  if (!u.every(x => /utm_campaign=Winter/.test(x))) throw new Error(u[0]);
});
await step('Die genannten Bilddateien liegen daneben und laden', async () => {
  const ordner = '/home/user/1/werbemittel/fahrradpumpe/pinterest/';
  const d = await pg.evaluate(() =>
    [...document.querySelectorAll('#pins .datei')].map(x => x.textContent));
  const fehlt = d.filter(n => !existsSync(ordner + n));
  if (fehlt.length) throw new Error('fehlt: ' + fehlt.join(', '));
  // Die Vorschauen laden verzögert; erst ans Seitenende rollen, dann zählen.
  await pg.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await pg.waitForTimeout(900);
  const leer = await pg.evaluate(() =>
    [...document.querySelectorAll('#pins img')].filter(i => !i.complete || !i.naturalWidth)
      .map(i => i.getAttribute('src')));
  if (leer.length) throw new Error('ohne Inhalt: ' + leer.join(', '));
});

await pg.screenshot({ path: 'pintexte.png', fullPage: true });
await b.close();
console.log('\n' + (errs.length ? 'FEHLER: ' + errs.join(', ') : 'Alles bestanden.'));
process.exit(errs.length ? 1 : 0);
