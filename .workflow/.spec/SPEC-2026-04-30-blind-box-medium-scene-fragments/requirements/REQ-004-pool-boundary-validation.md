---
session_id: SPEC-2026-04-30-blind-box-medium-scene-fragments
phase: 3
document_type: requirements
kind: functional
generated_at: 2026-04-30T13:10:00+08:00
stepsCompleted:
  - load-context
  - expand-requirements
  - codex-review
version: 1
dependencies:
  - ../product-brief.md
  - ../glossary.json
  - ../refined-requirements.json
id: REQ-004
type: functional
priority: Must
traces_to: [G-001, G-003]
status: complete
---

# REQ-004: 校验 `scene_expansion_items` 与其余三池的边界

**Priority**: Must

## Description

实现方案 MUST 验证 `scene_expansion_items` 与 `core_items`、`support_items`、`visible_small_items` 的边界。第四池 MUST 表示可见、可圈选、可承载场景状态的中号片段，而不是单个大型主体、单个工具配件、散落小件或未经升级的信息碎片。边界规则 MUST 支持指出冲突池及迁移建议。

## User Story

As a blind-box content maintainer, I want pool-boundary validation so that each item lands in the correct pool and the four-pool schema stays semantically stable.

## Acceptance Criteria

- [ ] 边界规则 MUST 说明 `core_items` 负责更大的主体或主角物，`support_items` 负责单个工具/托座/配件，`visible_small_items` 负责小而清晰的零散物，`scene_expansion_items` 负责中号场景片段。
- [ ] 对于与其他池角色重叠的条目，校验 MUST 输出冲突池名称和推荐迁移方向。
- [ ] 信息类词汇 MUST NOT 以原始微小形态通过第四池边界检查。
- [ ] “升级后的信息载体” MAY 通过第四池边界检查，但前提是条目本身仍是中号、首眼可见、可整体圈选的主体。

## Traces

- **Goal**: [G-001](../product-brief.md#goals--success-metrics), [G-003](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-004](../architecture/ADR-004-pool-boundary-rules.md)
- **Implemented by**: [EPIC-003](../epics/EPIC-003-quality-boundary-and-regression-gates.md)
