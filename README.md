# Raudrohi & Münt

Eestikeelne I Chingi (Muutuste raamatu) rakendus brauseris. Heida heksagramm, loe selle tähendust tänapäeva keeles koos klassikalise tekstiga, sirvi kõiki 64 heksagrammi ja pea oma lugemiste päevikut.

## Võimalused

- **Heitmine:** kolm virtuaalset münti (kirjaga pool 3, sile pool 2) või raudrohuvarte meetodi tõenäosused. Kui heidad päris münte, saad joone summa (6, 7, 8, 9) ka ise sisestada.
- **Lugemine:** põhiheksagramm (praegune olukord) ja muutuvate joonte korral seotud heksagramm (kuhu olukord liigub). Lisaks juhis, millele lugemisel kõige rohkem kaalu anda.
- **Selgitused:** igal heksagrammil on tänapäevane selgitus koos osadega „Mida teha“ ja „Millest hoiduda“. Igal joonel on lühike seletus argikeeles.
- **Klassikaline tekst:** iga heksagrammi otsus ja iga joone tekst James Legge tõlke järgi, eestindatuna. Nupuga saab vaadata ka Legge ingliskeelset originaali.
- **Heksagrammid:** kõik 64 heksagrammi. Otsida saab nime, numbri, märksõna või trigrammi järgi.
- **Päevik:** iga lõpetatud lugemine salvestatakse automaatselt sinu brauserisse (`localStorage`).

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

JSON-failide struktuur:

- `legge*.json`: massiiv 64 objektiga `{ "j": otsus, "l": [joon1, …, joon6, (kõik muutuvad)] }`, King Wen'i järjekorras.
- `jooned.json`: massiiv 64 massiiviga `[joon1, …, joon6, (kõik muutuvad)]`.

## Tekstide päritolu

- **Legge ingliskeelne tekst** pärineb teosest *The Sacred Books of the East, vol. 16: The Yi King* (Oxford, 1882), mis on avalikus omandis. Tekst on võetud Internet Archive'is olevatest skaneeringutest. Kahe sõltumatu skaneeringu OCR-teksti võrreldi omavahel sõna-sõnalt ja vead parandati käsitsi.
- **Eestikeelne klassikaline tekst** on tõlgitud Legge ingliskeelsest tekstist, mitte otse hiina keelest. Sulgudes olevad sõnad on Legge enda lisatud selgitused.
- **Heksagrammide selgitused ja joonte tänapäevased seletused** on selle rakenduse jaoks kirjutatud algupärased tõlgendused.

## Litsents

Kood ja selle rakenduse jaoks kirjutatud tekstid (selgitused, joonte seletused ja eestikeelne tõlge) on avaldatud [MIT-litsentsi](LICENSE) all. James Legge 1882. aasta ingliskeelne tekst (`legge.json`) on avalikus omandis.

## Tehniline

- Väliseid teeke ei kasutata, ainult Google Fontsi kirjatüübid (Cormorant Garamond, IBM Plex Sans, IBM Plex Mono, Noto Serif TC).
- Leht kohandub telefoni ekraaniga ning toetab heledat ja tumedat teemat.
- Juhuslikkuse allikas on `crypto.getRandomValues`.
