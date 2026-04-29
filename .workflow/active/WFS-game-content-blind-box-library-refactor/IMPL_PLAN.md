---
session_id: WFS-game-content-blind-box-library-refactor
status: ready_for_review
generated_at: 2026-04-29T00:00:00+08:00
source_spec: .workflow/.spec/SPEC-2026-04-29-game-content-extraction-blind-box-library-refactor/
---

# Implementation Plan: Game content extraction 盲盒物品内容库重构

## 1. Requirements Summary

This plan implements the MVP from the spec package:

- Define the new blind-box content model around 20 `场景+用途` entries.
- Represent pilot content with five layers: `core_items`, `support_items`, `visible_small_items`, `conditional_items`, `blocked_or_risky`.
- Keep current runtime compatibility by exposing `large`, `medium`, `small`, `hanging`.
- Deliver three pilot categories: `桌面+学习`, `海底+潜水`, `公园+野餐`.
- Validate schema completeness, risk isolation, legacy input behavior and documentation sync.

Out of scope for this plan:

- Full rewrite of all 20 categories.
- UI redesign for new 20-category display.
- `draw_history.json` migration.
- Web/database/server changes or new third-party dependencies.
- Desktop release version bump.

## 2. Architecture Decisions

| Decision | Implementation Guidance |
|----------|-------------------------|
| 20 scene entries are the canonical authoring model | Keep a structured list or mapping in `Game content extraction/data/`, but do not require UI changes in MVP. |
| Five-layer model maps to four runtime buckets | Implement a compatibility view that preserves `BLIND_BOXES[box_id][large|medium|small|hanging]`. |
| Pilot-first rollout | Limit production data changes to `桌面+学习`, `海底+潜水`, `公园+野餐` or their explicit compatibility slots. |
| Risk isolation | `blocked_or_risky` must never appear in default runtime buckets. |
| History/input compatibility | Preserve comma syntax, category override labels and `box:{box_id}:{category_key}` history keys. |

## 3. Task Breakdown

| Task | Title | Depends On | Type |
|------|-------|------------|------|
| [IMPL-1](.task/IMPL-1.json) | Add blind-box content model and compatibility mapping contract | None | data/model |
| [IMPL-2](.task/IMPL-2.json) | Author three pilot category content bundles | IMPL-1 | content/data |
| [IMPL-3](.task/IMPL-3.json) | Preserve runtime extraction and history compatibility | IMPL-1, IMPL-2 | runtime |
| [IMPL-4](.task/IMPL-4.json) | Add validation tests for schema, risk leakage and compatibility | IMPL-1, IMPL-2, IMPL-3 | tests |
| [IMPL-5](.task/IMPL-5.json) | Sync docs and review workflow artifacts | IMPL-4 | docs |

## 4. Implementation Strategy

Recommended execution is sequential with one natural checkpoint after IMPL-2:

1. **Model first**: add the minimal static schema and mapping helper without touching UI behavior.
2. **Pilot content second**: author only three pilot bundles, then expose them through the existing four-bucket shape.
3. **Compatibility check third**: verify extraction still sees `large`, `medium`, `small`, `hanging`; do not alter labels unless tests prove compatibility.
4. **Validation fourth**: add tests before considering broader category expansion.
5. **Docs last**: sync required project docs with exact implementation details and known deferrals.

## 5. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Full static data rewrite creates hard-to-review diff | High | Limit MVP content edits to three pilot categories. |
| New model breaks old input/history semantics | High | Keep runtime bucket keys and parser labels unchanged; add regression tests. |
| `blocked_or_risky` leaks into default output | High | Add zero-leak tests against generated four-bucket view. |
| Risky `item_states.py` wording reintroduces transparent/reflection output | Medium | Add explicit test or safe-state handling for blind-box default output. |
| Documentation drifts from implementation | Medium | Make doc sync a required final implementation task. |

## 6. Verification Commands

Run after implementation:

```powershell
python -B -m py_compile 'Game content extraction\内容抽取.py'
python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'
```

If implementation touches release packaging, use the broader release validation from `agents.md`; this MVP plan should not require packaging.

## 7. Next Step

Review this plan, then execute with:

```text
$workflow-execute --session WFS-game-content-blind-box-library-refactor
```
