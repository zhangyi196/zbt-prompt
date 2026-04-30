---
session_id: SPEC-2026-04-30-blind-box-medium-scene-fragments
phase: 2
document_type: product-brief
status: complete
generated_at: 2026-04-30T11:37:25.7949092+08:00
stepsCompleted:
  - load-context
  - local-synthesis
  - glossary-definition
  - generation
version: 1
dependencies:
  - spec-config.json
  - refined-requirements.json
  - discovery-context.json
  - ../../.brainstorm/BS-2026-04-30-scene-expansion-items-small/spec-handoff.md
---

# Product Brief: 盲盒 `scene_expansion_items` 中号场景片段模型

本规格把 `scene_expansion_items` 固定为“中号场景片段”而不是“大件家具/收纳设施”或“小卡片/标签”。目标是在不改动 20 个场景入口、四池契约、运行时映射和 UI 的前提下，重写 20 个场景的 `scene_expansion_items`，并补上可回归的内容质量校验。

## Concepts & Terminology

| Term | Definition | Aliases |
|------|------------|---------|
| 中号场景片段 | 比卡片、标签、单张纸更大，比柜、车、落地架、工作台更小，且能独立成区、第一眼可见的场景扩展主体。 | medium-scale scene fragment |
| `scene_expansion_items` | 四池中的场景扩展池，承载活动结果、任务面、铺垫界面、成组阵列和完整成果等中号主体。 | 场景扩展池 |
| 四池契约 | `core_items`、`support_items`、`visible_small_items`、`scene_expansion_items` 四个固定键，各池保持 50 条唯一内容。 | four-pool schema |
| 升级后的信息载体 | 把价格、标签、编号、记录等信息词升级为板、页组、排版面、记录面等中号主体后的可用形式。 | upgraded information surface |
| 成组可见阵列 | 多个可见对象组成一个边界明确、可整体圈选的阵列或区域。 | grouped visible array |
| 首眼可见主体 | 不依赖灯光、反光、透明、细线或微痕即可被快速识别的对象或区域。 | first-eye visible object |
| 运行时兼容视图 | `BLIND_BOXES` 中保留 `large` / `medium` / `small` / `hanging` 四栏的兼容输出结构。 | runtime compatibility view |

后续规格文档统一使用上表术语，不再混用“场景锚点”“小容器替代品”“小卡片主体”等歧义说法。

## Vision

让 `scene_expansion_items` 成为一个稳定、可维护、可测试的中号场景片段池：维护者看到词条就能判断其所属边界，工具用户抽到词条就能直接把它当作明显、可圈选、可放置的差异对象。成功状态下，20 个场景都能扩展画面感，而不会再通过大件家具、收纳容器或微小信息片来堆数量。

## Problem Statement

### Current Situation

当前 `scene_expansion_items` 在多场景中仍大量使用柜、车、落地架、陈列架、桌、台、架等大件名词；而此前尝试的小替代方向又容易退化成盒、篮、筐、卡片、标签、票据等过小主体。结果是第四池缺少明确语义中心，既容易挤占 `core_items` 的大件空间，又容易滑向 `visible_small_items` 的碎片化写法。

### Impact

- 维护者无法稳定判断第四池应写“什么尺度、什么形态、什么语义”的主体，后续扩写高概率回退到旧问题。
- 工具运行时把 `core_items + scene_expansion_items` 合并进 `large`，过大的第四池词条会直接提高布局压力和选点风险。
- 过小的信息片或单张纸无法承担“场景扩展”的职责，输出给下游提示词时需要二次筛除，降低可用率。
- 如果没有结构化校验，20 个场景全量改写后仍可能出现重复、超大主体、过小主体或跨池语义混淆。

## Target Users

### Prompt maintainer

- **Role**: 维护仓库中文提示词规则和盲盒内容边界的人。
- **Needs**: 稳定的第四池语义、可复用的允许族群、明确的禁用主体边界。
- **Pain Points**: 大件词条造成布局负担，小容器和小卡片又会混入其他池的职责。
- **Success Criteria**: 能用少量规则持续维护 20 个场景，不需要反复口头解释尺度边界。

### Game content extraction tool maintainer

- **Role**: 维护 `blind_boxes.py`、兼容映射、单元测试和文档的人。
- **Needs**: 数据改写不破坏运行时契约，新增质量校验能覆盖主要回归风险。
- **Pain Points**: 一次内容修正容易牵动 UI、历史数据或兼容层，人工审查 20 个场景成本高。
- **Success Criteria**: 保持四池键名、50 条唯一项和兼容映射不变，并用测试锁定新规则。

