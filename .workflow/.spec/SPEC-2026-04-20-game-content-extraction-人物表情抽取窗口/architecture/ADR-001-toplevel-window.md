---
id: ADR-001
status: Accepted
traces_to: [REQ-001, NFR-U-001, NFR-R-001]
date: 2026-04-20T14:44:00+08:00
---

# ADR-001: 使用独立 Toplevel 窗口

## Context

现有主窗口输入框服务于盲盒数字、动物类型和子类指令。人物表情抽取输入是多字段长文本，若复用主输入框会破坏现有语法和用户心智。

## Decision

新增“人物表情抽取”按钮，点击后打开独立 Toplevel 窗口。表情窗口独立持有输入、输出和策略控件。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| Toplevel 窗口 | 隔离功能，符合需求，风险低 | 多一个窗口管理点 |
| 主界面内嵌区域 | 单窗口 | 主界面变长，干扰现有流程 |
| Notebook 标签页 | 结构清晰 | 对当前小工具来说略重 |

## Consequences

- **Positive**: 现有抽取流程不受影响。
- **Negative**: 需要处理重复打开窗口。
- **Risks**: 窗口状态和复制按钮需要和主窗口清晰区分。

## Traces

- **Requirements**: [REQ-001](../requirements/REQ-001-expression-window.md), [NFR-U-001](../requirements/NFR-U-001-simple-copy-flow.md), [NFR-R-001](../requirements/NFR-R-001-no-regression.md)
- **Implemented by**: [EPIC-001](../epics/EPIC-001-expression-window-ui.md)
