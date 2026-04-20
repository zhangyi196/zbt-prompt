import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import os
import random
import re
import sys
from data.animals import ANIMALS
from data.blind_boxes import BLIND_BOXES
from data.item_states import ITEM_STATE_GROUPS, ITEM_STATE_GROUP_WEIGHTS

class BlindBoxExtractor:
    UI_COLORS = {
        "app_bg": "#eef4f8",
        "panel_bg": "#ffffff",
        "surface_bg": "#f7fbff",
        "line": "#d8e2ec",
        "muted_text": "#6f7f90",
        "text": "#1f2937",
        "blue": "#1687d9",
        "blue_hover": "#0f75bd",
        "blue_soft": "#e7f1ff",
        "field_bg": "#fbfdff",
    }
    UI_FONT = ("Microsoft YaHei UI", 10)
    UI_FONT_BOLD = ("Microsoft YaHei UI", 10, "bold")

    def __init__(self, root):
        self.root = root
        self.root.title("游戏内容抽取软件")
        self.root.geometry("980x720")
        
        # Static content lives in data/ so this file can focus on logic.
        self.item_state_groups = ITEM_STATE_GROUPS
        self.item_state_group_weights = ITEM_STATE_GROUP_WEIGHTS


        self.category_info = [
            ("large", "大型物品"),
            ("medium", "中型物品"),
            ("small", "散落小型物品"),
            ("hanging", "悬挂物品"),
        ]

        self.animal_info = [
            ("动物本体", "动物本体"),
            ("动物用品", "动物用品"),
            ("动物痕迹", "动物痕迹"),
        ]

        self.input_override_targets = {
            label: ("category", key) for key, label in self.category_info
        }
        self.input_override_targets.update({
            label: ("animal", key) for key, label in self.animal_info
        })
        
        self.blind_boxes = BLIND_BOXES
        self.animals = ANIMALS
        self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "draw_history.json")
        self.draw_history = self._load_draw_history()
        self.expression_window = None
        self.expression_input_text = None
        self.expression_output_text = None
        self.expression_template_mode_var = None
        self.expression_template_index_var = None
        self.workspace_buttons = {}
        self.workspace_frames = {}
        self.current_workspace = None
        self.setup_ui()

    
    def _create_empty_draw_history(self):
        return {
            "version": 1,
            "item_pools": {},
            "animal_pools": {},
        }

    def _load_draw_history(self):
        history = self._create_empty_draw_history()

        if not os.path.exists(self.history_file):
            self.draw_history = history
            self._save_draw_history()
            return history

        try:
            with open(self.history_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            self.draw_history = history
            self._save_draw_history()
            return history

        if isinstance(data, dict):
            item_pools = data.get("item_pools", {})
            animal_pools = data.get("animal_pools", {})
            history["item_pools"] = item_pools if isinstance(item_pools, dict) else {}
            history["animal_pools"] = animal_pools if isinstance(animal_pools, dict) else {}

        self.draw_history = history
        self._save_draw_history()
        return history

    def _save_draw_history(self):
        with open(self.history_file, "w", encoding="utf-8") as file:
            json.dump(self.draw_history, file, ensure_ascii=False, indent=2)

    def _make_item_pool_key(self, box_id, category_key):
        return f"box:{box_id}:{category_key}"

    def _make_animal_pool_key(self, animal_type, category_key):
        return f"animal:{animal_type}:{category_key}"

    def _get_or_init_pool_state(self, pool_group, pool_key, items):
        pool_state = pool_group.setdefault(
            pool_key,
            {
                "seen_in_cycle": [],
                "cooldown": {},
            },
        )

        if not isinstance(pool_state, dict):
            pool_state = {
                "seen_in_cycle": [],
                "cooldown": {},
            }
            pool_group[pool_key] = pool_state

        item_set = set(items)
        seen_raw = pool_state.get("seen_in_cycle", [])
        if not isinstance(seen_raw, list):
            seen_raw = []
        pool_state["seen_in_cycle"] = list(dict.fromkeys(item for item in seen_raw if item in item_set))

        cooldown_raw = pool_state.get("cooldown", {})
        if not isinstance(cooldown_raw, dict):
            cooldown_raw = {}

        normalized_cooldown = {}
        for item in items:
            raw_value = cooldown_raw.get(item, 0)
            try:
                value = int(raw_value)
            except (TypeError, ValueError):
                value = 0
            normalized_cooldown[item] = max(0, value)

        pool_state["cooldown"] = normalized_cooldown
        return pool_state

    def _decay_pool_cooldown(self, pool_state, items):
        cooldown_map = pool_state["cooldown"]
        for item in items:
            cooldown_map[item] = max(0, cooldown_map.get(item, 0) - 1)

    def _weighted_pick(self, items, cooldown_map, count, exclude=None):
        excluded_items = set(exclude or [])
        available_items = [item for item in items if item not in excluded_items]
        selected_items = []

        while available_items and len(selected_items) < count:
            weights = [
                max(0.15, 1 / (1 + max(0, cooldown_map.get(item, 0))))
                for item in available_items
            ]
            chosen_item = random.choices(available_items, weights=weights, k=1)[0]
            selected_items.append(chosen_item)
            available_items.remove(chosen_item)

        return selected_items

    def _draw_from_history_pool(self, pool_group, pool_key, items, count):
        if count <= 0 or not items:
            return []

        actual_count = min(count, len(items))
        pool_state = self._get_or_init_pool_state(pool_group, pool_key, items)
        self._decay_pool_cooldown(pool_state, items)

        seen_items = set(pool_state["seen_in_cycle"])
        unseen_items = [item for item in items if item not in seen_items]
        selected_items = self._weighted_pick(
            unseen_items,
            pool_state["cooldown"],
            min(actual_count, len(unseen_items)),
        )

        remaining_count = actual_count - len(selected_items)
        if remaining_count > 0:
            selected_items.extend(
                self._weighted_pick(
                    items,
                    pool_state["cooldown"],
                    remaining_count,
                    exclude=selected_items,
                )
            )

        for item in selected_items:
            if item not in seen_items:
                pool_state["seen_in_cycle"].append(item)
                seen_items.add(item)
            pool_state["cooldown"][item] = min(6, pool_state["cooldown"].get(item, 0) + 3)

        if len(pool_state["seen_in_cycle"]) >= len(items):
            pool_state["seen_in_cycle"] = []

        return selected_items

    def _show_output_message(self, message):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message)

    def _reset_item_history(self):
        self.draw_history["item_pools"] = {}
        self._save_draw_history()
        self._show_output_message("物品抽取历史已重置")

    def _reset_animal_history(self):
        self.draw_history["animal_pools"] = {}
        self._save_draw_history()
        self._show_output_message("动物抽取历史已重置")

    def _reset_all_history(self):
        self.draw_history["item_pools"] = {}
        self.draw_history["animal_pools"] = {}
        self._save_draw_history()
        self._show_output_message("全部抽取历史已重置")

    def setup_ui(self):
        self._configure_styles()

        self.app_shell = ttk.Frame(self.root, style="App.TFrame")
        self.app_shell.pack(fill=tk.BOTH, expand=True)

        self._build_workspace_switcher(self.app_shell)

        self.workspace_host = ttk.Frame(
            self.app_shell,
            style="WorkspaceHost.TFrame",
            padding=(18, 16),
            borderwidth=1,
            relief="solid",
        )
        self.workspace_host.pack(padx=24, pady=(0, 24), fill=tk.BOTH, expand=True)

        self.blind_box_workspace = ttk.Frame(self.workspace_host, style="Workspace.TFrame")
        self.expression_workspace = ttk.Frame(self.workspace_host, style="Workspace.TFrame")
        self.workspace_frames = {
            "blind_box": self.blind_box_workspace,
            "expression": self.expression_workspace,
        }

        self._build_blind_box_workspace(self.blind_box_workspace)
        self._build_expression_workspace(self.expression_workspace)
        self._show_workspace("blind_box")

    def _configure_styles(self):
        colors = self.UI_COLORS
        self.root.configure(bg=colors["app_bg"])
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(".", font=self.UI_FONT)
        self.style.configure("TFrame", background=colors["panel_bg"])
        self.style.configure("TLabel", background=colors["panel_bg"], foreground=colors["text"])
        self.style.configure("TCheckbutton", background=colors["panel_bg"], foreground=colors["text"])
        self.style.configure("TRadiobutton", background=colors["panel_bg"], foreground=colors["text"])
        self.style.configure("TEntry", fieldbackground=colors["field_bg"], foreground=colors["text"])
        self.style.configure("TSpinbox", fieldbackground=colors["field_bg"], foreground=colors["text"])
        self.style.configure(
            "TLabelframe",
            background=colors["panel_bg"],
            bordercolor=colors["line"],
            lightcolor=colors["line"],
            darkcolor=colors["line"],
            padding=(12, 10),
        )
        self.style.configure(
            "TLabelframe.Label",
            background=colors["panel_bg"],
            foreground=colors["text"],
            font=self.UI_FONT_BOLD,
        )
        self.style.configure("App.TFrame", background=colors["app_bg"])
        self.style.configure("Header.TFrame", background=colors["app_bg"])
        self.style.configure(
            "SwitchBar.TFrame",
            background=colors["panel_bg"],
            bordercolor=colors["line"],
            lightcolor=colors["line"],
            darkcolor=colors["line"],
        )
        self.style.configure(
            "WorkspaceHost.TFrame",
            background=colors["panel_bg"],
            bordercolor=colors["line"],
            lightcolor=colors["line"],
            darkcolor=colors["line"],
        )
        self.style.configure("Workspace.TFrame", background=colors["panel_bg"])
        self.style.configure("Muted.TLabel", background=colors["panel_bg"], foreground=colors["muted_text"])
        self.style.configure(
            "Switcher.TButton",
            padding=(18, 8),
            background=colors["surface_bg"],
            foreground=colors["text"],
            bordercolor=colors["line"],
            focusthickness=0,
        )
        self.style.configure(
            "ActiveSwitcher.TButton",
            padding=(18, 8),
            background=colors["blue_soft"],
            foreground=colors["blue"],
            bordercolor=colors["blue_soft"],
            font=self.UI_FONT_BOLD,
            focusthickness=0,
        )
        self.style.configure(
            "Primary.TButton",
            padding=(16, 8),
            background=colors["blue"],
            foreground="#ffffff",
            bordercolor=colors["blue"],
            font=self.UI_FONT_BOLD,
            focusthickness=0,
        )
        self.style.configure(
            "Secondary.TButton",
            padding=(14, 7),
            background=colors["surface_bg"],
            foreground=colors["text"],
            bordercolor=colors["line"],
            focusthickness=0,
        )
        self.style.map(
            "Primary.TButton",
            background=[("pressed", colors["blue_hover"]), ("active", colors["blue_hover"])],
            foreground=[("pressed", "#ffffff"), ("active", "#ffffff")],
        )
        self.style.map(
            "ActiveSwitcher.TButton",
            background=[("pressed", colors["blue_soft"]), ("active", colors["blue_soft"])],
            foreground=[("pressed", colors["blue"]), ("active", colors["blue"])],
        )
        self.style.map(
            "Switcher.TButton",
            background=[("pressed", colors["blue_soft"]), ("active", colors["blue_soft"])],
            foreground=[("pressed", colors["blue"]), ("active", colors["blue"])],
        )

    def _build_workspace_switcher(self, parent):
        header_frame = ttk.Frame(parent, style="Header.TFrame")
        header_frame.pack(padx=24, pady=(22, 14), fill=tk.X)

        switcher_frame = ttk.Frame(
            header_frame,
            style="SwitchBar.TFrame",
            padding=6,
            borderwidth=1,
            relief="solid",
        )
        switcher_frame.pack(side=tk.LEFT)

        self.workspace_buttons = {
            "blind_box": ttk.Button(
                switcher_frame,
                text="盲盒物品/动物抽取",
                style="Switcher.TButton",
                command=lambda: self._show_workspace("blind_box"),
            ),
            "expression": ttk.Button(
                switcher_frame,
                text="人物表情抽取",
                style="Switcher.TButton",
                command=lambda: self._show_workspace("expression"),
            ),
        }
        self.workspace_buttons["blind_box"].pack(side=tk.LEFT, padx=(0, 6))
        self.workspace_buttons["expression"].pack(side=tk.LEFT)

    def _show_workspace(self, name):
        if name not in self.workspace_frames:
            raise ValueError(f"未知工作区：{name}")

        for workspace_name, frame in self.workspace_frames.items():
            if workspace_name == name:
                frame.pack(fill=tk.BOTH, expand=True)
            else:
                frame.pack_forget()

        for workspace_name, button in self.workspace_buttons.items():
            button.configure(
                style="ActiveSwitcher.TButton" if workspace_name == name else "Switcher.TButton"
            )

        self.current_workspace = name

    def _build_blind_box_workspace(self, parent):
        input_frame = ttk.Frame(parent)
        input_frame.pack(pady=(4, 8), fill=tk.X)
        ttk.Label(input_frame, text="盲盒数字/动物类型(逗号分隔):").pack(side=tk.LEFT, padx=(0, 10))
        self.input_entry = ttk.Entry(input_frame, width=36)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            parent,
            text="示例：1,5,地面动物,无大型物品,中型物品+1",
            style="Muted.TLabel",
        ).pack(anchor=tk.W)

        state_frame = ttk.Frame(parent)
        state_frame.pack(pady=(12, 8), fill=tk.X)
        self.state_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(state_frame, text="启用物品状态", variable=self.state_var).pack(side=tk.LEFT)

        category_frame = ttk.LabelFrame(parent, text="物品类别与抽取数量")
        category_frame.pack(pady=(4, 10), fill=tk.X)

        self.category_vars = {}
        self.category_spin_vars = {}
        for key, label in self.category_info:
            row_frame = ttk.Frame(category_frame)
            row_frame.pack(fill=tk.X, pady=4)

            var = tk.BooleanVar(value=True)
            self.category_vars[key] = var
            ttk.Checkbutton(row_frame, text=label, variable=var).pack(side=tk.LEFT, padx=(0, 14))

            ttk.Label(row_frame, text="数量:").pack(side=tk.LEFT)
            default_count = 1 if key != "medium" else 2
            spin_var = tk.IntVar(value=default_count)
            self.category_spin_vars[key] = spin_var
            tk.Spinbox(
                row_frame,
                from_=1,
                to=5,
                width=3,
                textvariable=spin_var,
                state="readonly",
                **self._spinbox_style_options(),
            ).pack(side=tk.LEFT, padx=6)

        animal_frame = ttk.LabelFrame(parent, text="动物内容与抽取数量")
        animal_frame.pack(pady=(0, 12), fill=tk.X)

        self.animal_vars = {}
        self.animal_spin_vars = {}
        for key, label in self.animal_info:
            row_frame = ttk.Frame(animal_frame)
            row_frame.pack(fill=tk.X, pady=4)

            default_selected = key == "动物本体"
            var = tk.BooleanVar(value=default_selected)
            self.animal_vars[key] = var
            ttk.Checkbutton(row_frame, text=label, variable=var).pack(side=tk.LEFT, padx=(0, 14))

            ttk.Label(row_frame, text="数量:").pack(side=tk.LEFT)
            spin_var = tk.IntVar(value=1)
            self.animal_spin_vars[key] = spin_var
            tk.Spinbox(
                row_frame,
                from_=1,
                to=5,
                width=3,
                textvariable=spin_var,
                state="readonly",
                **self._spinbox_style_options(),
            ).pack(side=tk.LEFT, padx=6)

        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=(2, 14))

        ttk.Button(button_frame, text="开始抽取", command=self.extract, style="Primary.TButton").pack(side=tk.LEFT, padx=8)

        clear_frame = ttk.Frame(button_frame)
        clear_frame.pack(side=tk.LEFT, padx=8)
        ttk.Button(clear_frame, text="清空输入", command=self.clear_input, style="Secondary.TButton").pack(side=tk.LEFT)
        self.auto_paste_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(clear_frame, text="自动粘贴", variable=self.auto_paste_var).pack(side=tk.LEFT, padx=(8, 0))

        ttk.Button(button_frame, text="复制结果", command=self.copy_to_clipboard, style="Secondary.TButton").pack(side=tk.LEFT, padx=8)

        ttk.Label(parent, text="提示词输出:", font=self.UI_FONT_BOLD).pack(anchor=tk.W)
        history_button_frame = ttk.Frame(parent)
        history_button_frame.pack(pady=(8, 10))
        ttk.Button(history_button_frame, text="重置物品历史", command=self._reset_item_history, style="Secondary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(history_button_frame, text="重置动物历史", command=self._reset_animal_history, style="Secondary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(history_button_frame, text="重置全部历史", command=self._reset_all_history, style="Secondary.TButton").pack(side=tk.LEFT, padx=5)

        self.output_text = scrolledtext.ScrolledText(parent, height=22, width=100)
        self._style_text_widget(self.output_text)
        self.output_text.pack(pady=(0, 2), fill=tk.BOTH, expand=True)

    def _build_expression_workspace(self, parent):
        ttk.Label(parent, text="表情组文本:", font=self.UI_FONT_BOLD).pack(pady=(4, 6), anchor=tk.W)
        self.expression_input_text = scrolledtext.ScrolledText(parent, height=12, width=92)
        self._style_text_widget(self.expression_input_text)
        self.expression_input_text.pack(pady=(0, 12), fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(parent)
        control_frame.pack(pady=(0, 12), fill=tk.X)

        self.expression_template_mode_var = tk.StringVar(value="specified")
        ttk.Radiobutton(
            control_frame,
            text="指定模板编号",
            variable=self.expression_template_mode_var,
            value="specified",
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Radiobutton(
            control_frame,
            text="随机模板",
            variable=self.expression_template_mode_var,
            value="random",
        ).pack(side=tk.LEFT, padx=(0, 12))

        ttk.Label(control_frame, text="编号:").pack(side=tk.LEFT)
        self.expression_template_index_var = tk.IntVar(value=4)
        tk.Spinbox(
            control_frame,
            from_=1,
            to=8,
            width=4,
            textvariable=self.expression_template_index_var,
            state="readonly",
            **self._spinbox_style_options(),
        ).pack(side=tk.LEFT, padx=5)
        ttk.Label(control_frame, text="单人 1-4，多人 5-8", style="Muted.TLabel").pack(side=tk.LEFT, padx=10)

        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=(0, 14))
        ttk.Button(button_frame, text="抽取表情", command=self.extract_expression_content, style="Primary.TButton").pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="清空", command=self.clear_expression_content, style="Secondary.TButton").pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="复制结果", command=self.copy_expression_result, style="Secondary.TButton").pack(side=tk.LEFT, padx=8)

        ttk.Label(parent, text="增强后文本:", font=self.UI_FONT_BOLD).pack(pady=(0, 6), anchor=tk.W)
        self.expression_output_text = scrolledtext.ScrolledText(parent, height=14, width=92)
        self._style_text_widget(self.expression_output_text)
        self.expression_output_text.pack(pady=(0, 2), fill=tk.BOTH, expand=True)

    def _style_text_widget(self, widget):
        colors = self.UI_COLORS
        widget.configure(
            bg=colors["field_bg"],
            fg=colors["text"],
            insertbackground=colors["blue"],
            selectbackground=colors["blue_soft"],
            selectforeground=colors["text"],
            relief=tk.SOLID,
            bd=1,
            padx=10,
            pady=8,
            font=self.UI_FONT,
            wrap=tk.WORD,
        )

    def _spinbox_style_options(self):
        colors = self.UI_COLORS
        return {
            "bg": colors["field_bg"],
            "buttonbackground": colors["surface_bg"],
            "foreground": colors["text"],
            "readonlybackground": colors["field_bg"],
            "relief": tk.SOLID,
            "bd": 1,
            "font": self.UI_FONT,
        }

    def _parse_input(self, input_str):
        normalized_input = (
            input_str
            .replace("，", ",")
            .replace("＋", "+")
            .replace("－", "-")
        )
        parts = [part.strip() for part in normalized_input.split(",") if part.strip()]
        if not parts:
            raise ValueError("请输入盲盒数字")

        numbers = []
        animal_type = None
        valid_animal_types = set(self.animals.keys()) | {"无动物"}
        input_overrides = {
            "category": {"disabled": set(), "count_delta": {}},
            "animal": {"disabled": set(), "count_delta": {}},
        }

        for part in parts:
            if part.isdigit():
                numbers.append(int(part))
                continue

            if part in valid_animal_types:
                if animal_type and animal_type != part:
                    raise ValueError("动物类型只能填写一个，可选：无动物、地面动物、空中动物、水中动物")
                animal_type = part
                continue

            matched_override = False
            for label, (target_group, target_key) in self.input_override_targets.items():
                if part == f"无{label}":
                    input_overrides[target_group]["disabled"].add(target_key)
                    matched_override = True
                    break

                match = re.fullmatch(rf"{re.escape(label)}\s*([+-])\s*(\d+)", part)
                if match:
                    delta = int(match.group(2))
                    if match.group(1) == "-":
                        delta = -delta
                    count_delta = input_overrides[target_group]["count_delta"]
                    count_delta[target_key] = count_delta.get(target_key, 0) + delta
                    matched_override = True
                    break

            if matched_override:
                continue

            raise ValueError(
                "输入格式错误，请输入“数字,动物类型,子类指令”，例如：1,5,地面动物,无大型物品,中型物品+1"
            )

        if not numbers:
            raise ValueError("请至少输入一个盲盒数字")

        invalid_numbers = [num for num in numbers if num not in self.blind_boxes]
        if invalid_numbers:
            invalid_text = ",".join(str(num) for num in invalid_numbers)
            raise ValueError(f"盲盒数字不存在：{invalid_text}")

        return numbers, animal_type or "无动物", input_overrides

    def _resolve_extract_config(self, info_list, var_map, spin_var_map, overrides):
        enabled_map = {}
        count_map = {}
        disabled_keys = overrides["disabled"]
        count_deltas = overrides["count_delta"]

        for key, _ in info_list:
            enabled_map[key] = var_map[key].get() and key not in disabled_keys
            count_map[key] = max(0, spin_var_map[key].get() + count_deltas.get(key, 0))

        return enabled_map, count_map

    def _extract_box_items(self, box_id, box, use_state, enabled_map, count_map):
        lines = []
        item_pools = self.draw_history["item_pools"]
        for key, _ in self.category_info:
            if not enabled_map[key]:
                continue
            count = count_map[key]
            if count <= 0:
                continue
            pool_key = self._make_item_pool_key(box_id, key)
            items = self._draw_from_history_pool(item_pools, pool_key, box[key], count)
            lines.extend(self._format_item(item, use_state) for item in items)
        return lines

    def _extract_animal_items(self, animal_type, enabled_map, count_map):
        if animal_type == "无动物":
            return []

        animal_group = self.animals[animal_type]
        lines = []
        animal_pools = self.draw_history["animal_pools"]
        for key, label in self.animal_info:
            if not enabled_map[key]:
                continue
            count = count_map[key]
            if count <= 0:
                continue
            pool_key = self._make_animal_pool_key(animal_type, key)
            items = self._draw_from_history_pool(animal_pools, pool_key, animal_group[key], count)
            lines.extend(f"{label}：{item}" for item in items)
        return lines

    def extract(self):
        try:
            input_str = self.input_entry.get().strip()
            numbers, animal_type, input_overrides = self._parse_input(input_str)
            selected_num = random.choice(numbers)

            box = self.blind_boxes[selected_num]
            use_state = self.state_var.get()
            category_enabled_map, category_count_map = self._resolve_extract_config(
                self.category_info,
                self.category_vars,
                self.category_spin_vars,
                input_overrides["category"],
            )
            animal_enabled_map, animal_count_map = self._resolve_extract_config(
                self.animal_info,
                self.animal_vars,
                self.animal_spin_vars,
                input_overrides["animal"],
            )
            item_lines = self._extract_box_items(selected_num, box, use_state, category_enabled_map, category_count_map)
            animal_lines = self._extract_animal_items(animal_type, animal_enabled_map, animal_count_map)
            self._save_draw_history()

            result_lines = [f"【{box['name']}】"]
            if item_lines:
                result_lines.extend(["", *item_lines])

            if animal_lines:
                result_lines.extend(["", f"【{animal_type}】", *animal_lines])

            if not item_lines and not animal_lines:
                result_lines.extend(["", "当前未勾选任何抽取内容"])

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "\n".join(result_lines))

        except ValueError as exc:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, str(exc))

    def _choose_item_state(self):
        group_names = list(self.item_state_groups)
        group_weights = [self.item_state_group_weights[name] for name in group_names]
        selected_group = random.choices(group_names, weights=group_weights, k=1)[0]
        return random.choice(self.item_state_groups[selected_group])
    
    def _format_item(self, item, use_state):
        if use_state:
            state = self._choose_item_state()
            return f"{state}{item}"
        return item

    def clear_input(self):
        self.input_entry.delete(0, tk.END)
        if self.auto_paste_var.get():
            try:
                clipboard_content = self.root.clipboard_get()
                self.input_entry.insert(0, clipboard_content)
            except tk.TclError:
                pass

    def open_expression_window(self):
        self._show_workspace("expression")
        if self.expression_input_text:
            self.root.after_idle(self.expression_input_text.focus_set)

    def extract_expression_content(self):
        if not self.expression_input_text or not self.expression_output_text:
            return

        try:
            input_text = self.expression_input_text.get(1.0, tk.END).strip()
            random_template = self.expression_template_mode_var.get() == "random"
            template_index = None if random_template else self.expression_template_index_var.get()
            result = self.enhance_expression_text(
                input_text,
                template_index=template_index,
                random_template=random_template,
            )
            self.expression_output_text.delete(1.0, tk.END)
            self.expression_output_text.insert(tk.END, result)
        except ValueError as exc:
            self.expression_output_text.delete(1.0, tk.END)
            self.expression_output_text.insert(tk.END, str(exc))

    def clear_expression_content(self):
        if self.expression_input_text:
            self.expression_input_text.delete(1.0, tk.END)
        if self.expression_output_text:
            self.expression_output_text.delete(1.0, tk.END)

    def copy_expression_result(self):
        if not self.expression_output_text:
            return

        content = self.expression_output_text.get(1.0, tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()

    def copy_to_clipboard(self):
        content = self.output_text.get(1.0, tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()

    def _get_expression_library_candidates(self):
        app_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(app_dir)
        candidates = [
            os.path.join(project_root, "组图 23 表情库.md"),
            os.path.join(app_dir, "组图 23 表情库.md"),
        ]

        if getattr(sys, "frozen", False):
            exe_dir = os.path.dirname(os.path.abspath(sys.executable))
            candidates.append(os.path.join(exe_dir, "组图 23 表情库.md"))

        meipass_dir = getattr(sys, "_MEIPASS", None)
        if meipass_dir:
            candidates.append(os.path.join(meipass_dir, "组图 23 表情库.md"))

        return list(dict.fromkeys(candidates))

    def _get_expression_library_path(self):
        candidates = self._get_expression_library_candidates()
        for path in candidates:
            if os.path.exists(path):
                return path

        candidate_text = "；".join(candidates)
        raise ValueError(f"表情库文件缺失，请确认可读取：{candidate_text}")

    def _load_expression_library(self):
        library_path = self._get_expression_library_path()
        try:
            with open(library_path, "r", encoding="utf-8") as file:
                content = file.read()
        except OSError as exc:
            raise ValueError(f"表情库文件读取失败：{exc}") from exc

        if not content.strip():
            raise ValueError("表情库文件为空")

        library = {"正向": {}, "负向": {}}
        current_polarity = None
        current_expression = None
        current_audience = None

        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            if re.match(r"^##\s+.*正向表情", line):
                current_polarity = "正向"
                current_expression = None
                current_audience = None
                continue

            if re.match(r"^##\s+.*负向表情", line):
                current_polarity = "负向"
                current_expression = None
                current_audience = None
                continue

            heading_match = re.match(r"^###\s*\d+\.\s*(.+)$", line)
            if heading_match and current_polarity:
                current_expression = heading_match.group(1).strip()
                library[current_polarity].setdefault(
                    current_expression,
                    {"单人": {}, "多人": {}},
                )
                current_audience = None
                continue

            if "单人" in line and line.startswith("**"):
                current_audience = "单人"
                continue

            if "多人" in line and line.startswith("**"):
                current_audience = "多人"
                continue

            template_match = re.match(r"^([1-8])\.\s*(眉：.+)$", line)
            if template_match and current_polarity and current_expression and current_audience:
                template_index = int(template_match.group(1))
                library[current_polarity][current_expression][current_audience][template_index] = (
                    template_match.group(2).strip()
                )

        if not library["正向"] or not library["负向"]:
            raise ValueError("表情库结构不符合预期：缺少正向或负向表情区")

        for polarity, expressions in library.items():
            for expression_name, audience_map in expressions.items():
                single_indexes = set(audience_map["单人"])
                multi_indexes = set(audience_map["多人"])
                if single_indexes != {1, 2, 3, 4} or multi_indexes != {5, 6, 7, 8}:
                    raise ValueError(
                        f"表情库结构不符合预期：{polarity}/{expression_name} 必须包含单人 1-4 和多人 5-8"
                    )

        return library

    def _normalize_expression_polarity(self, value):
        if "正向" in value:
            return "正向"
        if "负向" in value:
            return "负向"
        raise ValueError("极性只能填写正向或负向")

    def _normalize_expression_audience(self, value):
        if "多人" in value:
            return "多人"
        if "单人" in value:
            return "单人"
        raise ValueError("单人/多人只能填写单人或多人")

    def _strip_existing_expression_template(self, value):
        stripped_value = value.strip()
        match = re.match(r"(?s)^(.*?)\s*[，,]\s*眉：.*?；眼：.*?；嘴：.*$", stripped_value)
        if match:
            return match.group(1).strip()
        return stripped_value

    def _get_field_matches(self, text, start=0, end=None):
        field_names = [
            "极性",
            "剧情",
            "单人/多人",
            "具体表情",
            "人物定位",
            "表情功能",
            "适配提示",
            "禁用区域",
        ]
        pattern = re.compile(rf"({'|'.join(re.escape(name) for name in field_names)})\s*[:：]")
        if end is None:
            return [match for match in pattern.finditer(text, start)]
        return [match for match in pattern.finditer(text, start, end)]

    def _parse_expression_blocks(self, text):
        if not text.strip():
            raise ValueError("请先粘贴表情组文本")

        all_matches = self._get_field_matches(text)
        if not all_matches:
            raise ValueError("未找到表情组字段，请确认包含极性、单人/多人和具体表情")

        group_starts = [match.start() for match in all_matches if match.group(1) == "极性"]
        if not group_starts:
            raise ValueError("缺少极性字段")

        group_starts.append(len(text))
        blocks = []
        for index in range(len(group_starts) - 1):
            group_start = group_starts[index]
            group_end = group_starts[index + 1]
            group_matches = self._get_field_matches(text, group_start, group_end)
            fields = {}

            for match_index, match in enumerate(group_matches):
                label = match.group(1)
                value_start = match.end()
                value_end = (
                    group_matches[match_index + 1].start()
                    if match_index + 1 < len(group_matches)
                    else group_end
                )
                raw_value = text[value_start:value_end]
                left_trimmed = raw_value.lstrip()
                right_trimmed = raw_value.rstrip()
                trimmed_start = value_start + len(raw_value) - len(left_trimmed)
                trimmed_end = value_start + len(right_trimmed)
                fields[label] = {
                    "value": text[trimmed_start:trimmed_end],
                    "trimmed_start": trimmed_start,
                    "trimmed_end": trimmed_end,
                }

            missing_fields = [name for name in ("极性", "单人/多人", "具体表情") if name not in fields]
            if missing_fields:
                raise ValueError(f"缺少字段：{'、'.join(missing_fields)}")

            blocks.append({
                "fields": fields,
                "group_start": group_start,
                "group_end": group_end,
            })

        return blocks

    def _select_expression_template(self, library, polarity, expression_name, audience, template_index=None, random_template=False):
        polarity_map = library.get(polarity, {})
        if expression_name not in polarity_map:
            other_polarity = "负向" if polarity == "正向" else "正向"
            if expression_name in library.get(other_polarity, {}):
                raise ValueError(f"极性与表情类别错配：{expression_name} 属于{other_polarity}")
            raise ValueError(f"表情类别不存在：{expression_name}")

        valid_indexes = [1, 2, 3, 4] if audience == "单人" else [5, 6, 7, 8]
        if random_template:
            selected_index = random.choice(valid_indexes)
        else:
            if template_index is None:
                raise ValueError("请填写模板编号，或切换为随机模板")
            try:
                selected_index = int(template_index)
            except (TypeError, ValueError) as exc:
                raise ValueError("模板编号必须是数字") from exc

            if selected_index not in valid_indexes:
                range_text = "1-4" if audience == "单人" else "5-8"
                raise ValueError(f"{audience}模板编号必须在 {range_text} 范围内")

        return polarity_map[expression_name][audience][selected_index]

    def enhance_expression_text(self, text, template_index=None, random_template=False):
        library = self._load_expression_library()
        blocks = self._parse_expression_blocks(text)
        replacements = []

        for block in blocks:
            fields = block["fields"]
            polarity = self._normalize_expression_polarity(fields["极性"]["value"])
            audience = self._normalize_expression_audience(fields["单人/多人"]["value"])
            expression_name = self._strip_existing_expression_template(fields["具体表情"]["value"])
            if not expression_name:
                raise ValueError("具体表情不能为空")

            template = self._select_expression_template(
                library,
                polarity,
                expression_name,
                audience,
                template_index=template_index,
                random_template=random_template,
            )
            replacement = f"{expression_name}，{template}"
            replacements.append((
                fields["具体表情"]["trimmed_start"],
                fields["具体表情"]["trimmed_end"],
                replacement,
            ))

        enhanced_text = text
        for start, end, replacement in sorted(replacements, reverse=True):
            enhanced_text = f"{enhanced_text[:start]}{replacement}{enhanced_text[end:]}"

        return enhanced_text
if __name__ == "__main__":
    root = tk.Tk()
    app = BlindBoxExtractor(root)
    root.mainloop()
