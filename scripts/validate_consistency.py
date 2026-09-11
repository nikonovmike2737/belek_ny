#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import html as html_lib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
registry = json.loads((ROOT / "data" / "room-category-registry.json").read_text(encoding="utf-8"))
state_path = ROOT / "data" / "current-price-state.json"
state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else None
price_state_path = ROOT / "data" / "price-update-state.json"
price_state = json.loads(price_state_path.read_text(encoding="utf-8")) if price_state_path.exists() else None
site_path = ROOT / "data" / "hotel-site-links.json"
site_data = json.loads(site_path.read_text(encoding="utf-8")) if site_path.exists() else None
acceptance_path = ROOT / "docs" / "EDITORIAL_COMMUNICATION_ACCEPTANCE_CURRENT.md"

m = re.search(r'data-report-version=["\']([^"\']+)', html)
assert m, "HTML report version marker missing"
version = m.group(1)
assert 'id="pdf-download"' in html or "id='pdf-download'" in html, "PDF download block missing"
assert './belek_new_year_comparison_2026_2027_current.pdf' in html, "current PDF href missing"
assert re.search(r'<a[^>]+download', html, re.I), "download attribute missing"
assert "HISTORICAL_SNAPSHOT" in html, "historical price labeling missing"

# Level A, automated subset. Only user-visible text is checked for editorial
# symbols/statuses; scripts/styles and the print-only machine marker are removed.
assert "—" not in html, "public HTML contains forbidden em dash"
assert "–" not in html, "public HTML contains forbidden en dash"
public = re.sub(r'<script\b[^>]*>.*?</script>', ' ', html, flags=re.I | re.S)
public = re.sub(r'<style\b[^>]*>.*?</style>', ' ', public, flags=re.I | re.S)
public = re.sub(r'<[^>]*id=["\']pdf-report-version-marker["\'][^>]*>.*?</[^>]+>', ' ', public, flags=re.I | re.S)
public = html_lib.unescape(re.sub(r'<[^>]+>', ' ', public))
public = re.sub(r'\s+', ' ', public)
for token in ["·", "→", "👧", "🎾", "🏊", "💶", "✅", "⚠", "❌", "❓"]:
    assert token not in public, f"public copy contains decorative symbol: {token}"
for token in ["UNKNOWN", "NOT_APPLICABLE", "report_version", "HISTORICAL_SNAPSHOT"]:
    assert token not in public, f"public copy exposes internal status: {token}"
assert "Изменение с прошлого запроса" not in public, "stale price-trend wording is forbidden"
assert "Сравнить" not in public and "В сравнении" not in public, "compare copy must stay removed"

family_pattern = r"2 взрослых\s*<br\s*/?>\s*с 1 ребёнком\s*<br\s*/?>\s*с 2 детьми"
assert re.search(family_pattern, html, re.I), "hero family composition must be three separate lines"
assert "2 взрослых; с 1 ребёнком; с 2 детьми" not in html, "semicolon-separated family composition is forbidden"

# Hotel card actions: exactly three actions in one row in both states.
assert site_data is not None, "data/hotel-site-links.json missing"
site_rows = site_data.get("hotels", [])
assert len(site_rows) == 10, f"expected 10 canonical hotel site links, found {len(site_rows)}"
site_map = {row["hotel"]: row["url"] for row in site_rows}
assert len(site_map) == 10, "hotel site map contains duplicate hotel names"
assert all(row.get("identity_verified") is True for row in site_rows), "all hotel site links must be identity-verified"

assert 'compare-toggle' not in html, "Compare button must be removed"
assert 'compareDock' not in html and 'compareModal' not in html, "Compare dock/modal must be removed"
assert '.compare-row' not in html and '.compare-dock' not in html and '.compare-modal' not in html, "Compare CSS must be removed"

