#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlparse
import html as html_lib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
data = json.loads((ROOT / "data" / "hotel-site-links.json").read_text(encoding="utf-8"))

assert data.get("language_policy") == "ru-first", "hotel site language policy must be ru-first"
rows = data.get("hotels", [])
assert len(rows) == 10, f"expected 10 hotel links, found {len(rows)}"
assert len({r.get("hotel") for r in rows}) == 10, "duplicate hotel names in site map"

site_map = {}
for row in rows:
    hotel = row.get("hotel")
    url = row.get("url")
    assert hotel and url, "hotel site row missing hotel/url"
    assert row.get("identity_verified") is True, f"{hotel}: hotel identity not verified"
    if row.get("russian_available") is True:
        assert row.get("preferred_language") == "ru", f"{hotel}: Russian must be preferred"
        assert row.get("language_verified") is True, f"{hotel}: Russian language route not verified"
        path_parts = [p.lower() for p in urlparse(url).path.split("/") if p]
        assert "ru" in path_parts, f"{hotel}: Russian is available but URL is not a /ru route"
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
        assert href_m and href_m.group(1) == expected, f"{name}: card URL differs from canonical Russian-first URL"

print(json.dumps({"status":"PASS","hotels":len(rows),"russian_first":sum(1 for r in rows if r.get("russian_available"))}, ensure_ascii=False))
