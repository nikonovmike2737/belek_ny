#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
registry = json.loads((ROOT / "data" / "room-category-registry.json").read_text(encoding="utf-8"))
state_path = ROOT / "data" / "current-price-state.json"
state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else None

m = re.search(r'data-report-version=["\']([^"\']+)', html)
assert m, "HTML report version marker missing"
version = m.group(1)
assert registry.get("report_version") == version, (registry.get("report_version"), version)
if state:
    assert state.get("report_version") == version, (state.get("report_version"), version)
assert 'id="pdf-download"' in html or "id='pdf-download'" in html, "PDF download block missing"
assert './belek_new_year_comparison_2026_2027_current.pdf' in html, "current PDF href missing"
assert re.search(r'<a[^>]+download', html, re.I), "download attribute missing"
assert "HISTORICAL_SNAPSHOT" in html, "historical price labeling missing"
print(json.dumps({"status":"PASS","report_version":version,"rooms":len(registry.get("rooms", [])),"quotes":len(state.get("quotes", [])) if state else 0}, ensure_ascii=False))