---
id: REQ-001
type: functional
priority: Must
traces_to: [G-001]
status: complete
---

# REQ-001: 人物表情抽取窗口入口

**Priority**: Must

## Description

系统 MUST 在现有 Game content extraction 主窗口中提供“人物表情抽取”入口。入口 MUST 打开独立人物表情抽取窗口，窗口包含表情组文本输入区、模板选择控件、抽取按钮、清空按钮、复制按钮和输出区。

## User Story

As a 提示词维护者, I want to open a dedicated expression extraction window so that I can enhance 表情组文本 without affecting the existing blind-box extraction flow.

## Acceptance Criteria

- [ ] 主窗口出现“人物表情抽取”按钮。
- [ ] 点击按钮打开独立 Toplevel 窗口。
- [ ] 窗口关闭后主窗口仍可继续使用。
- [ ] 现有“开始抽取”“清空输入”“复制结果”按钮行为不变。
- [ ] 输入区和输出区支持多行中文文本。

## Traces

- **Goal**: [G-001](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-001](../architecture/ADR-001-toplevel-window.md)
- **Implemented by**: [EPIC-001](../epics/EPIC-001-expression-window-ui.md)
