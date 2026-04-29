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
id: REQ-001
type: functional
priority: Must
traces_to:
  - G-001
---

# REQ-001: 定义 20 个场景入口分类法

**Priority**: Must

## Description

系统规范 MUST 定义 20 个中文“场景+用途”入口，并为每个入口提供固定名称、场景提示和是否为试点类别的标记。该分类法 MUST 取代旧式宽泛主题作为后续盲盒内容重写的唯一入口词表，但 MUST NOT 在 Phase 3 里要求立即废弃旧编号。

## User Story

As a 内容维护者, I want to 使用统一的 20 类入口重写盲盒库 so that 我能稳定判断一个物品属于哪个场景，并避免旧主题命名继续漂移。

## Acceptance Criteria

- [ ] PRD MUST 列出 20 个完整入口，名称全部使用中文短名并遵循“场景+用途”模式。
- [ ] 每个入口 MUST 包含 `name_zh`、`scene_hint`、`pilot` 三个最小属性，且 `pilot` 只允许标记 `桌面+学习`、`海底+潜水`、`公园+野餐`。
- [ ] 入口表 MUST 保留与旧编号体系共存的空间，例如 `legacy_aliases` 或等价映射字段，但 MUST NOT 要求本阶段删除旧编号。
- [ ] `海底+潜水` MUST 作为特殊主题保留，不得被合并进泛化的海洋或旅行类入口。

## Traces

- **Goal**: [G-001](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-001](../architecture/ADR-001-scene-entry-model.md) (if applicable)
- **Implemented by**: [EPIC-001](../epics/EPIC-001-scene-entry-taxonomy.md) (added in Phase 5)
