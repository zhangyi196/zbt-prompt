---
title: "Wiki Connections Check 2026-06-18"
category: learning
source: "maestro-milestone-complete:M2"
---

# Wiki Connections Check 2026-06-18

## Baseline

- Command attempted: `maestro wiki-connect --fix`
- Result: unavailable in current CLI (`unknown command 'wiki-connect'`)
- Fallback commands:
  - `maestro wiki list --json`
  - `maestro wiki health`
  - `maestro wiki orphans`
  - `maestro wiki hubs --limit 10`

## Result

- Health score: 90/100
- Entries: 20
- Broken links: 0
- Orphans: 10
- Missing titles: 0

Post-persist recheck:

- Health score: 89/100
- Entries: 27
- Broken links: 0
- Orphans: 11
- Reason: the new wiki-connection report is itself indexed as a new orphaned knowledge entry until a root-linking convention exists.

## Orphan Pattern

The orphan entries are top-level project/spec containers:

- `project-project`
- `roadmap-roadmap`
- `spec:project:architecture-constraints`
- `spec:project:coding-conventions`
- `spec:project:debug-notes`
- `spec:project:learnings`
- `spec:project:quality-rules`
- `spec:project:review-standards`
- `spec:project:test-conventions`
- `spec:project:ui-conventions`

## Decision

No automatic link mutation was applied during M2 completion. The graph has no broken links, and the orphan set is made of stable root containers where forced links would create broad metadata churn outside the milestone-completion archive.

## Follow-up

If graph density becomes important, define a stable root-linking convention first, such as `project-project -> roadmap-roadmap -> spec containers`, then apply it as a dedicated knowledge-graph maintenance task.
