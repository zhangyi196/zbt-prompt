---
id: NFR-R-001
type: non-functional
category: Reliability
priority: Must
status: complete
---

# NFR-R-001: 防止非物品条目回归

**Category**: Reliability  
**Priority**: Must

## Requirement

测试 MUST 防止非物品禁用模式回流到任何五层池。

## Metric & Target

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| forbidden pattern coverage | 3/3 试点、5/5 池层 | `test_blind_box_content_model.py` |
| regression test result | pass | `python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'` |

## Traces

- **Goal**: [G-003](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-forbidden-pattern-validation.md)
