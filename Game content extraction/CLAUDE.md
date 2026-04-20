# 项目说明

这是一个基于 `tkinter` 的中文桌面工具，用来快速生成“主图内容/场景内容”抽取结果。核心目标是：按盲盒编号抽取物品，按动物类型抽取动物内容，输出可直接复制的中文提示词，并通过历史机制降低重复。

人物表情抽取窗口已完成规格化与实现，位置：

- `../.workflow/.spec/SPEC-2026-04-20-game-content-extraction-人物表情抽取窗口/`
- `../.workflow/active/WFS-game-content-expression-window/`

维护前优先读规格包的 `spec-summary.md`、`requirements/_index.md`、`architecture/_index.md`、`epics/_index.md`，再读 workflow 的 `IMPL_PLAN.md`、`TODO_LIST.md`、`.task/IMPL-*.json`、`.process/PLAN_VERIFICATION.md` 和 `.process/verify_expression.py`。

UI 改版已完成分析与规划但尚未执行，位置：

- `../.workflow/.analysis/ANL-2026-04-20-game-content-extraction-ui-redesign/`
- `../.workflow/active/WFS-game-content-ui-redesign/`

执行 UI 改版前先读 `IMPL_PLAN.md`、`TODO_LIST.md`、`.task/IMPL-*.json`、`.process/context-package.json` 和 `.process/PLAN_VERIFICATION.md`；质量门为 `PROCEED_WITH_CAUTION`，建议按任务顺序执行。

## 当前功能

- 图形界面输入盲盒编号和动物类型。
- 主界面按钮 `人物表情抽取` 可打开独立表情抽取窗口。
- 支持多个盲盒编号，程序随机选中一个盲盒。
- 支持物品类别、动物内容类别开关和数量设置。
- 支持“物品状态词 + 物品名”组合输出。
- 支持输入附加指令：禁用某类内容、调整某类抽取数量。
- 支持复制结果、清空输入、自动粘贴。

## 待执行 UI 改版规划

目标：把当前“主窗口盲盒/动物 + 人物表情 `Toplevel`”改为单主窗口双工作区。

- 顶部两个切换按钮：`盲盒物品/动物抽取`、`人物表情抽取`。
- 默认显示盲盒物品/动物抽取；点击人物表情后在同一主窗口切换内容，不再默认弹出独立窗口。
- 保留现有业务逻辑、输入语法、历史机制、表情库解析、模板编号、重复增强替换和验证样例。
- 参考 `../UI风格参考.png` 做轻量 Tkinter 转译：浅灰蓝背景、白色内容区、蓝色主操作、胶囊式切换、宽松间距。
- 第一版不引入第三方 UI 依赖，不追求完整阴影、真实圆角或像素级复刻。

实现建议：

1. `setup_ui()` 只负责主壳、样式、切换按钮和工作区容器。
2. 盲盒/动物控件迁入 `build_blind_box_workspace(parent)`，保留 `input_entry`、`state_var`、`category_vars`、`category_spin_vars`、`animal_vars`、`animal_spin_vars`、`auto_paste_var`、`output_text`。
3. 表情控件迁入 `build_expression_workspace(parent)`，保留 `expression_input_text`、`expression_output_text`、`expression_template_mode_var`、`expression_template_index_var`。
4. `open_expression_window()` 可改为兼容薄包装：切换到人物表情工作区并聚焦输入框。
5. 两个工作区建议持久存在，切换时隐藏/显示，不要反复销毁控件。

## 历史机制

- 历史文件：`draw_history.json`。
- 物品池 key：`box:{box_id}:{category_key}`。
- 动物池 key：`animal:{animal_type}:{category_key}`。
- 每个池记录 `seen_in_cycle` 和 `cooldown`。
- 抽中过的内容会临时降权；一轮基本跑完后自动开启下一轮。
- 输入新内容不会自动重置历史；程序重启后历史保留；只有重置按钮清空历史。
- 重置按钮语义固定：`重置物品历史` 只清物品，`重置动物历史` 只清动物，`重置全部历史` 同时清两者。

## 关键文件

- `内容抽取.py`：界面、输入解析、抽取逻辑、历史读写、按钮行为；当前人物表情窗口入口、`Toplevel` 和 `enhance_expression_text` 也在此文件；UI 改版后应成为主窗口双工作区。
- `data/blind_boxes.py`：盲盒物品数据常量 `BLIND_BOXES`。
- `data/animals.py`：动物数据常量 `ANIMALS`。
- `data/item_states.py`：物品状态词 `ITEM_STATE_GROUPS` 和权重 `ITEM_STATE_GROUP_WEIGHTS`。
- `draw_history.json`：物品池和动物池历史状态。
- `../组图 23 表情库.md`：人物表情抽取窗口的模板资料源。
- `内容抽取.spec`：PyInstaller 打包配置，`datas` 已包含 `../组图 23 表情库.md`。
- `../.workflow/active/WFS-game-content-expression-window/.process/verify_expression.py`：人物表情抽取轻量回归验证脚本。

## 输入格式

主输入框必须保持逗号分隔单行语法：

