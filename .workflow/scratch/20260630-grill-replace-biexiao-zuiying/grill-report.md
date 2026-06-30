# Grill Report: 替换正向表情“憋笑嘴硬”

**Session**: GRL-003
**Depth**: shallow (3 branches)
**Date**: 2026-06-30T15:50:00+08:00
**Upstream**: user request

## Discovery Summary

### Project Context

- `组图 23 表情库.md` 是人物表情模板事实源，当前声明为正向 24 类、负向 24 类。
- `prompts/2.group-image/组图 23 表情前置.md` 的 `正向类别` 行必须与表情库类别一致。
- `Game content extraction/test_expression_enhancement.py` 中 `test_front_prompt_categories_match_expression_library` 会校验前置提示词类别顺序等于表情库顺序。
- 每次修改表情库后，需要追加 `组图 23 表情库 版本管理.md` 记录。
- 当前工作区存在未提交的 `.workflow` 索引和一个未跟踪根目录文档，本次不得误纳入。

### Codebase Surface

- `组图 23 表情库.md:771` 定义 `### 23. 憋笑嘴硬`，含适用场景、8 个具体表情变体、单人 8 条模板、多人 8 条模板。
- `prompts/2.group-image/组图 23 表情前置.md:51` 的正向类别列表包含 `憋笑嘴硬`。
- `表情库 2.0.0版本.md:63` 和 `美式卡通具体表情写法.md:169`、`:205` 是草案 / 方法文档中的旧分类参考，并非 App 直接事实源。

### Upstream Material

用户反馈：正向表情中 `憋笑嘴硬` 很少用到，想把它替换。

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

### Q1.1: 替换粒度

**Question**: 你说“把憋笑嘴硬进行替换”，这里是要替换整个顶层类别名和它的 16 条单人/多人模板，还是只保留类别名但改写它的适用场景和具体模板，让它更容易被前置选中？
**Evidence**: `组图 23 表情库.md:771-803` 是完整类别块；`prompts/2.group-image/组图 23 表情前置.md:51` 直接引用类别名；测试会校验前置类别列表和表情库顺序一致。
**Answer**: 替换 `憋笑嘴硬` 的整个顶层类别。
**Decision**: Locked.
**Constraint**: MUST remove `憋笑嘴硬` as a formal positive category and replace it with a new positive category across the expression library and front prompt category list.
**Risk**: 替换类别名后，需要同步处理前置提示词、版本记录和测试；本地历史 / 统计文件中的旧类别名属于用户数据，不能在仓库内硬改。

### Q1.2: 新类别定位

**Question**: 新的正向类别要叫什么、承担什么反馈功能？从现有正向表看，`憋笑嘴硬` 与 `忍笑`、`偷乐憋笑`、`眯眼坏笑` 明显重叠，建议换成更常见且不重叠的 `松口气`：用于“危险解除、误会化解、终于过关、紧张后放松”的正向反馈。是否用 `松口气` 替换？
**Evidence**: `组图 23 表情库.md:771-803`；`prompts/2.group-image/组图 23 表情前置.md:51`；现有正向类别中已有多个藏笑 / 坏笑类。
**Answer**: 使用 `松口气` 替换。
**Decision**: Locked.
**Constraint**: MUST replace positive category 23 with `松口气`, keeping the positive category count at 24 and preserving the category position.
**Risk**: `松口气` 需要避免写成负向惊吓后遗症；模板应以正向放松、确认安全、终于过关为主，汗点只能作为残留紧张的辅助。

---

## Branch 2: Data Model & State

**Status**: Completed
**Questions asked**: 2
**Decisions locked**: 2

### Q2.1: 文件同步范围

**Question**: 哪些文件必须同步？
**Answer**: 必须同步 `组图 23 表情库.md`、`prompts/2.group-image/组图 23 表情前置.md`、`组图 23 表情库 版本管理.md`、`prompts/2.group-image/组图 23 表情前置 版本管理.md`。草案文件 `表情库 2.0.0版本.md` 和 `美式卡通具体表情写法.md` 也包含旧类别引用，应同步避免后续误导。
**Evidence**: `rg 憋笑嘴硬`。
**Decision**: Locked.
**Constraint**: MUST update all repository references that define or list the formal category.

### Q2.2: 历史用户数据

**Question**: 是否迁移本地 `draw_history.json` 或 `expression_stats.json` 中可能存在的旧类别？
**Answer**: 不迁移仓库内用户数据。表情库替换后，正式输入不再输出 `憋笑嘴硬`；本地历史属于运行时数据，不应在仓库修改中硬改。
**Evidence**: 工具规则规定 `draw_history.json.expression_pools` 和 `expression_stats.json` 是本地历史 / 统计文件。
**Decision**: Locked.
**Constraint**: MUST NOT edit runtime history/stat files for this library replacement.

---

## Branch 3: Edge Cases & Failure Modes

**Status**: Completed
**Questions asked**: 2
**Decisions locked**: 2

### Q3.1: 模板结构

**Question**: 新类别模板必须满足哪些结构？
**Answer**: `松口气` 必须保留 8 个具体表情变体、单人 1-8、多人 1-8；每条模板只写合法脸部字段，3-5 个字段，至少包含眼或嘴，不写姿态、身体动作、衣领、头发或耳饰。
**Evidence**: `组图 23 表情库.md` 顶部规则；`Game content extraction/test_expression_enhancement.py` 会校验正式库结构和字段。
**Decision**: Locked.
**Constraint**: MUST keep the official expression library structure valid.

### Q3.2: 重叠风险

**Question**: 如何避免新类别再次低频或与旧类别重叠？
**Answer**: `松口气` 主锚点固定为放松下来的眼神 + 轻吐气嘴，适用场景围绕“危险解除、误会化解、终于过关、紧张后放松”；不写偷笑、坏笑、嘴硬或藏笑。
**Evidence**: 现有 `忍笑`、`眯眼坏笑`、`偷乐憋笑` 已覆盖藏笑 / 坏笑。
**Decision**: Locked.
**Constraint**: MUST keep `松口气` semantically distinct from laughing/smirk categories.

---

## Synthesis

### Decision Summary

| # | Decision | Status | Branch | RFC 2119 |
|---|----------|--------|--------|----------|
| 1 | 替换整个 `憋笑嘴硬` 顶层类别 | Locked | Scope | MUST remove `憋笑嘴硬` |
| 2 | 新类别使用 `松口气` | Locked | Scope | MUST use `松口气` |
| 3 | 同步所有正式引用和版本记录 | Locked | Data | MUST update all formal references |
| 4 | 不迁移本地运行时历史 | Locked | Data | MUST NOT edit runtime history |
| 5 | 保持表情库结构合法 | Locked | Edge | MUST keep 8 + 8 + 8 structure |
| 6 | 避免藏笑 / 坏笑语义重叠 | Locked | Edge | MUST distinguish from laugh/smirk categories |

### Risk Register

| # | Risk | Branch | Severity | Mitigation |
|---|------|--------|----------|------------|
| 1 | 前置类别列表和表情库不一致导致 App 测试失败 | Data | High | 同步修改并运行 `test_expression_enhancement.py` |
| 2 | 新类别写成负向后怕表情 | Edge | Medium | 模板以放松、安心、吐气为主，只保留少量残留汗点 |

### Recommended Next Step

直接实施 `松口气` 替换，并运行表情库一致性测试。
