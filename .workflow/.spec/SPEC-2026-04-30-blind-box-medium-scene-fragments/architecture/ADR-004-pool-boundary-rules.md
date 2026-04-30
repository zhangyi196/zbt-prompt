---
id: ADR-004
status: Accepted
traces_to: [REQ-004]
date: 2026-04-30T14:20:00+08:00
---

# ADR-004: 用职责边界区分四池

## Context

即使第四池本身语义更清楚，仍可能与 `core_items`、`support_items`、`visible_small_items` 发生角色重叠。没有边界规则时，维护者仍会把条目随意塞进第四池。

## Decision

固定四池职责边界：`core_items` 负责更大的主体或主角物，`support_items` 负责单个工具、托座和配件，`visible_small_items` 负责小而清晰的零散物，`scene_expansion_items` 只负责中号场景片段。边界检查对冲突项必须输出冲突池名称和迁移建议；原始微小信息词不得直接通过第四池边界。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 明确四池职责并校验冲突 | 迁移方向清楚，维护成本低 | 需要写清规则和示例 |
| 只规定第四池，不规定其他三池 | 改动表面更小 | 冲突项仍无处安放 |
| 允许维护者自由判断 | 灵活 | 规则无法复用，也无法自动回归 |

## Consequences

- **Positive**: 冲突项出现时能快速判断应迁回哪一池。
- **Negative**: 边界附近条目需要更多人工复核。
- **Risks**: 如果边界说明过长，会削弱可扫描性，需保持简洁。

## Traces

- **Requirements**: [REQ-004](../requirements/REQ-004-pool-boundary-validation.md)
- **Implemented by**: [EPIC-003](../epics/EPIC-003-quality-boundary-and-regression-gates.md)
