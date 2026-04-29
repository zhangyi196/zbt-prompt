---
session_id: SPEC-2026-04-29-game-content-extraction-four-pool-refactor
phase: 3
document_type: requirements-index
status: complete
generated_at: 2026-04-29T00:00:00+08:00
version: 1
dependencies:
  - ../spec-config.json
  - ../product-brief.md
---

# Requirements: Game content extraction 盲盒物品四类内容池重构

本 PRD 将三类盲盒试点从五层池迁移到四类内容池：`core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`。`conditional_items` 和 `blocked_or_risky` 不再作为候选池，风险内容进入 `blocked_patterns` 测试规则，运行时继续提供旧四栏兼容视图。

## Requirement Summary

| Priority | Count | Coverage |
|----------|-------|----------|
| Must Have | 6 | 四池 schema、场景扩展物、移除风险池、四栏兼容、试点重写、测试文档 |
| Should Have | 2 | 回归防护与维护者可读性 |
| Could Have | 0 | 本阶段不扩展 |
| Won't Have | 3 | 图像识别、用户文本触发、发布打包 |

## Functional Requirements

| ID | Title | Priority | Traces To |
|----|-------|----------|-----------|
| [REQ-001](REQ-001-four-pool-schema.md) | 试点 bundle 必须采用四类内容池 schema | Must | [G-001](../product-brief.md#goals--success-metrics) |
| [REQ-002](REQ-002-scene-expansion-items.md) | `scene_expansion_items` 必须是默认安全的场景扩展物 | Must | [G-002](../product-brief.md#goals--success-metrics) |
| [REQ-003](REQ-003-remove-risky-pool.md) | `blocked_or_risky` 必须从候选内容池移除 | Must | [G-003](../product-brief.md#goals--success-metrics) |
| [REQ-004](REQ-004-legacy-runtime-compatibility.md) | 保持 `BLIND_BOXES` 四栏兼容视图 | Must | [G-004](../product-brief.md#goals--success-metrics) |
| [REQ-005](REQ-005-pilot-content-rewrite.md) | 三个试点盒必须按四池模型重写 | Must | [G-001](../product-brief.md#goals--success-metrics), [G-002](../product-brief.md#goals--success-metrics) |
| [REQ-006](REQ-006-regression-tests-docs.md) | 测试和文档必须同步四池模型 | Must | [G-005](../product-brief.md#goals--success-metrics) |

## Non-Functional Requirements

| ID | Title | Target |
|----|-------|--------|
| [NFR-R-001](NFR-R-001-regression-prevention.md) | 防止条件池 / 风险池 / 低质量词回流 | 单元测试覆盖四池 schema 和 blocked patterns |
| [NFR-U-001](NFR-U-001-maintainer-clarity.md) | 维护者可读性 | 项目文档明确四类内容池定义和禁用项 |

## Data Requirements

| Entity | Description | Key Attributes |
|--------|-------------|----------------|
| `BlindBoxSceneEntry` | 20 类场景入口清单 | `id`, `name_zh`, `scene_hint`, `legacy_aliases`, `pilot` |
| `FourPoolBundle` | 三类试点四池内容数据 | `core_items`, `support_items`, `visible_small_items`, `scene_expansion_items` |
| `BlockedPattern` | 禁用模式测试规则 | `pattern`, `reason`, `applies_to` |
| `LegacyBlindBoxEntry` | 旧四栏兼容视图 | `name`, `large`, `medium`, `small`, `hanging` |
| `CompatibilityMapping` | 四池到四栏来源说明 | `large_sources`, `medium_sources`, `small_sources`, `hanging_sources`, `excluded_sources` |

## Integration Requirements

| System | Direction | Protocol | Data Format | Notes |
|--------|-----------|----------|-------------|-------|
| `Game content extraction/data/blind_boxes.py` | Both | Python import | dict/list | 四池数据源和兼容视图 |
| `Game content extraction/内容抽取.py` | Inbound | Python import | `BLIND_BOXES` dict | 不改 UI 和抽取入口 |
| `Game content extraction/test_blind_box_content_model.py` | Outbound | unittest | assertions | schema、禁用模式、兼容映射测试 |
| 项目文档 | Outbound | Markdown | Chinese docs | 同步维护规则 |

## Constraints & Assumptions

### Constraints

- MUST 不做图像识别或锚点检测。
- MUST 不引入用户文本触发解析。
- MUST 不改 UI 和四栏勾选语义。
- MUST 首阶段只处理 15 / 16 / 17 三个试点。
- MUST 不做版本发布和安装包构建。

### Assumptions

- `BLIND_BOXES` 仍是运行时消费层。
- `blocked_patterns` 可先保留在测试中。
- `hanging` 可以保守映射，不能为凑数引入低质量悬挂物。

## Priority Rationale

四池 schema 和兼容映射是基础，必须优先；场景扩展物定义和风险规则测试决定输出质量，也必须纳入 MVP。全量 20 类扩展和输入语境解析属于后续增强，避免本轮范围失控。

## Traceability Matrix

| Goal | Requirements |
|------|--------------|
| G-001 | [REQ-001](REQ-001-four-pool-schema.md), [REQ-005](REQ-005-pilot-content-rewrite.md), [NFR-U-001](NFR-U-001-maintainer-clarity.md) |
| G-002 | [REQ-002](REQ-002-scene-expansion-items.md), [REQ-005](REQ-005-pilot-content-rewrite.md) |
| G-003 | [REQ-003](REQ-003-remove-risky-pool.md), [NFR-R-001](NFR-R-001-regression-prevention.md) |
| G-004 | [REQ-004](REQ-004-legacy-runtime-compatibility.md) |
| G-005 | [REQ-006](REQ-006-regression-tests-docs.md), [NFR-R-001](NFR-R-001-regression-prevention.md) |

## Open Questions

- [ ] `hanging` 是否允许为空或减少默认数量？
- [ ] `scene_expansion_items` 是否只映射到 `large`？
- [ ] `blocked_patterns` 是否抽为数据常量？

## References

- Derived from: [Product Brief](../product-brief.md)
- Next: [Architecture](../architecture/_index.md)