### Downstream prompt user

- **Role**: 使用盲盒输出继续写差异提示词的人。
- **Needs**: 第一眼可见、边界清楚、可单独圈选的中号主体。
- **Pain Points**: 大件主体难以落位，过小主体不够显眼，信息碎片难以单独成点。
- **Success Criteria**: 抽到的 `scene_expansion_items` 可以直接作为可见差异对象，不需要二次剔除明显不合格项。

## Goals & Success Metrics

| Goal ID | Goal | Success Metric | Target |
|---------|------|----------------|--------|
| G-001 | 固定第四池的语义边界 | 规格中明确 5 类允许族群、3 类主要禁用边界 | 1 份统一定义，后续文档复用 |
| G-002 | 完成 20 个场景的第四池重写目标 | 每个场景 `scene_expansion_items` 数量与唯一性校验通过 | 20/20 场景、每池 50 条唯一项 |
| G-003 | 阻止大件或过小主体回流 | 质量校验能识别大件家具/收纳词和小卡片/标签/票据类独立主体 | 关键风险词误入率 0 |
| G-004 | 保持运行时兼容 | `BLIND_BOXES` 与 `BLIND_BOX_COMPATIBILITY_MAPPING` 相关测试通过 | 现有兼容契约 100% 保持 |
| G-005 | 让维护规则可长期复用 | `Game content extraction/agents.md` 中有精简稳定的第四池规则 | 1 处稳定规则源，无长列表重复 |

## Scope

### In Scope

- 为 `scene_expansion_items` 定义“中号场景片段”内容模型与允许族群。
- 重写 20 个场景的 `scene_expansion_items`，保留四池键名和每池 50 条唯一项。
- 增加或扩展内容质量校验，覆盖超大主体、过小主体和跨池语义混淆。
- 在实现被接受的前提下，同步精简的维护文档规则。

### Out of Scope

- 新增第五池或改变 `BLIND_BOX_SCENE_ENTRIES` 的 20 个入口和编号。
- 改动 `tkinter` UI、抽取历史、动物池、表情池、图像抓取或批量重命名逻辑。
- 改动 `BLIND_BOX_COMPATIBILITY_MAPPING` 的四栏结构或历史 key。
- 把第四池重写成“容器池”“卡片池”或任何新的运行时专用语义层。

### Non-Goals

| Non-Goal | Rationale |
|----------|-----------|
| 用箱、篮、筐等小容器替代大件家具 | 这类对象仍会和 `core_items` / `support_items` 的收纳或承载物混淆，不能作为第四池主骨架。 |
| 用卡片、标签、票据、编号牌等微小信息片凑满第四池 | 这类对象更接近 `visible_small_items` 或细碎差异点，无法承担场景扩展职责。 |
| 通过运行时过滤掩盖静态内容问题 | 本次目标是把语义边界写进数据和测试，而不是靠临时过滤容错。 |
| 追求所有场景统一模板化名词 | 第四池需要统一边界，不需要牺牲每个场景的专属活动语义。 |

### Assumptions

- 用户已经接受“中号场景片段”作为本轮规格方向，不再回到大件或小容器路线。
- 运行时兼容层无需改变，只要四池数据和映射约束保持不变即可承接新语义。
- 升级后的信息载体可以作为少量合法例外，但不能重新变成第四池主流写法。

## Competitive Landscape

| Aspect | Current State | Proposed Solution | Advantage |
|--------|---------------|-------------------|-----------|
| 第四池语义 | 大件家具、收纳设施和小信息片并存，边界漂移严重 | 固定为中号场景片段，围绕五类允许族群写作 | 维护判断更快，后续扩写不易跑偏 |
| 尺度控制 | 依赖人工感觉，没有统一的上下边界 | 同时禁止“大件主语”和“微小主语”，保留中号主体带 | 兼顾可见性和可放置性 |
| 信息类内容使用方式 | 价格、标签、记录等词容易直接作为主体 | 只允许升级为板、页组、排版面、记录面等载体后进入第四池 | 保留场景语义，同时避免过小主体 |
| 兼容风险 | 内容修正容易被误解为要改 UI 或映射 | 只改数据、测试和精简规则文档 | 变更面小，回归成本低 |
| 质量保证 | 人工检查为主，难以覆盖 20 个场景 | 用测试锁定数量、唯一性和高风险词边界 | 可持续回归，减少人工反复审阅 |

