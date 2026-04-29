# Brainstorm: 重新定义 `conditional_items` 与 `blocked_or_risky`

## Session Metadata

- Session ID: `BS-2026-04-29-重新定义conditional-items-blocked-or-risky`
- Date: 2026-04-29
- Topic: 盲盒物品库中 `conditional_items` 和 `blocked_or_risky` 仍然产出质量不稳定，是否需要重新定义
- User feedback:
  - `conditional_items` 示例“显示器下方收纳架”如果画面没有显示器，就无法成立。
  - `blocked_or_risky` 示例“细绳挂饰”仍然太小，对游戏不适合。
  - 当前内容质量不够好，可能需要重新定义两个类别，而不是继续微调条目。

## Seed Understanding

上一轮修正解决了“非物品表达进入池层”的问题，但没有解决两个更深层问题：

1. `conditional_items` 仍然把“需要画面前置条件”的对象放进普通字符串池。只要抽取时没有显式检查前置物，就会输出与画面不匹配的物品。
2. `blocked_or_risky` 仍然混合了两类东西：真正要禁用的内容，以及“具体但质量不好/太小/太细/不适合游戏”的内容。它的名称像风险池，但实际承担了“负样本、禁用规则、低质量候选、场景排除”的多重责任。

## Current Failure Examples

### `conditional_items`

- `显示器下方收纳架`：需要画面已有显示器或明显桌面电子设备，否则不成立。
- `白板磁吸收纳盒`：需要画面已有白板或磁吸承载面。
- `桌侧耳机支架`：需要桌侧可见且有可安装空间。
- `遮阳伞底座`：需要画面有遮阳伞或伞杆语境，否则只是突兀大物。

这些条目不是“不具体”，而是“依赖条件未结构化”。问题在定义，不只在内容。

### `blocked_or_risky`

- `细绳挂饰`：虽然是具体物品，但太细、太小、边界不稳，不适合游戏抽取。
- `流苏书签`、`细绳渔网`、`细绳挂旗`：有对象名，但视觉主体依赖细线/流苏/重复网格，圈选和识别不稳。
- `透明胶带卷`、`透明食品罩`：具体但透明，可能不是“永远禁用”，更像视觉风险标签。

这些条目说明 `blocked_or_risky` 不应该只是“具体风险物清单”，而应该拆成更明确的质量门禁。

## Exploration Vectors

1. 是否保留 `conditional_items` 这个池？
2. 如果保留，它是“默认可抽池”还是“仅在条件命中后启用的结构化池”？
3. `blocked_or_risky` 是不是应该从“物品池”变成“禁用规则 / 风险标签 / 审查规则”？
4. 当前四栏兼容映射是否应该继续把 `conditional_items` 映射到 `hanging`？
5. 对游戏可用性而言，最重要的质量门槛是：具体、常见、边界清楚、体量足够、无需未验证前置物、可独立圈选。

## Round 1: Multi-Perspective Analysis

### Creative Perspective

把五层池从“物品大小分类”改成“抽取策略分类”会更稳定：

- `core_items`：无条件默认可抽。
- `support_items`：无条件可抽，但更依赖场景。
- `visible_small_items`：只有成组、块状、有承载的小物。
- `conditional_items`：不再是字符串池，而是“带条件的候选组”，每个条目必须声明 `required_anchor`。
- `blocked_or_risky`：不再提供候选物，只作为禁用规则和风险标签。

新想法：把 `conditional_items` 改名为 `anchor_required_items`，让名称直接表达“必须有锚点”。例如：

```json
{
  "name": "显示器下方收纳架",
  "required_anchor": ["显示器", "电脑屏幕", "桌面电子设备"],
  "min_visible_area": "medium",
  "fallback": "skip"
}
```

如果当前工具没有图像识别锚点能力，就不进入默认输出。

### Pragmatic Perspective

短期最稳妥的做法不是立刻引入复杂结构，而是先改变语义和映射：

- `conditional_items` 不再映射到默认 `hanging`。
- `hanging` 仍用旧的安全悬挂物或从 `support_items` 中筛选边界清楚的中型物补齐。
- 三个试点的 `conditional_items` 暂时只作为“人工未来扩展池”，不参与随机抽取。
- `blocked_or_risky` 中删除所有太细、太小、透明、反光、动物本体等候选输出，只保留为审查说明；或者保留字段但永远 excluded。

这样不需要改 UI，也不需要改输入语法，但能马上降低输出失败率。

