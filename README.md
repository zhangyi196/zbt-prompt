# zbt prompt

本仓库主要维护中文提示词规则，并包含配套本地 `tkinter` 工具目录 `Game content extraction/`。

## 目录说明

- `主图 第一步.md`：主图候选生成前置规则；先判断画面是否真的需要新增内容，若不需要则固定输出 `不需要新增物品`，若需要再生成 6 个小型候选。
- `主图 第二步 .md`：候选物审核与摆放规则，采用“优先级 + 硬规则 + 固定输出”的稳定写法。
- `组图 4.md`：找不同润色规则。
- `组图 23 表情前置.md`：剧情表情类别前置规则，人物块数量沿用单人 1 个、多人 2-3 个；每块 `具体表情` 一栏写 4 个同极性类别，字段值不得用 `[]` 包裹。
- `组图 23 表情库.md`：人物表情模板库；每类包含单人 8 条、多人 8 条眉 / 眼 / 嘴模板。
- `组图 23.md`：Ref-A / Ref-B 到 Target 的差异迁移规则；当前 v1.7.10.8 为中等压缩结构版，保留 List 1 人物贴邻热区互斥、List 2 冷区兜底、新增物体空间可放置性、高可见差异与重复抑制约束。
- `Game content extraction/`：本地 `tkinter` 小工具，详细说明见 [Game content extraction/README.md](Game%20content%20extraction/README.md)。

## 盲盒内容库优化方向

`Game content extraction` 的盲盒物品内容库已从旧式主题杂货池，替换为 20 个 `常见场景+用途` 入口：`桌面+学习`、`餐桌+茶歇`、`厨房+烘焙`、`卧室+梳妆`、`浴室+洗护`、`客厅+装饰`、`儿童房+玩具`、`宠物+日常`、`庭院+园艺`、`门口+雨具`、`沙滩+度假`、`公园+野餐`、`营地+露营`、`街道+出行`、`运动场+装备`、`海底+潜水`、`节日+礼物`、`手作+缝纫`、`手作+编织`、`商店+零食`。

每个类别下均按四类内容池维护：`core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`；运行时继续映射回现有大型 / 中型 / 小型 / 悬挂四栏。完整头脑风暴见 `.workflow/.brainstorm/BS-2026-04-29-重新定义conditional-items-blocked-or-risky/`，最新规格包见 `.workflow/.spec/SPEC-2026-04-29-game-content-extraction-four-pool-refactor/`。

当前已完成 20 类全量替换，旧静态盲盒物品内容已从数据文件移除。盒号 1-20 保留用于旧逗号输入、四栏输出和 `draw_history.json.item_pools` 历史兼容，但盒号语义已切换为新的场景+用途目录；`hanging` 仅作为兼容字段保留为空。

四类内容池重构已按 `.workflow/.spec/SPEC-2026-04-29-game-content-extraction-four-pool-refactor/` 落地。后续不再把 `conditional_items`、`anchor_required_items`、`blocked_or_risky` 作为目标内容类别；风险内容只进入 `blocked_patterns` 测试/校验规则。

## 提示词维护要点

