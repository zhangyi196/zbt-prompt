# Implementation Plan: Blind Box Medium Scene Fragments

## Requirements Summary

Goal: implement `SPEC-2026-04-30-blind-box-medium-scene-fragments` by rewriting the fourth blind-box pool as medium-scale scene fragments without changing the four-pool runtime contract.

In scope:

- Define the executable rule baseline for medium-scale scene fragments.
- Rewrite all 20 `scene_expansion_items` lists in `Game content extraction/data/blind_boxes.py`.
- Add or extend regression checks for oversized subjects, tiny subjects, pool-boundary separation, uniqueness, and runtime compatibility.
- Sync stable maintainer docs after the data and tests settle.

Out of scope:

- Adding a fifth pool.
- Changing scene IDs, category names, tkinter UI, runtime extraction logic, animal pools, expression pools, image fetching, or renaming behavior.
- Cleaning or rewriting unrelated workflow artifacts.

Hard constraints:

- Keep the four pool keys exactly `core_items`, `support_items`, `visible_small_items`, `scene_expansion_items`.
- Keep every scene pool at 50 unique UTF-8 strings.
- Keep `BLIND_BOX_COMPATIBILITY_MAPPING` and `BLIND_BOXES` runtime shape compatible with the current tool.
- Treat `blind_boxes.py` as a single-owner sequential file because conflict risk is medium.

## Architecture Decisions

1. Rules-first execution: define the medium-fragment boundary helpers and sample-level checks before editing the 20 scene lists; full-list assertions are enabled after the rewrite.
2. Data-only refactor: keep the implementation centered on `Game content extraction/data/blind_boxes.py`; no UI, runtime-flow, or storage changes are allowed.
3. Existing harness only: extend `Game content extraction/test_blind_box_content_model.py` instead of adding a new validation framework.
4. Runtime compatibility is a hard contract: `BLIND_BOXES` must still expose `name`, `large`, `medium`, `small`, and `hanging`, and `scene_expansion_items` must continue to feed the legacy `large` view through the current mapping.
5. Docs last and minimal: update `Game content extraction/agents.md` first, then check `agents.md`, `README.md`, and `.gitignore` only for stable-rule or cache-tracking changes.

## Task Breakdown with Dependencies

### IMPL-1: Freeze medium-scene-fragment rules and runtime contract

Depends on: none

Files:

- `Game content extraction/test_blind_box_content_model.py`

Deliverables:

- Add 1 reusable rule baseline covering 4 rule groups: allowed medium-scene fragments, forbidden oversized subjects, forbidden tiny subjects, upgraded information-surface exceptions.
- Add helper/sample-level tests that pass against representative examples without asserting the current full data file must already comply.
- Keep existing structural/runtime tests green before the full rewrite starts.

### IMPL-2: Rewrite all 20 `scene_expansion_items` lists

Depends on: `IMPL-1`

Files:

- `Game content extraction/data/blind_boxes.py`

Deliverables:

- Rewrite 20 fourth-pool lists in place for all scenes inside `BLIND_BOX_ITEM_POOL_BUNDLES`.
- Preserve 20 scene IDs, 4 pool keys, and 50 unique UTF-8 strings per pool.
- Remove oversized furniture/storage subjects and standalone tiny information subjects except for the explicit medium-surface exceptions codified in `IMPL-1`.

### IMPL-3: Finish quality gates and run regression verification

Depends on: `IMPL-2`

Files:

- `Game content extraction/test_blind_box_content_model.py`

Deliverables:

- Enable full-list assertions for 5 regression dimensions in the existing unittest file: oversized-subject exclusion, tiny-subject exclusion, pool-boundary separation, 20x50 uniqueness, runtime compatibility.
- Run compile and unittest verification against the rewritten data.
- Leave 0 failing checks in the blind-box regression suite.

### IMPL-4: Sync stable docs and close the review loop

Depends on: `IMPL-3`

Files:

- `Game content extraction/agents.md`
- `agents.md`
- `README.md`
- `.gitignore`

Deliverables:

- Update 1 primary maintainer rule source: `Game content extraction/agents.md`.
- Check 3 root files and edit only the files that need stable-rule or cache-tracking changes.
- Record the verification commands/results in `.workflow/active/WFS-blind-box-medium-scene-fragments/.process/EXECUTION_SUMMARY.md` without touching unrelated workflow files.

## Implementation Strategy

The plan is sequential end to end:

1. Establish the rule baseline helpers and sample checks so the content rewrite has explicit boundaries while the suite remains green.
2. Rewrite `scene_expansion_items` once, in a single owner pass, to avoid fragmented edits in `blind_boxes.py`.
3. Tighten and execute regression coverage only after the full data rewrite exists.
4. Sync stable docs last so they describe accepted behavior rather than draft semantics.

Execution notes:

- The executor should study at least 3 existing scene patterns inside `blind_boxes.py` before rewriting lists, then keep naming style consistent across all 20 scenes.
- If uncommitted changes appear in `Game content extraction/data/blind_boxes.py` or `Game content extraction/test_blind_box_content_model.py`, stop and report the conflict instead of merging by assumption.
- The plan intentionally avoids parallel subtasks because `blind_boxes.py` and the main unittest file are shared hotspots.

## Risk Assessment

| Risk | Severity | Mitigation |
|---|---|---|
| Full-list rewrite in `blind_boxes.py` is hard to review and easy to conflict with adjacent work | Medium | Keep a single sequential owner and complete all 20 list edits in one bounded task |
| Fourth-pool entries drift back to cabinets, carts, racks, shelves, desks, or similar oversized subjects | Medium | Freeze deny rules in `IMPL-1` and enforce them again in `IMPL-3` |
| Fourth-pool entries shrink into cards, labels, tickets, bookmarks, price tags, or similar tiny subjects | Medium | Encode tiny-subject exclusions and upgraded-surface exceptions in tests before the rewrite |
| Structural tests pass while semantic quality regresses | Medium | Add explicit semantic checks for large/tiny boundaries and pool-boundary separation |
| Stable docs become noisy or duplicate the spec | Low | Update docs only after tests pass and keep them limited to durable maintainer rules |

## Verification Plan

Primary commands:

```powershell
python -B -m py_compile 'Game content extraction\内容抽取.py' 'Game content extraction\data\blind_boxes.py'
python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'
```

Per-task verification:

- `IMPL-1`: run the unittest suite and keep it green; do not enable full-list fourth-pool assertions until `IMPL-3`.
- `IMPL-2`: run `py_compile` plus a unittest pass to catch syntax and immediate contract regressions before refining tests.
- `IMPL-3`: run the full compile and unittest commands until both pass cleanly.
- `IMPL-4`: confirm docs reflect the accepted rule baseline, write `.process/EXECUTION_SUMMARY.md`, and leave `.gitignore` unchanged unless a real cache-tracking issue was found.
