# Brainstorm Session

**Session ID**: BS-2026-04-29-盲盒条件风险池物品化修正  
**Topic**: 修正 `conditional_items` 与 `blocked_or_risky` 的内容定义  
**Started**: 2026-04-29T00:00:00+08:00  
**Mode**: Balanced  
**Perspectives**: creative, pragmatic, systematic

## Current Ideas

1. **所有五层池条目必须是具体物品**  
   痕迹、阴影、边线、微小颗粒、气泡、折线等非物品内容不得进入任何 item pool。

2. **`conditional_items` 改成条件启用的完整可见物品**  
   条件池不再写小标签、小扣件、小贴片，而写中等以上体量、可圈选、需要场景前提的具体物品。

3. **`blocked_or_risky` 只保留具体风险物**  
   风险池可以写透明杯、玻璃瓶、发光灯、反光刀、动物本体、细绳流苏类具体物品；不能写“微小擦痕”“海底阴影斑”。

4. **新增 `forbidden_patterns` / reject terms**  
   非物品禁用表达作为校验清单存在，不参与抽取、不作为物品池。

## Session Context

### User Input

用户反馈：上次盲盒物品中，`conditional_items` 和 `blocked_or_risky` 实际产出的内容不太行；`conditional_items` 内容太小，对游戏用处不大；`blocked_or_risky` 会生成类似 `纸张边缘折线`、`微小擦痕`、`细小气泡串`、`漂浮细海草丝`、`海底阴影斑` 这类不可用内容。用户需要的是具体物品。

### Code Context

- `Game content extraction/data/blind_boxes.py` 当前三类试点存在此问题。
- `REQ-005` 已要求默认条目真实、常见、边界清楚、可单独圈选、强场景相关。
- `ADR-004` 把风险物隔离为架构决策，但需要补充“风险物也必须是具体物品”。

## Exploration Vectors

1. `conditional_items` 是否应该继续存在？如果存在，它的最小体量是什么？
2. `blocked_or_risky` 应该是物品池，还是禁用词池？
3. 非物品内容应该放在哪里，才能帮助校验但不污染抽取？
4. 三类试点应如何替换为更可用的具体物品？
5. 需要新增哪些测试防止回归？

---

## Thought Evolution Timeline

### Round 1 - Failure Pattern Analysis

#### Ideas Generated

- `conditional_items` 不是“小附属关系池”，而应是“条件启用的大/中型具体物品池”。
- `blocked_or_risky` 不是“垃圾桶”，而应是“具体风险物池”。
- 痕迹、阴影、边线、气泡、碎叶、微小颗粒应进入 `forbidden_patterns`，用于测试和审查。

#### Challenged Assumptions

- ~~只要 `blocked_or_risky` 不进入默认输出，就可以写任何不可用内容。~~  
  → 不成立。它仍然是内容库的一部分，会影响维护者理解，也可能污染后续生成或审查。

- ~~`conditional_items` 可以写依赖承载关系的小物。~~  
  → 只部分成立。条件池可以依赖承载关系，但条目本身必须有足够体量和独立可见性。

#### Decision Log

> **Decision**: 五层池统一执行“具体物品”底线。  
> - **Context**: 用户指出风险池和条件池实际产出不可用。  
> - **Options considered**: 删除两个字段、保留但改规则、拆分字段。  
> - **Chosen**: 短期保留字段名但重写内容规则。  
> - **Rejected**: 立即删字段会影响刚建立的 spec 和测试；继续原规则会复发问题。  
> - **Impact**: 后续修正范围聚焦为内容替换 + 校验增强 + 文档同步。

#### Narrative Synthesis

本轮把问题从“某几个词不好”推进到“字段语义边界不清”。真正要修的不是单条替换，而是建立新底线：只要是 item pool，就必须是具体物品；不可用现象不能伪装成物品。

---

## Synthesis & Conclusions

### Primary Recommendation

短期保留 `conditional_items` 和 `blocked_or_risky` 字段名，但立即修改定义：

- `conditional_items`: 条件启用的完整可见物品，体量不低于 medium，不写小标签、小贴片、小扣件。
- `blocked_or_risky`: 具体风险物品，因透明、反光、发光、动物本体、细绳、流苏、软布等原因默认禁用。
- `forbidden_patterns`: 新增校验概念，收纳折线、擦痕、阴影、气泡、碎叶、边线、微小颗粒等非物品禁用表达。

### Concrete Replacement Direction

详见 [pool-rule-rewrite.md](ideas/pool-rule-rewrite.md)。

### Implementation Handoff Candidate

若进入执行，应做三件事：

1. 替换三类试点的 `conditional_items` 和 `blocked_or_risky`。
2. 新增测试，禁止非物品禁用词进入任何五层池。
3. 同步文档中对 `conditional_items` / `blocked_or_risky` 的定义。

## Artifacts

- [exploration-codebase.json](exploration-codebase.json)
- [perspectives.json](perspectives.json)
- [synthesis.json](synthesis.json)
- [pool-rule-rewrite.md](ideas/pool-rule-rewrite.md)
- [handoff-spec.json](handoff-spec.json)

## Terminal Gate

用户选择：`Execute Task`。

已生成 `handoff-spec.json`，建议后续按该文件做 scoped edit 或进入 `workflow-plan`。
