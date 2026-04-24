# Understanding Document

**Session ID**: DBG-2026-04-24-expression-clear-input
**Bug Description**: 表情抽取中的“清空输入”没有像盲盒区那样把剪贴板内容回填，只做了内容清空
**Started**: 2026-04-24T00:00:00+08:00

---

## Exploration Timeline

### Iteration 1 - Initial Exploration

#### Current Understanding

- 盲盒区 `clear_input()` 会先清空输入框，再在 `auto_paste_var` 开启时读取剪贴板并回填。
- 表情区 `clear_expression_input()` 只清空 `expression_input_text`，没有读取剪贴板。
- 用户期望“跟盲盒物品中的清空输入一个逻辑”，所以这里属于行为不一致，不是单纯文案问题。

#### Evidence from Code Search

- `Game content extraction/内容抽取.py:1254-1261`
  盲盒区 `clear_input()` 先删除输入，再读取剪贴板回填。
- `Game content extraction/内容抽取.py:1287-1289`
  表情区 `clear_expression_input()` 只删除文本，没有自动粘贴。
- `Game content extraction/内容抽取.py:887`
  表情区按钮已经叫“清空输入”，因此更容易放大这种行为差异。

#### Corrected Understanding

- ~~表情区“清空输入”只需要做到不清输出即可。~~
- 更准确地说：表情区“清空输入”要同时对齐盲盒区的两层行为。
  1. 只清输入，不清输出。
  2. 若开启“自动粘贴”，清空后回填当前剪贴板文本。

---

## Current Consolidated Understanding

根因是两个工作区的“清空输入”没有复用同一套逻辑：盲盒区实现了“清空 + 按需回填剪贴板”，表情区只实现了“清空”。修复应当把两者收敛到共享辅助逻辑，避免后续再次漂移。
