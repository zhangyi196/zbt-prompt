# TLV4 Context

- User wants to replace blind-box item content with the new content model after the pilot cases looked viable.
- Previous implementation completed four-pool pilot cases in `Game content extraction/data/blind_boxes.py`.
- Target model: `core_items`, `support_items`, `visible_small_items`, `scene_expansion_items`.
- Deprecated target pools: `conditional_items`, `anchor_required_items`, `blocked_or_risky`.
- Risky/non-object outputs should be represented only as validation/test blocked patterns, not as normal candidate content.
- Repo rule: after execution, sync `agents.md`, `Game content extraction/CLAUDE.md`, `README.md`, `.gitignore`; also update local tool README if behavior changes.
