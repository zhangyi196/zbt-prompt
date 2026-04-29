---
id: ADR-005
status: Accepted
traces_to: [REQ-003, REQ-006, NFR-P-001, NFR-S-001]
date: 2026-04-29T00:00:00+08:00
---

# ADR-005: 保持旧输入与历史语义

## Context

用户已经习惯逗号输入、旧编号和四栏勾选。`draw_history.json` 的 `item_pools` 语义也与 box id 和四栏 key 绑定。若本阶段同时改变输入、历史和数据模型，会让内容质量优化变成高风险运行时重构。

## Decision

本阶段不迁移 `draw_history.json`，不改变逗号输入语法，不改变动物池和表情历史。新类别与五层池先通过兼容映射输出旧四栏结果；旧编号可作为别名或映射入口保留，直到未来明确 UI 迁移方案。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 保持旧输入和历史 | 用户无感迁移，回归风险低。 | 新 20 类的 UI 展示需要后续设计。 |
| 立即切换到新编号 | 模型更清晰。 | 破坏用户习惯和历史 key，可能需要迁移脚本。 |
| 新旧两套历史并行 | 可精细追踪新模型使用次数。 | 增加状态复杂度，容易和动物/表情历史混淆。 |

## Consequences

- **Positive**: 内容库试点可以独立推进，不阻塞于 UI 和历史迁移。
- **Negative**: 兼容期内文档必须清楚说明“新模型”和“旧运行时”的关系。
- **Risks**: 若旧编号别名映射不透明，维护者可能误以为旧主题仍是主模型。

## Traces

- **Requirements**: [REQ-003](../requirements/REQ-003-four-bucket-compatibility-mapping.md), [REQ-006](../requirements/REQ-006-history-and-input-compatibility.md), [NFR-P-001](../requirements/NFR-P-001-compatibility-latency-budget.md), [NFR-S-001](../requirements/NFR-S-001-local-safety-boundary.md)
- **Implemented by**: Phase 5 epics.
