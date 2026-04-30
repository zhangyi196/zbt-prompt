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
id: NFR-M-001
type: non-functional
category: Maintainability
priority: Should
status: complete
---

# NFR-M-001: 规则可维护性

**Category**: Maintainability
**Priority**: Should

## Requirement

规则集 SHOULD 让维护者在不打开全部 20 个场景列表的情况下理解第四池边界。正式规格、质量校验和文档同步规则 SHOULD 复用同一套术语、同一组禁区和同一套例外定义，避免维护者记忆多套口径。

## Metric & Target

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 规则扫描时间 | <= 10 分钟 | 维护者按 `_index.md` + REQ-001/003/004/006 完成一次规则复核 |
| 规则口径来源 | 1 套主定义 | 检查 glossary、REQ-001、REQ-004、`Game content extraction/agents.md` 是否一致 |
| 文档冗余 | 无完整 20 场景复制列表 | 文档人工审查 |

## Traces

- **Goal**: [G-001](../product-brief.md#goals--success-metrics), [G-005](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-006](../architecture/ADR-006-documentation-sync-policy.md)
