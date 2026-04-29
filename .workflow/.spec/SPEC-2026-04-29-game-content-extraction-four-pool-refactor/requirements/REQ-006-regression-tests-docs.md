---
id: REQ-006
type: functional
priority: Must
traces_to: [G-005]
status: complete
---

# REQ-006: 测试和文档必须同步四池模型

**Priority**: Must

## Description

测试必须从五层池断言迁移到四类内容池断言，文档必须同步说明 `scene_expansion_items` 的定义和 `blocked_or_risky` 的移除。

## User Story

As a 未来实现代理, I want 测试和文档都描述同一套四池模型 so that 执行时不会混入旧五层语义。

## Acceptance Criteria

- [ ] `test_blind_box_content_model.py` 更新四池 key 集合。
- [ ] 测试新增 `blocked_or_risky` 不存在断言。
- [ ] 测试保留禁用模式扫描，覆盖四个默认池。
- [ ] `agents.md`、`README.md`、`Game content extraction/CLAUDE.md`、`Game content extraction/README.md` 同步四池定义。
- [ ] `.gitignore` 按仓库规则同步检查，无无意义忽略规则漂移。

## Traces

- **Goal**: [G-005](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-risk-as-validation.md)
- **Implemented by**: [EPIC-003](../epics/EPIC-003-validation-and-doc-sync.md)
