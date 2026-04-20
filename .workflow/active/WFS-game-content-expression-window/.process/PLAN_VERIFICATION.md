# Plan Verification: WFS-game-content-expression-window

Quality Gate: `PROCEED_WITH_CAUTION`

结论：计划可执行，整体与 spec 对齐，没有阻断性矛盾。需要谨慎的点主要是两个执行期决策：重复增强时如何处理已有眉/眼/嘴模板，以及 PyInstaller 打包时如何稳定读取 `组图 23 表情库.md`。

## A. User Intent Alignment: PASS

计划匹配用户目标：为 `Game content extraction` 新增独立人物表情抽取窗口，解析 `极性`、`具体表情`、`单人/多人`，读取 `组图 23 表情库.md`，并只把眉/眼/嘴模板追加到 `具体表情:` 字段。

## B. Requirements Coverage: PASS

已覆盖 MVP：

- 独立 `Toplevel`。
- 单行和多行解析。
- Markdown 表情库查询。
- 指定模板编号。
- 固定验收样例：`负向 + 困惑 + 单人 + 编号 4`。
- 原文局部回填和复制。
- 中文错误提示。
- 不接入 `draw_history.json`。
- 不自动替换占位符。
- 不改变盲盒/动物主输入语法。

注意：性能和流程类 NFR 尚未在任务验收中细写，例如双组输入响应时间和“粘贴 -> 抽取 -> 复制”的步数，但当前设计较轻，风险不高。

## C. Consistency Validation: PASS

`IMPL_PLAN.md`、`plan.json`、`TODO_LIST.md`、`planning-notes.md` 和 `.task/IMPL-*.json` 在任务数量、执行顺序、核心文件、非目标、验收样例和打包关注点上保持一致。

## D. Dependency Integrity: PASS

依赖关系合理：

- `IMPL-1` 无依赖，负责表情库解析。
- `IMPL-2` 依赖 `IMPL-1`，负责文本解析和回填。
- `IMPL-3` 依赖 `IMPL-1`、`IMPL-2`，负责 UI。
- `IMPL-4` 依赖 `IMPL-1`、`IMPL-3`，负责打包路径。
- `IMPL-5` 依赖 `IMPL-2`、`IMPL-3`、`IMPL-4`，负责验收和回归。

无循环依赖。

## E. Spec Alignment: PASS

计划与既有 spec 包对齐：

- 保持 `组图 23 表情库.md` 为单一事实源。
- 保留占位符，不自动替换。
- 原文局部回填，不重写全文。
- 不接入 `draw_history.json`。
- 优先实现纯逻辑，再接 UI，最后处理打包和验证。

## F. Task Specification Quality: WARN

任务整体可执行，但有三处需要执行时明确：

- `IMPL-2` 要求避免重复堆叠眉/眼/嘴，但未指定行为。建议采用“替换已有追加模板”。
- `IMPL-3` 提到模板策略控件，但没有固定默认值。建议默认“指定模板编号”，并保证验收样例可直接选择编号 4。
- `IMPL-4` 说可以“包含或说明”表情库资源；实际打包必须选择一种可运行路径，不能只写说明。

## G. Duplication Detection: PASS

任务之间没有职责重复导致的冲突：

- `IMPL-1` 表情库解析。
- `IMPL-2` 文本解析与回填。
- `IMPL-3` UI。
- `IMPL-4` 打包。
- `IMPL-5` 验证。

多个任务会顺序修改 `内容抽取.py`，符合当前单文件 tkinter 工具现状。

## H. Feasibility: PASS

当前仓库具备实施条件：

- `Game content extraction/内容抽取.py` 存在。
- `Game content extraction/内容抽取.spec` 存在。
- `组图 23 表情库.md` 存在。
- 表情库结构符合正负向、表情标题、单人/多人、1-8 条模板的预期。
- 现有应用结构与计划假设一致。

## I. Constraints Compliance: PASS

计划遵守约束：

- 不改成 Web、数据库、服务端。
- 不破坏主输入语法。
- 不让表情抽取进入历史降权。
- 不自动替换占位符。
- 不复制第二份长期维护表情库。
- 保持中文 UI 和中文错误提示。
- 保持 Markdown 表情库为事实源。

## J. Context Validation: WARN

上下文有效，但执行时注意：

- `.workflow/active/` 当前为未跟踪 workflow 产物，后续不要用 `git add .`。
- Windows 下读取中文文件建议显式 UTF-8，避免控制台显示乱码影响判断。

## Required Execution Decisions

1. 重复增强行为：建议替换同一 `具体表情:` 字段中已有的 `眉：...；眼：...；嘴：...` 段落，避免模板堆叠。
2. UI 默认策略：建议默认指定模板编号，随机仅作为可选项；验收样例必须能稳定选择编号 4。
3. 打包策略：必须在 `内容抽取.spec` 的 `datas` 或相邻外部 Markdown 路径中选择一个可运行方案，并实际验证。
4. 验收补充：`IMPL-5` 应加入多组 `极性:` 输入、重复点击不堆叠、主抽取输入回归和复制按钮作用域检查。

最终判断：`PROCEED_WITH_CAUTION`。计划足够进入执行阶段，以上决策可在实现时按保守方案落地。
