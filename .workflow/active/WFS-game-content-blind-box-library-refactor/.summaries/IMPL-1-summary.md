## Summary

Added the blind-box content-model compatibility layer in `Game content extraction/data/blind_boxes.py`.

## Files Modified

- `Game content extraction/data/blind_boxes.py`

## Key Decisions

- Kept legacy `BLIND_BOXES` as the runtime view.
- Added `BLIND_BOX_SCENE_ENTRIES`, `BLIND_BOX_ITEM_POOL_BUNDLES`, `BLIND_BOX_COMPATIBILITY_MAPPING`, and generated pilot entries.

## Tests

- Covered by full unittest run after IMPL-4.
