---
id: ADR-005
status: Accepted
traces_to: [REQ-005, NFR-R-001]
date: 2026-04-30T14:20:00+08:00
---

# ADR-005: 保持四池事实源与运行时四栏兼容契约

## Context

当前桌面工具依赖 `BLIND_BOXES` 的 `large` / `medium` / `small` / `hanging` 四栏结构，测试也显式断言 `BLIND_BOX_COMPATIBILITY_MAPPING` 的来源关系。若本轮为了改进第四池语义而改变运行时输出，会波及 UI、history key 和输入覆盖语法。

## Decision

保留现有四池事实源和运行时兼容契约。`BLIND_BOX_ITEM_POOL_BUNDLES` 继续作为数据事实源；`BLIND_BOXES` 继续由 `core_items + scene_expansion_items` 生成 `large`，由 `support_items + core_items:first_6` 生成 `medium`，由 `visible_small_items` 生成 `small`，`hanging` 保持空兼容桶；新增质量校验与现有 `unittest` 共同组成同一回归基线。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 保持现有兼容契约 | 影响面最小，符合约束 | 第四池只能在现有四栏框架内表达 |
| 新增第五运行时列 | 语义更直观 | 破坏 UI 和历史兼容，不在本次范围内 |
| 修改 `large` / `medium` 映射比例 | 可微调呈现 | 会改变既有抽取行为，回归风险高 |

## Consequences

- **Positive**: 数据重写不会连带改动 UI 或输入输出协议。
- **Negative**: 新语义必须适配旧四栏视图，而不能重新设计运行时结构。
- **Risks**: 如果第四池条目仍偏大，会直接污染 `large` 视图，因此必须依赖 ADR-003 先做质量闸门。

## Traces

- **Requirements**: [REQ-005](../requirements/REQ-005-runtime-and-unittest-compatibility.md), [NFR-R-001](../requirements/NFR-R-001-regression-compatibility.md)
- **Implemented by**: [EPIC-003](../epics/EPIC-003-quality-boundary-and-regression-gates.md)
