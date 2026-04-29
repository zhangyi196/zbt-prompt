---
session_id: SPEC-2026-04-29-blind-box-pool-itemization-fix
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

No GitHub issues were created in this run. The spec is export-ready and can be used by `workflow-plan`, direct scoped edit, or manual issue creation.

## Proposed Issues

| Issue Title | Source Epic | Wave | Labels | Dependencies |
|-------------|-------------|------|--------|--------------|
| 修正三类盲盒试点的条件池和风险池内容 | EPIC-001 | wave-1 | spec-generated, blind-box, content-quality | None |
| 增加非物品禁用模式测试并同步文档 | EPIC-002 | wave-2 | spec-generated, validation, docs | EPIC-001 |

## Issue Body Template

```markdown
Source spec: .workflow/.spec/SPEC-2026-04-29-blind-box-pool-itemization-fix/

Read first:
- spec-summary.md
- epics/{EPIC_FILE}
- requirements/_index.md
- architecture/_index.md

Acceptance criteria:
- All five item-pool layers contain concrete objects only.
- `conditional_items` are medium-or-larger conditionally enabled visible objects.
- `blocked_or_risky` contains concrete risky objects only.
- forbidden patterns do not appear in any pilot five-layer pool.
- Existing 15/16/17 pilot boxes keep legacy four-bucket compatibility.
```

## Phase 7 Result

| Field | Value |
|-------|-------|
| issues_created | 0 |
| export_mode | manual-ready |
| all_mvp_epics_covered | yes |
| spec_documents_resolve | yes |
