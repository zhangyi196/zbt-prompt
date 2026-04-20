---
id: NFR-P-001
type: non-functional
category: Performance
priority: Must
status: complete
---

# NFR-P-001: 本地快速处理

**Category**: Performance
**Priority**: Must

## Requirement

人物表情抽取窗口 MUST 在本地完成解析、查库和回填，不引入网络调用。

## Metric & Target

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 双组输入处理耗时 | <= 500ms | 手工或自动计时 |
| 外部网络调用 | 0 | 代码检查 |

## Traces

- **Goal**: [G-002](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-002](../architecture/ADR-002-markdown-library.md)
