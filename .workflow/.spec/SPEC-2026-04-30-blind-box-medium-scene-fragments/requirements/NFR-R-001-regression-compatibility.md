---
session_id: SPEC-2026-04-30-blind-box-medium-scene-fragments
phase: 3
document_type: requirements
kind: non-functional
generated_at: 2026-04-30T13:10:00+08:00
stepsCompleted:
  - load-context
  - expand-requirements
  - codex-review
version: 1
dependencies:
  - ../product-brief.md
  - ../glossary.json
  - ../refined-requirements.json
id: NFR-R-001
type: non-functional
category: Reliability
priority: Must
status: complete
---

# NFR-R-001: 回归兼容性

**Category**: Reliability
**Priority**: Must

## Requirement

第四池重写后的数据和校验 MUST 保持现有回归基线稳定。任何实现若导致场景数量、四池结构、每池数量唯一性、兼容映射或既有 `unittest` 失败，均视为不满足规格。

## Metric & Target

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 现有 `unittest` 通过率 | 100% | `python -B -m unittest discover -s . -p 'test_*.py'` |
| 四池结构回归错误 | 0 | 结构断言和兼容映射断言 |
| 第四池质量规则漏检 | 0 个已知示例 | 人工样例 + 自动质量测试 |

## Traces

- **Goal**: [G-004](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-005](../architecture/ADR-005-runtime-compatibility.md)
