## Summary

Preserved runtime compatibility and filtered risky item state words.

## Files Modified

- `Game content extraction/内容抽取.py`

## Key Decisions

- Parser labels, bucket keys and history keys remain unchanged.
- `_choose_item_state` filters states containing `半透明`, `高光反光`, or `带有光泽`.

## Tests

- `python -B -m py_compile 'Game content extraction\内容抽取.py'`
- `python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'`
