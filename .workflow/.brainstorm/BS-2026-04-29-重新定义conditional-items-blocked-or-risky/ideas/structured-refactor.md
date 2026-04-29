# Idea: Structured Refactor For Conditional And Risk Pools

## Problem

String-only item pools cannot express whether an item depends on a visible anchor. They also blur the difference between risky concrete objects, tiny unusable objects, and validation rules.

## Proposed Direction

Introduce a structured item candidate model:

- `name`
- `pool`
- `default_enabled`
- `required_anchor`
- `min_size`
- `visibility`
- `risk_tags`

Replace:

- `conditional_items` -> `anchor_required_items`
- `blocked_or_risky` -> `blocked_rules`

## Immediate Rule Changes

- Anchor-required candidates are excluded from default output.
- Default four-column output is generated only from safe default-enabled candidates.
- Risk rules are not item candidates.
- Thin/string/line-like objects are blocked by rule, not kept as risky candidate examples.

## Acceptance Direction

The model should prevent examples like `显示器下方收纳架` from being output unless `显示器` is known to exist, and should prevent examples like `细绳挂饰` from being treated as a usable game object.
