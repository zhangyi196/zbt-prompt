---
id: REQ-001
type: functional
priority: Must
traces_to: [G-001]
status: complete
---

# REQ-001: 试点 bundle 必须采用四类内容池 schema

**Priority**: Must

## Description

`BLIND_BOX_ITEM_POOL_BUNDLES` 中三个试点场景必须从五层池迁移为四类内容池：`core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`。`conditional_items`、`blocked_or_risky`、`anchor_required_items` 等旧概念不得作为候选池保留。

## User Story

As a 盲盒内容维护者, I want 试点数据只使用四类清晰内容池 so that 我可以稳定扩展内容而不再纠结条件池和风险池边界。

## Acceptance Criteria

- [ ] `BLIND_BOX_ITEM_POOL_BUNDLES[scene]` 的 key 集合严格等于四类内容池。
- [ ] 三个试点场景均通过四池 schema 测试。
- [ ] `conditional_items`、`blocked_or_risky` 不再出现在试点 bundle key 中。
- [ ] 每个四池列表均非空。

## Traces

- **Goal**: [G-001](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-001](../architecture/ADR-001-four-pool-data-model.md)
- **Implemented by**: [EPIC-001](../epics/EPIC-001-four-pool-data-model.md)
