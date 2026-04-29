---
id: NFR-U-001
type: non-functional
category: Usability
priority: Should
status: complete
---

# NFR-U-001: 维护者可读性

**Category**: Usability
**Priority**: Should

## Requirement

项目文档必须让后续维护者明确知道四类内容池的边界、`scene_expansion_items` 的写法、以及风险内容不再作为候选池。

## Metric & Target

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 必要文档同步 | 4 个核心文档全部更新 | 文档检查 |
| 旧概念状态 | 明确标记废弃或移除 | 文档搜索 |
| 示例覆盖 | 至少桌面、野餐示例 | 文档检查 |

## Traces

- **Goal**: [G-001](../product-brief.md#goals--success-metrics), [G-005](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-001](../architecture/ADR-001-four-pool-data-model.md)
