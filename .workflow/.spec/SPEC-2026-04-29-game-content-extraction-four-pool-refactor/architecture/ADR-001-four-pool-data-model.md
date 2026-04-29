---
id: ADR-001
status: Accepted
traces_to: [REQ-001, REQ-005, NFR-U-001]
date: 2026-04-29T00:00:00+08:00
---

# ADR-001: 四类内容池作为试点数据源

## Context

当前五层模型中的 `conditional_items` 和 `blocked_or_risky` 与工具能力不匹配。工具不能看图，无法判断条件物成立；风险池作为候选池也容易误导后续维护。

## Decision

三个试点 bundle 使用严格四池 schema：`core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`。旧条件池和风险池从候选内容模型中移除。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 四池模型 | 边界清晰，默认安全，适配当前工具 | 需要迁移测试和文档 |
| 保留五层模型 | 改动小 | 继续保留错误语义 |
| 引入结构化锚点字段 | 表达力强 | 工具没有图像事实来源 |

## Consequences

- **Positive**: 数据模型更贴近当前工具能力。
- **Negative**: 需要更新现有五层 schema 测试。
- **Risks**: 后续维护者可能把场景扩展物写成杂物池，需用文档和测试约束。

## Traces

- **Requirements**: [REQ-001](../requirements/REQ-001-four-pool-schema.md), [REQ-005](../requirements/REQ-005-pilot-content-rewrite.md), [NFR-U-001](../requirements/NFR-U-001-maintainer-clarity.md)
- **Implemented by**: [EPIC-001](../epics/EPIC-001-four-pool-data-model.md)
