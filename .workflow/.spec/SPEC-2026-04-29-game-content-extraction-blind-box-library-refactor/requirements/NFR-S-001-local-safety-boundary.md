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
id: NFR-S-001
type: non-functional
category: Security
priority: Must
---

# NFR-S-001: 重构不得突破本地静态数据安全边界

**Category**: Security
**Priority**: Must

## Requirement

本次重构 MUST 保持仓库当前的本地桌面工具边界。需求与后续实现 MUST NOT 引入远程服务依赖、在线配置拉取、新的账号体系或额外持久化面；静态数据文件与现有 `draw_history.json` 之外，不得扩展新的用户数据存储通道。

## Metric & Target

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 远程依赖数量 | 0 | 审查实施方案与依赖清单 |
| 新持久化面数量 | 0 个新增用户状态文件或数据库 | 审查数据目录与实现变更 |

## Traces

- **Goal**: [G-003](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-006](../architecture/ADR-006-history-compatibility.md) (if applicable)
