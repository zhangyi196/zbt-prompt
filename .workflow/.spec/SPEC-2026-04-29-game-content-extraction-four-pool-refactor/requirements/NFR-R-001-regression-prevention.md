---
id: NFR-R-001
type: non-functional
category: Reliability
priority: Should
status: complete
---

# NFR-R-001: 防止条件池 / 风险池 / 低质量词回流

**Category**: Reliability
**Priority**: Should

## Requirement

测试必须防止旧 `conditional_items`、`blocked_or_risky`、锚点依赖词、细线/痕迹/光效/动物本体等低质量模式回流到默认候选池。

## Metric & Target

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 回归测试通过率 | 100% | `python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'` |
| 旧 key 回流 | 0 | schema tests |
| 禁用模式回流 | 0 | blocked pattern scan |

## Traces

- **Goal**: [G-003](../product-brief.md#goals--success-metrics), [G-005](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-risk-as-validation.md)
