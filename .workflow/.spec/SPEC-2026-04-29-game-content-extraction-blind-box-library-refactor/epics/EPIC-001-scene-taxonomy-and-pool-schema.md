---
id: EPIC-001
title: 场景入口与五层池模型
priority: Must
mvp: true
size: L
requirements: [REQ-001, REQ-002, NFR-U-001]
architecture: [ADR-001]
dependencies: []
status: complete
---

# EPIC-001: 场景入口与五层池模型

## Description

建立盲盒物品新内容模型的基础层：20 个“场景+用途”入口，以及每个入口必须遵守的五层物品池 schema。这个 epic 不负责具体试点内容的完整条目，只冻结分类和入池规则。

## Stories

### STORY-001-001: 冻结 20 个中文场景入口

As a 内容维护者, I want 20 个短、清晰、互不重叠的“场景+用途”入口 so that 后续写库和用户选类都不再依赖旧宽泛主题。

- Acceptance Criteria:
  - 20 个入口完整列出，且全部使用中文“场景+用途”格式。
  - 每个入口有一句场景提示，不使用过度抽象主题名。
  - `桌面+学习`、`海底+潜水`、`公园+野餐` 标记为试点。
  - 入口清单链接到 [REQ-001](../requirements/REQ-001-scene-entry-taxonomy.md)。
- Size: L
- Trace: REQ-001, NFR-U-001

### STORY-001-002: 定义旧入口别名和迁移注释

As a 开发维护者, I want 每个新入口可记录旧主题别名 so that 兼容期内不会让旧编号和旧主题语义失踪。

- Acceptance Criteria:
  - 数据模型包含 `legacy_aliases` 字段。
  - 别名只用于兼容和迁移说明，不作为新主分类。
  - 未能确定旧映射的入口必须显式标注待确认。
- Size: S
- Trace: REQ-001

### STORY-001-003: 定义五层物品池字段与职责

As a 内容维护者, I want 每个类别都有固定五层字段 so that 默认可抽、条件可抽和风险物不会混在一起。

- Acceptance Criteria:
  - schema 包含 `core_items`、`support_items`、`visible_small_items`、`conditional_items`、`blocked_or_risky`。
  - 每层有写入条件、禁止条件和至少 1 个示例说明。
  - `blocked_or_risky` 明确禁止进入默认输出。
- Size: M
- Trace: REQ-002

### STORY-001-004: 写明可见小物与条件物的边界

As a 工具使用者, I want 小物和条件物遵守可见性与承载规则 so that 抽出的内容可以直接用于差异提示词。

- Acceptance Criteria:
  - `visible_small_items` 必须要求块状、成组或有明确承载面。
  - `conditional_items` 必须写明承载、悬挂或包裹依赖。
  - 微型痕迹、细线、边缘接缝不能作为默认小物。
- Size: M
- Trace: REQ-002

## Architecture Links

- [ADR-001](../architecture/ADR-001-scene-entry-content-model.md)

## Risks

- 类别语义过近会导致用户选择困难；入口冻结前需要统一审阅。
