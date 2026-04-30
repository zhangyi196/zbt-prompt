---
session_id: SPEC-2026-04-30-blind-box-medium-scene-fragments
phase: 5
document_type: epics
kind: index
status: complete
generated_at: 2026-04-30T15:20:00+08:00
stepsCompleted:
  - load-phase-context
  - local-epic-decomposition
  - codex-review
  - write-epics
version: 1
dependencies:
  - ../spec-config.json
  - ../product-brief.md
  - ../requirements/_index.md
  - ../architecture/_index.md
  - ../glossary.json
---

# Epics & Stories: blind-box `scene_expansion_items` medium-scale scene fragments

本拆解把实施工作收敛为 4 个连续 Epic：先固化 medium-scale scene fragment 规则和兼容基线，再按 20 个场景完成第四池重写，随后用规模/边界/兼容性回归锁定结果，最后完成稳定文档同步和维护者审查闭环。4 个 Epic 全部纳入 MVP，因为本轮目标不是实验性试点，而是一次可交付的全量语义替换。

## Epic Overview

| Epic ID | Title | Priority | MVP | Stories | Est. Size |
|---------|-------|----------|-----|---------|-----------|
| [EPIC-001](EPIC-001-rule-baseline-and-compatibility-contract.md) | 规则基线与兼容契约 | Must | Yes | 3 | M |
| [EPIC-002](EPIC-002-full-scene-expansion-rewrite.md) | 20 场景第四池全量重写 | Must | Yes | 3 | L |
| [EPIC-003](EPIC-003-quality-boundary-and-regression-gates.md) | 质量闸门、边界校验与回归基线 | Must | Yes | 3 | M |
| [EPIC-004](EPIC-004-doc-sync-and-maintainer-review.md) | 文档同步与维护者审查闭环 | Must | Yes | 3 | S |

## Dependency Map

```mermaid
graph LR
    EPIC-001[规则基线与兼容契约] --> EPIC-002[20 场景全量重写]
    EPIC-001 --> EPIC-003[质量与边界回归]
    EPIC-002 --> EPIC-003
    EPIC-002 --> EPIC-004[文档同步与审查]
    EPIC-003 --> EPIC-004
```

### Dependency Notes

`EPIC-001` 提供 allowed families、forbidden roots、升级后信息载体例外和兼容边界，是后续所有故事的共同前提。`EPIC-002` 只负责把 20 个场景写进新模型；`EPIC-003` 在全量内容存在后才能对规模和跨池冲突做完整断言。`EPIC-004` 最后执行，避免在规则或测试尚未稳定前同步入口文档。

### Recommended Execution Order

1. [EPIC-001](EPIC-001-rule-baseline-and-compatibility-contract.md): 先冻结第四池语义和兼容契约，阻止实现阶段回退到大件或微小主体。
2. [EPIC-002](EPIC-002-full-scene-expansion-rewrite.md): 依据规则批量重写 20 个 `scene_expansion_items`。
3. [EPIC-003](EPIC-003-quality-boundary-and-regression-gates.md): 用回归测试锁定规模、边界和运行时兼容性。
4. [EPIC-004](EPIC-004-doc-sync-and-maintainer-review.md): 在数据和测试定稿后同步稳定文档并完成审查闭环。

## MVP Scope

### MVP Epics

MVP 包含全部 4 个 Epic。原因是本轮 Product Brief 的 Must 目标同时要求全量重写、兼容回归、质量闸门和稳定文档同步；缺少任何一个 Epic，都不能算完成 medium-scale scene fragment 模型切换。

### MVP Definition of Done

- [ ] `scene_expansion_items` 在 20 个场景中都遵守统一的 medium-scale scene fragment 规则。
- [ ] 每个场景第四池保持 50 条唯一项，且不通过大件家具、容器替代品或卡片/标签类微小主体凑数。
- [ ] `BLIND_BOX_ITEM_POOL_BUNDLES`、`BLIND_BOXES`、`BLIND_BOX_COMPATIBILITY_MAPPING` 和既有 `unittest` 结构契约保持不变。
- [ ] 质量校验能定位超大主体、超小主体和跨池冲突，并输出统一修复提示字段。
- [ ] `agents.md`、`Game content extraction/agents.md`、`README.md`、`.gitignore` 已完成精简同步检查。

## Traceability Matrix

