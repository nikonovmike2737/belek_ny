#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import html as html_lib
import json, re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
registry = json.loads((ROOT / "data" / "room-category-registry.json").read_text(encoding="utf-8"))
state_path = ROOT / "data" / "current-price-state.json"
state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else None
price_update_state_path = ROOT / "data" / "price-update-state.json"
price_update_state = json.loads(price_update_state_path.read_text(encoding="utf-8")) if price_update_state_path.exists() else None
hotel_site_links_path = ROOT / "data" / "hotel-site-links.json"
hotel_site_links = json.loads(hotel_site_links_path.read_text(encoding="utf-8")) if hotel_site_links_path.exists() else None

m = re.search(r'data-report-version=["\']([^"\']+)', html)
assert m, "HTML report version marker missing"
version = m.group(1)
assert 'id="pdf-download"' in html or "id='pdf-download'" in html, "PDF download block missing"
assert './belek_new_year_comparison_2026_2027_current.pdf' in html, "current PDF href missing"
assert re.search(r'<a[^>]+download', html, re.I), "download attribute missing"
assert "HISTORICAL_SNAPSHOT" in html, "historical price labeling missing"

# Public-copy source of truth: no typographic long dashes anywhere in the
# published HTML. Use ordinary punctuation or an ASCII hyphen for ranges.
assert "—" not in html, "public HTML contains forbidden em dash"
assert "–" not in html, "public HTML contains forbidden en dash"

# Hero family composition must stay readable. Accept equivalent HTML break
# syntax (<br>, <br/> or <br />), but never a semicolon-separated line.
family_pattern = r"2 взрослых\s*<br\s*/?>\s*с 1 ребёнком\s*<br\s*/?>\s*с 2 детьми"
assert re.search(family_pattern, html, re.I), "hero family composition must be three separate lines"
assert "2 взрослых; с 1 ребёнком; с 2 детьми" not in html, "semicolon-separated family composition is forbidden"

# Hotel card actions and exact official-site mapping. This is a hard QA gate:
# each card has two actions in both visual states, and the right action must
# open the exact hotel's verified official page in a new tab.
assert hotel_site_links is not None, "data/hotel-site-links.json missing"
site_rows = hotel_site_links.get("hotels", [])
assert len(site_rows) == 10, f"expected 10 canonical hotel site links, found {len(site_rows)}"
site_map = {row["hotel"]: row["url"] for row in site_rows}
assert len(site_map) == 10, "hotel site map contains duplicate hotel names"
assert all(row.get("identity_verified") is True for row in site_rows), "all hotel site links must be identity-verified"

hotel_cards = re.findall(r'<article\b[^>]*class=["\'][^"\']*\bhotel-card\b[^"\']*["\'][^>]*>.*?</article>', html, re.I | re.S)
assert len(hotel_cards) == 10, f"expected 10 hotel cards, found {len(hotel_cards)}"
for card in hotel_cards:
    name_m = re.search(r'<div class=["\']photo-caption["\']>.*?<h3>(.*?)</h3>', card, re.I | re.S)
    assert name_m, "hotel card title missing"
    hotel_name = html_lib.unescape(re.sub(r'<[^>]+>', '', name_m.group(1))).strip()
    assert hotel_name in site_map, f"hotel card has no verified official-site mapping: {hotel_name}"
    expected_url = site_map[hotel_name]

    assert card.count('>Подробнее</button>') == 1, f"{hotel_name}: collapsed action must contain one Подробнее button"
    assert card.count('>Свернуть</button>') == 1, f"{hotel_name}: expanded action must contain one Свернуть button"
    assert card.count('>Сайт отеля</a>') == 2, f"{hotel_name}: official site action must be present in both states"
    assert "Открыть полный разбор" not in card, f"{hotel_name}: old details summary is forbidden"
    assert "Официальный сайт ↗" not in card, f"{hotel_name}: old official-site label is forbidden"
    assert "Дети, зима и услуги ↗" not in card, f"{hotel_name}: old secondary footer action is forbidden"

    site_anchors = re.findall(r'<a\b([^>]*)>Сайт отеля</a>', card, re.I | re.S)
    assert len(site_anchors) == 2, f"{hotel_name}: expected two official-site anchors"
    for attrs in site_anchors:
        href_m = re.search(r'href=["\']([^"\']+)["\']', attrs, re.I)
        target_m = re.search(r'target=["\']([^"\']+)["\']', attrs, re.I)
        rel_m = re.search(r'rel=["\']([^"\']+)["\']', attrs, re.I)
        assert href_m and href_m.group(1) == expected_url, f"{hotel_name}: wrong official-site URL"
        assert target_m and target_m.group(1) == "_blank", f"{hotel_name}: official site must open in a new tab"
        rel = (rel_m.group(1) if rel_m else "").lower().split()
        assert "noopener" in rel and "noreferrer" in rel, f"{hotel_name}: safe new-tab rel attributes missing"

assert html.count('id="hotel-card-actions-style"') == 1, "hotel card action style block missing or duplicated"
assert ".hotel-card.is-open>.hotel-body>.hotel-actions-collapsed{display:none}" in html.replace("\n", ""), "collapsed actions must hide while details are open"
assert "details.open=!details.open" in html.replace(" ", ""), "hotel details toggle logic missing"

