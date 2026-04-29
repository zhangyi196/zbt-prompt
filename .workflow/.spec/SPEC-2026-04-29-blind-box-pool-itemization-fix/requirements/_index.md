---
session_id: SPEC-2026-04-29-blind-box-pool-itemization-fix
phase: 3
document_type: requirements-index
status: complete
generated_at: 2026-04-29T00:00:00+08:00
version: 1
dependencies:
  - ../spec-config.json
  - ../product-brief.md
  - ../glossary.json
---

# Requirements: 盲盒条件池与风险池物品化修正

本 PRD 将用户反馈转化为可执行验收规则：所有五层物品池都只能包含具体物品；`conditional_items` 必须具备中等以上体量；`blocked_or_risky` 必须是具体风险物；折线、擦痕、阴影、气泡等非物品内容进入校验禁用模式。

## Requirement Summary

| Priority | Count | Coverage |
|----------|-------|----------|
| Must Have | 5 | 条件池替换、风险池替换、forbidden patterns、兼容保持、测试覆盖 |
| Should Have | 1 | 文档同步 |
| Could Have | 0 | 本阶段不扩展 |
| Won't Have | 0 | 延后项见产品简报 Out of Scope |

## Functional Requirements

| ID | Title | Priority | Traces To |
|----|-------|----------|-----------|
| [REQ-001](REQ-001-conditional-items-visible-object.md) | `conditional_items` 必须改为条件启用的完整可见物品 | Must | [G-001](../product-brief.md#goals--success-metrics) |
| [REQ-002](REQ-002-blocked-risky-concrete-object.md) | `blocked_or_risky` 必须只保留具体风险物 | Must | [G-002](../product-brief.md#goals--success-metrics) |
| [REQ-003](REQ-003-forbidden-pattern-validation.md) | 建立非物品禁用模式校验 | Must | [G-003](../product-brief.md#goals--success-metrics) |
| [REQ-004](REQ-004-pilot-runtime-compatibility.md) | 保持三类试点运行时兼容 | Must | [G-004](../product-brief.md#goals--success-metrics) |
| [REQ-005](REQ-005-documentation-sync.md) | 同步池层定义文档 | Should | [G-005](../product-brief.md#goals--success-metrics) |

## Non-Functional Requirements

| ID | Title | Target |
|----|-------|--------|
| [NFR-R-001](NFR-R-001-regression-prevention.md) | 防止非物品条目回归 | 单元测试覆盖三类试点五层池 |
| [NFR-U-001](NFR-U-001-maintainer-clarity.md) | 维护者规则可读性 | 文档明确“池层=具体物品，禁用模式=校验规则” |

## Data Requirements

| Entity | Description | Key Attributes |
|--------|-------------|----------------|
| `ConditionalItem` | 条件启用的完整可见物品。 | `scene_name`, `item_name`, `requires_context`, `visible_size_level` |
| `BlockedRiskyObject` | 具体但默认禁用的风险物。 | `scene_name`, `item_name`, `risk_reason` |
| `ForbiddenPattern` | 不允许进入任何物品池的非物品表达。 | `pattern`, `reason`, `examples` |
| `PilotBundle` | 三类试点五层池集合。 | `scene_name`, `box_id`, `five_layer_keys` |

## Integration Requirements

| System | Direction | Data Format | Notes |
|--------|-----------|-------------|-------|
| `Game content extraction/data/blind_boxes.py` | Both | Python dict/list | 修改三类试点池层内容 |
| `Game content extraction/test_blind_box_content_model.py` | Outbound | unittest | 新增 forbidden patterns 校验 |
| 文档文件 | Outbound | Markdown | 同步规则与示例 |

## Constraints & Assumptions

### Constraints

- MUST 不改 `BLIND_BOXES` 运行时四栏 contract。
- MUST 不改盒号 15、16、17。
- MUST 不把 `forbidden_patterns` 当作可抽数据。
- SHOULD 不在本阶段重命名字段。

### Assumptions

- 当前字段名足以承载修正后的语义。
- 用户反馈代表后续扩库的关键质量门槛。

## Traceability Matrix

| Goal | Requirements |
|------|--------------|
| G-001 | [REQ-001](REQ-001-conditional-items-visible-object.md), [NFR-U-001](NFR-U-001-maintainer-clarity.md) |
| G-002 | [REQ-002](REQ-002-blocked-risky-concrete-object.md), [NFR-U-001](NFR-U-001-maintainer-clarity.md) |
| G-003 | [REQ-003](REQ-003-forbidden-pattern-validation.md), [NFR-R-001](NFR-R-001-regression-prevention.md) |
| G-004 | [REQ-004](REQ-004-pilot-runtime-compatibility.md) |
| G-005 | [REQ-005](REQ-005-documentation-sync.md) |

## References

- Derived from: [Product Brief](../product-brief.md)
- Next: [Architecture](../architecture/_index.md)
