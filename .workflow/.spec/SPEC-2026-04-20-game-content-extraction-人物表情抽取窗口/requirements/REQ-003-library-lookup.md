---
id: REQ-003
type: functional
priority: Must
traces_to: [G-002]
status: complete
---

# REQ-003: 表情库查找与校验

**Priority**: Must

## Description

系统 MUST 从表情库读取正向和负向表情类别，并为每个类别解析 1-8 条模板。系统 MUST 使用 `极性 + 具体表情字段 + 单人/多人` 作为匹配条件。单人 MUST 只允许 1-4 范围，多人 MUST 只允许 5-8 范围。

## User Story

As a 提示词维护者, I want templates to come from the canonical expression library so that generated text stays consistent with prompt rules.

## Acceptance Criteria

- [ ] 能解析 `困惑` 在负向章节中的 8 条模板。
- [ ] `负向 + 困惑 + 单人 + 第4条` 返回：`眉：一侧眉尾抬起，另一侧眉尾压平；眼：一侧眼撑开看着[目标物]，另一侧眼半垂；嘴：一侧嘴巴闭住下压，另一侧嘴角收紧。`
- [ ] 输入 `负向 + 得意` 时提示极性错配。
- [ ] 输入未知表情类别时提示未找到类别。
- [ ] 表情库文件缺失或结构不完整时提示具体原因。

## Traces

- **Goal**: [G-002](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-002](../architecture/ADR-002-markdown-library.md)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-parser-library.md)
