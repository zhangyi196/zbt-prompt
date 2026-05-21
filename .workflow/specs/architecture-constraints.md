---
title: "Architecture Constraints"
readMode: required
priority: high
category: arch
keywords:
  - architecture
  - module
  - layer
  - boundary
  - dependency
  - structure
---

# Architecture Constraints

Auto-generated from project structure. Update manually as architecture evolves.

## Module Structure

- Type: single-package（单仓库）
- Key modules:
  - `prompts/` — AI 提示词规则（0.image-prompt / 1.main-image / 2.group-image）
  - `skills/` — Claude Code Skills（green-circle-photo-prompts）
  - `Game content extraction/` — Python tkinter 桌面工具 + 盲盒数据层
  - `agents.md` — 项目总导航
  - `组图 23 表情库.md` — 表情模板事实源

## Layer Boundaries

```
agents.md (总导航 + 全局硬规则)
  ├── prompts/
  │   ├── 0.image-prompt/      → 绿圈洗图（独立链路）
  │   ├── 1.main-image/        → 主图生成链路
  │   └── 2.group-image/       → 组图差异链路
  ├── skills/                   → 调用 prompts/ 规则
  └── Game content extraction/
      ├── data/                 → 盲盒数据事实源
      └── *.py                  → 桌面工具 UI
```

## Dependency Rules

- `skills/` 引用 `prompts/` 中的系统提示词作为规则源
- `Game content extraction/data/` 是盲盒数据的唯一事实源
- 根目录 `agents.md` 只保留稳定入口和全局规则，执行细则收敛在子目录
- 提示词不直接依赖 `blind_boxes.py`，通过第一步的类别库保持同步

## Technology Constraints

- 桌面工具: Python 3.13 + tkinter/ttk 原生（不引入 Web/数据库）
- 提示词规则: Markdown, UTF-8, 中文
- Skills: Claude Code Skills 框架
- 无外部 API 依赖

## Entries
