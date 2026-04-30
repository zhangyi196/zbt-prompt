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
id: REQ-003
type: functional
priority: Must
traces_to: [G-003]
status: complete
---

# REQ-003: 建立超大主体与超小主体质量校验

**Priority**: Must

## Description

实现方案 MUST 为第四池建立可执行的质量校验，至少覆盖两类失败模式：超大主体回流和超小主体回流。校验规则 MUST 可定位到场景、池名、条目和违规则目，并 SHOULD 输出可执行的修复提示，帮助维护者判断是改词、删词，还是把条目迁移到其他池。

## User Story

As a prompt maintainer, I want the validation layer to catch oversized and undersized scene fragments so that regressions are blocked before they re-enter the library.

## Acceptance Criteria

- [ ] 校验 MUST 能识别柜、车、架、工作台、桌、台、收纳柜等超大主体词根或等价表达。
- [ ] 校验 MUST 能识别小卡、标签、票据、书签、单张、编号牌等超小主体词根或等价表达。
- [ ] 对于合规例外，校验 MUST 允许“价格板”“记录板”“展开页组”“标签排版面”等升级后的信息载体形式通过。
- [ ] 校验失败输出 MUST 包含 `scene_name`、`item_name`、`rule_id`、`message`、`recovery_hint` 五类信息。

## Traces

- **Goal**: [G-003](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-scale-quality-validation.md)
- **Implemented by**: [EPIC-003](../epics/EPIC-003-quality-boundary-and-regression-gates.md)
