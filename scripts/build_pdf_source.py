#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "index.html"
OUT = ROOT / "report" / "BELEK_NY_REPORT_SOURCE.html"
OUT.parent.mkdir(parents=True, exist_ok=True)

html = SRC.read_text(encoding="utf-8")

# Keep the canonical report content and embedded images, but make the stored
# source deterministic and print-oriented. The main HTML owns the detailed
# editorial print layout; this block only enforces generic print safety.
print_css = """
<style id="belek-print-source-style">
@page { size: A4; margin: 14mm 13mm 16mm; }
@media print {
  body { background: #fff !important; color: #17211d !important; }
  button, dialog, input, select, textarea, .compare-control, .compare-actions,
  .sticky-compare, .compare-dock, #pdf-download, .hotel-actions { display: none !important; }
  details { display: block !important; }
  details > * { display: block !important; }
  table { width: 100%; border-collapse: collapse; }
  .hotel-photo, .pricing-cards, .detail-grid section, .proscons > div { break-inside: avoid; }
  img { max-width: 100%; }
}
</style>
"""
if 'id="belek-print-source-style"' not in html:
    html = re.sub(r"</head>", print_css + "</head>", html, count=1, flags=re.I)

# PDF source must not depend on interactive execution.
html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.I | re.S)
OUT.write_text(html, encoding="utf-8")
print(f"built {OUT} ({OUT.stat().st_size} bytes)")
