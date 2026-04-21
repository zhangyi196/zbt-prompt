# Understanding Document

**Session ID**: DBG-2026-04-21-update-check-release-button
**Bug Description**: 检查更新提示“当前 GitHub Releases 还没有发布文件”，但仓库已有发布；没有新版本时希望隐藏检查更新按钮。
**Started**: 2026-04-21

---

## Exploration Timeline

### Iteration 1 - Initial Exploration

#### Current Understanding

- 更新逻辑集中在 `Game content extraction/内容抽取.py` 的 `_fetch_latest_release()`、`_handle_update_result()` 和顶部切换区按钮构建。
- 当前按钮在 UI 初始化时直接 `pack(side=tk.RIGHT)`，所以无论是否有新版都会显示。
- 原逻辑只访问 `/releases/latest`，并把 HTTP 404 直接映射为“当前 GitHub Releases 还没有发布文件”。
- 通过 GitHub CLI 验证，`zhangyi196/zbt-prompt` 的 `v0.1.1` Release 存在、非草稿、非预发布，并有 `GameContentExtraction-Setup-v0.1.1.exe` 资产；`/releases/latest` 当前也可返回该发布。

#### Hypotheses

- H1: `/releases/latest` 在某些状态或短暂 API 异常下返回 404，原逻辑没有 fallback，导致误报。已通过代码结构确认该路径会产生用户看到的文案。
- H2: 按钮常驻导致用户在没有新版本时也会主动触发“检查更新”，和期望的“没更新新版本时隐藏”不一致。已通过 UI 初始化代码确认。
- H3: 文件本身编码正常，早先乱码来自 PowerShell 输出编码。已用 UTF-8 读取确认。

---

## Current Consolidated Understanding

修复方向是让程序启动后静默检查更新，只在发现高于 `APP_VERSION` 的 Release 时显示按钮；同时给 `/releases/latest` 的 404 增加 releases 列表回退，避免仓库已有发布时误判为无发布。
