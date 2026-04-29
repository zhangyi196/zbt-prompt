---
id: ADR-001
status: Accepted
traces_to: [REQ-001, REQ-002, REQ-003, NFR-U-001]
date: 2026-04-29T00:00:00+08:00
---

# ADR-001: 五层池条目必须是具体物品

## Context

用户反馈指出，条件池和风险池出现了不可用内容。根因是五层池没有统一执行“具体物品”底线，导致小附属件和视觉现象进入池层。

## Decision

所有五层池条目都必须是具体物品、动物本体或物品组。非物品现象、痕迹、边线、阴影、气泡、微小颗粒不得进入任何五层池。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 统一 object-only 规则 | 简单、可测试、便于维护 | 需要清理已有试点条目 |
| 只修 blocked_or_risky | 改动更小 | conditional_items 仍会保留低价值小件 |
| 删除 conditional/blocked 两层 | 彻底避免误用 | 失去条件启用和风险审查价值 |

## Consequences

- **Positive**: 所有内容池都可被理解为游戏画面中的对象。
- **Negative**: 部分原先“风险原因”不能再作为条目保存。
- **Risks**: 需要测试帮助维护者持续遵守。

## Traces

- **Requirements**: [REQ-001](../requirements/REQ-001-conditional-items-visible-object.md), [REQ-002](../requirements/REQ-002-blocked-risky-concrete-object.md), [REQ-003](../requirements/REQ-003-forbidden-pattern-validation.md), [NFR-U-001](../requirements/NFR-U-001-maintainer-clarity.md)