cards = re.findall(r'<article\b[^>]*class=["\'][^"\']*\bhotel-card\b[^"\']*["\'][^>]*>.*?</article>', html, re.I | re.S)
assert len(cards) == 10, f"expected 10 hotel cards, found {len(cards)}"
for card in cards:
    name_m = re.search(r'<div class=["\']photo-caption["\']>.*?<h3>(.*?)</h3>', card, re.I | re.S)
    assert name_m, "hotel card title missing"
    hotel_name = html_lib.unescape(re.sub(r'<[^>]+>', '', name_m.group(1))).strip()
    assert hotel_name in site_map, f"hotel card has no verified official-site mapping: {hotel_name}"
    expected_url = site_map[hotel_name]

    collapsed = re.search(r'<div class=["\']hotel-actions hotel-actions-collapsed["\']>(.*?)</div>', card, re.I | re.S)
    expanded = re.search(r'<div class=["\']hotel-actions hotel-actions-expanded["\']>(.*?)</div>', card, re.I | re.S)
    assert collapsed and expanded, f"{hotel_name}: action rows missing"
    c, e = collapsed.group(1), expanded.group(1)
    assert re.search(r'>\s*Подробнее\s*</button>.*class=["\']reviews-link["\'].*>\s*Отзывы\s*</span>\s*</a>.*>\s*Сайт отеля\s*</a>', c, re.I | re.S), f"{hotel_name}: collapsed actions must be Подробнее, Отзывы, Сайт отеля"
    assert re.search(r'>\s*Свернуть\s*</button>.*class=["\']reviews-link["\'].*>\s*Отзывы\s*</span>\s*</a>.*>\s*Сайт отеля\s*</a>', e, re.I | re.S), f"{hotel_name}: expanded actions must be Свернуть, Отзывы, Сайт отеля"

    for row in (c, e):
        assert row.count('class="reviews-link"') == 1, f"{hotel_name}: each action row needs one Reviews link"
        assert 'tripadvisor.ru/' in row, f"{hotel_name}: Reviews must use Russian Tripadvisor"
        review_m = re.search(r'<a\b([^>]*)class=["\']reviews-link["\'][^>]*>', row, re.I | re.S)
        if not review_m:
            review_m = re.search(r'<a\b([^>]*class=["\']reviews-link["\'][^>]*)>', row, re.I | re.S)
        assert review_m, f"{hotel_name}: Reviews anchor missing"
        attrs = review_m.group(1)
        assert re.search(r'target=["\']_blank["\']', attrs, re.I), f"{hotel_name}: Reviews must open new tab"

        site_anchors = re.findall(r'<a\b([^>]*)>\s*Сайт отеля\s*</a>', row, re.I | re.S)
        assert len(site_anchors) == 1, f"{hotel_name}: each action row needs one Hotel site link"
        attrs = site_anchors[0]
        href_m = re.search(r'href=["\']([^"\']+)["\']', attrs, re.I)
        assert href_m and href_m.group(1) == expected_url, f"{hotel_name}: wrong official-site URL"
        assert re.search(r'target=["\']_blank["\']', attrs, re.I), f"{hotel_name}: Hotel site must open new tab"
        rel_m = re.search(r'rel=["\']([^"\']+)["\']', attrs, re.I)
        rel = (rel_m.group(1) if rel_m else "").lower().split()
        assert "noopener" in rel and "noreferrer" in rel, f"{hotel_name}: safe new-tab rel missing"

compact = re.sub(r"\s+", "", html)
assert '.hotel-actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));' in compact, "hotel actions must be a fixed three-column row"
assert '@media(max-width:620px){.hotel-actions{grid-template-columns:repeat(3,minmax(0,1fr));' in compact, "mobile hotel actions must stay in one three-column row"
assert '.hotel-card.is-open>.hotel-body>.hotel-actions-collapsed{display:none}' in compact, "collapsed action row must hide while card is open"
assert "details.open=!details.open" in compact, "hotel details toggle logic missing"

# Price update timestamp state.
legend_m = re.search(r'<div\b([^>]*\bclass=["\'][^"\']*\bprice-trend-legend\b[^"\']*["\'][^>]*)>', html, re.I | re.S)
assert legend_m, "price trend legend missing"
attrs = legend_m.group(1)
prev_m = re.search(r'data-previous-price-update-at=["\']([^"\']+)["\']', attrs, re.I)
curr_m = re.search(r'data-current-price-update-at=["\']([^"\']+)["\']', attrs, re.I)
assert prev_m and curr_m, "price update timestamp attributes missing"
previous_at, current_at = prev_m.group(1), curr_m.group(1)
previous_dt, current_dt = datetime.fromisoformat(previous_at), datetime.fromisoformat(current_at)
assert previous_dt.tzinfo is not None and current_dt.tzinfo is not None, "price timestamps must be timezone-aware"
assert previous_dt < current_dt, "previous price update must be older than current"
previous_display = previous_dt.strftime("%d.%m, %H:%M")
assert html.count(f"Изменение с прошлого обновления цен {previous_display}") == 1, "visible price legend does not match previous timestamp"
assert price_state is not None, "data/price-update-state.json missing"
assert price_state.get("previous_price_update_at") == previous_at, "previous price state differs from HTML"
assert price_state.get("current_price_update_at") == current_at, "current price state differs from HTML"
assert price_state.get("previous_display") == previous_display, "previous display differs from HTML"
assert price_state.get("current_display") == current_dt.strftime("%d.%m, %H:%M"), "current display mismatch"
assert price_state.get("report_version") == version, "price state report version differs from HTML"