### Systematic Perspective

当前问题来自字段职责混淆：

| 字段 | 当前职责 | 问题 | 建议职责 |
|---|---|---|---|
| `conditional_items` | 默认映射到 `hanging` 的条件物 | 没有条件检测，导致前置物缺失 | 仅存放带锚点要求的候选，不默认输出 |
| `blocked_or_risky` | 风险物池 / 禁用物池 | 容易混入“具体但低质量”的候选 | 改为风险规则或 excluded metadata |
| `visible_small_items` | 可见小物 | 仍需防微型化 | 只允许成组、块状、有承载 |
| `support_items` | 配套物 | 可作为默认池补位 | 可承担部分中型/悬挂输出 |

系统性定义应从“类别是什么”变成“什么时候能输出”：

- 默认输出池：无需验证额外前置物。
- 条件输出池：必须验证锚点。
- 禁止输出规则：永不作为候选。

## Key Decision Candidate

建议重新定义两个类别：

1. `conditional_items` 改为 **锚点条件池**：
   - 不是默认抽取池。
   - 每个条目必须能回答“需要画面中已有哪个锚点？”
   - 如果无法自动判断锚点，就默认不输出。
   - 条目体量必须中等以上，禁止细绳、标签、边线、小夹子、小贴片。

2. `blocked_or_risky` 改为 **禁用规则 / 风险标签池**：
   - 不再当作物品内容库。
   - 主要维护风险原因：透明、反光、发光、动物本体、细长线状、微型、阴影痕迹、依赖光效。
   - 如果仍保留具体示例，也只作为测试/审查负例，不作为候选。

## Narrative Synthesis

**Starting point**: 用户指出“显示器下方收纳架”依赖显示器，“细绳挂饰”仍然太小。  
**Key progress**: 问题从“具体物品 vs 非物品”推进到“是否需要未验证前置物”和“是否满足游戏可圈选体量”。  
**Decision impact**: 继续换词无法根治，字段定义和默认映射都需要调整。  
**Current state**: 最推荐方案是 `conditional_items` 结构化为锚点条件池，并从默认输出中移除；`blocked_or_risky` 退化为禁用规则/风险标签，不再是可候选物品池。  
**Open directions**: 需要决定短期是保守禁用这两个池，还是引入结构化 item schema 支持条件判断。

## User Input: Direction Selection

用户选择：`结构化重构`。

> **Decision**: 进入结构化重构方向，而不是继续修补字符串池。
> - **Context**: 用户明确指出“显示器下方收纳架”这类条目必须依赖画面已有显示器，而当前数据无法表达和验证这个条件；同时“细绳挂饰”虽是具体物品但仍然太小，不适合游戏。
> - **Options considered**: 保守修正、结构化重构、继续讨论。
> - **Chosen**: 结构化重构 — **Reason**: 只有结构化字段才能表达 `required_anchor`、`default_enabled`、`risk_tags`、`min_size` 等质量门槛。
> - **Rejected**: 继续字符串替换，因为它会把“条件是否成立”的判断藏在物品名里，后续仍会反复产生不匹配内容。
> - **Impact**: 下一步应生成规格，目标是数据模型和兼容映射重构，而不是单纯内容替换。

## Round 2: Structured Refactor Concept

### Proposed Data Model

将 `BLIND_BOX_ITEM_POOL_BUNDLES` 从五层 `list[str]` 扩展为安全兼容的结构化候选模型：

```python
{
    "name": "显示器下方收纳架",
    "pool": "anchor_required_items",
    "default_enabled": False,
    "required_anchor": ["显示器", "电脑屏幕"],
    "min_size": "medium",
    "visibility": "independent_circleable",
    "risk_tags": [],
}
```

风险/禁用项不再作为可抽物品：

```python
{
    "pattern": "细绳",
    "risk_reason": "细长线状主体，边界不稳定，游戏可圈选性差",
    "severity": "blocked",
    "applies_to": ["all_pools"],
}
```

### New Field Semantics

- `core_items`：默认启用，无额外锚点要求，体量和边界最稳。
- `support_items`：默认启用，场景强相关，但不依赖未验证前置物。
- `visible_small_items`：默认启用，但必须成组、块状或有明确承载。
- `anchor_required_items`：替代 `conditional_items`；默认不启用，只有锚点命中才进入候选。
- `blocked_rules`：替代 `blocked_or_risky`；不是物品池，只用于校验和过滤。

### Compatibility Strategy

