---
name: green-circle-photo-prompts
description: "按文件夹批量生成绿圈洗图提示词。适用于用户给出图像文件夹路径、按 3 图一组分批、由主 agent 并行调度 4 个 GPT-5.4 high subagent，并把 `prompts/0.image-prompt/绿圈洗图 2 v1.2.1.1 3组.md` 作为系统提示词来源，为每张参考图写出对应英文提示词并保存为同目录同名 UTF-8 txt 文件的场景。"
---

# 绿圈洗图批处理

## 概述

把一个参考图文件夹转换成同名 `.txt` 提示词文件，用于批量洗图。
系统提示词不在 skill 内重写，固定直接调用 [绿圈洗图 2 v1.2.1.1 3组.md](</F:/vscode projects/zbt prompt/prompts/0.image-prompt/绿圈洗图 2 v1.2.1.1 3组.md>) 作为规则源；以后你只要改这份源文件，skill 的执行规则就会同步更新。

## 快速开始

1. 解析用户提供的文件夹路径；除非用户明确说明，否则默认递归处理子目录。
2. 在看图或分发任务前，先读取系统提示词源文件 `F:\vscode projects\zbt prompt\prompts\0.image-prompt\绿圈洗图 2 v1.2.1.1 3组.md`；`references/prompt-spec.md` 只负责说明调度方式和返回格式。
3. 先生成批处理清单：

   ```powershell
   python scripts/build_manifest.py "<folder-path>" --output ".workflow/.scratchpad/green-circle-photo-prompts/manifest.json"
   ```

4. 按 wave 逐轮处理。每轮最多并行 4 个 subagent；每个 subagent 最多处理 3 组图，每组默认 3 张，最后一组允许不足 3 张。
5. 汇总 subagent 返回的结构化结果，确认每张图都有 1 条提示词，再把 UTF-8 `.txt` 写回图片所在目录，文件名与参考图同名。
6. 如果同名 `.txt` 已存在，而用户没有明确要求覆盖，先停下来确认再写入。

## 工作流

### 1. 准备清单

- 对目标文件夹运行 `scripts/build_manifest.py`。
- 把 `.png`、`.jpg`、`.jpeg`、`.webp`、`.bmp`、`.gif`、`.tif`、`.tiff` 视为候选图片。
- 系统提示词固定来源是 `F:\vscode projects\zbt prompt\prompts\0.image-prompt\绿圈洗图 2 v1.2.1.1 3组.md`。
- 以脚本输出为唯一事实源，统一控制图片顺序、分组结果、wave 边界、目标 `.txt` 路径，以及现有同名文件冲突。
- 如果当前环境不支持 subagent，直接说明限制，再按同样的清单顺序串行处理。

### 2. 调度 subagent

- 使用 `spawn_agent`，并固定 `model: gpt-5.4`、`reasoning_effort: high`。
- 优先使用 `fork_context: false`，只传 skill 路径、系统提示词源文件路径、`references/prompt-spec.md` 路径，以及该 worker 的 assignment JSON，避免上下文过重。
- 保持 4 条 worker lane；如果某一轮不足 4 份有效 assignment，只创建非空 lane。
- 按轮转方式把分组分发到 4 条 lane，避免小批量任务全部堆到同一个 worker。
- 如果总分组数超过 12 组，继续开启下一轮 wave，直到 manifest 处理完毕。
- 主 agent 在发给 subagent 的任务中，必须明确要求先读取源文件全文，并把该文件内容视为本轮洗图的系统提示词。
- 不要让 subagent 直接写文件，只返回结构化结果。

### 3. 使用 worker 契约

给每个 worker 的提示可以等价于：

```text
使用位于 <skill-path> 的 skill。
先读取 <source-prompt-path>，并把该文件全文视为本轮洗图的系统提示词。
再读取 <skill-path>/references/prompt-spec.md，了解 assignment 格式和返回约束。
只处理下面 assignment JSON 中分配给你的图片。逐张看图，只返回 JSON：
[
  {
    "image_path": "绝对路径或相对根目录的图片路径",
    "text_path": "对应的 txt 路径",
    "prompt": "单条英文洗图提示词"
  }
]

约束：
- 每张图只返回 1 个对象。
- 提示词必须全英文。
- 提示词内容以源系统提示词文件为最高优先级。
- 如果源系统提示词要求固定起手式、风格、禁用词或输出格式，严格照做。
- 不要写文件。
- 不要处理未分配给你的图片。
```

### 4. 主 agent 汇总落盘

- 按 manifest 顺序合并所有 worker 返回数组。
- 如果某条提示词为空，或明显违反源系统提示词文件中的硬规则，先拦截并修正。
- 每个 `.txt` 只写 1 条提示词；不要加入编号、markdown 代码块或额外说明。
- 把每条提示词写入 manifest 指定的 `text_path`。
- 当文件较多，或需要统一处理覆盖逻辑时，优先使用 `scripts/write_prompt_files.py` 落盘。
- 对跳过或阻塞的文件单独汇报。

### 5. 收尾校验

- 确认提示词数量与图片数量完全一致。
- 确认每个 `.txt` 文件名都与图片 basename 完全对应。
- 按源系统提示词文件做一致性自检；如果源文件要求固定起手式、全英文输出、忽略 green circles / highlight rings / markers 等规则，逐条核对。
- 确认每条提示词都是单段英文，没有列表标记。
- 除非用户明确要求覆盖，否则先暴露重名冲突，再决定是否替换已有文件。

## 资源

- `prompts/0.image-prompt/绿圈洗图 2 v1.2.1.1 3组.md`：洗图系统提示词的唯一主规则来源。
- `references/prompt-spec.md`：说明如何把源系统提示词接入 subagent 调度，而不是替代主规则。
- `scripts/build_manifest.py`：用于稳定地发现图片、分组、切 wave，并生成目标 `.txt` 路径。
- `scripts/write_prompt_files.py`：用于把主 agent 汇总后的结果安全写成 UTF-8 文本文件。
