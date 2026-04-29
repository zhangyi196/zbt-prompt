# Planning Notes: Game Content Four-Pool Blind Box Refactor

## Goal

按最新四类内容池规格，将 `Game content extraction` 三类盲盒试点从当前五层池过渡状态，重构为：

- `core_items`
- `support_items`
- `visible_small_items`
- `scene_expansion_items`

并移除 `conditional_items`、`anchor_required_items`、`blocked_or_risky` 作为候选内容类别。

## Source Spec

- `.workflow/.spec/SPEC-2026-04-29-game-content-extraction-four-pool-refactor/spec-summary.md`
- Readiness: 96.5 / 100, Pass
- Source brainstorm: `.workflow/.brainstorm/BS-2026-04-29-重新定义conditional-items-blocked-or-risky/`

## Current Code State

- `Game content extraction/data/blind_boxes.py` 当前仍保留三类五层池过渡状态。
- `_build_legacy_blind_box_entry` 当前将 `conditional_items` 映射到 `hanging`。
- `BLIND_BOX_COMPATIBILITY_MAPPING` 当前声明 `hanging_sources=["conditional_items"]` 和 `excluded_sources=["blocked_or_risky"]`。
- `Game content extraction/test_blind_box_content_model.py` 当前测试 `FIVE_LAYER_KEYS`，并验证 `blocked_or_risky` 不泄漏。

## Key Planning Decisions

- 本轮不做图像识别、锚点检测、用户文本触发或 UI 改版。
- 先改数据 schema 和兼容映射，再重写内容，再改测试和文档。
- `hanging` 字段作为兼容字段保留，但不再由低质量细绳/挂饰/锚点依赖物强制填充。
- `blocked_patterns` 可先作为测试常量存在，不一定抽到运行时数据模块。
