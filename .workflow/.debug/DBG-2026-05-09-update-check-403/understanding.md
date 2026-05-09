# Understanding Document

**Session ID**: DBG-2026-05-09-update-check-403
**Bug Description**: 当前检查更新点击后返回 403 报错
**Started**: 2026-05-09 00:00:00 +08:00

---

## Exploration Timeline

### Iteration 1 - Initial Exploration (2026-05-09)

#### Current Understanding

- 手动点击 `检查更新` 会走 `内容抽取.py` 中的 `_fetch_latest_release()`。
- 当前实现先请求 GitHub API 的 `/releases/latest`，只有 `404` 才会降级到 `/releases?per_page=20`。
- 对 `403` 没有额外兜底，因此会直接向用户显示 `GitHub 返回 HTTP 403`。

#### Evidence from Code Search

- `Game content extraction/内容抽取.py` 的 `_fetch_latest_release()` 仅对 `404` 做降级处理。
- `Game content extraction/test_update_check.py` 已覆盖 `404` 回退场景，但没有覆盖 `403`。
- 历史会话 `DBG-2026-04-28-update-check-private-release` 记录过 GitHub 无认证请求在仓库公开后仍可能触发 `403 rate limit`。

#### Hypotheses Generated

- H1: GitHub API 403 来自无认证限流，当前代码缺少非 API 兜底。
- H2: 403 不是版本解析问题，而是请求通道问题；只要能绕过 API，现有版本比较逻辑仍可复用。
- H3: 现有手动检查按钮行为变更后，旧测试对“隐藏按钮”的断言也需要同步更新。

### Iteration 2 - Resolution (2026-05-09)

#### Fix Applied

- 为 `403/429` 增加 GitHub `releases/latest` 页面重定向兜底，通过最终 URL 解析最新版本。
- 保留现有 API 优先路径和 `404 -> releases list` 回退逻辑。
- 新增 403 回退测试，并把“无更新时隐藏按钮”的旧断言更新为“恢复为可见的手动检查按钮”。

#### Verification Results

- `python -B -m unittest discover -s 'Game content extraction' -p 'test_update_check.py'` 通过。
- `python -B -m py_compile 'Game content extraction/内容抽取.py'` 通过。

#### Lessons Learned

1. GitHub 更新检查不能只依赖 API 成功路径，手动检查需要有非 API 兜底。
2. UI 行为改动后，相关单测要同步更新，否则会制造假回归。

---

## Current Consolidated Understanding

### What We Know

- 当前 403 的直接原因是 GitHub API 请求被拒绝，而不是版本比较逻辑失效。
- `https://github.com/.../releases/latest` 的重定向链可以作为手动检查时的可靠兜底来源。
- 修复需要同时覆盖代码路径和测试路径。

### What Was Disproven

- ~~版本号解析错误导致 403~~：403 发生在请求层，版本解析尚未执行。

### Current Investigation Focus

确认回退逻辑在本地测试中稳定通过，并同步更新 README 中的更新说明。
