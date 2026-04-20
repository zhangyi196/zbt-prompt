# Brainstorm Session

**Session ID**: BS-2026-04-20-game-content-extraction-人物表情抽取窗口
**Topic**: 为 Game content extraction 新增人物表情内容抽取窗口
**Started**: 2026-04-20T00:00:00+08:00
**Dimensions**: technical, ux, feasibility, scalability
**Mode**: Balanced

## Table of Contents
- [Session Context](#session-context)
- [Current Ideas](#current-ideas)
- [Exploration Vectors](#exploration-vectors)
- [Thought Evolution Timeline](#thought-evolution-timeline)
- [Synthesis & Conclusions](#synthesis--conclusions)

## Current Ideas

1. **独立人物表情抽取窗口** - 主窗口新增按钮，打开专用 Toplevel；不改现有盲盒/动物抽取输入与输出。
2. **原文局部回填** - 保持用户粘贴文本的字段顺序和其余内容，只增强“具体表情”字段。
3. **Markdown 表情库解析器** - 直接读取 `组图 23 表情库.md`，按正向/负向、表情名、单人/多人、编号模板索引。
4. **模板编号可控策略** - 支持指定模板编号以复现示例，同时保留自动/随机扩展空间。
5. **多组批量增强** - 一次处理负向组 + 正向组，适配 `组图 23 表情前置.md` 默认输出。

## Session Context
- Focus areas: 新窗口入口、表情库匹配、输入文本解析、结果回填、错误提示
- Perspectives: creative, pragmatic, systematic
- Constraints: 不修改现有提示词规则；优先贴合当前工具结构；支持中文字段；只做分析与实施范围建议
- Seed example: 输入一段包含「极性 / 剧情 / 单人多人 / 具体表情」等字段的文本，工具根据极性、具体表情、单人/多人从 `组图 23 表情库.md` 抽取对应眉眼嘴模板，并直接追加到「具体表情」字段后。

## Exploration Vectors
1. 当前 Game content extraction 工具的窗口、处理按钮和输出区如何组织？
2. 表情库 Markdown 的稳定结构是什么，能否用确定性解析而不是模型推断？
3. 输入字段可能换行、同一行、带全角/半角冒号时如何鲁棒识别？
4. 匹配结果应该选择固定条目、首条、轮换条目，还是允许用户选择？
5. 追加到「具体表情」后的返回格式如何保持原文其他字段不变？
6. 缺字段、未知表情、极性不匹配、单人/多人不匹配时怎么提示？
7. 后续如何与 `组图 23 表情前置.md` 和 `组图 23.md` 的链路接上？

## Initial Decisions

> **Decision**: 本轮采用 Balanced 模式，使用 creative / pragmatic / systematic 三个视角。
> - **Context**: 用户已经给出明确示例，但还需要把功能落成窗口和抽取规则。
> - **Options considered**: 直接实施、先写完整 PRD、轻量脑暴形成实施范围。
> - **Chosen**: 轻量脑暴形成实施范围 - **Reason**: 用户显式调用 `brainstorm-with-file`，该技能要求不直接改源码。
> - **Rejected**: 直接改源码，因为当前技能为 brainstorming-only。
> - **Impact**: 输出会聚焦于设计、规则、实施清单和后续 handoff。

---

## Thought Evolution Timeline

### Round 1 - Divergent Exploration (2026-04-20T00:00:00+08:00)

#### User Input
用户希望为 `Game content extraction` 新增窗口，用于抽取人物表情内容。输入文本包含极性、剧情、单人/多人、具体表情、人物定位、表情功能、适配提示、禁用区域；工具根据极性、具体表情、单人/多人从 `组图 23 表情库.md` 抽取对应眉 / 眼 / 嘴模板，并追加到“具体表情”字段后。

#### Decision Log

> **Decision**: 新功能采用独立窗口，而不是复用现有盲盒输入框。
> - **Context**: 当前输入框是逗号分隔单行盲盒/动物输入，用户新需求是多字段文本增强。
> - **Options considered**: 复用主输入框、增加主界面第二块区域、打开独立窗口。
> - **Chosen**: 打开独立窗口 - **Reason**: 不破坏现有语法，符合“新增窗口”的表述。
> - **Rejected**: 复用主输入框会和现有 `_parse_input` 的数字/动物类型语法冲突。
> - **Impact**: 实施时应新增独立 `_open_expression_window`、`_extract_expression_content` 等路径。

> **Decision**: 保持 `组图 23 表情库.md` 为单一事实源。
> - **Context**: 表情库已有 50 类、每类 8 条的固定结构，且仓库规则强调维护 Markdown 提示词。
> - **Options considered**: 运行时解析 Markdown、复制为 Python 常量、转 JSON。
> - **Chosen**: 运行时解析 Markdown - **Reason**: 减少双份维护。
> - **Rejected**: 复制为常量会让表情库更新时更容易漏同步。
> - **Impact**: 打包 exe 时需要确认 md 文件路径或 datas 配置。

> **Decision**: 模板选择必须可控。
> - **Context**: 用户示例期望“困惑 / 单人”的第 4 条，但表情库同类下有 1-4 四条单人模板。
> - **Options considered**: 随机、固定第一条、固定第四条、允许指定编号。
> - **Chosen**: 允许指定编号，默认策略可配置 - **Reason**: 同时满足稳定验收和抽取工具的多样性。
> - **Rejected**: 纯随机会导致示例不稳定；固定第四条会牺牲所有类别的多样性。
> - **Impact**: 实施时把模板选择封装为独立函数。

#### Ideas Generated
- 独立人物表情抽取窗口，评分 9/10。
- 原文局部回填，评分 9/10。
- Markdown 表情库解析器，评分 8/10。
- 模板编号可控策略，评分 8/10。
- 多组批量增强，评分 7/10。

#### Analysis Results
- 当前工具主类为 `BlindBoxExtractor`，UI 建在 `Game content extraction/内容抽取.py:209` 附近。
- 现有 `_parse_input` 位于 `Game content extraction/内容抽取.py:301`，只适合盲盒逗号语法，不应复用来解析表情字段文本。
- 现有 `extract` 位于 `Game content extraction/内容抽取.py:409`，应保持原行为。
- 表情库规则写明 1-4 为单人、5-8 为多人；“困惑/单人”第 4 条与用户示例完全一致。

#### Challenged Assumptions
- ~~新增功能可以只是随机抽模板。~~ 新理解：用户示例强依赖确定模板，至少需要指定编号或稳定策略。
- ~~只会输入一组表情。~~ 新理解：前置文档默认输出负向和正向两组，解析器应支持多组。
- ~~表情内容应复制到 Python 数据层。~~ 新理解：Markdown 是当前提示词仓库里的单一事实源，优先解析原文件。

#### Open Items
- 默认模板策略应设为“自动按关键词评分”还是“用户指定编号”？
- `[目标物]`、`[证据物]` 等占位符是否保持原样，还是从剧情/适配提示里替换成具体物体？
- 重复点击时，已存在眉 / 眼 / 嘴模板的“具体表情”字段是覆盖、跳过还是提示？

#### Narrative Synthesis
**Starting point**: 本轮从用户示例出发，探索如何把上游表情组文本和表情库模板接成可复制输出。
**Key progress**: 明确了新功能不是新内容生成器，而是“字段文本增强器”；现有窗口和解析逻辑不适合直接复用，独立窗口更稳。
**Decision impact**: 方向收敛到 tkinter Toplevel + Markdown 解析 + 局部回填 + 模板策略控制。
**Current state**: Top ideas 为独立窗口、原文回填、Markdown 解析、模板编号可控、多组批量增强。
**Open directions**: 下一轮可直接进入实施范围定义，或先让用户确认模板选择策略与占位符处理。

---

## Synthesis & Conclusions

### Executive Summary

推荐把新功能做成 **独立人物表情抽取窗口**：用户粘贴 `组图 23 表情前置.md` 生成的表情组文本，工具读取 `组图 23 表情库.md`，用 `极性 + 具体表情 + 单人/多人` 查到对应模板，并只在“具体表情”字段后追加眉 / 眼 / 嘴内容。

### Primary Recommendation

1. 主窗口增加按钮：`人物表情抽取`。
2. 点击后打开 `Toplevel`，包含输入框、模板选择策略、抽取按钮、复制按钮、输出框。
3. 默认保持原文格式，不重排字段。
4. 表情库保持 Markdown 单一事实源，解析出正向/负向、类别、单人/多人、编号模板。
5. MVP 支持指定模板编号；用户示例应以 `困惑 + 单人 + 第4条` 验证。

### Implementation Scope

- `Game content extraction/内容抽取.py`
  - 新增表情窗口入口。
  - 新增字段解析函数，兼容同一行和多行。
  - 新增 Markdown 表情库解析函数。
  - 新增模板选择函数。
  - 新增局部回填函数。
- `Game content extraction/内容抽取.spec`
  - 若运行时读取 `组图 23 表情库.md`，打包时需要把该 md 文件加入 datas 或确认相对路径。

### Acceptance Example

输入识别结果：

- 极性：负向
- 单人/多人：单人
- 具体表情：困惑
- 模板编号：4

应追加：

`眉：一侧眉尾抬起，另一侧眉尾压平；眼：一侧眼撑开看着[目标物]，另一侧眼半垂；嘴：一侧嘴巴闭住下压，另一侧嘴角收紧。`

### Open Decisions

1. 默认模板策略：建议 UI 支持“指定编号”，测试用第 4 条；日常使用可选随机。
2. 占位符处理：建议第一版保留 `[目标物]` / `[证据物]` / `[对方人物]`，不要从剧情里自动替换，避免脑补。
3. 重复回填处理：建议检测到“眉：/眼：/嘴：”已存在时提示或覆盖，不要叠加。

### Session Statistics

- Rounds completed: 1
- Ideas generated: 5
- Top ideas accepted: 5
- Artifacts generated: `exploration-codebase.json`, `perspectives/*.json`, `perspectives.json`, `synthesis.json`

### Terminal Gate

User selected: **Done**

No source-code implementation was started in this brainstorm-only session.
