---
title: "Test Conventions"
readMode: required
priority: high
category: test
keywords:
  - test
  - coverage
  - mock
  - fixture
  - assertion
  - framework
---

# Test Conventions

Auto-generated from project analysis. Update manually as patterns evolve.

## Framework

- Framework: pytest（通过 `Game content extraction/.venv/` 运行）
- Run command: `Game content extraction/.venv/Scripts/python.exe -m pytest` 或直接运行测试文件

## Directory Structure

- Pattern: 测试文件放在被测模块同级目录（`Game content extraction/`）
- 测试文件命名: `test_*.py`

## Naming Conventions

- Test files: `test_blind_box_content_model.py`, `test_clear_input_behavior.py`, `test_expression_enhancement.py`

## Known Test Files

- `Game content extraction/test_blind_box_content_model.py` — 盲盒内容模型验证
- `Game content extraction/test_clear_input_behavior.py` — 输入行为测试
- `Game content extraction/test_expression_enhancement.py` — 表情增强测试

## Patterns

- 修改盲盒数据后必须运行 `test_blind_box_content_model.py`
- 额外检查四池数量、重复、跨池重叠、禁词、尾词配额和模板密度

## Entries
