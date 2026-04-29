---
session_id: SPEC-2026-04-29-blind-box-pool-itemization-fix
phase: 2
document_type: product-brief
status: complete
generated_at: 2026-04-29T00:00:00+08:00
stepsCompleted:
  - load-handoff
  - synthesize-feedback
  - define-corrected-scope
version: 1
dependencies:
  - spec-config.json
  - refined-requirements.json
  - discovery-context.json
  - ../../.brainstorm/BS-2026-04-29-盲盒条件风险池物品化修正/handoff-spec.json
---

# Product Brief: 盲盒条件池与风险池物品化修正

本规格是对 `Game content extraction` 盲盒物品库试点实现的窄范围修正。目标不是重新设计 20 类入口，而是修正 `conditional_items` 和 `blocked_or_risky` 的内容边界：所有五层物品池条目都必须是具体物品，折线、擦痕、阴影、气泡、边线等非物品内容只能作为校验禁用模式存在。

## Concepts & Terminology

| Term | Definition | Aliases |
|------|------------|---------|
| 具体物品 | 可在目标图中作为独立对象被识别、放置和圈选的物品或物品组。 | 具体对象, 完整物品 |
| 条件启用物品 | 只有在特定承载面、挂架、空间或场景关系成立时才适合使用，但本身仍具备中等以上体量和独立可见性的具体物品。 | conditional_items, 条件物 |
| 具体风险物 | 与场景相关且具体可见，但因透明、反光、发光、动物本体、细绳、流苏、软布飘带等风险默认禁用的物品。 | blocked_or_risky |
| 非物品禁用模式 | 折线、擦痕、阴影、气泡、边线、微小颗粒等不可作为物品池条目的视觉现象或痕迹表达。 | forbidden_patterns, reject terms |
| 五层物品池 | `core_items`、`support_items`、`visible_small_items`、`conditional_items`、`blocked_or_risky` 五个内容层，修正后全部只允许写具体物品。 | 五层池 |

## Vision

盲盒物品库里的每个条目都应该像一个能进入游戏画面的对象，而不是差异痕迹、视觉现象或局部描述。成功时，维护者看到任何池层都能按“具体物品”标准写库，工具使用者不会再抽到或审查到 `纸张边缘折线`、`微小擦痕`、`海底阴影斑` 这类不可用内容。

## Problem Statement

### Current Situation

上一轮实现已经建立三类试点：15 `桌面+学习`、16 `海底+潜水`、17 `公园+野餐`，并加入五层池和四栏兼容映射。但 `conditional_items` 被写成大量小标签、小卡片、小扣件、贴在边缘的附属物；`blocked_or_risky` 则混入折线、擦痕、气泡、阴影、边线、碎叶点、微小污点等非物品内容。

### Impact

- 内容维护者会误以为风险池可以收纳“任何不可用表达”，导致后续继续写出非物品条目。
- 工具使用者需要的是可见、可圈选、可放置的游戏差异物品；非物品现象无法直接使用。
- 当前测试只验证 `blocked_or_risky` 不进入默认四栏，但没有验证风险池本身必须是具体物品。

## Target Users

### 内容维护者
- **Role**: 维护 `blind_boxes.py` 与提示词规则的人。
- **Needs**: 清晰知道所有五层池都只写具体物品，非物品禁用内容只放校验清单。
- **Pain Points**: 条件池容易写小附属件，风险池容易变成不可用词垃圾桶。
- **Success Criteria**: 能按规则替换三类试点，并在后续扩库时不再写入非物品条目。

### 工具使用者
- **Role**: 使用盲盒输出继续写游戏差异或图像局部替换建议的人。
- **Needs**: 每个输出候选都接近真实可见物品，而不是折线、阴影、气泡或微小痕迹。
- **Pain Points**: 不可用内容会增加二次筛选成本。
- **Success Criteria**: 默认输出和风险审查内容都能被理解为具体物品。

### App 维护者
- **Role**: 维护数据结构、测试和文档的人。
- **Needs**: 保持当前字段名和运行时兼容，同时补上更强校验。
- **Pain Points**: 不希望为一次内容修正引入 UI 或历史迁移。
- **Success Criteria**: 通过测试锁定规则，避免后续回归。

