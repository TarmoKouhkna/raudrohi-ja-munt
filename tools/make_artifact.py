#!/usr/bin/env python3
"""Teeb repo index.html-ist claude.ai artefakti versiooni (vt CLAUDE.md, „claude.ai artefakt“).

Artefaktis lisab claude.ai ise <!doctype>, <html>, <head>, <body> ja põhistiilid, seega
eemaldatakse need koos ainult GitHubi versioonile mõeldud päisesiltidega (PWA, eelvaade).

Kasutus:  python3 tools/make_artifact.py VÄLJUNDFAIL.html
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / 'index.html').read_text(encoding='utf-8')

start = src.index('<title>')
head_end = src.index('</head>')
body_start = src.index('<body>') + len('<body>')
body_end = src.rindex('</body>')

head = src[start:head_end]
title_end = head.index('</title>') + len('</title>')
rest = head[title_end:]
# Jäta alles ainult fondid ja rakenduse stiilid (alates esimesest <link rel="preconnect">).
rest = rest[rest.index('<link rel="preconnect"'):]

out = head[:title_end] + '\n<meta name="claude:viewport-fit-sides" content="cover">\n' + rest.rstrip() + '\n' + src[body_start:body_end].strip() + '\n'
Path(sys.argv[1]).write_text(out, encoding='utf-8')
print(f'Kirjutatud: {sys.argv[1]} ({len(out.encode())} baiti)')
