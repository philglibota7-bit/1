import { chromium } from 'playwright';
const errs = [];
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport: { width: 1100, height: 1000 }, deviceScaleFactor: 2,
  permissions: ['notifications'], origin: 'file://' });
const pg = await ctx.newPage();
pg.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
pg.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });
const step = async (n, f) => { try { await f(); console.log('✓', n); }
  catch (e) { console.log('✗', n, '—', e.message.split('\n')[0]); errs.push(n); } };

await pg.goto('file:///home/user/1/squelly.html');
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(800);

await step('Preis, Stand und Beispiel-Kennzeichnung je Karte', async () => {
  const d = await pg.evaluate(() => [...document.querySelectorAll('.card')].map(c => ({
    preis: c.querySelector('.preis')?.textContent,
    stand: c.querySelector('.stand')?.textContent,
    demo: !!c.querySelector('.demo')
  })));
  const soll = await pg.evaluate(() => PRODUKTE.length);
  if (d.length !== soll) throw new Error(d.length + ' Karten zu ' + soll + ' Produkten');
  d.forEach(x => {
    if (!/€/.test(x.preis || '')) throw new Error('kein Preis: ' + JSON.stringify(x));
    if (!/Stand .*Tief .*Höchstwert/.test(x.stand || '')) throw new Error('Stand unvollständig: ' + x.stand);
    if (!x.demo) throw new Error('Beispiel-Kennzeichnung fehlt');
  });
  console.log('   ', d.map(x => x.preis).join(' | '));
});

await step('Trend zeigt Richtung und Betrag', async () => {
  const t = await pg.evaluate(() => [...document.querySelectorAll('.trend')].map(e => ({
    klasse: e.className, text: e.textContent.trim() })));
  // Vakuumierer 32,99 -> 29,99 fällt; Massagepistole 47,99 -> 49,99 steigt; Lampe unverändert
  if (!/ab/.test(t[0].klasse) || !/−/.test(t[0].text)) throw new Error(JSON.stringify(t[0]));
  if (!/auf/.test(t[1].klasse) || !/\+/.test(t[1].text)) throw new Error(JSON.stringify(t[1]));
  if (!/gleich/.test(t[2].klasse)) throw new Error(JSON.stringify(t[2]));
  console.log('   ', t.map(x => x.text).join(' | '));
});

await step('Verlaufslinie mit allen Messpunkten', async () => {
  const n = await pg.evaluate(() => {
    const pl = document.querySelector('.spark .linie');
    return pl.getAttribute('points').trim().split(/\s+/).length;
  });
  if (n !== 8) throw new Error(n + ' Punkte');
});

await step('Alarm: Ziel über dem Preis wird abgelehnt', async () => {
  await pg.evaluate(() => alarmUmschalten('vakuumierer'));
  await pg.fill('#ziel-vakuumierer', '99');
  await pg.evaluate(() => alarmSpeichern('vakuumierer'));
  await pg.waitForTimeout(300);
  const gespeichert = await pg.evaluate(() => Object.keys(ALARME).length);
  if (gespeichert !== 0) throw new Error('trotzdem gespeichert');
  const t = await pg.locator('.toast').innerText();
  if (!/erreicht/i.test(t)) throw new Error(t);
});

await step('Alarm setzen, speichern, im Knopf sichtbar', async () => {
  await pg.fill('#ziel-vakuumierer', '25');
  await pg.evaluate(() => alarmSpeichern('vakuumierer'));
  await pg.waitForTimeout(400);
  const a = await pg.evaluate(() => ALARME.vakuumierer);
  if (!a || a.ziel !== 25) throw new Error(JSON.stringify(a));
  const knopf = await pg.locator('.card').first().locator('.alarmbtn').innerText();
  if (!/25,00/.test(knopf) || !/noch/.test(knopf)) throw new Error(knopf);
});

await step('Schnellwahl rechnet vom aktuellen Preis', async () => {
  await pg.evaluate(() => zielSetzen('lampe', 0.9));
  const v = await pg.inputValue('#ziel-lampe');
  if (Math.abs(parseFloat(v) - 22.99 * 0.9) > 0.01) throw new Error(v);
});

await step('Alarm übersteht Neuladen', async () => {
  await pg.reload();
  await pg.waitForTimeout(800);
  const a = await pg.evaluate(() => ALARME.vakuumierer);
  if (!a || a.ziel !== 25) throw new Error('verloren');
});

await step('Erreichtes Ziel löst Meldung aus', async () => {
  await pg.evaluate(() => {
    const p = PRODUKTE.filter(x => x.kuerzel === 'lampe')[0];
    ALARME.lampe = { ziel: 25, seit: Date.now(), start: 29.99, gemeldet: null };
    alarmePruefen(false);
  });
  await pg.waitForTimeout(400);
  const t = await pg.locator('.toast').last().innerText();
  if (!/ausgelöst/i.test(t)) throw new Error(t);
});

await step('Meldung wiederholt sich nicht beim selben Preis', async () => {
  const vorher = await pg.evaluate(() => document.querySelectorAll('.toast').length);
  await pg.evaluate(() => alarmePruefen(false));
  await pg.waitForTimeout(300);
  const nachher = await pg.evaluate(() => document.querySelectorAll('.toast').length);
  if (nachher > vorher) throw new Error('doppelte Meldung');
});

await step('Alarm entfernen', async () => {
  await pg.evaluate(() => alarmLoeschen('vakuumierer'));
  await pg.waitForTimeout(300);
  const a = await pg.evaluate(() => ALARME.vakuumierer);
  if (a) throw new Error('noch da');
});

await step('Partner-Link und Zuordnung unverändert', async () => {
  const u = decodeURIComponent(await pg.evaluate(() => document.querySelector('.cta').href));
  if (!/tag=squelly-21/.test(u) || !/ascsubtag=sq-/.test(u)) throw new Error(u.slice(0, 120));
});

await pg.screenshot({ path: 'preis-desktop.png' });
const m = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true });
m.on('pageerror', e => errs.push('MOBIL: ' + e.message));
await m.goto('file:///home/user/1/squelly.html');
await m.evaluate(() => document.fonts.ready);
await m.waitForTimeout(800);
const ovf = await m.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
console.log(ovf > 2 ? '✗ mobiler Überlauf ' + ovf : '✓ kein mobiler Überlauf');
if (ovf > 2) errs.push('Überlauf');
await m.evaluate(() => alarmUmschalten('vakuumierer'));
await m.waitForTimeout(300);
await m.screenshot({ path: 'preis-mobil.png', fullPage: true });

await b.close();
console.log('\n' + (errs.length ? 'FEHLER: ' + errs.join(', ') : 'Alles bestanden, keine JS-Fehler.'));
process.exit(errs.length ? 1 : 0);
