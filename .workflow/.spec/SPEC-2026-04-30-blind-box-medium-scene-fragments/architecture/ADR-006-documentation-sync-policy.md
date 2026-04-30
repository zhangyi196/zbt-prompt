---
id: ADR-006
status: Accepted
traces_to: [REQ-006, NFR-M-001]
date: 2026-04-30T14:20:00+08:00
---

# ADR-006: 将文档同步限定为稳定规则边界

## Context

仓库入口文档必须保持精简，但第四池语义又需要被长期维护者复用。如果把完整 spec 或 20 场景长列表复制进 `agents.md`、`Game content extraction/agents.md` 或 `README.md`，会快速造成重复和漂移。

## Decision

文档同步只覆盖稳定规则边界，不同步长内容表。实施完成后必须检查 `agents.md`、`Game content extraction/agents.md`、`README.md`、`.gitignore` 四个文件是否与新语义一致；其中仅 `Game content extraction/agents.md` 在必要时增加一到少量规则，用于固定 medium-scale scene fragment 定义和禁区边界；`README.md` 只在用户可见行为变化时更新。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 只同步稳定规则 | 文档精简，入口清楚，漂移小 | 详细背景需要回看 spec |
| 复制完整 spec 内容到入口文档 | 单处可读 | 极易过时，入口文件膨胀 |
| 不同步入口文档 | 省时 | 稳定规则无法被后续维护快速发现 |

## Consequences

- **Positive**: 维护者能在入口文件看到必须遵守的稳定规则。
- **Negative**: 详细设计背景仍需查阅 spec。
- **Risks**: 如果实施者忘记做同步检查，会造成规范和代码脱节。

## Traces

- **Requirements**: [REQ-006](../requirements/REQ-006-documentation-sync-checks.md), [NFR-M-001](../requirements/NFR-M-001-rule-maintainability.md)
- **Implemented by**: [EPIC-004](../epics/EPIC-004-doc-sync-and-maintainer-review.md)
