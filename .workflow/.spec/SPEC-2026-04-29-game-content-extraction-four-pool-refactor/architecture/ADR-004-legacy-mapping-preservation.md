---
id: ADR-004
status: Accepted
traces_to: [REQ-004]
date: 2026-04-29T00:00:00+08:00
---

# ADR-004: 保留四栏兼容视图

## Context

桌面工具 UI、输入覆盖语法和历史权重都围绕 `large`、`medium`、`small`、`hanging` 工作。底层数据重构不应扩大到 UI 改造。

## Decision

保留 `BLIND_BOXES` 四栏兼容视图，由四池内容派生。`large` 可聚合 `core_items` 和 `scene_expansion_items`，`medium` 聚合 `support_items` 和部分 `core_items`，`small` 来源于 `visible_small_items`，`hanging` 保守处理且不得强制填充低质量物。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 保留四栏兼容视图 | UI 零改动，风险低 | 底层/运行时存在映射层 |
| UI 直接改四池 | 概念统一 | 范围过大 |
| 删除 hanging | 消除低质来源 | 破坏现有 UI contract |

## Consequences

- **Positive**: 降低实现风险。
- **Negative**: `hanging` 的语义会弱化为兼容字段。
- **Risks**: 如果强行填充 `hanging`，可能引入旧问题；实现时必须保守。

## Traces

- **Requirements**: [REQ-004](../requirements/REQ-004-legacy-runtime-compatibility.md)
- **Implemented by**: [EPIC-001](../epics/EPIC-001-four-pool-data-model.md)
