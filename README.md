# zbt prompt

本仓库维护中文提示词规则，并包含本地 `tkinter` 工具 `Game content extraction/`。维护规则入口见 [agents.md](agents.md)，工具细则见 [Game content extraction/agents.md](Game%20content%20extraction/agents.md)。

## 目录

- `主图 第一步.md`：主图新增候选前置规则；不需要新增时固定输出 `不需要新增物品`，需要时输出 2 个盲盒类别编号和控制字段。
- `主图 第二步 .md`：候选物审核与摆放规则。
- `组图 4.md`：找不同润色规则。
- `组图 23 表情前置.md`：剧情表情类别前置规则。
- `组图 23 表情库.md`：人物表情模板库。
- `组图 23.md`：Ref-A / Ref-B 到 Target 的差异迁移规则。
- `Game content extraction/data/agents.md`：盲盒四池物品写库规则。
- `Game content extraction/`：本地工具，说明见 [Game content extraction/README.md](Game%20content%20extraction/README.md)。

## 盲盒内容库

盲盒物品库已替换为 20 个 `常见场景+用途` 入口，并同步到 `主图 第一步.md`。每类按四池维护：

- `core_items`
- `support_items`
- `visible_small_items`
- `scene_expansion_items`

运行时继续映射到 `large` / `medium` / `small` / `hanging` 四栏，`hanging` 当前为空兼容桶。`conditional_items`、`anchor_required_items`、`blocked_or_risky` 不再作为目标内容类别；风险内容只进入 `blocked_patterns` 测试 / 校验规则。

四池写库细则以 `Game content extraction/data/agents.md` 为准：核心物写主题主体，配套物写工具，小物写成组可见单位，`scene_expansion_items` 按去核心化的中型单物维护；生成时检查反模板、尾词配额和雷同密度，避免 `组合`、尾词矩阵和同物品族换前缀凑数。

日常维护以 `Game content extraction/data/agents.md`、`Game content extraction/data/blind_boxes.py`、`Game content extraction/test_blind_box_content_model.py` 和 `Game content extraction/agents.md` 为准；历史规格保留在 `.workflow/.spec/`。

## 维护要点

- 提示词保持中文风格、固定输出、数量配额、自检项和既有链路。
- `组图 23.md` 保留 Ref 绑定、人物热区互斥、冷区兜底、空间可放置性和灯具照明关系约束。
- 新增、异物植入或替换为更大物体前，必须确认 Target 中有完整可见、未被占用且不会挤压原主体的空间。
- 根目录 `agents.md`、`README.md`、`.gitignore`，以及工具目录 `Game content extraction/agents.md`、`Game content extraction/README.md` 必须保持精简，只记录稳定规则和必要入口。

## 发布

源码包使用保留目录结构的 zip 资产，推荐：

- 发布标识：`source-YYYYMMDD`
- 资产名：`zbt-prompt-source-YYYYMMDD.zip`

桌面工具当前发布版为 `v0.1.4`，安装包 `GameContentExtraction-Setup-v0.1.4.exe`。桌面工具版本、安装包和更新检查以 `Game content extraction/` 下文档为准。
