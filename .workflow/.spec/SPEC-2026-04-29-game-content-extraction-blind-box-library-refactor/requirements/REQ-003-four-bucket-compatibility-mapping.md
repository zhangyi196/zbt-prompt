---
session_id: SPEC-2026-04-29-game-content-extraction-blind-box-library-refactor
phase: 3
document_type: requirements
status: complete
generated_at: 2026-04-29T00:00:00+08:00
stepsCompleted:
  - load-context
  - expand-requirements
  - codex-review
version: 1
dependencies:
  - ../product-brief.md
  - ../refined-requirements.json
  - ../discovery-context.json
id: REQ-003
type: functional
priority: Must
traces_to:
  - G-003
---

# REQ-003: 定义五层池到四栏运行时的兼容映射

**Priority**: Must

## Description

规范 MUST 提供从五层物品池回写到现有 `large`、`medium`、`small`、`hanging` 结构的明确映射规则。映射规则 MUST 允许现有 UI、输入语法和抽取逻辑继续运行，且 MUST NOT 把 `hanging` 重新当成补量主池。

## User Story

As a 开发维护者, I want to 用确定性的映射规则连接新模型和旧运行时 so that 我能先改数据结构与类别定义，而不需要一次性重写现有抽取流程。

## Acceptance Criteria

- [ ] 文档 MUST 声明 `large` 主要来自 `core_items`，`medium` 来自 `support_items` 与少量清晰主锚点，`small` 只来自 `visible_small_items`，`hanging` 只来自低权重 `conditional_items`。
- [ ] 映射表 MUST 说明每个 bucket 的允许来源和禁止来源，尤其 `small` 与 `hanging` MUST NOT 接收 `blocked_or_risky` 条目。
- [ ] 兼容说明 MUST 保留当前编号输入与分栏覆盖语法，不要求用户改写已有输入习惯。
- [ ] 兼容说明 MUST 明确 `draw_history` 仍按旧 box id 与 bucket key 工作，任何未来迁移都应视为后续实现议题。

## Traces

- **Goal**: [G-003](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-four-bucket-compatibility.md) (if applicable)
- **Implemented by**: [EPIC-003](../epics/EPIC-003-compatibility-mapping.md) (added in Phase 5)
