---
session_id: SPEC-2026-04-20-game-content-extraction-人物表情抽取窗口
phase: 6
document_type: spec-summary
status: complete
generated_at: 2026-04-20T14:46:00+08:00
stepsCompleted:
  - summary-generated
version: 1
dependencies:
  - readiness-report.md
---

# Spec Summary: 人物表情抽取窗口

## Summary

为 Game content extraction 新增人物表情抽取窗口。用户粘贴表情组文本后，工具根据 `极性 + 具体表情 + 单人/多人` 从 `组图 23 表情库.md` 查找眉/眼/嘴模板，并通过原文局部回填把模板追加到具体表情字段后。

## MVP

- 独立 Toplevel 表情窗口。
- 支持单行和多行字段解析。
- 读取 Markdown 表情库并校验正负向和单人/多人。
- 支持指定模板编号，能复现 `困惑 + 单人 + 第4条`。
- 输出增强文本并支持复制。
- 中文错误提示。

## Key Decisions

- 使用独立 Toplevel，不复用主输入框。
- 保持 Markdown 表情库为单一事实源。
- 保留占位符，不自动替换为剧情物体。
- 使用原文局部回填，不重写全文。

## Implementation Order

1. EPIC-002: 解析和表情库核心逻辑。
2. EPIC-001: UI 窗口接入。
3. EPIC-003: 输出、复制和错误提示。
4. EPIC-004: 打包和验证。

## Primary Acceptance Example

`极性=负向, 具体表情=困惑, 单人/多人=单人, template_index=4`

Expected append:

`眉：一侧眉尾抬起，另一侧眉尾压平；眼：一侧眼撑开看着[目标物]，另一侧眼半垂；嘴：一侧嘴巴闭住下压，另一侧嘴角收紧。`

## Documents

- [Product Brief](product-brief.md)
- [Requirements](requirements/_index.md)
- [Architecture](architecture/_index.md)
- [Epics](epics/_index.md)
- [Readiness Report](readiness-report.md)
