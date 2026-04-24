每次完成执行任务后，都要同步更新 `agents.md`、`CLAUDE.md`、`README.md`、`.gitignore` 文件。
若 `.gitignore` 命中已跟踪的缓存文件或构建缓存，必须同步执行取消跟踪清理，避免再次提交到仓库。

# 游戏内容抽取工具

本工具是基于 `tkinter` 的本地中文桌面应用，主窗口含四个工作区：

- `盲盒物品/动物抽取`：按盲盒编号抽取物品，可叠加动物类型。
- `人物表情抽取`：把 `具体表情` 类别补全为眉 / 眼 / 嘴描述。
- `图像抓取`：按参考目录奇数位置文件名，从目标图库复制同名文件到桌面 `图像抓取/`。
- `批量重命名`：批量重命名 `.txt` 文档和常见图像文件。

当前 `盲盒物品/动物抽取` 工作区采用左侧配置、右侧提示词输出的双栏布局，方便一边调参数一边查看结果。

核心功能不依赖 Web、数据库或服务端。更新检查启动后静默执行，只有发现新版时才显示右上角 `发现新版本` 按钮。

## 下载

当前发布版：`v0.1.2`

- Release 页面：<https://github.com/zhangyi196/zbt-prompt/releases/tag/v0.1.2>
- 安装包：`GameContentExtraction-Setup-v0.1.2.exe`
- 大小：`14,031,056` bytes
- SHA256：`1b6a32dc6947a554a7aa2dc8b0cf6293271740c4118e0df613c74dcf02f0d875`
- 安装器会显示安装路径选择页，可修改默认安装目录。

## 运行

```powershell
python 'Game content extraction\内容抽取.py'
```

或进入本目录：

```powershell
python '内容抽取.py'
```

## 盲盒物品/动物抽取

输入语法：

```text
盲盒编号[,盲盒编号2...][,动物类型][,子类指令1][,子类指令2...]
```

规则：

- 至少一个数字编号；多个编号会随机选中一个。
- 动物类型最多一个：`无动物`、`地面动物`、`空中动物`、`水中动物`；未填默认 `无动物`。
- 禁用类目：`无` + 类别标签，如 `无大型物品`、`无动物用品`。
- 数量调整：`类别标签+数字` 或 `类别标签-数字`，如 `中型物品+1`、`动物本体-1`。
- 输入覆盖只影响本次抽取，不改默认勾选和数量，不清空历史。

示例：

```text
1
1,5
1,地面动物
1,5,地面动物,无大型物品,中型物品+1
```

历史保存在 `draw_history.json`，只包含 `item_pools` 和 `animal_pools`。重置按钮分别清空物品、动物或全部抽取历史。

## 人物表情抽取

表情工作区读取 `极性`、`具体表情`、`单人/多人`，从 `../组图 23 表情库.md` 查模板，并只把眉 / 眼 / 嘴追加到 `具体表情:` 后。每类 8 条模板：1-4 单人，5-8 多人；可随机或指定编号。

核心规则：

- `组图 23 表情库.md` 是单一事实源。
- 支持同一输入中的多组 `极性:`。
- 重复增强会替换旧眉 / 眼 / 嘴，不会堆叠。
- “清空输入”只清空表情输入框，不清空输出框；若盲盒区“自动粘贴”处于开启状态，会像盲盒区一样把剪贴板内容回填到表情输入框，方便连续测试。
- 保留 `[目标物]`、`[证据物]`、`[对方人物]`、`[剧情食物]`、`[剧情小物]`。
- 不写入 `draw_history.json`，不影响盲盒/动物历史。

模板编号 `4` 的示例输出：

```text
具体表情: 困惑，眉：一侧眉尾抬起，另一侧眉尾压平；眼：一侧眼撑开看着[目标物]，另一侧眼半垂；嘴：一侧嘴巴闭住下压，另一侧嘴角收紧。
```

## 图像抓取

流程：

1. 文件夹1作为参考名单，读取非隐藏文件并排序。
2. 取奇数位置文件名，即内部切片 `valid_files[::2]`。
3. 文件夹2作为目标图库，查找同名文件。
4. 找到的文件复制到桌面 `图像抓取/`。

