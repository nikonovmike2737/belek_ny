# BELEK NY: Site Structure Canon

**Status:** CURRENT

The public site has exactly eight top-level blocks, in this fixed order:
`hero` -> `ranking` -> `cards` -> `prices` -> `extras` -> `gastro` -> `pdf-download` -> `shortlist`.

The former standalone `booking-readiness` / «Бронирование» block is removed and must not return. Future releases may update content inside these blocks, but must not add, remove, rename or reorder top-level blocks unless the user explicitly changes this canon. `scripts/validate_consistency.py` fails closed on structure drift.
