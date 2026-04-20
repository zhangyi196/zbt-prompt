---
id: REQ-004
type: functional
priority: Should
traces_to: [G-002]
status: complete
---

# REQ-004: 模板编号选择

**Priority**: Should

## Description

系统 SHOULD 允许用户指定模板编号或选择随机策略。指定编号时，系统 MUST 根据单人/多人限制编号范围：单人 1-4，多人 5-8。

## User Story

As a 游戏内容设计者, I want to choose a template number so that I can reproduce a known expected output during review.

## Acceptance Criteria

- [ ] 单人输入可指定 1、2、3、4。
- [ ] 多人输入可指定 5、6、7、8。
- [ ] 用户示例可通过指定第 4 条稳定复现。
- [ ] 指定越界编号时提示合法范围。
- [ ] 随机策略只从合法范围中选择。

## Traces

- **Goal**: [G-002](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-parse-and-replace.md)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-parser-library.md)
