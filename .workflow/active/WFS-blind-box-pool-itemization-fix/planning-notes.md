# Planning Notes: Blind Box Pool Itemization Fix

## Goal

修正 `Game content extraction` 盲盒物品库试点内容中 `conditional_items` 和 `blocked_or_risky` 的语义漂移问题：池层仍然是物品池，所有条目必须是具体物品；折线、擦痕、气泡、阴影、边线、微小颗粒等非物品表达只作为测试禁用模式存在。

## Source Context

- Spec: `.workflow/.spec/SPEC-2026-04-29-blind-box-pool-itemization-fix/`
- Brainstorm: `.workflow/.brainstorm/BS-2026-04-29-盲盒条件风险池物品化修正/`
- Prior implementation session: `.workflow/active/WFS-game-content-blind-box-library-refactor/`

## Key Constraints

- 仅修正三个试点盒：15 `桌面+学习`、16 `海底+潜水`、17 `公园+野餐`。
- 不改 `BLIND_BOXES` 四栏 runtime contract：`large`、`medium`、`small`、`hanging`。
- 不改 UI、输入语法、历史 key、盒号、版本发布流程。
- `blocked_or_risky` 不得进入默认抽取结果。
- `conditional_items` 需要是中等体量或更大、可独立看见/圈选、仅在特定承载环境启用的具体物品。
- `blocked_or_risky` 需要是具体风险物，例如透明、反光、发光、细长悬挂、动物本体、易误判对象；不得是痕迹、线条、阴影、气泡、颗粒等非物品。

## Observed Current State

- `Game content extraction/data/blind_boxes.py` 已有三类试点五层池。
- 现有问题条目包括：
  - `纸张边缘折线`、`微小擦痕`
  - `细小气泡串`、`漂浮细海草丝`、`海底阴影斑`、`水面高光`、`微小沙粒`
  - `草地碎叶点`、`地面细小石子`、`风吹纸片边缘`、`野餐垫边线`、`微小污点`
- `Game content extraction/test_blind_box_content_model.py` 已覆盖五层 schema、runtime bucket contract、blocked leakage、pilot input override、state filter，但还没有 forbidden patterns 覆盖。

## Planning Decision

采用顺序执行：

1. 先替换 `conditional_items`，建立正确正向样板。
2. 再替换 `blocked_or_risky`，移除非物品表达。
3. 增加 forbidden pattern 测试锁定规则。
4. 同步维护文档和 workflow 状态。