短期保留旧四栏输出：

- `large` 从 `core_items` 生成。
- `medium` 从 `support_items + core_items:first_6` 生成。
- `small` 从 `visible_small_items` 生成。
- `hanging` 不再直接等于 `conditional_items`；改为从明确安全的 `support_items` 或新建 `safe_hanging_items` 生成。
- `anchor_required_items` 只有当未来输入/识别能证明 `required_anchor` 存在时才参与输出。
- `blocked_rules` 永远不进入 `BLIND_BOXES`。

### Required Tests

- 结构化 schema 校验：每个候选必须有 `name`、`pool`、`default_enabled`、`min_size`。
- 锚点池校验：`anchor_required_items` 必须有非空 `required_anchor` 且 `default_enabled=False`。
- 风险规则校验：`blocked_rules` 不得进入默认输出；风险关键词如 `细绳`、`流苏`、`透明`、`反光`、`发光`、`动物本体` 必须以规则形式存在。
- 兼容映射校验：旧 `BLIND_BOXES` 四栏仍然存在，且不包含 `anchor_required_items` / `blocked_rules`。
- 内容质量校验：默认输出禁止 `显示器下方`、`白板磁吸` 等隐含锚点短语，除非已结构化声明并默认禁用。

### Converged Recommendation

生成下一轮 spec 时，任务名建议为：

`Game content extraction 盲盒物品池结构化重构：锚点条件池与风险规则`

目标不是继续“修列表”，而是让数据模型明确区分：

1. 默认可抽物品。
2. 锚点命中才可抽物品。
3. 永不抽取、只用于校验的风险规则。

## User Input: No Image Recognition Constraint

用户进一步澄清：工具没有识别图像的能力，所以 `anchor_required_items` 的“画面锚点”并不成立；`blocked_or_risky` 可以去除，需要重点研究 `anchor_required_items` 应该重新定义成什么。

> **Decision**: 废弃“图像锚点条件池”概念。
> - **Context**: 当前工具只能基于盒号、类别、用户输入文本、抽取规则和历史权重工作，不能确认画面里是否存在显示器、白板、伞杆、墙面挂点等对象。
> - **Options considered**: 继续保留 `anchor_required_items`、改成用户显式语境池、改成默认可抽安全扩展池、改成纯排除参考池。
> - **Chosen**: 将“锚点”从图像条件改为“显式文本语境”，推荐命名为 `explicit_context_items`；若暂不实现文本触发，则先落为 `context_dependent_excluded_items`。
> - **Rejected**: 图像锚点版 `anchor_required_items`，因为工具没有对应事实来源，字段再结构化也无法判断条件是否成立。
> - **Impact**: 下一轮 spec 不应要求图像锚点检测；应围绕“默认安全池 + 显式语境池 + 禁用规则测试”设计。

## Round 3: No-Image Context Model

### What The Tool Can Know

当前工具能可靠使用的信息只有：

- 用户输入的盲盒编号，例如 `15`。
- 用户输入的文本覆盖语法，例如 `无大型物品`、`中型物品+1`。
- 未来可扩展的用户文本关键词，例如 `电脑桌`、`白板`、`露营灯`。
- 固定类别数据和历史权重。

当前工具不能知道：

- 图片里有没有显示器。
- 图片里有没有白板。
- 图片里有没有伞杆、挂点、墙面、桌侧空间。
- 某个物品是否已经存在、是否有空位、是否被遮挡。

因此任何定义都必须遵守：**不能把图像条件当作抽取条件**。

### Candidate Definitions

#### Option A: `explicit_context_items`

定义：只由用户显式文本触发的语境候选池，不由图像触发。

示例：

```python
{
    "context_key": "电脑桌学习",
    "trigger_keywords": ["电脑桌", "显示器", "屏幕", "键盘"],
    "items": ["显示器增高架", "键盘收纳托", "桌面理线盒"],
    "default_enabled": False
}
```

规则：

- 用户没有输入触发词时不参与输出。
- 触发词来自用户文本，不来自图像。
- 适合承载“某个子场景很合理，但大场景不总是合理”的物品。
- 仍然禁止太细、太小、透明、反光、发光和动物本体。

优点：保留“条件物”的价值，但条件来源真实可靠。  
缺点：需要扩展输入解析或至少先作为未来结构保留。

#### Option B: `context_dependent_excluded_items`

定义：依赖具体画面条件、但当前工具无法判断，因此默认排除的参考池。

示例：

