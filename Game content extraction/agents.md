每次完成会话后，同步检查本目录 `agents.md`、`README.md`，以及根目录 `agents.md`、`README.md`、`.gitignore` 是否需要随本次变更更新；这些文件必须保持精简，只记录稳定规则和必要入口。
若 `.gitignore` 命中已跟踪的缓存文件或构建缓存，必须同步取消跟踪清理。

# Game Content Extraction Guide

本目录是本地中文 `tkinter` 小工具。主入口 `内容抽取.py` 含四个工作区：`盲盒物品/动物抽取`、`人物表情抽取`、`图像抓取`、`批量重命名`。全仓提示词规则见上级目录 `agents.md`。

## 关键文件

- `内容抽取.py`：主 UI、抽取逻辑、历史读写、表情增强、图像抓取、批量重命名、更新检查。
- `data/blind_boxes.py`：盲盒 20 个 `场景+用途` 入口、四类内容池、四栏兼容映射和 `blocked_patterns`。
- `data/animals.py`、`data/item_states.py`：动物池和物品状态词；透明、反光、高光语义视为风险。
- `draw_history.json`：物品、动物和表情历史；表情只写 `expression_pools`。
- `config.json`：批量重命名参数；不得接入抽取历史。
- `data/agents.md`：盲盒四池物品写库规则；改盲盒内容前先读。
- `../主图 第一步.md`：与盲盒类别库保持同步，只输出类别编号和控制字段。
- `../组图 23 表情库.md`：人物表情模板单一事实源。
- `内容抽取.spec`、`installer.iss`：打包配置。

## UI 约束

- 只用原生 `tkinter/ttk`，不引入第三方 UI 依赖。
- 保持浅灰蓝背景、白色内容区、蓝色主操作、胶囊切换和宽松间距。
- `盲盒物品/动物抽取` 保持左侧配置、右侧结果的双栏结构，输出框常驻可见。
- 表情区“清空输入”只清输入、不清输出；若“自动粘贴”开启，清空后回填剪贴板文本。
- 保留主要实例属性：`input_entry`、`output_text`、`category_vars`、`animal_vars`、`expression_input_text`、`expression_output_text`、`image_fetcher_folder1_var`、`image_fetcher_folder2_var`、`renamer_work_dir_var`、`txt_*_var`、`img_*_var`。

## 盲盒 / 动物抽取

输入语法：`盲盒编号[,盲盒编号2...][,动物类型][,子类指令1][,子类指令2...]`

- 至少一个数字编号；动物类型最多一个：`无动物`、`地面动物`、`空中动物`、`水中动物`。
- 禁用类目写 `无大型物品`、`无动物用品`；数量调整写 `中型物品+1`、`动物本体-1`。
- 输入覆盖只影响本次抽取，不改默认值，不清空历史。
- 历史 key：物品 `box:{box_id}:{category_key}`，动物 `animal:{animal_type}:{category_key}`。

盲盒数据事实源：

- `BLIND_BOX_SCENE_ENTRIES`：20 个 `场景+用途` 入口。
- `BLIND_BOX_ITEM_POOL_BUNDLES`：四池模型，固定为 `core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`。
- `BLIND_BOXES`：运行时四栏兼容视图。
- `BLIND_BOX_COMPATIBILITY_MAPPING`：四池到 `large` / `medium` / `small` / `hanging` 的映射，`hanging` 当前为空兼容桶。

写库验收：每池 50 条且池内唯一；条目必须是真实可见、单点差异、边界清楚、可单独圈选的物品或成单位物品集合，禁止靠 `收纳盒`、`整理篮`、`展示架`、`托座`、`分装盒`、`组合` 等尾词批量扩写。同一基础对象不得在同一类别四池机械重复；若数量不足，优先扩展不同物品族，不用同质尾词凑数。生成时先按真实物品族选物，再检查反模板规则和尾词配额，避免 `功能词 + 板/盘/垫/盒/包/册/卷` 成片造词。禁止依赖光影、透明感、反光、高光、发光、细线或微型痕迹作为识别点；普通杯、瓶、罐可以写，但不得强调透明或反光特征。`conditional_items`、`anchor_required_items`、`blocked_or_risky` 不再作为候选池，风险内容只进 `blocked_patterns`。

