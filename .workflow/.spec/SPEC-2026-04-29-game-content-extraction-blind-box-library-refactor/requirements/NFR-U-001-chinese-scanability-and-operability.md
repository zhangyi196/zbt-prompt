---
session_id: SPEC-2026-04-29-game-content-extraction-blind-box-library-refactor
phase: 3
document_type: requirements
status: complete
generated_at: 2026-04-29T00:00:00+08:00
stepsCompleted:
  - load-context
  - expand-requirements
  - codex-review
version: 1
dependencies:
  - ../product-brief.md
  - ../glossary.json
id: NFR-U-001
type: non-functional
category: Usability
priority: Must
---

# NFR-U-001: 类别命名与操作入口保持高可扫读性

**Category**: Usability
**Priority**: Must

## Requirement

新入口命名 MUST 服务中文 UI 的快速扫描。20 个类别 SHOULD 使用短而稳定的“场景+用途”格式；后续实现 MUST 保持现有输入习惯、分栏心智和输出阅读方式，不要求用户学习额外的专业术语或新操作流。

## Metric & Target

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 命名格式一致性 | 20/20 类别遵循“场景+用途” | 对类别表进行人工校对 |
| 输入习惯变更 | 0 个强制新增输入步骤 | 对实施方案与现有使用说明做差异检查 |

## Traces

- **Goal**: [G-001](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-001](../architecture/ADR-001-scene-entry-model.md) (if applicable)
