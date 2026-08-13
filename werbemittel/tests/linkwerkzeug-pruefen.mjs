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

await step('Sechs Adressen (3 Motive x 2 Formate)', async () => {
  const n = await pg.evaluate(() => document.querySelectorAll('#zeilen tr').length);
  if (n !== 6) throw new Error(n + ' Zeilen');
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
await step('Kanalwechsel schlägt durch', async () => {
  await pg.selectOption('#kanal', 'pinterest|pin');
  await pg.waitForTimeout(250);
  const u = await pg.evaluate(() => document.querySelector('#zeilen .url').textContent);
  if (!/utm_source=pinterest/.test(u) || !/utm_medium=pin/.test(u)) throw new Error(u);
});
await pg.screenshot({ path: 'linktool.png', fullPage: true });
await b.close();
console.log('\n' + (errs.length ? 'FEHLER: ' + errs.join(', ') : 'Alles bestanden.'));
