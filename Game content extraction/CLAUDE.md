每次完成执行任务后，都要同步更新 `agents.md`、`CLAUDE.md`、`README.md`、`.gitignore` 文件。
若 `.gitignore` 命中已跟踪的缓存文件或构建缓存，必须同步执行取消跟踪清理，避免再次提交到仓库。

# 项目说明

本目录是本地中文 `tkinter` 小工具集合。主入口 `内容抽取.py` 采用单窗口四工作区：`盲盒物品/动物抽取`、`人物表情抽取`、`图像抓取`、`批量重命名`。使用说明见 `README.md`。

## 关键文件

- `内容抽取.py`：主 UI、抽取逻辑、历史读写、表情增强、图像抓取、批量重命名、更新检查。
- `image_fetcher_ui.py`：图像奇数抓取规则来源；主窗口已内置同等功能。
- `file_batch_renamer.py`：批量重命名规则来源；主窗口已内置同等功能。
- `data/*.py`：盲盒、动物、物品状态词数据。
- `draw_history.json`：物品池、动物池和人物表情历史；表情只写独立 `expression_pools`，不得混入 `item_pools` / `animal_pools`；重命名配置不得接入。
- `config.json`：批量重命名参数配置；不是抽取历史。
- `../组图 23.md`：差异迁移主提示词；当前为压缩结构版，维护时避免恢复重复表述；维护剧情字段时保持简短自然小剧情，不输出 `->` 箭头链路或用户原文复述；维护 List 2 时必须保留冷区避让、边角覆盖低于可执行性、新增物体空间可放置性、以及灯具照明关系不可被整体消失破坏的约束。
- `../组图 23 表情前置.md`：人物表情类别前置规则；人物块数量沿用单人 1 个、多人 2-3 个，每块 `具体表情` 一栏写 4 个同极性类别；人物块字段值必须是纯文本，不得把 `极性`、`具体表情`、`单人/多人` 等值包进 `[]`。
- `../组图 23 表情库.md`：人物表情模板单一事实源。
- `内容抽取.spec` / `installer.iss`：PyInstaller 与 Inno Setup 打包配置。

## 主 UI

`setup_ui()` 创建主壳、切换栏和工作区容器；各工作区由 `_build_blind_box_workspace()`、`_build_expression_workspace()`、`_build_image_fetcher_workspace()`、`_build_renamer_workspace()` 构建。`open_expression_window()` 仅兼容旧调用，切到表情工作区并聚焦输入框。

维护时保留主要实例属性：`input_entry`、`output_text`、`category_vars`、`animal_vars`、`expression_input_text`、`expression_output_text`、`image_fetcher_folder1_var`、`image_fetcher_folder2_var`、`renamer_work_dir_var`、`txt_*_var`、`img_*_var`。

UI 只用原生 `tkinter/ttk`，保持浅灰蓝背景、白色内容区、蓝色主操作、胶囊切换和宽松间距；不要引入第三方 UI 依赖。
`盲盒物品/动物抽取` 工作区保持左侧配置、右侧结果的双栏结构；优先让输出框常驻可见，不要再改回单列后把结果区压到底部。
表情区“清空输入”与盲盒区共用同一套清空逻辑：只清输入、不清输出；若“自动粘贴”开启，清空后回填当前剪贴板文本。

## 盲盒 / 动物抽取

输入保持单行逗号语法：

`盲盒编号[,盲盒编号2...][,动物类型][,子类指令1][,子类指令2...]`

规则：至少一个数字编号；动物类型最多一个：`无动物`、`地面动物`、`空中动物`、`水中动物`；禁用类目写 `无大型物品`、`无动物用品`；数量调整写 `中型物品+1`、`动物本体-1`。输入覆盖只影响本次抽取，不改默认值，不清空历史。

`draw_history.json` 中物品池 key 为 `box:{box_id}:{category_key}`，动物池 key 为 `animal:{animal_type}:{category_key}`。人物表情历史独立写入 `expression_pools`，类别 key 为 `expression_category:{极性}:{单人/多人}`，模板 key 为 `expression_template:{极性}:{单人/多人}:{具体表情}`；旧历史缺少该字段时自动创建。只有界面重置按钮清空对应历史。

## 人物表情抽取

流程：逐个人物块读取 `极性`、`具体表情`、`单人/多人` -> 从 `../组图 23 表情库.md` 查模板 -> 只增强 `具体表情:` 字段。前置提示词可在同一 `具体表情` 一栏给出 4 个候选类别；App 支持用 `、`、`，`、`,`、`/`、`|` 分隔候选，先校验候选都存在且极性一致，再按历史降权随机择一类别补全。每类模板分为单人 1-8、多人 1-8，强度从中等可见起步，不保留轻微档；默认随机模板同样按历史降权选择，可指定编号。

约束：`极性` 必须匹配 `具体表情` 类别；多人块写“多人”以使用多人模板池。前置输出的 `具体表情` 字段必须是纯类别名，如 `具体表情: 意外满意`，不得写成 `具体表情: [意外满意]`。若同栏给出多个候选，最终输出只保留随机选中的 1 个类别及其眉 / 眼 / 嘴描述，不回写整串候选；单一类别和指定模板编号不随机，但增强成功后仍记录历史。保留 `[目标物]`、`[证据物]`、`[对方人物]`、`[剧情食物]`、`[剧情小物]`；只补眉 / 眼 / 嘴，不改人物姿态、头身朝向、四肢、衣领、头发、耳饰；重复增强必须替换旧眉/眼/嘴，不得堆叠。

