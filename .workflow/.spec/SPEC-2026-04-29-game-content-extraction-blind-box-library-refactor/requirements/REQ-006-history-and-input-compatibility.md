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
  - ../refined-requirements.json
  - ../discovery-context.json
id: REQ-006
type: functional
priority: Should
traces_to:
  - G-003
---

# REQ-006: 保持输入语法与历史语义兼容

**Priority**: Should

## Description

重构方案 SHOULD 在内容层定义清楚与现有编号输入、分栏覆盖语法和 `draw_history.json` 之间的兼容边界。该需求聚焦“不能破坏什么”，而不是立即设计迁移脚本。

## User Story

As a 开发维护者, I want to 在文档中先锁定兼容边界 so that 我能在不惊动现有用户输入习惯和历史逻辑的前提下推进试点实现。

## Acceptance Criteria

- [ ] 规范 SHOULD 明确保留当前逗号分隔、编号输入和按 bucket 覆盖的输入语法，且 MUST NOT 要求用户在试点阶段学习新格式。
- [ ] `draw_history.json` 的 `item_pools` 语义 SHOULD 继续按旧 box id 与 bucket key 降权；Phase 3 MUST NOT 把表情或动物历史混入盲盒历史设计。
- [ ] 若后续需要从旧编号迁移到新 20 类入口，PRD SHOULD 要求单独定义映射表或迁移脚本，而不是隐式修改既有 key。
- [ ] 兼容章节 MUST 记录与 `Game content extraction/内容抽取.py`、`draw_history.json` 的集成点，便于实现 phase 验证。

## Traces

- **Goal**: [G-003](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-006](../architecture/ADR-006-history-compatibility.md) (if applicable)
- **Implemented by**: [EPIC-006](../epics/EPIC-006-compatibility-guardrails.md) (added in Phase 5)
