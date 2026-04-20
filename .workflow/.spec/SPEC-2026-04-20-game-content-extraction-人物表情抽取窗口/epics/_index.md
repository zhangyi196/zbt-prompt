---
session_id: SPEC-2026-04-20-game-content-extraction-人物表情抽取窗口
phase: 5
document_type: epics-index
status: complete
generated_at: 2026-04-20T14:45:00+08:00
version: 1
dependencies:
  - ../spec-config.json
  - ../product-brief.md
  - ../requirements/_index.md
  - ../architecture/_index.md
---

# Epics & Stories: 人物表情抽取窗口

实现分为四个 epic：先搭建窗口 UI，再实现解析与表情库匹配，随后完成回填和错误提示，最后处理打包与验证。MVP 包含前三个 epic，第四个用于提高发布可靠性。

## Epic Overview

| Epic ID | Title | Priority | MVP | Stories | Est. Size |
|---------|-------|----------|-----|---------|-----------|
| [EPIC-001](EPIC-001-expression-window-ui.md) | 表情窗口 UI | Must | Yes | 3 | M |
| [EPIC-002](EPIC-002-parser-library.md) | 字段解析与表情库匹配 | Must | Yes | 5 | L |
| [EPIC-003](EPIC-003-output-errors.md) | 回填、复制与错误提示 | Must | Yes | 4 | M |
| [EPIC-004](EPIC-004-packaging-tests.md) | 打包与验证 | Should | No | 3 | M |

## Dependency Map

```mermaid
graph LR
    EPIC001[EPIC-001 UI] --> EPIC002[EPIC-002 Parser/Library]
    EPIC002 --> EPIC003[EPIC-003 Output/Errors]
    EPIC003 --> EPIC004[EPIC-004 Packaging/Tests]
```

### Dependency Notes

UI 可先搭出空窗口，但完整抽取依赖解析和查库。回填与错误提示依赖解析结果。打包和验证应在功能稳定后执行。

### Recommended Execution Order

1. [EPIC-002](EPIC-002-parser-library.md): 先完成纯逻辑函数，便于测试用户示例。
2. [EPIC-001](EPIC-001-expression-window-ui.md): 接入窗口和按钮。
3. [EPIC-003](EPIC-003-output-errors.md): 把逻辑接到 UI 输出和复制。
4. [EPIC-004](EPIC-004-packaging-tests.md): 验证打包路径和回归。

## MVP Scope

### MVP Epics

- [EPIC-001](EPIC-001-expression-window-ui.md): 用户可打开窗口并输入文本。
- [EPIC-002](EPIC-002-parser-library.md): 可按三元条件找到模板。
- [EPIC-003](EPIC-003-output-errors.md): 可输出增强结果并复制。

### MVP Definition of Done

- [ ] 用户示例 `负向 + 困惑 + 单人 + 第4条` 输出目标模板。
- [ ] 多行前置文档双组输入可分别增强。
- [ ] 现有主抽取流程无回归。
- [ ] 缺字段、错配、编号越界、表情库缺失都有中文提示。

## Traceability Matrix

| Requirement | Epic | Stories | Architecture |
|-------------|------|---------|--------------|
| [REQ-001](../requirements/REQ-001-expression-window.md) | [EPIC-001](EPIC-001-expression-window-ui.md) | STORY-001-001, STORY-001-002, STORY-001-003 | [ADR-001](../architecture/ADR-001-toplevel-window.md) |
| [REQ-002](../requirements/REQ-002-field-parser.md) | [EPIC-002](EPIC-002-parser-library.md) | STORY-002-001, STORY-002-002 | [ADR-003](../architecture/ADR-003-parse-and-replace.md) |
| [REQ-003](../requirements/REQ-003-library-lookup.md) | [EPIC-002](EPIC-002-parser-library.md) | STORY-002-003, STORY-002-004 | [ADR-002](../architecture/ADR-002-markdown-library.md) |
| [REQ-004](../requirements/REQ-004-template-selection.md) | [EPIC-002](EPIC-002-parser-library.md) | STORY-002-005 | [ADR-003](../architecture/ADR-003-parse-and-replace.md) |
| [REQ-005](../requirements/REQ-005-output-copy.md) | [EPIC-003](EPIC-003-output-errors.md) | STORY-003-001, STORY-003-002 | [ADR-003](../architecture/ADR-003-parse-and-replace.md) |
| [REQ-006](../requirements/REQ-006-error-handling.md) | [EPIC-003](EPIC-003-output-errors.md) | STORY-003-003, STORY-003-004 | [ADR-003](../architecture/ADR-003-parse-and-replace.md) |
| [NFR-R-001](../requirements/NFR-R-001-no-regression.md) | [EPIC-004](EPIC-004-packaging-tests.md) | STORY-004-001, STORY-004-002 | [ADR-001](../architecture/ADR-001-toplevel-window.md) |

## Estimation Summary

| Size | Meaning | Count |
|------|---------|-------|
| S | Small, isolated task | 4 |
| M | Moderate UI or integration task | 7 |
| L | Parser/library logic with edge cases | 1 |
| XL | Must split before implementation | 0 |

## Risks & Considerations

| Risk | Affected Epics | Mitigation |
|------|----------------|------------|
| Markdown 结构变化 | [EPIC-002](EPIC-002-parser-library.md) | 加结构校验和清晰错误 |
| UI 挤压主窗口 | [EPIC-001](EPIC-001-expression-window-ui.md) | 使用独立 Toplevel |
| 重复回填叠加 | [EPIC-003](EPIC-003-output-errors.md) | 检测已有眉/眼/嘴 |
| 打包找不到库 | [EPIC-004](EPIC-004-packaging-tests.md) | 更新 spec datas |

## Versioning & Changelog

### Version Strategy

- **Versioning Scheme**: feature version v1 for MVP.
- **Breaking Change Definition**: 改变现有主输入语法或输出语义即视为破坏性变更。
- **Deprecation Policy**: 不删除现有盲盒/动物抽取功能。

### Changelog

| Version | Date | Type | Description |
|---------|------|------|-------------|
| v1 | 2026-04-20 | Added | 新增人物表情抽取窗口规格 |

## Open Questions

- [ ] 默认模板策略。
- [ ] 打包读取 Markdown 的最终路径策略。

## References

- Derived from: [Requirements](../requirements/_index.md), [Architecture](../architecture/_index.md)
- Handoff to: execution workflows
