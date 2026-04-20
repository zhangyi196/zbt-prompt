---
id: REQ-002
type: functional
priority: Must
traces_to: [G-002]
status: complete
---

# REQ-002: 表情组字段解析

**Priority**: Must

## Description

系统 MUST 从表情组文本中解析 `极性`、`单人/多人` 和 `具体表情字段`。解析 MUST 兼容中文冒号 `：`、英文冒号 `:`、单行连续字段和多行字段。系统 SHOULD 支持一次输入负向组和正向组。

## User Story

As a 游戏内容设计者, I want the tool to understand the copied expression plan text so that I do not need to reformat it manually.

## Acceptance Criteria

- [ ] 可解析用户示例中的单行连续字段。
- [ ] 可解析 `组图 23 表情前置.md` 的多行字段格式。
- [ ] 可识别单组和双组表情。
- [ ] 可定位具体表情字段值的替换范围。
- [ ] 输入缺少 `极性`、`单人/多人` 或 `具体表情` 时进入错误提示路径。

## Traces

- **Goal**: [G-002](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-parse-and-replace.md)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-parser-library.md)
