每次完成会话后，同步检查本目录 `agents.md`、`README.md`，以及根目录 `agents.md`、`README.md`、`.gitignore` 是否需要随本次变更更新；这些文件必须保持精简，只记录稳定规则和必要入口。
若 `.gitignore` 命中已跟踪的缓存文件或构建缓存，必须同步取消跟踪清理。

# Game Content Extraction Guide

本目录是本地中文 `tkinter` 小工具。主入口 `内容抽取.py` 含四个工作区：`盲盒物品/动物抽取`、`人物表情抽取`、`图像抓取`、`批量重命名`。全仓高层规则见上级 `../agents.md`。

## 关键文件

- `内容抽取.py`：主 UI、抽取逻辑、历史读写、表情增强、图像抓取、批量重命名、更新检查。
- `data/blind_boxes.py`：盲盒 20 个 `场景+用途` 入口、四池内容库和兼容映射。
- `data/animals.py`、`data/item_states.py`：动物池和物品状态词。
- `draw_history.json`：物品、动物和表情历史；表情只写 `expression_pools`。
- `config.json`：批量重命名参数；不得接入抽取历史。
- `data/agents.md`、`data/审查规则.md`、`data/审查文件.md`、`data/审查文件/{类别} 审查文档.md`、`data/修改规则.md`：盲盒写库、审查和修改规则；改盲盒内容前先读。
- `内容抽取.spec`、`installer.iss`：打包配置。

## UI 约束

- 只用原生 `tkinter/ttk`，不引入第三方 UI 依赖。
- 保持当前双栏信息结构和主要实例属性名稳定，避免打断现有事件绑定和测试脚本。
- 表情区“清空输入”只清输入，不清输出；若“自动粘贴”开启，清空后回填剪贴板文本。

## 盲盒 / 动物抽取

- 输入语法：`盲盒编号[,盲盒编号2...][,动物类型][,子类指令1][,子类指令2...]`。
- 至少一个数字编号；动物类型最多一个：`无动物`、`地面动物`、`空中动物`、`水中动物`。
- 禁用类目写 `无大型物品`、`无动物用品`；数量调整写 `中型物品+1`、`动物本体-1`。
- 输入覆盖只影响本次抽取，不改默认值，不清空历史。
- 盲盒写库以 `data/blind_boxes.py` 为唯一事实源；抽取逻辑优先直连四池事实源，不要把第四池重新并回兼容空桶。
- 改盲盒内容时，先看 `data/agents.md`、`审查规则.md`、对应类别审查文档和 `修改规则.md`；目标不是换词，而是解决场景错位、视觉本体重复、模板化和伪多样性；同族平移替换如 `作品记录本 -> 项目说明本` 不算修复。

## 人物表情抽取

- 流程：读取 `极性`、`具体表情`、`单人/多人`，再从 `../组图 23 表情库.md` 查模板；只增强 `具体表情:` 字段。
- 只补眉 / 眼 / 嘴；不改姿态、头身朝向、四肢、衣领、头发、耳饰。
- 同栏多候选支持 `、`、`，`、`,`、`/`、`|`；校验后按历史降权随机选 1 个。
- 表情历史只写 `expression_category:*` 和 `expression_template:*`。

## 图像抓取与重命名

- 图像抓取只复制，不移动、不改名、不删除源文件。
- 批量重命名参数保存到同目录 `config.json`。
- 目标文件已存在且不是当前文件时必须跳过并记录日志；不得静默覆盖、删除文件、递归处理子目录或改写不支持扩展名。
- `data/` 只放数据，不加入 UI、抽样逻辑或历史保存逻辑。

## 更新与发布

- 更新检查只提示并打开 Releases 页面；不得自动下载、覆盖 exe、重启程序、写入 `draw_history.json` 或阻塞 UI。
- 只有发布桌面工具新版本时，才更新 `APP_VERSION`、`installer.iss` 输出名和正式 tag。

## 验证

```powershell
python -B -m py_compile '内容抽取.py'
python -B -m py_compile 'image_fetcher_ui.py' 'file_batch_renamer.py'
python -B -m unittest discover -s . -p 'test_*.py'
```

盲盒内容改动还需额外运行：

```powershell
python -B 'test_blind_box_content_model.py'
```

## 打包

```powershell
pyinstaller --clean --noconfirm '内容抽取.spec'
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" 'installer.iss'
pyi-archive_viewer 'dist\内容抽取.exe' --list | Select-String -Pattern 'tkinter|_tkinter|tcl86t|tk86t'
```
