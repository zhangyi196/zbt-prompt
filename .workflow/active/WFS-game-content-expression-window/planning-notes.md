# Planning Notes

## User Intent

GOAL: 为 `Game content extraction` 新增独立“人物表情内容抽取窗口”。

SCOPE: 只规划实现，不执行代码修改。目标功能是读取用户粘贴的表情组文本，解析 `极性`、`具体表情`、`单人/多人`，从 `../组图 23 表情库.md` 查找匹配眉/眼/嘴模板，并把模板追加到原文 `具体表情:` 字段后。

CONTEXT: 已有 spec 包 `.workflow/.spec/SPEC-2026-04-20-game-content-extraction-人物表情抽取窗口/`，已更新 `agents.md`、`Game content extraction/CLAUDE.md`，并新增 `Game content extraction/agents.md` 指向 `CLAUDE.md`。

## Context Findings

- 主程序集中在 `Game content extraction/内容抽取.py` 的 `BlindBoxExtractor` 类中。
- 现有 UI 使用 `tkinter` / `ttk` / `scrolledtext`，主界面输入仍是逗号分隔单行语法。
- 现有抽取历史只服务盲盒和动物内容，文件为 `draw_history.json`；表情抽取不应接入该历史。
- `Game content extraction/内容抽取.spec` 当前 `datas=[]`，打包时需要额外确认表情库 Markdown 路径。
- `组图 23 表情库.md` 是单一事实源；每个表情 8 条模板，1-4 单人，5-8 多人。
- 关键验收样例：`极性=负向`、`具体表情=困惑`、`单人/多人=单人`、`模板编号=4`，应追加“眉：一侧眉尾抬起...”那条模板。
- 同一段输入可能包含多组 `极性:`；计划需要支持多组逐个增强，或在 MVP 中明确限制并给出中文错误。当前建议支持多组。
- 重复点击抽取不应无限叠加已有 `眉/眼/嘴` 模板；需要检测并替换或跳过已有追加内容。

## Planning Constraints

- 计划只生成实施任务，不开始实现。
- 新窗口必须是独立 `Toplevel`，不复用或改变主输入框语法。
- 原文局部回填，只改 `具体表情:` 字段后内容，其他字段和顺序尽量保持原样。
- 第一版保留 `[目标物]`、`[证据物]`、`[对方人物]`、`[剧情食物]`、`[剧情小物]`，不自动替换。
- 重复增强时不得堆叠多份 `眉：...；眼：...；嘴：...`。
- 中文 UI 和中文错误提示；不引入 Web、数据库、服务端或大型工程化结构。
- 不削弱现有盲盒/动物抽取、历史、重置按钮和复制行为。
