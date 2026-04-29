# Implementation Plan: Game Content Four-Pool Blind Box Refactor

## Objective

Implement the four-pool blind-box pilot refactor from `SPEC-2026-04-29-game-content-extraction-four-pool-refactor`: replace `conditional_items` with `scene_expansion_items`, remove `blocked_or_risky` as a candidate pool, keep the legacy `BLIND_BOXES` four-column runtime view, and update tests/docs.

## Scope

In scope:

- `Game content extraction/data/blind_boxes.py`
- `Game content extraction/test_blind_box_content_model.py`
- Required docs: `agents.md`, `README.md`, `Game content extraction/CLAUDE.md`, `Game content extraction/README.md`, `.gitignore`
- Workflow status artifacts

Out of scope:

- UI changes
- image recognition / anchor detection
- user text trigger parsing
- all 20 category expansion
- release packaging or version bump

## Execution Order

### IMPL-1: Refactor pilot schema and legacy mapping

Files:

- `Game content extraction/data/blind_boxes.py`

Actions:

- Replace pilot bundle key `conditional_items` with `scene_expansion_items`.
- Remove `blocked_or_risky` from pilot bundle schema.
- Update `_build_legacy_blind_box_entry` to use four pools.
- Update `BLIND_BOX_COMPATIBILITY_MAPPING` to reflect four-pool sources and no candidate excluded pool.
- Keep `BLIND_BOXES` four-column view intact.

Acceptance:

- Pilot bundle keys are exactly `core_items`, `support_items`, `visible_small_items`, `scene_expansion_items`.
- `BLIND_BOXES[15/16/17]` still expose `name`, `large`, `medium`, `small`, `hanging`.
- Mapping no longer references `conditional_items` or `blocked_or_risky`.

### IMPL-2: Rewrite pilot content with high-quality scene_expansion_items

Files:

- `Game content extraction/data/blind_boxes.py`

Actions:

- Rewrite `scene_expansion_items` for `桌面+学习`, `海底+潜水`, `公园+野餐`.
- Use user examples as anchors for quality direction:
  - 桌面: `桌面日历`, `桌面小风扇`, `护眼书架`, `桌面收纳抽屉`.
  - 野餐: `折叠野餐桌`, `便携冷藏箱`, `户外收纳箱`, `野餐遮阳布`.
- Ensure 海底+潜水 uses equipment/storage/work objects, not animal bodies, transparent/glowing/reflective objects, or thin rope/net objects.

Acceptance:

- `scene_expansion_items` are medium-or-larger, scene-relevant, boundary-clear, independently circleable.
- No image-anchor-dependent terms such as `显示器下方`, `白板磁吸`, `伞杆`, `挂点`, `桌侧`.
- No thin/string-like, transparent, reflective, glowing, animal-body, or micro-detail terms in default pools.

### IMPL-3: Update regression tests for four-pool schema and blocked patterns

Files:

- `Game content extraction/test_blind_box_content_model.py`

Actions:

- Replace `FIVE_LAYER_KEYS` with a four-pool constant.
- Update schema tests to assert exact four-pool keys.
- Add/keep assertions that `conditional_items` and `blocked_or_risky` are absent.
- Update forbidden pattern scan to cover all four default pools.
- Remove old `blocked_or_risky` leakage test or replace it with a no-risk-candidate-pool test.

Acceptance:

- Test suite covers four-pool schema, legacy runtime bucket contract, forbidden patterns, input override, and risky item states.
- `python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'` passes.

### IMPL-4: Sync docs and verification records

Files:

- `agents.md`
- `README.md`
- `Game content extraction/CLAUDE.md`
- `Game content extraction/README.md`
- `.gitignore`
- `.workflow/active/WFS-game-content-four-pool-refactor/TODO_LIST.md`

Actions:

- Update docs from “current code is five-layer transition state” to implemented four-pool status.
- Document `scene_expansion_items` quality rules and `blocked_patterns` validation.
- Record verification commands and results.

Acceptance:

- Required docs align with implemented four-pool model.
- TODO and task JSON status are updated during execution.
- `git status --short` shows only intended files.

## Verification Commands

```powershell
python -B -m py_compile 'Game content extraction\内容抽取.py' 'Game content extraction\data\blind_boxes.py'
python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'
```

## Notes For Executor

- This is a sequential plan because `blind_boxes.py` is shared across the data tasks.
- Do not add image anchors, user-text triggers, or runtime UI controls.
- Prefer fewer safe `hanging` candidates over low-quality forced fill.
