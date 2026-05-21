# Roadmap: zbt-prompt

## Overview

本轮继续优化组图提示词的可见性与分布质量，重点把 `组图 23` 的辅助差异从“合规补点”提升为“第一眼可见的小区域强信号”，同时把 `组图 4` 的变化显著性从“面积达标”提升为“首屏可见”。所有改动仍限制在 prompt 文案层，不改变现有链路、表情库、盲盒数据或桌面工具。

## Phases

- [ ] **Phase 1: 组图显著性定向增强** - 提升组图23辅助差异显著性，并增强组图4第一眼可见性

## Phase Details

### Phase 1: 组图显著性定向增强

**Goal**: 在不破坏既有硬约束的前提下，同时提升 `组图 23.md` 的 List 2 显著性与 `组图 4.md` 的第一眼可见性

**Depends on**: Nothing (first phase)

**Requirements**: REQ-001, REQ-002, REQ-003, REQ-004

**Success Criteria** (what must be TRUE):
  1. `组图 23.md` 的 List 2 能以抽象差异类别表达更明显的小区域变化，且临时提升到 18 条仍不破坏九宫格覆盖、紧邻互斥与对象指代禁令
  2. `组图 4.md` 的差异点在保留 18 点与九宫格 2×9 的前提下，必须满足第一眼可见的更高准入标准，而不只是面积下限
  3. 两份 prompt 都继续满足禁颜色/材质前缀、大主体禁改、冷区优先与空间均匀分布约束
  4. 相关 `agents.md`、自检项和一致性描述同步更新，避免规则分叉

## Scope Decisions

- **In scope**: `prompts/2.group-image/组图 23.md`、`prompts/2.group-image/组图 4.md`、`prompts/2.group-image/agents.md` 与其配套自检的显著性增强
- **Deferred**: 主图链路、绿圈洗图、表情库、盲盒数据、桌面工具、链路结构变更
- **Out of scope**: 任何会改变现有差异点生成流程结构的改动

## Progress

| Phase | Status | Completed |
|-------|--------|-----------|
| 1. 组图显著性定向增强 | Not started | - |

---
*Updated: 2026-05-21*
