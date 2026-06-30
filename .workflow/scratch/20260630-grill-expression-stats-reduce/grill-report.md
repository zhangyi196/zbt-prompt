# Grill Report: 人物表情统计主动降低次数

**Session**: GRL-002
**Depth**: shallow (3 branches)
**Date**: 2026-06-30T15:20:00+08:00
**Upstream**: user request

## Discovery Summary

### Project Context

- `Game content extraction/` 是 Python `tkinter/ttk` 桌面工具，不引入 Web、数据库或服务端。
- 人物表情统计写入 `Game content extraction/expression_stats.json`，独立于 `draw_history.json.expression_pools`。
- 修改表情逻辑后需要运行 `Game content extraction/test_expression_enhancement.py`，UI 改动至少运行 `py_compile`。
- 任务前存在与本任务无关的未提交 `.workflow` 变更，不能回滚或混入业务修改。

### Codebase Surface

- `Game content extraction/内容抽取.py:235` 建立 `expression_stats` 结构，核心计数字段是 `committed_counts.{正向,负向}`。
- `Game content extraction/内容抽取.py:363` 的 `_adjust_expression_stats_counts(entries, delta)` 已支持按条目加减，减到 0 以下时删除 key。
- `Game content extraction/内容抽取.py:381` 的 `_commit_pending_expression_stats()` 会把当前输入最后一次结果提交；如果本组已提交，会先对旧 `current_committed_entries` 扣 1，再给 `current_last_entries` 加 1。
- `Game content extraction/内容抽取.py:424` 的 `_format_expression_stats_summary()` 只读取 `committed_counts`，并按 0、1、2、3-4、5+ 分组输出权重。
- `Game content extraction/内容抽取.py:1659` 的表情工作区当前只有模板编号控件和 `表情统计`、`清空输入`、`抽取表情`、`复制结果` 4 个按钮。
- `Game content extraction/test_expression_enhancement.py:532` 覆盖统计摘要分组；`567`、`583`、`597` 覆盖同一输入只提交最后一次、切换输入提交旧输入、重提替换旧统计。

### Upstream Material

用户期望在人物表情抽取中新增主动降低正负向表情次数的功能，例如主动降低正向所有表情 3 次，主动降低负向所有表情 2 次，默认作用于所有表情。

---

## Branch Log

| # | Branch | Status | Decisions | Open Questions |
|---|--------|--------|-----------|----------------|
| 1 | Scope & Boundaries | Completed | 2 | 0 |
| 2 | Data Model & State | Completed | 2 | 0 |
| 3 | Edge Cases & Failure Modes | Completed | 2 | 0 |

---

## Branch 1: Scope & Boundaries

**Status**: Completed
**Questions asked**: 2
**Decisions locked**: 2

### Q1.1: 主动降低是否应先提交当前暂存结果

**Question**: 当前 `表情统计` 按钮会先调用 `_commit_pending_expression_stats()`，把当前输入最后一次实际抽取结果提交后再复制摘要。新增“降低正向所有表情 3 次 / 降低负向所有表情 2 次”时，是否也必须先提交当前未提交的最后一次结果，再执行降低？
**Evidence**: `内容抽取.py:381-404`；`内容抽取.py:2153-2158`；`test_expression_enhancement.py:567-612`。
**Answer**: 不需要。这个功能是人工认为要降低的时候再手动点击，不是脚本自动检测或自动跟随统计按钮。
**Decision**: Locked.
**Constraint**: MUST keep manual reduction separate from `_commit_pending_expression_stats()`; clicking the reduction control MUST NOT auto-submit `current_last_entries`.
**Risk**: 当前未提交的最后一次抽取结果仍可能在后续点击 `表情统计`、切换输入或关闭 App 时被提交；这是现有统计语义，不由手动降低按钮隐式处理。

### Q1.2: 手动降低入口的形态

**Question**: 表情工作区当前按钮顺序固定为 `表情统计`、`清空输入`、`抽取表情`、`复制结果`，且只有一个模板编号 `Spinbox`。新增人工降低功能时，是在同一页面加“正向降低次数 / 负向降低次数”的数字输入和两个按钮，还是只加一个按钮并通过弹窗输入次数？
**Evidence**: `内容抽取.py:1659-1700`；`Game content extraction/agents.md` 表情区按钮顺序约束。
**Answer**: 放置一个按钮；点击后输入降低次数，并通过单选选择正向或负向，一次不同时选择两个极性。
**Decision**: Locked.
**Constraint**: MUST expose one manual reduction button; the dialog MUST contain polarity radio selection and one reduction count, and each confirm MUST apply to exactly one polarity.
**Risk**: 需要同步更新表情区按钮顺序文档，因为现有文档把 4 个按钮顺序写为固定。

