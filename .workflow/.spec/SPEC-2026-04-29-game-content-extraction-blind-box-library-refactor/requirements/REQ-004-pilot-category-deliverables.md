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
id: REQ-004
type: functional
priority: Must
traces_to:
  - G-004
  - G-005
---

# REQ-004: 交付三个试点类别的统一样板

**Priority**: Must

## Description

首轮重构 MUST 以 `桌面+学习`、`海底+潜水`、`公园+野餐` 三个试点类别为唯一交付样板。每个试点 MUST 同时包含五层池内容、四栏兼容映射、审查记录入口和风险说明，作为后续扩展到其余 17 类的基线。

## User Story

As a 内容维护者, I want to 先用三个覆盖面不同的试点验证新模型 so that 我可以在全量扩库前发现日常桌面、户外承载和特殊主题的主要风险。

## Acceptance Criteria

- [ ] 三个试点类别 MUST 全部具备五层池字段，且任何一层为空都必须在审查记录里说明原因。
- [ ] `桌面+学习` MUST 覆盖日常高频桌面物与学习承载物；`公园+野餐` MUST 覆盖户外成组小物与承载关系；`海底+潜水` MUST 覆盖特殊主题但排除动物本体、发光、反光与透明依赖。
- [ ] 每个试点 MUST 生成一份可回写到 `large`、`medium`、`small`、`hanging` 的映射说明，且映射后仍可参与现有抽取流程。
- [ ] 全量扩展决策 MUST 以后续抽样通过为前提；在试点未达标前，其余 17 类 MUST NOT 进入全量重写阶段。

## Traces

- **Goal**: [G-004](../product-brief.md#goals--success-metrics)
- **Goal**: [G-005](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-004](../architecture/ADR-004-pilot-first-rollout.md) (if applicable)
- **Implemented by**: [EPIC-004](../epics/EPIC-004-pilot-categories.md) (added in Phase 5)
