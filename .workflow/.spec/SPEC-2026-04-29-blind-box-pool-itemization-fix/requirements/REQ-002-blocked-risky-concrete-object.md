---
id: REQ-002
type: functional
priority: Must
traces_to: [G-002]
status: complete
---

# REQ-002: `blocked_or_risky` 必须只保留具体风险物

**Priority**: Must

## Description

`blocked_or_risky` MUST 只包含具体但默认禁用的风险物品。折线、擦痕、气泡、阴影、边线、碎叶点、石子、微小污点等非物品内容 MUST NOT 出现在该池层。

## User Story

As a 内容维护者, I want blocked_or_risky 只记录具体风险物 so that 风险池不会变成不可用视觉现象的垃圾桶。

## Acceptance Criteria

- [ ] 三类试点的 `blocked_or_risky` 每个条目都是具体物品、动物本体或物品组。
- [ ] `blocked_or_risky` 不包含折线、擦痕、气泡、阴影、边线、碎叶点、细小石子、微小污点、微小沙粒等非物品表达。
- [ ] 透明、反光、发光、动物本体、细绳、流苏等风险原因可以保留，但条目本体必须是具体对象。
- [ ] `blocked_or_risky` 仍不得映射到默认四栏输出。

## Traces

- **Goal**: [G-002](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-002](../architecture/ADR-002-blocked-risky-as-object-pool.md)
- **Implemented by**: [EPIC-001](../epics/EPIC-001-pilot-pool-content-correction.md)
