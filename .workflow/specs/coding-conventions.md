---
title: "Coding Conventions"
readMode: required
priority: high
category: coding
keywords:
  - style
  - naming
  - import
  - pattern
  - convention
  - formatting
---

# Coding Conventions

Auto-generated from project analysis. Update manually as patterns evolve.

## Formatting

- Indentation: Markdown 无严格要求；Python 4 空格
- Line length: 未配置
- Trailing commas: Python 无强制
- Semicolons: 不使用
- Encoding: UTF-8（所有中文文件）

## Naming

- Prompt 文件: 中文描述性名称（如 `主图 第一步.md`、`组图 23.md`）
- Python 文件: snake_case（如 `blind_boxes.py`、`item_states.py`）
- Skills 目录: kebab-case（如 `green-circle-photo-prompts/`）

## Imports

- Python: 标准库 → 项目内模块
- 无路径别名配置

## Patterns

- 提示词文件采用固定结构：角色设定 → 核心任务 → 规则 → 输出格式 → 自检
- 每个子模块有专属 `agents.md` 做入口导航
- 规则层级：全局硬规则（根 agents.md）→ 模块执行细则（子目录 agents.md）
- 数据修改遵循审查→修改→复查闭环

## Entries