```python
{
    "reason": "requires_unobservable_context",
    "items": ["显示器下方收纳架", "白板磁吸收纳盒", "遮阳伞底座"]
}
```

规则：

- 永不进入默认输出。
- 用于维护者知道“这些东西不是坏物品，但当前工具不能自动抽”。
- 可作为未来 `explicit_context_items` 的素材来源。

优点：立即安全，改动小。  
缺点：不产生新可抽内容，只是避免误用。

#### Option C: `optional_safe_items`

定义：无任何前置条件、只是优先级较低的安全扩展池。

示例：

```python
{
    "items": ["桌面资料篮", "折叠阅读架", "硬壳收纳盒"],
    "default_enabled": True,
    "weight": 0.4
}
```

规则：

- 必须不依赖图像前置条件。
- 可以低权重进入默认输出。
- 本质上是 `support_items` 的低频扩展，不再表达“条件”。

优点：当前工具马上可用。  
缺点：如果这样定义，`conditional_items` 这个概念就没有必要存在，直接并入 `support_items` 更清晰。

### Recommended Definition

最推荐采用双层定义：

1. `explicit_context_items`：未来可启用的“用户显式语境池”。
2. `context_dependent_excluded_items`：当前不能自动判断的画面依赖物，默认排除。

不建议继续使用 `anchor_required_items` 这个名字，因为它天然让人误解为图像锚点。

### Revised Pool Model

建议从五层池改为：

| 新字段 | 是否默认输出 | 作用 |
|---|---:|---|
| `core_items` | 是 | 最稳的默认大/中型主物 |
| `support_items` | 是 | 无图像前置条件的场景配套物 |
| `visible_small_items` | 是 | 成组、块状、有承载的小物 |
| `safe_hanging_items` | 是 | 体量足够、边界清楚、不细线化的悬挂/垂挂物 |
| `explicit_context_items` | 否，除非用户文本触发 | 由用户输入语境启用的子场景物 |
| `context_dependent_excluded_items` | 否 | 当前工具无法判断条件的排除参考物 |
| `blocked_patterns` | 否 | 禁用模式测试规则，不是物品池 |

### What Happens To `blocked_or_risky`

同意用户判断：`blocked_or_risky` 可以去除。

替代方式：

- 具体禁用物不再作为池保存。
- 使用 `blocked_patterns` / `blocked_terms` 维护规则，例如：
  - `细绳`
  - `流苏`
  - `边线`
  - `折线`
  - `擦痕`
  - `阴影`
  - `高光`
  - `反光`
  - `透明`
  - `动物本体`
- 测试负责确保这些模式不进入默认输出池。

### Revised Converged Recommendation

下一轮规格应改名为：

`Game content extraction 盲盒物品池无图像条件重构`

核心目标：

1. 删除 `blocked_or_risky` 作为物品池。
2. 废弃图像锚点版 `anchor_required_items`。
3. 新增或预留 `explicit_context_items`，只允许由用户显式文本触发。
4. 新增 `context_dependent_excluded_items`，收纳当前不能自动判断的画面依赖物。
5. 新增 `safe_hanging_items`，替代当前 `conditional_items -> hanging` 的默认映射。
6. 默认输出只来自无需图像条件的安全池。

### Round 3 Narrative Synthesis

**Starting point**: 上一轮假设可以用 `required_anchor` 表达条件，但用户指出工具并不识别图像。  
**Key progress**: 条件来源被重新限定为“用户显式文本”，而不是“图像已有物”。  
**Decision impact**: `anchor_required_items` 这个名字和模型被废弃；新的候选方向是 `explicit_context_items` + `context_dependent_excluded_items`。  
**Current state**: 最稳设计是默认池只输出无条件安全物；需要语境的物品必须由用户文本触发，不能从图像推断。  
**Open directions**: 需要决定第一版实现是否加入用户文本触发，还是先只做字段重构与默认排除。

## User Input: Final Content Category Direction

用户进一步收敛：可以将内容类别整体重构，不再做任何锚点相关设计。前三类固定为：

1. `core_items`
2. `support_items`
3. `visible_small_items`

第四类将原 `anchor_required_items` / `conditional_items` 重构为：

```text
scene_expansion_items
```

中文定义：

```text
场景扩展物
```

同时，`blocked_or_risky` 不再作为内容类别保留。

