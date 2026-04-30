---
id: ADR-003
status: Accepted
traces_to: [REQ-003, NFR-U-001]
date: 2026-04-30T14:20:00+08:00
---

# ADR-003: 用质量闸门拦截超大与超小主体

## Context

第四池的主要风险不是结构缺失，而是内容失真。仅靠人工浏览很难在 20 个场景、1000 条第四池条目中稳定发现“柜/车/架/台”类超大主体和“卡/标签/票据/书签/单张”类超小主体。

## Decision

在现有 `test_blind_box_content_model.py` 回归基线上增加 scale-quality validation。校验必须识别超大与超小词根，必须允许“价格板”“记录板”“展开页组”“标签排版面”等合规中号例外，并在失败时输出 `scene_name`、`item_name`、`rule_id`、`message`、`recovery_hint`。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 在现有 `unittest` 中增加语义闸门 | 成本低，回归入口统一，可快速定位问题 | 需要维护规则词根 |
| 仅依靠人工审查 | 无需写规则 | 规模扩大后不稳定，遗漏率高 |
| 新建独立校验工具 | 规则可扩展 | 引入额外维护面，不符合最小变更目标 |

## Consequences

- **Positive**: 可以把语义错误变成可回归的失败项。
- **Negative**: 词根规则需要定期维护。
- **Risks**: 规则过严会误伤少量合规例外，需保留小范围白名单策略。

## Traces

- **Requirements**: [REQ-003](../requirements/REQ-003-scale-quality-validation.md), [NFR-U-001](../requirements/NFR-U-001-first-eye-visible-wording.md)
- **Implemented by**: [EPIC-003](../epics/EPIC-003-quality-boundary-and-regression-gates.md)
