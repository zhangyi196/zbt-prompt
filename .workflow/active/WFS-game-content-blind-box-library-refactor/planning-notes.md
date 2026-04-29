# Planning Notes

## User Intent

GOAL: 基于已完成的 spec-generator 规格包，生成 `Game content extraction` 盲盒物品内容库重构的实现计划。

SCOPE: 规划阶段只输出实施计划、任务 JSON 和 TODO，不执行代码实现。计划覆盖 20 个场景入口、五层物品池 schema、五层到四栏兼容映射、三个试点类别、风险校验、历史兼容和文档同步。

CONTEXT: Source spec 位于 `.workflow/.spec/SPEC-2026-04-29-game-content-extraction-blind-box-library-refactor/`，readiness gate 为 Pass，建议 issue 已在 `issue-export-report.md` 中列出。

## Context Findings

- Critical files: `Game content extraction/data/blind_boxes.py`, `Game content extraction/内容抽取.py`, `Game content extraction/data/item_states.py`, `Game content extraction/test_*.py`, `agents.md`, `README.md`, `Game content extraction/CLAUDE.md`, `Game content extraction/README.md`, `.gitignore`.
- Existing runtime shape: `BLIND_BOXES` is a numeric-id Python dict; each entry exposes `name`, `large`, `medium`, `small`, `hanging`.
- Runtime coupling: input overrides derive from `category_info`; history keys use `box:{box_id}:{category_key}` under `draw_history.json.item_pools`.
- Test pattern: existing tests import `内容抽取.py` via `importlib` and use fake UI vars/objects for logic-level testing.
- Conflict risk: medium. A full data rewrite is risky; planning should isolate schema/mapping work, pilot content, tests and docs.