---

## Branch 2: Data Model & State

**Status**: Completed
**Questions asked**: 2
**Decisions locked**: 2

### Q2.1: 降低目标字段

**Question**: 手动降低应修改哪个状态字段？
**Answer**: 根据用户确认的人工校准语义和代码结构，应只修改 `expression_stats.committed_counts[polarity]`，不修改 `draw_history.json.expression_pools`，也不提交 `current_last_entries`。
**Evidence**: `内容抽取.py:235-245`；`内容抽取.py:363-379`；项目文档说明统计独立于抽取降权历史。
**Decision**: Locked.
**Constraint**: MUST reduce only `committed_counts` for the selected polarity; MUST NOT mutate `expression_pools`.

### Q2.2: 降低范围与下限

**Question**: 当选择正向或负向并输入次数时，应作用哪些类别，计数不够时怎么办？
**Answer**: 用户前置需求是“默认所有表情”，因此选择某个极性后作用于该极性的全部表情库类别；每个计数最多降到 0，降到 0 后从 `committed_counts` 删除。
**Evidence**: 用户需求；`_adjust_expression_stats_counts` 现有减法语义已经在 `next_count <= 0` 时删除 key。
**Decision**: Locked.
**Constraint**: MUST apply reduction to all official categories in the selected polarity by default; counts MUST NOT go below zero.

---

## Branch 3: Edge Cases & Failure Modes

**Status**: Completed
**Questions asked**: 2
**Decisions locked**: 2

### Q3.1: 非法次数

**Question**: 输入 0、负数或非数字时怎么办？
**Answer**: 弹窗输入应限制为正整数；确认时仍做校验，非法输入给出错误提示，不写文件。
**Evidence**: `tkinter` UI 当前已使用 `Spinbox` 输入模板编号；项目使用 `messagebox` 展示 UI 错误。
**Decision**: Locked.
**Constraint**: MUST validate reduction count as a positive integer before mutation.

### Q3.2: 当前提交指针

**Question**: 降低后是否清空或改写 `current_last_entries` / `current_committed_entries`？
**Answer**: 不清空、不改写。它们只服务“当前输入最后一次结果”的替换语义；手动降低是对统计摘要的校准，不应破坏现有同输入重提逻辑。
**Evidence**: `内容抽取.py:381-404` 的替换提交逻辑依赖两个字段判断是否需要撤销旧提交。
**Decision**: Locked.
**Constraint**: MUST preserve `current_last_entries`, `current_committed_entries`, and `current_input_hash` during manual reduction.

---

## Synthesis

### Decision Summary

| # | Decision | Status | Branch | RFC 2119 |
|---|----------|--------|--------|----------|
| 1 | 手动降低不自动提交当前暂存结果 | Locked | Scope | MUST NOT auto-submit `current_last_entries` |
| 2 | UI 使用一个按钮 + 弹窗内极性单选 + 次数输入 | Locked | Scope | MUST expose one manual reduction button |
| 3 | 只修改 `expression_stats.committed_counts` | Locked | Data | MUST NOT mutate `expression_pools` |
| 4 | 默认作用于所选极性的全部正式类别 | Locked | Data | MUST apply to all categories in selected polarity |
| 5 | 次数必须是正整数 | Locked | Edge | MUST validate positive integer |
| 6 | 保留当前输入提交指针 | Locked | Edge | MUST preserve current tracking fields |

### Risk Register

| # | Risk | Branch | Severity | Mitigation |
|---|------|--------|----------|------------|
| 1 | 新按钮改变表情区按钮顺序文档 | Scope | Medium | 同步更新 `Game content extraction/agents.md` 和 `README.md` |
| 2 | 用户降低后又提交当前暂存结果，统计可能再次增加 | Scope | Low | 这是现有提交语义；按钮文案和实现不做隐式提交 |

### Recommended Next Step

Scope is clear; implement directly in `Game content extraction/内容抽取.py` with focused tests in `test_expression_enhancement.py` and document updates.
