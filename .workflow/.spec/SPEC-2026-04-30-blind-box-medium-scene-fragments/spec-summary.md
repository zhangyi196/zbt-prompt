---
session_id: SPEC-2026-04-30-blind-box-medium-scene-fragments
phase: 6
document_type: spec-summary
status: complete
generated_at: 2026-04-30T16:00:00+08:00
stepsCompleted:
  - synthesis
version: 1
dependencies:
  - product-brief.md
  - requirements/_index.md
  - architecture/_index.md
  - epics/_index.md
  - readiness-report.md
---

# Spec Summary: Blind Box Medium Scene Fragments

## Executive Summary

This specification defines a data-library refactor for `scene_expansion_items` in the blind-box content source. The accepted direction is **medium-scale scene fragments**: not large furniture/storage subjects, not generic boxes/baskets, and not tiny cards/labels.

## Problem

The current `scene_expansion_items` pool contains many carts, cabinets, racks, shelves, desks, and similar oversized objects. Earlier smaller alternatives risked becoming containers or tiny labels, which would blur the four-pool model and weaken visual recognizability.

## Target Users

- Prompt maintainer: needs stable, reusable content rules.
- Game content extraction tool maintainer: needs data changes that preserve runtime contracts.
- Downstream prompt user: needs blind-box output items that are visible, placeable, and semantically useful.

## Core Scope

In scope:

- Define the medium-scale scene fragment model.
- Rewrite all 20 `scene_expansion_items` lists while keeping 50 unique items per scene.
- Preserve `BLIND_BOX_ITEM_POOL_BUNDLES`, `BLIND_BOXES`, and `BLIND_BOX_COMPATIBILITY_MAPPING` contracts.
- Add/extend quality tests for oversized and undersized subjects.
- Sync concise stable rules to `Game content extraction/agents.md` after implementation.

Out of scope:

- Adding a fifth pool.
- Changing scene IDs or category names.
- Changing tkinter UI, runtime extraction logic, animal pools, expression pools, image fetching, or renaming features.

## Key Requirements

| ID | Priority | Summary |
|---|---|---|
| REQ-001 | Must | Define the formal medium-scale scene fragment model. |
| REQ-002 | Must | Rewrite all 20 scenes while preserving 50 unique fourth-pool items per scene. |
| REQ-003 | Must | Add large-subject and tiny-subject quality checks. |
| REQ-004 | Must | Validate fourth-pool boundaries against core/support/small. |
| REQ-005 | Must | Preserve runtime view and existing unittest contract. |
| REQ-006 | Must | Perform stable-document sync checks. |
| REQ-007 | Should | Provide maintainable review feedback for future edits. |

## Architecture Summary

Architecture style: data-only content library refactor.

Primary data source remains `Game content extraction/data/blind_boxes.py`. Runtime compatibility remains derived through `BLIND_BOXES` and `BLIND_BOX_COMPATIBILITY_MAPPING`; validation belongs in the existing unittest suite, and documentation sync stays a maintainer workflow.

Key ADRs:

- ADR-001: Fixed medium-scale scene fragment model.
- ADR-002: Full 20-scene rewrite instead of pilot-only expansion.
- ADR-003: Quality gates for oversized and undersized subjects.
- ADR-004: Four-pool boundary rules.
- ADR-005: Runtime compatibility preservation.
- ADR-006: Stable documentation sync policy.
- ADR-007: Maintainer review loop.

## Epic Overview

| Epic | MVP | Purpose |
|---|---|---|
| EPIC-001 | Yes | Freeze rule baseline and compatibility contract. |
| EPIC-002 | Yes | Rewrite all 20 scene expansion pools. |
| EPIC-003 | Yes | Add quality boundary and regression gates. |
| EPIC-004 | Yes | Sync docs and complete maintainer review. |

Recommended order: EPIC-001 -> EPIC-002 -> EPIC-003 -> EPIC-004.

## Readiness

Gate: **Pass**  
Overall score: **91 / 100**

No blocking issues remain. One stale cross-reference class was found and fixed during readiness validation.

## File Manifest

| Document | Path |
|---|---|
| Product Brief | `product-brief.md` |
| Requirements | `requirements/_index.md` |
| Architecture | `architecture/_index.md` |
| Epics | `epics/_index.md` |
| Readiness Report | `readiness-report.md` |
| Source Brainstorm Handoff | `.workflow/.brainstorm/BS-2026-04-30-scene-expansion-items-small/spec-handoff.md` |
