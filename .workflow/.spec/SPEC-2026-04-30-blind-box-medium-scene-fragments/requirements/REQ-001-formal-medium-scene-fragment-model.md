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
id: REQ-001
type: functional
priority: Must
traces_to: [G-001]
status: complete
---

# REQ-001: 正式定义 medium-scale scene fragment 模型

**Priority**: Must

## Description

规格 MUST 将 `scene_expansion_items` 定义为“medium-scale scene fragment”，并把该定义写成可复用的正式规则，而不是留在 brainstorm 描述层。该模型 MUST 同时定义允许的 5 类主体家族、尺度上界、尺度下界、与其余三池的角色区分，以及“升级后的信息载体”作为例外的准入方式。

## User Story

As a prompt maintainer, I want a formal fourth-pool model so that I can rewrite and review scene items without falling back to large furniture, storage objects, cards, or labels.

## Acceptance Criteria

- [ ] 规则文档 MUST 明确 5 类允许家族：活动结果件、中号任务面、铺垫界面件、成组阵列件、完整成果件。
- [ ] 规则文档 MUST 明确禁止把柜、车、架、桌、台等超大主体作为第四池主模式。
- [ ] 规则文档 MUST 明确禁止把小卡、标签、票据、书签、单张等超小主体作为第四池独立主模式。
- [ ] 规则文档 MUST 说明“升级后的信息载体”只能以板、面、页组、记录面、排列表面等中号载体形态进入第四池。

## Traces

- **Goal**: [G-001](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-001](../architecture/ADR-001-medium-scene-fragment-model.md)
- **Implemented by**: [EPIC-001](../epics/EPIC-001-rule-baseline-and-compatibility-contract.md)
