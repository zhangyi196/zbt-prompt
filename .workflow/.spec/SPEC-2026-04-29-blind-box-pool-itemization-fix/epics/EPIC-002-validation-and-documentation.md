---
id: EPIC-002
priority: Must
mvp: true
size: S
requirements: [REQ-003, REQ-005, NFR-R-001, NFR-U-001]
architecture: [ADR-001, ADR-003]
dependencies: [EPIC-001]
status: complete
---

# EPIC-002: 禁用模式校验与文档同步

**Priority**: Must  
**MVP**: Yes  
**Estimated Size**: S

## Description

为物品化规则增加回归测试，并同步项目文档，确保后续不会再次把非物品内容写入任何五层池。

## Requirements

- [REQ-003](../requirements/REQ-003-forbidden-pattern-validation.md): 建立非物品禁用模式校验
- [REQ-005](../requirements/REQ-005-documentation-sync.md): 同步池层定义文档
- [NFR-R-001](../requirements/NFR-R-001-regression-prevention.md): 防止非物品条目回归
- [NFR-U-001](../requirements/NFR-U-001-maintainer-clarity.md): 维护者规则可读性

## Architecture

- [ADR-001](../architecture/ADR-001-pool-entry-object-only.md): 五层池条目必须是具体物品
- [ADR-003](../architecture/ADR-003-forbidden-pattern-validation.md): 非物品禁用模式进入测试校验

## Dependencies

- [EPIC-001](EPIC-001-pilot-pool-content-correction.md) (blocking): 测试应验证替换后的目标状态。

## Stories

### STORY-002-001: 增加 forbidden patterns 测试

**User Story**: As an App 维护者, I want tests to reject non-object patterns so that future edits cannot reintroduce unusable entries.

**Acceptance Criteria**:
- [ ] 测试覆盖所有五层池。
- [ ] 测试覆盖三类试点。
- [ ] 任一 forbidden pattern 出现时测试失败。

**Size**: S  
**Traces to**: [REQ-003](../requirements/REQ-003-forbidden-pattern-validation.md), [NFR-R-001](../requirements/NFR-R-001-regression-prevention.md)

### STORY-002-002: 运行完整回归测试

**User Story**: As an App 维护者, I want the existing test suite to pass so that the patch does not break current behavior.

**Acceptance Criteria**:
- [ ] `python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'` 通过。
- [ ] `python -B -m py_compile 'Game content extraction\\内容抽取.py' 'Game content extraction\\data\\blind_boxes.py'` 通过。

**Size**: S  
**Traces to**: [REQ-003](../requirements/REQ-003-forbidden-pattern-validation.md)

### STORY-002-003: 同步文档中的池层定义

**User Story**: As a 内容维护者, I want docs to state the object-only rule so that future edits follow the corrected model.

**Acceptance Criteria**:
- [ ] 必更文档说明所有五层池只写具体物品。
- [ ] 文档说明 forbidden patterns 是校验规则，不是池条目。
- [ ] 文档保留 workflow/spec 输出可跟踪策略。

**Size**: S  
**Traces to**: [REQ-005](../requirements/REQ-005-documentation-sync.md), [NFR-U-001](../requirements/NFR-U-001-maintainer-clarity.md)
