# Terminology

| Term | Definition | Code Reference | Status |
|------|------------|----------------|--------|
| 人物表情抽取 | 桌面工具中的表情工作区，读取极性、单人/多人和具体表情并写回增强文本。 | `Game content extraction/内容抽取.py:1659` | locked |
| 表情统计 | 独立 `expression_stats.json` 中的前置反馈统计，只用于摘要排序参考。 | `Game content extraction/内容抽取.py:235` | locked |
| committed_counts | 已提交实际使用结果的累计次数，按 `正向` / `负向` 分组。 | `Game content extraction/内容抽取.py:238` | locked |
| current_last_entries | 当前输入最后一次成功抽取的暂存结果。 | `Game content extraction/内容抽取.py:243` | locked |
| current_committed_entries | 当前输入已经提交进统计的结果，用于再次抽取后替换本组旧统计。 | `Game content extraction/内容抽取.py:244` | locked |
| 主动降低次数 | 用户通过手动按钮把所选极性的一组表情类别统计计数统一下调，计数不能低于 0。 | new | locked |
| 所有表情 | 所选极性下表情库中的全部正式类别；一次只作用正向或负向之一。 | `组图 23 表情库.md` | locked |
| 降低统计按钮 | 表情工作区新增的一个手动校准入口，点击后弹出极性单选和次数输入。 | new | locked |