`盲盒编号[,盲盒编号2...][,动物类型][,子类指令1][,子类指令2...]`

规则：

- 至少一个盲盒编号，编号必须是数字。
- 可一次输入多个盲盒编号。
- 动物类型可选且最多一个：`无动物`、`地面动物`、`空中动物`、`水中动物`；未填默认 `无动物`。
- 禁用某类：`无` + 类别标签，如 `无大型物品`、`无动物用品`。
- 调整数量：`类别标签+数字` 或 `类别标签-数字`，如 `中型物品+1`、`动物本体-1`。
- 输入覆盖只影响本次抽取，不修改界面默认值，不清空历史。

合法示例：

- `1`
- `1,5`
- `1,地面动物`
- `1,5,地面动物,无大型物品,中型物品+1`

## 修改原则

- 保持现有用户使用方式、中文输出风格和复制即用的提示词风格。
- 不要改成 Web、数据库、服务端或大型工程。
- 不要改成英文界面。
- 不要删除盲盒/动物数据。
- 不要擅自修改输入语法、抽取历史、重置按钮语义或默认行为。
- 改内容优先看 `data/`；改 UI、解析、抽取算法、历史、输出格式才进入 `内容抽取.py`。
- 不要把 `data/` 拆得过碎，不要在 `data/` 中加入 UI、抽样逻辑或历史保存逻辑。

## 人物表情抽取窗口

目标：把 `组图 23 表情前置.md` 输出的表情组文本，自动补全为 `组图 23.md` 可用的眉 / 眼 / 嘴描述。

核心流程：

1. 用户粘贴表情组文本。
2. 工具读取 `极性`、`具体表情`、`单人/多人`。
3. 工具从 `../组图 23 表情库.md` 按 `极性 + 具体表情 + 单人/多人` 查模板。
4. 工具只把模板追加到 `具体表情:` 字段后，其他字段和顺序尽量保持原样。
5. 用户复制增强后的文本交给 `组图 23.md`。

已实现行为与约束：

- 使用独立 `Toplevel`，不复用现有盲盒/动物单行输入框。
- `组图 23 表情库.md` 是单一事实源；每类 1-4 为单人模板，5-8 为多人模板。
- 支持指定模板编号；随机只作为可选策略。
- UI 默认策略优先“指定模板编号”；验收样例必须能稳定选择模板编号 4。
- 支持同一输入中的多组 `极性:` 逐组回填。
- 重复增强不得堆叠多份 `眉/眼/嘴`；当前实现会替换同一 `具体表情:` 字段中已有模板。
- 第一版保留 `[目标物]`、`[证据物]`、`[对方人物]`、`[剧情食物]`、`[剧情小物]`，不自动替换。
- 不接入 `draw_history.json`，不影响物品和动物抽取历史。
- 只补全眉 / 眼 / 嘴文字，不修改人物姿态、头身朝向、四肢动作、衣领、头发或耳饰等提示词约束。

验收样例：

- 输入识别结果：`极性=负向`、`具体表情=困惑`、`单人/多人=单人`、`模板编号=4`
- 应追加：`眉：一侧眉尾抬起，另一侧眉尾压平；眼：一侧眼撑开看着[目标物]，另一侧眼半垂；嘴：一侧嘴巴闭住下压，另一侧嘴角收紧。`

维护入口：

1. 纯逻辑：`enhance_expression_text` 及其辅助方法负责字段解析、表情库解析、模板编号选择、原文局部回填。
2. UI：`open_expression_window`、`extract_expression_content`、`clear_expression_content`、`copy_expression_result` 负责独立窗口行为。
3. 打包：`内容抽取.spec` 的 `datas=[('../组图 23 表情库.md', '.')]` 已加入表情库；代码同时查源码根目录、程序相邻目录和 `_MEIPASS`。

必须覆盖的错误提示：

- 空输入或未粘贴表情组文本。
- 缺少 `极性`、`单人/多人` 或 `具体表情`。
- 表情类别不存在。
- 极性与表情类别错配。
- 模板编号越界。
- 表情库文件缺失或结构不符合预期。
- 多组输入处理失败。
- 重复增强检测或替换失败。

非目标：

- 不自动替换占位符。
- 不自动生成新表情类别。
- 不把表情模板复制成第二份长期维护数据，除非打包路径明确需要。
- 不把表情抽取结果写入 `draw_history.json`。

## AI 快速判断

1. 这是内容数据变化还是程序逻辑变化？
2. 内容变化是否只需要改 `data/`？
3. 是否会影响输入语法、抽取历史、按钮语义或输出格式？
4. 若涉及人物表情抽取，是否仍遵守 Markdown 单一事实源、原文局部回填、占位符保留和不接入历史机制？
5. 若涉及 UI 改版，是否遵守 `WFS-game-content-ui-redesign` 的双工作区计划，并保留现有实例属性名？
6. 改完表情抽取逻辑或 UI 入口后，运行 `python -B '..\.workflow\active\WFS-game-content-expression-window\.process\verify_expression.py'` 做回归；UI 改版还要运行 `python -m py_compile '内容抽取.py'` 并手动检查双按钮切换。
