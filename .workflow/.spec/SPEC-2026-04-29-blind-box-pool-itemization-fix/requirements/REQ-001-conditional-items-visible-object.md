---
id: REQ-001
type: functional
priority: Must
traces_to: [G-001]
status: complete
---

# REQ-001: `conditional_items` 必须改为条件启用的完整可见物品

**Priority**: Must

## Description

三类试点的 `conditional_items` MUST 从小标签、小卡片、小扣件、小贴片和边缘附属物，替换为中等以上体量、可单独圈选、只有在特定场景前提下才合理的具体物品。

## User Story

As a 工具使用者, I want conditional_items 也是完整可见物品 so that 条件启用时仍能用于游戏画面差异点。

## Acceptance Criteria

- [ ] `桌面+学习`、`海底+潜水`、`公园+野餐` 的 `conditional_items` 每个条目都是具体物品或物品组。
- [ ] `conditional_items` 不包含标签、卡片、扣件、贴片、边缘附属物等低价值小件。
- [ ] 每个 `conditional_items` 条目具备中等以上可见体量，可单独圈选。
- [ ] 条件语义来自场景前提，而不是靠“贴在/夹在/套在”包装小物。

## Traces

- **Goal**: [G-001](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-001](../architecture/ADR-001-pool-entry-object-only.md)
- **Implemented by**: [EPIC-001](../epics/EPIC-001-pilot-pool-content-correction.md)
