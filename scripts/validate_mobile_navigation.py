#!/usr/bin/env python3
from pathlib import Path
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
    ("#cards", "Карточки"),
    ("#prices", "Номера"),
    ("#extras", "Доплаты"),
    ("#gastro", "Еда"),
    ("#shortlist", "Выбор"),
]
menu_m = re.search(r'<nav class="mobile-menu-panel" id="mobileMenu"[^>]*>(.*?)</nav>', html, re.I | re.S)
assert menu_m, "mobile navigation markup missing"
menu = menu_m.group(1)
for href, label in expected:
    assert f'href="{href}"' in menu and f'>{label}</a>' in menu, f"mobile navigation item missing: {label}"
    assert re.search(rf'<section\b[^>]*id=["\']{re.escape(href[1:])}["\']', html, re.I), f"mobile navigation target missing: {href}"

compact = re.sub(r"\s+", "", html)
assert 'html{scroll-padding-top:76px}' in compact, "mobile scroll-padding-top must protect section start from sticky header"
assert '.section[id]{scroll-margin-top:76px}' in compact, "mobile section scroll-margin-top missing"
assert '.mobile-menu-toggle{display:inline-flex' in compact, "mobile burger must be visible on mobile"
assert '.nav{display:none}' in compact, "desktop navigation must be hidden on mobile"
assert '@mediaprint{.mobile-menu-toggle,.mobile-menu-panel{display:none!important}}' in compact, "mobile menu must be hidden in print/PDF"

assert "if(event.target.closest('a'))closeMenu()" in compact, "mobile menu must close after section selection"
assert "if(event.key==='Escape')closeMenu()" in compact, "mobile menu must close on Escape"
assert "window.matchMedia('(min-width:681px)')" in html, "mobile menu must reset when returning to desktop width"

print('{"status":"PASS","mobile_navigation":true,"items":6,"header_offset_px":76}')
