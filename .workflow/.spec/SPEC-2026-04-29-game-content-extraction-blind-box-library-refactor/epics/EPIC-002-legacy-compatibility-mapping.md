---
id: EPIC-002
title: 四栏兼容映射与历史边界
priority: Must
mvp: true
size: M
requirements: [REQ-003, REQ-006, NFR-P-001, NFR-S-001]
architecture: [ADR-002, ADR-005]
dependencies: [EPIC-001]
status: complete
---

# EPIC-002: 四栏兼容映射与历史边界

## Description

把五层内容模型安全映射回现有 `large`、`medium`、`small`、`hanging` 运行时 contract，同时保持旧逗号输入、四栏选择和 `draw_history.json` 物品历史语义不变。

## Stories

### STORY-002-001: 定义五层到四栏的映射表

As a 开发维护者, I want 明确的映射规则 so that 新内容模型可以被旧运行时消费。

- Acceptance Criteria:
  - `core_items` 主要映射到 `large`。
  - `support_items` 映射到 `medium`。
  - `visible_small_items` 映射到 `small`。
  - 只有合规 `conditional_items` 可映射到 `hanging`。
  - `blocked_or_risky` 不映射到任何默认四栏。
- Size: M
- Trace: REQ-003

### STORY-002-002: 保持单次抽取路径性能

As a 工具使用者, I want 新模型不让抽取明显变慢 so that 本地工具仍然轻快可用。

- Acceptance Criteria:
  - 兼容映射结果可预先形成旧四栏结构。
  - 单次抽取不增加额外多轮桶级扫描。
  - 现有抽取路径不依赖远程服务或数据库。
- Size: S
- Trace: REQ-003, NFR-P-001, NFR-S-001

### STORY-002-003: 保持旧输入和历史语义

As a 既有用户, I want 原来的逗号输入和历史降权继续工作 so that 内容库优化不会破坏使用习惯。

- Acceptance Criteria:
  - 逗号输入语法保持不变。
  - `draw_history.json` 的 `item_pools` 不迁移、不混入动物池或表情历史。
  - 旧编号可通过别名或映射说明继续解释。
  - 批量重命名、图像抓取等非盲盒模块不接入本模型。
- Size: M
- Trace: REQ-006, NFR-S-001

## Architecture Links

- [ADR-002](../architecture/ADR-002-five-layer-to-four-bucket-mapping.md)
- [ADR-005](../architecture/ADR-005-history-input-compatibility.md)

## Risks

- 若映射逻辑和数据定义分散，后续容易出现文档和运行时不一致。
