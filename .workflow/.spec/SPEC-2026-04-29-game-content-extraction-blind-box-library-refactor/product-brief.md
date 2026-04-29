---
session_id: SPEC-2026-04-29-game-content-extraction-blind-box-library-refactor
phase: 2
document_type: product-brief
status: complete
generated_at: 2026-04-29T00:00:00+08:00
stepsCompleted:
  - load-context
  - synthesis
  - generation
version: 1
dependencies:
  - spec-config.json
  - refined-requirements.json
  - discovery-context.json
  - ../../.brainstorm/BS-2026-04-29-优化game-content-extraction盲盒物品内容/handoff-spec.json
  - ../../.brainstorm/BS-2026-04-29-优化game-content-extraction盲盒物品内容/synthesis.json
---

# Product Brief: Game content extraction 盲盒物品内容库重构

本项目重构 `Game content extraction` 的盲盒物品内容库，把旧式主题杂货池收敛为 20 个“常见场景+用途”入口，并用五层物品池定义默认可抽、条件可抽与应隔离风险物。首期目标不是改运行时代码，而是先建立可维护、可验收、可映射回现有四栏 UI 的内容规范，再用三个试点类别验证质量。

## Concepts & Terminology

| Term | Definition | Aliases |
|------|-----------|---------|
| 场景入口 | 面向用户和维护者的盲盒类别名称，采用“场景+用途”命名。 | 类别入口, 主题入口 |
| 五层物品池 | `core_items`、`support_items`、`visible_small_items`、`conditional_items`、`blocked_or_risky` 五种内容层级。 | 五层池 |
| 四栏兼容映射 | 把五层池内容映射回现有 `large`、`medium`、`small`、`hanging` 运行时结构的规则。 | 四栏映射 |
| 可见小物 | 默认可抽的小型物品，必须成组、块状或有明确承载面。 | visible_small_items |
| 条件物 | 依赖承载面、包裹关系或悬挂关系才适合使用的物品。 | conditional_items |
| 风险物 | 默认不进入主抽取池的高风险内容，如灯、镜、透明反光物、细绳、流苏、动物本体、微型痕迹。 | blocked_or_risky |
| 试点类别 | 首批先重写并验证的类别，用于确认规范能产出高质量结果。 | pilot categories |

所有后续规格文档必须优先使用以上术语，避免“主题池”“挂件池”等旧术语继续漂移。

## Vision

让盲盒物品抽取从“勉强有量”转向“默认高可用”，让维护者能稳定写库、让创作者更快选类、让开发者在不破坏现有工具体验的前提下逐步升级内容模型。成功时，用户看到的是更直观的 20 个场景入口，抽到的是更真实、清晰、可圈选、贴近目标图的物品，而不是依赖反光透明、细碎痕迹或容器凑数的低质量项。

## Problem Statement

### Current Situation

当前盲盒库围绕旧主题维护，运行时结构强绑定 `large`、`medium`、`small`、`hanging` 四栏。这个结构便于现有 UI 和输入语法工作，但内容写库长期被“每栏凑满”和“主题太宽泛”驱动，导致容器化条目、小而难圈的小物、缺承载的悬挂物以及依赖透明反光或微小痕迹的条目频繁混入默认输出。与此同时，用户已经形成按编号输入和四栏勾选的使用习惯，不能用一次性大改换来新的内容库。

### Impact

受影响的主要是三类人：

- 内容维护者难以判断某个物品应该写到哪里，复用规则不稳定，后续扩库成本持续升高。
- 工具使用者会抽到不贴图、难圈选或不具备安全放置空间假设的物品，影响提示词生成效率。
- 开发维护者缺少“内容质量”和“结构兼容”的中间层，只能在旧四栏与未来新模型之间硬切。

本次重构以试点标准定义成功阈值：试点类别人工抽样 30 次时，明显不适合项占比低于 10%，且 `blocked_or_risky` 不得进入默认输出。

