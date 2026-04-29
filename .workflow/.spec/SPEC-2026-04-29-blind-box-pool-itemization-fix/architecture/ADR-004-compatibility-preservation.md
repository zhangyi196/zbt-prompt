---
id: ADR-004
status: Accepted
traces_to: [REQ-004]
date: 2026-04-29T00:00:00+08:00
---

# ADR-004: 保持四栏运行时兼容

## Context

这次反馈针对内容质量，不针对 UI、输入语法或历史结构。扩大为运行时重构会偏离目标。

## Decision

保持 15/16/17 试点盒号、`BLIND_BOXES` 四栏输出、逗号输入语法、`draw_history.json` 语义全部不变。只修改静态内容、测试和文档。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 只修静态内容与测试 | 风险低，直接解决反馈 | 不处理长期字段命名问题 |
| 改 UI 展示条件池/风险池 | 更透明 | 超出本反馈范围 |
| 改历史 key 到新五层模型 | 长期更纯 | 高风险且不必要 |

## Consequences

- **Positive**: 可快速实施，不破坏已有用户习惯。
- **Negative**: 五层模型仍通过兼容层映射到四栏。
- **Risks**: 后续若继续扩库，需要再次审查字段语义。

## Traces

- **Requirements**: [REQ-004](../requirements/REQ-004-pilot-runtime-compatibility.md)
