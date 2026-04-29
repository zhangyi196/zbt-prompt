---
id: EPIC-001
priority: Must
mvp: true
size: M
requirements: [REQ-001, REQ-002, REQ-004]
architecture: [ADR-001, ADR-002, ADR-004]
dependencies: []
status: complete
---

# EPIC-001: 三类试点池层内容修正

**Priority**: Must  
**MVP**: Yes  
**Estimated Size**: M

## Description

替换 `Game content extraction/data/blind_boxes.py` 中 15 `桌面+学习`、16 `海底+潜水`、17 `公园+野餐` 的 `conditional_items` 和 `blocked_or_risky`，让它们全部成为具体物品或具体风险物。

## Requirements

- [REQ-001](../requirements/REQ-001-conditional-items-visible-object.md): `conditional_items` 必须改为条件启用的完整可见物品
- [REQ-002](../requirements/REQ-002-blocked-risky-concrete-object.md): `blocked_or_risky` 必须只保留具体风险物
- [REQ-004](../requirements/REQ-004-pilot-runtime-compatibility.md): 保持三类试点运行时兼容

## Architecture

- [ADR-001](../architecture/ADR-001-pool-entry-object-only.md): 五层池条目必须是具体物品
- [ADR-002](../architecture/ADR-002-blocked-risky-as-object-pool.md): `blocked_or_risky` 保留为具体风险物池
- [ADR-004](../architecture/ADR-004-compatibility-preservation.md): 保持四栏运行时兼容

## Stories

### STORY-001-001: 替换三类试点 `conditional_items`

**User Story**: As a 工具使用者, I want conditional_items to be complete visible objects so that conditional output can still be useful for game differences.

**Acceptance Criteria**:
- [ ] 三类试点条件池不包含标签、卡片、扣件、贴片、边缘附属物。
- [ ] 每个条件池条目具备中等以上体量。
- [ ] 每个条件池条目可单独圈选。

**Size**: S  
**Traces to**: [REQ-001](../requirements/REQ-001-conditional-items-visible-object.md)

### STORY-001-002: 替换三类试点 `blocked_or_risky`

**User Story**: As a 内容维护者, I want blocked_or_risky to contain concrete risky objects so that it remains useful as a review list.

**Acceptance Criteria**:
- [ ] 风险池不包含折线、擦痕、气泡、阴影、边线、碎叶点、微小污点等非物品。
- [ ] 风险池保留透明、反光、发光、动物本体、细绳、流苏等具体风险物。
- [ ] 风险池不进入默认四栏。

**Size**: S  
**Traces to**: [REQ-002](../requirements/REQ-002-blocked-risky-concrete-object.md)

### STORY-001-003: 验证四栏兼容未变

**User Story**: As an App 维护者, I want pilot boxes to keep the legacy runtime shape so that content correction does not break extraction.

**Acceptance Criteria**:
- [ ] 15 / 16 / 17 号盒仍存在。
- [ ] 每盒仍暴露 `name`、`large`、`medium`、`small`、`hanging`。
- [ ] 不修改输入语法和历史 key。

**Size**: S  
**Traces to**: [REQ-004](../requirements/REQ-004-pilot-runtime-compatibility.md)
