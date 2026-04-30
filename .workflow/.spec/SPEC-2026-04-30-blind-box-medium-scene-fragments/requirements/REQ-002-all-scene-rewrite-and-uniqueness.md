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
id: REQ-002
type: functional
priority: Must
traces_to: [G-002]
status: complete
---

# REQ-002: 全量重写 20 个 `scene_expansion_items` 并保持每场景 50 条唯一项

**Priority**: Must

## Description

实现方案 MUST 重写 20 个场景的 `scene_expansion_items`，并把每个场景的第四池收敛到正式模型内。每个场景的第四池 MUST 恰好保留 50 条唯一字符串，且重写不得通过复制近义词、轻微字面变化或退化为容器/卡片来凑数。

## User Story

As a Game content extraction tool maintainer, I want every scene to adopt the same fourth-pool contract so that the library stays structurally consistent across all 20 scene categories.

## Acceptance Criteria

- [ ] 20 个场景 MUST 全部存在 `scene_expansion_items`，不得只覆盖 pilot 场景。
- [ ] 每个场景的 `scene_expansion_items` MUST 精确包含 50 条唯一项。
- [ ] 重写后的第四池 MUST 保留场景专属语义，不得把 20 个场景写成同质化模板词表。
- [ ] 任何为了补足数量而引入的大型家具、收纳设施、微小卡片或标签条目 MUST 被视为不合格。

## Traces

- **Goal**: [G-002](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-002](../architecture/ADR-002-all-scene-rewrite-strategy.md)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-full-scene-expansion-rewrite.md)