## Constraints & Dependencies

### Technical Constraints

- 必须保留 `BLIND_BOX_ITEM_POOL_BUNDLES` 作为权威四池数据源。
- `BLIND_BOXES` 仍然通过 `core_items + scene_expansion_items` 提供 `large` 兼容视图。
- 每个场景四池都必须维持 50 条唯一字符串。
- 不得依赖灯光、反光、透明、发光、细线或微痕来定义第四池主体。

### Business Constraints

- 仓库规则文件必须保持精简，只保留稳定规则和必要入口。
- 本次规格是数据内容模型规格，不是服务、API 或 UI 改版提案。
- 用户侧行为不应因第四池改写而出现新的输入语法或操作路径要求。

### Dependencies

- [spec-config.json](spec-config.json)
- [refined-requirements.json](refined-requirements.json)
- [discovery-context.json](discovery-context.json)
- [Spec Handoff](../../.brainstorm/BS-2026-04-30-scene-expansion-items-small/spec-handoff.md)
- [Game content extraction/agents.md](<../../../Game content extraction/agents.md>)

## Multi-Perspective Synthesis

### Product Perspective

从产品价值看，第四池的核心不是“再提供一组可抽的名词”，而是让盲盒结果多一层稳定的场景扩展能力。用户接受的方向已经很明确：第四池必须比小碎片更显眼、比大件家具更易放置，并且能用少量规则长期维护。五类允许族群因此成为范围定义的中心，而不是实现细节。

### Technical Perspective

从技术可行性看，这是一项中等复杂度的数据与测试改写任务，而不是架构重构。现有代码已经把 `BLIND_BOX_ITEM_POOL_BUNDLES` 作为事实源，并通过 `BLIND_BOX_COMPATIBILITY_MAPPING` 维护兼容层；因此最佳路径是只修改第四池数据、扩展测试和同步精简文档，不改 UI、运行时逻辑或历史键结构。

### User Perspective

从维护和下游使用体验看，最重要的是“拿到词条后不用再解释它是不是太大或太小”。维护者需要可快速扫描的规则，下游用户需要第一眼可见、可单独圈选的对象或区域。因此第四池更适合以任务面、成果面、阵列区、半成品区这类可见结构来承载场景信息，而不是单个小标签或占地很大的家具。

### Convergent Themes

- 第四池必须围绕“中号场景片段”而不是“容器替代品”或“信息碎片替代品”。
- 规则必须同时定义允许族群和禁用边界，单独强调其中一端都会导致回退。
- 最稳妥的实现方式是数据改写 + 测试加固 + 精简文档同步，不扩大到 UI 或运行时重构。
- 信息类词汇只有在升级为中号载体后才适合进入第四池。

### Conflicting Views

- **冲突 1**: 第四池需要明显扩展场景，但又不能重新回到大件家具。  
  解决方向：用活动结果、任务面、成组阵列、半成品区等“可见但不过分占地”的中号主体替代柜、车、台、架。
- **冲突 2**: 第四池需要比 `visible_small_items` 更大，但又不能把所有信息词都排除掉。  
  解决方向：允许“升级后的信息载体”，例如记录板、排版板、展开页组，而不是单张卡片、标签或票据。
- **冲突 3**: 20 个场景需要统一边界，但每个场景又需要保留自身语义。  
  解决方向：统一主体尺度和族群规则，保留场景专属词根与活动结果表达。

## Open Questions

- [ ] 内容质量校验是采用显式黑名单、词根规则，还是“黑名单 + 少量白名单例外”的组合更稳妥？
- [ ] 是否需要为 20 个场景各自保留 8-12 个推荐词根，作为后续维护参考而不直接写入稳定规则文档？
- [ ] 升级后的信息载体是否需要统一后缀规范，例如优先使用“板 / 页组 / 记录面 / 排列组”以降低维护分歧？

## References

- Derived from: [spec-config.json](spec-config.json)
- Derived from: [refined-requirements.json](refined-requirements.json)
- Derived from: [discovery-context.json](discovery-context.json)
- Derived from: [Spec Handoff](../../.brainstorm/BS-2026-04-30-scene-expansion-items-small/spec-handoff.md)
- Next: [Requirements PRD](requirements/_index.md)
