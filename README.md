# Raudrohi & Münt

Eestikeelne I Chingi (Muutuste raamatu) rakendus brauseris. Heida heksagramm, loe selle tähendust tänapäeva keeles koos klassikalise tekstiga, sirvi kõiki 64 heksagrammi ja pea oma lugemiste päevikut.

**Kasuta veebis:** <https://tarmokouhkna.github.io/raudrohi-ja-munt/>

## Võimalused

- **Heitmine:** kolm virtuaalset münti (kull ehk pildiga pool 3, kiri ehk numbriga pool 2) või raudrohuvarte meetodi tõenäosused. Kui heidad päris münte, saad joone summa (6, 7, 8, 9) ka ise sisestada. Kolmas viis, **Küsimusest**, arvutab heksagrammi küsimuse sõnadest ja kellaajast – see on Hiina Ploomiõie numeroloogia (梅花易數) kohandus eesti keelele: hiina märgi kriipsude asemel loetakse sõnade tähti. Neljas viis, **Ajast**, on Ploomiõie numeroloogia klassikaline põhivariant: heksagramm arvutatakse Hiina kuukalendri aastast, kuust, päevast ja kahetunnisest ajast. Kuukalendri kuupäeva arvutab rakendus ise (aastad 1900–2100).
- **Lugemine:** põhiheksagramm (praegune olukord) ja muutuvate joonte korral seotud heksagramm (kuhu olukord liigub). Lisaks juhis, millele lugemisel kõige rohkem kaalu anda.
- **Selgitused:** igal heksagrammil on tänapäevane selgitus koos osadega „Mida teha“ ja „Millest hoiduda“. Igal joonel on lühike seletus argikeeles.
- **Klassikaline tekst:** iga heksagrammi otsus ja iga joone tekst James Legge tõlke järgi, eestindatuna. Nupuga saab vaadata ka Legge ingliskeelset originaali.
- **Heksagrammid:** kõik 64 heksagrammi. Otsida saab nime, numbri või märksõna järgi; filtreerida ülemise ja alumise trigrammi järgi (mõlema valimisel jääb alles täpselt üks heksagramm).
- **Päevik:** iga lõpetatud lugemine salvestatakse automaatselt sinu brauserisse (`localStorage`). Igale lugemisele saab lisada märkmeid.
- **Varukoopia:** päeviku saab kopeerida või failina alla laadida ning hiljem (ka teises seadmes) tagasi importida.
- **Jagamine:** lugemist saab jagada lingiga (`#lugemine-779878`). Lingis on ainult jooned – küsimus ja märkmed jäävad jagajale.
- **Esmakülastaja tutvustus:** avalehel on uuele kasutajale lühike riba (mis see on ja kolm sammu); see kaob pärast esimest lugemist või sulgemist.
- **Juhend:** jaotis „Juhend“ selgitab algajale, kuidas küsimust sõnastada, münte heita ja vastust lugeda.
- **Paigaldatav rakendus:** telefonis saab lehe lisada avaekraanile („Lisa avakuvale“ / „Install app“) ja see töötab ka ilma internetita.

## Käivitamine

Rakendus on üks staatiline leht ilma ehitussammudeta. Andmefailid laaditakse `fetch()`-iga, seega tuleb leht avada veebiserveri kaudu, mitte otse failina (`file://`).

```bash
python3 -m http.server 8000
```

Seejärel ava brauseris <http://localhost:8000>.

### GitHub Pages

Repo saab avaldada GitHub Pagesis: **Settings → Pages → Build and deployment → Deploy from a branch**, vali haru `main` ja kaust `/ (root)`.

## Failid

| Fail | Sisu |
|---|---|
| `index.html` | Kogu rakendus: HTML, CSS, JavaScript, heksagrammide nimed, märksõnad ja selgitused |
| `legge-et.json` | Klassikaline tekst eesti keeles (Legge järgi): 64 otsust ja 384 joont, 1. ja 2. heksagrammil lisatekst |
| `legge.json` | James Legge ingliskeelne originaaltekst (1882) |
| `jooned.json` | Joonte tänapäevased seletused (64 × 6, 1. ja 2. heksagrammil lisaks 7.) |
| `manifest.webmanifest`, `sw.js`, `icons/` | Paigaldatava rakenduse (PWA) failid; `sw.js` võimaldab töötada ilma internetita |
| `og.png` | Eelvaatepilt, mida näidatakse lingi jagamisel |
| `tools/check.py` | Andmete terviklikkuse kontroll (käivitub GitHubis iga pushi peale) |
| `tools/make_artifact.py` | Teeb `index.html`-ist claude.ai artefakti versiooni |

JSON-failide struktuur:

- `legge*.json`: massiiv 64 objektiga `{ "j": otsus, "l": [joon1, …, joon6, (kõik muutuvad)] }`, King Wen'i järjekorras.
- `jooned.json`: massiiv 64 massiiviga `[joon1, …, joon6, (kõik muutuvad)]`.

## Kontroll

```bash
python3 tools/check.py
```

Skript kontrollib, et heksagramme on 64 ja trigramme 8, nimed on unikaalsed, märksõnad ei korda nime ning iga joone tekst (katkematu/katkendlik) vastab heksagrammi tegelikule joonele. Sama kontroll käivitub GitHub Actionsis iga pushi ja pull requesti peale.

## Tekstide päritolu

- **Legge ingliskeelne tekst** pärineb teosest *The Sacred Books of the East, vol. 16: The Yi King* (Oxford, 1882), mis on avalikus omandis. Tekst on võetud Internet Archive'is olevatest skaneeringutest. Kahe sõltumatu skaneeringu OCR-teksti võrreldi omavahel sõna-sõnalt ja vead parandati käsitsi.
- **Eestikeelne klassikaline tekst** on tõlgitud Legge ingliskeelsest tekstist, mitte otse hiina keelest. Sulgudes olevad sõnad on Legge enda lisatud selgitused.
- **Heksagrammide selgitused ja joonte tänapäevased seletused** on selle rakenduse jaoks kirjutatud algupärased tõlgendused.

## Litsents

Kood ja selle rakenduse jaoks kirjutatud tekstid (selgitused, joonte seletused ja eestikeelne tõlge) on avaldatud [MIT-litsentsi](LICENSE) all. James Legge 1882. aasta ingliskeelne tekst (`legge.json`) on avalikus omandis.

Virtuaalmündi kullipoolel olev kotkas on ikoon „Eagle emblem“ saidilt [game-icons.net](https://game-icons.net) litsentsiga [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/); originaalfail on `icons/eagle-emblem.svg`.

## Tehniline

- Väliseid teeke ei kasutata, ainult Google Fontsi kirjatüübid (Cormorant Garamond, IBM Plex Sans, IBM Plex Mono, Noto Serif TC).
- Leht kohandub telefoni ekraaniga. Hele ja tume režiim järgivad vaikimisi süsteemi seadet; päise nupuga saab režiimi vahetada ja valik jäetakse meelde.
- Juhuslikkuse allikas on `crypto.getRandomValues`.
- Ekraanilugejale kirjeldatakse heksagrammi jooned tekstina.
- Service worker laadib oma failid esmalt võrgust (uuendused jõuavad kohe kasutajani) ja kasutab vahemälu ainult siis, kui ühendust pole.
