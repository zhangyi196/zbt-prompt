## Summary

新增主界面“人物表情抽取”入口按钮，并接入独立 `Toplevel` 窗口。窗口包含输入区、指定/随机模板策略、模板编号、抽取、清空、复制和输出区。

## Files Modified

- `Game content extraction/内容抽取.py`

## Key Decisions

- 表情窗口拥有独立输入/输出，不复用主盲盒/动物输入框。
- 复制按钮只复制表情窗口输出内容。

## Tests

- `python -m py_compile 'Game content extraction\\内容抽取.py'`
- `python '.workflow\\active\\WFS-game-content-expression-window\\.process\\verify_expression.py'`
