#!/usr/bin/env python3
from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "room-category-registry.json"
STATE = ROOT / "data" / "current-price-state.json"

reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
if STATE.exists():
    raise SystemExit(0)

room_fields = {name: i for i, name in enumerate(reg["room_fields"])}
source_fields = {name: i for i, name in enumerate(reg["sources_fields"])}
quotes = []
for room_id, room in enumerate(reg["rooms"]):
    src = reg["sources"][room[room_fields["source_id"]]]
    source_url = src[source_fields["url"]]
    checked_at = room[room_fields["checked_at"]]
    for occ in ("2A", "2A1C5", "2A2C5_7"):
        compatibility = room[room_fields[occ]]
        availability = "NOT_APPLICABLE" if compatibility == "NOT_APPLICABLE" else "UNKNOWN"
        confidence = "HIGH" if availability == "NOT_APPLICABLE" else "LOW"
        quotes.append({
            "room_id": room_id,
            "occupancy": occ,
            "availability": availability,
            "currency": None,
            "nightly_price": None,
            "total_stay_price": None,
            "mandatory_gala_fees": None,
            "source": source_url,
            "checked_at": checked_at,
            "confidence": confidence,
        })

state = {
    "schema_version": "2.0",
    "report_version": reg["report_version"],
    "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "date_window": reg["date_window"],
    "quotes": quotes,
    "legacy_snapshot": {
        "date": "2026-09-04",
        "status": "HISTORICAL_SNAPSHOT_NOT_LIVE",
        "currency": "EUR",
        "note": "Legacy values in the supplied report are historical comparison context only, not current monitored room-only quotes."
    }
}
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"created {STATE} with {len(quotes)} quote keys")