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
id: EPIC-003
priority: Must
mvp: true
size: M
requirements: [REQ-003, REQ-004, REQ-005, REQ-007, NFR-R-001]
architecture: [ADR-003, ADR-004, ADR-005, ADR-007]
epic_dependencies: [EPIC-001, EPIC-002]
---

# EPIC-003: 质量闸门、边界校验与回归基线

**Priority**: Must
**MVP**: Yes
**Estimated Size**: M

## Description

在 20 场景重写完成后，把超大主体、超小主体、跨池角色冲突和兼容回归统一纳入 `unittest` 基线。该 Epic 的目标不是再写内容，而是让失败能定位到具体 `scene_name`、`item_name` 和规则类型，并在发布前给维护者稳定反馈。

## Requirements

- [REQ-003](../requirements/REQ-003-scale-quality-validation.md): 建立超大主体与超小主体质量校验
- [REQ-004](../requirements/REQ-004-pool-boundary-validation.md): 校验 `scene_expansion_items` 与其余三池的边界
- [REQ-005](../requirements/REQ-005-runtime-and-unittest-compatibility.md): 保持运行时兼容视图和现有 `unittest` 契约
- [REQ-007](../requirements/REQ-007-maintainer-feedback-and-review.md): 向维护者提供可定位的校验反馈和审查流程
- [NFR-R-001](../requirements/NFR-R-001-regression-compatibility.md): 回归兼容性

## Architecture

- [ADR-003](../architecture/ADR-003-scale-quality-validation.md): 用质量闸门拦截超大与超小主体
- [ADR-004](../architecture/ADR-004-pool-boundary-rules.md): 用职责边界区分四池
- [ADR-005](../architecture/ADR-005-runtime-compatibility.md): 保持四池事实源与运行时四栏兼容契约
- [ADR-007](../architecture/ADR-007-maintainer-review-loop.md): 固定维护者审查闭环

## Dependencies

- [EPIC-001](EPIC-001-rule-baseline-and-compatibility-contract.md): 需要先有统一规则和失败字段。
- [EPIC-002](EPIC-002-full-scene-expansion-rewrite.md): 需要先有 20 场景最终候选，才能执行全量回归。

## Stories

### STORY-003-001: 实现规模质量闸门

**User Story**: As a 测试维护者, I want 质量规则自动拦住超大和超小主体 so that 第四池不会在后续维护中静默回退。

**Acceptance Criteria**:

- [ ] 规则覆盖超大主体回流、超小主体回流和升级后信息载体例外三类情况。
- [ ] 失败输出至少包含 `scene_name`、`pool_name`、`item_name`、`rule_id`、`severity`、`recovery_hint`。
- [ ] 20 个场景第四池全部经过同一套质量闸门，且能用 `subTest` 或等效机制定位失败来源。

**Size**: M
**Traces to**: [REQ-003](../requirements/REQ-003-scale-quality-validation.md), [REQ-007](../requirements/REQ-007-maintainer-feedback-and-review.md)

---

### STORY-003-002: 实现跨池边界校验

**User Story**: As a Prompt maintainer, I want 第四池与其余三池的职责冲突被明确指出 so that 我知道应删词还是迁回其他池。

**Acceptance Criteria**:

- [ ] 边界校验能区分更像 `core_items`、`support_items` 或 `visible_small_items` 的冲突项。
- [ ] 每条冲突输出都给出 `conflicting_pool` 和 `resolution_hint`。
- [ ] 校验规则使用“中号片段承载场景状态”的同一标准，不允许按场景各自漂移。

**Size**: M
**Traces to**: [REQ-004](../requirements/REQ-004-pool-boundary-validation.md), [REQ-007](../requirements/REQ-007-maintainer-feedback-and-review.md)

---

### STORY-003-003: 保持兼容映射与旧回归契约

**User Story**: As a 桌面工具用户, I want 运行时四栏输出和现有断言继续有效 so that 数据语义升级不会改变工具使用方式。

**Acceptance Criteria**:

- [ ] `BLIND_BOX_ITEM_POOL_BUNDLES` 仍保持 20 个场景、四池 key 和每池 50 条唯一项。
- [ ] `BLIND_BOX_COMPATIBILITY_MAPPING` 继续声明 `large`、`medium`、`small`、`hanging` 的既有来源关系。
- [ ] 现有 `unittest` 基线与新增质量/边界断言可以在同一回归入口执行。

**Size**: S
**Traces to**: [REQ-005](../requirements/REQ-005-runtime-and-unittest-compatibility.md), [NFR-R-001](../requirements/NFR-R-001-regression-compatibility.md)
