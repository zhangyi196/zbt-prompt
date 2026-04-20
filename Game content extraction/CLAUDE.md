# 项目说明

这是一个本地中文 `tkinter` 桌面工具，用于生成主图 / 场景抽取结果：按盲盒编号抽物品，按动物类型抽动物内容，并把人物表情类别补全为眉 / 眼 / 嘴描述。使用说明见 `README.md`。

## 当前功能

- 主窗口双工作区：`盲盒物品/动物抽取`、`人物表情抽取`。
- 默认显示盲盒/动物；人物表情在同一主窗口切换，不再默认弹出独立 `Toplevel`。
- 支持多个盲盒编号随机选中、物品/动物类别开关、数量设置、物品状态词、复制、清空、自动粘贴。
- 支持输入指令禁用某类或调整某类数量。

## 关键文件

- `内容抽取.py`：UI、输入解析、抽取逻辑、历史读写、双工作区、表情增强。
- `data/blind_boxes.py`：盲盒物品数据。
- `data/animals.py`：动物内容数据。
- `data/item_states.py`：物品状态词与权重。
- `draw_history.json`：物品池和动物池历史。
- `../组图 23 表情库.md`：人物表情模板单一事实源。
- `内容抽取.spec`：PyInstaller 配置，已包含 `../组图 23 表情库.md`。

参考文档 / 工作流：

- `README.md`：用户说明。
- `../.workflow/active/WFS-game-content-expression-window/.process/verify_expression.py`：表情回归脚本。
- `../.workflow/active/WFS-game-content-ui-redesign/`：双工作区 UI 改版计划与记录。

## 输入格式

盲盒/动物输入必须保持单行逗号语法：

`盲盒编号[,盲盒编号2...][,动物类型][,子类指令1][,子类指令2...]`

规则：至少一个数字编号；动物类型最多一个：`无动物`、`地面动物`、`空中动物`、`水中动物`；未填默认 `无动物`。禁用类目写 `无大型物品`、`无动物用品`；数量调整写 `中型物品+1`、`动物本体-1`。输入覆盖只影响本次抽取，不改默认值，不清空历史。

## 历史机制

历史文件是 `draw_history.json`。物品池 key 为 `box:{box_id}:{category_key}`，动物池 key 为 `animal:{animal_type}:{category_key}`。抽中过的内容临时降权，一轮基本跑完后进入下一轮。只有界面重置按钮清空历史：`重置物品历史`、`重置动物历史`、`重置全部历史` 语义不得改变。人物表情抽取不得写入历史。

## 双工作区 UI

`setup_ui()` 建主壳、样式、顶部切换按钮和工作区容器；`_build_blind_box_workspace(parent)` 建盲盒/动物控件；`_build_expression_workspace(parent)` 建表情控件；`open_expression_window()` 仅兼容旧调用，切换到表情工作区并聚焦输入框。

维护时保留实例属性名：`input_entry`、`state_var`、`category_vars`、`category_spin_vars`、`animal_vars`、`animal_spin_vars`、`auto_paste_var`、`output_text`、`expression_input_text`、`expression_output_text`、`expression_template_mode_var`、`expression_template_index_var`。

UI 风格只做原生 `tkinter/ttk` 轻量转译：浅灰蓝背景、白色内容区、蓝色主操作、胶囊切换、宽松间距；不要引入第三方 UI 依赖。

## 人物表情抽取

目标：把 `组图 23 表情前置.md` 输出的表情组文本补全为 `组图 23.md` 可用描述。

流程：读取 `极性`、`具体表情`、`单人/多人` -> 从 `../组图 23 表情库.md` 查模板 -> 只增强 `具体表情:` 字段。每类模板 8 条：1-4 单人，5-8 多人；默认指定编号 4，可随机。支持多组 `极性:`；重复增强必须替换旧眉/眼/嘴，不得堆叠。

约束：保留 `[目标物]`、`[证据物]`、`[对方人物]`、`[剧情食物]`、`[剧情小物]`，不自动替换；只补眉 / 眼 / 嘴，不改人物姿态、头身朝向、四肢、衣领、头发、耳饰；不接入 `draw_history.json`。

验收样例：`极性=负向`、`具体表情=困惑`、`单人/多人=单人`、`模板编号=4` 应追加：

`眉：一侧眉尾抬起，另一侧眉尾压平；眼：一侧眼撑开看着[目标物]，另一侧眼半垂；嘴：一侧嘴巴闭住下压，另一侧嘴角收紧。`

## 修改原则

- 保持中文界面、中文输出和复制即用风格。
- 不改成 Web、数据库、服务端或大型工程。
- 不删除盲盒/动物数据；内容变更优先改 `data/`。
- 不破坏输入语法、历史语义、重置按钮语义、表情库单一事实源和占位符保留。
- `data/` 不加入 UI、抽样逻辑或历史保存逻辑。

验证：

```powershell
python -B -m py_compile '内容抽取.py'
python -B '..\.workflow\active\WFS-game-content-expression-window\.process\verify_expression.py'
```

环境允许时，手动打开窗口检查两个工作区切换、中文显示和主按钮状态。
