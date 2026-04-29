# Implementation Plan: Blind Box Pool Itemization Fix

## Objective

把三个盲盒试点的 `conditional_items` 与 `blocked_or_risky` 修正为“具体物品池”，并用测试防止折线、擦痕、气泡、阴影、边线、微小颗粒等非物品表达再次进入物品库。

## Scope

In scope:

- `桌面+学习`、`海底+潜水`、`公园+野餐` 三个试点盒。
- `conditional_items` 内容替换。
- `blocked_or_risky` 内容替换。
- forbidden pattern 单元测试。
- 项目文档同步。

Out of scope:

- 全量 20 类重写。
- UI、输入语法、历史文件、版本发布、安装包。
- 字段重命名或 runtime bucket contract 改动。

## Execution Order

### IMPL-1: 修正 conditional_items 为条件启用的具体物品

文件：`Game content extraction/data/blind_boxes.py`

将三个试点的 `conditional_items` 从偏小、依附式标签/夹子/边缘物，替换为中等体量或更大、边界清楚、可独立圈选、需要特定承载环境才适合启用的具体物品。

验收：

- 每个试点仍有非空 `conditional_items`。
- 条目是完整物品，不是痕迹、线条、边缘变化或微型附着件。
- 盒号 15/16/17 和四栏映射不变。

### IMPL-2: 修正 blocked_or_risky 为具体风险物

文件：`Game content extraction/data/blind_boxes.py`

替换 `blocked_or_risky` 中的非物品表达，保留“具体但默认不宜抽取”的风险对象，例如透明、反光、发光、动物本体、细长悬挂、过大或易误判对象。

验收：

- `blocked_or_risky` 条目均为具体对象。
- 不包含 `纸张边缘折线`、`微小擦痕`、`细小气泡串`、`漂浮细海草丝`、`海底阴影斑`、`水面高光`、`微小沙粒`、`草地碎叶点`、`地面细小石子`、`风吹纸片边缘`、`野餐垫边线`、`微小污点`。
- `blocked_or_risky` 仍不进入 `BLIND_BOXES` 默认四栏。

### IMPL-3: 增加 forbidden pattern 回归测试

文件：`Game content extraction/test_blind_box_content_model.py`

新增测试遍历三类试点五层池，禁止非物品表达进入任意池层。测试应该验证“禁用模式只作为校验规则存在，不是可抽数据”。

验收：

- 新测试覆盖所有 `BLIND_BOX_ITEM_POOL_BUNDLES` 的五层池。
- 现有 schema、runtime bucket、blocked leakage 测试继续保留。
- `python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'` 通过。

### IMPL-4: 同步文档和 workflow 状态

文件：

- `agents.md`
- `README.md`
- `Game content extraction/CLAUDE.md`
- `Game content extraction/README.md`
- `.gitignore`
- `.workflow/active/WFS-blind-box-pool-itemization-fix/TODO_LIST.md`

同步说明本次修正后的规则：所有池层只写具体物品；`conditional_items` 是可见、可圈选、条件启用物；`blocked_or_risky` 是具体风险物；非物品表达进入 forbidden pattern 测试。

验收：

- 文档不再停留在“待修正”状态。
- `.gitignore` 如无新增缓存规则需求则保持现有内容，不做无意义变动。
- TODO 状态随执行结果更新。

## Verification

执行阶段应运行：

```powershell
python -B -m py_compile 'Game content extraction\内容抽取.py' 'Game content extraction\data\blind_boxes.py'
python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'
```

## Dependencies

`IMPL-1` 和 `IMPL-2` 都修改同一数据块，建议顺序执行或由同一个执行者完成。`IMPL-3` 依赖前两项完成后再写断言。`IMPL-4` 最后执行。