## Target Users

### 内容维护者

- **Role**: 维护 `blind_boxes.py`、提示词规则与相关中文文档的人。
- **Needs**: 明确的 20 类入口、五层池职责、物品进入或隔离规则、统一验收标准。
- **Pain Points**: 旧主题太宽、旧四栏太粗、容易被“箱/篮/袋/挂件”类凑数条目拖偏。
- **Success Criteria**: 能按统一模板新增或重写类别，不依赖临场判断即可做出大多数归类决策。

### 工具使用者

- **Role**: 用盲盒输出继续写差异提示词、图像内容建议或局部替换建议的人。
- **Needs**: 直观类别名、稳定高质量抽取结果、兼容现有输入方式。
- **Pain Points**: 抽到的小物太碎、挂件没承载、主题不贴图导致结果不好用。
- **Success Criteria**: 只凭类别名就能快速选类，默认输出更接近“能直接写进提示词”的质量。

### 开发维护者

- **Role**: 维护 `内容抽取.py`、数据加载、历史降权和兼容逻辑的人。
- **Needs**: 新模型与旧四栏的清晰边界、编号兼容策略、试点迁移路线。
- **Pain Points**: 旧结构和历史 key 强绑定，缺少能在不中断功能前提下逐步迁移的方案。
- **Success Criteria**: 可以先只改数据和映射，再决定是否升级运行时结构，而不是被迫一次性重写。

## Goals & Success Metrics

| Goal ID | Goal | Success Metric | Target |
|---------|------|----------------|--------|
| G-001 | 用 20 个“场景+用途”入口替代旧式宽泛主题认知 | 已定义并通过审阅的类别数量 | 20/20 |
| G-002 | 建立五层物品池并把默认可抽与风险物分离 | 试点类别五层字段完整率 | 100% |
| G-003 | 在不改现有 UI 的前提下保持运行时兼容 | 现有编号输入与四栏输出样例可解析率 | 100% |
| G-004 | 提升默认抽取内容质量 | 试点抽样中明显不适合项占比 | < 10% |
| G-005 | 建立可维护的写库与审查流程 | 每个试点类别具备结构校验、人工 spot check、文档同步要求 | 3/3 试点完成 |

## Target Model

### 20 个场景入口

| 类别 | 场景提示 |
|------|---------|
| 桌面+学习 | 书桌、文具、学习收纳、书本周边 |
| 餐桌+茶歇 | 餐具、甜点配套、茶歇小物 |
| 厨房+烘焙 | 烘焙工具、厨房操作台、食材承载物 |
| 卧室+梳妆 | 梳妆台、床边收纳、个人整理物 |
| 浴室+洗护 | 洗护用品、台面收纳、毛巾配套 |
| 客厅+装饰 | 客厅陈设、软装点缀、台面装饰 |
| 儿童房+玩具 | 儿童场景、玩具收纳、学习玩乐混合物 |
| 宠物+日常 | 宠物用品、喂养配套、清洁收纳 |
| 庭院+园艺 | 花盆、园艺工具、户外整理物 |
| 门口+雨具 | 门垫、雨伞架、鞋具与出门配套 |
| 沙滩+度假 | 海边用品、防晒承载物、度假小件 |
| 公园+野餐 | 野餐垫、餐盒、便携食物承载物 |
| 营地+露营 | 露营桌面、便携装备、营地收纳 |
| 街道+出行 | 通勤随身物、街边停靠点配套 |
| 运动场+装备 | 球场或健身周边装备、收纳与承载物 |
| 海底+潜水 | 潜水装备、海底可见器物、非动物本体 |
| 节日+礼物 | 节庆包装、礼物承载、陈列装饰 |
| 手作+缝纫 | 缝纫工具、线盒、布面承载物 |
| 手作+编织 | 编织工具、毛线收纳、半成品承载 |
| 商店+零食 | 零食展示、包装集合、台面陈列 |

### 五层物品池

