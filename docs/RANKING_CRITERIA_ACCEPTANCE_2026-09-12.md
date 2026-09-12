# BELEK NY: Ranking Criteria Acceptance 2026-09-12

**Release candidate:** `20260912T191617Z`  
**Scope:** territory size, distinctive extra entertainment, first-line/direct beach criterion, recalculated ranking and related public copy.

## Evidence and semantics

- Territory is non-blocking: `<80k = 0`, `80k-119,999 = +0.1`, `>=120k = +0.2`.
- Distinctive extra entertainment is non-blocking and adds at most `+0.1` when not already reflected in the base score.
- First-line/direct beach is high-weight baseline. Confirmed absence = `-0.5` and mandatory risk disclosure.
- All ten current hotels have supported first-line/direct-beach evidence; no beach penalty is applied in this release.
- Price timestamps remain exactly `2026-09-10T14:00:00+03:00` -> `2026-09-12T00:11:00+03:00`.

## Web desktop

Level A: PASS. Public copy contains no forbidden em/en dash, internal status, decorative token or stale price wording introduced by this change. Ranking, card scores and ranking order are internally consistent.

Level B: PASS. The scoring explanation is concrete, exposes adjustments, avoids unsupported certainty and distinguishes baseline criteria from bonuses.

Level C: PASS. Criteria table is readable and the ranking remains decision-oriented; hotel cards show territory/beach facts without turning the new non-blocking criteria into hard filters.

Final result: ACCEPTED

## Web mobile

Level A: PASS. Existing mobile navigation/action contract is unchanged.

Level B: PASS. New ranking copy remains compact enough for the existing responsive structure.

Level C: PASS. No action-row, navigation or card interaction geometry was changed by this release.

Final result: ACCEPTED

## PDF

Level A: PASS. Report-version marker is `20260912T191617Z`; PDF is openable, 22 pages, 19 portrait and 3 landscape.

Level B: PASS. The PDF carries the same transparent ranking criteria and recalculated scores as web.

Level C: PASS. All 22 pages rendered at 110 dpi and were reviewed. The new criteria table spans pages 1-2 without clipping; hotel cards, landscape price section, service/gastronomy tables and final shortlist remain readable. No overlap, clipped text, broken glyphs or black boxes were found.

Final result: ACCEPTED

## Ranking result

1. Spice 9.6
2. Voyage 9.4
3. Susesi 9.2
4. Bellis 9.2
5. Rixos Park 8.7
6. Pine Beach 8.7
7. Papillon Zeugma 8.5
8. Xanadu 8.4
9. Limak Arcadia 8.1
10. Limak Atlantis 7.4

Bellis rises from 8.9 to 9.2 because of `+0.2` territory and `+0.1` zoo/horse-riding entertainment. Bellis stays the control benchmark, so the replacement shortlist remains Spice, Voyage and Susesi.
