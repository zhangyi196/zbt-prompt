---
id: EPIC-001
priority: Must
mvp: true
size: M
requirements: [REQ-001, NFR-U-001]
architecture: [ADR-001]
dependencies: []
status: complete
---

# EPIC-001: 表情窗口 UI

**Priority**: Must
**MVP**: Yes
**Estimated Size**: M

## Description

在现有主窗口中新增人物表情抽取入口，并创建独立 Toplevel 窗口。窗口提供粘贴输入、模板策略选择、执行抽取和复制输出的基础交互。

## Requirements

- [REQ-001](../requirements/REQ-001-expression-window.md): 人物表情抽取窗口入口
- [NFR-U-001](../requirements/NFR-U-001-simple-copy-flow.md): 简洁复制流程

## Architecture

- [ADR-001](../architecture/ADR-001-toplevel-window.md): 使用独立 Toplevel 窗口

## Dependencies

- None

## Stories

### STORY-001-001: 主窗口入口按钮

**User Story**: As a 提示词维护者, I want a visible button for 人物表情抽取窗口 so that I can launch the feature from the existing tool.

**Acceptance Criteria**:
- [ ] 主窗口按钮区包含“人物表情抽取”按钮。
- [ ] 点击按钮不触发现有盲盒抽取。
- [ ] 按钮文字为中文。

**Size**: S
**Traces to**: [REQ-001](../requirements/REQ-001-expression-window.md)

---

### STORY-001-002: Toplevel 窗口布局

**User Story**: As a 游戏内容设计者, I want a dedicated input and output area so that I can paste long 表情组文本 and inspect the result.

**Acceptance Criteria**:
- [ ] 窗口包含输入 ScrolledText。
- [ ] 窗口包含输出 ScrolledText。
- [ ] 窗口包含抽取、清空、复制按钮。
- [ ] 窗口尺寸适合多行中文文本。

**Size**: M
**Traces to**: [REQ-001](../requirements/REQ-001-expression-window.md)

---

### STORY-001-003: 模板策略控件

**User Story**: As a 游戏内容设计者, I want to choose a template strategy so that I can reproduce the expected template or use random selection.

**Acceptance Criteria**:
- [ ] UI 支持选择指定编号或随机策略。
- [ ] 指定编号控件能表达单人 1-4、多人数 5-8。
- [ ] 默认值能复现用户示例或清晰可调整。

**Size**: M
**Traces to**: [REQ-004](../requirements/REQ-004-template-selection.md)
