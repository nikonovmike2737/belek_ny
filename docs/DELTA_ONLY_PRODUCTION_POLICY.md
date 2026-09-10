# BELEK NY: Delta-only production policy

Status: HARD GATE. This rule is mandatory for every 3-hour monitoring run and every production publication.

## Core rule

Production is updated only when monitoring discovers a meaningful, evidence-backed delta relative to the currently published production state.

A scheduled monitoring run by itself is never a reason to update Google Drive, regenerate PDF, create a GitHub commit, trigger GitHub Actions, or deploy GitHub Pages.

No delta = no write, no commit, no deploy.

## Required run sequence

1. Read the current published production state before monitoring:
   - canonical HTML from Google Drive;
   - canonical PDF from Google Drive;
   - current `main` state from GitHub;
   - `data/current-price-state.json` and room registry;
   - current published price values and their comparison baseline.
2. Build a normalized baseline snapshot of the currently published facts.
3. Run monitoring against the configured official hotel/booking sources, reputable supplier/OTA evidence, and the other approved evidence sources.
4. Normalize the monitoring result to the same schema as the baseline.
5. Compute the delta field-by-field against the published baseline.
6. Ignore observation-only differences that do not change a published fact, including retrieval timestamps, cache-busting parameters, source-check timestamps, formatting-only differences, regenerated file bytes with identical report content, or a new internal run ID.
7. If the normalized delta is empty, stop. Do not write or publish anything.
8. If the delta is non-empty, validate that each changed fact is supported by admissible evidence and is genuinely comparable to the published value where comparison is required.
9. Apply only the confirmed delta to structured state, HTML and PDF. Unchanged published facts remain unchanged.
10. Run consistency, rendering and readback checks.
11. Only after all checks pass, publish the updated HTML and PDF to the canonical Google Drive file IDs and allow GitHub sync to commit the actual changed artifacts.
12. GitHub Pages may deploy only from a commit that contains a real artifact/data delta. Do not create a trigger-only or timestamp-only commit.
13. After successful production publication, the newly published state becomes the baseline snapshot for the next monitoring run.

## Meaningful delta

A meaningful delta is a confirmed change to a user-visible or decision-relevant fact, for example:

- comparable room price increased or decreased;
- comparable availability changed;
- room category was added, removed or renamed;
- board basis, mandatory gala fee, cancellation terms or other material booking conditions changed;
- a material winter service/infrastructure fact changed;
- strong new evidence resolves a previously material uncertainty;
- a ranking or recommendation changes because its underlying confirmed facts changed.

A source being checked again is not a delta. A new `checked_at` value is not a delta. A fresh PDF render with the same content is not a delta. A changed publication timestamp alone is not a delta.

## Price-delta semantics

For every comparable published price cell, retain the immediately previous published comparable price as the comparison baseline.

- `current > previous` => price increased => `data-price-trend="up"` and a red `↑`.
- `current < previous` => price decreased => `data-price-trend="down"` and a green `↓`.
- `current == previous` => no price delta => `data-price-trend="same"` and no arrow.

Do not compare unlike dates, occupancies, room categories, board bases, currencies, package prices or otherwise non-comparable quotes. If comparability is not proven, do not publish an up/down status.

The arrow is derived from the confirmed delta only. It is never generated from monitoring timestamps or from a newly fetched but non-comparable quote.

## No-op behavior

When no meaningful delta exists, all of the following are forbidden:

- changing the visible report update time;
- changing an internal report version only to force publication;
- regenerating and replacing PDF with equivalent content;
- rewriting canonical Drive files;
- touching `.github/belek-sync-trigger` or any equivalent trigger file;
- creating a GitHub commit whose only purpose is to wake a workflow;
- creating an empty commit;
- triggering a production deployment merely because three hours have elapsed.

The monitoring run may finish silently after recording no production change in its transient runtime state.

## GitHub sync rule

The existing sync workflow must behave idempotently: it may read canonical artifacts on schedule, but it must commit only when the actual tracked artifacts/data differ from the currently checked-in production version.

Do not use a trigger-only commit as a substitute for `workflow_dispatch`.

If direct workflow dispatch is unavailable, do not manufacture a GitHub commit. Let the existing scheduled sync pick up the already validated canonical delta. The scheduled sync must still commit only the changed production artifacts/data.

## Failure behavior

If monitoring finds a candidate delta but evidence, comparability, HTML/PDF consistency, Drive dual-write/readback or GitHub publication checks fail, do not partially publish. Keep the previous production version and report the blocker only when it is systematic or materially prevents publication of a confirmed change.

## Production invariant

At any time, a production commit/deployment must be explainable as:

`published baseline -> confirmed monitoring delta -> updated canonical HTML/PDF/data -> validated artifact commit -> Pages deployment`

If there is no confirmed monitoring delta in that chain, production publication is forbidden.
