---
session_id: SPEC-2026-04-29-game-content-extraction-four-pool-refactor
phase: 7
document_type: issue-export-report
status: complete
generated_at: 2026-04-29T00:00:00+08:00
stepsCompleted:
  - epic-to-issue-mapping
version: 1
dependencies:
  - epics/_index.md
  - readiness-report.md
---

# Issue Export Report

## Summary

未实际创建 GitHub issue。本报告提供可手动创建或交给 workflow-plan 使用的 Epic issue 映射。

## Issue Mapping

| Proposed Issue | Epic | Wave | Priority | Labels |
|----------------|------|------|----------|--------|
| 四池数据模型与兼容映射 | [EPIC-001](epics/EPIC-001-four-pool-data-model.md) | wave-1 | Must | `spec-generated`, `blind-box`, `data-model` |
| 三类试点内容重写 | [EPIC-002](epics/EPIC-002-pilot-content-rewrite.md) | wave-2 | Must | `spec-generated`, `blind-box`, `content-quality` |
| 回归测试与文档同步 | [EPIC-003](epics/EPIC-003-validation-and-doc-sync.md) | wave-3 | Must | `spec-generated`, `blind-box`, `tests`, `docs` |

## Dependency Map

```mermaid
graph LR
    ISSUE1[四池数据模型与兼容映射] --> ISSUE2[三类试点内容重写]
    ISSUE2 --> ISSUE3[回归测试与文档同步]
```

## Suggested Issue Bodies

### 四池数据模型与兼容映射

Implement EPIC-001 from `SPEC-2026-04-29-game-content-extraction-four-pool-refactor`: migrate pilot bundles to four pool keys and preserve `BLIND_BOXES` four-column compatibility.

### 三类试点内容重写

Implement EPIC-002: rewrite 15 `桌面+学习`, 16 `海底+潜水`, and 17 `公园+野餐` with high-quality `scene_expansion_items`.

### 回归测试与文档同步

Implement EPIC-003: update schema tests, blocked pattern tests, and required docs.

## Handoff Recommendation

Use `workflow-plan` rather than manual issue creation for this local repo task, because the next step is a scoped local data/test/docs change.
