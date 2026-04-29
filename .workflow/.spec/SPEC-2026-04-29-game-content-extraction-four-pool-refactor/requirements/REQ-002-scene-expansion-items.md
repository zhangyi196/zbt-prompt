---
id: REQ-002
type: functional
priority: Must
traces_to: [G-002]
status: complete
---

# REQ-002: `scene_expansion_items` 必须是默认安全的场景扩展物

**Priority**: Must

## Description

`scene_expansion_items` 必须承载第四类内容：中等以上体量、常见、边界清楚、可单独圈选、无需图像锚点、能自然扩展当前场景变化的物品。它不是条件池、不是悬挂池、不是风险池。

## User Story

As a 盲盒抽取工具用户, I want 第四类物品能增加场景变化但不依赖图像条件 so that 输出更丰富且仍然可用于游戏。

## Acceptance Criteria

- [ ] `scene_expansion_items` 不包含 `显示器下方`、`白板磁吸`、`伞杆`、`挂点`、`桌侧` 等不可验证图像条件语义。
- [ ] 条目是中等以上体量的完整物品，不是标签、夹片、细绳、边线或痕迹。
- [ ] 条目与场景强相关，但不重复核心物和配套物的主要职责。
- [ ] 桌面试点包含类似 `桌面日历`、`桌面小风扇`、`护眼书架`、`桌面收纳抽屉` 的扩展物。
- [ ] 野餐试点包含类似 `折叠野餐桌`、`便携冷藏箱`、`户外收纳箱`、`野餐遮阳布` 的扩展物。

## Traces

- **Goal**: [G-002](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-002](../architecture/ADR-002-scene-expansion-default-safe.md)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-pilot-content-rewrite.md)
