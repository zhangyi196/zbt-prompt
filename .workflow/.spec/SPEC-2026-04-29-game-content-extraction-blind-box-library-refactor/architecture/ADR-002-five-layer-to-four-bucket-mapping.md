---
id: ADR-002
status: Accepted
traces_to: [REQ-002, REQ-003, NFR-P-001, NFR-SC-001]
date: 2026-04-29T00:00:00+08:00
---

# ADR-002: 五层池映射回四栏运行时

## Context

新内容模型需要 `core_items`、`support_items`、`visible_small_items`、`conditional_items`、`blocked_or_risky` 五层，但现有 UI、输入解析、抽取输出和历史降权仍绑定 `large`、`medium`、`small`、`hanging` 四栏。

## Decision

短期保留四栏运行时 contract。每个五层 bundle 必须提供兼容映射：`core_items` 主要进入 `large`，`support_items` 进入 `medium`，`visible_small_items` 进入 `small`，少量合规 `conditional_items` 进入 `hanging`，`blocked_or_risky` 不进入任何默认抽取栏。

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| 五层到四栏映射 | 兼容现有工具，降低发布风险，允许逐类试点。 | 内容模型与运行时结构短期并存，需要维护映射。 |
| 直接把运行时改成五层 | 模型更纯粹。 | 会影响 UI、输入语法、历史 key 和测试面，超出本阶段范围。 |
| 只在文档中描述五层，数据仍完全四栏 | 改动最少。 | 容易让风险物继续混入默认池，规范难以验证。 |

## Consequences

- **Positive**: 试点可以先验证内容质量，不需要一次性重写 UI 和历史逻辑。
- **Negative**: 实现阶段要确保映射生成结果与旧数据格式完全一致。
- **Risks**: 映射若缺少测试，`blocked_or_risky` 可能泄漏进默认输出。

## Traces

- **Requirements**: [REQ-002](../requirements/REQ-002-five-layer-item-pool-schema.md), [REQ-003](../requirements/REQ-003-four-bucket-compatibility-mapping.md), [NFR-P-001](../requirements/NFR-P-001-compatibility-latency-budget.md), [NFR-SC-001](../requirements/NFR-SC-001-incremental-rollout-scale.md)
- **Implemented by**: Phase 5 epics.
