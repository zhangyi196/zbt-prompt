# zbt prompt

本仓库主要维护中文提示词规则，并包含配套本地 `tkinter` 工具目录 `Game content extraction/`。

## 目录说明

- `主图 第二步 .md`：候选物审核与摆放规则，采用“优先级 + 硬规则 + 固定输出”的稳定写法。
- `组图 4.md`：找不同润色规则。
- `组图 23 表情前置.md`：剧情表情类别前置规则。
- `组图 23 表情库.md`：人物表情模板库。
- `组图 23.md`：Ref-A / Ref-B 到 Target 的差异迁移规则。
- `Game content extraction/`：本地 `tkinter` 小工具，详细说明见 [Game content extraction/README.md](Game%20content%20extraction/README.md)。

## 仓库打包发布

仓库源码打包发布到 GitHub Release 时，使用保留目录结构的 zip 资产，不直接上传文件夹。

- 推荐资产名：`zbt-prompt-v0.1.3-source-YYYYMMDD.zip`
- 推荐 tag：`v0.1.3-source-YYYYMMDD`
- 该类 source-bundle release 只用于分发仓库快照，不作为桌面工具新版本发布
- tag 必须保持版本规范化后仍为当前正式桌面版本，避免触发应用内“发现新版本”提示

## 桌面工具发布

当前桌面工具发布版为 `v0.1.3`，安装包为 `GameContentExtraction-Setup-v0.1.3.exe`。

桌面工具版本、安装包和更新检查约定仍以 `Game content extraction/` 下文档为准，不因源码打包 release 改变。
