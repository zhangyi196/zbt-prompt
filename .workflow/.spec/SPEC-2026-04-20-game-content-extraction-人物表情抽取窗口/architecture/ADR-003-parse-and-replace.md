---
id: ADR-003
status: Accepted
traces_to: [REQ-002, REQ-004, REQ-005, REQ-006]
date: 2026-04-20T14:44:00+08:00
---

# ADR-003: 解析字段并原文局部回填

## Context

用户希望返回的文本和输入文本保持一致，只在 `具体表情` 后追加模板。重写全文会增加格式漂移风险。

## Decision

解析器记录具体表情字段值的字符 span。匹配模板后，回填引擎只替换该 span，不重排其他字段。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 原文局部回填 | 最大限度保留格式 | span 解析要谨慎 |
| 重新生成标准格式 | 实现简单 | 破坏用户原文和字段顺序 |
| 只输出模板片段 | 最简单 | 用户仍需手动拼接 |

## Consequences

- **Positive**: 输出可直接交给下游 prompt。
- **Negative**: 单行连续字段的边界解析需要测试覆盖。
- **Risks**: 重复回填可能叠加，需要检测已有眉/眼/嘴。

## Traces

- **Requirements**: [REQ-002](../requirements/REQ-002-field-parser.md), [REQ-004](../requirements/REQ-004-template-selection.md), [REQ-005](../requirements/REQ-005-output-copy.md), [REQ-006](../requirements/REQ-006-error-handling.md)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-parser-library.md), [EPIC-003](../epics/EPIC-003-output-errors.md)
