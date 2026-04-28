# REVIEW-001 Report

Verdict: CONDITIONAL

## Findings

1. Documentation and repo-level contract still forbid expression history in `draw_history.json`, but the implementation now persists `expression_pools`.
   - `Game content extraction/内容抽取.py:115-120` creates draw history version `2` with `expression_pools`.
   - `Game content extraction/内容抽取.py:123-150` loads and rewrites `expression_pools`.
   - `agents.md:42`, `Game content extraction/CLAUDE.md:39`, `Game content extraction/README.md:64-78,117,172-173` still state that only item/animal history belongs in `draw_history.json` and that expression enhancement does not write there.
   - Risk: reviewers, maintainers, and release validation will disagree on intended behavior until those docs are updated in the same change.

2. The new expression history uses a different persistence model from item/animal pools and needs explicit validation coverage to guard migration and reset semantics.
   - `Game content extraction/内容抽取.py:177-211` stores flat per-value usage counts under `expression_pools`.
   - `Game content extraction/内容抽取.py:305-326` and `1231-1260` show existing item/animal pool behavior: cooldown-based weighted draws with separate pool groups.
   - `Game content extraction/内容抽取.py:373-377` clears `expression_pools` only as part of `重置全部历史`; there is no expression-only reset path.
   - Risk: the new scope is independent from item/animal selection logic, but not independently resettable, so user-facing semantics should be documented and tested.

3. The implementation and unit tests are aligned, but the validation surface should stay focused on weighting inputs rather than only random output selection.
   - `Game content extraction/内容抽取.py:1887-1897` applies history weighting to multi-candidate `具体表情`.
   - `Game content extraction/内容抽取.py:1899-1924` applies history weighting to random template selection and still records specified template choices.
   - `Game content extraction/内容抽取.py:1926-1967` records both category and template history after successful enhancement and saves once at the end.
   - `Game content extraction/test_expression_enhancement.py:68-103,127-176,189-218` covers weighted category selection, weighted random-template selection, explicit-template history recording, legacy-history upgrade, and isolation from `item_pools` / `animal_pools`.

## Scope Notes

- History storage now lives in `Game content extraction/draw_history.json` under three top-level groups:
  - `item_pools`: cooldown-based item draw state.
  - `animal_pools`: cooldown-based animal draw state.
  - `expression_pools`: flat usage counters for expression categories and template indexes.
- Multi-candidate `具体表情` still accepts `、` `，` `,` `/` `|` separators via `Game content extraction/内容抽取.py:1802-1810`, validates every candidate against polarity via `1879-1893`, then selects a single category with inverse-frequency weighting.
- Prior session `TLV4-20260427-expression-multi-candidate` established the multi-candidate parsing/validation path; the current scope extends that path with persistence and weighting rather than changing the parsing contract.

## Recommended Validation Focus

1. Keep the unit tests that prove:
   - multi-candidate category weighting uses `random.choices` weights derived from prior counts;
   - random template weighting uses the same inverse-frequency rule;
   - single-category and specified-template runs still record history;
   - loading a version `1` history upgrades to version `2` with `expression_pools`;
   - expression history updates do not mutate `item_pools` or `animal_pools`.

2. Add or keep workflow-level verification that proves:
   - persisted `draw_history.json` contains `expression_pools` after enhancement;
   - repeated enhancement replaces old `眉/眼/嘴` text without stacking;
   - `重置全部历史` clears `expression_pools` together with existing history groups.

3. Do not ship the change without synchronizing `agents.md`, `Game content extraction/CLAUDE.md`, and `Game content extraction/README.md` to the new history contract.
