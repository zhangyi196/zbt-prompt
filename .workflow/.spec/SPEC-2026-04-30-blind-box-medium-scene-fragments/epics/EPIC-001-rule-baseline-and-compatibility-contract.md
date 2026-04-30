---
session_id: SPEC-2026-04-30-blind-box-medium-scene-fragments
phase: 5
document_type: epics
kind: epic
status: complete
generated_at: 2026-04-30T15:20:00+08:00
stepsCompleted:
  - load-phase-context
  - epic-decomposition
  - codex-review
version: 1
dependencies:
  - ../product-brief.md
  - ../requirements/_index.md
  - ../architecture/_index.md
id: EPIC-001
priority: Must
mvp: true
size: M
requirements: [REQ-001, REQ-003, REQ-005, REQ-007]
architecture: [ADR-001, ADR-003, ADR-005, ADR-007]
epic_dependencies: []
---

# EPIC-001: 规则基线与兼容契约

**Priority**: Must
**MVP**: Yes
**Estimated Size**: M

## Description

先把 `scene_expansion_items` 的目标语义写成正式、可测试、可复用的规则基线，包括 allowed families、forbidden large roots、forbidden tiny roots、升级后信息载体例外和统一反馈字段。该 Epic 同时锁定 `BLIND_BOX_ITEM_POOL_BUNDLES`、`BLIND_BOXES` 与 `BLIND_BOX_COMPATIBILITY_MAPPING` 的硬边界，避免后续重写时以“顺手改结构”的方式绕过内容问题。

## Requirements

- [REQ-001](../requirements/REQ-001-formal-medium-scene-fragment-model.md): 正式定义 medium-scale scene fragment 模型
- [REQ-003](../requirements/REQ-003-scale-quality-validation.md): 建立超大主体与超小主体质量校验
- [REQ-005](../requirements/REQ-005-runtime-and-unittest-compatibility.md): 保持运行时兼容视图和现有 `unittest` 契约
- [REQ-007](../requirements/REQ-007-maintainer-feedback-and-review.md): 向维护者提供可定位的校验反馈和审查流程

## Architecture

- [ADR-001](../architecture/ADR-001-medium-scene-fragment-model.md): 固定 medium-scale scene fragment 内容模型
- [ADR-003](../architecture/ADR-003-scale-quality-validation.md): 用质量闸门拦截超大与超小主体
- [ADR-005](../architecture/ADR-005-runtime-compatibility.md): 保持四池事实源与运行时四栏兼容契约
- [ADR-007](../architecture/ADR-007-maintainer-review-loop.md): 固定维护者审查闭环

## Dependencies

无前置 Epic。该 Epic 为后续所有实现提供统一规则和兼容边界。

## Stories

### STORY-001-001: 固化第四池正式规则集

**User Story**: As a Prompt maintainer, I want `scene_expansion_items` 的 formal rule set 被明确定义 so that 20 场景重写时不会再次回退到模糊语义。

**Acceptance Criteria**:

- [ ] 规则文本明确列出 5 类 allowed families，并说明它们为何属于 medium-scale scene fragment。
- [ ] 规则文本明确写出尺度上界、尺度下界和“第一眼可见、可圈选、可承载场景状态”的判定语句。
- [ ] 规则集说明升级后信息载体只作为例外入口，不能重新演变为卡片/标签池。

**Size**: M
**Traces to**: [REQ-001](../requirements/REQ-001-formal-medium-scene-fragment-model.md)

---

### STORY-001-002: 定义 forbidden roots 与例外准入表

**User Story**: As a 测试维护者, I want large/tiny forbidden roots 和少量例外项被统一整理 so that 规模校验和人工复核使用同一判断标准。

**Acceptance Criteria**:

- [ ] 规则集中列出柜、车、架、台、桌等超大主体主模式及其处理原则。
- [ ] 规则集中列出卡、标签、票据、编号牌等超小主体主模式及其处理原则。
- [ ] 升级后信息载体例外使用统一术语，并能映射到后续 `ValidationFinding` 的 `rule_id` 或恢复提示。

**Size**: S
**Traces to**: [REQ-001](../requirements/REQ-001-formal-medium-scene-fragment-model.md), [REQ-003](../requirements/REQ-003-scale-quality-validation.md)

---

### STORY-001-003: 锁定兼容契约与审查字段

**User Story**: As a Game content extraction tool maintainer, I want 兼容层边界和审查输出字段先被锁定 so that 后续内容改写不会顺带破坏运行时或测试入口。

**Acceptance Criteria**:

- [ ] 明确声明四池 key、20 场景入口、`large` / `medium` / `small` / `hanging` 兼容视图和 draw history 行为保持不变。
- [ ] 维护者反馈字段至少统一 `scene_name`、`pool_name`、`item_name`、`rule_id`、`severity`、`recovery_hint`。
- [ ] 审查顺序固定为“规则模型 -> 场景重写 -> 回归结果 -> 文档同步”。

**Size**: S
**Traces to**: [REQ-005](../requirements/REQ-005-runtime-and-unittest-compatibility.md), [REQ-007](../requirements/REQ-007-maintainer-feedback-and-review.md)
