---
id: REQ-003
type: functional
priority: Must
traces_to: [G-003]
status: complete
---

# REQ-003: `blocked_or_risky` 必须从候选内容池移除

**Priority**: Must

## Description

`blocked_or_risky` 不得继续作为候选物品池存在。风险内容应迁移为 `blocked_patterns` / `blocked_terms` 测试和校验规则，用于防止低质量内容进入默认池。

## User Story

As a 测试维护者, I want 风险内容以测试规则存在 so that 它不会被未来维护者误当成候选物品。

## Acceptance Criteria

- [ ] 试点 bundle 中不存在 `blocked_or_risky` key。
- [ ] 兼容映射中的 `excluded_sources` 不再依赖 `blocked_or_risky` 候选池。
- [ ] 测试覆盖细绳、流苏、边线、折线、擦痕、阴影、高光、反光、透明、发光、动物本体、微小等禁用模式。
- [ ] 禁用模式不进入 `large`、`medium`、`small`、`hanging` 默认输出。

## Traces

- **Goal**: [G-003](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-risk-as-validation.md)
- **Implemented by**: [EPIC-003](../epics/EPIC-003-validation-and-doc-sync.md)
