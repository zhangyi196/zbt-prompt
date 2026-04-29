---
id: ADR-003
status: Accepted
traces_to: [REQ-004, REQ-005, NFR-SC-001]
date: 2026-04-29T00:00:00+08:00
---

# ADR-003: 三个试点优先而非全量替换

## Context

全量替换 20 个类别会带来大量内容质量、兼容性和审查风险。需求指定 `桌面+学习`、`海底+潜水`、`公园+野餐` 作为首轮试点，用于覆盖高频桌面、特殊主题和户外承载场景。

## Decision

先完成三个试点类别的五层池、四栏映射和抽样审查。只有当每个试点都满足 schema 完整、风险物零泄漏、30 次抽样明显不适合项低于 10% 时，才建议扩展到更多类别。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 三个试点优先 | 风险可控，覆盖典型难点，便于复盘标准。 | 全量收益需要后续阶段逐步释放。 |
| 一次性重写 20 类 | 用户很快看到完整新入口。 | 容易扩大不适合项和兼容回归，审查成本高。 |
| 只做一个试点 | 最快启动。 | 无法验证特殊主题和户外承载关系。 |

## Consequences

- **Positive**: 能用真实抽样数据决定是否扩库，避免凭感觉全量替换。
- **Negative**: 需要暂时维护旧库与试点新库的边界。
- **Risks**: 若试点样本只看“条目数量”而不看输出质量，会误判模型有效。

## Traces

- **Requirements**: [REQ-004](../requirements/REQ-004-pilot-category-deliverables.md), [REQ-005](../requirements/REQ-005-quality-risk-validation.md), [NFR-SC-001](../requirements/NFR-SC-001-incremental-rollout-scale.md)
- **Implemented by**: Phase 5 epics.