UI 约束：表情工作区的“清空输入”按钮只清空输入框，不清空输出框，便于保留上一轮增强结果做对照。

验收样例：`极性=负向`、`具体表情=困惑`、`单人/多人=单人`、`模板编号=4` 应追加：

`眉：一侧眉尾抬起，另一侧眉尾压平；眼：一侧眼撑开看着[目标物]，另一侧眼半垂；嘴：一侧嘴巴闭住下压，另一侧嘴角收紧。`

## 图像抓取

`图像抓取` 工作区提供文件夹1（参考名单）和文件夹2（目标图库）。程序读取文件夹1中非隐藏文件并排序，取奇数位置文件名（`valid_files[::2]`），再从文件夹2复制同名文件到桌面 `图像抓取/`。

维护约束：只复制，不移动、不重命名、不删除源文件；保留成功 / 未找到统计和日志；不要改成递归扫描或自动覆盖主流程。

## 批量重命名

`批量重命名` 工作区含 `文档命名 (Txt)`、`图像命名 (Images)` 两个 Tab。参数保存到脚本 / exe 同目录 `config.json`，不得混入 `draw_history.json`。

规则：`.txt` 文件按括号内数字优先排序，找不到则取文件名第一个数字，输出 `[前缀][编号].txt`。图像支持 `.png`、`.jpg`、`.jpeg`、`.webp`、`.bmp`、`.gif`，按文件名数字排序；每组数量大于 1 输出 `[前缀][组编号]_([组内序号]).扩展名`，等于 1 输出 `[前缀][编号].扩展名`。

安全约束：目标文件已存在且不是当前文件时必须跳过并记录日志；不得静默覆盖、删除文件、递归处理子目录或改写不支持的扩展名。保留输入校验：起始编号非负、编号位数 1-10、每组数量大于 0。

## 检查更新与发布

`APP_VERSION = "0.1.4"`；`UPDATE_API_URL` 读 latest release，404 时回退 `UPDATE_RELEASES_LIST_API_URL`。只有发现高于当前版本的 Release 才显示右上角 `发现新版本` 按钮；点击后只提示并打开 Releases 页面。不得自动下载、覆盖 exe、重启程序、写入 `draw_history.json` 或阻塞 UI。

更新检查依赖无认证 GitHub API，因此 release 所在仓库必须保持 public；仓库 private 时旧版安装包会收到 404，静默检查不会显示更新按钮。无认证 API 若返回 403 rate limit exceeded，需等 GitHub 返回的 reset 时间后再检查。

已发布：`v0.1.4` -> <https://github.com/zhangyi196/zbt-prompt/releases/tag/v0.1.4>；资产 `GameContentExtraction-Setup-v0.1.4.exe`，大小 `14,037,509` bytes，SHA256 `e3174f9e02e3631a5859ff3e041f06408771998964f10d0967c8a3db93b04098`。安装器会显示安装路径选择页。

发新版：先更新 `APP_VERSION` 和 `installer.iss` 的 `MyAppVersion` / `MyOutputName`，再构建 exe、生成安装包、检查 PyInstaller 归档包含 `pyi_rth__tkinter`、`_tkinter.pyd`、`tcl86t.dll`、`tk86t.dll`，做启动与静默安装烟测，最后创建更高 tag。若未来做自动更新，必须新增独立 updater/helper、校验和失败回滚。

## 修改原则

- 保持中文界面、中文输出和复制即用风格。
- 不改成 Web、数据库、服务端或大型工程。
- 不破坏输入语法、历史语义、重置按钮语义、表情库单一事实源和占位符保留。
- 若同步维护 `../组图 23.md`，剧情字段要改写为短小自然句；新增 / 异物植入 / 替换为更大物体必须有完整可见且未被占用的空间，不能为了容纳差异点缩小、移动、遮挡或重排原图主体；灯具、灯罩、灯泡、蜡烛火焰等不得整体消失导致光照关系变化。
- `data/` 不加入 UI、抽样逻辑或历史保存逻辑。

验证：

```powershell
python -B -m py_compile '内容抽取.py'
python -B -m py_compile 'image_fetcher_ui.py' 'file_batch_renamer.py'
python -B '..\.workflow\active\WFS-game-content-expression-window\.process\verify_expression.py'
python -B -m unittest discover -s . -p 'test_*.py'
```

打包：

```powershell
pyinstaller --clean --noconfirm '内容抽取.spec'
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" 'installer.iss'
pyi-archive_viewer 'dist\内容抽取.exe' --list | Select-String -Pattern 'tkinter|_tkinter|tcl86t|tk86t'
```

环境允许时，手动打开窗口检查四个工作区切换、中文显示和主按钮状态；发 Release 前还要启动 `dist\内容抽取.exe`，并静默安装 `release\GameContentExtraction-Setup-v*.exe` 后启动安装目录中的 exe。若沙箱内构建误报 `tkinter installation is broken` 或生成缺 Tk 的 exe，改用可读取本机 Python Tcl/Tk 目录的提权环境，并在命令前设置 UTF-8 控制台。
