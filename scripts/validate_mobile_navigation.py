#!/usr/bin/env python3
from pathlib import Path
import base64
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")

assert html.count('id="mobileMenuToggle"') == 1, "mobile burger button missing or duplicated"
assert html.count('id="mobileMenu"') == 1, "mobile navigation panel missing or duplicated"
assert html.count('id="mobile-menu-script"') == 1, "mobile navigation script missing or duplicated"
assert 'class="mobile-menu-toggle"' in html, "mobile burger class missing"
assert 'aria-expanded="false"' in html, "mobile burger aria-expanded missing"
assert 'aria-controls="mobileMenu"' in html, "mobile burger aria-controls missing"
assert 'aria-label="Открыть меню"' in html, "mobile burger accessible label missing"

expected = [
    ("#ranking", "Рейтинг"),
    ("#cards", "Отели"),
    ("#prices", "Стоимость"),
    ("#extras", "Услуги"),
    ("#gastro", "Еда"),
    ("#shortlist", "Рекомендация"),
]
menu_m = re.search(r'<nav class="mobile-menu-panel" id="mobileMenu"[^>]*>(.*?)</nav>', html, re.I | re.S)
assert menu_m, "mobile navigation markup missing"
menu = menu_m.group(1)
for href, label in expected:
    assert f'href="{href}"' in menu and f'>{label}</a>' in menu, f"mobile navigation item missing: {label}"
    assert re.search(rf'<section\b[^>]*id=["\']{re.escape(href[1:])}["\']', html, re.I), f"mobile navigation target missing: {href}"

desktop_m = re.search(r'<nav class="nav"[^>]*>(.*?)</nav>', html, re.I | re.S)
assert desktop_m, "desktop navigation markup missing"
desktop = desktop_m.group(1)
for href, label in expected:
    assert f'href="{href}"' in desktop and f'>{label}</a>' in desktop, f"desktop navigation item missing: {label}"

favicon_m = re.search(r'<link\s+rel="icon"\s+type="image/png"\s+sizes="64x64"\s+href="data:image/png;base64,([A-Za-z0-9+/=]+)"\s*/?>', html, re.I)
assert favicon_m, "approved embedded favicon missing"
favicon_bytes = base64.b64decode(favicon_m.group(1), validate=True)
assert favicon_bytes.startswith(b'\x89PNG\r\n\x1a\n'), "favicon must be PNG"
assert hashlib.sha256(favicon_bytes).hexdigest() == "c5021df59ae2bea0ff4808dd20cdd028b7aab51a8168f5befcf64c0ba3e74b54", "favicon does not match approved artwork"

compact = re.sub(r"\s+", "", html)
assert 'html{scroll-padding-top:76px}' in compact, "mobile scroll-padding-top must protect section start from sticky header"
assert '.section[id]{scroll-margin-top:76px}' in compact, "mobile section scroll-margin-top missing"
assert '.mobile-menu-toggle{display:inline-flex' in compact, "mobile burger must be visible on mobile"
assert '.nav{display:none}' in compact, "desktop navigation must be hidden on mobile"
assert '.mobile-menu-toggle,.mobile-menu-panel{display:none!important}' in compact, "mobile menu must be hidden in print/PDF"

# Hotel cards have exactly three user actions in one row in both states:
# Details/Collapse, Reviews, Hotel site. Interactive comparison is removed.
assert 'compare-toggle' not in html, "Compare button must be removed"
assert 'compareDock' not in html and 'compareModal' not in html, "Compare dock/modal must be removed"
assert '＋ Сравнить' not in html and '✓ В сравнении' not in html, "Compare copy must be removed"
assert '.compare-row' not in html and '.compare-dock' not in html and '.compare-modal' not in html, "Compare CSS must be removed"

cards = re.findall(r'<article\b[^>]*class=["\'][^"\']*\bhotel-card\b[^"\']*["\'][^>]*>.*?</article>', html, re.I | re.S)
assert len(cards) == 10, f"expected 10 hotel cards, found {len(cards)}"
for card in cards:
    collapsed = re.search(r'<div class="hotel-actions hotel-actions-collapsed">(.*?)</div>', card, re.I | re.S)
    expanded = re.search(r'<div class="hotel-actions hotel-actions-expanded">(.*?)</div>', card, re.I | re.S)
    assert collapsed and expanded, "hotel action rows missing"
    c = collapsed.group(1)
    e = expanded.group(1)
    assert re.search(r'>Подробнее</button>.*class="reviews-link".*>Отзывы</span></a>.*>Сайт отеля</a>', c, re.I | re.S), "collapsed actions must be Подробнее, Отзывы, Сайт отеля"
    assert re.search(r'>Свернуть</button>.*class="reviews-link".*>Отзывы</span></a>.*>Сайт отеля</a>', e, re.I | re.S), "expanded actions must be Свернуть, Отзывы, Сайт отеля"
    for row in (c, e):
        assert row.count('class="reviews-link"') == 1, "each action row must have one Reviews link"
        assert row.count('class="btn primary hotel-site-link"') == 1, "each action row must have one Hotel site link"
        assert 'tripadvisor.ru/' in row, "Reviews must open Russian Tripadvisor"
        assert 'target="_blank"' in row, "external card actions must open in new tab"

assert '.hotel-actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));' in compact, "hotel actions must use a fixed three-column row"
assert '@media(max-width:620px){.hotel-actions{grid-template-columns:repeat(3,minmax(0,1fr));' in compact, "mobile hotel actions must stay in one three-column row"
assert 'white-space:nowrap' in compact, "button labels must stay on one line"
assert '.hotel-card.is-open>.hotel-body>.hotel-actions-collapsed{display:none}' in compact, "collapsed row must hide when card is open"
assert "details.open=!details.open" in compact, "hotel details toggle logic missing"

assert "if(event.target.closest('a'))closeMenu()" in compact, "mobile menu must close after section selection"
assert "if(event.key==='Escape')closeMenu()" in compact, "mobile menu must close on Escape"
assert "window.matchMedia('(min-width:681px)')" in html, "mobile menu must reset when returning to desktop width"

print('{"status":"PASS","mobile_navigation":true,"items":6,"header_offset_px":76,"labels":"current","favicon":"approved","hotel_actions":"three-horizontal","compare":"removed","mobile_390":"required"}')
