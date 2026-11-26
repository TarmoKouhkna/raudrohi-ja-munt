# CLAUDE.md – Raudrohi & Münt

Eestikeelne I Chingi rakendus: üks staatiline leht (`index.html`) ja kolm JSON-andmefaili. Ehitussamme, teeke ega pakettide haldurit ei ole. Avalik leht asub aadressil https://tarmokouhkna.github.io/raudrohi-ja-munt/ (GitHub Pages, haru `main`, kaust `/`); iga push harusse `main` avaldab muudatuse umbes minutiga.

## Struktuur

- `index.html` – kogu rakendus: CSS (värvid tokenitena `:root`-is, hele ja tume teema), HTML ja üks `<script>`, kus on:
  - `TRI` – 8 trigrammi (nimi, sümbol, kirjeldus `attr`).
  - `RAW` – 64 heksagrammi King Wen'i järjekorras: `[hanzi, pinyin, eestikeelne nimi, ülemine trigramm, alumine trigramm, 'märksõna · märksõna · märksõna', mida see tähendab, mida teha, millest hoiduda]`.
  - `POS` – kuue joone koha tähendused, `VNAME` – joone väärtuste (6/7/8/9) nimed, `guidance()` – lugemisreeglid muutuvate joonte arvu järgi.
- `legge-et.json` – klassikaline tekst eesti keeles: 64 × `{ "j": otsus, "l": [joon1…joon6, (kõik muutuvad)] }`. 7. element on ainult heksagrammidel 1 ja 2.
- `legge.json` – sama struktuur, James Legge ingliskeelne originaal (1882, avalik omand).
- `jooned.json` – joonte tänapäevased seletused: 64 × `[joon1…joon6, (kõik muutuvad)]`.
- `manifest.webmanifest`, `sw.js`, `icons/`, `og.png` – PWA ja jagamise eelvaade. **Ainult GitHubi versioonis**: neid ei avaldata artefakti ja nende päisesildid on ainult repo `index.html` `<head>`-is. `sw.js` kasutab oma failide puhul võrk-enne-vahemälu strateegiat; kui lisad uue andmefaili, lisa see ka `CORE` loendisse ja suurenda `CACHE` versiooni.
- `tools/check.py` – andmete kontroll (käivitub ka GitHub Actionsis, `.github/workflows/check.yml`). `tools/make_artifact.py` – teeb artefakti versiooni.

Vaated (aadressi `#`): `#cast` (heitmine), `#library`, `#journal`, `#juhend`. `#lugemine-XXXXXX` (6 numbrit 6–9) avab jagatud lugemise; lingis ei ole küsimust ega märkmeid. Päeviku kirje: `{id, q, date, method, lines, notes?}` võtme `yc-journal` all `localStorage`-is. Muud võtmed: `yc-classic` (klassikalise teksti keel), `yc-intro` (esmakülastaja riba suletud), `yc-theme` (`light`/`dark`, päise režiiminupu valik; puudumisel järgitakse süsteemi). Teema rakendatakse `<body>` alguse väikese skriptiga enne lehe joonistamist ja see seab `data-theme` atribuudi, mida CSS juba toetab. Esmakülastaja riba (`#intro`) näidatakse ainult siis, kui päevik on tühi ja riba pole suletud.

CSS-klassid: päise logo on `.seal`, raudrohuvarte pitser `.y-seal` – ära kasuta neid nimesid muuks.

Andmefailid laaditakse `fetch()`-iga, seega testi lehte serveri kaudu, mitte `file://` kaudu.

## Keel ja sisu

- Kogu liides ja sisu on **eesti keeles**. Kasuta eesti jutumärke „…“ ja mõttekriipsu –.
- Heksagrammide nimed on loomulikud eesti **nimisõnad** (nt „Loov jõud“, „Ühtehoidmine“, „Kitsikus“), mitte omadussõnad ega otsetõlked. Märksõnad ei tohi korrata heksagrammi nime.
- Selgitused ja joonte seletused on kirjutatud tavainimesele arusaadavas tänapäeva keeles, igapäevaelu näidetega. Need on **algupärased tõlgendused**, mitte tõlge – ära esita neid klassikalise tekstina.
- `legge-et.json` on tõlgitud Legge **ingliskeelsest** tekstist, mitte hiina keelest. Legge sulgudes olevad lisandused on säilitatud. Legge „its subject“ on eesti keeles **„inimene“** („näitab inimest ootamas…“), mitte „selle kandja“; viide teisele joonele on „esimese joone inimene“.
- Iga joone tekst algab tema kohaga („Esimene joon, katkematu, …“). „Katkematu“ = jang (1), „katkendlik“ = jin (0) – see peab vastama heksagrammi tegelikule joonele.

## Kontrollid enne commiti

1. Andmed: käivita `python3 tools/check.py` (64 heksagrammi, joonte arv, unikaalsed nimed ja trigrammipaarid, märksõnad ei korda nime, „katkematu/katkendlik“ vastab joonele).
2. Leht kohalikult: `python3 -m http.server 8000`, seejärel ava http://localhost:8000. Kontrolli Playwrightiga (Chromium on keskkonnas olemas), et konsoolis vigu pole, andmed laadivad (`.classic.wait` ja `.plain.wait` puuduvad) ja `document.documentElement.scrollWidth` on telefonilaiusel (390 px) 390.

## claude.ai artefakt

Rakendusest on olemas ka claude.ai artefakt: https://claude.ai/artifact/QALdoaKSqjmpNyfs9xB3Ee (failid `index.html`, `legge.json`, `legge-et.json`, `jooned.json`). Hoia see GitHubi versiooniga samas seisus: kui muudad repot, uuenda ka artefakti.

Artefakti `index.html` on repo `index.html` **ilma** raamistikuta: claude.ai lisab ise `<!doctype>`, `<html>`, `<head>`, `<body>` ja põhistiilid. Tee see käsuga `python3 tools/make_artifact.py VÄLJUND.html` – skript eemaldab raamistiku ja ainult GitHubile mõeldud päisesildid ning lisab `<meta name="claude:viewport-fit-sides" content="cover">`. Avalda väljund artefakti `index.html`-ina; andmefailid avalda ainult siis, kui need muutusid.

Kood töötab mõlemas keskkonnas: allalaadimise nupp, lingi kopeerimine ja service worker lülituvad sisse ainult GitHub Pagesis ja `localhost`-is (`canCopyUrl`). Artefaktis paneb „Jaga lugemist“ lingi aadressiribale.

## Litsents

MIT (`LICENSE`). Legge 1882. aasta tekst on avalikus omandis.
