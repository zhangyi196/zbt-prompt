每次完成会话后，同步检查根目录 `agents.md`、`README.md`、`.gitignore`，以及涉及工具时的 `Game content extraction/agents.md`、`Game content extraction/README.md` 是否需要更新；这些文件只记录稳定规则和必要入口。
若 `.gitignore` 命中已跟踪的缓存或构建文件，必须同步取消跟踪清理。

# Agents Guide

本仓库维护中文提示词规则与配套桌面工具；根目录 `agents.md` 只做总导航，主图提示词细则收敛在 `prompts/main-image/agents.md`，`Game content extraction/` 工具细则见 `Game content extraction/agents.md`。

## 入口

- `prompts/main-image/agents.md`：主图 AI 提示词总入口。
- `prompts/main-image/主图 第一步.md`：判断 Target 是否需要新增内容；需要时只输出盲盒类别编号、动物字段、禁用字段和补偿字段。
- `prompts/main-image/主图 第二步 .md`：审核和摆放候选物；用户给了候选就不得脑补新候选，默认按稳定承载面上的可见物体处理。
- `prompts/group-image/agents.md`：组图 AI 提示词总入口。
- `prompts/group-image/组图 4.md`：18 个找不同差异点，九宫格每区 2 个。
- `prompts/group-image/组图 23.md`：Ref-A / Ref-B 到 Target 的差异迁移。
- `prompts/group-image/组图 23 表情前置.md`、`组图 23 表情库.md`：人物表情前置规则与事实源；其中表情库固定留在根目录。
- `Game content extraction/data/agents.md`、`审查规则.md`、`审查文件.md`、`审查文件/{类别} 审查文档.md`、`修改规则.md`、`全局重复词定位清单.md`：盲盒数据和审查 / 修改规则；改 `blind_boxes.py` 前先读。

## 全局硬规则

- 禁止脑补不可见对象、画外空间、遮挡后区域或身份不稳定对象。
- 差异点遵守“一圈一物一变化”；不得依赖细线、小点、刻痕、碎屑、污渍、标签或价格签。
- 不改人物骨架、姿态、头身朝向、四肢动作、支撑关系和贴邻热区。
- 不做灯光、发光、明暗、阴影、高光、反光、滤光、投影或镜面成像变化。
- 灯具、灯罩、灯泡、蜡烛火焰等照明对象不得整体消失、整体移动或替换成不发光物。
- 新增、异物植入或替换为更大物体前，必须确认 Target 有完整可见且未被占用的可放置空间。
- 位置字段只定位，不写颜色、材质、纹理、风格、明暗等外观修饰。
- 中文文件用 UTF-8；中文路径命令使用引号或 `-LiteralPath`。

## 盲盒修改总则

- 数据事实源是 `Game content extraction/data/blind_boxes.py`。
- 盲盒修改必须先审查、后替换：先按 `审查规则.md` 和对应类别审查文档定位问题，再按 `修改规则.md` 落库。
- 四池固定为 `core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`；每池固定 50 条且池内唯一。
- `visible_small_items` 只写升级后的可见单位，如一盒、一包、一筒、一盘、一套、一卷、一束、一叠、一册、一排。
- `scene_expansion_items` 虽保留历史字段名，实际按“场景补充中型物”维护：以单个前台自然中型实物为主，全池只允许极少量简单组合，最多 5 条且每条最多 3 个内容；不得把它写成抽取器、支架、分区盒、托盘、收纳壳，也不要滑向架子类、箱子类、柜子类常规扩写，或 `说明词 + 板 / 垫 / 盘 / 盒 / 册` 这类弱本体、`记录 / 说明 / 参考 + 本 / 册 / 牌` 这类抽象职能文书堆叠池。
- 统一修改目标不是换词，而是让命名先让人看到主体物、第一眼就能成像，同时解决视觉本体重复、场景错位、模板化、跨池扩写和伪多样性。
- 若原名过于功能化、壳体化或抽象化，可在内容本身清楚可见时用“可见内容 + 主体物”增强直观度，但整条仍必须像物名，不像说明句。
- 不要用“场景词 / 口味词 / 材质词 + 原主词”制造伪多样性；若主词没变，如 `磅蛋糕 -> 柠檬磅蛋糕`、`茶包 -> 篝火茶包`，默认视为未修复，优先直接换成另一种自然、同场景、真实可见的物体。
- 若一轮替换只是把旧坏家族换成另一条 `xx板 / xx架 / xx器 / xx机 / xx本 / xx册` 弱模板链，视为假修复，必须继续重做。
- 收尾复查必须额外检查同后缀家族是否成串，例如 `xx布包 / xx工具包 / xx防尘袋 / xx提篮`；不能只过测试、不看读感。
- 默认面向欧美 / 国际化用户；除非类别明确要求，不写强中式、强地域或强课程体系绑定物品。
- 修改盲盒内容后运行 `Game content extraction/test_blind_box_content_model.py`，并额外检查四池数量、重复、第四池跨池重叠、禁词、尾词配额和模板密度。

## 工具总则

- `Game content extraction/` 只用原生 `tkinter/ttk`；不改成 Web、数据库、服务端或大型工程。
- `Game content extraction/` 的开发、验证和打包默认使用项目内解释器 `Game content extraction/.venv/Scripts/python.exe`，避免缺少 `tkinter`、Tcl 或 Tk。
- `draw_history.json` 服务物品、动物和表情历史；表情只写 `expression_pools`。
- 图像抓取只复制文件；批量重命名必须保留“目标文件已存在则跳过”的保护逻辑。

## 修改与发布

- 修改前先读目标文件职责和对应规则文档；修改中只动相关段落；修改后做回归验证。
- 根目录 `agents.md` 只保留稳定规则和入口；主图执行细则写在 `prompts/main-image/agents.md`，工具执行细则写在 `Game content extraction/agents.md`。
- 涉及 App 逻辑时同步查看 `Game content extraction/agents.md`。
- `Game content extraction/build/`、`Game content extraction/dist/` 和 `Game content extraction/release/*.exe` 属于本地构建产物，默认保持忽略；若 `.gitignore` 命中已跟踪文件，需同步取消跟踪。
- 桌面工具安装包固定输出到 `Game content extraction/release/`；发布前先确认本地安装包名、版本号和 Release 资产一致。
- 检查更新默认走“安装包内更新”，不要直接覆盖正在运行的 exe；若由 PyInstaller 单文件程序启动安装器，先清理 DLL 搜索路径、`_PYI_*`、`_MEIPASS2`、`TCL_LIBRARY`、`TK_LIBRARY` 等运行时环境，再拉起安装包。
- 源码包推荐发布标识 `source-YYYYMMDD`、资产名 `zbt-prompt-source-YYYYMMDD.zip`；只有发布桌面工具新版本时，才提升 `APP_VERSION`、安装包名和正式 `v0.1.x` tag。
