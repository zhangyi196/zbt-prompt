---
session_id: SPEC-2026-04-29-game-content-extraction-blind-box-library-refactor
phase: 3
document_type: requirements
status: complete
generated_at: 2026-04-29T00:00:00+08:00
stepsCompleted:
  - load-context
  - expand-requirements
  - codex-review
version: 1
dependencies:
  - ../product-brief.md
  - ../refined-requirements.json
id: REQ-007
type: functional
priority: Should
traces_to:
  - G-005
---

# REQ-007: 规范写库审查、实施交接与文档同步

**Priority**: Should

## Description

内容库重构 SHOULD 配套固定的写库审查步骤、实施交接边界和文档同步清单。该需求保证试点一旦进入实现，不会只改数据而遗漏维护指南、仓库说明和忽略规则。

## User Story

As a 内容维护者, I want to 在每次落地时按统一清单同步代码周边文档 so that 新内容模型不会只存在于数据文件里，后续维护者也能沿用同一规则。

## Acceptance Criteria

- [ ] 实施阶段 SHOULD 为每个试点类别执行固定审查流程，至少包含结构校验、30 次抽样、人工 spot check 和风险回看。
- [ ] 当实现落地影响盲盒库、维护说明或缓存忽略规则时，交接清单 MUST 包含 `agents.md`、`Game content extraction/CLAUDE.md`、`README.md`、`.gitignore` 的同步义务。
- [ ] 若 `.gitignore` 新增命中已跟踪缓存或构建产物，交接说明 MUST 要求同步取消跟踪清理，避免脏缓存再次进入仓库。
- [ ] PRD SHOULD 把文档同步视为实施验收的一部分，而不是可选补充项。

## Traces

- **Goal**: [G-005](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-007](../architecture/ADR-007-doc-sync-guardrails.md) (if applicable)
- **Implemented by**: [EPIC-007](../epics/EPIC-007-authoring-and-doc-sync.md) (added in Phase 5)
