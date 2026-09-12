# BELEK NY: Product Backlog and Release Plan

**Status:** CURRENT working plan  
**Base:** `main` at `46a6e72a649f9156608419a933c52c9f4eb73084`  
**Operating canon:** `docs/PRODUCT_OPERATING_PRINCIPLES_CURRENT.md`

This plan is the current prioritization of active BELEK NY work. It does not grant new production authority. Production movement continues to follow the project's explicit release rules and user instructions.

## Current product state

The product compares 10 Belek hotels for 25.12.2026-03.01.2027, 9 nights, for three occupancies: 2 adults; 2 adults + child 5; 2 adults + children 5 and 7.

Current public surfaces are HTML + PDF. The product already has:

- a ranked 10-hotel comparison and shortlist;
- current/historical price presentation with strict comparable-price semantics;
- winter services, family/sport/food evidence and explicit uncertainty;
- three hotel-card actions: details/collapse, Reviews, official hotel site;
- mobile navigation and 390 px contract;
- service-wide editorial/UX gate A+B+C;
- delta-only production policy;
- one-release/one-production-commit rule;
- price monitoring at 09:00 and 21:00 Europe/Moscow.

## Backlog audit through the seven operating principles

| Workstream | Client value now | Autonomy impact | Resource cost | Time to value | Simpler path / reuse | Hypothesis / minimum increment | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Comparable price truth for all 10 hotels / 3 occupancies | Very high | High: fewer manual booking checks | Medium | Fast | Reuse official/public booking paths and approved suppliers; HTTP first | Can current exact comparable coverage be increased without paid infra? Start with hotels whose published basis is historical, missing or weak | P0 |
| Twice-daily price monitoring correctness and delta-only publication | Very high | Very high | Low-medium | Immediate/ongoing | Existing automation + existing state/diff rules | 09:00/21:00 checks catch meaningful changes without no-delta commits/Actions churn | P0 |
| Decision-critical uncertainty closure for top candidates | High | Medium | Low-medium | Fast | Target only facts able to change shortlist: NY programme, winter kids club/pools, tennis, shared evening spaces, mandatory gala/board terms | Can 3-5 highest-impact unknowns be confirmed or falsified and materially sharpen the shortlist? | P0 |
| Evidence-driven ranking/shortlist refresh | High when evidence changes | Medium | Low | Fast | Existing scoring/recommendation surface; no new recommender system | New verified facts should change ranking only when decision impact is material | P0 conditional |
| Booking-readiness facts for final 3 hotels | High, especially as booking approaches | Medium | Medium | Medium | Official terms + approved suppliers; narrow to shortlist | Can we produce exact room/occupancy/board/gala/cancellation basis sufficient for a booking decision? | P1 |
| Official site + TripAdvisor link health | Medium | High | Low | Fast | Simple HTTP checks; reuse current link registry | Keep user paths actionable without touching ranking/price clocks | P1 ongoing |
| Gastronomy evidence for specific requested dishes | Medium | Low | Medium | Medium | Official menus + recent reviews; no broad restaurant crawler | Resolve only decision-relevant dishes for finalists, not all culinary detail | P1 |
| HTML/PDF/mobile consistency and A+B+C acceptance | High as release gate, low as standalone feature | High | Medium | Per release | Reuse existing validators and PDF toolchain | Every meaningful release can ship without regressions or duplicate QA infrastructure | P1 gate |
| Additional supplier/parser infrastructure | Unknown until coverage gap is proven | Potentially high | Medium-high | Medium | Pilot one or two hard sources before generalization | A new integration is justified only if it produces verified comparable quotes or materially lowers manual work | P1 hypothesis, otherwise P2 |
| Consolidate old mobile-navigation docs / repository cleanup | Low | Low-medium | Low | Low | Consolidate only when touching same area | Cleanup should not consume its own production release | P2 |
| New VPS, paid price API, commercial scraper, large crawling platform | Unproven | Could increase autonomy | High / paid | Slow | First exhaust existing sources and small pilots | Build only after evidence that existing paths cannot deliver required coverage/economics | P2 |
| General recommendation-engine rewrite | Low while current decision surface works | Low | High | Slow | Improve evidence inputs before algorithm | No rewrite until current ranking quality is shown to be the limiting factor | P2 |

## New P0 / P1 / P2

### P0

1. **Price truth and monitoring correctness.** Maintain exact comparable price monitoring twice daily and eliminate operational drift between schedule, docs and automation behavior.
2. **Increase current comparable price coverage where the public basis is historical/missing/weak.** Do not broaden into a generic crawler first.
3. **Close decision-critical unknowns for the leading alternatives.** Focus only on facts that can change the booking decision or shortlist.
4. **Rerank only on material evidence.** A new source or changed fact is not itself a reason to move ranking.

### P1

1. Build a **booking-readiness package for the final three hotels**: exact room category for each occupancy, board, mandatory New Year/gala charges, cancellation/payment conditions and current comparable total.
2. Maintain official-site/review link health using the existing registry and current language priority.
3. Resolve gastronomy questions only for finalists or when they become a real tie-breaker.
4. Keep HTML/PDF/mobile and A+B+C as release gates, not independent feature programmes.
5. Pilot new source integrations only when a concrete price-coverage gap justifies them.

### P2

