#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / 'index.html').read_text(encoding='utf-8')

class PublicTextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts = []
        self.attrs = []
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in {'script','style','noscript','template'}:
            self.skip += 1
        if not self.skip:
            d = dict(attrs)
            for key in ('aria-label','title','alt'):
                val = d.get(key)
                if val:
                    self.attrs.append(val)
    def handle_endtag(self, tag):
        if tag.lower() in {'script','style','noscript','template'} and self.skip:
            self.skip -= 1
    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data)

p = PublicTextParser(); p.feed(html)
public = ' '.join(p.parts + p.attrs)
public = re.sub(r'\s+', ' ', public).strip()

# Formal punctuation and service hygiene.
for ch, name in [('—','em dash'),('–','en dash'),('·','middle dot'),('→','decorative right arrow')]:
    assert ch not in public, f'public copy contains forbidden {name}: {ch}'

for emoji in ('👧','🎾','🏊','💶','✅','⚠','❌','❓'):
    assert emoji not in public, f'public copy contains decorative emoji: {emoji}'

for internal in ('UNKNOWN','NOT_APPLICABLE','HISTORICAL_SNAPSHOT','report_version'):
    assert internal not in public, f'public copy exposes internal status: {internal}'

for stale in ('с прошлого запроса', 'Важно отметить', 'важно отметить', 'Таким образом', 'таким образом', 'В целом можно сказать', 'в целом можно сказать'):
    assert stale not in public, f'public copy contains stale/AI-style phrase: {stale}'

# Slash-separated user copy is prohibited when normal Russian wording is available.
assert not re.search(r'\s/\s', public), 'public copy contains spaced slash construction'

# Current product terminology and interaction contract.
for label in ('Рейтинг','Отели','Стоимость','Услуги','Еда','Рекомендация'):
    assert label in public, f'canonical navigation term missing: {label}'
assert 'Скачать PDF' in public, 'specific PDF CTA missing'
assert public.count('Отзывы') >= 20, 'Reviews action missing from card states'
assert public.count('Сайт отеля') >= 20, 'Hotel site action missing from card states'
assert 'Сравнить' not in public and 'В сравнении' not in public, 'compare copy must stay removed'

# Hero family composition remains explicit and scannable.
family_pattern = r'2 взрослых\s*<br\s*/?>\s*с 1 ребёнком\s*<br\s*/?>\s*с 2 детьми'
assert re.search(family_pattern, html, re.I), 'hero family composition must be three lines'

print('{"status":"PASS","communication_level_a":"PASS","public_copy":"formal-service-hygiene"}')
