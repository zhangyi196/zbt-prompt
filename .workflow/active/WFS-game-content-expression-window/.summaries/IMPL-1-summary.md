## Summary

新增表情库路径解析和 Markdown 解析核心。工具现在可从源码根目录、可执行文件相邻目录或 PyInstaller `_MEIPASS` 中定位 `组图 23 表情库.md`，并解析正向/负向、表情类别、单人 1-4、多人 5-8 模板。

## Files Modified

- `Game content extraction/内容抽取.py`

## Key Decisions

- 保持 `组图 23 表情库.md` 为单一事实源。
- 表情库缺失、空文件或结构不完整时抛出中文 `ValueError`。

## Tests

- `python -m py_compile 'Game content extraction\\内容抽取.py'`
- `python '.workflow\\active\\WFS-game-content-expression-window\\.process\\verify_expression.py'`