1. Broad infrastructure rewrite, new crawler platform or recommendation engine.
2. Paid APIs/VPS/licences before a measured need.
3. Repository/doc cleanup that does not improve correctness, autonomy or booking quality now.
4. Full-scale gastronomy research across every hotel when it cannot change the current choice.
5. Generic scaling capability for use cases not yet demonstrated by the current trip.

## Release and hypothesis decomposition

### Increment A: Decision-quality price truth uplift

**User value:** fewer stale/historical price assumptions and a more reliable cost comparison.

**Hypothesis:** existing authorized sources plus current monitoring can materially improve current comparable price evidence without new paid infrastructure.

**Minimum scope:** identify hotels/occupancies whose published basis is historical, absent or weak; start with the smallest decision-critical subset and check exact hotel + exact supplier room category + occupancy + dates + board + currency.

**PASS evidence:** at least one meaningful gap is replaced by a verified current comparable quote, or bounded research proves that no comparable current quote is available and the product preserves that uncertainty correctly. No guessed price, package substitution or timestamp movement without an actual published price delta.

**Excluded until PASS:** general crawler framework, paid APIs, new VPS, mass supplier integrations.

**Next step after PASS:** expand only to the next highest-value uncovered hotel/occupancy.

### Increment B: Top-candidate uncertainty closure

**User value:** a shortlist based on fewer assumptions about winter life and New Year fit.

**Hypothesis:** a small set of unresolved facts, not more UI or more ranking logic, is the main remaining source of decision uncertainty.

**Minimum scope:** select 3-5 unresolved facts that can change the relative position of the leading hotels, such as confirmed New Year programme, winter kids-club hours, heated pools, tennis availability/lighting, large-group common spaces, gala/board conditions.

**PASS evidence:** each selected item ends as confirmed, falsified or explicitly unavailable with source evidence; recommendation changes only if the new fact materially changes the decision.

**Excluded until PASS:** broad hotel-content refresh, generic research platform, cosmetic redesign.

**Next step after PASS:** either update ranking/shortlist in one meaningful release or leave ranking unchanged and move to booking readiness.

### Increment C: Final-three booking readiness

**User value:** transform comparison into an actionable booking decision.

**Hypothesis:** once shortlist uncertainty is low, exact commercial terms for the final three become more valuable than expanding the comparison to more hotels or more editorial dimensions.

**Minimum scope:** for each finalist and each relevant occupancy, capture exact room category, current stay price, board, mandatory gala/New Year charges, payment/cancellation conditions and official/approved booking path when verifiable.

**PASS evidence:** the user can compare the final three on a like-for-like commercial basis and see every unresolved term explicitly.

**Excluded until PASS:** booking automation, payment automation, supplier accounts, paid inventory feeds.

**Next step after PASS:** user booking decision or a targeted refresh of only the decisive unresolved commercial terms.

## What to simplify, postpone or combine

- Do not release documentation cleanup by itself. Bundle it with the next meaningful product release.
- Do not build a generic price crawler before a small source pilot proves incremental coverage.
- Do not broaden gastronomy research beyond finalists unless food becomes a demonstrated tie-breaker.
- Do not rewrite the recommendation model while evidence quality is the more obvious constraint.
- Combine HTML, PDF, state, docs, validators and release evidence into one production commit per release.
- Treat old mobile-navigation micro-doc consolidation as opportunistic cleanup when that area is next modified.

## What to accelerate

- Current-price evidence for historical/weak rows.
- New Year/winter-operation facts that can move the shortlist.
- Exact commercial terms for the eventual final three.
- Automation correctness that removes user checking without adding GitHub Actions churn.

## Reuse and workaround opportunities

1. **HTTP/public structured data first.** Prefer stable official/public endpoints, embedded JSON/JSON-LD and normal HTTP requests before browser automation.
2. **Existing project stack first.** Reuse current HTML parsers, validators, PDF generation and state contracts before adding libraries or services.
3. **Browser only where required.** Use rendered/browser checks for genuinely JS-only evidence; do not move routine monitoring into expensive browser/CI loops.
4. **Approved supplier fallback.** When an official hotel engine cannot expose exact comparable rates, use an already-approved supplier with the exact same hotel/category/occupancy/dates/board/currency contract rather than inventing a workaround.
5. **Fail closed on access controls.** CAPTCHA or blocked inventory means unavailable evidence, not permission to bypass controls.
6. **Small integration pilots.** Test one difficult source before building a generalized adapter architecture.

## Resource decision

No new paid resources are justified by the current backlog audit. Existing GitHub, Drive, automation, web/public sources and current validation stack are sufficient for the next increment. Any paid API, additional VPS, licence or commercial scraping service requires separate approval after a measured gap.

## Next minimal product increment

**Start with Increment A: Decision-quality price truth uplift.**

The first bounded slice should target the smallest set of currently historical/missing/weak comparable-price rows that can materially affect the shortlist, beginning with Rixos Park's current 9-night comparable rate for the three occupancies if accessible through authorized sources. Preserve all existing public values unless stronger exact evidence is found. If no exact current rate can be verified, record that result and stop instead of building infrastructure around the failure.

A production release is justified only if this work produces a meaningful user-visible delta or is bundled with another meaningful accepted increment. No docs-only release is required for this planning package.