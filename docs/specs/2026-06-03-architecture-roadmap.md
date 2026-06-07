# hebrewcal — Architektur & Roadmap

**Status:** Entwurf, genehmigt
**Datum:** 2026-06-03
**Repo:** https://github.com/bsesic/hebrewcal
**Lizenz:** MIT

---

## 1. Zielsetzung

`hebrewcal` ist eine vollständige, **rein in Python** geschriebene Bibliothek für den
hebräischen Kalender. Sie macht den hebräischen Kalender programmatisch nutzbar und
rechnet ihn bidirektional gegen den gregorianischen und julianischen Kalender um —
**vollständig lokal, ohne jeden API-Call** zu einem abhängigen System.

Die Bibliothek dient gleichermaßen:

1. **religiösen Zwecken** — Feiertage, Schabbat, Havdala, Zmanim, Tora-Lesungen, Omer,
   Jahrzeit, Schmita/Jubeljahr, für Israel und die Diaspora.
2. **akademischen Zwecken** — historische, mittelalterliche und antike Daten,
   babylonische und biblische Monatsnamen, proleptische Kalender, korrekte Behandlung
   der Julian↔Gregorian-Reform und der „missing years" der Anno-Mundi-Zählung.

### Abgrenzung zu bestehenden Paketen

- `hebcal` (PyPI): unvollständig, für die Zielsetzung nicht ausreichend.
- `hebcal-api`: nur ein Wrapper um hebcal.com — erfordert API-Calls. **Explizit nicht
  gewollt.** `hebrewcal` rechnet alles lokal.
