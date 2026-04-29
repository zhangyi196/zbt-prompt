---
id: ADR-003
status: Accepted
traces_to: [REQ-003, NFR-R-001]
date: 2026-04-29T00:00:00+08:00
---

# ADR-003: 非物品禁用模式进入测试校验

## Context

折线、擦痕、气泡、阴影、边线、微小颗粒等表达对写库有警示价值，但不能作为物品条目保存。

## Decision

把这些表达定义为 `forbidden_patterns` 校验概念，在测试中检查三类试点的所有五层池，确保禁用模式不进入内容数据。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 测试中维护 forbidden patterns | 实施快，无运行时影响 | 规则不对外导出 |
| 数据模块导出 forbidden patterns | 可供更多工具复用 | 稍微增加数据 API 面 |
| 只靠文档约束 | 零代码成本 | 无法防止回归 |

## Consequences

- **Positive**: 非物品内容回流会立即被测试发现。
- **Negative**: 关键词需要谨慎，避免误伤合法物品。
- **Risks**: 若 forbidden patterns 太宽泛，可能限制正常命名。

## Traces

- **Requirements**: [REQ-003](../requirements/REQ-003-forbidden-pattern-validation.md), [NFR-R-001](../requirements/NFR-R-001-regression-prevention.md)
