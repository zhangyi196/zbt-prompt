---
id: EPIC-004
title: 质量验证、审查与文档同步
priority: Should
mvp: true
size: M
requirements: [REQ-005, REQ-007, NFR-SC-001]
architecture: [ADR-004]
dependencies: [EPIC-002, EPIC-003]
status: complete
---

# EPIC-004: 质量验证、审查与文档同步

## Description

为盲盒内容库重构建立可重复的质量门禁：静态 schema 校验、风险泄漏校验、人工 spot check、文档同步和后续扩库交接。

## Stories

### STORY-004-001: 增加风险泄漏校验

As a 开发维护者, I want 自动检查风险物不会进入默认输出 so that 内容质量不依赖人工记忆。

- Acceptance Criteria:
  - 校验覆盖 `blocked_or_risky` 到四栏映射的零泄漏。
  - 透明、反光、灯光、微型痕迹、细线类风险词纳入审查。
  - 校验失败时能指出类别和条目。
- Size: M
- Trace: REQ-005, NFR-S-001

### STORY-004-002: 增加 schema 完整性校验

As a 内容维护者, I want 新类别缺字段时能尽早失败 so that 后续抽取不会消费半成品数据。

- Acceptance Criteria:
  - 每个试点必须包含五层字段。
  - 每个试点必须包含四栏兼容映射。
  - 试点标记、中文入口名和场景提示不能为空。
- Size: S
- Trace: REQ-005

### STORY-004-003: 固化人工审查表

As a 内容维护者, I want 一份固定人工审查清单 so that 每次扩库都能按同样标准判断。

- Acceptance Criteria:
  - 审查项包含可见性、承载关系、可圈选性、风险物泄漏、类别贴合度。
  - 审查记录保留样本数、不适合项占比和处理结论。
  - 审查表链接到试点类别和相关需求。
- Size: S
- Trace: REQ-007

### STORY-004-004: 同步项目维护文档

As a 项目维护者, I want 执行完成后同步关键文档 so that 后续会话不会遗忘新约束。

- Acceptance Criteria:
  - 更新 `agents.md`、`Game content extraction/CLAUDE.md`、`README.md`、`.gitignore`。
  - 如涉及小工具说明，同步 `Game content extraction/README.md`。
  - `.gitignore` 对 workflow spec/brainstorm 输出的跟踪策略保持明确。
- Size: S
- Trace: REQ-007, NFR-SC-001

## Architecture Links

- [ADR-004](../architecture/ADR-004-risk-isolation-validation.md)

## Risks

- 文档同步若漏掉工具目录说明，会导致后续实现按旧盲盒库理解继续修改。