# Price update timestamp state. The legend carries both machine-readable
# timestamps, while visible copy shows the previous published price update.
legend_open_m = re.search(
    r'<div\b([^>]*\bclass=["\'][^"\']*\bprice-trend-legend\b[^"\']*["\'][^>]*)>',
    html,
    re.I | re.S,
)
assert legend_open_m, "price trend legend missing"
legend_attrs = legend_open_m.group(1)
prev_time_m = re.search(r'data-previous-price-update-at=["\']([^"\']+)["\']', legend_attrs, re.I)
curr_time_m = re.search(r'data-current-price-update-at=["\']([^"\']+)["\']', legend_attrs, re.I)
assert prev_time_m and curr_time_m, "price update timestamp attributes missing"
previous_price_update_at = prev_time_m.group(1)
current_price_update_at = curr_time_m.group(1)
previous_dt = datetime.fromisoformat(previous_price_update_at)
current_dt = datetime.fromisoformat(current_price_update_at)
assert previous_dt.tzinfo is not None and current_dt.tzinfo is not None, "price update timestamps must be timezone-aware"
assert previous_dt < current_dt, "previous price update must be older than current price update"
previous_display = previous_dt.strftime("%d.%m, %H:%M")
legend_copy = f"Изменение с прошлого обновления цен {previous_display}"
assert html.count(legend_copy) == 1, "price trend legend must show previous price update date/time exactly once"
assert "Изменение с прошлого запроса:" not in html, "old price trend legend copy is forbidden"

assert price_update_state is not None, "data/price-update-state.json missing"
assert price_update_state.get("previous_price_update_at") == previous_price_update_at, "previous price update state differs from canonical HTML"
assert price_update_state.get("current_price_update_at") == current_price_update_at, "current price update state differs from canonical HTML"
assert price_update_state.get("previous_display") == previous_display, "previous price update display differs from canonical HTML"
assert price_update_state.get("current_display") == current_dt.strftime("%d.%m, %H:%M"), "current price update display mismatch"
assert price_update_state.get("report_version") == version, "price update state report version differs from canonical HTML"

# Price trend arrows. Every public price cell stores the previous and current
# comparable value plus the derived direction. The visual arrow must match the
# numeric comparison exactly; unchanged values must stay visually quiet.
style_m = re.search(r'<style id=["\']price-trend-style["\']>(.*?)</style>', html, re.I | re.S)
assert style_m, "price trend style block missing"
trend_style = style_m.group(1)
compact_style = re.sub(r"\s+", "", trend_style).lower()
assert re.search(r'td\[data-price-trend\]\s*\{[^}]*white-space\s*:\s*nowrap', trend_style, re.I | re.S), "price and trend arrow must stay on one line"
assert "border-radius:999px" not in compact_style and "border-radius:50%" not in compact_style, "trend arrows must not have circular styling"
assert "background:rgba(" not in compact_style, "trend arrows must not have a colored background"
assert "border:1px" not in compact_style and "border:0.35mm" not in compact_style, "trend arrows must not have an outline"
assert "background:none" in compact_style, "trend arrows must use a transparent background"
assert "border:0" in compact_style, "trend arrows must have no border"

trend_cells = re.findall(
    r'<td\b([^>]*\bdata-prev-price-eur=["\'][^"\']+["\'][^>]*)>(.*?)</td>',
    html,
    re.I | re.S,
)
assert len(trend_cells) == 60, f"expected 60 price trend cells, found {len(trend_cells)}"
counts = {"up": 0, "down": 0, "same": 0}
for attrs, body in trend_cells:
    prev_m = re.search(r'data-prev-price-eur=["\']([0-9]+)["\']', attrs, re.I)
    curr_m = re.search(r'data-current-price-eur=["\']([0-9]+)["\']', attrs, re.I)
    trend_m = re.search(r'data-price-trend=["\'](up|down|same)["\']', attrs, re.I)
    assert prev_m and curr_m and trend_m, f"price trend metadata incomplete: {attrs[:160]}"
    prev = int(prev_m.group(1))
    curr = int(curr_m.group(1))
    trend = trend_m.group(1).lower()
    expected = "up" if curr > prev else "down" if curr < prev else "same"
    assert trend == expected, f"trend {trend} does not match {prev} -> {curr}"
    has_up = bool(re.search(r'class=["\'][^"\']*\bprice-trend\b[^"\']*\bup\b[^"\']*["\'][^>]*>\s*↑\s*</span>', body, re.I | re.S))
    has_down = bool(re.search(r'class=["\'][^"\']*\bprice-trend\b[^"\']*\bdown\b[^"\']*["\'][^>]*>\s*↓\s*</span>', body, re.I | re.S))
    if trend == "up":
        assert has_up and not has_down, "up cell must contain exactly an up visual and no down visual"
        assert not re.search(r'<br\s*/?>\s*<span[^>]*\bprice-trend\b', body, re.I | re.S), "up arrow must never be placed below the price"
    elif trend == "down":
        assert has_down and not has_up, "down cell must contain exactly a down visual and no up visual"
        assert not re.search(r'<br\s*/?>\s*<span[^>]*\bprice-trend\b', body, re.I | re.S), "down arrow must never be placed below the price"
    else:
        assert not has_up and not has_down, "unchanged cell must not contain a trend arrow"
    counts[trend] += 1

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
    "price_updates": {
        "previous": previous_price_update_at,
        "current": current_price_update_at,
    },
    "price_trends": counts,
    "warnings": warnings
}, ensure_ascii=False))
