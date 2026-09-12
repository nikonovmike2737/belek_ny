# BELEK NY: Product Operating Principles

**Status:** CURRENT working canon  
**Scope:** product prioritization, engineering prioritization, architecture decisions, task decomposition, resource decisions, release planning, hypothesis testing and blocker handling for `nikonovmike2737/belek_ny`.

This document is the single source of truth for how work on BELEK NY is prioritized and executed. Other current roadmap, release and engineering documents may add domain-specific constraints, but should reference this canon instead of duplicating it.

These principles do not grant new production authority, permission to buy resources, add secrets, perform irreversible migrations or change material product logic. Such actions remain governed by explicit project-specific authority and user approval.

## 1. Maximum client value now

Choose the work that produces the largest visible improvement for the user now.

Client value is more important than architectural elegance, low-priority technical debt, documentation for its own sake, optional hardening or infrastructure that is not yet needed.

For BELEK NY, the core user job is to make a better booking decision for the 25.12.2026-03.01.2027 trip. Work that materially improves comparable price truth, winter-operation truth, New Year programme truth, room/occupancy fit, shortlist confidence or booking readiness normally outranks internal cleanup.

Before selecting the next task ask: what available backlog item will produce the largest noticeable improvement in the user's decision after delivery?

If a useful capability already exists but one missing layer prevents it from reaching the user, complete that last layer before starting unrelated new functionality.

## 2. Maximum practical autonomy

Design development, monitoring, validation and release flow to minimize user intervention.

Prefer autonomous checks, durable state, fail-closed automation, deterministic validation, safe automated publication where already authorized, and rollback that does not require manual reconstruction.

Do not ask the user to perform an action that can be completed safely with existing tools and permissions.

Escalate only when a real blocker remains after bounded investigation and requires a user decision, credential, new cost, irreversible migration, material product-logic change or genuinely user-only manual action.

Autonomy must not silently expand production authority.

## 3. Rational use of resources and budget

Treat as limited resources: tokens, GitHub Actions, API calls, storage, external-service usage, user time, repeated checks, CI/release cycles and paid infrastructure.

Use the minimum sufficient model, reasoning depth, runtime, number of calls and number of validations needed for the required quality.

Do not repeat discovery that is already confirmed and still fresh. Do not run expensive rendered or full acceptance repeatedly when a narrow targeted check is sufficient during remediation. Do not create CI churn.

For BELEK NY:

- normal monitoring must not create commits or Actions runs when there is no meaningful delta;
- one product release should normally be one production commit containing the complete relevant HTML/PDF/docs/state/code package;
- current price monitoring cadence is 09:00 and 21:00 Europe/Moscow;
- new paid APIs, VPS, licences or other additional cost require explicit approval.

Optimize for:

`maximum autonomy + maximum client value / minimum necessary resources`.

## 4. Fast incremental development and delivery

Break work into bounded slices that converge quickly on a useful, complete product increment.

Do not build one oversized release when independent meaningful increments can be delivered safely. Do not turn every small change into its own production release either.

A release must provide visible user value or clear learning value, justify CI/acceptance/deploy cost and be coherent enough for production.

Inside one approved release, use small bounded implementation slices and aggregate them into one meaningful release package.

Small documentation, housekeeping or technical cleanup changes should normally wait for the nearest meaningful release unless they are themselves blocking correctness or safety.

## 5. Do not stop at the first wall

A blocked implementation path is not automatically a blocked task.

First identify the exact constraint. Then test a simpler transport, source, integration sequence, reuse path or operational workaround while preserving product semantics and safety.

For hotel research, for example, a blocked official booking UI does not justify guessing, CAPTCHA bypass or a paid workaround. Try other authorized official/public paths, stable booking endpoints, public structured data or approved suppliers. If exact comparable evidence still cannot be obtained, preserve UNKNOWN/historical truth and move on rather than fabricating certainty.

Escalate only after bounded alternatives are exhausted and the remaining blocker truly requires user action or a material project decision.

## 6. Use mature open practices and reuse

Before writing generic infrastructure from scratch, check official documentation, mature open-source libraries, upstream implementations and established patterns.

Prefer reuse when it reduces code, development time, token cost and defect risk without adding disproportionate integration or operating complexity.

Before adopting a dependency, verify licence, security, maintenance, compatibility, integration cost and runtime cost.

For BELEK NY, prefer simple HTTP/public structured-data extraction before browser automation, existing validators/parsers before parallel implementations, and established PDF/HTML tooling already in the project before introducing a second rendering stack.

Reuse is not a reason to import Theatre Guide-specific infrastructure or contracts.

## 7. Fast hypothesis testing

For every substantial new capability, state the hypothesis before building the full system.

Define:

1. the hypothesis;
2. the minimum product increment that can test it;
3. PASS evidence;
4. evidence that means adjust or stop;
5. what will deliberately not be built before the result.

Use bounded pilots, small source sets, test contours, staging, feature flags or limited scenarios where practical.

For BELEK NY, a new scraper, supplier integration, alerting mechanism or recommendation layer should first prove that it materially improves booking-decision quality or operating economics on a small decision-critical subset. Do not build a general platform before that proof.

Each hypothesis release must combine learning value with real product value. Do not create micro-releases merely to exercise the process.

## Decision checklist for every new task

Before implementation, check internally:

1. Is this the highest-value available work for the user's current booking decision?
2. Does the solution increase or reduce autonomy?
3. Is resource use proportional to the value and risk?
4. Can the work be reduced to a smaller meaningful increment?
5. If the obvious path is blocked, is there a safe workaround?
6. Is there a mature reusable solution instead of custom infrastructure?
7. What hypothesis is being tested and what evidence ends the iteration?

If the answers are clear, proceed without unnecessary questions. Ask the user only when a material product choice, new cost, new credential, new production authority, irreversible migration or substantially larger scope is required.

## Relationship to existing BELEK NY canon

This document governs operating decisions. Domain-specific truth and release rules remain authoritative within their scope, including:

- `docs/DELTA_ONLY_PRODUCTION_POLICY.md`;
- `docs/PRICE_UPDATE_TIMESTAMPS_RULE.md`;
- `docs/PRICE_TREND_DISPLAY_RULE.md`;
- `docs/PRICE_REFRESH_ROLLBACK_POLICY.md`;
- `docs/TEXT_STYLE_SOURCE_OF_TRUTH.md`;
- `docs/PUBLIC_COPY_QA_CHECKLIST.md`;
- hotel-card, official-site and mobile-navigation rules.

Where two valid approaches satisfy domain correctness, prefer the one that better satisfies these seven operating principles.