"""werkbank - Steuerung des Tool-Portfolios.

    python3 -m cockpit heute        Was heute ansteht
    python3 -m cockpit --hilfe      Alle Befehle
"""

from __future__ import annotations

import argparse
import random
import sys
from datetime import date

from . import bericht, bewertung, plan, store
from .geld import fmt, zu_cent

ALPHABET = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"  # ohne I und O - Verwechslungsgefahr


# --------------------------------------------------------------------------
# Ausgabe
# --------------------------------------------------------------------------
def kopf(text: str) -> None:
    print(f"\n\033[1m{text}\033[0m")


def leise(text: str) -> None:
    print(f"\033[2m{text}\033[0m")


# --------------------------------------------------------------------------
# Ideen
# --------------------------------------------------------------------------
def idee_add(db, args) -> None:
    b = {k: getattr(args, k) for k in bewertung.KRITERIEN if getattr(args, k) is not None}
    idee = {
        "id": store.naechste_id(db, "idee"),
        "titel": args.titel,
        "notiz": args.notiz or "",
        "bewertung": b,
        "punkte": bewertung.punkte(b) if b else 0,
        "status": "geprueft" if b else "neu",
        "erstellt": date.today().isoformat(),
    }
    db["ideen"].append(idee)
    store.speichern(db)
    if b:
        print(f"Idee {idee['id']}: {idee['titel']} – {idee['punkte']} Punkte "
              f"→ {bewertung.urteil(idee['punkte'])}")
        leise(f"  {bewertung.begruendung(b)}")
    else:
        print(f"Idee {idee['id']}: {idee['titel']} (unbewertet)")
        leise(f"  Bewerten mit: werkbank idee bewerten {idee['id']}")


def idee_bewerten(db, args) -> None:
    idee = store.idee_finden(db, args.kennung)
    if not idee:
        sys.exit(f"Idee {args.kennung!r} nicht gefunden.")
    b = dict(idee.get("bewertung", {}))
    gesetzt = {k: getattr(args, k) for k in bewertung.KRITERIEN if getattr(args, k) is not None}

    if not gesetzt:  # interaktiv nachfragen
        kopf(idee["titel"])
        for name, k in bewertung.KRITERIEN.items():
            leise(f"  {k['hilfe']}")
            while True:
                roh = input(f"  {k['frage']} [0-5, aktuell {b.get(name, 0)}]: ").strip()
                if roh == "":
                    break
                if roh.isdigit() and 0 <= int(roh) <= 5:
                    b[name] = int(roh)
                    break
                print("  Bitte eine Zahl von 0 bis 5.")
    else:
        b.update(gesetzt)

    idee["bewertung"] = b
    idee["punkte"] = bewertung.punkte(b)
    idee["status"] = "geprueft"
    store.speichern(db)
    print(f"\n{idee['titel']}: {idee['punkte']} Punkte → "
          f"{bewertung.urteil(idee['punkte'])}")
    leise(f"  {bewertung.begruendung(b)}")


def idee_liste(db, args) -> None:
    ideen = db["ideen"]
    if args.alle is False:
        ideen = [i for i in ideen if i["status"] in ("neu", "geprueft")]
    if not ideen:
        print("Keine Ideen. Anlegen mit: werkbank idee add \"Titel\"")
        return
    ideen.sort(key=lambda i: -i.get("punkte", 0))
    kopf(f"{len(ideen)} Ideen")
    print(f"{'Nr.':>4}  {'Punkte':>6}  {'Urteil':<14} Titel")
    for i in ideen:
        p = i.get("punkte", 0)
        u = bewertung.urteil(p) if p else "unbewertet"
        print(f"{i['id']:>4}  {p:>6}  {u:<14} {i['titel']}")


def idee_status(db, args) -> None:
    idee = store.idee_finden(db, args.kennung)
    if not idee:
        sys.exit(f"Idee {args.kennung!r} nicht gefunden.")
    if args.status not in store.IDEE_STATUS:
        sys.exit(f"Status muss einer von {store.IDEE_STATUS} sein.")
    idee["status"] = args.status
    store.speichern(db)
    print(f"Idee {idee['id']} → {args.status}")


