---
id: ADR-003
status: Accepted
traces_to: [REQ-003, REQ-006, NFR-R-001]
date: 2026-04-29T00:00:00+08:00
---

# ADR-003: 风险内容迁移为测试规则

## Context

`blocked_or_risky` 保存风险条目会让“不可用内容”继续出现在主数据模型中。即使不进入默认输出，也会给维护者错误信号。

## Decision

删除 `blocked_or_risky` 候选池，使用 `blocked_patterns` / `blocked_terms` 在测试层阻止风险模式进入默认池。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 测试规则 | 不会误当候选，质量门槛硬 | 运行时暂不复用 |
| excluded 池 | 可记录负例 | 仍容易被误读为数据池 |
| 保留 blocked_or_risky | 改动小 | 问题根源未解决 |

## Consequences

- **Positive**: 风险内容不再污染内容模型。
- **Negative**: 若未来运行时也需过滤，需要抽出共享常量。
- **Risks**: 禁用词过宽可能误杀合法物品，需保持精确。

## Traces

- **Requirements**: [REQ-003](../requirements/REQ-003-remove-risky-pool.md), [REQ-006](../requirements/REQ-006-regression-tests-docs.md), [NFR-R-001](../requirements/NFR-R-001-regression-prevention.md)
- **Implemented by**: [EPIC-003](../epics/EPIC-003-validation-and-doc-sync.md)
