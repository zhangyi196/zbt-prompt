---
id: REQ-006
type: functional
priority: Must
traces_to: [G-002]
status: complete
---

# REQ-006: 中文错误提示

**Priority**: Must

## Description

系统 MUST 对用户可修复错误输出清晰中文提示。错误提示 MUST 写入人物表情抽取窗口输出区，不应弹出复杂阻断对话框。

## User Story

As a 游戏内容设计者, I want clear Chinese error messages so that I can fix the copied text or selection quickly.

## Acceptance Criteria

- [ ] 空输入提示用户粘贴表情组文本。
- [ ] 缺少关键字段时提示缺哪个字段。
- [ ] 表情库文件缺失时提示检查路径或打包配置。
- [ ] 极性错配时提示该表情属于另一极性。
- [ ] 模板编号越界时提示合法编号范围。

## Traces

- **Goal**: [G-002](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-parse-and-replace.md)
- **Implemented by**: [EPIC-003](../epics/EPIC-003-output-errors.md)
