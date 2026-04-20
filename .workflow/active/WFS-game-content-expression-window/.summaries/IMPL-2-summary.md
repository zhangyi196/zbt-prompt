## Summary

新增表情组字段解析、模板编号选择、随机模板策略和原文局部回填。支持单行、多行和多组 `极性:` 输入，只替换对应 `具体表情:` 字段值。

## Files Modified

- `Game content extraction/内容抽取.py`

## Key Decisions

- 重复增强时替换已有 `眉/眼/嘴` 模板，避免堆叠。
- 保留 `[目标物]`、`[证据物]`、`[对方人物]`、`[剧情食物]`、`[剧情小物]`，不自动替换。

## Tests

- `python -m py_compile 'Game content extraction\\内容抽取.py'`
- `python '.workflow\\active\\WFS-game-content-expression-window\\.process\\verify_expression.py'`
