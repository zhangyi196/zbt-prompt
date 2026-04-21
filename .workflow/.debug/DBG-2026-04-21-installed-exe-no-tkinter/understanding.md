# Understanding Document

**Session ID**: DBG-2026-04-21-installed-exe-no-tkinter
**Bug Description**: 安装后打开主窗口失败，入口第 1 行报 `ModuleNotFoundError: No module named 'tkinter'`
**Started**: 2026-04-21

---

## Exploration Timeline

### Iteration 1 - Initial Exploration

#### Current Understanding

- 报错发生在 `内容抽取.py` 第 1 行 `import tkinter as tk`，主窗口尚未初始化。
- 当前 `dist\内容抽取.exe` 的 PyInstaller 归档包含 `pyi_rth__tkinter`、`_tkinter.pyd`、`tcl86t.dll`、`tk86t.dll`。
- 旧安装包解出的 exe 只有约 9.15MB，归档中没有 `tkinter` / `_tkinter` / Tcl / Tk 条目。
- 因此用户安装后看到的错误来自安装包内嵌的旧坏 exe，而不是应用源码的运行逻辑。

#### Hypotheses Generated

- H1: 安装包携带了旧的坏 exe，缺少 Tk 运行时。已确认。
- H2: 当前 Python/Tk 安装损坏，导致 PyInstaller 排除 Tk。沙箱内复现过该误判；提权运行 `tkinter.Tk()` 正常，确认是沙箱文件访问限制导致。
- H3: spec 没有显式声明 Tk 子模块，未来构建可能在异常环境下静默漏收。已通过 hidden imports 加固。

### Iteration 2 - Resolution

#### Fix Applied

- 修改 `Game content extraction/内容抽取.spec`，显式加入 `tkinter`、`tkinter.filedialog`、`tkinter.messagebox`、`tkinter.scrolledtext`、`tkinter.ttk`。
- 在提权环境重新执行 `pyinstaller --clean --noconfirm "内容抽取.spec"`，避免沙箱误判 Tcl/Tk broken。
- 用 Inno Setup 重新生成 `release\GameContentExtraction-Setup-v0.1.2.exe`。

#### Verification Results

- `python -B -m py_compile '内容抽取.py'` 通过。
- `python -B -m py_compile 'image_fetcher_ui.py' 'file_batch_renamer.py'` 通过。
- `python -B -m unittest discover -s . -p 'test_*.py'` 通过，3 个测试 OK。
- 新 `dist\内容抽取.exe` 归档包含 Tk 运行时。
- 全新隔离目录安装后的 exe 归档包含 `pyi_rth__tkinter`、`_tkinter.pyd`、`tcl86t.dll`、`tk86t.dll`。
- 启动烟测打开主窗口标题 `游戏内容抽取软件`，未出现 `Unhandled exception in script`。

---

## Current Consolidated Understanding

### What We Know

- 根因是安装包内旧 exe 缺少 `tkinter` 相关归档项。
- 当前源码没有入口导入错误。
- 当前正确构建产物必须包含 `pyi_rth__tkinter`、`_tkinter.pyd`、`tcl86t.dll`、`tk86t.dll`。
- 在沙箱中运行 Tk/PyInstaller 会误报 Tcl/Tk broken；构建 GUI 包时需要提权环境。

### What Was Disproven

- ~~应用源码删除或改错了 `tkinter` 导入~~：源码导入正常。
- ~~本机 Python/Tk 安装真实损坏~~：提权环境 `tkinter.Tk()` 验证通过。

### Follow-Up

- 若要让 GitHub Release 用户下载到修复版，需要替换 `v0.1.2` 资产或按发布流程升到 `v0.1.3`。
