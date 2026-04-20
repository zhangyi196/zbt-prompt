import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import os
import random
import re
from data.animals import ANIMALS
from data.blind_boxes import BLIND_BOXES
from data.item_states import ITEM_STATE_GROUPS, ITEM_STATE_GROUP_WEIGHTS

class BlindBoxExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("游戏内容抽取软件")
        self.root.geometry("560x760")
        
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
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=(10, 4), padx=10, fill=tk.X)
        ttk.Label(input_frame, text="盲盒数字/动物类型(逗号分隔):").pack(side=tk.LEFT, padx=5)
        self.input_entry = ttk.Entry(input_frame, width=36)
        self.input_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Label(
            self.root,
            text="示例：1,5,地面动物,无大型物品,中型物品+1",
        ).pack(padx=15, anchor=tk.W)

        state_frame = ttk.Frame(self.root)
        state_frame.pack(pady=5, padx=10, fill=tk.X)
        self.state_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(state_frame, text="启用物品状态", variable=self.state_var).pack(side=tk.LEFT, padx=5)

        category_frame = ttk.LabelFrame(self.root, text="物品类别与抽取数量")
        category_frame.pack(pady=5, padx=10, fill=tk.X)

        self.category_vars = {}
        self.category_spin_vars = {}
        for key, label in self.category_info:
            row_frame = ttk.Frame(category_frame)
            row_frame.pack(fill=tk.X, padx=5, pady=2)

            var = tk.BooleanVar(value=True)
            self.category_vars[key] = var
            ttk.Checkbutton(row_frame, text=label, variable=var).pack(side=tk.LEFT, padx=(0, 10))

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
            ).pack(side=tk.LEFT, padx=5)

        animal_frame = ttk.LabelFrame(self.root, text="动物内容与抽取数量")
        animal_frame.pack(pady=5, padx=10, fill=tk.X)

        self.animal_vars = {}
        self.animal_spin_vars = {}
        for key, label in self.animal_info:
            row_frame = ttk.Frame(animal_frame)
            row_frame.pack(fill=tk.X, padx=5, pady=2)

            default_selected = key == "动物本体"
            var = tk.BooleanVar(value=default_selected)
            self.animal_vars[key] = var
            ttk.Checkbutton(row_frame, text=label, variable=var).pack(side=tk.LEFT, padx=(0, 10))

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
            ).pack(side=tk.LEFT, padx=5)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="开始抽取", command=self.extract).pack(side=tk.LEFT, padx=10)

        clear_frame = ttk.Frame(button_frame)
        clear_frame.pack(side=tk.LEFT, padx=10)
        ttk.Button(clear_frame, text="清空输入", command=self.clear_input).pack(side=tk.LEFT)
        self.auto_paste_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(clear_frame, text="自动粘贴", variable=self.auto_paste_var).pack(side=tk.LEFT, padx=(5, 0))

        ttk.Button(button_frame, text="复制结果", command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=10)

        ttk.Label(self.root, text="提示词输出:").pack(padx=10, anchor=tk.W)
        history_button_frame = ttk.Frame(self.root)
        history_button_frame.pack(pady=(0, 10))
        ttk.Button(history_button_frame, text="重置物品历史", command=self._reset_item_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(history_button_frame, text="重置动物历史", command=self._reset_animal_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(history_button_frame, text="重置全部历史", command=self._reset_all_history).pack(side=tk.LEFT, padx=5)

        self.output_text = scrolledtext.ScrolledText(self.root, height=22, width=100)
        self.output_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

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

    def copy_to_clipboard(self):
        content = self.output_text.get(1.0, tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()
if __name__ == "__main__":
    root = tk.Tk()
    app = BlindBoxExtractor(root)
    root.mainloop()
