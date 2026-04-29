---
id: REQ-004
type: functional
priority: Must
traces_to: [G-004]
status: complete
---

# REQ-004: 保持三类试点运行时兼容

**Priority**: Must

## Description

修正内容 MUST 保持 15 / 16 / 17 号试点盒的运行时兼容。`BLIND_BOXES` 中每个试点盒仍必须暴露 `name`、`large`、`medium`、`small`、`hanging`，并保持 `blocked_or_risky` 不进入默认四栏。

## User Story

As an App 维护者, I want the correction to preserve runtime compatibility so that a content quality fix does not become a UI or history migration.

## Acceptance Criteria

- [ ] 15 / 16 / 17 号盒仍存在。
- [ ] 每个试点盒仍具备 `name`、`large`、`medium`、`small`、`hanging`。
- [ ] `conditional_items` 继续映射到 `hanging`，但内容必须符合 REQ-001。
- [ ] `blocked_or_risky` 继续不进入默认四栏。
- [ ] 不修改逗号输入语法、四栏标签或 `draw_history.json` 语义。

## Traces

- **Goal**: [G-004](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-004](../architecture/ADR-004-compatibility-preservation.md)
- **Implemented by**: [EPIC-001](../epics/EPIC-001-pilot-pool-content-correction.md)