该功能只复制文件，不移动、不重命名、不删除源文件。

## 批量重命名

工作区包含两个 Tab：

- `文档命名 (Txt)`：扫描工作目录 `.txt`，按文件名括号内数字优先排序，输出 `[前缀][编号].txt`。
- `图像命名 (Images)`：扫描 `.png`、`.jpg`、`.jpeg`、`.webp`、`.bmp`、`.gif`，按文件名数字排序后按组重命名。

图像命名格式：

- 每组数量为 1：`[前缀][编号].[扩展名]`
- 每组数量大于 1：`[前缀][组编号]_([组内序号]).[扩展名]`

参数保存到 `config.json`（打包后为 exe 同目录），不写入 `draw_history.json`。目标文件已存在时跳过并写日志，不会静默覆盖。

## 数据与文件

- `内容抽取.py`：主程序。
- `image_fetcher_ui.py`：图像抓取规则来源和独立参考脚本。
- `file_batch_renamer.py`：批量重命名规则来源和独立参考脚本。
- `data/blind_boxes.py`、`data/animals.py`、`data/item_states.py`：抽取数据。
- `draw_history.json`：物品 / 动物抽取历史。
- `config.json`：批量重命名参数。
- `../组图 23 表情库.md`：表情模板源。
- `内容抽取.spec`：PyInstaller 打包配置。
- `installer.iss`：Inno Setup 安装包配置。

## 检查更新

程序后台读取：

```text
https://api.github.com/repos/zhangyi196/zbt-prompt/releases/latest
```

若 latest 返回 404，则回退：

```text
https://api.github.com/repos/zhangyi196/zbt-prompt/releases?per_page=20
```

当前版本写在 `内容抽取.py` 的 `APP_VERSION`。检查更新只比较 GitHub Release 版本并打开发布页，不自动下载、覆盖或重启。没有高于当前版本的 Release 时，更新按钮保持隐藏。

发布新版时：更新 `APP_VERSION` 和 `installer.iss` 输出名 -> 构建 exe -> 检查 exe 归档包含 `tkinter` / `_tkinter` / Tcl / Tk -> 生成安装包 -> 做启动/静默安装烟测 -> 创建更高 tag（如 `v0.1.3`）并上传安装包。

## 验证

```powershell
python -B -m py_compile 'Game content extraction\内容抽取.py'
python -B -m py_compile 'Game content extraction\image_fetcher_ui.py' 'Game content extraction\file_batch_renamer.py'
python -B '.workflow\active\WFS-game-content-expression-window\.process\verify_expression.py'
python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'
```

预期输出：

```text
expression acceptance checks passed
```

## 打包

在 `Game content extraction` 目录运行：

```powershell
pyinstaller --clean --noconfirm '内容抽取.spec'
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" 'installer.iss'
pyi-archive_viewer 'dist\内容抽取.exe' --list | Select-String -Pattern 'tkinter|_tkinter|tcl86t|tk86t'
```

打包配置已包含 `../组图 23 表情库.md`，并显式声明 `tkinter` 相关 hidden imports。程序会按源码目录、程序相邻目录和 `_MEIPASS` 查找表情库。发布前至少确认 `dist\内容抽取.exe` 可启动，并静默安装 `release\GameContentExtraction-Setup-v*.exe` 后启动安装目录中的 exe。若构建时出现 `tkinter installation is broken`，通常是受限环境无法读取 Python 的 Tcl/Tk 目录，应在可访问该目录的环境中重新构建。

## 维护注意

- 保持中文界面和中文输出。
- 不破坏盲盒/动物逗号输入语法。
- 不修改 `draw_history.json` 历史语义；不要把 `config.json` 混入其中。
- 不把人物表情接入物品/动物历史。
- 图像抓取只复制文件。
- 批量重命名必须保留目标文件存在时跳过的保护逻辑。
- 检查更新不写历史、不自动替换 exe。
- `data/` 只放数据，不加入 UI、抽样逻辑或历史保存逻辑。
- 改表情逻辑后运行回归脚本；改 UI 后至少运行 `py_compile`，环境允许时手动检查四个工作区。
