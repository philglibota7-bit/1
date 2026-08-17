import { chromium } from 'playwright';
const errs = [];
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage({ viewport: { width: 900, height: 1000 }, deviceScaleFactor: 2 });
pg.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
pg.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });
await pg.goto('file:///home/user/1/werbemittel/kampagnen-links.html');
await pg.waitForTimeout(500);

const step = async (n, f) => { try { await f(); console.log('✓', n); }
  catch (e) { console.log('✗', n, '—', e.message.split('\n')[0]); errs.push(n); } };

// Zeilen ohne die Zwischenüberschriften je Produkt
const zeilen = () => pg.evaluate(() =>
  [...document.querySelectorAll('#zeilen tr')].filter(t => !t.classList.contains('gruppe')).length);

await step('Feed-Kanal zeigt nur Feed-Motive', async () => {
  const n = await zeilen();
  if (n !== 11) throw new Error(n + ' Zeilen (erwartet 3x2 + 5 der Pumpe)');
  const arten = await pg.evaluate(() =>
    [...document.querySelectorAll('#zeilen .url')].map(u => /utm_content=([^&]+)/.exec(u.textContent)[1]));
  if (arten.some(a => a.indexOf('-pin-') !== -1)) throw new Error('Pin im Feed-Kanal: ' + arten.join(','));
});
await step('Adresse trägt alle vier UTM-Felder', async () => {
  const u = await pg.evaluate(() => document.querySelector('#zeilen .url').textContent);
  for (const f of ['utm_source=instagram', 'utm_medium=paid', 'utm_campaign=Herbst%20Start',
                   'utm_content=vakuumierer-quad'])
    if (u.indexOf(f) === -1) throw new Error('fehlt: ' + f + ' in ' + u);
});
await step('SubID-Vorschau stimmt mit der Seite überein', async () => {
  const s = await pg.evaluate(() => document.querySelector('#zeilen .sub').textContent);
  if (!/sq-instagram-herbststart-vakuumiererquad-vakuumierer/.test(s)) throw new Error(s);
});
await step('Pinterest zeigt alle Pins und keine Feed-Motive', async () => {
  await pg.selectOption('#kanal', 'pinterest|pin|pin');
  await pg.waitForTimeout(250);
  const n = await zeilen();
  if (n !== 18) throw new Error(n + ' Zeilen (erwartet 3x3 + 9 der Pumpe)');
  const u = await pg.evaluate(() => document.querySelector('#zeilen .url').textContent);
  if (!/utm_source=pinterest/.test(u) || !/utm_medium=pin/.test(u)) throw new Error(u);
  if (!/utm_content=vakuumierer-pin-plakat/.test(u)) throw new Error(u);
  const alle = await pg.evaluate(() =>
    [...document.querySelectorAll('#zeilen .url')].map(x => /utm_content=([^&]+)/.exec(x.textContent)[1]));
  if (!alle.some(a => a === 'pumpe-pin-1-nachtfahrt')) throw new Error('Pumpenpins fehlen');
});
await step('Jeder Pin bleibt im Provisionsbericht unterscheidbar', async () => {
  const subs = await pg.evaluate(() =>
    [...document.querySelectorAll('#zeilen .sub')].map(s => s.textContent));
  const einzeln = new Set(subs);
  if (einzeln.size !== subs.length) throw new Error('gekürzte SubIDs doppelt: ' + subs.join(' | '));
  for (const s of subs) if (s.length > 100 + 'im Provisionsbericht: '.length) throw new Error('zu lang: ' + s);
});
await step('Profil-Link zeigt alle Motive zusammen', async () => {
  await pg.selectOption('#kanal', 'bio|link|alle');
  await pg.waitForTimeout(250);
  const n = await zeilen();
  if (n !== 29) throw new Error(n + ' Zeilen (erwartet 6 + 9 + 14)');
});
await step('Sammelkopie liefert eine vollständige Tabelle', async () => {
  const t = await pg.evaluate(() => {
    let g = "";
    navigator.clipboard.writeText = async v => { g = v; };
    document.getElementById('alle').click();
    return new Promise(r => setTimeout(() => r(g), 60));
  });
  const z = t.trim().split('\n');
  if (z.length !== 30) throw new Error(z.length + ' Zeilen inkl. Kopf');
  if (z[0] !== 'Motiv\tFormat\tAdresse\tSubID') throw new Error('Kopfzeile: ' + z[0]);
  if (z[1].split('\t').length !== 4) throw new Error('Spalten: ' + z[1]);
});
await pg.selectOption('#kanal', 'pinterest|pin|pin');
await pg.waitForTimeout(250);
await pg.screenshot({ path: 'linktool.png', fullPage: true });
await b.close();
console.log('\n' + (errs.length ? 'FEHLER: ' + errs.join(', ') : 'Alles bestanden.'));
process.exit(errs.length ? 1 : 0);
