每次完成会话后，同步检查根目录 `agents.md`、`README.md`、`.gitignore`，以及涉及工具时的 `Game content extraction/agents.md`、`Game content extraction/README.md` 是否需要更新；这些文件只记录稳定规则和必要入口。
若 `.gitignore` 命中已跟踪的缓存或构建文件，必须同步取消跟踪清理。

# Agents Guide

本仓库维护中文提示词规则；`Game content extraction/` 是配套本地 `tkinter` 工具，工具细则见 `Game content extraction/agents.md`。

## 入口

- `主图 第一步.md`：Target 是否需要新增内容；需要时输出 2 个盲盒类别编号、动物字段、禁用字段和补偿字段。
- `主图 第二步 .md`：审核和摆放候选物；用户给了候选就不得脑补新候选。
- `组图 4.md`：18 个找不同差异点，九宫格每区 2 个，禁灯光 / 明暗 / 反光 / 阴影变化。
- `组图 23.md`：Ref-A / Ref-B 到 Target 的差异迁移，保留 Ref 绑定、人物热区互斥、冷区避让和空间可放置性。
- `组图 23 表情前置.md`、`组图 23 表情库.md`：人物表情类别和模板事实源。
- `Game content extraction/data/agents.md`：盲盒四池物品写库细则，改 `blind_boxes.py` 前先读。

## 全局硬规则

- 禁止脑补不可见对象、画外空间、遮挡后区域或身份不稳定对象。
- 差异点遵守“一圈一物一变化”；不得依赖细线、小点、刻痕、碎屑、污渍、标签或价格签。
- 不改人物骨架、姿态、头身朝向、四肢动作、支撑关系和贴邻热区。
- 不做灯光、发光、明暗、阴影、高光、反光、滤光、投影或镜面成像变化。
- 灯具、灯罩、灯泡、蜡烛火焰等照明对象不得整体消失、整体移动或替换成不发光物。
- 新增、异物植入或替换为更大物体前，必须确认 Target 有完整可见且未被占用的可放置空间。
- 位置字段只定位，不写颜色、材质、纹理、风格、明暗等外观修饰。
- 中文文件用 UTF-8；中文路径命令使用引号或 `-LiteralPath`。

## 盲盒要点

- 数据事实源：`Game content extraction/data/blind_boxes.py`；当前为 20 个 `常见场景+用途` 入口。
- 四池固定为 `core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`，运行时兼容 `large` / `medium` / `small` / `hanging`。
- `scene_expansion_items` 保留历史字段名，实际按可放置中型单物维护；不得写 `组合`，且必须去核心化。
- 写库时先按真实物品族选物，再检查尾词配额和雷同密度；禁止 `收纳盒`、`展示架`、`托座`、`分装盒`、`xxx清洁刷`、`xxx袋` 等模板凑数。
- `conditional_items`、`anchor_required_items`、`blocked_or_risky` 不再作为目标内容类别；风险内容只进入 `blocked_patterns`。

## 工具要点

- `Game content extraction/` 只用原生 `tkinter/ttk`；不改成 Web、数据库、服务端或大型工程。
- `draw_history.json` 服务物品、动物和表情历史；表情只写 `expression_pools`。
- 图像抓取只复制文件；批量重命名必须保留目标文件存在时跳过的保护逻辑。

## 修改与发布

修改前读目标文件职责和核心约束；修改中只动相关段落；修改后检查数量、格式、禁区、承载关系、固定输出和自检是否一致。涉及 App 逻辑时同步查看 `Game content extraction/agents.md`。

源码包推荐发布标识 `source-YYYYMMDD`、资产名 `zbt-prompt-source-YYYYMMDD.zip`；只有发布桌面工具新版本时，才提升 `APP_VERSION`、安装包名和正式 `v0.1.x` tag。
