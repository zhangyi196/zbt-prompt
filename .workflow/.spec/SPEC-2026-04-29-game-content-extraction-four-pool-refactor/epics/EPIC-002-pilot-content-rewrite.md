---
id: EPIC-002
priority: Must
mvp: true
size: M
requirements: [REQ-002, REQ-005]
architecture: [ADR-001, ADR-002]
dependencies: [EPIC-001]
status: complete
---

# EPIC-002: 三类试点内容重写

**Priority**: Must
**MVP**: Yes
**Estimated Size**: M

## Description

按四池模型重写 15 `桌面+学习`、16 `海底+潜水`、17 `公园+野餐` 的内容，重点补齐高质量 `scene_expansion_items`，移除锚点依赖和风险条目。

## Requirements

- [REQ-002](../requirements/REQ-002-scene-expansion-items.md): `scene_expansion_items` 必须是默认安全的场景扩展物
- [REQ-005](../requirements/REQ-005-pilot-content-rewrite.md): 三个试点盒必须按四池模型重写

## Architecture

- [ADR-001](../architecture/ADR-001-four-pool-data-model.md): 四类内容池作为试点数据源
- [ADR-002](../architecture/ADR-002-scene-expansion-default-safe.md): 场景扩展物作为第四类内容

## Dependencies

- [EPIC-001](EPIC-001-four-pool-data-model.md): 需要先建立四池 schema。

## Stories

### STORY-002-001: 重写桌面+学习四池内容

**User Story**: As a 工具用户, I want 桌面学习类输出不依赖显示器或白板 so that 没有图像识别时也合理。

**Acceptance Criteria**:

- [ ] `scene_expansion_items` 包含桌面日历、桌面小风扇、护眼书架、桌面收纳抽屉或同等质量对象。
- [ ] 不包含 `显示器下方`、`白板磁吸`、`桌侧` 等图像条件语义。
- [ ] 不包含透明、反光、发光、细绳、流苏、微型痕迹。

**Size**: M
**Traces to**: [REQ-002](../requirements/REQ-002-scene-expansion-items.md), [REQ-005](../requirements/REQ-005-pilot-content-rewrite.md)

---

### STORY-002-002: 重写公园+野餐四池内容

**User Story**: As a 工具用户, I want 野餐类输出有丰富但自然的扩展物 so that 游戏场景更可玩。

**Acceptance Criteria**:

- [ ] `scene_expansion_items` 包含折叠野餐桌、便携冷藏箱、户外收纳箱、野餐遮阳布或同等质量对象。
- [ ] 不包含伞杆、挂旗、细杆风车、昆虫本体、远处飞鸟等风险对象。
- [ ] 可见小物保持成组、块状或有承载。

**Size**: M
**Traces to**: [REQ-002](../requirements/REQ-002-scene-expansion-items.md), [REQ-005](../requirements/REQ-005-pilot-content-rewrite.md)

---

### STORY-002-003: 重写海底+潜水四池内容

**User Story**: As a 内容维护者, I want 海底潜水类也有无动物本体、无透明发光风险的扩展物 so that 三个试点都有完整样板。

**Acceptance Criteria**:

- [ ] `scene_expansion_items` 使用潜水装备收纳、海底作业器具、标记/样本承载等具体物。
- [ ] 不包含鱼群、海龟、水母、发光珊瑚、反光贝壳、细绳渔网等风险对象。
- [ ] 不依赖光效、透明或动物本体。

**Size**: M
**Traces to**: [REQ-005](../requirements/REQ-005-pilot-content-rewrite.md)
