---
session_id: SPEC-2026-04-29-game-content-extraction-four-pool-refactor
phase: 5
document_type: epics-index
status: complete
generated_at: 2026-04-29T00:00:00+08:00
version: 1
dependencies:
  - ../spec-config.json
  - ../product-brief.md
  - ../requirements/_index.md
  - ../architecture/_index.md
---

# Epics & Stories: Game content extraction 盲盒物品四类内容池重构

本执行拆解将四池重构分为三个 MVP Epic：数据模型与兼容映射、三类试点内容重写、测试与文档同步。三个 Epic 均属于 MVP，按顺序执行可降低同文件冲突和回归风险。

## Epic Overview

| Epic ID | Title | Priority | MVP | Stories | Est. Size |
|---------|-------|----------|-----|---------|-----------|
| [EPIC-001](EPIC-001-four-pool-data-model.md) | 四池数据模型与兼容映射 | Must | Yes | 3 | M |
| [EPIC-002](EPIC-002-pilot-content-rewrite.md) | 三类试点内容重写 | Must | Yes | 3 | M |
| [EPIC-003](EPIC-003-validation-and-doc-sync.md) | 回归测试与文档同步 | Must | Yes | 3 | S |

## Dependency Map

```mermaid
graph LR
    EPIC-001[四池模型] --> EPIC-002[试点内容重写]
    EPIC-002 --> EPIC-003[测试与文档]
```

### Dependency Notes

`EPIC-001` 先建立可执行的数据结构和兼容映射；`EPIC-002` 在新结构下改写内容；`EPIC-003` 最后用测试和文档锁定结果。

### Recommended Execution Order

1. [EPIC-001](EPIC-001-four-pool-data-model.md): 先替换 schema 和映射。
2. [EPIC-002](EPIC-002-pilot-content-rewrite.md): 再按四池模型重写内容。
3. [EPIC-003](EPIC-003-validation-and-doc-sync.md): 最后更新测试和文档。

## MVP Scope

### MVP Epics

三个 Epic 全部属于 MVP。本轮只覆盖 15 / 16 / 17 三个试点盒，不扩展到 20 类全量库。

### MVP Definition of Done

- [ ] 三个试点 bundle 只含四类内容池。
- [ ] `scene_expansion_items` 内容具体、常见、边界清楚、无图像锚点依赖。
- [ ] `blocked_or_risky` 不再作为候选池存在。
- [ ] `BLIND_BOXES` 四栏兼容视图继续工作。
- [ ] 测试和文档同步四池模型。

## Traceability Matrix

| Requirement | Epic | Stories | Architecture |
|-------------|------|---------|--------------|
| [REQ-001](../requirements/REQ-001-four-pool-schema.md) | [EPIC-001](EPIC-001-four-pool-data-model.md) | STORY-001-001, STORY-001-002 | [ADR-001](../architecture/ADR-001-four-pool-data-model.md) |
| [REQ-004](../requirements/REQ-004-legacy-runtime-compatibility.md) | [EPIC-001](EPIC-001-four-pool-data-model.md) | STORY-001-002, STORY-001-003 | [ADR-004](../architecture/ADR-004-legacy-mapping-preservation.md) |
| [REQ-002](../requirements/REQ-002-scene-expansion-items.md) | [EPIC-002](EPIC-002-pilot-content-rewrite.md) | STORY-002-001, STORY-002-002 | [ADR-002](../architecture/ADR-002-scene-expansion-default-safe.md) |
| [REQ-005](../requirements/REQ-005-pilot-content-rewrite.md) | [EPIC-002](EPIC-002-pilot-content-rewrite.md) | STORY-002-001, STORY-002-002, STORY-002-003 | [ADR-001](../architecture/ADR-001-four-pool-data-model.md), [ADR-002](../architecture/ADR-002-scene-expansion-default-safe.md) |
| [REQ-003](../requirements/REQ-003-remove-risky-pool.md) | [EPIC-003](EPIC-003-validation-and-doc-sync.md) | STORY-003-001 | [ADR-003](../architecture/ADR-003-risk-as-validation.md) |
| [REQ-006](../requirements/REQ-006-regression-tests-docs.md) | [EPIC-003](EPIC-003-validation-and-doc-sync.md) | STORY-003-001, STORY-003-002, STORY-003-003 | [ADR-003](../architecture/ADR-003-risk-as-validation.md) |
| [NFR-R-001](../requirements/NFR-R-001-regression-prevention.md) | [EPIC-003](EPIC-003-validation-and-doc-sync.md) | STORY-003-001 | [ADR-003](../architecture/ADR-003-risk-as-validation.md) |
| [NFR-U-001](../requirements/NFR-U-001-maintainer-clarity.md) | [EPIC-003](EPIC-003-validation-and-doc-sync.md) | STORY-003-002 | [ADR-001](../architecture/ADR-001-four-pool-data-model.md) |

## Estimation Summary

| Size | Meaning | Count |
|------|---------|-------|
| S | Small - well-understood, minimal risk | 1 |
| M | Medium - same module changes plus tests/docs | 2 |
| L | Large - significant complexity | 0 |
| XL | Extra Large - must split | 0 |

## Risks & Considerations

| Risk | Affected Epics | Mitigation |
|------|---------------|------------|
| `hanging` 兼容字段质量下降 | EPIC-001, EPIC-002 | 不强制细绳挂饰补位，允许保守映射 |
| 四池测试与旧五层测试冲突 | EPIC-003 | 先改 schema，再同步测试 |
| 文档多处仍提五层模型 | EPIC-003 | 按仓库规则同步四个核心文档 |

## Versioning & Changelog

### Version Strategy

- **Versioning Scheme**: workflow/spec session version。
- **Breaking Change Definition**: UI 或输入语法变化才算桌面工具破坏性变化，本轮不触发。
- **Deprecation Policy**: `conditional_items` 和 `blocked_or_risky` 在试点模型中直接移除，文档标记为旧概念。

## Open Questions

- [ ] `hanging` 为空时 UI 是否可接受？
- [ ] `scene_expansion_items` 是否应进入 `large` 全量？

## References

- Derived from: [Requirements](../requirements/_index.md), [Architecture](../architecture/_index.md)
- Handoff to: workflow-plan / workflow-execute
