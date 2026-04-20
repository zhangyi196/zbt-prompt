---
id: EPIC-004
priority: Should
mvp: false
size: M
requirements: [NFR-R-001, NFR-P-001]
architecture: [ADR-001, ADR-002]
dependencies: [EPIC-001, EPIC-002, EPIC-003]
status: complete
---

# EPIC-004: 打包与验证

**Priority**: Should
**MVP**: No
**Estimated Size**: M

## Description

补充测试和打包确认，确保功能在源码运行和 PyInstaller 打包场景都能读取表情库，同时保证现有抽取流程不回归。

## Requirements

- [NFR-R-001](../requirements/NFR-R-001-no-regression.md): 不回归现有抽取
- [NFR-P-001](../requirements/NFR-P-001-local-fast.md): 本地快速处理

## Architecture

- [ADR-001](../architecture/ADR-001-toplevel-window.md): 使用独立 Toplevel 窗口
- [ADR-002](../architecture/ADR-002-markdown-library.md): 读取 Markdown 表情库

## Dependencies

- [EPIC-001](EPIC-001-expression-window-ui.md) (blocking)
- [EPIC-002](EPIC-002-parser-library.md) (blocking)
- [EPIC-003](EPIC-003-output-errors.md) (blocking)

## Stories

### STORY-004-001: 核心函数测试

**User Story**: As a maintainer, I want tests for parsing and lookup so that future prompt-library changes do not silently break the tool.

**Acceptance Criteria**:
- [ ] 单行字段解析测试。
- [ ] 多行双组解析测试。
- [ ] 困惑单人第 4 条测试。
- [ ] 极性错配和编号越界测试。

**Size**: M
**Traces to**: [NFR-R-001](../requirements/NFR-R-001-no-regression.md)

---

### STORY-004-002: 主流程回归验证

**User Story**: As a user of the existing extractor, I want the original blind-box extraction to keep working so that the new feature does not disrupt current work.

**Acceptance Criteria**:
- [ ] 示例输入 `1,5,地面动物,无大型物品,中型物品+1` 仍可解析。
- [ ] draw_history.json schema 不变。
- [ ] 主复制按钮仍复制主输出区。

**Size**: S
**Traces to**: [NFR-R-001](../requirements/NFR-R-001-no-regression.md)

---

### STORY-004-003: PyInstaller datas 检查

**User Story**: As a maintainer, I want the packaged app to find the expression library so that users do not see missing-file errors after build.

**Acceptance Criteria**:
- [ ] 决定 Markdown 旁置或 spec datas。
- [ ] 若使用 datas，`内容抽取.spec` 包含表情库。
- [ ] 打包后表情库路径解析有 fallback。

**Size**: M
**Traces to**: [REQ-003](../requirements/REQ-003-library-lookup.md)
