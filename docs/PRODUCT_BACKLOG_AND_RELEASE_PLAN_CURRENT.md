# BELEK NY: Product Backlog and Release Plan

**Status:** CURRENT  
**Operating canon:** `docs/PRODUCT_OPERATING_PRINCIPLES_CURRENT.md`  
**Ranking canon:** `docs/HOTEL_RANKING_CRITERIA_CURRENT.md`

The current product goal is to improve the booking decision for 25.12.2026-03.01.2027 without unnecessary infrastructure or release churn.

## P0

1. **Ranking criteria release - shipping now.** Add territory size, distinctive extra entertainment and high-weight first-line/direct-beach semantics to the ranking. Recalculate all ten hotels, expose the criteria in HTML/PDF, and flag any non-first-line hotel in risks. This increment must not change price clocks.
2. **Comparable price truth.** Continue exact comparable price coverage for all ten hotels and three occupancies, starting with historical/missing/weak rows. No guessed prices and no generic crawler before a bounded source pilot proves value.
3. **Twice-daily monitoring correctness.** Keep 09:00 and 21:00 Europe/Moscow checks with `NO DELTA = NO WRITE = NO COMMIT = NO DEPLOY`.
4. **Decision-critical uncertainty closure.** Resolve only facts that can materially change the shortlist: New Year programme, winter kids club/pools, adult sport, common evening spaces, mandatory gala/board terms.
5. **Evidence-driven reranking.** Recalculate only when verified facts or explicit user preference changes materially affect the decision.

## P1

1. Build booking-readiness for the final three alternatives: exact room category, board, mandatory gala charges, current comparable total, payment/cancellation terms and verified booking path.
2. Maintain official-site and review-link health.
3. Resolve gastronomy only when it becomes a real tie-breaker.
4. Keep HTML/PDF/mobile consistency and A+B+C as release gates.
5. Pilot additional supplier/parser integrations only for a measured price-coverage gap.

## P2

- generic crawler platform;
- recommendation-engine rewrite;
- new VPS/paid APIs/licences before measured need;
- broad content refresh that cannot change the booking decision;
- docs/repository cleanup as a standalone release.

## Current meaningful increments

### Increment R: ranking criteria expansion

**Hypothesis:** territory, distinctive extra entertainment and direct beach access improve the ranking for this family's actual stay without creating blocking filters.

**Minimum scope:** all ten current hotels, transparent score correction, risk rule for non-first-line hotels, HTML + PDF + ranking canon.

**PASS:** every hotel has a supported territory/beach state, corrections are deterministic, no double counting, ranking/cards/shortlist are internally consistent, price timestamps remain unchanged, HTML/PDF acceptance passes.

**Excluded:** redesign, new recommender engine, new paid data source.

### Increment A: decision-quality price truth uplift

Continue immediately after this release. The ranking release does not cancel or block it.

### Increment B: top-candidate uncertainty closure

Continue after the highest-value price gaps and in parallel where research is cheap.

### Increment C: final-three booking readiness

Start once shortlist uncertainty is sufficiently low.

## Release economy

One meaningful product release = one production commit containing all changed HTML, PDF, docs, state and code. No docs-only, trigger-only, timestamp-only, housekeeping or automatic follow-up sync commits.
