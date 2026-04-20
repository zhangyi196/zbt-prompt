---
session_id: SPEC-2026-04-20-game-content-extraction-人物表情抽取窗口
phase: 7
document_type: issue-export-report
status: complete
generated_at: 2026-04-20T14:47:00+08:00
stepsCompleted:
  - epic-to-issue-mapping
  - wave-assignment
version: 1
dependencies:
  - epics/_index.md
  - readiness-report.md
---

# Issue Export Report: 人物表情抽取窗口

No external issues were created in this session. This report maps epics to issue-ready tasks and execution waves.

## Issue Mapping

| Proposed Issue | Epic | Wave | Priority | MVP | Status |
|----------------|------|------|----------|-----|--------|
| ISSUE-001 | [EPIC-002: 字段解析与表情库匹配](epics/EPIC-002-parser-library.md) | wave-1 | Must | Yes | ready |
| ISSUE-002 | [EPIC-001: 表情窗口 UI](epics/EPIC-001-expression-window-ui.md) | wave-1 | Must | Yes | ready |
| ISSUE-003 | [EPIC-003: 回填、复制与错误提示](epics/EPIC-003-output-errors.md) | wave-1 | Must | Yes | ready |
| ISSUE-004 | [EPIC-004: 打包与验证](epics/EPIC-004-packaging-tests.md) | wave-2 | Should | No | ready |

## Recommended Wave Plan

### wave-1 MVP

1. ISSUE-001: Implement parser, library loader, lookup, template selection.
2. ISSUE-002: Add Toplevel window and controls.
3. ISSUE-003: Wire output, copy behavior, and errors.

### wave-2 Hardening

4. ISSUE-004: Add regression tests and packaging path support.

## Issue Body Template

```markdown
## Context
Spec session: SPEC-2026-04-20-game-content-extraction-人物表情抽取窗口

## Scope
See linked epic and requirements.

## Acceptance Criteria
Copy from the epic stories.

## Spec Documents
- Product Brief: .workflow/.spec/SPEC-2026-04-20-game-content-extraction-人物表情抽取窗口/product-brief.md
- Requirements: .workflow/.spec/SPEC-2026-04-20-game-content-extraction-人物表情抽取窗口/requirements/_index.md
- Architecture: .workflow/.spec/SPEC-2026-04-20-game-content-extraction-人物表情抽取窗口/architecture/_index.md
- Epic: <epic path>
```

## Export Notes

- `ccw issue create` was not run.
- Proposed issues are ready for manual creation or workflow execution.
- Wave ordering starts with pure parsing logic so the user example can be verified before UI wiring.