| 池层 | 用途 | 默认要求 |
|------|------|---------|
| `core_items` | 每类最能代表场景的主锚点物 | 一眼可识别、边界清楚、可单独圈选、强场景相关 |
| `support_items` | 配套但仍清晰的主力补充物 | 不抢主锚点，但足够独立、可稳定承载 |
| `visible_small_items` | 默认可抽的小物 | 必须成组、块状或有明确承载面 |
| `conditional_items` | 只有满足承载或关系条件才适用的物品 | 必须注明其依赖的承载面或挂放关系 |
| `blocked_or_risky` | 默认隔离的高风险物 | 不进入默认输出，用于审查和后续人工判断 |

### 与现有四栏的兼容

| 现有四栏 | 主要来源 | 说明 |
|---------|---------|------|
| `large` | `core_items` | 只保留场景锚点物，不再用容器类凑满 |
| `medium` | `support_items` + 部分清晰 `core_items` | 作为默认主力抽取池 |
| `small` | `visible_small_items` | 仅接收高可见、可承载的小物 |
| `hanging` | 少量 `conditional_items` | 明确保留为条件池，不当作默认主池扩容工具 |

### 三个试点类别

- `桌面+学习`: 验证日常高频桌面场景。
- `海底+潜水`: 验证特殊主题与高风险隔离能力。
- `公园+野餐`: 验证户外场景、承载关系和成组小物规则。

## Scope

### In Scope

- 定义 20 个场景入口及命名规范。
- 定义五层物品池职责、进入条件与隔离规则。
- 定义五层池到现有四栏结构的兼容映射原则。
- 重写三个试点类别并形成可验收样板。
- 定义内容质量目标、风险清单、人工 spot check 和文档同步边界。

### Out of Scope

- 一次性重写全部 20 类完整生产数据。
- 改成 Web、数据库、服务端或新大型工程。
- 自动理解目标图并自动选择最合适类别。
- 调整动物抽取、人物表情抽取或其历史语义。
- 发布新应用版本、修改 `APP_VERSION` 或引入自动更新。

### Non-Goals

| Non-Goal | Rationale |
|----------|-----------|
| 立刻替换所有旧编号和旧数据 | 先验证模型有效性，再考虑全量迁移，避免一次性重写带来大面积回归。 |
| 用更多 `hanging` 条目补齐内容量 | `hanging` 天然高风险，应该继续被收缩为条件池，而不是扩容工具。 |
| 让内容库承担运行时逻辑升级 | 本阶段聚焦数据规范与质量门槛，不在规范文档里绑定具体代码改造方案。 |
| 通过微型痕迹、边线、透明反光物提升“丰富度” | 这类内容违背现有提示词禁区，也最容易制造不可用输出。 |

### Assumptions

- 用户接受“20 个常见场景+用途”作为新入口方向。
- 旧编号与现有输入语法短期内必须继续可用。
- 试点质量可以作为是否扩展全量库的决策依据。
- 若 `item_states.py` 与新规则冲突，后续需要单独清洗或约束，而不是放任沿用。

## Competitive Landscape

| Aspect | Current State | Proposed Solution | Advantage |
|--------|--------------|-------------------|-----------|
| 类别认知 | 旧主题宽泛，入口不够直观 | 20 个场景+用途短命名 | 更快选类，减少维护歧义 |
| 内容分层 | 只有四栏，没有显式风险层 | 五层池拆出条件物和风险物 | 默认输出更可控 |
| 小物质量 | 容易混入过细、难圈条目 | `visible_small_items` 强制成组或承载 | 更适合差异提示词 |
| 悬挂物处理 | `hanging` 容易被当成补量池 | 收缩为条件池，只保留少量合规项 | 降低悬挂与软布风险 |
| 迁移策略 | 要么不动，要么全量推翻 | 先三类试点，再扩全量 | 更低风险，更适合现有桌面工具 |

## Constraints & Dependencies

### Technical Constraints

