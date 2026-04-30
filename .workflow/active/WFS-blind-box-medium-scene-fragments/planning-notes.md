# Planning Notes

## User Intent

GOAL: Implement `SPEC-2026-04-30-blind-box-medium-scene-fragments`.

SCOPE:
- Rewrite `Game content extraction/data/blind_boxes.py` `scene_expansion_items` for all 20 scenes as medium-scale scene fragments.
- Preserve the four-pool data contract, category IDs, runtime `BLIND_BOXES`, and `BLIND_BOX_COMPATIBILITY_MAPPING`.
- Add/extend tests for large-subject, tiny-subject, pool-boundary, count, uniqueness, and compatibility constraints.
- Sync stable rules to `Game content extraction/agents.md`; check root `agents.md`, `README.md`, and `.gitignore` after implementation.

CONTEXT:
- Spec summary: `.workflow/.spec/SPEC-2026-04-30-blind-box-medium-scene-fragments/spec-summary.md`
- Epics: `.workflow/.spec/SPEC-2026-04-30-blind-box-medium-scene-fragments/epics/_index.md`
- Readiness: Gate Pass, score 91/100.

## Constraints

- Planning only in this workflow-plan turn; do not implement code changes.
- Do not add a fifth pool.
- Do not change scene IDs, category names, UI, runtime extraction logic, animal pools, expression pools, image fetching, or renaming behavior.
- Chinese content remains UTF-8.

## Context Findings

- Critical files: `Game content extraction/data/blind_boxes.py`, `Game content extraction/test_blind_box_content_model.py`, `Game content extraction/agents.md`, root `agents.md`, `README.md`, `.gitignore`.
- Conflict risk: medium.
- Resolution: use a sequential single-owner implementation plan; avoid parallel edits to `blind_boxes.py`.
- Planning modules: rules, data_rewrite, tests, docs.

## N+1 Context

### Decisions

| Decision | Rationale | Revisit? |
|---|---|---|
| Use a 4-task sequential plan | `blind_boxes.py` and the main unittest file are shared hotspots with medium conflict risk | No |
| Put rule baseline before the 20-scene rewrite | Prevents the rewrite from drifting back to oversized or tiny fourth-pool entries | No |
| Keep docs as the last task | Stable docs should describe accepted behavior, not draft semantics | No |

### Deferred

- [ ] Consider an optional maintainer-only reference sheet of scene-specific word roots after this execution session, but keep it out of stable docs unless repetition makes it necessary.
- [ ] Consider a future lint helper for fourth-pool authoring only if the expanded unittest rules prove too noisy to maintain inside one file.
