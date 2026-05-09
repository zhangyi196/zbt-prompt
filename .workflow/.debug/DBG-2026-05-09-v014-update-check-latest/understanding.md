# Understanding Document

**Session ID**: DBG-2026-05-09-v014-update-check-latest
**Bug Description**: v0.1.4 client still says it is the latest version after v0.1.5 was published
**Started**: 2026-05-09 16:00:00 +08:00

---

## Exploration Timeline

### Iteration 1 - Initial Exploration (2026-05-09)

#### Current Understanding

- The issue is specifically about a client that the user identifies as `v0.1.4`.
- GitHub already has a public `v0.1.5` release.
- The observed symptom is "still shows latest version", not "update check failed".

#### Evidence from Code Search

- The `v0.1.4` git tag code compares `APP_VERSION` against the latest GitHub Release version.
- The current main-branch code includes a `403/429` fallback via `releases/latest` redirect parsing.
- The release API endpoints are:
  - `https://api.github.com/repos/zhangyi196/zbt-prompt/releases/latest`
  - `https://api.github.com/repos/zhangyi196/zbt-prompt/releases?per_page=20`

#### New Evidence

- GitHub `releases/latest` currently returns `v0.1.5`.
- GitHub releases list also shows `v0.1.5` ahead of `v0.1.4`.
- GitHub metadata shows:
  - `v0.1.4` asset was updated on **2026-05-09 15:03 CST**.
  - `v0.1.5` was published on **2026-05-09 15:40 CST**.
- The current `v0.1.4` installer asset on GitHub is not the original historical asset:
  - current SHA256: `02bdd1d089a24fe5d9b95e3165ddf0c05ccb60bf75a47269c47fd35774590bc6`
  - current size: `14,042,322` bytes
- After extracting the rebuilt `v0.1.4` installer asset, the packaged script contains:
  - `APP_VERSION = "0.1.4"`
  - the newer `_resolve_latest_release_via_redirect` fallback logic

#### Reproduction Results

- Running the original `v0.1.4` tag code against the live API on this machine produced `HTTP 403 rate limit exceeded`.
- Running the current update-check logic with `APP_VERSION` forced to `0.1.4` produced:
  - `status = update_available`
  - `latest_version = 0.1.5`

#### Corrected Understanding

- ~~The current GitHub `v0.1.4` asset might secretly be `0.1.5`~~ -> The rebuilt `v0.1.4` asset still embeds `APP_VERSION = "0.1.4"`.
- ~~The release itself may not be marked latest~~ -> GitHub `releases/latest` already points to `v0.1.5`.
- ~~Updating the old `v0.1.4` asset today explains the “latest version” message~~ -> asset update time alone does not explain the symptom; live release metadata still points old clients to `v0.1.5`.

---

## Current Consolidated Understanding

### What We Know

- GitHub currently exposes `v0.1.5` as the latest public release.
- The currently downloadable `v0.1.4` installer asset was rebuilt on 2026-05-09 and is not byte-identical to the original `v0.1.4` asset.
- That rebuilt `v0.1.4` installer embeds `APP_VERSION = "0.1.4"` plus the newer `403` fallback logic.
- With that newer logic, a `0.1.4` client should now detect `v0.1.5` as an available update.
- The rebuilt `v0.1.5` one-file executable itself starts normally when launched directly on the build machine.
- PyInstaller official guidance for launching external programs from a frozen Windows app says the process should clear its `SetDllDirectoryW` override before starting external installers, because the modified DLL search path is inherited by child processes.

### What Was Disproven

- ~~`v0.1.5` release metadata is wrong~~
- ~~current `v0.1.4` asset is actually `0.1.5` under a different filename~~
- ~~the rebuilt `v0.1.5` executable is intrinsically broken~~

### Current Investigation Focus

- Why the upgraded `v0.1.5` install fails at first launch with `Failed to load Python DLL`.
- Most likely root cause:
  - the running PyInstaller `v0.1.4` app launches the installer while its own frozen-process DLL search overrides and `_PYI_*` environment variables are still active
  - the installer inherits that frozen runtime state
  - the installer then launches the newly installed `v0.1.5` app under the inherited state, causing the new frozen app to fail during bootstrap
