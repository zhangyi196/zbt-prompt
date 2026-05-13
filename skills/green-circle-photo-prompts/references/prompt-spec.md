# 绿圈洗图系统提示词接入说明

## 主规则来源

- 洗图系统提示词固定来源：
  `F:\vscode projects\zbt prompt\prompts\0.image-prompt\绿圈洗图 2 v1.2.1.1 3组.md`
- 该文件是唯一主规则来源。
- 本文件只负责说明主 agent / subagent 如何接入和返回结果，不负责替代、改写或摘录源系统提示词。

## 主 agent 职责

- 先读取源系统提示词文件全文。
- 在每次调用 subagent 时，明确要求 subagent 先读取该文件，并把该文件内容视为本轮洗图系统提示词。
- 主 agent 只负责分组、调度、汇总、落盘和校验，不在 skill 内自行重写系统提示词正文。

## Subagent 职责

- 先读取源系统提示词文件，再处理分配到的图片。
- 只处理 assignment JSON 中的图片，不越权处理其他文件。
- 返回结果时遵守源系统提示词文件中的全部硬规则。
- 不直接写 `.txt`，只返回结构化 JSON。

## 返回格式

只返回 JSON：

```json
[
  {
    "image_path": "path/to/image.png",
    "text_path": "path/to/image.txt",
    "prompt": "single prompt text"
  }
]
```

每张分配到的图片必须且只允许返回 1 个对象。

## 收尾检查

- 主 agent 合并 worker 结果后，按源系统提示词文件逐条做一致性检查。
- 如果源文件更新，skill 不需要复制新规则，只需要继续读取该源文件。
