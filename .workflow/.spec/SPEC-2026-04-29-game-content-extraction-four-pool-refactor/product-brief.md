---
session_id: SPEC-2026-04-29-game-content-extraction-four-pool-refactor
phase: 2
document_type: product-brief
status: complete
generated_at: 2026-04-29T00:00:00+08:00
stepsCompleted:
  - synthesis
version: 1
dependencies:
  - spec-config.json
  - refined-requirements.json
  - ../.brainstorm/BS-2026-04-29-重新定义conditional-items-blocked-or-risky/handoff-spec.json
---

# Product Brief: Game content extraction 盲盒物品四类内容池重构

本规格将 `Game content extraction` 的盲盒试点物品库从“条件池 / 风险池”语义，收敛为更适合当前工具能力的四类内容池。工具不识别图像，因此不再设计锚点条件物；风险内容也不再作为候选物品池，而是迁移到 `blocked_patterns` 测试和校验规则。

## Concepts & Terminology

| Term | Definition | Aliases |
|------|------------|---------|
| 四类内容池 | `core_items`、`support_items`、`visible_small_items`、`scene_expansion_items` 四类默认安全内容池。 | four-pool model |
| 场景扩展物 | 中等以上体量、无需图像锚点、能自然扩展场景变化的物品。 | `scene_expansion_items` |
| 默认安全池 | 不依赖图像识别、用户额外触发或不可验证前置条件即可默认抽取的池。 | default-safe pool |
| `blocked_patterns` | 测试 / 校验层禁用模式，不是候选物品池。 | blocked terms |
| 四栏兼容视图 | 现有 `BLIND_BOXES` 的 `large` / `medium` / `small` / `hanging` 输出结构。 | legacy runtime contract |

## Vision

盲盒物品库应只输出当前工具能够稳定支持的内容：具体、常见、边界清楚、无需看图判断前置条件、适合游戏圈选。四类内容池让维护者能持续扩展内容，同时避免条件物、风险物和微型痕迹反复回流。

## Problem Statement

### Current Situation

当前三类试点盒已引入五层池：`core_items`、`support_items`、`visible_small_items`、`conditional_items`、`blocked_or_risky`。用户反馈表明，即便条目改成具体物品，`conditional_items` 仍会产生“显示器下方收纳架”这类需要图像锚点的内容；`blocked_or_risky` 也容易保存“细绳挂饰”等具体但游戏不可用的低质量对象。

### Impact

盲盒输出如果依赖工具无法验证的图像条件，会降低结果可用性；如果风险内容仍作为池存在，后续维护者容易误把它当候选物品。目标是让三类试点抽取结果中明显不适合项降到 10% 以下，并用测试阻止旧问题回归。

## Target Users

### 提示词和数据维护者

- **Role**: 维护中文提示词规则和 `Game content extraction` 数据库。
- **Needs**: 清晰的池层定义、可执行的写库规则、稳定的测试边界。
- **Pain Points**: 条件池和风险池职责不清，导致反复修词。
- **Success Criteria**: 能按四类内容池独立扩展试点数据，不需要猜测某物应归入条件池还是风险池。

### 盲盒抽取工具用户

- **Role**: 使用本地工具生成游戏差异物品候选。
- **Needs**: 输出物品真实、常见、可圈选、与所选场景自然相关。
- **Pain Points**: 抽到依赖未验证图像条件或太细太小的对象时，游戏用处不大。
- **Success Criteria**: 试点盒默认输出不出现锚点依赖物、细线挂饰、透明反光发光物、动物本体或微型痕迹。

## Goals & Success Metrics

| Goal ID | Goal | Success Metric | Target |
|---------|------|----------------|--------|
| G-001 | 建立四类内容池 schema | 三类试点 bundle 仅含四类内容池键 | 100% |
| G-002 | 定义并落地场景扩展物 | `scene_expansion_items` 全部为中等以上、无图像锚点依赖物 | 100% |
| G-003 | 移除风险候选池 | `blocked_or_risky` 不再作为 pilot candidate pool 出现 | 100% |
| G-004 | 保持运行时兼容 | `BLIND_BOXES[15/16/17]` 仍提供四栏输出 | 100% |
| G-005 | 建立回归测试 | 单元测试覆盖四池 schema、禁用模式、兼容映射 | 通过 |

## Scope

### In Scope

- 重构 15 `桌面+学习`、16 `海底+潜水`、17 `公园+野餐` 三个试点盒。
- 用 `scene_expansion_items` 替代 `conditional_items`。
- 删除 `blocked_or_risky` 作为候选物品池。
- 更新四栏兼容映射和测试。
- 同步 `agents.md`、`README.md`、`Game content extraction/CLAUDE.md`、`Game content extraction/README.md`、`.gitignore`。

### Out of Scope

- 图像识别、锚点检测或用户文本触发解析。
- UI 改版。
- 全量 20 类内容扩展。
- 数据库、服务端或 Web 化。
- 版本发布、安装包构建或 tag。

### Non-Goals

| Non-Goal | Rationale |
|----------|-----------|
| 不做图像锚点判断 | 当前工具没有图像输入分析能力，设计该能力会产生虚假约束。 |
| 不保留风险物品池 | 风险项作为池存在会诱导未来误用，测试规则更合适。 |
| 不强制填满悬挂栏 | 为了填满 `hanging` 而使用细绳、挂饰、边线会降低质量。 |

### Assumptions

- `BLIND_BOXES` 四栏结构是 UI 和输入语法的短期兼容层。
- `blocked_patterns` 可先在测试中定义，未来若需要运行时复用再提升为数据模块。
- 三类试点足够验证四池模型边界。

## Multi-Perspective Synthesis

### Product Perspective

用户价值来自更稳定的默认输出，而不是更复杂的条件系统。第四类用“场景扩展物”表达内容丰富度，比条件池和悬挂池更符合工具当前能力。

### Technical Perspective

改动应集中在 `blind_boxes.py` 的数据模型、兼容映射和 `test_blind_box_content_model.py`。不需要 UI 改动，也不需要第三方依赖。

### User Perspective

用户不关心池层术语，只关心抽到的物品是否适合游戏。四池模型应把“不用看图也合理”的物品放进默认池，把风险词放进测试。

### Convergent Themes

- 默认候选必须无需图像条件。
- 第四类应扩展场景，而不是承担锚点、悬挂、风险或排除语义。
- 测试必须比文档更硬，防止旧词回流。

### Conflicting Views

`hanging` 是否继续输出仍有实现取舍。推荐保守处理：不强制填充低质量悬挂物，必要时从高质量场景扩展物中少量映射。

## Open Questions

- [ ] `hanging` 是否允许为空或减少默认数量？
- [ ] `scene_expansion_items` 是否只映射到 `large`，还是也低权重进入 `medium`？
- [ ] `blocked_patterns` 是否只保留在测试文件，还是抽为数据常量？

## References

- Derived from: [.workflow/.brainstorm/BS-2026-04-29-重新定义conditional-items-blocked-or-risky/handoff-spec.json](../../.brainstorm/BS-2026-04-29-重新定义conditional-items-blocked-or-risky/handoff-spec.json)
- Next: [Requirements](requirements/_index.md)
