# Project: zbt-prompt

## What This Is

找不同游戏的 AI 提示词规则仓库，包含三条核心提示词链路（绿圈洗图、主图生成、组图差异）和盲盒数据管理桌面工具。面向内部生产人员，目标是稳定产出可玩的找不同差异点。

## Core Value

内部人员能稳定执行找不同游戏差异点生产流程 —— AI 生成的差异点分布均匀、位置描述不依赖颜色/材质、紧邻物体不冲突。

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] 优化 `prompts/2.group-image/组图 23.md`：差异点空间分布按九宫格均匀覆盖（左上/中上/右上/左中/中心/右中/左下/中下/右下），List 1 + List 2 合起来覆盖大部分区域
- [ ] 优化位置描述规则：禁止颜色/材质等前缀修饰词（如"褐色的墙壁"），避免 VLM 模型颜色识别错误导致大面积差异点
- [ ] 优化紧邻物体冲突规则：画面上紧挨着的物体不得同时被设为差异点，必须在空间上分散
- [ ] 同步检查并优化 `prompts/` 下其他文件的相关规则，保持一致性

### Out of Scope

- 不改变盲盒 20 类别体系 — 数据事实源保持稳定
- 不修改桌面工具（Game content extraction/）— 当前聚焦提示词
- 不调整表情库（组图 23 表情库.md）— 表情模板保持不变
- 不改变现有链路结构（第一步→第二步、表情前置→组图23）— 只优化规则内容

## Context

项目已有成熟的提示词链路和盲盒数据体系。近期发现组图 23 的生成结果存在三个核心问题：差异点空间分布不均（某些区域扎堆、某些区域空白）、VLM 模型因颜色描述产生大面积识别错误、紧邻物体被同时修改导致冲突。本次优化聚焦于强化空间分布的九宫格约束、禁止位置字段中的颜色/材质修饰、以及增加紧邻物体互斥规则。

## Constraints

- **输出语言**: 提示词规则使用中文，UTF-8 编码
- **全局硬规则**: 禁脑补、一圈一物一变化、禁改灯光/人物骨架/姿态、位置字段只定位
- **兼容性**: 不破坏现有链路，不改输出格式和字段名
- **国际化**: 盲盒数据默认面向欧美用户，避免强中式绑定

## Tech Stack

- **Language**: Markdown（提示词规则）、Python 3.13（桌面工具）
- **Framework**: tkinter/ttk（桌面工具原生 GUI）
- **AI Skill**: Claude Code Skills（绿圈洗图批处理）

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 位置字段禁止颜色/材质修饰 | VLM 颜色识别不稳定，导致大面积错误差异点 | Pending |
| 九宫格均匀分布作为硬约束 | 当前差异点容易扎堆，需要空间配额兜底 | Pending |
| 提示词优化优先，不动数据和工具 | 问题根源在规则表达，不在数据或工具 | Pending |

## Stakeholders

- 内部生产人员（直接用户）

---
## Milestone Status

- 2026-06-18: M2 completed and archived. Group-image salience rules passed audit after root navigation and roadmap state were synchronized.

---
*Last updated: 2026-06-18 after M2 completion*
