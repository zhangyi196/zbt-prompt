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
id: REQ-006
type: functional
priority: Must
traces_to: [G-005]
status: complete
---

# REQ-006: 对稳定文档执行同步检查

**Priority**: Must

## Description

实现方案 MUST 在第四池语义落地后检查 `agents.md`、`Game content extraction/agents.md`、`README.md` 和 `.gitignore` 是否需要同步更新。同步规则 MUST 保持精简，只记录稳定规则和必要入口，不复制 20 个场景的完整条目列表；若 `.gitignore` 新命中已跟踪缓存或构建产物，实施阶段 MUST 同步取消跟踪清理。

## User Story

As a repository maintainer, I want documentation sync checks baked into the change process so that stable rules remain accurate without bloating the docs.

## Acceptance Criteria

- [ ] 实施完成后 MUST 检查 `agents.md`、`Game content extraction/agents.md`、`README.md`、`.gitignore` 四个文件是否与新语义一致。
- [ ] `Game content extraction/agents.md` MUST 在需要时用一句或少量规则固定“中号场景片段”定义和禁区边界。
- [ ] `README.md` SHOULD 仅在用户可见行为变化时更新，不能为了内部规则重写而扩写。
- [ ] `.gitignore` 若命中新产生的缓存或构建产物，实施阶段 MUST 清理已跟踪项并保持仓库整洁。

## Traces

- **Goal**: [G-005](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-006](../architecture/ADR-006-documentation-sync-policy.md)
- **Implemented by**: [EPIC-004](../epics/EPIC-004-doc-sync-and-maintainer-review.md)
