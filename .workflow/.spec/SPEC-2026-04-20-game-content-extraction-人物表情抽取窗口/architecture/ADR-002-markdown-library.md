---
id: ADR-002
status: Accepted
traces_to: [REQ-003, NFR-P-001]
date: 2026-04-20T14:44:00+08:00
---

# ADR-002: 读取 Markdown 表情库

## Context

表情模板已维护在 `组图 23 表情库.md`。复制到 Python 常量会产生双份维护风险。

## Decision

MVP 运行时读取 Markdown 表情库，并解析正向/负向章节、表情标题、单人/多人段和编号模板。若打包后路径不可控，再考虑生成 `data/expressions.py`。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 运行时读取 Markdown | 单一事实源，维护简单 | 打包路径需要处理 |
| Python 常量 | 打包稳定 | 双份维护 |
| JSON 中间文件 | 解析简单 | 增加生成和同步步骤 |

## Consequences

- **Positive**: 表情库更新后工具自动使用最新内容。
- **Negative**: Markdown 结构变化会影响解析。
- **Risks**: PyInstaller datas 配置缺失导致文件找不到。

## Traces

- **Requirements**: [REQ-003](../requirements/REQ-003-library-lookup.md), [NFR-P-001](../requirements/NFR-P-001-local-fast.md)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-parser-library.md), [EPIC-004](../epics/EPIC-004-packaging-tests.md)