| Requirement | Epic | Stories | Architecture |
|-------------|------|---------|--------------|
| [REQ-001](../requirements/REQ-001-formal-medium-scene-fragment-model.md) | [EPIC-001](EPIC-001-rule-baseline-and-compatibility-contract.md) | STORY-001-001, STORY-001-002 | [ADR-001](../architecture/ADR-001-medium-scene-fragment-model.md) |
| [REQ-002](../requirements/REQ-002-all-scene-rewrite-and-uniqueness.md) | [EPIC-002](EPIC-002-full-scene-expansion-rewrite.md) | STORY-002-001, STORY-002-002, STORY-002-003 | [ADR-002](../architecture/ADR-002-all-scene-rewrite-strategy.md) |
| [REQ-003](../requirements/REQ-003-scale-quality-validation.md) | [EPIC-001](EPIC-001-rule-baseline-and-compatibility-contract.md), [EPIC-003](EPIC-003-quality-boundary-and-regression-gates.md) | STORY-001-002, STORY-003-001 | [ADR-003](../architecture/ADR-003-scale-quality-validation.md) |
| [REQ-004](../requirements/REQ-004-pool-boundary-validation.md) | [EPIC-003](EPIC-003-quality-boundary-and-regression-gates.md) | STORY-003-002 | [ADR-004](../architecture/ADR-004-pool-boundary-rules.md) |
| [REQ-005](../requirements/REQ-005-runtime-and-unittest-compatibility.md) | [EPIC-001](EPIC-001-rule-baseline-and-compatibility-contract.md), [EPIC-003](EPIC-003-quality-boundary-and-regression-gates.md) | STORY-001-003, STORY-003-003 | [ADR-005](../architecture/ADR-005-runtime-compatibility.md) |
| [REQ-006](../requirements/REQ-006-documentation-sync-checks.md) | [EPIC-004](EPIC-004-doc-sync-and-maintainer-review.md) | STORY-004-001, STORY-004-002, STORY-004-003 | [ADR-006](../architecture/ADR-006-documentation-sync-policy.md) |
| [REQ-007](../requirements/REQ-007-maintainer-feedback-and-review.md) | [EPIC-001](EPIC-001-rule-baseline-and-compatibility-contract.md), [EPIC-003](EPIC-003-quality-boundary-and-regression-gates.md), [EPIC-004](EPIC-004-doc-sync-and-maintainer-review.md) | STORY-001-003, STORY-003-001, STORY-003-002, STORY-004-003 | [ADR-007](../architecture/ADR-007-maintainer-review-loop.md) |
| [NFR-R-001](../requirements/NFR-R-001-regression-compatibility.md) | [EPIC-003](EPIC-003-quality-boundary-and-regression-gates.md) | STORY-003-003 | [ADR-005](../architecture/ADR-005-runtime-compatibility.md) |
| [NFR-M-001](../requirements/NFR-M-001-rule-maintainability.md) | [EPIC-004](EPIC-004-doc-sync-and-maintainer-review.md) | STORY-004-001, STORY-004-003 | [ADR-006](../architecture/ADR-006-documentation-sync-policy.md), [ADR-007](../architecture/ADR-007-maintainer-review-loop.md) |
| [NFR-U-001](../requirements/NFR-U-001-first-eye-visible-wording.md) | [EPIC-002](EPIC-002-full-scene-expansion-rewrite.md), [EPIC-003](EPIC-003-quality-boundary-and-regression-gates.md) | STORY-002-001, STORY-002-002, STORY-002-003, STORY-003-001 | [ADR-001](../architecture/ADR-001-medium-scene-fragment-model.md), [ADR-003](../architecture/ADR-003-scale-quality-validation.md) |

## Estimation Summary

| Size | Meaning | Count |
|------|---------|-------|
| S | Small - narrow scope, low dependency risk | 1 |
| M | Medium - same module plus linked tests or docs | 2 |
| L | Large - full-scene batch rewrite with bounded acceptance checks | 1 |
| XL | Extra Large - must split before implementation | 0 |

## Risks & Considerations

| Risk | Affected Epics | Mitigation |
|------|---------------|------------|
| 第四池在批量重写时回退成“柜/车/架/桌/台”集合 | EPIC-001, EPIC-002 | 先冻结 forbidden large roots，再按批次重写并复核 |
| 为凑满 50 条而退化为卡片、标签、票据等微小主体 | EPIC-002, EPIC-003 | 用 forbidden tiny roots 和边界校验阻断 |
| 数据改对但运行时兼容层或旧断言被破坏 | EPIC-001, EPIC-003 | 把兼容 mapping 和旧 `unittest` 结构视作硬约束 |
| 入口文档复制过多 spec 细节导致维护成本上升 | EPIC-004 | 只同步稳定规则和必要入口，不复制 20 场景长列表 |

## Versioning & Changelog

### Version Strategy

- **Versioning Scheme**: workflow/spec session version。
- **Breaking Change Definition**: 只有改动四池 key、运行时四栏结构、用户输入路径或 UI 行为才算破坏性变化；本轮不允许发生。
- **Deprecation Policy**: 旧的 scene-expansion 写法通过测试规则和文档边界淘汰，而不是保留并行双模型。

### Changelog

| Version | Date | Type | Description |
|---------|------|------|-------------|
| 1 | 2026-04-30 | Added | 为 medium-scale scene fragment 全量替换生成执行级 Epic/Story 拆解 |

## Open Questions

- [ ] 质量校验是否需要同时维护“黑名单词根 + 少量白名单例外”，还是把例外全部收敛到升级后信息载体一类即可？
- [ ] 是否需要在实现阶段保留非规范性的场景参考词根表，仅供维护者扩写，不进入稳定文档？
- [ ] 升级后信息载体是否应统一优先使用“板 / 面 / 页组 / 排列组”等后缀，以降低命名漂移？

## References

- Derived from: [Requirements](../requirements/_index.md), [Architecture](../architecture/_index.md), [Product Brief](../product-brief.md)
- Handoff to: implementation planning / issue export
