---
id: ADR-001
status: Accepted
traces_to: [REQ-001]
date: 2026-04-30T14:20:00+08:00
---

# ADR-001: 固定 medium-scale scene fragment 内容模型

## Context

当前 `scene_expansion_items` 混入大量柜、车、架、桌、台等超大主体，也存在卡片、标签、票据、单张等超小主体。维护者缺少统一语义中心，导致第四池不断在“大件家具池”和“微小信息片池”之间摇摆。

## Decision

第四池统一采用 medium-scale scene fragment 模型。允许家族固定为 5 类：活动结果件、中号任务面、铺垫界面件、成组阵列件、完整成果件；“升级后的信息载体”只允许以板、面、页组、记录面、排列表面等中号载体通过。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 固定 5 类中号场景片段模型 | 语义清晰，易于测试，能同时排除超大与超小主体 | 需要重写现有第四池内容 |
| 继续沿用“场景扩展物”宽泛说法 | 文档改动小 | 仍会回退到柜车架台或卡片标签 |
| 按场景单独解释第四池 | 灵活 | 无法形成统一规则，也难以批量回归 |

## Consequences

- **Positive**: 维护者可用同一套规则审查 20 个场景。
- **Negative**: 一些现有大件或微小条目必须被替换。
- **Risks**: 例外载体如果定义过宽，仍可能重新演变成信息碎片池。

## Traces

- **Requirements**: [REQ-001](../requirements/REQ-001-formal-medium-scene-fragment-model.md)
- **Implemented by**: [EPIC-001](../epics/EPIC-001-rule-baseline-and-compatibility-contract.md)
