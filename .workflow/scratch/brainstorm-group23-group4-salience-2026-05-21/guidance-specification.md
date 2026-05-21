# Brainstorm Guidance Specification

## 1. Project Positioning & Goals

本轮 brainstorm 聚焦 `prompts/2.group-image/组图 23.md` 与 `prompts/2.group-image/组图 4.md` 的差异显著性增强。

目标：在 **不改变现有链路结构**、**不扩大差异区域**、**不回退已确认硬约束** 的前提下，让差异点对中老年用户更容易第一眼发现。

核心结果：
- `组图 23` 的 List 2 MUST 从“合规但偏弱”升级为“单点、小区域、第一眼可见”。
- `组图 4` MUST 不再只满足面积阈值，而要满足更强的视觉可读性。
- 两份 prompt 都 MUST 优先使用抽象差异类别，而不是固定例子堆砌。

## 2. Concepts & Terminology

| Term | Definition | Category |
|---|---|---|
| first-glance visibility | 首次扫视 1 秒内即可定位的差异可见性 | core |
| bounded difference | 差异集中在单个局部，不跨多个主体，不扩散成大片改面 | core |
| structural discontinuity | 轮廓、边界、连接、开合、完整性出现明显中断 | technical |
| micro-trace | 需细看才发现的细线、细点、细裂纹、轻微磨损等低可见变化 | technical |
| large carrier surface | 地板、毛毯、整墙、整窗帘、大片家具表层等大块承载面 | technical |
| category collapse | 模型反复生成少数固定模板，导致差异单一化 | business |
| cold-zone fill | 优先在冷区补点，而非把差异继续堆在热区 | core |

## 3. Non-Goals

- MUST NOT 改动盲盒 20 类别体系。
- MUST NOT 改动桌面工具、表情库或现有链路结构。
- MUST NOT 用颜色、材质、纹理前缀去增强可见性。
- MUST NOT 依赖少数固定例子来驱动“明显变化”。
- MUST NOT 通过大面积背景或大承载面改动来制造显著性。

## 4. UX Decisions

- 差异 MUST 优先体现为轮廓中断、开合反差、缺损、附着、异常连接、明显方向变化等高可读信号。
- 差异 SHOULD 在手机屏幕正常浏览下无需放大即可识别。
- 差异 MUST 保持“单点主信号”，避免同一点同时叠加多个变化维度。
- 差异 MUST NOT 依赖细小痕迹、弱纹理、轻微位移或低对比变化成立。

## 5. Subject-Matter Decisions

- `组图 23` 的 List 2 SHOULD 从 16 条提升为 18 条，以便在保持九宫格均匀覆盖的同时增加明显辅助差异的调度空间。
- `组图 23` 的 List 2 SHOULD 优先使用抽象类别：局部结构缺损、局部表面破坏、局部状态反转、局部异常附着/脱落、局部方向/连接异常。
- `组图 23` 的差异 MUST 维持“小区域但强信号”，不得扩散到相邻主体或演变成大面积破坏。
- `组图 4` MUST 把“变化面积 ≥ 30% 或存在感变化”升级为“面积阈值只是下限，第一眼可见性才是最终准入条件”。
- `组图 4` 的图案内容变化 SHOULD 只落在中小型独立承载物，不得落在地板、毛毯、整墙等大承载面。

## 6. Test Decisions

- 差异点 MUST 满足首次扫视可定位，不得依赖逐格对照。
- 差异点 MUST 同时满足：局部集中、边界清楚、单点独立、与周边不混圈。
- 若某差异“面积合规但仍需细看”，则 MUST 判不通过。
- 若某差异“很明显但已经影响大主体识别或扩散成大片变化”，则 MUST 判不通过。

## 7. Cross-Role Integration

- `组图 23`：优先增强 List 2 的显著性，再回头校验冷区、九宫格、紧邻互斥、类型轮换。
- `组图 4`：优先增强单点视觉信号，再校验 18 点配额、九宫格 2×9、类型配额与大背景稳定。
- 两份 prompt 都 SHOULD 用“类别 + 准入条件 + 禁止项”的规则表达，避免“举 3 个例子然后模型只学那 3 个”。

## 8. Risks & Constraints

- 风险 1：过度依赖破坏类信号，导致画面气质变脏。应以“局部、干净、边界清楚”为约束。
- 风险 2：为了显著而侵入大主体。必须坚持 bounded difference。
- 风险 3：为了防模板化而写得过虚。需要保留类别级约束与验收语言。

## 9. Feature Decomposition

| ID | Feature | Scope | Priority |
|---|---|---|---|
| F-001 | group23-list2-salience | 提升 `组图 23` List 2 的显著性，并临时增至 18 条 | P1 |
| F-002 | group4-visibility-salience | 提升 `组图 4` 差异点的第一眼可见性与准入标准 | P1 |

## Appendix: Decision Tracking

- CONFIRMED：保留九宫格覆盖、禁颜色/材质前缀、紧邻互斥、大主体禁改。
- CONFIRMED：中老年用户需要更明显但区域有限的差异。
- CONFIRMED：`组图 4` 的变化也可以更加明显。
- SELECTED：采用抽象差异类别而非固定物体范例。