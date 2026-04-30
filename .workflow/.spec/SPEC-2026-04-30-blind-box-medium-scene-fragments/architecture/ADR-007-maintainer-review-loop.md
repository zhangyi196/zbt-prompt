---
id: ADR-007
status: Accepted
traces_to: [REQ-007]
date: 2026-04-30T14:20:00+08:00
---

# ADR-007: 固定维护者审查闭环

## Context

第四池重写既有规则层风险，也有内容层和文档层风险。若维护者没有统一审查顺序，常见结果是先修文档、后发现内容仍不合格，或只修内容却遗漏稳定规则入口。

## Decision

固定三步审查闭环：先做规则模型复核，再做 20 场景内容复核，最后做稳定文档同步复核。校验输出统一使用 `error`、`warning`、`info` 严重级别，并复用 glossary 中的规范术语。修复顺序固定为“删超大主体 -> 删超小主体 -> 处理跨池冲突 -> 最后补文档”。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 固定审查闭环与修复顺序 | 流程稳定，反馈可复用 | 对临时快速试验不够灵活 |
| 由维护者自由决定顺序 | 灵活 | 容易遗漏文档或边界问题 |
| 只提供测试，不定义人工复核步骤 | 自动化简单 | 无法保证规则可读性和文档一致性 |

## Consequences

- **Positive**: 审查反馈格式和修复动作更加一致。
- **Negative**: 需要维护者遵守统一流程。
- **Risks**: 若 severity 或术语不统一，反馈仍会变得难以扫描。

## Traces

- **Requirements**: [REQ-007](../requirements/REQ-007-maintainer-feedback-and-review.md)
- **Implemented by**: [EPIC-004](../epics/EPIC-004-doc-sync-and-maintainer-review.md)
