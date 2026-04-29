---
session_id: SPEC-2026-04-29-blind-box-pool-itemization-fix
phase: 6
document_type: spec-summary
status: complete
generated_at: 2026-04-29T00:00:00+08:00
stepsCompleted:
  - synthesis
version: 1
dependencies:
  - product-brief.md
  - requirements/_index.md
  - architecture/_index.md
  - epics/_index.md
  - readiness-report.md
---

# Spec Summary

## Product

**盲盒条件池与风险池物品化修正** 是对上一次盲盒物品库试点的窄范围补丁规格。它要求 `conditional_items` 和 `blocked_or_risky` 都只包含具体物品；折线、擦痕、气泡、阴影、边线、微小颗粒等非物品表达只作为 forbidden patterns 校验规则存在。

## Scope

In scope:

- 修正 15 `桌面+学习`、16 `海底+潜水`、17 `公园+野餐` 的 `conditional_items`。
- 修正三类试点的 `blocked_or_risky`。
- 新增 forbidden patterns 测试。
- 同步项目文档。

Out of scope:

- 全量 20 类重写。
- UI、输入语法、历史 key 或四栏输出变化。
- 字段重命名和版本发布。

## Key Requirements

| Type | Count | Focus |
|------|-------|-------|
| Functional | 5 | 条件池物品化、风险池具体物、禁用模式校验、兼容保持、文档同步 |
| Non-functional | 2 | 防回归、维护者可读性 |

## Architecture

架构采用静态数据补丁 + 单元测试校验。`blind_boxes.py` 继续保留五层池与四栏兼容视图；`test_blind_box_content_model.py` 负责阻止 forbidden patterns 回流；文档负责固定维护规则。

## Epics

| Epic | MVP | Purpose |
|------|-----|---------|
| EPIC-001 三类试点池层内容修正 | true | 替换条件池和风险池内容。 |
| EPIC-002 禁用模式校验与文档同步 | true | 增加测试并同步文档。 |

## Quality Result

Readiness score: **95.25 / 100, Pass**. All 7 requirements have acceptance criteria, architecture coverage, and story coverage.

## Recommended Next Step

进入执行时，按 EPIC-001 -> EPIC-002 顺序：先替换三类试点内容，再加 forbidden patterns 测试和文档同步。

## Documents

- [Product Brief](product-brief.md)
- [Requirements](requirements/_index.md)
- [Architecture](architecture/_index.md)
- [Epics](epics/_index.md)
- [Readiness Report](readiness-report.md)
- [Issue Export Report](issue-export-report.md)
