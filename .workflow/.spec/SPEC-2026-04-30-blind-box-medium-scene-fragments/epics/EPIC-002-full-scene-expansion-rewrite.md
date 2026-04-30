---
session_id: SPEC-2026-04-30-blind-box-medium-scene-fragments
phase: 5
document_type: epics
kind: epic
status: complete
generated_at: 2026-04-30T15:20:00+08:00
stepsCompleted:
  - load-phase-context
  - epic-decomposition
  - codex-review
version: 1
dependencies:
  - ../product-brief.md
  - ../requirements/_index.md
  - ../architecture/_index.md
id: EPIC-002
priority: Must
mvp: true
size: L
requirements: [REQ-002, NFR-U-001]
architecture: [ADR-001, ADR-002]
epic_dependencies: [EPIC-001]
---

# EPIC-002: 20 场景第四池全量重写

**Priority**: Must
**MVP**: Yes
**Estimated Size**: L

## Description

按 `BLIND_BOX_SCENE_ENTRIES` 的 20 个 `场景+用途` 入口，对全部 `scene_expansion_items` 执行一次性重写。故事按场景批次划分，而不是拆成单个超大故事；每个批次都必须满足 50 条唯一项、首眼可见命名和非大件/非微小主体边界。

## Requirements

- [REQ-002](../requirements/REQ-002-all-scene-rewrite-and-uniqueness.md): 全量重写 20 个 `scene_expansion_items` 并保持每场景 50 条唯一项
- [NFR-U-001](../requirements/NFR-U-001-first-eye-visible-wording.md): 首眼可见命名一致性

## Architecture

- [ADR-001](../architecture/ADR-001-medium-scene-fragment-model.md): 固定 medium-scale scene fragment 内容模型
- [ADR-002](../architecture/ADR-002-all-scene-rewrite-strategy.md): 对 20 个场景执行全量重写而非 pilot-only 扩写

## Dependencies

- [EPIC-001](EPIC-001-rule-baseline-and-compatibility-contract.md): 需要先冻结第四池语义、禁区和兼容边界。

## Stories

### STORY-002-001: 重写室内日常与家居批次

**User Story**: As a Prompt maintainer, I want 室内日常场景先完成同口径重写 so that 规则能在最常见场景上被快速验证。

**Acceptance Criteria**:

- [ ] 盒号 1-7 的 `桌面+学习`、`餐桌+茶歇`、`厨房+烘焙`、`卧室+梳妆`、`浴室+洗护`、`客厅+装饰`、`儿童房+玩具` 都完成第四池重写。
- [ ] 每个场景的 `scene_expansion_items` 恰好 50 条唯一项，不通过近义词堆叠或轻微字面变化凑数。
- [ ] 重写结果不回退到大件家具/收纳设施，也不退化为卡片、标签、票据或单张信息碎片。

**Size**: L
**Traces to**: [REQ-002](../requirements/REQ-002-all-scene-rewrite-and-uniqueness.md), [NFR-U-001](../requirements/NFR-U-001-first-eye-visible-wording.md)

---

### STORY-002-002: 重写户外、出行与装备批次

**User Story**: As a downstream prompt user, I want 户外与出行场景拥有可直接圈选的中号片段 so that 抽到第四池条目时不需要二次删词。

**Acceptance Criteria**:

- [ ] 盒号 8-15 的 `宠物+日常`、`庭院+园艺`、`门口+雨具`、`沙滩+度假`、`公园+野餐`、`营地+露营`、`街道+出行`、`运动场+装备` 都完成第四池重写。
- [ ] 每个场景的第四池条目保持“首眼可见、可圈选、可承载场景状态”，且不依赖透明、发光、反光或微痕迹。
- [ ] 所有条目都符合 medium-scale scene fragment 模型，不借用大件载具、落地架或微小标签类对象充数。

**Size**: L
**Traces to**: [REQ-002](../requirements/REQ-002-all-scene-rewrite-and-uniqueness.md), [NFR-U-001](../requirements/NFR-U-001-first-eye-visible-wording.md)

---

### STORY-002-003: 重写专门活动与文化场景批次

**User Story**: As a Game content extraction tool maintainer, I want 高风险语义场景也按同一模型收口 so that 20 个入口不会出现特例逃逸。

**Acceptance Criteria**:

- [ ] 盒号 16-20 的 `海底+潜水`、`节日+礼物`、`手作+缝纫`、`手作+编织`、`商店+零食` 都完成第四池重写。
- [ ] `海底+潜水` 不回退到动物本体、发光珊瑚或透明反光主体；其余场景不回退到礼盒容器、线团碎件或标签牌主体。
- [ ] 每个场景在重写完成后都能通过唯一性和命名可读性检查。

**Size**: M
**Traces to**: [REQ-002](../requirements/REQ-002-all-scene-rewrite-and-uniqueness.md), [NFR-U-001](../requirements/NFR-U-001-first-eye-visible-wording.md)
