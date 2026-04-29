---
id: EPIC-003
priority: Must
mvp: true
size: S
requirements: [REQ-003, REQ-006, NFR-R-001, NFR-U-001]
architecture: [ADR-003]
dependencies: [EPIC-002]
status: complete
---

# EPIC-003: 回归测试与文档同步

**Priority**: Must
**MVP**: Yes
**Estimated Size**: S

## Description

更新测试以锁定四池 schema、`blocked_or_risky` 移除和禁用模式扫描；同步仓库要求的核心文档。

## Requirements

- [REQ-003](../requirements/REQ-003-remove-risky-pool.md): `blocked_or_risky` 必须从候选内容池移除
- [REQ-006](../requirements/REQ-006-regression-tests-docs.md): 测试和文档必须同步四池模型
- [NFR-R-001](../requirements/NFR-R-001-regression-prevention.md): 防止条件池 / 风险池 / 低质量词回流
- [NFR-U-001](../requirements/NFR-U-001-maintainer-clarity.md): 维护者可读性

## Architecture

- [ADR-003](../architecture/ADR-003-risk-as-validation.md): 风险内容迁移为测试规则

## Dependencies

- [EPIC-002](EPIC-002-pilot-content-rewrite.md): 内容重写完成后再写最终断言。

## Stories

### STORY-003-001: 更新四池 schema 与 blocked pattern 测试

**User Story**: As a 测试维护者, I want 测试能拦住旧池和低质量词 so that 回归会立刻失败。

**Acceptance Criteria**:

- [ ] `FIVE_LAYER_KEYS` 改为四池 key 集合或重命名为四池常量。
- [ ] 测试断言 `conditional_items` 和 `blocked_or_risky` 不存在。
- [ ] 禁用模式扫描覆盖四个默认池。

**Size**: S
**Traces to**: [REQ-003](../requirements/REQ-003-remove-risky-pool.md), [REQ-006](../requirements/REQ-006-regression-tests-docs.md)

---

### STORY-003-002: 同步项目文档

**User Story**: As a 未来维护者, I want 文档说明四池模型 so that 我不会再按五层池写库。

**Acceptance Criteria**:

- [ ] `agents.md` 同步四池模型。
- [ ] 根 `README.md` 同步 spec 状态和四池定义。
- [ ] `Game content extraction/CLAUDE.md` 同步维护规则。
- [ ] `Game content extraction/README.md` 同步用户/维护说明。
- [ ] `.gitignore` 按仓库规则检查并保持合理注释。

**Size**: S
**Traces to**: [REQ-006](../requirements/REQ-006-regression-tests-docs.md), [NFR-U-001](../requirements/NFR-U-001-maintainer-clarity.md)

---

### STORY-003-003: 执行验证命令并记录结果

**User Story**: As a 发布前审核者, I want 编译和测试结果被记录 so that 我能确认重构没有破坏工具。

**Acceptance Criteria**:

- [ ] `python -B -m py_compile 'Game content extraction\内容抽取.py' 'Game content extraction\data\blind_boxes.py'` 通过。
- [ ] `python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'` 通过。
- [ ] workflow 执行记录写明测试数量和结果。

**Size**: S
**Traces to**: [REQ-006](../requirements/REQ-006-regression-tests-docs.md), [NFR-R-001](../requirements/NFR-R-001-regression-prevention.md)
