---
title: "Quality Rules"
readMode: required
priority: medium
category: review
keywords:
  - quality
  - lint
  - rule
  - enforcement
---

# Quality Rules

## 全局硬规则

- 禁止脑补不可见对象、画外空间、遮挡后区域或身份不稳定对象
- 差异点遵守"一圈一物一变化"；不得依赖细线、小点、刻痕、碎屑、污渍、标签或价格签
- 不改人物骨架、姿态、头身朝向、四肢动作、支撑关系和贴邻热区
- 不做灯光、发光、明暗、阴影、高光、反光、滤光、投影或镜面成像变化
- 灯具、灯罩、灯泡、蜡烛火焰等照明对象不得整体消失、整体移动或替换成不发光物
- 新增、异物植入或替换为更大物体前，必须确认 Target 有完整可见且未被占用的可放置空间
- 位置字段只定位，不写颜色、材质、纹理、风格、明暗等外观修饰

## 盲盒数据质量门

- 四池各 50 条，池内唯一
- 条目真实、自然、第一眼可识别
- 修改后必须运行 `test_blind_box_content_model.py`
- 伪多样性检查：主词未变仅换前缀视为未修复

## 提示词输出质量门

- 固定输出格式，不做额外解释
- 数量配额必须精确满足
- 每条差异点第一眼可见，手机屏幕无需放大
- 自检项逐条通过

## Entries

<spec-entry category="quality" keywords="group23,expression,ordinary-label,face-only" date="2026-06-11" source="commit:ce18e76">

### 组图 23 普通标签不等于普通表情点

组图 23 中，标签 `普通` 不等于普通表情点；只有纯脸部字段变化才可按普通表情点规则处理，身体、姿态、头部朝向和四肢动作不变只作内部约束，不输出额外说明。

</spec-entry>

<spec-entry category="quality" keywords="group23,expression,face-fields,pose-lock" date="2026-06-11" source="commit:ce18e76">

### 组图 23 普通表情点只写脸部字段

组图 23 的普通表情点只能写脸部字段，包括眉、眼、脸颊、额头、嘴、牙齿、舌头、口边、脸侧；不得写身体状态、姿态、头部朝向、四肢动作、服装主体、发型、背景或地面变化。

</spec-entry>

<spec-entry category="rule" keywords="visual-difference,label-taxonomy,quota,weak-difference" date="2026-06-25" source="prompts/2.group-image/组图 23.md:v2.0.25">

### 视觉差异提示词应合并语义重叠标签

在找不同、组图差异等视觉差异提示词中，若两个标签本质承载同一类视觉变化，应优先合并标签，并用准入条件区分具体用法。不要为了类型配额保留重复标签，否则模型容易为满足配额生成小点、小线、小装饰、夹缝小物等弱差异。

</spec-entry>

<spec-entry category="rule" keywords="visual-difference,count-quota,quality-gate,strong-signal" date="2026-06-25" source="prompts/2.group-image/组图 23.md:v2.0.25">

### 差异数量不得优先于差异质量

在视觉差异提示词中，差异点数量、类型配额、空间覆盖都不能压过有效落点、强信号、不重叠。若剩余点只能依赖边缘、小标记、细线、无意义新增或热区冲突成立，应停止补点或降低数量，而不是凑满上限。

</spec-entry>

<spec-entry category="rule" keywords="visual-difference,add-object,carrier-zone,strong-signal" date="2026-06-25" source="prompts/2.group-image/组图 23.md:v2.0.25">

### 新增类差异必须具备真实物体性和稳定承载区

在视觉差异提示词中，新增类差异必须是可命名、可单独圈选、有明确体量和场景功能的真实物体，或整块可见内容区。细杆、线缆、树枝、窄边框、接缝、收边、远景局部、遮挡缝和贴边区不得作为新增承载体。

</spec-entry>

<spec-entry category="rule" keywords="visual-difference,color-change,attribute-change,weak-change" date="2026-06-25" source="prompts/2.group-image/组图 23.md:v2.0.25">

### 颜色变化只允许强信号整体变化

在视觉差异提示词中，颜色变化只有在整件独立物体或边界清楚的整块内容区发生高对比整体换色时才成立。局部小色块、颜色微调、材质、纹理、明暗、光照、反光变化仍属于弱差异。

</spec-entry>

<spec-entry category="rule" keywords="visual-difference,content-replacement,content-surface,sketch-line-ban" date="2026-06-25" source="prompts/2.group-image/组图 23.md:v2.0.25">

### 内容或图案替换只落在明确内容承载面

在视觉差异提示词中，内容或图案替换应只落在屏幕、画布、纸张、书页、包装正面、牌面、标识牌、相框画面等本来承载内容的区域。自然景观、头发、织物纹理、墙面、大表面、远景景观不得包装成内容替换；几条线、轮廓线、简笔画线也不应作为替换结果。

</spec-entry>

<spec-entry category="rule" keywords="visual-difference,person-feedback,hot-zone,label-bypass" date="2026-06-25" source="prompts/2.group-image/组图 23.md:v2.0.25">

### 人物反馈后禁止用通用标签绕行拆分同一人物

在视觉差异提示词中，同一人物已经承载表情或人物反馈后，不应再用颜色变化、内容替换、新增等通用标签修改其头发、头饰、耳饰、衣领、颈部、项链等邻近附属区。否则会把同一人物热区拆成多个弱差异。

</spec-entry>

<spec-entry category="quality" keywords="group23,expression,attachments,overlays" date="2026-06-11" source="commit:ce18e76">

### 组图 23 普通表情点不得承载外来物

组图 23 的普通表情点不得承载外来覆盖物或附属区内容，例如面具、口罩、眼罩、头套、纸片、布条、项链、领角、脖子饰品、耳饰或头饰。

</spec-entry>

<spec-entry category="quality" keywords="group23,list2,attachments,visual-hot-zone" date="2026-06-11" source="commit:ce18e76">

### 组图 23 表情点与附属区分流

组图 23 中，同一人物已使用普通表情点后，项链、脖子、领角等附属区只能出现在 List 2；不得与该表情差异同圈、贴边、重叠、近邻或落入同一头颈视觉热区。

</spec-entry>

<spec-entry category="quality" keywords="group23,prompt-maintenance,minimal-diff,three-changes" date="2026-06-11" source="commit:ce18e76">

### 组图 23 提示词优化采用最小必要修改

组图 23 的提示词优化应采用最小必要修改：不整体重写，不改动无问题内容，每次最多修改 3 处；优先删除、合并、替换，并说明每处修改原因。

</spec-entry>
