---
id: ADR-001
status: Accepted
traces_to: [REQ-001, REQ-002, NFR-U-001]
date: 2026-04-29T00:00:00+08:00
---

# ADR-001: 20 个场景入口作为内容模型主索引

## Context

当前旧主题过宽，内容维护者容易把不稳定的小物、容器和挂件写进默认池。需求要求用 20 个“常见场景+用途”入口建立更直观的分类法，并让每个入口都能承载五层物品池。

## Decision

采用 20 个场景入口作为盲盒物品内容库的主索引。每个入口必须有中文短名、场景提示、旧入口别名、是否试点标记，以及对应的 `ItemPoolBundle`。旧主题不再作为内容写库的主要认知框架，但可以在兼容期作为别名或迁移注释保留。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 20 个场景入口 | 类别直观，便于按目标图选择，适合逐类迁移。 | 需要建立旧入口到新入口的迁移说明。 |
| 保留 14 个旧主题，仅清洗条目 | 改动小，运行时风险最低。 | 无法解决主题过宽和写库判断不稳定的问题。 |
| 按物品尺寸重新分类 | 与四栏 key 接近。 | 用户无法按真实场景选类，也不能表达承载关系。 |

## Consequences

- **Positive**: 用户和维护者都能用更接近真实图像场景的入口理解内容。
- **Negative**: 后续实现需要处理旧编号、旧主题名和新入口名之间的兼容。
- **Risks**: 若入口名过长或语义重叠，会降低选择效率，需要保持短名和场景提示一致。

## Traces

- **Requirements**: [REQ-001](../requirements/REQ-001-scene-entry-taxonomy.md), [REQ-002](../requirements/REQ-002-five-layer-item-pool-schema.md), [NFR-U-001](../requirements/NFR-U-001-chinese-scanability-and-operability.md)
- **Implemented by**: Phase 5 epics.