# --------------------------------------------------------------------------
# Zahlen
# --------------------------------------------------------------------------
def zahlen(db, args) -> None:
    bekannt = {t["slug"] for t in store.registry().get("tools", [])}
    if args.slug not in bekannt:
        sys.exit(f"Unbekanntes Tool {args.slug!r}. Bekannt: {', '.join(sorted(bekannt))}")
    monat = args.monat or bericht.monat_heute()
    e = store.monat_eintrag(db, monat, args.slug)
    if args.besucher is not None:
        e["besucher"] = args.besucher
    if args.kaeufe is not None:
        e["kaeufe"] = args.kaeufe
    if args.umsatz is not None:
        e["umsatz_cent"] = zu_cent(args.umsatz)
    store.speichern(db)
    print(f"{monat} · {args.slug}: {e['besucher']} Aufrufe, "
          f"{e['kaeufe']} Kaeufe, {fmt(e['umsatz_cent'])} EUR")


# --------------------------------------------------------------------------
# Auswertung
# --------------------------------------------------------------------------
def zeige_bericht(db, args) -> None:
    reg = store.registry()
    titel = {t["slug"]: t["titel"] for t in reg.get("tools", [])}
    monat = bericht.monat_heute()
    akt = bericht.letzter_monat(db, monat)
    ziel = db["einstellungen"]["ziel_monat_cent"]

    kopf(f"Monat {monat}")
    anteil = round(akt["umsatz_cent"] / ziel * 100) if ziel else 0
    balken = "█" * min(20, anteil // 5) + "·" * (20 - min(20, anteil // 5))
    print(f"  Umsatz    {fmt(akt['umsatz_cent']):>10} EUR   {balken} {anteil} % von "
          f"{fmt(ziel)} EUR")
    print(f"  Aufrufe   {akt['besucher']:>10}")
    print(f"  Kaeufe    {akt['kaeufe']:>10}")

    werte = bericht.je_tool(db)
    if werte:
        kopf("Portfolio (alle erfassten Monate)")
        print(f"  {'Tool':<24} {'Aufrufe':>9} {'Kaeufe':>7} {'Umsatz':>10}  Entscheidung")
        for slug, w in sorted(werte.items(), key=lambda x: -x[1]["umsatz_cent"]):
            print(f"  {titel.get(slug, slug)[:24]:<24} {w['besucher']:>9} "
                  f"{w['kaeufe']:>7} {fmt(w['umsatz_cent']):>10}  {bericht.empfehlung(w)}")

    offen = [i for i in db["ideen"] if i["status"] in ("neu", "geprueft")]
    reif = [i for i in offen if i.get("punkte", 0) >= bewertung.GRENZE_BAUEN]
    kopf("Ideen")
    print(f"  {len(offen)} offen, davon {len(reif)} ueber "
          f"{bewertung.GRENZE_BAUEN} Punkten (bauwuerdig)")

    kopf("Naechster Schritt")
    print(f"  {plan.naechster_schritt(db)}")
    print()


def tafel(db, args) -> None:
    ziel = store.home() / "tafel.html"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(bericht.tafel_html(db), encoding="utf-8")
    print(f"Tafel geschrieben: {ziel}")
    leise("  Im Browser oeffnen. Liegt bewusst ausserhalb des Repos.")


def heute(db, args) -> None:
    nr = plan.woche_nummer(db["einstellungen"]["gestartet_am"])
    _, schwerpunkt, aufgabe = plan.woche(nr)
    wochentag = ["Montag", "Dienstag", "Mittwoch", "Donnerstag",
                 "Freitag", "Samstag", "Sonntag"][date.today().weekday()]

    kopf(f"Woche {nr} · {schwerpunkt}")
    print(f"  {aufgabe}")

    kopf(f"Heute ist {wochentag}")
    for tage, was in plan.TAKT:
        if wochentag in tage or (tage.startswith("Dienstag") and
                                 wochentag in ("Dienstag", "Mittwoch", "Donnerstag")):
            print(f"  {was}")
            break

    kopf("Woran es gerade hakt")
    print(f"  {plan.naechster_schritt(db)}")
    print()


# --------------------------------------------------------------------------
# Werkzeuge
# --------------------------------------------------------------------------
def schluessel(db, args) -> None:
    """Lizenzschluessel erzeugen - dieselbe Pruefziffer wie in werkbank.js."""
    kopf(f"{args.anzahl} Schluessel")
    for _ in range(args.anzahl):
        kern = "".join(random.choice(ALPHABET) for _ in range(8))
        pruef = ALPHABET[sum(ord(c) for c in kern) % len(ALPHABET)]
        print(f"  WB-{kern[:4]}-{kern[4:]}-{pruef}")
    leise("\n  Nach einem Kauf einen davon per E-Mail schicken und hier abhaken.")
    print()


def ziel(db, args) -> None:
    db["einstellungen"]["ziel_monat_cent"] = zu_cent(args.betrag)
    store.speichern(db)
    print(f"Monatsziel: {fmt(db['einstellungen']['ziel_monat_cent'])} EUR")


# --------------------------------------------------------------------------
def parser_bauen() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="werkbank", description="Steuerung des Werkbank-Tool-Portfolios.")
    u = p.add_subparsers(dest="befehl", required=True)

    def bewertungs_flags(sp):
        for name, k in bewertung.KRITERIEN.items():
            sp.add_argument(f"--{name}", type=int, choices=range(6),
                            metavar="0-5", default=None, help=k["frage"])

    s = u.add_parser("idee", help="Ideen sammeln und bewerten")
    su = s.add_subparsers(dest="unterbefehl", required=True)

    sa = su.add_parser("add", help="Neue Idee anlegen")
    sa.add_argument("titel")
    sa.add_argument("--notiz", default="")
    bewertungs_flags(sa)
    sa.set_defaults(funktion=idee_add)

    sb = su.add_parser("bewerten", help="Idee bewerten (ohne Angaben: interaktiv)")
    sb.add_argument("kennung")
    bewertungs_flags(sb)
    sb.set_defaults(funktion=idee_bewerten)

    sl = su.add_parser("liste", help="Ideen anzeigen")
    sl.add_argument("--alle", action="store_true", help="auch verworfene und gebaute")
    sl.set_defaults(funktion=idee_liste)

    ss = su.add_parser("status", help="Status setzen")
    ss.add_argument("kennung")
    ss.add_argument("status", choices=store.IDEE_STATUS)
    ss.set_defaults(funktion=idee_status)

    z = u.add_parser("zahlen", help="Monatszahlen eines Tools erfassen")
    z.add_argument("slug")
    z.add_argument("--monat", help="JJJJ-MM, Standard: aktueller Monat")
    z.add_argument("--besucher", type=int)
    z.add_argument("--kaeufe", type=int)
    z.add_argument("--umsatz", help="in Euro, z. B. 57 oder 57,50")
    z.set_defaults(funktion=zahlen)

    u.add_parser("bericht", help="Auswertung im Terminal").set_defaults(funktion=zeige_bericht)
    u.add_parser("tafel", help="Auswertung als HTML-Datei").set_defaults(funktion=tafel)
    u.add_parser("heute", help="Was heute ansteht").set_defaults(funktion=heute)

    k = u.add_parser("schluessel", help="Lizenzschluessel erzeugen")
    k.add_argument("--anzahl", type=int, default=5)
    k.set_defaults(funktion=schluessel)

    g = u.add_parser("ziel", help="Monatsziel setzen")
    g.add_argument("betrag", help="in Euro, z. B. 500")
    g.set_defaults(funktion=ziel)

    return p


def main(argv: list[str] | None = None) -> None:
    args = parser_bauen().parse_args(argv)
    db = store.laden()
    args.funktion(db, args)


if __name__ == "__main__":
    main()
