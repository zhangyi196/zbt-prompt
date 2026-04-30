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
id: NFR-U-001
type: non-functional
category: Usability
priority: Should
status: complete
---

# NFR-U-001: 首眼可见命名一致性

**Category**: Usability
**Priority**: Should

## Requirement

20 个场景的第四池条目 SHOULD 保持“首眼可见、边界清楚、可整体圈选”的命名质量。条目 SHOULD 使用清晰中文名词短语表达中号片段，不依赖光影、反光、透明、细线、微痕或抽象状态词来成立。

## Metric & Target

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 首眼可见条目占比 | 100% | 人工抽检每场景代表性条目 |
| 微小主体误入率 | 0 | 超小主体质量校验 |
| 抽象命名误入率 | 0 | 场景列表人工复核 |

## Traces

- **Goal**: [G-002](../product-brief.md#goals--success-metrics), [G-003](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-scale-quality-validation.md)
