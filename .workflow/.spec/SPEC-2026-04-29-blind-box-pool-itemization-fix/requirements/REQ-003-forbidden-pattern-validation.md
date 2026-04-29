---
id: REQ-003
type: functional
priority: Must
traces_to: [G-003]
status: complete
---

# REQ-003: 建立非物品禁用模式校验

**Priority**: Must

## Description

实现 MUST 增加 `forbidden_patterns` 校验概念，禁止非物品禁用模式出现在 `core_items`、`support_items`、`visible_small_items`、`conditional_items`、`blocked_or_risky` 任一池层。

## User Story

As an App 维护者, I want tests to reject non-object patterns so that future content edits cannot reintroduce unusable phenomena.

## Acceptance Criteria

- [ ] 测试覆盖三类试点的所有五层池。
- [ ] 测试至少覆盖折线、擦痕、气泡、阴影、高光、边线、碎叶点、细小石子、微小污点、微小沙粒、漂浮细等模式。
- [ ] 若任何 forbidden pattern 出现在任一五层池，测试 MUST 失败。
- [ ] 完整 `python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'` MUST 通过。

## Traces

- **Goal**: [G-003](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-forbidden-pattern-validation.md)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-validation-and-documentation.md)