四池书写规则：

- `core_items`：写主题核心主体物，必须一眼可识别、边界清楚、可单独圈选；允许少量真实容器，但容器类不应主导整池；禁止大量同物变体、抽象主题词和过小零散物。
- `support_items`：写配套工具物，包括工具、夹取器具、承托小器具、使用配件和操作辅助物；不得把 `core_items` 换小名重写一遍，也不得堆叠 `托座`、`分装盒`、`夹盒` 等同质尾词。
- `visible_small_items`：写成组可见小物，优先使用 `一盒`、`一包`、`一筒`、`一盘`、`一套`、`一卷`、`一束`、`一叠`；`一组` 只用于体量足够的物品；禁止单个微小物、碎屑、小点、刻痕、标签、价格签、文字卡和 `两枚` / `三枚` 微小物。
- `scene_expansion_items`：保留历史字段名，实际语义为可放置中型单物；写适合找不同新增、删除、替换的中型物品，不写 `A+B组合`、`用品组合`、`小物组合`、`包装组合`，不写推车、抽屉柜、陈列架、货架、书桌、柜台等大型家具 / 存储主体；先覆盖多个真实物品族，再控制 `板/盘/垫/盒/包/册/卷` 等尾词配额。

若改变盒号语义，必须同步 `../主图 第一步.md`。回归测试以 `test_blind_box_content_model.py` 为准。

## 人物表情抽取

流程：读取 `极性`、`具体表情`、`单人/多人` -> 从 `../组图 23 表情库.md` 查模板 -> 只增强 `具体表情:` 字段。

- `极性` 必须匹配 `具体表情` 类别；多人块写“多人”。
- `具体表情` 字段必须是纯类别名，不得写成 `[意外满意]`。
- 同栏多候选支持 `、`、`，`、`,`、`/`、`|`，校验后按历史降权随机选 1 个。
- 只补眉 / 眼 / 嘴；不改姿态、头身朝向、四肢、衣领、头发、耳饰。
- 重复增强必须替换旧眉 / 眼 / 嘴，不得堆叠。
- 表情历史 key：`expression_category:{极性}:{单人/多人}`、`expression_template:{极性}:{单人/多人}:{具体表情}`。

## 图像抓取与重命名

- 图像抓取：读取文件夹1非隐藏文件并排序，取 `valid_files[::2]`，从文件夹2复制同名文件到桌面 `图像抓取/`；只复制，不移动、不改名、不删除源文件。
- 批量重命名：参数保存到脚本 / exe 同目录 `config.json`；目标文件已存在且不是当前文件时必须跳过并记录日志；不得静默覆盖、删除文件、递归处理子目录或改写不支持的扩展名。
- `data/` 只放数据，不加入 UI、抽样逻辑或历史保存逻辑。

## 更新与发布

- `APP_VERSION = "0.1.4"`；已发布 `v0.1.4`，安装包 `GameContentExtraction-Setup-v0.1.4.exe`。
- 更新检查只提示并打开 Releases 页面；不得自动下载、覆盖 exe、重启程序、写入 `draw_history.json` 或阻塞 UI。
- Release 仓库需保持 public；无认证 GitHub API 限流时等待 reset 后重试。
- 发新版：更新 `APP_VERSION` 和 `installer.iss` 输出名 -> 构建 exe -> 检查 Tk 归档 -> 生成安装包 -> 启动 / 静默安装烟测 -> 创建更高 tag。

## 验证

```powershell
python -B -m py_compile '内容抽取.py'
python -B -m py_compile 'image_fetcher_ui.py' 'file_batch_renamer.py'
python -B -m unittest discover -s . -p 'test_*.py'
```

若 `.workflow\active\WFS-game-content-expression-window\.process\verify_expression.py` 仍存在，改表情逻辑后可额外运行该验收脚本。

## 打包

```powershell
pyinstaller --clean --noconfirm '内容抽取.spec'
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" 'installer.iss'
pyi-archive_viewer 'dist\内容抽取.exe' --list | Select-String -Pattern 'tkinter|_tkinter|tcl86t|tk86t'
```
