---
id: REQ-005
type: functional
priority: Must
traces_to: [G-001, G-002]
status: complete
---

# REQ-005: 三个试点盒必须按四池模型重写

**Priority**: Must

## Description

15 `桌面+学习`、16 `海底+潜水`、17 `公园+野餐` 必须使用四池模型重写内容。每个池都必须真实、常见、边界清楚、可单独圈选、场景强相关。

## User Story

As a 内容审核者, I want 三个试点都有完整四池样板 so that 后续扩展 20 类时有明确参照。

## Acceptance Criteria

- [ ] 三个试点均包含非空 `core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`。
- [ ] 桌面和野餐示例中的方向被纳入或等价体现。
- [ ] 海底试点也必须给出无动物本体、无透明发光反光、无细绳网格的场景扩展物。
- [ ] 人工抽样 30 次时明显不适合项目标低于 10%。

## Traces

- **Goal**: [G-001](../product-brief.md#goals--success-metrics), [G-002](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-001](../architecture/ADR-001-four-pool-data-model.md), [ADR-002](../architecture/ADR-002-scene-expansion-default-safe.md)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-pilot-content-rewrite.md)
