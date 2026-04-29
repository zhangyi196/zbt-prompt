---
session_id: SPEC-2026-04-29-game-content-extraction-blind-box-library-refactor
phase: 7
document_type: issue-export-report
status: complete
generated_at: 2026-04-29T00:00:00+08:00
version: 1
dependencies:
  - spec-summary.md
  - epics/_index.md
---

# Issue Export Report

## Export Status

No GitHub issues were created in this run. The specification package is export-ready, and the table below can be used to create issues manually or by a later GitHub-enabled execution step.

## Proposed Issues

| Issue Title | Source Epic | Wave | Labels | Dependencies |
|-------------|-------------|------|--------|--------------|
| 实现盲盒 20 场景入口与五层池 schema | EPIC-001 | wave-1 | spec-generated, blind-box, content-model | None |
| 实现五层到四栏兼容映射与历史边界保护 | EPIC-002 | wave-1 | spec-generated, compatibility, blind-box | EPIC-001 |
| 交付三个盲盒试点类别内容样板 | EPIC-003 | wave-2 | spec-generated, pilot, content-quality | EPIC-001, EPIC-002 |
| 增加盲盒质量校验、审查记录与文档同步 | EPIC-004 | wave-2 | spec-generated, validation, docs | EPIC-002, EPIC-003 |

## Issue Body Template

```markdown
Source spec: .workflow/.spec/SPEC-2026-04-29-game-content-extraction-blind-box-library-refactor/

Read first:
- spec-summary.md
- epics/{EPIC_FILE}
- requirements/_index.md
- architecture/_index.md

Acceptance criteria:
- Follow the source Epic stories and linked requirements.
- Keep changes scoped to Game content extraction blind-box item extraction.
- Preserve local tkinter app boundaries and old input/history compatibility.
- Sync agents.md, Game content extraction/CLAUDE.md, README.md and .gitignore after execution.
```

## Phase 7 Result

| Field | Value |
|-------|-------|
| issues_created | 0 |
| export_mode | manual-ready |
| all_mvp_epics_covered | yes |
| spec_documents_resolve | yes |