- `组图 23.md` 的 List 2 可以追求边角和边缘覆盖，但不得为了填点新增无法容纳的物体。
- `组图 23.md` 的 List 1 若已占用人物面部、手中物、脸侧符号、后背标识或身后紧邻对象，同一人物热区内不再叠加其他差异点；符号只用功能性符号，不用星星 / 闪光等情绪装饰。
- `组图 23.md` 的 List 2 每块预留冷区都要先尝试已有独立小物或块状局部承载面兜底；只用完整小物增减、大块图案替换、明显结构缺失、长距离位移、明显开合 / 翻转等第一眼可见变化，不用刻痕、细裂纹、小点、轻微磨损、细小石子等微型痕迹。
- `组图 23.md` 的 List 2 禁止把踢脚线、墙角线、接缝线、边线、轮廓线、红毯 / 地毯边缘线等细长线条作为差异主体；不得写线条变色、直线变波浪线、断开、偏移、增减或把线条变化包装成大块图案替换。
- `组图 23.md` 的 List 2 不得左右 / 上下 / 对称成对套用同一修改模板；同类对象默认最多 1 点，完整小物新增、完整小物消失、大块图案替换等高可见类型要轮换，避免连续或成对输出“新增一块……”“移除一个……”“……消失”等同句式。
- `组图 23.md` 已继续压缩输出区重复规则；维护时不要用重复段落换取强调，优先在对应规则段补充一句硬约束。
- `组图 23 表情前置.md` 的人物块字段值必须输出纯文本；每个 `具体表情` 字段固定写 4 个互不重复的同极性类别；除 `[证据物]`、`[目标物]`、`[对方人物]` 等占位符外，不要给字段值加方括号。
- `Game content extraction/` 中的人物表情增强现在可直接读取同一 `具体表情` 字段里的多候选类别，支持 `、`、`，`、`,`、`/`、`|` 分隔；App 会先校验整组候选，再按 `draw_history.json.expression_pools` 历史降权随机择一类别补全眉 / 眼 / 嘴，最终结果只保留被选中的单一类别。
- `组图 23 表情库.md` 的单人和多人模板均使用 1-8 编号，强度从中等可见起步，不保留轻微表情档。
- `组图 23.md` 的剧情字段应输出简短自然小剧情，不输出 `->` 箭头链路、清单式并列或用户原文复述。
- `组图 23.md` 不允许让灯具、灯罩、灯泡、蜡烛火焰等照明关联对象整体消失；这类对象只能做不改变光照关系的局部变化。
- 新增、异物植入或替换为更大物体前，必须确认 Target 中有完整可见、未被占用且不会挤压原主体的空间；否则改用已有独立小物体的局部替换、消失、翻转、破损、大块图案替换或长距离平移。

## 仓库打包发布

仓库源码打包发布到 GitHub Release 时，使用保留目录结构的 zip 资产，不直接上传文件夹。

- 推荐资产名：`zbt-prompt-v0.1.4-source-YYYYMMDD.zip`
- 推荐 tag：`v0.1.4-source-YYYYMMDD`
- 该类 source-bundle release 只用于分发仓库快照，不作为桌面工具新版本发布
- tag 必须保持版本规范化后仍为当前正式桌面版本，避免触发应用内“发现新版本”提示

## 桌面工具发布

## 盲盒物品库重构 Spec 状态

`Game content extraction` 的盲盒物品库重构已完成 spec-generator 全链路规格包，工作目录位于 `.workflow/.spec/SPEC-2026-04-29-game-content-extraction-blind-box-library-refactor/`。当前已全量落地 20 类新内容，旧内容不再作为盲盒物品来源，并继续保持旧运行时兼容：

- 20 个 `常见场景+用途` 入口：如 `桌面+学习`、`餐桌+茶歇`、`沙滩+度假`、`海底+潜水`。
- 四类内容池目标：`core_items`、`support_items`、`visible_small_items`、`scene_expansion_items`。
- 兼容现有四栏：仍映射回 `large` / `medium` / `small` / `hanging`，不破坏现有编号输入和 UI；`hanging` 当前为空兼容桶。
- 全量类别：20 个场景+用途盒号均已由四池内容生成，运行时不再保留旧主题杂货池。
- 质量目标：人工抽样 30 次时，明显不适合项低于 10%，且风险内容不进入默认输出。
- Readiness 结果：`readiness-report.md` 评分 92.75 / 100，Gate 为 Pass；`issue-export-report.md` 已给出 4 个可手动创建的 Epic issue。
- 当前测试覆盖：`Game content extraction/test_blind_box_content_model.py` 检查 20 类四池 schema、旧条件/风险池移除、全量四栏兼容、旧输入覆盖、物品状态风险过滤和 `blocked_patterns`。
- 最新规格：`.workflow/.spec/SPEC-2026-04-29-game-content-extraction-four-pool-refactor/` 已生成，Readiness 评分 96.5 / 100；全量替换执行会话为 `.workflow/.team/TLV4-2026-04-29-blind-box-content-replace/`。

当前桌面工具发布版为 `v0.1.4`，安装包为 `GameContentExtraction-Setup-v0.1.4.exe`。

桌面工具版本、安装包和更新检查约定仍以 `Game content extraction/` 下文档为准，不因源码打包 release 改变。应用内更新检查使用无认证 GitHub Release API，仓库需保持 public，否则旧版安装包无法发现新版本。
