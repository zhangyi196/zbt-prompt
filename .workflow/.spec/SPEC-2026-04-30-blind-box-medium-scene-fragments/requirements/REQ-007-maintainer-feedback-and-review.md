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
id: REQ-007
type: functional
priority: Should
traces_to: [G-005]
status: complete
---

# REQ-007: 向维护者提供可定位的校验反馈和审查流程

**Priority**: Should

## Description

作为 library 规格的开发体验补充，质量校验和人工审查 SHOULD 让维护者在最少上下文切换下完成复核。失败信息 SHOULD 使用统一字段、统一严重级别和统一修复建议术语；审查流程 SHOULD 支持先看模型、再看场景列表、最后看文档同步结果的顺序。

## User Story

As a library maintainer, I want clear feedback and a predictable review sequence so that I can fix invalid items quickly and keep future edits consistent.

## Acceptance Criteria

- [ ] 校验输出 SHOULD 使用统一严重级别，例如 `error`、`warning`、`info`。
- [ ] 校验输出 SHOULD 复用 glossary 中的规范术语，不混用“容器替代品”“卡片池”等旧说法。
- [ ] 审查流程 SHOULD 至少覆盖三步：规则模型复核、20 场景内容复核、稳定文档同步复核。
- [ ] 审查说明 SHOULD 告诉维护者优先执行“删超大主体、删超小主体、处理跨池冲突、最后补文档”的修复顺序。

## Traces

- **Goal**: [G-005](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-007](../architecture/ADR-007-maintainer-review-loop.md)
- **Implemented by**: [EPIC-004](../epics/EPIC-004-doc-sync-and-maintainer-review.md)
