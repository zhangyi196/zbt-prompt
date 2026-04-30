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
id: REQ-005
type: functional
priority: Must
traces_to: [G-004]
status: complete
---

# REQ-005: 保持运行时兼容视图和现有 `unittest` 契约

**Priority**: Must

## Description

第四池重写 MUST 保持 `BLIND_BOX_ITEM_POOL_BUNDLES`、运行时兼容视图和现有 `unittest` 的结构契约不变。实现 MUST 证明新语义只影响静态内容和质量规则，不要求修改四池 key、兼容映射列结构、draw history 语义或 UI 工作流。

## User Story

As a Game content extraction tool maintainer, I want the rewrite to preserve runtime compatibility so that existing extraction flows and tests continue to work without schema migration.

## Acceptance Criteria

- [ ] 现有 `unittest` MUST 继续覆盖 20 个场景、四池结构、每池 50 条唯一项和兼容映射关系。
- [ ] 第四池重写 MUST NOT 改变 `BLIND_BOXES` 的 `large` / `medium` / `small` / `hanging` 兼容输出结构。
- [ ] 第四池重写 MUST NOT 要求改动 UI、draw history 键结构、动物池或表情池。
- [ ] 若新增质量校验测试，测试套件 MUST 与现有 `unittest` 一起作为同一回归基线运行。

## Traces

- **Goal**: [G-004](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-005](../architecture/ADR-005-runtime-compatibility.md)
- **Implemented by**: [EPIC-003](../epics/EPIC-003-quality-boundary-and-regression-gates.md)
