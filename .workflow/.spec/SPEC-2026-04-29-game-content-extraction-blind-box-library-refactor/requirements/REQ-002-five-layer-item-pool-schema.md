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
  - ../glossary.json
  - ../refined-requirements.json
id: REQ-002
type: functional
priority: Must
traces_to:
  - G-002
---

# REQ-002: 定义五层物品池结构与入池规则

**Priority**: Must

## Description

每个新类别 MUST 使用统一的五层物品池：`core_items`、`support_items`、`visible_small_items`、`conditional_items`、`blocked_or_risky`。每一层 MUST 同时定义用途、准入规则、排除规则和与其他层的边界，避免同一条目在没有理由的情况下跨层漂移。

## User Story

As a 内容维护者, I want to 按固定五层结构写库 so that 默认可抽条目、条件条目和风险条目有明确边界，后续审查不再依赖临场判断。

## Acceptance Criteria

- [ ] PRD MUST 为五层池分别定义字段名、职责说明和至少 2 条入池或排除规则。
- [ ] `visible_small_items` MUST 只收录成组、块状或有明确承载面的高可见小物，MUST NOT 收录微型痕迹、细线、边缝或难以圈选的碎项。
- [ ] `conditional_items` MUST 记录其依赖的承载、包裹或悬挂关系，脱离该关系时 MUST NOT 进入默认输出。
- [ ] `blocked_or_risky` MUST 收录灯、镜、透明反光物、细绳、流苏、动物本体、微型痕迹等高风险内容，并在文档中声明其默认隔离状态。

## Traces

- **Goal**: [G-002](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-002](../architecture/ADR-002-five-layer-item-pool.md) (if applicable)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-item-pool-schema.md) (added in Phase 5)
