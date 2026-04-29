---
id: EPIC-003
title: 三个试点类别内容交付
priority: Must
mvp: true
size: L
requirements: [REQ-004, REQ-005, NFR-SC-001]
architecture: [ADR-003, ADR-004]
dependencies: [EPIC-001, EPIC-002]
status: complete
---

# EPIC-003: 三个试点类别内容交付

## Description

按新模型重写 `桌面+学习`、`海底+潜水`、`公园+野餐` 三个试点类别，形成可复用样板。每个试点都必须包含五层池、四栏兼容映射和风险隔离结果。

## Stories

### STORY-003-001: 交付桌面+学习试点

As a 内容维护者, I want 一个高频日常场景样板 so that 后续普通室内类目有可复用写法。

- Acceptance Criteria:
  - 类别包含完整五层池。
  - 条目围绕书桌、文具、书本、学习收纳等清晰物件。
  - 默认池不使用微型痕迹、透明反光物或不稳定挂件。
  - 具备四栏映射。
- Size: M
- Trace: REQ-004, NFR-SC-001

### STORY-003-002: 交付海底+潜水试点

As a 内容维护者, I want 一个特殊主题样板 so that 可以验证高风险内容隔离能力。

- Acceptance Criteria:
  - 类别聚焦潜水装备、海底可见器物、非动物本体。
  - 动物本体、微小气泡、反光透明物等进入 `blocked_or_risky` 或被排除。
  - 默认池条目必须有清晰形体和可圈选边界。
  - 具备四栏映射。
- Size: M
- Trace: REQ-004, REQ-005

### STORY-003-003: 交付公园+野餐试点

As a 内容维护者, I want 一个户外承载场景样板 so that 可以验证成组小物和承载关系规则。

- Acceptance Criteria:
  - 类别围绕野餐垫、餐盒、便携食物承载物和户外收纳。
  - 小物必须成组、块状或明确放在垫、篮、桌面等承载面上。
  - 不使用草地小碎片、地面痕迹、边缘线等低可见条目。
  - 具备四栏映射。
- Size: M
- Trace: REQ-004, REQ-005

### STORY-003-004: 记录试点抽样质量

As a 开发维护者, I want 每个试点都有抽样审查记录 so that 是否继续扩库有证据。

- Acceptance Criteria:
  - 每个试点抽样不少于 30 次。
  - 记录明显不适合项数量、原因和修正建议。
  - 每个试点 `blocked_or_risky` 泄漏数为 0。
  - 不适合项占比低于 10% 才标记通过。
- Size: M
- Trace: REQ-005

## Architecture Links

- [ADR-003](../architecture/ADR-003-pilot-first-rollout.md)
- [ADR-004](../architecture/ADR-004-risk-isolation-validation.md)

## Risks

- 试点样板若追求数量而牺牲质量，会把旧问题带入新模型。
