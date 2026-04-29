## Summary

Added focused validation coverage for the new blind-box content model.

## Files Modified

- `Game content extraction/test_blind_box_content_model.py`

## Key Decisions

- Tests are importlib/unittest-based to match existing project style.
- Coverage includes schema, risk leakage, runtime buckets, parser overrides and state filtering.

## Tests

- `python -B -m unittest discover -s 'Game content extraction' -p 'test_*.py'`
