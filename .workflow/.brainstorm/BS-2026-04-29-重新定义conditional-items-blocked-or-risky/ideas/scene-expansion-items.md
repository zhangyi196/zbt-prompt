# Idea: scene_expansion_items

## Definition

`scene_expansion_items` means 场景扩展物: medium-or-larger objects that do not require image anchors and do not need existing objects to be present, but naturally enrich the current scene.

It replaces `conditional_items`, `anchor_required_items`, `explicit_context_items`, and `safe_hanging_items` as the fourth content pool.

## Boundaries

Allowed:

- common scene enrichment objects
- medium-or-larger objects
- independently visible and circleable objects
- objects that make sense from the selected blind-box category alone

Not allowed:

- objects requiring visual anchors such as monitor, whiteboard, umbrella pole, wall hook, or visible side space
- thin/string/line-like objects
- tiny accessories
- traces, scratches, folds, edge lines, shadows, highlights
- transparent, reflective, glowing, or animal-body objects

## Examples

### 桌面+学习

- 核心物：硬壳笔记本、桌面文件架、书桌小白板
- 配套物：笔筒、资料夹、计时器
- 可见小物：一排彩色笔套、三块记号小卡
- 场景扩展物：桌面日历、桌面小风扇、护眼书架、桌面收纳抽屉

### 公园+野餐

- 核心物：格纹野餐垫、藤编食物篮、双层餐盒
- 配套物：餐具盒、保温水壶、杯架托盘
- 可见小物：三块三明治切块、一组水果叉盒
- 场景扩展物：折叠野餐桌、便携冷藏箱、户外收纳箱、野餐遮阳布

## Recommended Runtime Mapping

- `large`: `core_items + scene_expansion_items`
- `medium`: `support_items + core_items:first_6`
- `small`: `visible_small_items`
- `hanging`: avoid forced fill; only use high-quality scene expansion objects if they are not thin or anchor-dependent

## Acceptance

The fourth pool should increase variety without requiring image understanding. It should never become a dumping ground for conditional, hanging, risky, or tiny objects.
