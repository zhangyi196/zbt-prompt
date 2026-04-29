# Idea: No-Image Context Model

## Problem

The tool cannot inspect images, so visual anchors such as monitor, whiteboard, umbrella pole, wall hook, or available tabletop space cannot be used as runtime conditions.

## Principle

Conditions must come from data the tool actually has:

- selected box id
- selected category
- user input text
- explicit override syntax
- static rules

No output rule should depend on unobservable image facts.

## Recommended Fields

### `explicit_context_items`

Items enabled only by explicit user text keywords.

Example:

```python
{
    "context_key": "电脑桌学习",
    "trigger_keywords": ["电脑桌", "显示器", "屏幕", "键盘"],
    "items": ["显示器增高架", "键盘收纳托", "桌面理线盒"],
    "default_enabled": False
}
```

### `context_dependent_excluded_items`

Items that may be valid in some images but cannot be safely generated because the tool cannot inspect the image.

Example:

```python
{
    "reason": "requires_unobservable_context",
    "items": ["显示器下方收纳架", "白板磁吸收纳盒", "遮阳伞底座"]
}
```

### `safe_hanging_items`

Default-enabled hanging/decorative items that are large enough, boundary-clear, and do not depend on thin strings, wall hooks, existing poles, or other unobservable anchors.

## Removed Field

`blocked_or_risky` should be removed as an item pool. Risk is represented by `blocked_patterns` tests/rules instead.

## Acceptance Direction

- Default output cannot include context-dependent items.
- Context items require explicit user text triggers.
- No image condition can be required by runtime logic.
- Blocked/risky examples are not candidate pools.
