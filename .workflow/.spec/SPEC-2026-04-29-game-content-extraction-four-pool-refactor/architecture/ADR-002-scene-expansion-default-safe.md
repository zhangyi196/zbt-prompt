---
id: ADR-002
status: Accepted
traces_to: [REQ-002, REQ-005]
date: 2026-04-29T00:00:00+08:00
---

# ADR-002: 场景扩展物作为第四类内容

## Context

第四类不应继续表达条件、锚点、悬挂或风险。用户明确希望将原 `anchor_required_items` 重构为 `scene_expansion_items`，用于增加场景变化。

## Decision

`scene_expansion_items` 定义为默认安全的场景扩展物：中等以上、边界清楚、可单独圈选、从场景类别本身即可成立，不依赖图像中已有显示器、白板、伞杆、墙面挂点等前置对象。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| `scene_expansion_items` | 扩展性好，不依赖锚点或悬挂 | 需要严控不变成杂物池 |
| `safe_hanging_items` | 能对接旧 hanging | 过窄，容易回到挂饰/细绳问题 |
| `explicit_context_items` | 可由用户文本触发 | 本阶段不想扩展输入解析 |

## Consequences

- **Positive**: 第四类有正向内容价值，适合默认抽取。
- **Negative**: 需要人工审查物品是否确实场景相关。
- **Risks**: 不合理扩展物可能稀释场景主题。

## Traces

- **Requirements**: [REQ-002](../requirements/REQ-002-scene-expansion-items.md), [REQ-005](../requirements/REQ-005-pilot-content-rewrite.md)
- **Implemented by**: [EPIC-002](../epics/EPIC-002-pilot-content-rewrite.md)
