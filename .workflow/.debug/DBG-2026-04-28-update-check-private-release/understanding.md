# Understanding Document

**Session ID**: DBG-2026-04-28-update-check-private-release
**Bug Description**: 0.1.4 安装包发布后，0.1.3 安装包没有显示检查更新按钮
**Started**: 2026-04-28 14:56:16 +08:00

---

## Exploration Timeline

### Iteration 1 - Initial Exploration (2026-04-28 14:56)

#### Current Understanding

- 0.1.3 的更新检查在启动后静默调用 GitHub Releases API。
- 静默检查失败时不会弹出错误，只会保持 `发现新版本` 按钮隐藏。
- `gh release list` 能看到 `v0.1.4` 是 Latest，但程序同款无认证请求最初对 `/releases/latest` 返回 404。

#### Evidence from Code Search

- `Game content extraction/内容抽取.py` 使用 `UPDATE_API_URL = https://api.github.com/repos/zhangyi196/zbt-prompt/releases/latest`。
- `_fetch_latest_release()` 只有拿到高于 `APP_VERSION` 的版本时才返回 `update_available`。
- `_handle_update_result(..., silent=True)` 对错误结果不显示提示。
- `gh repo view zhangyi196/zbt-prompt --json visibility` 显示仓库原先为 `PRIVATE`。

#### Hypotheses Generated

- H1: GitHub Release 没有发布为 latest。已排除，`gh release list` 显示 `v0.1.4 Latest`。
- H2: 旧版 0.1.3 的版本比较逻辑无法识别 `v0.1.4`。已排除，代码会把 `v0.1.3` 与 `v0.1.4` 正确比较为可更新。
- H3: 仓库 private 导致无认证 API 返回 404，静默检查隐藏按钮。已确认。

### Iteration 2 - Resolution (2026-04-28 14:56)

#### Fix Applied

- 用户选择公开仓库后，执行 `gh repo edit zhangyi196/zbt-prompt --visibility public --accept-visibility-change-consequences`。
- `gh repo view` 复查显示仓库可见性已为 `PUBLIC`。

#### Verification Results

- 无认证 `curl` 请求 `https://api.github.com/repos/zhangyi196/zbt-prompt/releases/latest` 返回 `HTTP/1.1 200 OK`。
- 响应中的 `tag_name` 为 `v0.1.4`，`draft=false`，`prerelease=false`，资产为 `GameContentExtraction-Setup-v0.1.4.exe`。
- 当前 Python `urllib` 无认证请求随后遇到 GitHub API rate limit，返回 403，reset 时间为 `2026-04-28 15:28:33 +08:00`；这是公开后的临时限流，不再是 private 404。

---

## Current Consolidated Understanding

### What We Know

- 根因是仓库为 private，0.1.3 安装包没有 GitHub 认证信息，访问 release API 得到 404。
- 因为 0.1.3 是静默启动检查，错误不会弹窗，所以用户看到的是“检查更新按钮没有出现”。
- 仓库公开后，无认证 API 已能读到 `v0.1.4`。

### What Was Disproven

- ~~`v0.1.4` 不是 latest~~：GitHub CLI 看到 `v0.1.4 Latest`。
- ~~版本号比较失败~~：0.1.3 代码路径能比较 `0.1.3 < 0.1.4`。

### Remaining Notes

- 若 GitHub 无认证 API 暂时返回 403 rate limit exceeded，0.1.3 仍会隐藏按钮；等待 reset 时间后重新打开 0.1.3 即可触发更新按钮。
