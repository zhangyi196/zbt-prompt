# Implementation Plan: Game Content Extraction UI Redesign

## 1. Requirements Summary

将 `Game content extraction` 从“主窗口盲盒/动物 + 人物表情弹窗”改为“单主窗口双工作区”：

- 顶部提供两个切换按钮：`盲盒物品/动物抽取` 与 `人物表情抽取`。
- 两个按钮在同一主窗口内切换内容。
- 默认展示盲盒物品/动物抽取。
- 人物表情抽取迁入主窗口，不再默认打开独立 `Toplevel`。
- UI 参考 `UI风格参考.png`：浅灰蓝背景、白色内容区、蓝色主操作、胶囊式切换、宽松间距。
- 保持现有业务逻辑、输入语法、历史机制、表情库解析和验证样例。

## 2. Architecture Decisions

### AD-1: Preserve Business Logic

不重写抽取算法、历史池、表情库解析和增强逻辑。改动集中在 UI 构建、控件挂载位置和样式。

### AD-2: Use Persistent Workspace Frames

主窗口创建两个持久 Frame：

- `self.blind_box_workspace`
- `self.expression_workspace`

切换时通过 `pack_forget()` / `pack()` 或 `tkraise()` 控制显示，避免反复销毁控件导致文本框内容、模板编号或按钮状态丢失。

### AD-3: Keep Existing Widget Attribute Names

继续保留以下实例属性，降低回归风险：

- 盲盒/动物：`input_entry`, `state_var`, `category_vars`, `category_spin_vars`, `animal_vars`, `animal_spin_vars`, `auto_paste_var`, `output_text`
- 表情：`expression_input_text`, `expression_output_text`, `expression_template_mode_var`, `expression_template_index_var`

### AD-4: Native Tkinter Style Translation

第一版不引入第三方 UI 依赖。使用 `ttk.Style`、Frame 背景色、padding、按钮选中态和内容面板层级模拟参考图；不追求完整阴影和真实圆角。

## 3. Task Breakdown

### IMPL-1: Build Main Shell and Workspace Switch

目标：把主窗口升级为有顶部切换按钮和内容容器的 UI 壳。

工作内容：

- 调整窗口尺寸，建议 `980x720` 或接近比例。
- 新增 `_configure_styles()`。
- 新增 `_build_header()` 或 `_build_workspace_switcher()`。
- 新增 `_show_workspace(name)`。
- `setup_ui()` 只负责组装主壳和两个工作区。

依赖：无。

验收：

- 启动后可见两个切换按钮。
- 默认显示盲盒物品/动物抽取。
- 点击按钮可切换工作区。

### IMPL-2: Move Blind Box / Animal UI Into Workspace

目标：把当前 `setup_ui()` 中的盲盒/动物控件迁入 `build_blind_box_workspace(parent)`。

工作内容：

- 保留原输入框、示例、状态勾选、物品类别、动物类别、操作按钮、历史重置、输出区。
- 删除原按钮区中的 `人物表情抽取` 按钮，因为顶层切换按钮承担入口。
- 保持所有原实例属性名与按钮 command。

依赖：IMPL-1。

验收：

- 原单行输入示例可继续使用。
- `开始抽取`、`清空输入`、`自动粘贴`、`复制结果`、三个历史重置按钮仍可用。
- `_parse_input` 旧格式不变。

### IMPL-3: Move Expression UI Into Workspace

目标：把当前 `open_expression_window()` 的内容迁入 `build_expression_workspace(parent)`。

工作内容：

- 在主窗口第二工作区中放置表情组输入框、模板策略、编号、说明、抽取/清空/复制按钮、增强后文本框。
- 复用 `extract_expression_content`、`clear_expression_content`、`copy_expression_result`。
- `open_expression_window()` 可改成兼容薄包装：调用 `_show_workspace("expression")` 并聚焦输入框；不再创建 `Toplevel`。
- 移除或停止使用 `expression_window` 生命周期清理逻辑。

依赖：IMPL-1。

验收：

- 点击 `人物表情抽取` 后同一窗口切换内容。
- 不弹出新窗口。
- 固定样例 `负向 / 困惑 / 单人 / 模板 4` 输出不变。
- 多组输入、重复增强、错误提示仍通过验证脚本。

### IMPL-4: Apply Reference-Inspired Visual Style

目标：使 UI 明显接近参考图，但保持 Tkinter 可靠性。

工作内容：

- 设置 root 背景为浅灰蓝。
- 主内容区使用白色或近白色。
- 顶部切换按钮用胶囊感布局和蓝色选中态。
- 主操作按钮使用蓝色强调；重置类按钮降低权重。
- 统一 LabelFrame、Entry、Spinbox、ScrolledText 周围 padding。
- 避免过度装饰，不引入不稳定图标资源。

依赖：IMPL-1、IMPL-2、IMPL-3。

验收：

- 视觉具备浅色背景、白色内容区、蓝色主操作和宽松间距。
- 中文文本不挤压、不遮挡。
- 两个工作区切换后布局稳定。

### IMPL-5: Update Docs and Run Verification

目标：同步文档并验证功能不回退。

工作内容：

- 更新 `Game content extraction/CLAUDE.md`：人物表情抽取已从独立 `Toplevel` 改为主窗口第二工作区。
- 更新 `agents.md`：记录 UI 新入口和验证命令。
- 运行 `python -m py_compile 'Game content extraction/内容抽取.py'`。
- 运行 `python -B '.workflow\\active\\WFS-game-content-expression-window\\.process\\verify_expression.py'`。
- 如环境允许，手动打开 GUI 检查两个按钮切换。

依赖：IMPL-1、IMPL-2、IMPL-3、IMPL-4。

验收：

- 文档与实际入口一致。
- 语法编译通过。
- 人物表情回归脚本通过。
- 记录是否完成 GUI 手动检查。

## 4. Implementation Strategy

推荐顺序执行，不建议并行：

1. IMPL-1 建壳层。
2. IMPL-2 迁移盲盒/动物 UI 并做快速语法检查。
3. IMPL-3 迁移人物表情 UI 并跑表情回归。
4. IMPL-4 做视觉样式。
5. IMPL-5 更新文档和最终验证。

原因：所有任务都集中在同一个 Python 文件，且控件属性共享，顺序执行能减少冲突。

## 5. Risk Assessment

- **中风险：控件属性丢失**  
  缓解：迁移时保留现有实例属性名，先移动 UI，再做样式。

- **中风险：表情文本框生命周期变化**  
  缓解：使用持久工作区 Frame，不在切换时销毁控件。

- **低风险：Tkinter 样式不能完全复刻参考图**  
  缓解：明确第一版做轻量转译，聚焦色彩、层级、间距和选中态。

- **低风险：文档滞后**  
  缓解：IMPL-5 单独覆盖 CLAUDE.md 和 agents.md。

## 6. Verification Commands

```powershell
python -m py_compile 'Game content extraction\内容抽取.py'
python -B '.workflow\active\WFS-game-content-expression-window\.process\verify_expression.py'
```

可选 GUI 检查：

```powershell
python 'Game content extraction\内容抽取.py'
```