- Das hebcal-Referenzrepo (https://github.com/hebcal/hebcal) dient als
  fachliche Vergleichsgrundlage, wird aber nicht 1:1 portiert.

---

## 2. Grundsatzentscheidungen

| Thema | Entscheidung |
|-------|--------------|
| **Astronomie** (Sonnenstand, Auf-/Untergang, Dämmerung) | Reines Python, **null Dependencies**; Meeus/NOAA-Sonnenstandsalgorithmen selbst implementiert. Genauigkeit ~1 Min reicht für Halacha. |
| **Algorithmisches Fundament** | Dershowitz & Reingold, *Calendrical Calculations* — akademischer Goldstandard, sauber dokumentiert, ideal für historische/proleptische Daten. |
| **Erweiterbarkeit** | Abstraktes Kalender-Interface **von Anfang an**, sodass alternative Systeme (Karäer, Qumran, Samaritaner) ohne Kernänderung andocken. |
| **MVP** | Kern + Konversion + Astronomie + Feiertage (Phasen 1–3). |
| **Abhängigkeiten** | Nur Python-Standardbibliothek (`zoneinfo` für Zeitzonen). Keine Laufzeit-Dependencies. |
| **Python-Version** | 3.11+ (für `zoneinfo`). |

---

## 3. Architektur-Grundprinzip

Alles dreht sich um **eine universelle Pivot-Zahl: die Rata Die (RD)** — die fortlaufende
Tagesnummer nach Dershowitz & Reingold (Tag 1 = 1. Januar 1 proleptisch-gregorianisch).

Jeder Kalender implementiert nur zwei Operationen:

```
to_rd(datum)  -> int      # Kalenderdatum → fortlaufende Tagesnummer
from_rd(int)  -> datum     # fortlaufende Tagesnummer → Kalenderdatum
```

Konversion zwischen **beliebigen** Kalendern läuft immer über RD. Damit ist das
erweiterbare Interface gesetzt: ein neuer Kalender braucht nur `to_rd`/`from_rd`, und ist
sofort mit allen anderen umrechenbar.

```
hebrewcal/
├── core/
│   ├── rata_die.py        # RD-Epoche & Arithmetik (Dreh- und Angelpunkt)
│   └── calendar.py        # abstrakte Calendar-Basisklasse (das Interface)
├── calendars/
│   ├── gregorian.py       # + proleptisch
│   ├── julian.py          # + Reform-Sprung 1582ff., proleptisch
│   └── hebrew.py          # hebräischer Kalender (nutzt hebrew/*)
├── hebrew/                # hebräische Maschinerie
│   ├── molad.py           # Molad, Halakim/Chalakim (1080 parts), Helek
│   ├── yeartype.py        # deficient/regular/complete, Schaltjahr, Jahres-/Monatslängen
│   ├── dechiyot.py        # die 4 Aufschub-Regeln für Rosch Haschana (die „4 Tore")
│   ├── keviah.py          # Jahrestyp-Signatur
│   └── metonic.py         # 19-Jahr-Zyklus
├── eras/
│   └── anno_mundi.py      # AM-Zählung + „missing years"-Behandlung (dokumentiert)
├── parsing/               # Eingabe: ISO 8601, DIN 5008, weitere Formate
├── formatting/            # Ausgabe-Formate
├── numerals.py            # Gematria ↔ Integer (Zahlen-/Jahresumrechner)
├── names.py               # Monats-/Tagesnamen: Standard, babylonisch, biblisch, Translit.
├── astro/                 # reines Python, null Dependencies
│   ├── solar.py           # Sonnenstand, Auf-/Untergang, Dämmerung (Meeus/NOAA)
│   ├── location.py        # geografischer Ort
│   └── timezone.py        # Zeitzonen (stdlib zoneinfo)
├── religious/
│   ├── holidays.py        # Feiertage: Israel/Diaspora, Minderheiten, Schuschan Purim
│   ├── shabbat.py         # Kerzenzünden, Havdala
│   ├── zmanim.py          # halachische Zeiten
│   ├── omer.py            # Omer-Zählung
│   ├── torah.py           # Tora-Lesungen (Paraschot)
│   ├── yahrzeit.py        # Jahrzeit
│   └── sabbatical.py      # Schmita / Jubeljahr
└── calendars_alt/         # Phase 5: karaite.py, qumran.py, samaritan.py
```

---

## 4. Roadmap (Phasen)

### Phase 0 — Gerüst & Infrastruktur
- src-Layout, `pyproject.toml` (PEP 621)
- pytest + ruff + mypy
- GitHub Actions CI (Test-Matrix über Python-Versionen)
- Sphinx + ReadTheDocs
- PyPI Trusted Publishing (OIDC), SemVer
- `CONTRIBUTING.md`, `CHANGELOG.md`
- **Policy: keine Claude-Attribution** in Code, Doku, Kommentaren oder Commits.

### Phase 1 — Kalenderkern + Konversion + Datumshandling  *(MVP, Teil 1)*
- RD-Pivot + abstraktes `Calendar`-Interface
- Gregorian + Julian (Reform-Sprung & proleptisch)
- Vollständiger hebräischer Kern: Molad/Halakim, Dechijot (4 Tore), Jahrestypen
  (deficient/regular/complete), Keviah, Schaltjahre/-monate, Metonzyklus
- Bidirektionale Konversion über RD (hebr. ↔ greg. ↔ jul.)
- Parsing (ISO 8601, DIN 5008, weitere) + Formatierung
- Gematria-Zahlen-/Jahresumrechner
- Monats-/Tagesnamen: Standard, babylonisch, biblisch, Transliteration
- Anno-Mundi-Ära inkl. dokumentierter „missing years"-Behandlung
- Testsuite gegen bekannte Referenzdaten

### Phase 2 — Astronomie & Orte
- Sonnenstand, Auf-/Untergang, Dämmerung (reines Python, Meeus/NOAA)
- `Location` (geografische Koordinaten, Höhe)
- Zeitzonen (stdlib `zoneinfo`)
- Neumond-/Molad-Bezug zur sichtbaren Astronomie

### Phase 3 — Feiertage  *(MVP, Teil 2)*
- Feiertags-Engine: alle Hauptfeste
- Israel vs. Diaspora (z. B. zweiter Feiertag, Schuschan Purim)
- Rosch Chodesch, Fastentage
- Moderne Tage (Jom haAtzmaut, Jom haScho'a, Jom Jeruschalajim …)
- Minderheiten-Feste (z. B. äthiopisches Sigd)
- Omer-Zählung
- Besondere Schabbatot

### Phase 4 — Religiöse Zeiten  *(baut auf Phase 2)*
- Schabbat-Kerzenzünden & Havdala (ortsabhängig)
- Vollständige Zmanim (halachische Zeiten)
- Molad-/Rosch-Chodesch-Ansage
- Jahrzeit (Yahrzeit)
- Tora-Lesungen (jährlich + dreijährig)
- Schmita / Jubeljahr (Hall- und Jubeljahr)

### Phase 5 — Alternative Kalender
- Karäer, Qumran, Samaritaner über das `Calendar`-Interface

### Phase 6 — Politur & 1.0
- Doku vollständig, Beispiele, optionale CLI
- Performance
- PyPI-Release 1.0

**MVP = Phasen 1–3.**

---

## 5. Sonderfälle & Risiken (verbindlich zu behandeln)

### Julian ↔ Gregorian-Reform
Die Kalenderreform von 1582 wurde regional zu unterschiedlichen Zeitpunkten
eingeführt. Die Bibliothek rechnet intern **proleptisch über RD** und macht die Reform
**explizit und konfigurierbar** — kein stillschweigender Sprung. Standardannahmen werden
dokumentiert.

### „Missing years" der Anno-Mundi-Zählung
Die traditionelle Anno-Mundi-Zählung weicht für die persische Epoche um ~165 Jahre von
der akademisch-historischen Chronologie ab
(vgl. https://en.wikipedia.org/wiki/Missing_years_(Jewish_calendar)).

**Lösung:** Die AM-Konversion ist rechnerisch korrekt und eindeutig. Die historische
Diskrepanz wird **dokumentiert und nicht stillschweigend „korrigiert"**. Optional bietet
die Bibliothek einen Hinweis-/Mapping-Helfer für akademische Nutzung. So bleiben
religiöser und akademischer Zweck beide sauber bedient.

### Kein abhängiges System
Sämtliche Berechnungen erfolgen lokal. Keine Netzwerk-Calls, keine externen Dienste.

### Datums-Eingabeformate
Gregorianische Daten in mehreren Formaten eingebbar (ISO 8601 / DIN 5008 / weitere),
robust geparst und eindeutig normalisiert.

---

## 6. Validierungs-Beispiele (akzeptanznah)

Die Bibliothek muss u. a. folgende Anfragen korrekt beantworten:

- „Wann beginnt der Schabbat am 26.06.2026 in New York?" (Phase 4)
- „Welches hebräische Datum und welcher Wochentag entspricht dem 31.10.1867?" (Phase 1)
- Vor- und Rückwärtsberechnung beliebiger Daten, inkl. historischer/antiker Daten.

---

## 7. Glossar der zu lösenden Kernprobleme

Molad · Halakim/Chalakim (1080 Teile/Stunde) · Helek · die 4 Tore (Dechijot) · Minor/Major
Era · Cycle of years · Schaltjahre/-monate · Rosch Haschana-Regeln · deficient/regular/
complete years · Keviah · Metonzyklus (19 Jahre) · celestial rotation.
