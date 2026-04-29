---
id: EPIC-001
priority: Must
mvp: true
size: M
requirements: [REQ-001, REQ-004]
architecture: [ADR-001, ADR-004]
dependencies: []
status: complete
---

# EPIC-001: 四池数据模型与兼容映射

**Priority**: Must
**MVP**: Yes
**Estimated Size**: M

## Description

将试点 `BLIND_BOX_ITEM_POOL_BUNDLES` 的 schema 从五层迁移到四类内容池，并更新 `_build_legacy_blind_box_entry`、`BLIND_BOX_COMPATIBILITY_MAPPING` 以继续生成旧四栏 `BLIND_BOXES`。

## Requirements

- [REQ-001](../requirements/REQ-001-four-pool-schema.md): 试点 bundle 必须采用四类内容池 schema
- [REQ-004](../requirements/REQ-004-legacy-runtime-compatibility.md): 保持 `BLIND_BOXES` 四栏兼容视图

## Architecture

- [ADR-001](../architecture/ADR-001-four-pool-data-model.md): 四类内容池作为试点数据源
- [ADR-004](../architecture/ADR-004-legacy-mapping-preservation.md): 保留四栏兼容视图

## Dependencies

无前置 Epic。

## Stories

### STORY-001-001: 将试点 bundle key 改为四类内容池

**User Story**: As a 内容维护者, I want 三类试点只保留四个候选池 so that 数据模型边界清楚。

**Acceptance Criteria**:

- [ ] `conditional_items` key 被 `scene_expansion_items` 替代。
- [ ] `blocked_or_risky` key 被移除。
- [ ] 三个试点 bundle key 集合一致。

**Size**: M
**Traces to**: [REQ-001](../requirements/REQ-001-four-pool-schema.md)

---

### STORY-001-002: 调整四池到旧四栏的兼容映射

**User Story**: As a 桌面工具用户, I want 旧四栏输出仍可用 so that 工具界面不需要改变。

**Acceptance Criteria**:

- [ ] `BLIND_BOXES[15/16/17]` 仍含 `large`、`medium`、`small`、`hanging`。
- [ ] 映射不再引用 `conditional_items` 或 `blocked_or_risky`。
- [ ] `hanging` 不以低质量细线物强制填充。

**Size**: M
**Traces to**: [REQ-004](../requirements/REQ-004-legacy-runtime-compatibility.md)

---

### STORY-001-003: 更新 compatibility mapping 元数据

**User Story**: As a 未来实现代理, I want mapping 元数据准确说明来源 so that 后续维护不会误读四栏来源。

**Acceptance Criteria**:

- [ ] `large_sources`、`medium_sources`、`small_sources`、`hanging_sources` 与新四池一致。
- [ ] `excluded_sources` 不再列出已删除的候选池。
- [ ] 注释或文档说明 `blocked_patterns` 属于测试规则。

**Size**: S
**Traces to**: [REQ-004](../requirements/REQ-004-legacy-runtime-compatibility.md)
