---
session_id: SPEC-2026-04-29-game-content-extraction-blind-box-library-refactor
phase: 3
document_type: requirements
status: complete
generated_at: 2026-04-29T00:00:00+08:00
stepsCompleted:
  - load-context
  - expand-requirements
  - codex-review
version: 1
dependencies:
  - ../product-brief.md
  - ../refined-requirements.json
  - ../discovery-context.json
id: REQ-005
type: functional
priority: Must
traces_to:
  - G-004
  - G-005
---

# REQ-005: 建立默认输出质量与风险隔离规则

**Priority**: Must

## Description

规范 MUST 把“默认可抽质量”转化为显式门槛，而不是口头原则。试点和后续类别都 MUST 使用同一套风险隔离表、抽样规则和通过阈值，确保 `blocked_or_risky` 与低可见条目不会混入默认输出。

## User Story

As a 工具使用者, I want to 默认抽到更清楚、更可圈选的物品 so that 我不需要二次筛掉透明反光、细碎痕迹或没有承载面的无效条目。

## Acceptance Criteria

- [ ] 质量规则 MUST 要求默认条目满足“真实、常见、边界清楚、可单独圈选、强场景相关”五项标准。
- [ ] 风险规则 MUST 明确列出不得进入默认输出的对象类型，包括灯、镜、透明反光物、细绳、流苏、微型痕迹、边线类变化和动物本体。
- [ ] 试点验收 MUST 使用 30 次人工抽样，明显不适合项占比 MUST 小于 10%，且 `blocked_or_risky` 泄漏次数 MUST 等于 0。
- [ ] 若 `item_states.py` 或其他状态修饰会把安全条目推向反光、透明或不稳定描述，实施方案 MUST 记录该冲突并在落地时处理，MUST NOT 在 PRD 中直接放宽质量门槛。

## Traces

- **Goal**: [G-004](../product-brief.md#goals--success-metrics)
- **Goal**: [G-005](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-005](../architecture/ADR-005-quality-gates.md) (if applicable)
- **Implemented by**: [EPIC-005](../epics/EPIC-005-quality-validation.md) (added in Phase 5)
