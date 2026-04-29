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
  - ../discovery-context.json
id: NFR-P-001
type: non-functional
category: Performance
priority: Must
---

# NFR-P-001: 兼容映射不得增加可感知运行时负担

**Category**: Performance
**Priority**: Must

## Requirement

试点实施时，五层池到四栏的兼容映射 MUST 保持现有抽取主路径的轻量特性。映射层 SHOULD 是静态、可预计算或单次查表式的；实现方案 MUST NOT 为一次抽取引入额外多轮桶级扫描、远程调用或高频持久化操作。

## Metric & Target

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 运行时映射步骤 | 每次抽取最多增加 1 次确定性映射决策 | 对实现方案做流程审查，确认不存在额外多轮 bucket 重算 |
| 抽取路径结构 | 保持现有单次输入解析 -> bucket 选择 -> 条目抽取主链路 | 对 `内容抽取.py` 的实现 diff 做人工检查 |

## Traces

- **Goal**: [G-003](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-003](../architecture/ADR-003-four-bucket-compatibility.md) (if applicable)
