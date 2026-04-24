每次完成执行任务后，都要同步更新 `agents.md`、`CLAUDE.md`、`README.md`、`.gitignore` 文件。
若 `.gitignore` 命中已跟踪的缓存文件或构建缓存，必须同步执行取消跟踪清理，避免再次提交到仓库。

# Agents Guide

本仓库主要维护中文提示词规则；`Game content extraction/` 是配套本地 `tkinter` 小工具目录。优先局部修改，保持中文风格、固定输出、数量配额、自检项和既有链路。

## 文件职责

- `主图 第二步 .md`：候选物审核与摆放；用户给了候选就不得脑补新候选。
- `组图 4.md`：找不同润色；18 个差异点，九宫格每区 2 个，类型配额 3 / 6 / 3 / 3 / 3；禁灯光、明暗、反光、高光、阴影等变化。
- `组图 23 表情前置.md`：只产出负向、正向、正负向剧情表情类别和摘要；具体表情只写类别名；多人每组 2-3 人，正负向组允许人物块极性混合。
- `组图 23 表情库.md`：正向 25、负向 25；每类 8 条眉/眼/嘴模板，1-4 单人、5-8 多人；只写面部。
- `组图 23.md`：Ref-A/B 到 Target 差异迁移；固定六板块，List 1 / List 2 各 16 条；不得削弱 Ref 绑定、冷区避让、人物互斥和禁改规则。
- `Game content extraction/`：本地小工具；维护细节见同目录 `CLAUDE.md`，使用说明见 `README.md`。

## 通用不变量

- 禁止脑补不可见对象、画外空间、遮挡后区域或身份不稳定对象。
- 差异点遵守“一圈一物一变化”或“单一不同点”。
- 不改人物骨架、姿态、头身朝向、四肢动作或支撑关系。
- 不做灯光、发光、明暗、阴影、高光、反光、滤光、投影、镜面成像等变化。
- 不整体修改大面积背景、大物体主体或大面积表层。
- 位置字段只定位，不写颜色、材质、纹理、风格、明暗等外观修饰。
- 小变化不得升级为灾难、阴谋、案件、长期危机或大型事故。
- 中文文件用 UTF-8；中文路径命令使用引号或 `-LiteralPath`。

## `组图 23` 链路

流程：`组图 23 表情前置.md` 输出类别 -> App 按类别补全眉/眼/嘴 -> `组图 23.md` 按剧情适配完整差异。前置默认三组：负向组、正向组、正负向组；单人时正负向组不适用，多人时每组 2-3 人且正负向组至少 1 正 1 负。`组图 23.md` 只能以 Ref-A -> Ref-B 的真实可见变化为准；前置预案和用户表情描述只作参考。

人物规则：同一人物若改面部表情，不得再改衣领/领带/颈部、头发/头饰、耳饰/耳侧饰品。单人眼部回指 `[证据物]` / `[目标物]`；多人眼部可回指 `[对方人物]`，但 `[对方人物]` 不作嘴部承载物。每个人物块的 `极性` 必须匹配 `具体表情` 类别；嘴部承载物必须来自 Ref 明确可见且剧情需要的物体或状态。

## `Game content extraction` 摘要

- 四工作区：`盲盒物品/动物抽取`、`人物表情抽取`、`图像抓取`、`批量重命名`。
- `盲盒物品/动物抽取` 工作区采用左侧配置、右侧输出的双栏布局；修改该区 UI 时优先保持输出框常驻可见，不要把结果区重新压回页面底部。
- `人物表情抽取` 工作区的“清空输入”只清空输入框，不清空增强结果；若“自动粘贴”开启，清空后要像盲盒区一样回填当前剪贴板文本。
- 不改成 Web、数据库、服务端或大型工程；不引入第三方 UI 依赖。
- `draw_history.json` 只服务物品池和动物池；表情和重命名配置不得接入。
- `config.json` 只服务批量重命名。
- 当前版本 `APP_VERSION = "0.1.3"`；GitHub Release `v0.1.3` 已上传 `GameContentExtraction-Setup-v0.1.3.exe`，大小 `14,031,310` bytes，SHA256 `58a9a2ac27be4553c33caa247f59994dd9dca4bde55fe1d1864e7da388ce9ad4`；安装器会显示安装路径选择页。
- 更新检查只提示并打开 Releases 页面，不自动下载/替换 exe，不写历史；没有更高 Release 时隐藏更新按钮。
- 图像抓取只复制同名文件到桌面 `图像抓取/`，不移动、不改名、不删除源文件。
- 批量重命名必须保留目标文件存在时跳过的保护逻辑。
- 发新版先更新 `APP_VERSION` 和 `installer.iss` 输出名，再构建 exe、确认 PyInstaller 归档包含 `pyi_rth__tkinter` / `_tkinter.pyd` / `tcl86t.dll` / `tk86t.dll`，生成安装包、做启动/静默安装烟测，最后创建更高 tag。若沙箱内构建误报 `tkinter installation is broken`，用可读取 Python Tcl/Tk 目录的提权环境重建。

验证：

```powershell
python -B -m py_compile 'Game content extraction\内容抽取.py'
python -B -m py_compile 'Game content extraction\image_fetcher_ui.py' 'Game content extraction\file_batch_renamer.py'
python -B '.workflow\active\WFS-game-content-expression-window\.process\verify_expression.py'
python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'
```

## 修改检查

修改前读目标文件的角色、输入、输出和核心约束；修改中只动相关段落；修改后检查数量、格式、禁区、承载关系、固定输出和自检是否一致。涉及表情链路时，同步检查 `组图 23 表情库.md`、`组图 23 表情前置.md`、`组图 23.md` 与 App 接入关系。

## 仓库源码打包发布

- 仓库源码打包到 GitHub Release 时，使用保留目录结构的 zip 资产，不直接上传文件夹。
- 推荐 source-bundle tag：`v0.1.3-source-YYYYMMDD`；该命名规范化后仍为当前正式桌面版本，不会误触发 App 更新提示。
- 推荐 source-bundle 资产名：`zbt-prompt-v0.1.3-source-YYYYMMDD.zip`。
- 仅当发布桌面工具新版本时，才提升 `APP_VERSION`、安装包名和正式 `v0.1.x` tag。