## Goals & Success Metrics

| Goal ID | Goal | Success Metric | Target |
|---------|------|----------------|--------|
| G-001 | 修正 `conditional_items` 的体量和独立性 | 三类试点条件池低价值小件数量 | 0 |
| G-002 | 修正 `blocked_or_risky` 的物品边界 | 三类试点风险池非物品条目数量 | 0 |
| G-003 | 建立非物品禁用模式校验 | forbidden patterns 测试覆盖范围 | 所有五层池、三类试点 |
| G-004 | 保持运行时兼容 | 15/16/17 号盒四栏 contract | 100% 保持 |
| G-005 | 同步维护文档 | 必更文档同步状态 | 5/5 |

## Scope

### In Scope

- 替换三类试点 `conditional_items`。
- 替换三类试点 `blocked_or_risky`。
- 新增或扩展 forbidden patterns 测试。
- 同步项目文档中的池层定义。

### Out of Scope

- 全量重写 20 类。
- 改名 `blocked_or_risky` 字段。
- 改 UI、输入语法、历史 key 或四栏输出。
- 发布新版本或打包安装器。

### Non-Goals

| Non-Goal | Rationale |
|----------|-----------|
| 删除 `conditional_items` | 条件池仍有价值，只是需要物品化和体量底线。 |
| 删除 `blocked_or_risky` | 风险池能提醒维护者哪些具体物品不该默认抽取。 |
| 把 forbidden patterns 作为抽取数据 | 它们是校验和审查规则，不是可抽内容。 |
| 通过运行时过滤掩盖数据问题 | 这次目标是修正静态内容和测试，不能让坏数据继续存在。 |

## Competitive Landscape

| Aspect | Current State | Proposed Solution | Advantage |
|--------|---------------|-------------------|-----------|
| 条件池 | 小标签、小卡片、小扣件偏多 | 中等以上体量的条件启用物品 | 更适合游戏画面差异 |
| 风险池 | 混入痕迹、阴影、边线等非物品 | 只保留具体风险物 | 规则更直观，不污染内容库 |
| 校验 | 只测风险池不泄漏 | 测非物品禁用模式不进入任何池 | 防止回归 |
| 实施范围 | 可能扩散到模型重构 | 只修三类试点和测试 | 风险低、反馈快 |

## Constraints & Dependencies

### Technical Constraints

- `BLIND_BOXES` 仍必须暴露 `name`、`large`、`medium`、`small`、`hanging`。
- 15 / 16 / 17 试点盒号保持不变。
- 不改 `draw_history.json` 结构。
- 不引入新依赖。

### Dependencies

- [refined-requirements.json](refined-requirements.json)
- [discovery-context.json](discovery-context.json)
- Upstream brainstorm handoff: [handoff-spec.json](../../.brainstorm/BS-2026-04-29-盲盒条件风险池物品化修正/handoff-spec.json)

## Multi-Perspective Synthesis

### Product Perspective

用户反馈说明“风险隔离”不能只做到不进入默认输出，还要保证风险池本身可读、可维护、是具体物品。否则后续维护会继续复制不可用表达。

### Technical Perspective

最稳妥的技术路径是保持字段名和运行时映射不变，只替换静态数据并扩展测试。这样不触碰 UI、历史和四栏兼容，回归面最小。

### User Perspective

工具使用者关心的是条目能否直接用作游戏差异对象。小标签和非物品现象都不满足这一点，因此所有池层都必须接受“可单独圈选”的物品化底线。

### Convergent Themes

- 五层池全都必须是具体物品池。
- 非物品内容应迁移为 forbidden patterns。
- 当前修正应局限于三类试点，快速关闭反馈。

## Open Questions

- [ ] `forbidden_patterns` 是否作为模块常量导出，还是只存在于测试中？
- [ ] 长期是否将 `blocked_or_risky` 改名为 `blocked_objects`？

## References

- Derived from: [spec-config.json](spec-config.json)
- Derived from: [refined-requirements.json](refined-requirements.json)
- Next: [Requirements PRD](requirements/_index.md)
