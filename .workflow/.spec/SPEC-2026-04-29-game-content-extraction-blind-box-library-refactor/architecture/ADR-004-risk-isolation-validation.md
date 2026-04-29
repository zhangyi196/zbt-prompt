---
id: ADR-004
status: Accepted
traces_to: [REQ-005, NFR-S-001]
date: 2026-04-29T00:00:00+08:00
---

# ADR-004: 风险物隔离与验证门禁

## Context

盲盒物品抽取当前的问题不只是类别不清，还包括透明反光物、灯具、细绳、流苏、动物本体、微型痕迹等条目进入默认输出。这些内容与仓库提示词禁区冲突，且常常不可安全放置或不可清晰圈选。

## Decision

将高风险条目统一放入 `blocked_or_risky`，并把“不得进入默认四栏输出”作为验证门禁。`item_states.py` 中与透明、反光、高光、阴影、灯光相关的状态词不得自动套用到盲盒物品默认输出；实现阶段优先采用盲盒专用白名单或过滤规则。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 显式风险池 + 验证门禁 | 风险可见，默认输出更稳。 | 需要额外维护风险清单和测试。 |
| 删除所有风险物 | 最干净。 | 失去审查记录，未来人工条件使用缺少依据。 |
| 保留风险物但靠人工判断 | 改动小。 | 默认抽取仍可能泄漏，无法稳定降低不适合率。 |

## Consequences

- **Positive**: 抽取结果更符合“第一眼可见、可圈选、可放置”的目标。
- **Negative**: 部分原有丰富度会下降，需要用更合规的主物和配套物补足。
- **Risks**: 风险词如果只靠字符串匹配，可能误杀合规物或漏掉同义表达。

## Traces

- **Requirements**: [REQ-005](../requirements/REQ-005-quality-risk-validation.md), [NFR-S-001](../requirements/NFR-S-001-local-safety-boundary.md)
- **Implemented by**: Phase 5 epics.
