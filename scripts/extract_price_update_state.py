#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import json
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"
OUT = ROOT / "data" / "price-update-state.json"

html = HTML.read_text(encoding="utf-8")

legend_m = re.search(
    r'<div\b([^>]*\bclass=["\'][^"\']*\bprice-trend-legend\b[^"\']*["\'][^>]*)>',
    html,
    re.I | re.S,
)
if not legend_m:
    raise SystemExit("price trend legend missing")
attrs = legend_m.group(1)

prev_m = re.search(r'data-previous-price-update-at=["\']([^"\']+)["\']', attrs, re.I)
curr_m = re.search(r'data-current-price-update-at=["\']([^"\']+)["\']', attrs, re.I)
if not prev_m or not curr_m:
    raise SystemExit("price update timestamp attributes missing")

previous = prev_m.group(1)
current = curr_m.group(1)
prev_dt = datetime.fromisoformat(previous)
curr_dt = datetime.fromisoformat(current)
if prev_dt.tzinfo is None or curr_dt.tzinfo is None:
    raise SystemExit("price update timestamps must be timezone-aware")
if not prev_dt < curr_dt:
    raise SystemExit("previous price update must be older than current price update")

version_m = re.search(r'data-report-version=["\']([^"\']+)["\']', html, re.I)
if not version_m:
    raise SystemExit("report version missing")

state = {
    "schema_version": "1.0",
    "timezone": "Europe/Moscow",
    "previous_price_update_at": previous,
    "current_price_update_at": current,
    "previous_display": prev_dt.strftime("%d.%m, %H:%M"),
    "current_display": curr_dt.strftime("%d.%m, %H:%M"),
    "report_version": version_m.group(1),
    "source": "canonical HTML price-trend-legend attributes",
}

OUT.parent.mkdir(parents=True, exist_ok=True)
serialized = json.dumps(state, ensure_ascii=False, indent=2) + "\n"
old = OUT.read_text(encoding="utf-8") if OUT.exists() else None
if old != serialized:
    OUT.write_text(serialized, encoding="utf-8")
    print(f"updated {OUT}")
else:
    print(f"unchanged {OUT}")
