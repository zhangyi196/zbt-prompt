# Quick Context

## Task

解决 M2 milestone audit 的两个 warning：

1. 根目录 `agents.md` / `README.md` 仍引用不存在的 `prompts/group-image/...`。
2. `.workflow/roadmap.md` 中 M2 Phase 1 仍显示 `Not started`。

## Findings

- 实际组图目录是 `prompts/2.group-image/`。
- 实际主图目录是 `prompts/1.main-image/`，根入口文档也存在同类旧路径风险。
- `.workflow/state.json` 已标记 `M2` completed，并记录 `PLN-002 -> EXC-002 -> VRF-002`。

## Execution

- 将根入口文档中的主图 / 组图路径同步为编号目录。
- 将 roadmap Phase 1 勾选为 completed，并在进度表记录完成日期。
