#!/usr/bin/env node
/* ══════════════════════════════════════════════════════════════════════════
   Motive über die offiziellen Schnittstellen ausspielen.

   Posten per API ist erlaubt und vorgesehen — anders als das Anlegen von
   Konten. Was es dafür braucht, steht in LIESMICH.md.

   Vorsichtsmaßnahmen, die hier eingebaut sind:
   · Probelauf ist die Voreinstellung. Wirklich gesendet wird nur mit --los.
   · Zugangsschlüssel kommen aus der Umgebung, nie aus einer Datei im Ordner.
     Nichts davon darf je eingecheckt werden.
   · Was gesendet wurde, steht in gesendet.json. Ein zweiter Lauf überspringt
     es, damit nicht doppelt gepostet wird.
   · Motive ohne Text werden übersprungen statt leer hochgeladen.
   ══════════════════════════════════════════════════════════════════════════ */
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const HIER = dirname(fileURLToPath(import.meta.url));
const PLAN = JSON.parse(readFileSync(join(HIER, 'plan.json'), 'utf8'));
const BUCH = join(HIER, 'gesendet.json');

const argv = process.argv.slice(2);
const hat = (f) => argv.includes(f);
const wert = (f, s) => { const i = argv.indexOf(f); return i === -1 ? s : argv[i + 1]; };

const LOS = hat('--los');
const KANAL = wert('--kanal', 'alle');
const NUR = wert('--nur', null);          // eine einzelne Motiv-Kennung
const GRENZE = parseInt(wert('--hoechstens', '5'), 10);

const gesendet = existsSync(BUCH) ? JSON.parse(readFileSync(BUCH, 'utf8')) : {};
const merken = (id, kanal, antwort) => {
  gesendet[id + '@' + kanal] = { wann: new Date().toISOString(), antwort };
  writeFileSync(BUCH, JSON.stringify(gesendet, null, 2) + '\n');
};

/* ---------- Schlüssel aus der Umgebung ---------- */
const S = {
  pinterest: process.env.PINTEREST_TOKEN,
  brett:     process.env.PINTEREST_BOARD_ID,
  meta:      process.env.META_TOKEN,
  ig:        process.env.IG_USER_ID,
  seite:     process.env.FB_PAGE_ID,
};

function fehlt(kanal) {
  if (kanal === 'pinterest') return !S.pinterest || !S.brett
    ? 'PINTEREST_TOKEN und PINTEREST_BOARD_ID' : null;
  if (kanal === 'instagram') return !S.meta || !S.ig ? 'META_TOKEN und IG_USER_ID' : null;
  if (kanal === 'facebook')  return !S.meta || !S.seite ? 'META_TOKEN und FB_PAGE_ID' : null;
  return 'unbekannter Kanal ' + kanal;
}

async function ruf(url, koerper) {
  const a = await fetch(url, {
    method: 'POST',
    headers: koerper instanceof URLSearchParams
      ? { 'Content-Type': 'application/x-www-form-urlencoded' }
      : { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + S.pinterest },
    body: koerper instanceof URLSearchParams ? koerper : JSON.stringify(koerper),
  });
  const t = await a.text();
  let j; try { j = JSON.parse(t); } catch { j = { roh: t }; }
  if (!a.ok) throw new Error(a.status + ' ' + t.slice(0, 300));
  return j;
}

/* ---------- Pinterest ----------
   Aus der Doku von Pinterest, Fassung v5. Ich konnte sie nicht abrufen —
   sie liegt hinter einer Anmeldung — also gilt: vor dem ersten echten Lauf
   gegen die aktuelle Referenz prüfen. Der Probelauf zeigt genau, was ginge.
   Nötige Rechte: pins:write, boards:read. */
async function pinterest(e) {
  return ruf('https://api.pinterest.com/v5/pins', {
    board_id: S.brett,
    title: e.titel.slice(0, 100),
    description: e.text.slice(0, 500),
    alt_text: e.alt.slice(0, 500),
    link: e.link,
    media_source: { source_type: 'image_url', url: e.bild },
  });
}

