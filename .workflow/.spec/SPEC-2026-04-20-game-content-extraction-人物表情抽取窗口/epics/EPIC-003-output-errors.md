---
id: EPIC-003
priority: Must
mvp: true
size: M
requirements: [REQ-005, REQ-006]
architecture: [ADR-003]
dependencies: [EPIC-002]
status: complete
---

# EPIC-003: 回填、复制与错误提示

**Priority**: Must
**MVP**: Yes
**Estimated Size**: M

## Description

把解析和查找结果应用到原文，生成增强输出，并完善复制与错误提示路径。

## Requirements

- [REQ-005](../requirements/REQ-005-output-copy.md): 原文局部回填与复制
- [REQ-006](../requirements/REQ-006-error-handling.md): 中文错误提示

## Architecture

- [ADR-003](../architecture/ADR-003-parse-and-replace.md): 解析字段并原文局部回填

## Dependencies

- [EPIC-002](EPIC-002-parser-library.md) (blocking): 需要 ExpressionBlock 和模板结果。

## Stories

### STORY-003-001: 原文局部回填

**User Story**: As a 提示词维护者, I want only 具体表情字段 to change so that the rest of my prompt text stays intact.

**Acceptance Criteria**:
- [ ] 只替换具体表情字段值。
- [ ] 其余字段和换行尽量保持。
- [ ] 双组输入分别回填。

**Size**: M
**Traces to**: [REQ-005](../requirements/REQ-005-output-copy.md)

---

### STORY-003-002: 复制输出

**User Story**: As a 游戏内容设计者, I want to copy the enhanced text so that I can paste it into the next prompt step.

**Acceptance Criteria**:
- [ ] 复制按钮复制输出区内容。
- [ ] 输出为空时不报错。
- [ ] 复制后窗口保持可继续使用。

**Size**: S
**Traces to**: [REQ-005](../requirements/REQ-005-output-copy.md)

---

### STORY-003-003: 用户输入错误提示

**User Story**: As a 游戏内容设计者, I want a clear message when my input is incomplete so that I can fix it immediately.

**Acceptance Criteria**:
- [ ] 空输入提示粘贴表情组文本。
- [ ] 缺字段提示字段名。
- [ ] 已重复回填时不叠加模板。

**Size**: M
**Traces to**: [REQ-006](../requirements/REQ-006-error-handling.md)

---

### STORY-003-004: 匹配和库错误提示

**User Story**: As a 提示词维护者, I want lookup errors to explain the rule that failed so that I can correct the polarity, expression, or template number.

**Acceptance Criteria**:
- [ ] 极性错配提示正确极性。
- [ ] 未知表情提示未找到类别。
- [ ] 编号越界提示合法范围。
- [ ] 表情库文件缺失提示路径/打包检查。

**Size**: M
**Traces to**: [REQ-006](../requirements/REQ-006-error-handling.md)
