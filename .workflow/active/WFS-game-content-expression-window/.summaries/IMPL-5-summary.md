## Summary

新增并运行轻量验证脚本，覆盖固定验收样例、多组输入、重复增强、错误分支和旧主输入解析。

## Files Modified

- `.workflow/active/WFS-game-content-expression-window/.process/verify_expression.py`

## Key Decisions

- 验证脚本放在 workflow `.process` 目录，避免污染业务代码。
- GUI 人工 smoke 未在当前无图形自动化环境中启动；核心逻辑和语法已验证。

## Tests

- `python -m py_compile 'Game content extraction\\内容抽取.py'`
- `python '.workflow\\active\\WFS-game-content-expression-window\\.process\\verify_expression.py'`
