#!/usr/bin/env python3
"""Kontrollib rakenduse andmete terviklikkust (vt CLAUDE.md, „Kontrollid enne commiti“).

Käivita repo juurkaustast:  python3 tools/check.py
Väljub koodiga 1, kui leiab vigu.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def err(msg):
    errors.append(msg)


html = (ROOT / 'index.html').read_text(encoding='utf-8')

# Trigrammid
tri = {k: b for k, b in re.findall(r"(\w+):\s*\{bits:'([01]{3})',name:'[^']+'", html)}
if len(tri) != 8 or len(set(tri.values())) != 8:
    err(f'Trigramme peab olema 8 ja kõigil erinevad bitid (leitud {len(tri)}).')

# Heksagrammid: [hanzi, pinyin, nimi, ülemine, alumine, 'märksõnad', tähendus, mida teha, millest hoiduda]
rows = re.findall(r"^\['([^']+)','([^']+)','([^']+)','(\w+)','(\w+)','([^']+)','((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)'\]", html, re.M)
if len(rows) != 64:
    err(f'RAW-s peab olema 64 heksagrammi, leitud {len(rows)}.')
bits = []
names = []
for n, (zh, py, name, up, lo, kw, m, t, h) in enumerate(rows, 1):
    if up not in tri or lo not in tri:
        err(f'#{n} {name}: tundmatu trigramm ({up}/{lo}).')
        continue
    bits.append(tri[lo] + tri[up])
    names.append(name)
    for k in kw.split(' · '):
        if k.lower() in name.lower() or name.lower() in k.lower():
            err(f'#{n} {name}: märksõna „{k}“ kordab nime.')
    if len(kw.split(' · ')) != 3:
        err(f'#{n} {name}: märksõnu peab olema 3.')
    for label, txt in (('tähendus', m), ('mida teha', t), ('millest hoiduda', h)):
        if len(txt.strip()) < 40:
            err(f'#{n} {name}: „{label}“ on puudu või liiga lühike.')
if len(set(bits)) != len(bits):
    err('Kahel heksagrammil on sama trigrammipaar.')
if len(set(names)) != len(names):
    err('Heksagrammide nimed ei ole unikaalsed.')


def expected_count(n):
    return 7 if n <= 2 else 6


def load(fn):
    try:
        return json.loads((ROOT / fn).read_text(encoding='utf-8'))
    except Exception as e:  # noqa: BLE001
        err(f'{fn}: ei õnnestunud lugeda ({e}).')
        return None


ORD_ET = ['Esime', 'Tei', 'Kolma', 'Nelja', 'Viie', 'Kuue|Ülemi']
for fn, yang_word, ord_check in (('legge-et.json', 'katkematu', True), ('legge.json', 'undivided', False)):
    data = load(fn)
    if data is None:
        continue
    if not isinstance(data, list) or len(data) != 64:
        err(f'{fn}: peab olema 64 kirjet.')
        continue
    for n, e in enumerate(data, 1):
        if not e.get('j'):
            err(f'{fn} #{n}: otsus puudub.')
        if not e.get('x'):
            err(f'{fn} #{n}: pilt (x) puudub.')
        lines = e.get('l', [])
        if len(lines) != expected_count(n):
            err(f'{fn} #{n}: jooni {len(lines)}, oodatud {expected_count(n)}.')
            continue
        if n - 1 < len(bits):
            for i in range(6):
                head = lines[i][:90]
                if (yang_word in head) != (bits[n - 1][i] == '1'):
                    err(f'{fn} #{n} joon {i + 1}: „{yang_word}“ ei vasta heksagrammi joonele.')
                if ord_check and not re.search(ORD_ET[i], lines[i]):
                    err(f'{fn} #{n} joon {i + 1}: joone koht puudub tekstist.')

jooned = load('jooned.json')
if jooned is not None:
    if not isinstance(jooned, list) or len(jooned) != 64:
        err('jooned.json: peab olema 64 kirjet.')
    else:
        for n, e in enumerate(jooned, 1):
            if len(e) != expected_count(n):
                err(f'jooned.json #{n}: seletusi {len(e)}, oodatud {expected_count(n)}.')
            if any(not str(x).strip() for x in e):
                err(f'jooned.json #{n}: tühi seletus.')

if errors:
    print('VIGU LEITI:')
    for e in errors:
        print(' -', e)
    sys.exit(1)
print('Kõik korras: 64 heksagrammi, 8 trigrammi, joonte tekstid ja seletused vastavad struktuurile.')
