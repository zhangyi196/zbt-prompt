# TASK-001: 收紧组图 23 的 List 2 强信号规则并统一输出项数量

## Changes
- `/f/vscode projects/zbt prompt/prompts/2.group-image/组图 23.md`：在 List 2 首条规则补入真实可见锚点硬限制，加入“`不存在的实体不得作为锚点或位置依据。`”。
- `/f/vscode projects/zbt prompt/prompts/2.group-image/组图 23.md`：收紧第一眼可见与强信号门槛，加入“`轻微破损、小痕迹、小划痕、细裂纹一律不得进入 List 2。`”，并把优先信号收敛到更直接的小范围强对比变化。
- `/f/vscode projects/zbt prompt/prompts/2.group-image/组图 23.md`：保留服装变化但不新增第 10 类，加入“`服装变化不是独立第 10 类，只能复用现有 9 类变化类型表达。`”，并明确 3 到 6 条与轮换约束。
- `/f/vscode projects/zbt prompt/prompts/2.group-image/组图 23.md`：把固定输出格式中的旧句改为“`按第五节固定 12 项输出。`”，与后文 12 项自检保持一致。
- `/f/vscode projects/zbt prompt/.workflow/scratch/quick-group23-list2-content-2026-05-27/.task/TASK-001.json`：将任务状态更新为 `completed`。

## Verification
- [x] 文件包含精确字符串 `不存在的实体不得作为锚点或位置依据。`：使用 `Grep` 检查目标文件命中。
- [x] 文件包含精确字符串 `轻微破损、小痕迹、小划痕、细裂纹一律不得进入 List 2。`：使用 `Grep` 检查目标文件命中。
- [x] 文件包含精确字符串 `服装变化不是独立第 10 类，只能复用现有 9 类变化类型表达。`：使用 `Grep` 检查目标文件命中。
- [x] 文件包含精确字符串 `按第五节固定 12 项输出。`：使用 `Grep` 检查目标文件命中。

## Tests
- [x] `Grep` 精确检查 `不存在的实体不得作为锚点或位置依据。``：通过。
- [x] `Grep` 精确检查 `轻微破损、小痕迹、小划痕、细裂纹一律不得进入 List 2。``：通过。
- [x] `Grep` 精确检查 `服装变化不是独立第 10 类，只能复用现有 9 类变化类型表达。``：通过。
- [x] `Grep` 精确检查 `按第五节固定 12 项输出。``：通过。

## Deviations
- 无。

## Notes
- 按用户要求未修改 `agents.md`、`组图 4.md` 或其他业务提示词文件；List 1 核心逻辑保持不变。
