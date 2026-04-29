---
session_id: SPEC-2026-04-29-game-content-extraction-blind-box-library-refactor
phase: 5
document_type: epics-index
status: complete
generated_at: 2026-04-29T00:00:00+08:00
version: 1
dependencies:
  - ../spec-config.json
  - ../product-brief.md
  - ../requirements/_index.md
  - ../architecture/_index.md
---

# Epics: Game content extraction 盲盒物品内容库重构

## Epic Overview

| Epic | Title | Priority | MVP | Size | Requirements | Architecture |
|------|-------|----------|-----|------|--------------|--------------|
| [EPIC-001](EPIC-001-scene-taxonomy-and-pool-schema.md) | 场景入口与五层池模型 | Must | true | L | REQ-001, REQ-002, NFR-U-001 | ADR-001 |
| [EPIC-002](EPIC-002-legacy-compatibility-mapping.md) | 四栏兼容映射与历史边界 | Must | true | M | REQ-003, REQ-006, NFR-P-001, NFR-S-001 | ADR-002, ADR-005 |
| [EPIC-003](EPIC-003-pilot-category-content.md) | 三个试点类别内容交付 | Must | true | L | REQ-004, REQ-005, NFR-SC-001 | ADR-003, ADR-004 |
| [EPIC-004](EPIC-004-validation-review-and-doc-sync.md) | 质量验证、审查与文档同步 | Should | true | M | REQ-005, REQ-007, NFR-SC-001 | ADR-004 |

## Dependency Map

```mermaid
graph LR
    E1[EPIC-001 场景入口与五层池模型] --> E2[EPIC-002 四栏兼容映射]
    E1 --> E3[EPIC-003 三个试点类别内容交付]
    E2 --> E3
    E2 --> E4[EPIC-004 质量验证与文档同步]
    E3 --> E4
```

## Recommended Execution Order

1. **EPIC-001**: 先固定类别入口和五层 schema，否则后续映射和试点没有稳定输入。
2. **EPIC-002**: 在试点落数据前定义四栏输出 contract，保护旧输入和历史行为。
3. **EPIC-003**: 用三个试点类别生成真实样板，暴露内容质量问题。
4. **EPIC-004**: 最后补齐自动校验、人工审查记录和文档同步，形成可扩库门槛。

## MVP Scope

MVP 包含全部 4 个 epic，但范围限制在三个试点类别，不做 20 类全量重写、不改 UI 展示、不迁移 `draw_history.json`。

### MVP Definition of Done

- 20 个场景入口和五层池字段定义稳定。
- 三个试点类别均具备五层池和四栏映射。
- `blocked_or_risky` 零泄漏到默认四栏输出。
- 旧逗号输入、四栏选择、物品历史语义不回归。
- 试点人工抽样 30 次，不适合项低于 10%。

### Deferred Post-MVP

- 全量 20 类生产数据重写。
- 新 20 类 UI 展示和旧编号迁移。
- `draw_history.json` 新历史 key 或迁移脚本。
- 盲盒专用状态词白名单的完整产品化。

## Traceability Matrix

| Requirement | Epic | Stories |
|-------------|------|---------|
| REQ-001 | EPIC-001 | STORY-001-001, STORY-001-002 |
| REQ-002 | EPIC-001 | STORY-001-003, STORY-001-004 |
| REQ-003 | EPIC-002 | STORY-002-001, STORY-002-002 |
| REQ-004 | EPIC-003 | STORY-003-001, STORY-003-002, STORY-003-003 |
| REQ-005 | EPIC-003, EPIC-004 | STORY-003-004, STORY-004-001, STORY-004-002 |
| REQ-006 | EPIC-002 | STORY-002-003 |
| REQ-007 | EPIC-004 | STORY-004-003, STORY-004-004 |
| NFR-P-001 | EPIC-002 | STORY-002-002 |
| NFR-S-001 | EPIC-002, EPIC-004 | STORY-002-003, STORY-004-001 |
| NFR-SC-001 | EPIC-003, EPIC-004 | STORY-003-001, STORY-004-004 |
| NFR-U-001 | EPIC-001 | STORY-001-001 |

## Estimation Summary

| Size | Count | Notes |
|------|-------|-------|
| S | 5 | 文档、映射样例、审查记录类任务 |
| M | 8 | 数据结构、兼容测试、单类试点内容 |
| L | 2 | 20 类入口冻结与三类试点整体验收 |
| XL | 0 | MVP 不包含 XL story |

## References

- [Requirements](../requirements/_index.md)
- [Architecture](../architecture/_index.md)
- [Product Brief](../product-brief.md)
