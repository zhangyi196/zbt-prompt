---
session_id: SPEC-2026-04-29-game-content-extraction-four-pool-refactor
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

**Game content extraction 盲盒物品四类内容池重构** 将三类试点盲盒从五层池重构为四类默认安全内容池：`core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`。该方向明确废弃 `conditional_items`、`anchor_required_items` 和 `blocked_or_risky` 候选池，因为工具不能识别图像，也不应把风险内容保留在可候选数据模型中。

## Scope

In scope:

- 15 `桌面+学习`、16 `海底+潜水`、17 `公园+野餐` 三个试点盒。
- 四池 schema 和四栏兼容映射。
- `scene_expansion_items` 场景扩展物内容定义和试点样板。
- `blocked_patterns` 回归测试。
- 项目文档同步。

Out of scope:

- 图像识别或锚点检测。
- 用户文本触发解析。
- UI 改版。
- 全量 20 类内容扩展。
- 版本发布和安装包。

## Key Requirements

| Type | Count | Focus |
|------|------:|-------|
| Functional | 6 | 四池 schema、场景扩展物、移除风险池、四栏兼容、试点重写、测试文档 |
| Non-functional | 2 | 回归防护、维护者可读性 |

## Architecture

架构采用静态数据模型重构：`BLIND_BOX_ITEM_POOL_BUNDLES` 保存四类试点内容，`_build_legacy_blind_box_entry` 派生旧四栏 `BLIND_BOXES`，`test_blind_box_content_model.py` 负责四池 schema 和 `blocked_patterns` 校验。

## Epics

| Epic | MVP | Purpose |
|------|-----|---------|
| EPIC-001 四池数据模型与兼容映射 | true | 建立四池 schema 并保持四栏运行时兼容 |
| EPIC-002 三类试点内容重写 | true | 按四池模型重写 15/16/17 内容 |
| EPIC-003 回归测试与文档同步 | true | 锁定质量规则并同步维护文档 |

## Quality Result

Readiness score: **96.5 / 100, Pass**.

## Recommended Next Step

运行：

```text
$workflow-plan .workflow/.spec/SPEC-2026-04-29-game-content-extraction-four-pool-refactor/spec-summary.md
```

或直接在下一轮使用 `$workflow-plan`，让计划器自动选择该最新规格包。

## Documents

- [Product Brief](product-brief.md)
- [Requirements](requirements/_index.md)
- [Architecture](architecture/_index.md)
- [Epics](epics/_index.md)
- [Readiness Report](readiness-report.md)
- [Issue Export Report](issue-export-report.md)
