---
session_id: SPEC-2026-04-20-game-content-extraction-人物表情抽取窗口
phase: 2
document_type: product-brief
status: complete
generated_at: 2026-04-20T14:42:00+08:00
stepsCompleted:
  - phase-2-inline-fallback
  - glossary-generated
version: 1
dependencies:
  - spec-config.json
  - refined-requirements.json
  - discovery-context.json
---

# Product Brief: 人物表情抽取窗口

人物表情抽取窗口为现有 Game content extraction 桌面工具增加一条专门处理 `组图 23` 表情链路的能力。用户粘贴表情组文本后，工具从表情库中按极性、具体表情和单人/多人查找模板，并通过原文局部回填生成可直接复制的增强文本。

## Concepts & Terminology

| Term | Definition | Aliases |
|------|------------|---------|
| 人物表情抽取窗口 | 新增独立 tkinter 窗口，用于表情组文本增强 | 表情抽取窗口 |
| 表情组文本 | 包含极性、剧情、单人/多人、具体表情等字段的输入文本 | 前置输出 |
| 具体表情字段 | `具体表情:` 后的字段值，增强后追加眉/眼/嘴模板 | 具体表情 |
| 表情库 | `组图 23 表情库.md`，50 类表情模板资料源 | Markdown 表情库 |
| 模板编号 | 每类表情下的 1-8 编号；1-4 单人，5-8 多人 | 编号模板 |
| 原文局部回填 | 只增强具体表情字段，保留其余文本 | 原文增强 |
| 占位符 | `[目标物]`、`[证据物]`、`[对方人物]` 等后续适配标记 | 回指占位符 |

All documents in this specification MUST use these terms consistently.

## Vision

用户不再需要人工在表情库中查找和复制眉/眼/嘴模板。新增窗口应像现有抽取工具一样简单直接：粘贴、抽取、复制，并且不破坏现有盲盒/动物抽取流程。

## Problem Statement

### Current Situation

`组图 23 表情前置.md` 只输出表情类别名，例如“困惑”。`组图 23.md` 下游需要眉/眼/嘴三段式具体描述。当前用户需要手动打开表情库，按正负向、表情类别、单人/多人定位模板，再复制到具体表情字段后。

### Impact

手动查找容易出现三类错误：选错正负向、选错单人/多人编号、复制时破坏原字段格式。对于批量制作找不同关卡内容的用户，这会增加重复劳动并降低输出稳定性。

## Target Users

### 提示词维护者
- **Role**: 维护 `组图 23` 系列表情和差异点提示词。
- **Needs**: 快速把表情类别转换为可执行眉/眼/嘴模板。
- **Pain Points**: 手动查表情库耗时，容易错配规则。
- **Success Criteria**: 一次粘贴即可得到可复制的增强文本。

### 游戏内容设计者
- **Role**: 为找不同游戏准备人物表情差异内容。
- **Needs**: 稳定复现指定模板，并能批量处理负向和正向两组。
- **Pain Points**: 随机选择会影响验收样例稳定性，重复处理双组文本低效。
- **Success Criteria**: 用户示例中的 `困惑 + 单人 + 第4条` 可稳定输出目标模板。

## Goals & Success Metrics

| Goal ID | Goal | Success Metric | Target |
|---------|------|----------------|--------|
| G-001 | 降低手动查找表情模板成本 | 单组表情增强操作步骤 | 3 步以内：粘贴、抽取、复制 |
| G-002 | 保证模板匹配正确性 | 核心匹配验收用例通过率 | 100% |
| G-003 | 保持现有工具稳定 | 现有盲盒/动物抽取回归结果 | 无行为回归 |
| G-004 | 保持输出可直接用于下游 | 输出文本结构保持率 | 除具体表情字段外不重排字段 |

## Scope

### In Scope

- 主界面新增“人物表情抽取”入口。
- 独立 tkinter Toplevel 窗口。
- 表情组文本输入和增强结果输出。
- 解析极性、单人/多人、具体表情字段。
- 读取和校验 `组图 23 表情库.md`。
- 支持指定模板编号，至少能稳定复现用户示例。
- 对缺字段、未知类别、极性错配、编号越界给出中文错误。

### Out of Scope

- 自动把占位符替换为剧情中的具体物体。
- 修改表情库 Markdown 内容。
- 引入 AI 生成、网络调用或数据库。
- 改造现有盲盒/动物抽取输入语法。
- 把表情抽取写入 draw_history.json 历史降权。

### Non-Goals

| Non-Goal | Rationale |
|----------|-----------|
| Web 化 | 项目定位是简单本地 tkinter 工具 |
| 自动剧情实体抽取 | 容易脑补不可见物，违反提示词链路规则 |
| 重构为大型多模块工程 | 当前功能范围有限，重构成本大于收益 |
| 修改表情库内容 | 本功能是消费表情库，不是维护表情库 |

### Assumptions

- 表情库保持 `### 编号. 表情名` 标题格式。
- 每类表情保持 1-4 单人、5-8 多人。
- 用户接受第一版保留占位符。
- 运行环境可以读取仓库根目录下的 Markdown 文件，或打包时将其纳入 datas。

## Competitive Landscape

| Aspect | Current State | Proposed Solution | Advantage |
|--------|---------------|-------------------|-----------|
| 模板查找 | 人工查 Markdown | 工具按三元条件查找 | 减少错配 |
| 输出格式 | 手工复制修改 | 原文局部回填 | 格式更稳定 |
| 验收复现 | 依赖手工选择 | 支持模板编号 | 示例可稳定验证 |
| 双组处理 | 重复操作 | 一次处理多组 | 更贴合前置输出 |

## Constraints & Dependencies

### Technical Constraints

- Python 标准库优先，不新增外部依赖。
- tkinter UI 风格应与现有工具一致。
- 表情库路径在源码运行和 PyInstaller 打包后都要可控。

### Business Constraints

- 中文输出风格必须保持提示词链路可直接复制。
- 第一版应保守，避免自动改写占位符和剧情内容。

### Dependencies

- `Game content extraction/内容抽取.py`
- `组图 23 表情库.md`
- `组图 23 表情前置.md`
- `Game content extraction/内容抽取.spec`

## Multi-Perspective Synthesis

### Product Perspective

该功能把“查表情库”从手动劳动变成工具内一键增强，最重要的产品价值是稳定、少出错、可复制。

### Technical Perspective

现有单文件 tkinter 架构足够承载该功能。推荐在主类中新增独立窗口方法和纯函数式解析/查找/回填函数，避免触碰现有抽取流程。

### User Perspective

用户的核心路径应该短：打开表情窗口，粘贴前置输出，选择模板编号或策略，抽取，复制结果。错误提示要直接指出缺少哪个字段或错配在哪里。

### Convergent Themes

- 独立窗口优于复用主输入框。
- 表情库应作为单一事实源。
- 模板选择必须支持稳定复现。
- 第一版不自动替换占位符。

### Conflicting Views

随机模板更像“抽取”，但用户示例需要第 4 条稳定输出。解决方案是支持指定编号，并把随机作为可选策略。

## Open Questions

- [ ] 默认模板策略是否设为“指定编号第 4 条”还是“随机”？
- [ ] PyInstaller 打包时是否读取外部 Markdown，还是生成 data 常量？

## References

- Derived from: [spec-config.json](spec-config.json)
- Derived from: [refined-requirements.json](refined-requirements.json)
- Next: [Requirements PRD](requirements/_index.md)
