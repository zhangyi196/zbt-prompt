---
id: NFR-R-001
type: non-functional
category: Reliability
priority: Must
status: complete
---

# NFR-R-001: 不回归现有抽取

**Category**: Reliability
**Priority**: Must

## Requirement

新增人物表情抽取窗口 MUST NOT 改变现有盲盒/动物抽取语法、按钮语义、draw_history.json 结构和复制结果行为。

## Metric & Target

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 现有输入解析回归 | 0 个失败 | 运行示例输入 `1,5,地面动物,无大型物品,中型物品+1` |
| draw_history.json schema 变化 | 0 | 代码和文件检查 |

## Traces

- **Goal**: [G-003](../product-brief.md#goals--success-metrics)
- **Architecture**: [ADR-001](../architecture/ADR-001-toplevel-window.md)