# Price arrows: 60 exact comparable cells and visual direction derived from numbers.
style_m = re.search(r'<style id=["\']price-trend-style["\']>(.*?)</style>', html, re.I | re.S)
assert style_m, "price trend style block missing"
trend_style = style_m.group(1)
compact_style = re.sub(r"\s+", "", trend_style).lower()
assert re.search(r'td\[data-price-trend\]\s*\{[^}]*white-space\s*:\s*nowrap', trend_style, re.I | re.S), "price and arrow must stay on one line"
assert "background:none" in compact_style and "border:0" in compact_style, "trend arrows must have no badge background/border"

cells = re.findall(r'<td\b([^>]*\bdata-prev-price-eur=["\'][^"\']+["\'][^>]*)>(.*?)</td>', html, re.I | re.S)
assert len(cells) == 60, f"expected 60 price trend cells, found {len(cells)}"
counts = {"up": 0, "down": 0, "same": 0}
for attrs, body in cells:
    prev = int(re.search(r'data-prev-price-eur=["\']([0-9]+)["\']', attrs, re.I).group(1))
    curr = int(re.search(r'data-current-price-eur=["\']([0-9]+)["\']', attrs, re.I).group(1))
    trend = re.search(r'data-price-trend=["\'](up|down|same)["\']', attrs, re.I).group(1).lower()
    expected = "up" if curr > prev else "down" if curr < prev else "same"
    assert trend == expected, f"trend {trend} does not match {prev} -> {curr}"
    has_up = bool(re.search(r'class=["\'][^"\']*\bprice-trend\b[^"\']*\bup\b[^"\']*["\'][^>]*>\s*↑\s*</span>', body, re.I | re.S))
    has_down = bool(re.search(r'class=["\'][^"\']*\bprice-trend\b[^"\']*\bdown\b[^"\']*["\'][^>]*>\s*↓\s*</span>', body, re.I | re.S))
    if trend == "up": assert has_up and not has_down
    elif trend == "down": assert has_down and not has_up
    else: assert not has_up and not has_down
    counts[trend] += 1

# Manual/editorial gate is a release requirement, not a replacement for checks above.
assert acceptance_path.exists(), "editorial acceptance evidence missing"
acceptance = acceptance_path.read_text(encoding="utf-8")
final_gate = acceptance.split("## 6. Final gate", 1)[-1].split("## 7.", 1)[0]
assert "PENDING" not in final_gate and "Level A: FAIL" not in final_gate and "Level B: FAIL" not in final_gate and "Level C: FAIL" not in final_gate, "editorial acceptance final gate is not green"
assert final_gate.count("Level A: PASS") >= 3 and final_gate.count("Level B: PASS") >= 3 and final_gate.count("Level C: PASS") >= 3, "A/B/C PASS evidence incomplete"
assert final_gate.count("Final result: ACCEPTED") >= 3, "surface acceptance incomplete"

warnings = []
if registry.get("report_version") != version:
    warnings.append(f"registry version {registry.get('report_version')} trails canonical {version}")
if state and state.get("report_version") != version:
    warnings.append(f"price state version {state.get('report_version')} trails canonical {version}")

print(json.dumps({
    "status": "PASS",
    "report_version": version,
    "rooms": len(registry.get("rooms", [])),
    "quotes": len(state.get("quotes", [])) if state else 0,
    "hotel_site_links": len(site_map),
    "hotel_actions": "three-horizontal",
    "compare": "removed",
    "editorial_gate": "A+B+C PASS",
    "price_updates": {"previous": previous_at, "current": current_at},
    "price_trends": counts,
    "warnings": warnings,
}, ensure_ascii=False))
