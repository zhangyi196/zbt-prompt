---
id: ADR-002
status: Accepted
traces_to: [REQ-002, REQ-004]
date: 2026-04-29T00:00:00+08:00
---

# ADR-002: `blocked_or_risky` 保留为具体风险物池

## Context

`blocked_or_risky` 的价值是记录哪些具体物品不应默认抽取。但当前它混入了折线、擦痕、气泡、阴影等非物品内容。

## Decision

短期保留字段名 `blocked_or_risky`，但将语义收窄为具体风险物池。动物本体、透明杯、玻璃瓶、发光灯、反光刀、细绳流苏类具体物品可以保留；非物品现象必须移出。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 保留字段名但收窄语义 | 兼容现有 spec 和测试，改动小 | 字段名仍略宽，需要文档解释 |
| 改名 `blocked_objects` | 语义更精确 | 会制造不必要的数据迁移和文档 churn |
| 删除风险池 | 最干净 | 失去对具体风险物的维护记录 |

## Consequences

- **Positive**: 风险池不再成为不可用现象列表。
- **Negative**: 未来若改名仍需一次小迁移。
- **Risks**: 文档若不同步，维护者可能继续按旧理解写库。

## Traces

- **Requirements**: [REQ-002](../requirements/REQ-002-blocked-risky-concrete-object.md), [REQ-004](../requirements/REQ-004-pilot-runtime-compatibility.md)
