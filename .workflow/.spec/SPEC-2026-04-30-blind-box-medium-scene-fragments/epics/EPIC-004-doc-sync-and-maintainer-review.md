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
id: EPIC-004
priority: Must
mvp: true
size: S
requirements: [REQ-006, REQ-007, NFR-M-001]
architecture: [ADR-006, ADR-007]
epic_dependencies: [EPIC-002, EPIC-003]
---

# EPIC-004: 文档同步与维护者审查闭环

**Priority**: Must
**MVP**: Yes
**Estimated Size**: S

## Description

把本轮 accepted 语义压缩成稳定、可复用、低漂移的维护说明，并把审查流程固定为可重复执行的顺序。该 Epic 不复制 20 场景长列表，只同步规则边界、入口文件和完成判定。

## Requirements

- [REQ-006](../requirements/REQ-006-documentation-sync-checks.md): 对稳定文档执行同步检查
- [REQ-007](../requirements/REQ-007-maintainer-feedback-and-review.md): 向维护者提供可定位的校验反馈和审查流程
- [NFR-M-001](../requirements/NFR-M-001-rule-maintainability.md): 规则可维护性

## Architecture

- [ADR-006](../architecture/ADR-006-documentation-sync-policy.md): 将文档同步限定为稳定规则边界
- [ADR-007](../architecture/ADR-007-maintainer-review-loop.md): 固定维护者审查闭环

## Dependencies

- [EPIC-002](EPIC-002-full-scene-expansion-rewrite.md): 需要先确定最终第四池写法。
- [EPIC-003](EPIC-003-quality-boundary-and-regression-gates.md): 需要先确认回归和失败字段稳定。

## Stories

### STORY-004-001: 同步根规则入口和工具规则入口

**User Story**: As a 未来维护者, I want `agents.md` 与 `Game content extraction/agents.md` 只保留稳定规则 so that 我能在 10 分钟内理解第四池边界。

**Acceptance Criteria**:

- [ ] 两份规则文档只记录 medium-scale scene fragment 模型、禁区和必要入口，不复制 20 场景条目长表。
- [ ] 文档术语与 glossary 保持一致，避免重新出现“容器替代品”“小卡片主体”等漂移表达。
- [ ] 新规则能直接支持“规则复核 -> 场景复核 -> 文档复核”的维护顺序。

**Size**: S
**Traces to**: [REQ-006](../requirements/REQ-006-documentation-sync-checks.md), [NFR-M-001](../requirements/NFR-M-001-rule-maintainability.md)

---

### STORY-004-002: 检查 README 与 `.gitignore` 的必要同步

**User Story**: As a repository maintainer, I want 用户入口文档和忽略规则只做必要更新 so that 仓库说明保持精简且不会误导实现范围。

**Acceptance Criteria**:

- [ ] `README.md` 只在用户可见行为或维护入口需要说明时更新，不复制 spec 细节。
- [ ] `.gitignore` 只在本轮新增缓存/构建产物时调整；若命中已跟踪缓存，则同步取消跟踪清理。
- [ ] 同步检查结果能明确标记“需要更新 / 无需更新”的判断依据。

**Size**: S
**Traces to**: [REQ-006](../requirements/REQ-006-documentation-sync-checks.md)

---

### STORY-004-003: 固定最终审查与交付判定

**User Story**: As a 发布前审核者, I want 最终审查顺序和完成条件被明确记录 so that 交付不会漏掉规则、测试或文档其中一环。

**Acceptance Criteria**:

- [ ] 审查顺序固定为“规则模型 -> 20 场景重写结果 -> 回归输出 -> 文档同步结果”。
- [ ] 完成条件明确包含 Must 需求覆盖、无 XL MVP 故事、回归可执行、入口文档精简同步。
- [ ] 复核记录使用统一术语描述失败级别和修复建议。

**Size**: S
**Traces to**: [REQ-006](../requirements/REQ-006-documentation-sync-checks.md), [REQ-007](../requirements/REQ-007-maintainer-feedback-and-review.md), [NFR-M-001](../requirements/NFR-M-001-rule-maintainability.md)
