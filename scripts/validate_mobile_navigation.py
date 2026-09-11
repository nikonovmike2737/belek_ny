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

# Desktop and mobile navigation must use the same labels for the same anchors.
desktop_m = re.search(r'<nav class="nav"[^>]*>(.*?)</nav>', html, re.I | re.S)
assert desktop_m, "desktop navigation markup missing"
desktop = desktop_m.group(1)
for href, label in expected:
    assert f'href="{href}"' in desktop and f'>{label}</a>' in desktop, f"desktop navigation item missing: {label}"

# Favicon must be the approved family New Year beach image, embedded so Pages has no binary-file dependency.
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
assert '@mediaprint{.mobile-menu-toggle,.mobile-menu-panel{display:none!important}}' in compact, "mobile menu must be hidden in print/PDF"

# Reviews and Compare are a fixed two-button row inside every hotel card.
# Reviews must be first, Compare second, and both stay left-aligned and horizontal on mobile.
review_compare_pairs = re.findall(
    r'<div class="compare-actions">\s*<a class="reviews-link"[^>]*>.*?<span>Отзывы</span></a>\s*<button class="compare-toggle"[^>]*>＋ Сравнить</button>\s*</div>',
    html,
    re.I | re.S,
)
assert len(review_compare_pairs) == 10, f"expected 10 Reviews+Compare action pairs, found {len(review_compare_pairs)}"
assert '.compare-actions{display:flex;flex-direction:row;align-items:center;justify-content:flex-start' in compact, "Reviews and Compare must be horizontal and left-aligned"
assert '@media(max-width:620px){.compare-row{display:flex;flex-direction:row;align-items:center;justify-content:flex-start' in compact, "mobile compare row must remain horizontal and left-aligned"
assert '.compare-actions{display:flex;flex-direction:row;justify-content:flex-start;align-items:center;width:100%;flex-wrap:nowrap}' in compact, "mobile Reviews and Compare must never stack"

assert "if(event.target.closest('a'))closeMenu()" in compact, "mobile menu must close after section selection"
assert "if(event.key==='Escape')closeMenu()" in compact, "mobile menu must close on Escape"
assert "window.matchMedia('(min-width:681px)')" in html, "mobile menu must reset when returning to desktop width"

print('{"status":"PASS","mobile_navigation":true,"items":6,"header_offset_px":76,"labels":"current","favicon":"approved","review_compare_row":"horizontal-left"}')
