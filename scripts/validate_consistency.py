#!/usr/bin/env python3
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
registry = json.loads((ROOT / "data" / "room-category-registry.json").read_text(encoding="utf-8"))
state_path = ROOT / "data" / "current-price-state.json"
state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else None

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

# Hero family composition must stay readable and must not regress to a
# semicolon-separated machine-like line.
assert "2 взрослых<br>с 1 ребёнком<br>с 2 детьми" in html, "hero family composition must be three separate lines"
assert "2 взрослых; с 1 ребёнком; с 2 детьми" not in html, "semicolon-separated family composition is forbidden"

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
    "warnings": warnings
}, ensure_ascii=False))
