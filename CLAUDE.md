# 仓库维护说明

本仓库以中文提示词规则为主，`Game content extraction/` 为配套本地 `tkinter` 工具目录。

提示词文档优先采用“执行优先级前置、硬规则集中、输出格式固定”的写法，减少同义重复，提升模型稳定性。

## 发布边界

- 桌面工具正式发布继续沿用 `v0.1.x` 语义版本和安装包资产。
- 仓库源码打包到 GitHub Release 时，使用 source-bundle 命名，避免误导应用更新检查。
- 推荐 source-bundle tag：`v0.1.3-source-YYYYMMDD`
- 推荐 source-bundle 资产名：`zbt-prompt-v0.1.3-source-YYYYMMDD.zip`
- 不要为仅含仓库快照的 release 提升到高于当前正式桌面版本的 semver，否则应用会把它识别成可更新版本。

## 打包约定

- 优先使用 `git archive` 生成 zip，排除 `.git/` 等本地元数据。
- zip 内保留顶层目录前缀 `zbt-prompt/`。
- 本地临时打包产物放在 `.release-assets/`，不提交到仓库。
