---
id: REQ-005
type: functional
priority: Should
traces_to: [G-005]
status: complete
---

# REQ-005: 同步池层定义文档

**Priority**: Should

## Description

实施完成后 SHOULD 同步项目文档，明确五层池都必须是具体物品，非物品禁用内容只能作为 forbidden patterns 或审查规则存在。

## User Story

As a 内容维护者, I want documentation to reflect the corrected rules so that future edits follow the same object-only standard.

## Acceptance Criteria

- [ ] `agents.md` 更新五层池物品化规则。
- [ ] `README.md` 更新试点修正说明。
- [ ] `Game content extraction/CLAUDE.md` 更新维护约束。
- [ ] `Game content extraction/README.md` 更新用户/维护说明。
- [ ] `.gitignore` 保持 workflow/spec 输出可跟踪策略。

## Traces

- **Goal**: [G-005](../product-brief.md#goals--success-metrics)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-validation-and-documentation.md)
