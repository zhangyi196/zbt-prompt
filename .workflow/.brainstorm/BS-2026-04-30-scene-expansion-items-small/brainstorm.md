# Brainstorm Session

**Session ID**: BS-2026-04-30-scene-expansion-items-small
**Topic**: `scene_expansion_items` 小型化替代方向
**Started**: 2026-04-30T00:00:00+08:00
**Dimensions**: innovation, feasibility, content-system
**Mode**: Creative-first

## Table of Contents

- [Session Context](#session-context)
- [Current Ideas](#current-ideas)
- [Thought Evolution Timeline](#thought-evolution-timeline)
- [Synthesis & Conclusions](#synthesis--conclusions)
- [Decision Trail](#decision-trail)

## Current Ideas

1. **场景片段物**: 不再把大件缩成盒/篮，而是用能直接讲出当前活动的可见片段，例如“待批改作业叠”“半完成拼图板”“包装到一半的礼物组”。
2. **中号任务面**: 用正在发生的动作结果表达场景扩展，但必须是板面、垫面、展开页、成组阵列这一类中号对象，例如“写满备注的复习板”“排好的训练标志盘阵列”“防水记录板”。
3. **铺垫界面物**: 用垫、板、布、展开页这类平面中件替代家具，例如“烘焙操作垫”“野餐餐布角”“沙滩毛巾垫”“门口擦鞋垫”。
4. **场景标识降级为附属特征**: 不再把菜单牌、价格签、小标签、小卡片当主物；若使用，必须附着在较大的板、垫、组、盘、展示面上。
5. **完整成果物**: 用已完成或半完成的成果替代收纳设施，例如“小蛋糕装饰盘”“织到一半的围巾片”“修剪好的花枝束”。

## Session Context

- User focus: 只要创意
- Perspectives: creative, pragmatic, systematic
- Constraints:
  - 技能边界：只做头脑风暴文档，不修改源文件。
  - 仓库约束：`scene_expansion_items` 是四池模型之一，当前运行时映射进 `large`。
  - 数据验收：物品要第一眼可识别、边界清楚、可单独圈选；不得依赖光影、透明、反光、发光、细线或微型痕迹。
  - 新增约束：不得以小卡片、小标签、单枚价格签、单个编号牌等过小物作为 `scene_expansion_items` 主体。

## Exploration Vectors

1. `scene_expansion_items` 真正要承担的是“扩展场景感”，还是“增加大型物品”？
2. 哪些小型物仍能稳定表达用途，不会退化成太细碎的差异点？
3. 如何避免把 `scene_expansion_items` 和 `visible_small_items` 做成同一池？
4. 是否需要一套跨 20 场景通用的后缀替换规则？
5. 哪些大件后缀应被降权或禁止：柜、车、落地架、桌、工作台、棚？
6. 生成新库时，应该优先改“物品形态”，还是优先改“命名语义”？

## Initial Decisions

> **Decision**: 本轮采用“创意优先”的头脑风暴。
> - **Context**: 用户明确表示目前觉得大件太大，但还没确定替代物。
> - **Options considered**: 平衡替代、只要创意、规则优先。
> - **Chosen**: 只要创意。**Reason**: 先打开替代物空间，后续再收敛为库改写规则。
> - **Rejected**: 直接实现替换。当前用户还处于概念探索期。
> - **Impact**: 输出偏候选方向和命名体系，不生成完整 1000 条替换数据。

---

## Thought Evolution Timeline

### Round 1 - Codebase Exploration

#### User Input

用户认为当前盲盒物品中 `scene_expansion_items` 里类似推车、抽屉柜、陈列架等内容太大，希望更小一些，但尚未确定具体替代物。

#### Analysis Results

- `Game content extraction/data/blind_boxes.py` 中 `_build_legacy_blind_box_entry` 将 `core_items + scene_expansion_items` 合并为运行时 `large`。
- `Game content extraction/test_blind_box_content_model.py` 固定四池每池 50 条、四池 key 不变、运行时 `large_sources` 为 `["core_items", "scene_expansion_items"]`。
- `Game content extraction/agents.md` 要求场景扩展物“必须中等以上且无需画面已有对象成立”，但现有数据把“中等以上”大量实现为柜、车、落地架、桌、箱。
- 粗略统计显示，每个场景约 29-35 条 `scene_expansion_items` 命中柜/车/桌/凳/棚/作业台/工作台/货架/书架等大件倾向词。

#### Ideas Generated

1. **台面替代，不做家具替代**: 所有替代物默认可放在桌面、地面小区域、垫子、台阶、箱面上。
2. **把“扩展”理解为场景证据**: 不再通过大家具扩展空间，而通过用途证据扩展叙事。
3. **每个场景保留少量中型锚点**: 例如提篮、整理箱、托盘、收纳盒；删除大多数车、柜、落地架。

#### Challenged Assumptions

- ~~场景扩展物必须是更大的家具或承载设施。~~
  - 新理解：它只要能在视觉上明确“这是某个场景的配套物”，不必占据新空间。
- ~~小型化会和 `visible_small_items` 重合。~~
  - 新理解：`visible_small_items` 偏散落/数量组，新的 `scene_expansion_items` 可以偏“块状承载物、成套用品、标签化场景证据”。

#### Narrative Synthesis

**Starting point**: 用户指出大件过多，本轮先确认问题是否来自数据结构或内容命名。  
**Key progress**: 发现 `scene_expansion_items` 当前进入运行时大型物品栏，因此大件命名会直接增加放置压力。  
**Decision impact**: 方向从“找更小家具”转为“找更小的场景锚点”。  
**Current state**: 最有价值的候选是托盘/盒/夹/卡座/套组/垫板/提篮这一类。  
**Open directions**: 需要决定是全量替换，还是先做 20 场景的后缀规则与样例库。

### Round 2 - Creative Exploration

#### Ideas Generated

1. **标签与票据系统**: 价格签、课程卡、补货卡、祝福卡、图样卡、训练编号牌、植物标签、潜水记录牌。
2. **托盘与垫板系统**: 茶点托盘、操作垫、分类垫、折叠垫、工具垫、试吃盘、杯垫套、门口接物盘。
3. **小盒与匣罐系统**: 配料盒、样本盒、工具匣、标签盒、针线盒、票卡盒、湿巾盒、封口夹盒。
4. **束带与套袋系统**: 雨伞束带、毛巾束带、餐具束带、露营防风夹套、潜水安全绳扣组、手作布样束。
5. **局部承载系统**: 卡座、托座、立夹、隔片、分隔格、压块、夹板、展示小座。
6. **口袋补给系统**: 出行补给包、沙滩防晒包、运动补给包、宠物护理包、露营洗漱包、园艺修枝包。

#### Analysis Results

- 小型化的核心不是“越小越好”，而是“可见、块状、能单独圈选”。
- 命名上应少用“柜/车/落地/多层/大型/工作台”，多用“盒/盘/座/夹/牌/包/篮/垫/束/套/匣/罐”。
- `scene_expansion_items` 可以比 `support_items` 更有场景叙事性，例如“露营锅盖托架盒”比“锅盖托架”更像扩展项。

#### Narrative Synthesis

**Starting point**: 本轮按用户选择的创意模式，大量发散小型物类别。  
**Key progress**: 形成 6 个跨场景物品族群，能覆盖 20 个场景。  
**Decision impact**: 后续收敛时可以先定“物品族群配额”，再为每个场景填 50 条。  
**Current state**: 最稳的是“盒/托盘/卡座/套组/补给包”五族。  
**Open directions**: 需要判断哪些族群适合放入 `scene_expansion_items`，哪些应留给 `support_items` 或 `visible_small_items`。

### Round 3 - User Challenge

#### User Input

用户指出：当前替换方向里的盒、提篮等内容，和其他几种物品池的区别仍然分不开。

#### Decision Log

> **Decision**: 降低“容器类替代物”的优先级，改用“场景片段/任务状态/铺垫界面/标识物/成果物”作为新的主方向。
> - **Context**: 盒、提篮、篮、托盘容易和 `core_items`、`support_items` 中已有的收纳盒、整理篮、托座重叠。
> - **Options considered**: 继续用小容器、为容器加更长限定词、转向非容器化场景扩展。
> - **Chosen**: 转向非容器化场景扩展。**Reason**: 更能保留 `scene_expansion_items` 的独立语义。
> - **Rejected**: 单纯把“柜”缩成“盒”。这只是尺寸变小，池间边界没有变清楚。
> - **Impact**: 后续实现应少写“收纳盒/整理篮/提篮”，多写“活动结果、状态证据、场景标识、铺垫界面”。

#### Ideas Updated

1. **活动结果物**: 作业叠、半成品、成品盘、包装组、修剪花枝、拼好一角的拼图板。
2. **状态证据物**: 写过的记录板、排好的训练标志盘、贴好标签的分类牌、待补货价格签。
3. **平面场景界面**: 操作垫、餐布角、桌旗、门垫、沙滩毛巾垫、露营防潮垫。
4. **独立标识物**: 菜单牌、课程表、计分牌、祝福牌、植物铭牌、潜水方向牌。

#### Challenged Assumptions

- ~~只要比柜/车小，就能成为好替代。~~
  - 新理解：还必须和其他池拉开语义边界，不能只是变小的收纳物。
- ~~盒、篮、提篮是最安全的小型化方向。~~
  - 新理解：它们安全但太普通，适合作为少量补充，不适合作为主干。

#### Narrative Synthesis

**Starting point**: 用户挑战了“盒/提篮”方向的池间辨识度。  
**Key progress**: 新方向从“容器小型化”转为“非容器化场景扩展”。  
**Decision impact**: `scene_expansion_items` 的定义应强调“改变场景叙事的完整片段”，而不是“放东西的小容器”。  
**Current state**: 最推荐的是场景片段物、任务状态物、铺垫界面物、独立标识物、完整成果物。  
**Open directions**: 下一步若执行，建议先用 3 个 pilot 场景验证这些新族群是否足够清晰。

### Round 4 - Scale Correction

#### User Input

用户指出：上次写的 brainstorm 仍有优化空间，期望不能有太小的内容，例如小卡片内容。

#### Decision Log

> **Decision**: 将 `scene_expansion_items` 的目标尺寸从“非容器化小物”修正为“中号场景片段”。
> - **Context**: 上一版虽然避开了柜、车、盒、提篮，但引入了课程卡、价格签、标签牌、小卡片等过小对象。
> - **Options considered**: 保留小卡片但要求成组、全部删除标识类、把标识类升级为中号板面或附属特征。
> - **Chosen**: 把标识类升级为中号板面或附属特征。**Reason**: 能保留“场景信息”的优点，同时避免差异主体过小。
> - **Rejected**: 单独使用小卡片/小标签。它们更适合 `visible_small_items` 或作为其他主体上的局部细节。
> - **Impact**: 后续实现时应优先写“板、垫、布、展开页、成组阵列、半成品区域、成果盘”，谨慎使用“卡、签、牌、标签”。

#### Ideas Updated

1. **中号场景片段**: 尺度介于桌面小物和家具之间，推荐文件夹、A4 板、餐垫、毛巾垫、拼图板、训练盘阵列、展开包装纸这类主体。
2. **小标识不独立成点**: 课程卡、价格签、标签牌、编号牌只能作为“贴在板面/垫面/成组物上的可见细节”，不能作为主物。
3. **场景状态用面积表达**: 用“摊开的一页/铺开的一角/排好的一组/做到一半的一块/完成的一盘”表达，而不是一枚小牌。
4. **命名过滤规则**: 强降权或禁止单独出现“小卡、卡片、标签、签、编号牌、小票、书签、铭牌、名牌”等词，除非前面有“板、组、阵列、垫、页、盘、布、底板”等中号主体。

#### Challenged Assumptions

- ~~非容器化就足够安全。~~
  - 新理解：非容器化还可能过小，必须增加“中号尺度”约束。
- ~~场景标识物能独立扩展场景。~~
  - 新理解：独立小标识太弱，应该并入较大的场景面或成组状态。

#### Narrative Synthesis

**Starting point**: 用户进一步指出小卡片类内容不符合预期。  
**Key progress**: 形成“中号场景片段”标准：比卡片大、比家具小，最好是板面、垫面、展开面、成组阵列或半成品区域。  
**Decision impact**: 上一轮的“独立标识物”不再作为主族群，而改为附属特征。  
**Current state**: 最推荐的是活动结果物、中号任务面、铺垫界面物、成组阵列、完整成果物。  
**Open directions**: 若进入实现，应先重写 pilot 场景样例，检查是否还有“卡/签/标签”独立主体。

---

## Synthesis & Conclusions

### Executive Summary

当前问题不是单个词条偏大，而是整池生成策略把“场景扩展”写成了“新增家具/收纳设备”。第一轮提出的盒、提篮、托盘方向虽然能缩小尺寸，但用户指出它们和其他池边界不清；第二轮转向非容器化后，又出现了小卡片、小标签、价格签等过小主体。最终建议把 `scene_expansion_items` 改为“中号场景片段池”：比卡片大、比家具小，通过活动结果、板面/垫面、展开面、成组阵列、完整成果来改变场景叙事。

### Primary Recommendation

采用 **“中号场景片段”** 作为新方向：

- 保留四池结构不变。
- `scene_expansion_items` 不再主打柜/车/落地架。
- 每个场景 50 条里，建议最多 5-8 条保留容器或承载物，其余改为活动结果物、中号任务面、铺垫界面物、成组阵列、完整成果物。
- 禁止以单张小卡、小标签、单枚价格签、单个编号牌作为主物；这类信息只能附着在更大的板、垫、页、盘、布、阵列或成果物上。
- 命名要回答“这里正在发生什么/属于什么场景”，而不只是“这里多了一个收纳物”。

### Top Idea Families

1. **活动结果物**: 待批改作业叠、小蛋糕装饰盘、半完成拼图板、修剪花枝束、包装到一半的礼物组。
2. **中号任务面**: 写满备注的复习板、防水记录板、护肤步骤板、训练动作提示板、烘焙步骤板。
3. **铺垫界面物**: 烘焙操作垫、野餐餐布角、沙滩毛巾垫、门口擦鞋垫、露营防潮垫。
4. **成组阵列物**: 排好的训练标志盘、摆好的杯垫阵列、分好的餐具束、排列好的玩沙工具组、补给瓶组。
5. **完整成果物**: 织到一半的围巾片、装饰好的礼物盒、调好的配料小碟、整理好的潜水采样瓶组。

### Parked Ideas

- 直接把 `scene_expansion_items` 映射到 `medium`：结构影响较大，先不作为本轮推荐。
- 新增第五池如 `scene_anchor_items`：概念清晰但会扩大测试和 UI 兼容面，后续若四池语义不够再考虑。

## Decision Trail

> **Decision**: 用“中号场景片段”替代“空间扩展家具”作为核心概念。
> - **Context**: 大件过多会触发放置空间不足，与提示词规则里的承载空间约束冲突。
> - **Options considered**: 缩小所有家具名、改映射、增加新池、重写为小型场景锚点、重写为非容器化场景片段、重写为中号场景片段。
> - **Chosen**: 重写为中号场景片段。**Reason**: 不动结构，也能同时避开大件、容器混淆和小卡片过小的问题。
> - **Rejected**: 只把“柜”改“盒”；单独使用小卡片/小标签。前者池间边界不清，后者视觉主体过小。
> - **Impact**: 后续实现应是全池命名策略调整，而不是零散替换几个词。

## Session Statistics

- Rounds completed: 4
- Perspectives used: creative, pragmatic, systematic
- Code files inspected: 3
- Recent workflow sessions checked: 3
- Source files modified: 0
