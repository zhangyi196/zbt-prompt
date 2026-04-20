---
id: EPIC-002
priority: Must
mvp: true
size: L
requirements: [REQ-002, REQ-003, REQ-004, NFR-P-001]
architecture: [ADR-002, ADR-003]
dependencies: [EPIC-001]
status: complete
---

# EPIC-002: 字段解析与表情库匹配

**Priority**: Must
**MVP**: Yes
**Estimated Size**: L

## Description

实现人物表情抽取窗口的核心逻辑：解析输入字段、读取 Markdown 表情库、校验极性和单人/多人规则，并按模板编号策略选中目标模板。

## Requirements

- [REQ-002](../requirements/REQ-002-field-parser.md): 表情组字段解析
- [REQ-003](../requirements/REQ-003-library-lookup.md): 表情库查找与校验
- [REQ-004](../requirements/REQ-004-template-selection.md): 模板编号选择
- [NFR-P-001](../requirements/NFR-P-001-local-fast.md): 本地快速处理

## Architecture

- [ADR-002](../architecture/ADR-002-markdown-library.md): 读取 Markdown 表情库
- [ADR-003](../architecture/ADR-003-parse-and-replace.md): 解析字段并原文局部回填

## Dependencies

- [EPIC-001](EPIC-001-expression-window-ui.md) (soft): UI 最终接入需要窗口。

## Stories

### STORY-002-001: 单行字段解析

**User Story**: As a 提示词维护者, I want the parser to handle the provided one-line example so that copied text does not need manual formatting.

**Acceptance Criteria**:
- [ ] 可识别 `极性: 负向`。
- [ ] 可识别 `单人/多人: 单人`。
- [ ] 可识别 `具体表情: 困惑`。
- [ ] 可定位具体表情字段值 span。

**Size**: M
**Traces to**: [REQ-002](../requirements/REQ-002-field-parser.md)

---

### STORY-002-002: 多行与双组解析

**User Story**: As a 游戏内容设计者, I want to paste the upstream two-section output so that both negative and positive groups can be enhanced together.

**Acceptance Criteria**:
- [ ] 可解析多行字段。
- [ ] 可按多个 `极性:` 识别多组。
- [ ] 每组独立输出 diagnostics。

**Size**: M
**Traces to**: [REQ-002](../requirements/REQ-002-field-parser.md)

---

### STORY-002-003: Markdown 表情库解析

**User Story**: As a 提示词维护者, I want templates read from 表情库 so that the tool stays aligned with the maintained prompt file.

**Acceptance Criteria**:
- [ ] 可解析正向和负向章节。
- [ ] 可解析 `### 编号. 表情名` 标题。
- [ ] 可解析每类 1-8 条模板。
- [ ] 缺失结构时返回明确错误。

**Size**: L
**Traces to**: [REQ-003](../requirements/REQ-003-library-lookup.md)

---

### STORY-002-004: 三元条件查找

**User Story**: As a 游戏内容设计者, I want the tool to match polarity, expression, and audience so that templates are not mixed up.

**Acceptance Criteria**:
- [ ] `负向 + 困惑 + 单人` 查找负向困惑的 1-4 条。
- [ ] `多人` 查找 5-8 条。
- [ ] 极性错配时不会返回模板。

**Size**: M
**Traces to**: [REQ-003](../requirements/REQ-003-library-lookup.md)

---

### STORY-002-005: 指定编号和随机策略

**User Story**: As a 游戏内容设计者, I want both deterministic and random template selection so that I can review exact examples and still vary daily use.

**Acceptance Criteria**:
- [ ] 指定第 4 条能返回用户示例模板。
- [ ] 单人越界编号报错。
- [ ] 随机策略不越过单人/多人合法范围。

**Size**: M
**Traces to**: [REQ-004](../requirements/REQ-004-template-selection.md)