/* ---------- Instagram ----------
   Bestätigt an der Doku von Meta: erst einen Behälter anlegen, dann
   veröffentlichen. Das Bild lädt Meta selbst herunter, es muss also
   öffentlich erreichbar liegen. Rechte: instagram_basic,
   instagram_content_publish, pages_read_engagement. 100 Beiträge je 24 h.
   Instagram macht Links im Text nicht anklickbar — die Adresse gehört ins
   Profil, im Text steht sie nur als Hinweis. */
async function instagram(e) {
  const behaelter = await ruf(
    'https://graph.facebook.com/v21.0/' + S.ig + '/media',
    new URLSearchParams({ image_url: e.bild, caption: e.text, access_token: S.meta }));
  if (!behaelter.id) throw new Error('kein Behälter: ' + JSON.stringify(behaelter));
  return ruf(
    'https://graph.facebook.com/v21.0/' + S.ig + '/media_publish',
    new URLSearchParams({ creation_id: behaelter.id, access_token: S.meta }));
}

/* ---------- Facebook-Seite ----------
   Ein Schritt, Bild und Text zusammen. Recht: pages_manage_posts.
   Anders als bei Instagram ist die Adresse im Text anklickbar. */
async function facebook(e) {
  return ruf(
    'https://graph.facebook.com/v21.0/' + S.seite + '/photos',
    new URLSearchParams({ url: e.bild, caption: e.text + '\n\n' + e.link,
                          access_token: S.meta }));
}

const SENDER = { pinterest, instagram, facebook };

/* ---------- Lauf ---------- */
const dran = PLAN
  .filter(e => !NUR || e.id === NUR)
  .flatMap(e => e.kanaele
    .filter(k => KANAL === 'alle' || k === KANAL)
    .map(k => ({ e, k })));

console.log(LOS ? '── ECHTER LAUF ──' : '── Probelauf. Zum Senden --los anhängen. ──');
console.log(dran.length + ' Paarungen aus Motiv und Kanal im Blick\n');

let getan = 0, uebersprungen = 0;
for (const { e, k } of dran) {
  const kennung = e.id + ' → ' + k;

  if (gesendet[e.id + '@' + k]) {
    console.log('· schon gesendet am ' + gesendet[e.id + '@' + k].wann.slice(0, 10) + ': ' + kennung);
    uebersprungen++; continue;
  }
  if (!e.fertig) {
    console.log('· ohne Text, übersprungen: ' + kennung);
    uebersprungen++; continue;
  }
  const mangel = fehlt(k);
  if (mangel) {
    console.log('· ' + mangel + ' fehlt in der Umgebung: ' + kennung);
    uebersprungen++; continue;
  }
  if (getan >= GRENZE) {
    console.log('· Tagesgrenze von ' + GRENZE + ' erreicht, Rest bleibt liegen');
    break;
  }

  if (!LOS) {
    console.log('✓ würde senden: ' + kennung);
    console.log('   Bild  ' + e.bild);
    console.log('   Titel ' + (e.titel || '—'));
    console.log('   Ziel  ' + e.link);
    getan++; continue;
  }

  try {
    const antwort = await SENDER[k](e);
    merken(e.id, k, antwort);
    console.log('✓ gesendet: ' + kennung + '  ' + JSON.stringify(antwort).slice(0, 120));
    getan++;
    await new Promise(r => setTimeout(r, 2500));   // nicht drängeln
  } catch (err) {
    console.log('✗ fehlgeschlagen: ' + kennung + '\n   ' + err.message);
  }
}

console.log('\n' + getan + (LOS ? ' gesendet, ' : ' vorgemerkt, ') + uebersprungen + ' übersprungen');
if (!LOS && getan) console.log('Wenn das stimmt: dasselbe noch einmal mit --los.');