- 运行时仍依赖 `large`、`medium`、`small`、`hanging` 四栏 key。
- `draw_history.json` 的物品池 key 与 box id 和四栏 key 强绑定。
- `data/` 目录只放静态数据，不能把 UI 或抽样逻辑塞进数据层。
- 现有 `item_states.py` 存在与反光、透明限制相冲突的状态词。

### Business Constraints

- 保持中文内容与本地 `tkinter` 工具定位。
- 不引入新的部署形态或复杂基础设施。
- 文档变更必须同步 `AGENTS.md`、`Game content extraction/CLAUDE.md`、`README.md`、`.gitignore`。

### Dependencies

- `Game content extraction/data/blind_boxes.py`
- `Game content extraction/内容抽取.py`
- `Game content extraction/data/item_states.py`
- `Game content extraction/draw_history.json`
- 上游 brainstorming handoff 与 synthesis 结论

## Multi-Perspective Synthesis

### Product Perspective

产品层面最强共识是：入口必须从旧主题转为“常见场景+用途”，因为这是用户最快理解、维护者最容易扩库的命名方式。盲盒库的价值不是“看起来种类多”，而是“默认抽出来就更能用”。

### Technical Perspective

技术层面最关键的边界是不能假装新模型已经替换运行时结构。现有 UI、输入解析、历史 key 和输出逻辑都绑定四栏，因此 Phase 2 的正确姿势是先写清五层模型，再写清四栏映射，而不是在规范里越级承诺代码改造。

### User Perspective

用户层面的诉求非常集中：更直观的类别名、更贴图的结果、更少需要人工二次筛掉的无效条目。对用户来说，五层池是后台逻辑，但它带来的直接感受应该是“默认抽取更稳、更清楚、更好写提示词”。

### Convergent Themes

- 20 个场景入口比旧主题更适合作为长期内容模型。
- 五层池必须把默认主池、条件池和风险池明确分开。
- 兼容现有四栏是短期硬约束，不能绕开。
- 三个试点类别足以覆盖日常、户外和特殊主题，适合作为首轮验证。
- 质量门槛必须写成可检查的规则，而不是笼统原则。

### Conflicting Views

- 冲突点一：是否应立即扩展全部 20 类。
  解决方向：不立即全量扩展，先做三个试点并绑定质量阈值。
- 冲突点二：是否继续沿用现有状态词。
  解决方向：本阶段只把它记为依赖与风险，后续在实现 phase 再决定清洗或隔离。
- 冲突点三：是否需要立刻替换旧编号。
  解决方向：本阶段不替换，优先保留兼容入口，并把迁移说明留给后续设计与实现。

## Open Questions

- [ ] 旧 14 类编号映射到新 20 类时，是保留旧编号入口、增加别名，还是定义迁移表后逐步切换？
- [ ] `item_states.py` 中和透明、反光冲突的状态词，最终是做过滤白名单还是拆成盲盒专用状态集？
- [ ] `draw_history.json` 在未来真正切换到 20 类运行时结构时，是否需要做历史迁移脚本？
- [ ] 三个试点类别的最小条目数和每层推荐配额，是否需要在下一阶段固化为硬性 schema？

## References

- Derived from: [spec-config.json](spec-config.json)
- Derived from: [refined-requirements.json](refined-requirements.json)
- Derived from: [discovery-context.json](discovery-context.json)
- Upstream: [.workflow/.brainstorm/BS-2026-04-29-优化game-content-extraction盲盒物品内容/handoff-spec.json](../../.brainstorm/BS-2026-04-29-优化game-content-extraction盲盒物品内容/handoff-spec.json)
- Upstream: [.workflow/.brainstorm/BS-2026-04-29-优化game-content-extraction盲盒物品内容/synthesis.json](../../.brainstorm/BS-2026-04-29-优化game-content-extraction盲盒物品内容/synthesis.json)
- Next: [Requirements PRD](requirements/_index.md)
