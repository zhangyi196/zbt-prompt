---
id: REQ-004
type: functional
priority: Must
traces_to: [G-004]
status: complete
---

# REQ-004: 保持 `BLIND_BOXES` 四栏兼容视图

**Priority**: Must

## Description

虽然底层试点数据迁移为四类内容池，运行时 `BLIND_BOXES` 仍必须提供 `name`、`large`、`medium`、`small`、`hanging` 五个字段，以保持 UI、输入覆盖语法和历史权重逻辑稳定。

## User Story

As a 桌面工具用户, I want 工具界面和输入方式保持不变 so that 数据重构不会打断当前使用流程。

## Acceptance Criteria

- [ ] `BLIND_BOXES[15]`、`BLIND_BOXES[16]`、`BLIND_BOXES[17]` 仍包含 `name`、`large`、`medium`、`small`、`hanging`。
- [ ] `large` 至少来源于 `core_items`，并可加入 `scene_expansion_items`。
- [ ] `medium` 来源于 `support_items` 和部分 `core_items`。
- [ ] `small` 来源于 `visible_small_items`。
- [ ] `hanging` 不得通过细绳、挂饰、边线或锚点依赖物强制填充。

## Traces

- **Goal**: [G-004](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-004](../architecture/ADR-004-legacy-mapping-preservation.md)
- **Implemented by**: [EPIC-001](../epics/EPIC-001-four-pool-data-model.md)
