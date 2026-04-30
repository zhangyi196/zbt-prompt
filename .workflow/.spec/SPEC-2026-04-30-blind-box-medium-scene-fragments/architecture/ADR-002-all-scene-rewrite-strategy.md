---
id: ADR-002
status: Accepted
traces_to: [REQ-002]
date: 2026-04-30T14:20:00+08:00
---

# ADR-002: 对 20 个场景执行全量重写而非 pilot-only 扩写

## Context

需求要求 20 个场景都具备合规的 `scene_expansion_items`，且每场景精确 50 条唯一项。现有数据中 pilot 概念只用于历史推进，不适合作为本轮语义落地的范围边界。

## Decision

本轮实施采用全量重写策略：20 个场景全部按同一规则模型重建第四池，每场景保留自身语义，同时满足 50 条唯一项，不允许通过保留旧不合格条目来“渐进兼容”。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 全量重写 20 场景 | 不会长期并存双语义，回归结果清楚 | 一次性工作量较大 |
| 只先改 pilot 场景 | 初期风险小 | 旧第四池语义继续存在，需求无法闭环 |
| 场景模板化批量替换 | 速度快 | 会丢失场景专属语义，违反需求 |

## Consequences

- **Positive**: 交付后仓库只有一套第四池语义。
- **Negative**: 需要更严格的唯一性和可读性审查。
- **Risks**: 为凑够 50 条而引入同质化模板词，需用规则和评审限制。

## Traces

- **Requirements**: [REQ-002](../requirements/REQ-002-all-scene-rewrite-and-uniqueness.md)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-full-scene-expansion-rewrite.md)
