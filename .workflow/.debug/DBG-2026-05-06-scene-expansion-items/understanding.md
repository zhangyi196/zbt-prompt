# Understanding Document

**Session ID**: DBG-2026-05-06-scene-expansion-items
**Bug Description**: `Game content extraction/内容抽取.py` 测试时无法抽取到 `scene_expansion_items`
**Started**: 2026-05-06T15:00:00+08:00

---

## Exploration Timeline

### Iteration 1 - Initial Exploration (2026-05-06 15:10)

#### Current Understanding

- 数据层 `Game content extraction/data/blind_boxes.py` 已稳定维护四池：`core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`。
- `内容抽取.py` 仍然只以 `large`、`medium`、`small`、`hanging` 作为抽取类别。
- 第四池没有直接抽取入口，测试时只能依赖旧 `large` 兼容桶被动命中。

#### Evidence from Code Search

- `BlindBoxExtractor.category_info` 仍定义为旧四栏。
- `_extract_box_items()` 直接从 `box[key]` 取值，无法访问四池事实源。
- `BLIND_BOXES` 兼容视图会把 `scene_expansion_items` 合并进 `large`，但 `hanging` 为空。

#### Hypotheses Generated

- H1: `scene_expansion_items` 数据本身缺失。
- H2: 抽取逻辑仍绑定旧兼容桶，第四池没有真实入口。
- H3: 历史池或冷却逻辑导致第四池被过滤掉。

### Iteration 2 - Evidence Analysis (2026-05-06 15:30)

#### Log Analysis Results

- **H1**: REJECTED
  - 证据：`BLIND_BOX_ITEM_POOL_BUNDLES` 的 20 个场景都保留 `scene_expansion_items`，且每池 50 条。
- **H2**: CONFIRMED
  - 证据：`内容抽取.py` 只认旧四栏；直接复现表明 `large` 内虽混有第四池内容，但用户无法单独抽取第四池。
- **H3**: REJECTED
  - 证据：历史池抽样复现可以从 `large` 命中第四池项，说明不是冷却逻辑吞掉了数据。

#### Corrected Understanding

- ~~第四池数据丢失~~ -> 第四池数据存在，但 UI 和抽取逻辑没有直接接入四池事实源。
  - Why wrong: 初始现象像“抽不到”，但运行时兼容桶实际仍包含第四池内容。
  - Evidence: `BLIND_BOXES[1]["large"]` 同时含有 `core_items` 与 `scene_expansion_items`。

#### Root Cause Identified

**H2**: `内容抽取.py` 仍按旧兼容桶抽取，`scene_expansion_items` 没有独立入口。

### Iteration 3 - Resolution (2026-05-06 15:45)

#### Fix Applied

- Modified files: `Game content extraction/内容抽取.py`, `Game content extraction/test_blind_box_content_model.py`, `Game content extraction/README.md`, `Game content extraction/agents.md`
- Fix description:
  - 将抽取工作区的四个类别切换为四池事实源。
  - 新增 `_get_box_item_sources()`，优先从 `BLIND_BOX_ITEM_POOL_BUNDLES` 读取四池。
  - 保留 `大型物品` / `中型物品` 等旧输入别名兼容。
  - 新增回归测试，确保第四池可定位、可抽取。
- Root cause addressed: 第四池仅存在于旧兼容视图，没有被抽取工作区直接消费。

#### Verification Results

- `python -B -m py_compile 'Game content extraction\内容抽取.py' 'Game content extraction\data\blind_boxes.py' 'Game content extraction\test_blind_box_content_model.py'`
- `python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'`
- 结果：31 个测试全部通过。

#### Lessons Learned

1. 四池数据结构升级后，UI 和抽取入口如果继续停留在兼容视图，就会出现“数据在，但用不到”的假性缺失。
2. 兼容桶适合保旧接口，不适合承担新事实源的唯一访问路径。
3. 第四池这类语义变化大的字段，需要专门的抽取回归测试，而不只是结构校验。

---

## Current Consolidated Understanding

### What We Know

- `scene_expansion_items` 数据没有缺失。
- 问题根因是 `内容抽取.py` 没有直接消费四池事实源。
- 修复后抽取工作区可以直接抽取第四池，且现有单测全部通过。

### What Was Disproven

- ~~第四池写库失败~~
- ~~历史池冷却机制导致第四池不可抽取~~

### Current Investigation Focus

验证用户在实际 GUI 操作中，是否能稳定看到“场景扩展物”抽取结果。