> **Decision**: 采用四类内容模型：`core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`。
> - **Context**: 工具无法读取图像，也不应引入伪锚点、隐式条件或需要用户额外触发的复杂语境池。
> - **Options considered**: `explicit_context_items`、`context_dependent_excluded_items`、`safe_hanging_items`、`scene_expansion_items`。
> - **Chosen**: `scene_expansion_items` — **Reason**: 它不依赖图像锚点，不需要输入触发，也不会把第四类限制成悬挂物；它表达的是“场景中合理但非核心、用于增加变化的中等以上物品”。
> - **Rejected**: `explicit_context_items` 和 `context_dependent_excluded_items`，因为它们仍然围绕条件/排除在建模；`safe_hanging_items` 过窄，容易把第四类重新带回挂饰、细绳、垂挂物的问题。
> - **Impact**: 下一轮 spec 应聚焦四类内容库重构；`blocked_or_risky` 转为测试层 `blocked_patterns`，不进入内容模型。

## Round 4: Four-Pool Content Model

### Final Pool Definitions

| 字段 | 中文名 | 默认输出 | 定义 |
|---|---|---:|---|
| `core_items` | 核心物 | 是 | 当前场景最典型、最稳定、最优先抽取的主物。 |
| `support_items` | 配套物 | 是 | 围绕核心物使用的工具、容器、收纳、承载或功能配件。 |
| `visible_small_items` | 可见小物 | 是 | 成组、块状、有承载、边界清楚的小物；禁止碎屑、痕迹、细线、小点。 |
| `scene_expansion_items` | 场景扩展物 | 是 | 不依赖图像锚点、不需要已有对象成立，但能扩展场景氛围和玩法变化的中等以上物品。 |

### Definition Of `scene_expansion_items`

`scene_expansion_items` 不是“条件物”，也不是“悬挂物”。它应满足：

- 不需要画面里已有某个对象才能成立。
- 不需要工具识别图像内容。
- 不是核心必需品，但放在该场景里自然、常见、可解释。
- 体量中等以上，边界清楚，可独立圈选。
- 能增加场景变化，而不是重复核心物或配套物。
- 禁止细绳、流苏、边线、微型挂件、透明反光、发光效果、动物本体、痕迹类对象。

### User Examples Preserved As Model Samples

#### 桌面+学习

- 核心物：硬壳笔记本、桌面文件架、书桌小白板
- 配套物：笔筒、资料夹、计时器
- 可见小物：一排彩色笔套、三块记号小卡
- 场景扩展物：桌面日历、桌面小风扇、护眼书架、桌面收纳抽屉

#### 公园+野餐

- 核心物：格纹野餐垫、藤编食物篮、双层餐盒
- 配套物：餐具盒、保温水壶、杯架托盘
- 可见小物：三块三明治切块、一组水果叉盒
- 场景扩展物：折叠野餐桌、便携冷藏箱、户外收纳箱、野餐遮阳布

### Runtime Mapping

为保持现有 UI 四栏不变，短期可映射为：

- `large` <- `core_items + scene_expansion_items`
- `medium` <- `support_items + core_items:first_6`
- `small` <- `visible_small_items`
- `hanging` <- 可以保留字段但从 `scene_expansion_items` 中筛选明确可悬挂且不细线化的对象，或短期降权/减少数量

更保守的方案：

- `hanging` 不再强制来自第四类。
- 如果没有高质量悬挂物，就减少或跳过悬挂输出，不用细绳、挂饰、边线类内容凑数。

### What Happens To Removed Concepts

- `conditional_items`：废弃，不再作为内容类别。
- `anchor_required_items`：废弃，避免暗示图像锚点。
- `explicit_context_items`：本轮不做，避免增加输入语境复杂度。
- `context_dependent_excluded_items`：本轮不做，避免把不可用内容继续留在主数据模型里。
- `blocked_or_risky`：从内容类别删除，规则迁移到测试层 `blocked_patterns`。

### Round 4 Narrative Synthesis

**Starting point**: 上一轮仍保留了“显式文本语境池”和“画面依赖排除池”两个复杂概念。  
**Key progress**: 用户把方向进一步压实为四类内容库，第四类从条件/锚点语义改为场景扩展语义。  
**Decision impact**: 内容模型不再围绕“条件是否成立”，而是围绕“默认可用且对场景有增益”。  
**Current state**: 推荐最终四池：`core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`；风险内容只作为 `blocked_patterns` 测试规则。  
**Open directions**: 下一步 spec 需要定义四池验收、三类试点重写、四栏兼容映射、blocked pattern 测试。
