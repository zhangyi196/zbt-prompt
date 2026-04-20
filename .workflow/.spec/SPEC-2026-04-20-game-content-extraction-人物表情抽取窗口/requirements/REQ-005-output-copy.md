---
id: REQ-005
type: functional
priority: Must
traces_to: [G-004]
status: complete
---

# REQ-005: 原文局部回填与复制

**Priority**: Must

## Description

系统 MUST 通过原文局部回填输出增强结果。除具体表情字段外，系统 MUST 保持输入文本原有字段、顺序和内容。具体表情字段增强格式为：`具体表情: 困惑，眉：...；眼：...；嘴：...。`

## User Story

As a 提示词维护者, I want the enhanced result to preserve the original prompt text so that it can be copied directly into the next workflow.

## Acceptance Criteria

- [ ] 输出保留剧情、人物定位、表情功能、适配提示、禁用区域等字段。
- [ ] 只增强具体表情字段值。
- [ ] 双组输入分别增强各自具体表情字段。
- [ ] 重复点击不会叠加两份眉/眼/嘴模板。
- [ ] 复制按钮复制输出区完整内容。

## Traces

- **Goal**: [G-004](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-parse-and-replace.md)
- **Implemented by**: [EPIC-003](../epics/EPIC-003-output-errors.md)
