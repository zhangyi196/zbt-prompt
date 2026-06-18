---
title: "Learnings"
readMode: optional
priority: medium
category: learning
keywords:
  - bug
  - lesson
  - gotcha
  - learning
---

# Learnings

Add entries with: `/spec-add learning <description>`

## Entries

- 2026-05-21: When prompt salience needs to be stronger, make the acceptance gate first-glance visible and tie it to the exact rule section; area thresholds alone are not enough.

<spec-entry category="learning" keywords="milestone,audit,documentation-state,prompt-navigation" date="2026-06-18" source="milestone-complete:M2">
When a milestone audit flags documentation-state gaps, fix both the root navigation paths and roadmap progress before milestone completion; otherwise the audit report and state registry can disagree even when the prompt implementation is complete.
</spec-entry>

<spec-entry category="learning" keywords="wiki-connect,knowledge-graph,orphan-containers,milestone-complete" date="2026-06-18" source="wiki-connect:M2">
When `wiki-connect --fix` is unavailable, run the underlying `maestro wiki` health/orphans/hubs checks and record the result; do not force links between top-level project/spec containers unless a root-linking convention already exists.
</spec-entry>
