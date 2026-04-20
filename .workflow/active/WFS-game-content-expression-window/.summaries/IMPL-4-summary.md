## Summary

更新打包资源配置，并在运行时代码中兼容源码路径、可执行文件相邻路径和 `_MEIPASS` 路径。

## Files Modified

- `Game content extraction/内容抽取.py`
- `Game content extraction/内容抽取.spec`

## Key Decisions

- `内容抽取.spec` 使用 `datas=[('../组图 23 表情库.md', '.')]` 将表情库打入包内。
- 找不到表情库时显示包含候选路径的中文错误。

## Tests

- `python -m py_compile 'Game content extraction\\内容抽取.py'`
- `python '.workflow\\active\\WFS-game-content-expression-window\\.process\\verify_expression.py'`
