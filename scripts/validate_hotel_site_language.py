#!/usr/bin/env python3
from pathlib import Path
import html as html_lib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
data = json.loads((ROOT / "data" / "hotel-site-links.json").read_text(encoding="utf-8"))

EXPECTED_PRIORITY = ["ru", "en", "de", "tr"]
assert data.get("language_policy") == "ru-en-de-tr-fallback", "hotel site language policy must be ru-en-de-tr-fallback"
assert data.get("language_priority") == EXPECTED_PRIORITY, "hotel site language priority must be ru -> en -> de -> tr"
rows = data.get("hotels", [])
assert len(rows) == 10, f"expected 10 hotel links, found {len(rows)}"
assert len({r.get("hotel") for r in rows}) == 10, "duplicate hotel names in site map"

site_map = {}
selected_counts = {lang: 0 for lang in EXPECTED_PRIORITY}
for row in rows:
    hotel = row.get("hotel")
    url = row.get("url")
    selected = row.get("selected_language")
    assert hotel and url, "hotel site row missing hotel/url"
    assert row.get("identity_verified") is True, f"{hotel}: hotel identity not verified"
    assert row.get("preferred_language") == "ru", f"{hotel}: absolute language preference must start with ru"
    assert selected in EXPECTED_PRIORITY, f"{hotel}: selected_language must be one of {EXPECTED_PRIORITY}"
    assert row.get("language_verified") is True, f"{hotel}: selected language route not verified"
    selected_counts[selected] += 1
    site_map[hotel] = url

cards = re.findall(
    r'<article\b[^>]*class=["\'][^"\']*\bhotel-card\b[^"\']*["\'][^>]*>.*?</article>',
    html,
    re.I | re.S,
)
assert len(cards) == 10, f"expected 10 hotel cards, found {len(cards)}"

for card in cards:
    name_m = re.search(r'<div class=["\']photo-caption["\']>.*?<h3>(.*?)</h3>', card, re.I | re.S)
    assert name_m, "hotel card title missing"
    name = html_lib.unescape(re.sub(r'<[^>]+>', '', name_m.group(1))).strip()
    expected = site_map.get(name)
    assert expected, f"{name}: no canonical hotel site URL"
    anchors = re.findall(r'<a\b([^>]*)>Сайт отеля</a>', card, re.I | re.S)
    assert len(anchors) == 2, f"{name}: expected two Сайт отеля links"
    for attrs in anchors:
        href_m = re.search(r'href=["\']([^"\']+)["\']', attrs, re.I)
        assert href_m and href_m.group(1) == expected, f"{name}: card URL differs from canonical selected-language URL"

print(json.dumps({
    "status": "PASS",
    "hotels": len(rows),
    "language_priority": EXPECTED_PRIORITY,
    "selected_languages": selected_counts,
}, ensure_ascii=False))
