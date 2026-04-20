# Planning Notes

## User Intent

GOAL: 将 `Game content extraction` 改为参考图风格的单主窗口双工作区 UI。

SCOPE:
- 主窗口顶部提供两个切换按钮：`盲盒物品/动物抽取`、`人物表情抽取`。
- 两个按钮在同一窗口内切换内容。
- 盲盒/动物抽取保留现有输入语法、历史机制、按钮语义和输出。
- 人物表情抽取迁入主工作区，继续使用现有表情库解析与增强逻辑。
- UI 风格参考 `UI风格参考.png`：浅灰蓝背景、白色内容区、蓝色主操作、胶囊导航、宽松间距。

CONTEXT:
- 来源分析：`.workflow/.analysis/ANL-2026-04-20-game-content-extraction-ui-redesign/`
- 既有人物表情 workflow：`.workflow/active/WFS-game-content-expression-window/`
- 规划阶段只产出计划，不改源码。

## Constraints

- 不改成 Web、数据库、服务端或大型工程。
- 不破坏盲盒/动物逗号分隔单行输入。
- 不破坏 `draw_history.json` 语义。
- 不破坏 `enhance_expression_text` 的固定样例、多组输入、重复增强与错误提示。
- 不新增第三方 UI 依赖，除非后续用户明确允许。

## Context Findings

- Critical files: `Game content extraction/内容抽取.py`, `Game content extraction/CLAUDE.md`, `agents.md`, `UI风格参考.png`.
- Existing implementation: `setup_ui()` currently owns the blind box / animal main UI; `open_expression_window()` owns an independent expression `Toplevel`.
- Must preserve widget attributes used by command handlers: `input_entry`, `state_var`, `category_vars`, `category_spin_vars`, `animal_vars`, `animal_spin_vars`, `auto_paste_var`, `output_text`, `expression_input_text`, `expression_output_text`, `expression_template_mode_var`, `expression_template_index_var`.
- Conflict risk: medium. The target change overlaps with recent expression-window work and docs currently describe `Toplevel`.
- Resolution strategy: refactor UI containers only, preserve business logic and verified expression helpers.
