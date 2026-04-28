import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import json
import os
import random
import re
import shutil
import sys
import threading
import urllib.error
import urllib.request
import webbrowser
from datetime import datetime
from pathlib import Path
from data.animals import ANIMALS
from data.blind_boxes import BLIND_BOXES
from data.item_states import ITEM_STATE_GROUPS, ITEM_STATE_GROUP_WEIGHTS

APP_VERSION = "0.1.3"
UPDATE_API_URL = "https://api.github.com/repos/zhangyi196/zbt-prompt/releases/latest"
UPDATE_RELEASES_LIST_API_URL = "https://api.github.com/repos/zhangyi196/zbt-prompt/releases?per_page=20"
UPDATE_RELEASES_URL = "https://github.com/zhangyi196/zbt-prompt/releases"
UPDATE_REQUEST_TIMEOUT_SECONDS = 8


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
    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}

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
        runtime_dir = (
            os.path.dirname(sys.executable)
            if getattr(sys, "frozen", False)
            else os.path.dirname(os.path.abspath(__file__))
        )
        self.runtime_dir = runtime_dir
        self.history_file = os.path.join(runtime_dir, "draw_history.json")
        self.draw_history = self._load_draw_history()
        self.renamer_config_file = os.path.join(runtime_dir, "config.json")
        self.renamer_config = self._load_renamer_config()
        self.expression_window = None
        self.expression_input_text = None
        self.expression_output_text = None
        self.expression_template_mode_var = None
        self.expression_template_index_var = None
        self.image_fetcher_folder1_var = tk.StringVar()
        self.image_fetcher_folder2_var = tk.StringVar()
        self.image_fetcher_log_text = None
        self.image_fetcher_run_button = None
        self.renamer_work_dir_var = tk.StringVar(value=self.renamer_config.get("work_dir", os.getcwd()))
        self.txt_start_number_var = tk.StringVar(value=self.renamer_config.get("txt_start_number", "33"))
        self.txt_prefix_var = tk.StringVar(value=self.renamer_config.get("txt_prefix", "kkx3_"))
        self.txt_digits_var = tk.StringVar(value=self.renamer_config.get("txt_digits", "3"))
        self.img_start_number_var = tk.StringVar(value=self.renamer_config.get("img_start_number", "33"))
        self.img_prefix_var = tk.StringVar(value=self.renamer_config.get("img_prefix", "kkx3_"))
        self.img_group_size_var = tk.StringVar(value=self.renamer_config.get("img_group_size", "4"))
        self.img_digits_var = tk.StringVar(value=self.renamer_config.get("img_digits", "3"))
        self.renamer_log_text = None
        self.workspace_buttons = {}
        self.workspace_frames = {}
        self.current_workspace = None
        self.update_button = None
        self.update_button_visible = False
        self.update_check_in_progress = False
        self.latest_update_result = None
        self.setup_ui()
        self._setup_renamer_config_listeners()
        self._schedule_initial_update_check()

    
    def _create_empty_draw_history(self):
        return {
            "version": 2,
            "item_pools": {},
            "animal_pools": {},
            "expression_pools": {},
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
            expression_pools = data.get("expression_pools", {})
            history["item_pools"] = item_pools if isinstance(item_pools, dict) else {}
            history["animal_pools"] = animal_pools if isinstance(animal_pools, dict) else {}
            history["expression_pools"] = (
                expression_pools if isinstance(expression_pools, dict) else {}
            )

        self.draw_history = history
        self._save_draw_history()
        return history

    def _save_draw_history(self):
        history_file = getattr(self, "history_file", None)
        if not history_file:
            return
        with open(self.history_file, "w", encoding="utf-8") as file:
            json.dump(self.draw_history, file, ensure_ascii=False, indent=2)

    def _ensure_draw_history(self):
        history = getattr(self, "draw_history", None)
        if not isinstance(history, dict):
            history = self._create_empty_draw_history()
            self.draw_history = history

        for key in ("item_pools", "animal_pools", "expression_pools"):
            if not isinstance(history.get(key), dict):
                history[key] = {}

        try:
            version = int(history.get("version", 0) or 0)
        except (TypeError, ValueError):
            version = 0
        history["version"] = max(2, version)
        return history

    def _make_expression_category_pool_key(self, polarity, audience):
        return f"expression_category:{polarity}:{audience}"

    def _make_expression_template_pool_key(self, polarity, audience, expression_name):
        return f"expression_template:{polarity}:{audience}:{expression_name}"

    def _get_expression_pool_counts(self, pool_key):
        history = self._ensure_draw_history()
        expression_pools = history["expression_pools"]
        raw_counts = expression_pools.get(pool_key, {})
        if not isinstance(raw_counts, dict):
            raw_counts = {}

        normalized_counts = {}
        for raw_name, raw_value in raw_counts.items():
            try:
                value = int(raw_value)
            except (TypeError, ValueError):
                value = 0
            normalized_counts[str(raw_name)] = max(0, value)

        expression_pools[pool_key] = normalized_counts
        return normalized_counts

    def _choose_weighted_history_value(self, candidates, used_counts):
        weights = [
            1 / (max(0, used_counts.get(str(candidate), 0)) + 1)
            for candidate in candidates
        ]
        return random.choices(candidates, weights=weights, k=1)[0]

    def _record_expression_history(self, pool_key, selected_value):
        used_counts = self._get_expression_pool_counts(pool_key)
        count_key = str(selected_value)
        used_counts[count_key] = used_counts.get(count_key, 0) + 1

    def _load_renamer_config(self):
        if not os.path.exists(self.renamer_config_file):
            return {}

        try:
            with open(self.renamer_config_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            return {}

        return data if isinstance(data, dict) else {}

    def _save_renamer_config(self):
        config = {
            "work_dir": self.renamer_work_dir_var.get(),
            "txt_start_number": self.txt_start_number_var.get(),
            "txt_prefix": self.txt_prefix_var.get(),
            "txt_digits": self.txt_digits_var.get(),
            "img_start_number": self.img_start_number_var.get(),
            "img_prefix": self.img_prefix_var.get(),
            "img_group_size": self.img_group_size_var.get(),
            "img_digits": self.img_digits_var.get(),
        }
        try:
            with open(self.renamer_config_file, "w", encoding="utf-8") as file:
                json.dump(config, file, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def _setup_renamer_config_listeners(self):
        variables = (
            self.renamer_work_dir_var,
            self.txt_start_number_var,
            self.txt_prefix_var,
            self.txt_digits_var,
            self.img_start_number_var,
            self.img_prefix_var,
            self.img_group_size_var,
            self.img_digits_var,
        )
        for variable in variables:
            variable.trace_add("write", lambda *_args: self._save_renamer_config())

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
        self.draw_history["expression_pools"] = {}
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
        self.image_fetcher_workspace = ttk.Frame(self.workspace_host, style="Workspace.TFrame")
        self.renamer_workspace = ttk.Frame(self.workspace_host, style="Workspace.TFrame")
        self.workspace_frames = {
            "blind_box": self.blind_box_workspace,
            "expression": self.expression_workspace,
            "image_fetcher": self.image_fetcher_workspace,
            "renamer": self.renamer_workspace,
        }

        self._build_blind_box_workspace(self.blind_box_workspace)
        self._build_expression_workspace(self.expression_workspace)
        self._build_image_fetcher_workspace(self.image_fetcher_workspace)
        self._build_renamer_workspace(self.renamer_workspace)
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
            "image_fetcher": ttk.Button(
                switcher_frame,
                text="图像抓取",
                style="Switcher.TButton",
                command=lambda: self._show_workspace("image_fetcher"),
            ),
            "renamer": ttk.Button(
                switcher_frame,
                text="批量重命名",
                style="Switcher.TButton",
                command=lambda: self._show_workspace("renamer"),
            ),
        }
        self.workspace_buttons["blind_box"].pack(side=tk.LEFT, padx=(0, 6))
        self.workspace_buttons["expression"].pack(side=tk.LEFT, padx=(0, 6))
        self.workspace_buttons["image_fetcher"].pack(side=tk.LEFT, padx=(0, 6))
        self.workspace_buttons["renamer"].pack(side=tk.LEFT)

        self.update_button = ttk.Button(
            header_frame,
            text="发现新版本",
            command=self._on_update_button_click,
            style="Secondary.TButton",
        )

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

    def _schedule_initial_update_check(self):
        try:
            self.root.after(500, lambda: self.check_for_updates(silent=True))
        except tk.TclError:
            pass

    def _show_update_button(self):
        if not self.update_button:
            return

        self.update_button.configure(text="发现新版本", state=tk.NORMAL)
        if not self.update_button_visible:
            self.update_button.pack(side=tk.RIGHT)
            self.update_button_visible = True

    def _hide_update_button(self):
        if not self.update_button:
            return

        if self.update_button_visible:
            self.update_button.pack_forget()
            self.update_button_visible = False

    def _on_update_button_click(self):
        if self.latest_update_result and self.latest_update_result.get("status") == "update_available":
            self._show_update_available_dialog(self.latest_update_result)
            return

        self.check_for_updates(silent=False)

    def check_for_updates(self, silent=False):
        if self.update_check_in_progress:
            return

        self.update_check_in_progress = True
        if self.update_button and self.update_button_visible:
            self.update_button.configure(text="检查中...", state=tk.DISABLED)

        thread = threading.Thread(target=lambda: self._run_update_check(silent), daemon=True)
        thread.start()

    def _run_update_check(self, silent=False):
        try:
            result = self._fetch_latest_release()
        except Exception as exc:  # noqa: BLE001 - surface unexpected update failures to the user.
            result = {
                "status": "error",
                "message": f"检查更新失败：{exc}",
            }

        try:
            self.root.after(0, lambda: self._handle_update_result(result, silent=silent))
        except tk.TclError:
            pass

    def _fetch_github_json(self, url):
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": f"GameContentExtractor/{APP_VERSION}",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=UPDATE_REQUEST_TIMEOUT_SECONDS) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError:
            raise
        except urllib.error.URLError as exc:
            raise ValueError(f"无法连接 GitHub：{exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError("GitHub 返回内容不是有效 JSON") from exc

    def _fetch_latest_release(self):
        try:
            payload = self._fetch_github_json(UPDATE_API_URL)
        except urllib.error.HTTPError as exc:
            if exc.code != 404:
                raise ValueError(f"GitHub 返回 HTTP {exc.code}") from exc

            payload = self._fetch_latest_release_from_list()
            if payload is None:
                return {
                    "status": "no_release",
                    "message": "当前没有可用发布版本。",
                    "url": UPDATE_RELEASES_URL,
                }

        return self._build_update_result(payload)

    def _fetch_latest_release_from_list(self):
        try:
            payload = self._fetch_github_json(UPDATE_RELEASES_LIST_API_URL)
        except urllib.error.HTTPError as exc:
            raise ValueError(f"GitHub 返回 HTTP {exc.code}") from exc

        if not isinstance(payload, list):
            raise ValueError("GitHub Releases 列表格式不符合预期")

        candidates = []
        for release in payload:
            if not isinstance(release, dict) or release.get("draft"):
                continue

            version = self._normalize_version_tag(str(release.get("tag_name", "")).strip())
            if version:
                candidates.append((self._version_sort_key(version), release))

        if not candidates:
            return None

        candidates.sort(key=lambda item: item[0], reverse=True)
        return candidates[0][1]

    def _build_update_result(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("GitHub 返回格式不符合预期")

        latest_tag = str(payload.get("tag_name", "")).strip()
        latest_version = self._normalize_version_tag(latest_tag)
        if not latest_version:
            raise ValueError("GitHub Release 缺少有效版本号")

        release_url = str(payload.get("html_url") or UPDATE_RELEASES_URL).strip()
        release_notes = str(payload.get("body") or "").strip()
        compare_result = self._compare_versions(APP_VERSION, latest_version)

        if compare_result < 0:
            return {
                "status": "update_available",
                "current_version": APP_VERSION,
                "latest_version": latest_version,
                "latest_tag": latest_tag,
                "notes": release_notes,
                "url": release_url,
            }

        return {
            "status": "up_to_date",
            "current_version": APP_VERSION,
            "latest_version": latest_version,
        }

    def _handle_update_result(self, result, silent=False):
        self.update_check_in_progress = False
        status = result.get("status")
        if status == "update_available":
            self.latest_update_result = result
            self._show_update_button()
            if not silent:
                self._show_update_available_dialog(result)
            return

        self.latest_update_result = None
        self._hide_update_button()
        if silent or status in {"up_to_date", "no_release"}:
            return

        messagebox.showwarning("检查更新", result.get("message", "检查更新失败"))

    def _show_update_available_dialog(self, result):
        notes = self._summarize_release_notes(result.get("notes", ""))
        message = (
            f"发现新版本：{result['latest_version']}\n"
            f"当前版本：{result['current_version']}\n\n"
            f"{notes}\n\n是否打开 GitHub Releases 页面？"
        )
        if messagebox.askyesno("检查更新", message):
            self._open_update_page(result.get("url"))

    def _open_update_page(self, url=None):
        webbrowser.open(url or UPDATE_RELEASES_URL)

    def _summarize_release_notes(self, notes):
        cleaned_notes = notes.strip()
        if not cleaned_notes:
            return "该版本未填写更新说明。"

        max_length = 300
        if len(cleaned_notes) <= max_length:
            return cleaned_notes
        return f"{cleaned_notes[:max_length].rstrip()}..."

    def _normalize_version_tag(self, tag):
        normalized = str(tag).strip()
        if normalized.lower().startswith("v"):
            normalized = normalized[1:]

        version_match = re.search(r"\d+(?:[.\-_+]\d+)*", normalized)
        if version_match:
            return version_match.group(0).strip()
        return normalized.strip()

    def _compare_versions(self, current_version, latest_version):
        current_parts = self._version_sort_key(current_version)
        latest_parts = self._version_sort_key(latest_version)
        max_length = max(len(current_parts), len(latest_parts))
        current_parts.extend([0] * (max_length - len(current_parts)))
        latest_parts.extend([0] * (max_length - len(latest_parts)))

        if current_parts < latest_parts:
            return -1
        if current_parts > latest_parts:
            return 1
        return 0

    def _version_sort_key(self, version):
        normalized = self._normalize_version_tag(version)
        parts = []
        for piece in re.split(r"[.\-_+]", normalized):
            match = re.match(r"^(\d+)", piece)
            if match:
                parts.append(int(match.group(1)))
            elif piece:
                parts.append(0)

        return parts or [0]

    def _build_blind_box_workspace(self, parent):
        layout_frame = ttk.Frame(parent, style="Workspace.TFrame")
        layout_frame.pack(fill=tk.BOTH, expand=True)
        layout_frame.columnconfigure(0, weight=0)
        layout_frame.columnconfigure(1, weight=1)
        layout_frame.rowconfigure(0, weight=1)

        left_panel = ttk.Frame(layout_frame, style="Workspace.TFrame", width=380)
        left_panel.grid(row=0, column=0, sticky="nsw", padx=(0, 18))
        left_panel.grid_propagate(False)

        right_panel = ttk.Frame(layout_frame, style="Workspace.TFrame")
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)

        input_frame = ttk.Frame(left_panel)
        input_frame.pack(pady=(4, 8), fill=tk.X)
        ttk.Label(input_frame, text="盲盒数字/动物类型(逗号分隔):").pack(side=tk.LEFT, padx=(0, 10))
        self.input_entry = ttk.Entry(input_frame, width=36)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            left_panel,
            text="示例：1,5,地面动物,无大型物品,中型物品+1",
            style="Muted.TLabel",
        ).pack(anchor=tk.W)

        state_frame = ttk.Frame(left_panel)
        state_frame.pack(pady=(12, 8), fill=tk.X)
        self.state_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(state_frame, text="启用物品状态", variable=self.state_var).pack(side=tk.LEFT)

        category_frame = ttk.LabelFrame(left_panel, text="物品类别与抽取数量")
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

        animal_frame = ttk.LabelFrame(left_panel, text="动物内容与抽取数量")
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

        button_frame = ttk.Frame(left_panel)
        button_frame.pack(pady=(2, 14), fill=tk.X)

        ttk.Button(button_frame, text="开始抽取", command=self.extract, style="Primary.TButton").pack(side=tk.LEFT, padx=(0, 8))

        clear_frame = ttk.Frame(button_frame)
        clear_frame.pack(side=tk.LEFT, padx=8)
        ttk.Button(clear_frame, text="清空输入", command=self.clear_input, style="Secondary.TButton").pack(side=tk.LEFT)
        self.auto_paste_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(clear_frame, text="自动粘贴", variable=self.auto_paste_var).pack(side=tk.LEFT, padx=(8, 0))

        ttk.Button(button_frame, text="复制结果", command=self.copy_to_clipboard, style="Secondary.TButton").pack(side=tk.LEFT, padx=8)

        history_button_frame = ttk.Frame(left_panel)
        history_button_frame.pack(pady=(8, 0), fill=tk.X)
        ttk.Button(history_button_frame, text="重置物品历史", command=self._reset_item_history, style="Secondary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(history_button_frame, text="重置动物历史", command=self._reset_animal_history, style="Secondary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(history_button_frame, text="重置全部历史", command=self._reset_all_history, style="Secondary.TButton").pack(side=tk.LEFT, padx=5)

        ttk.Label(right_panel, text="提示词输出:", font=self.UI_FONT_BOLD).grid(row=0, column=0, sticky="w")
        self.output_text = scrolledtext.ScrolledText(right_panel, height=22, width=72)
        self._style_text_widget(self.output_text)
        self.output_text.grid(row=1, column=0, pady=(8, 2), sticky="nsew")

    def _build_expression_workspace(self, parent):
        ttk.Label(parent, text="表情组文本:", font=self.UI_FONT_BOLD).pack(pady=(4, 6), anchor=tk.W)
        self.expression_input_text = scrolledtext.ScrolledText(parent, height=12, width=92)
        self._style_text_widget(self.expression_input_text)
        self.expression_input_text.pack(pady=(0, 12), fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(parent)
        control_frame.pack(pady=(0, 12), fill=tk.X)

        self.expression_template_mode_var = tk.StringVar(value="random")
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
        ttk.Button(button_frame, text="清空输入", command=self.clear_expression_input, style="Secondary.TButton").pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="复制结果", command=self.copy_expression_result, style="Secondary.TButton").pack(side=tk.LEFT, padx=8)

        ttk.Label(parent, text="增强后文本:", font=self.UI_FONT_BOLD).pack(pady=(0, 6), anchor=tk.W)
        self.expression_output_text = scrolledtext.ScrolledText(parent, height=14, width=92)
        self._style_text_widget(self.expression_output_text)
        self.expression_output_text.pack(pady=(0, 2), fill=tk.BOTH, expand=True)

    def _build_image_fetcher_workspace(self, parent):
        path_frame = ttk.LabelFrame(parent, text="图像抓取目录")
        path_frame.pack(pady=(4, 12), fill=tk.X)

        self._build_directory_row(
            path_frame,
            "文件夹1（参考名单）:",
            self.image_fetcher_folder1_var,
            "选择文件夹1（参考名单）",
        )
        self._build_directory_row(
            path_frame,
            "文件夹2（目标图库）:",
            self.image_fetcher_folder2_var,
            "选择文件夹2（目标图库）",
        )

        action_frame = ttk.Frame(parent)
        action_frame.pack(pady=(0, 12), fill=tk.X)
        self.image_fetcher_run_button = ttk.Button(
            action_frame,
            text="开始抓取",
            command=self.start_image_fetching,
            style="Primary.TButton",
        )
        self.image_fetcher_run_button.pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            action_frame,
            text="清除日志",
            command=self.clear_image_fetcher_log,
            style="Secondary.TButton",
        ).pack(side=tk.LEFT)
        ttk.Label(
            action_frame,
            text="输出到桌面“图像抓取”文件夹，只复制同名文件。",
            style="Muted.TLabel",
        ).pack(side=tk.LEFT, padx=12)

        ttk.Label(parent, text="运行日志:", font=self.UI_FONT_BOLD).pack(anchor=tk.W, pady=(0, 6))
        self.image_fetcher_log_text = scrolledtext.ScrolledText(parent, height=24, width=96)
        self._style_text_widget(self.image_fetcher_log_text)
        self.image_fetcher_log_text.pack(fill=tk.BOTH, expand=True)

    def _build_renamer_workspace(self, parent):
        path_frame = ttk.LabelFrame(parent, text="工作目录")
        path_frame.pack(pady=(4, 10), fill=tk.X)
        self._build_directory_row(
            path_frame,
            "文件夹路径:",
            self.renamer_work_dir_var,
            "选择工作目录",
            refresh_command=self.refresh_renamer_path,
        )

        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        txt_tab = ttk.Frame(notebook)
        image_tab = ttk.Frame(notebook)
        notebook.add(txt_tab, text="文档命名 (Txt)")
        notebook.add(image_tab, text="图像命名 (Images)")
        self._build_txt_renamer_tab(txt_tab)
        self._build_image_renamer_tab(image_tab)

        log_frame = ttk.LabelFrame(parent, text="运行日志")
        log_frame.pack(fill=tk.BOTH, expand=True)
        self.renamer_log_text = scrolledtext.ScrolledText(log_frame, width=96, height=10, font=("Courier New", 9))
        self._style_text_widget(self.renamer_log_text)
        self.renamer_log_text.pack(fill=tk.BOTH, expand=True)
        self.renamer_log_text.tag_config("success", foreground="green")
        self.renamer_log_text.tag_config("error", foreground="red")
        self.renamer_log_text.tag_config("info", foreground="blue")
        self.renamer_log_text.tag_config("warning", foreground="#b7791f")
        self.log_renamer(f"系统已就绪，当前工作目录: {self.renamer_work_dir_var.get()}", "info")
        self.log_renamer("=" * 80, "info")

    def _build_directory_row(self, parent, label, variable, browse_title, refresh_command=None):
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row_frame, text=label).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Entry(row_frame, textvariable=variable).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        ttk.Button(
            row_frame,
            text="浏览",
            command=lambda: self.browse_directory(variable, browse_title),
            style="Secondary.TButton",
        ).pack(side=tk.LEFT)
        if refresh_command:
            ttk.Button(
                row_frame,
                text="刷新",
                command=refresh_command,
                style="Secondary.TButton",
            ).pack(side=tk.LEFT, padx=(8, 0))

    def _build_txt_renamer_tab(self, parent):
        content_frame = ttk.Frame(parent, padding=(12, 12))
        content_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content_frame, text="文档命名配置 (.txt 文件)", font=self.UI_FONT_BOLD).pack(anchor=tk.W, pady=(0, 10))
        params_frame = ttk.LabelFrame(content_frame, text="参数设置")
        params_frame.pack(fill=tk.X, pady=(0, 10))

        self._build_renamer_param_entry(params_frame, 0, "起始编号:", self.txt_start_number_var)
        self._build_renamer_param_entry(params_frame, 1, "重命名前缀:", self.txt_prefix_var)
        self._build_renamer_param_entry(params_frame, 2, "后缀编号位数:", self.txt_digits_var)

        ttk.Label(
            content_frame,
            text="扫描当前目录下的 .txt 文件，按文件名括号内数字自然排序后重命名为 [前缀][编号].txt。",
            style="Muted.TLabel",
            wraplength=760,
            justify=tk.LEFT,
        ).pack(fill=tk.X, pady=(0, 12))

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X)
        ttk.Button(
            button_frame,
            text="开始重命名文档",
            command=self.execute_txt_rename,
            style="Primary.TButton",
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            button_frame,
            text="清除日志",
            command=self.clear_renamer_log,
            style="Secondary.TButton",
        ).pack(side=tk.LEFT)

    def _build_image_renamer_tab(self, parent):
        content_frame = ttk.Frame(parent, padding=(12, 12))
        content_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content_frame, text="图像命名配置 (.png, .jpg, .jpeg, .webp, .bmp, .gif)", font=self.UI_FONT_BOLD).pack(anchor=tk.W, pady=(0, 10))
        params_frame = ttk.LabelFrame(content_frame, text="参数设置")
        params_frame.pack(fill=tk.X, pady=(0, 10))

        self._build_renamer_param_entry(params_frame, 0, "起始编号:", self.img_start_number_var)
        self._build_renamer_param_entry(params_frame, 1, "重命名前缀:", self.img_prefix_var)
        self._build_renamer_param_entry(params_frame, 2, "每组图像数量:", self.img_group_size_var)
        self._build_renamer_param_entry(params_frame, 3, "后缀编号位数:", self.img_digits_var)

        ttk.Label(
            content_frame,
            text="扫描当前目录下的图像文件，按文件名数字排序后输出 [前缀][组编号]_([组内序号]).扩展名；每组数量为 1 时省略组内序号。",
            style="Muted.TLabel",
            wraplength=760,
            justify=tk.LEFT,
        ).pack(fill=tk.X, pady=(0, 12))

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X)
        ttk.Button(
            button_frame,
            text="开始重命名图像",
            command=self.execute_img_rename,
            style="Primary.TButton",
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            button_frame,
            text="清除日志",
            command=self.clear_renamer_log,
            style="Secondary.TButton",
        ).pack(side=tk.LEFT)

    def _build_renamer_param_entry(self, parent, row, label, variable):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=6, padx=(0, 10))
        ttk.Entry(parent, textvariable=variable, width=22).grid(row=row, column=1, sticky=tk.W, pady=6)

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
        self._clear_and_optionally_paste(self.input_entry)

    def _clear_and_optionally_paste(self, widget, is_text_widget=False):
        if is_text_widget:
            widget.delete(1.0, tk.END)
        else:
            widget.delete(0, tk.END)

        auto_paste_var = getattr(self, "auto_paste_var", None)
        if not auto_paste_var or not auto_paste_var.get():
            return

        try:
            clipboard_content = self.root.clipboard_get()
        except tk.TclError:
            return

        if is_text_widget:
            widget.insert(1.0, clipboard_content)
        else:
            widget.insert(0, clipboard_content)

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

    def clear_expression_input(self):
        if self.expression_input_text:
            self._clear_and_optionally_paste(self.expression_input_text, is_text_widget=True)

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

    def browse_directory(self, variable, title):
        folder = filedialog.askdirectory(title=title)
        if folder:
            variable.set(folder)

    def _log_image_fetcher(self, message):
        if not self.image_fetcher_log_text:
            return
        self.image_fetcher_log_text.insert(tk.END, f"{message}\n")
        self.image_fetcher_log_text.see(tk.END)
        self.root.update()

    def clear_image_fetcher_log(self):
        if self.image_fetcher_log_text:
            self.image_fetcher_log_text.delete(1.0, tk.END)

    def start_image_fetching(self):
        folder1_path = self.image_fetcher_folder1_var.get().strip()
        folder2_path = self.image_fetcher_folder2_var.get().strip()

        if not folder1_path or not folder2_path:
            messagebox.showwarning("警告", "请先选择文件夹1和文件夹2的路径")
            return

        if not os.path.isdir(folder1_path):
            messagebox.showerror("路径错误", f"文件夹1不存在：{folder1_path}")
            return

        if not os.path.isdir(folder2_path):
            messagebox.showerror("路径错误", f"文件夹2不存在：{folder2_path}")
            return

        self.clear_image_fetcher_log()
        if self.image_fetcher_run_button:
            self.image_fetcher_run_button.configure(state=tk.DISABLED)

        try:
            output_dir = Path.home() / "Desktop" / "图像抓取"
            output_dir.mkdir(parents=True, exist_ok=True)

            self._log_image_fetcher(f"准备抓取，文件将保存至：{output_dir}")
            self._log_image_fetcher("-" * 60)

            files_in_folder1 = sorted(os.listdir(folder1_path))
            valid_files = [filename for filename in files_in_folder1 if not filename.startswith(".")]
            odd_files = valid_files[::2]

            self._log_image_fetcher(f"文件夹1中共发现 {len(valid_files)} 个可见条目")
            self._log_image_fetcher(f"准备抓取 {len(odd_files)} 个奇数位置文件")
            self._log_image_fetcher("")

            success_count = 0
            not_found_count = 0

            for filename in odd_files:
                source_file = Path(folder2_path) / filename
                destination_file = output_dir / filename

                if source_file.exists() and source_file.is_file():
                    shutil.copy2(source_file, destination_file)
                    self._log_image_fetcher(f"成功抓取：{filename}")
                    success_count += 1
                else:
                    self._log_image_fetcher(f"未找到：{filename}")
                    not_found_count += 1

            self._log_image_fetcher("-" * 60)
            self._log_image_fetcher("抓取任务完成")
            self._log_image_fetcher(f"成功：{success_count} 张；未找到：{not_found_count} 张")
            messagebox.showinfo(
                "任务完成",
                f"图像抓取完毕！\n成功：{success_count} 张\n未找到：{not_found_count} 张\n\n已保存至桌面“图像抓取”文件夹。",
            )
        except Exception as exc:
            self._log_image_fetcher(f"发生错误：{exc}")
            messagebox.showerror("运行错误", f"发生错误：\n{exc}")
        finally:
            if self.image_fetcher_run_button:
                self.image_fetcher_run_button.configure(state=tk.NORMAL)

    def log_renamer(self, message, tag="normal"):
        if not self.renamer_log_text:
            return
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        if tag == "normal":
            self.renamer_log_text.insert(tk.END, log_message)
        else:
            self.renamer_log_text.insert(tk.END, log_message, tag)
        self.renamer_log_text.see(tk.END)
        self.root.update()

    def clear_renamer_log(self):
        if self.renamer_log_text:
            self.renamer_log_text.delete(1.0, tk.END)
            self.log_renamer("日志已清除", "info")

    def refresh_renamer_path(self):
        path = self.renamer_work_dir_var.get().strip()
        if os.path.isdir(path):
            self.log_renamer(f"路径有效，已刷新：{path}", "info")
        else:
            self.log_renamer(f"错误：路径不存在 - {path}", "error")

    def _renamer_txt_sort_key(self, filename):
        match = re.search(r"\((\d+)\)", filename)
        if match:
            return int(match.group(1))

        numbers = re.findall(r"\d+", filename)
        if numbers:
            return int(numbers[0])

        return -1

    def _renamer_image_sort_key(self, filename):
        numbers = re.findall(r"\d+", filename)
        if numbers:
            return int(numbers[0])
        return -1

    def _validate_renamer_input(self, start_num_str, digits_str, group_size_str=None):
        try:
            start_num = int(start_num_str)
            digits = int(digits_str)

            if start_num < 0:
                self.log_renamer("错误：起始编号必须为非负整数", "error")
                return False

            if digits < 1 or digits > 10:
                self.log_renamer("错误：后缀编号位数必须在 1-10 之间", "error")
                return False

            if group_size_str is not None:
                group_size = int(group_size_str)
                if group_size < 1:
                    self.log_renamer("错误：每组图像数量必须大于 0", "error")
                    return False

            return True
        except ValueError:
            self.log_renamer("错误：请输入有效的整数", "error")
            return False

    def _renamer_paths_match(self, old_path, new_path):
        old_absolute = os.path.normcase(os.path.abspath(old_path))
        new_absolute = os.path.normcase(os.path.abspath(new_path))
        return old_absolute == new_absolute

    def execute_txt_rename(self):
        self.log_renamer("=" * 80, "info")
        self.log_renamer("开始执行文档重命名任务...", "info")

        work_dir = self.renamer_work_dir_var.get().strip()
        if not os.path.isdir(work_dir):
            self.log_renamer(f"错误：工作目录不存在 - {work_dir}", "error")
            return

        if not self._validate_renamer_input(
            self.txt_start_number_var.get(),
            self.txt_digits_var.get(),
        ):
            return

        start_num = int(self.txt_start_number_var.get())
        prefix = self.txt_prefix_var.get()
        digits = int(self.txt_digits_var.get())
        format_str = f"{{:0{digits}d}}"

        self.log_renamer(f"工作目录：{work_dir}", "info")
        self.log_renamer(f"参数：起始编号={start_num}, 前缀='{prefix}', 位数={digits}", "info")

        try:
            txt_files = [
                filename for filename in os.listdir(work_dir)
                if filename.lower().endswith(".txt") and os.path.isfile(os.path.join(work_dir, filename))
            ]
            if not txt_files:
                self.log_renamer("在指定目录中没有找到任何 .txt 文件", "warning")
                return

            txt_files.sort(key=self._renamer_txt_sort_key)
            self.log_renamer(f"找到 {len(txt_files)} 个 .txt 文件，开始按自然顺序重命名...", "info")
            self.log_renamer("")

            success_count = 0
            skip_count = 0
            error_count = 0
            current_num = start_num

            for index, old_name in enumerate(txt_files, 1):
                new_name = f"{prefix}{format_str.format(current_num)}.txt"
                old_path = os.path.join(work_dir, old_name)
                new_path = os.path.join(work_dir, new_name)

                try:
                    if os.path.exists(new_path) and not self._renamer_paths_match(old_path, new_path):
                        self.log_renamer(
                            f"[{index}] 跳过 '{old_name}' -> '{new_name}'（目标文件已存在）",
                            "warning",
                        )
                        skip_count += 1
                    else:
                        os.rename(old_path, new_path)
                        self.log_renamer(f"[{index}] '{old_name}' -> '{new_name}'", "success")
                        success_count += 1
                except OSError as exc:
                    self.log_renamer(f"[{index}] 重命名 '{old_name}' 失败：{exc}", "error")
                    error_count += 1
                finally:
                    current_num += 1

            self.log_renamer("")
            self.log_renamer("=" * 80, "info")
            self.log_renamer(f"文档重命名完成！成功：{success_count}，跳过：{skip_count}，失败：{error_count}", "info")
            self.log_renamer("=" * 80, "info")
        except Exception as exc:
            self.log_renamer(f"执行过程中发生错误：{exc}", "error")

    def execute_img_rename(self):
        self.log_renamer("=" * 80, "info")
        self.log_renamer("开始执行图像重命名任务...", "info")

        work_dir = self.renamer_work_dir_var.get().strip()
        if not os.path.isdir(work_dir):
            self.log_renamer(f"错误：工作目录不存在 - {work_dir}", "error")
            return

        if not self._validate_renamer_input(
            self.img_start_number_var.get(),
            self.img_digits_var.get(),
            self.img_group_size_var.get(),
        ):
            return

        start_num = int(self.img_start_number_var.get())
        prefix = self.img_prefix_var.get()
        group_size = int(self.img_group_size_var.get())
        digits = int(self.img_digits_var.get())
        format_str = f"{{:0{digits}d}}"

        self.log_renamer(f"工作目录：{work_dir}", "info")
        self.log_renamer(f"参数：起始编号={start_num}, 前缀='{prefix}', 每组数量={group_size}, 位数={digits}", "info")

        try:
            image_files = [
                filename for filename in os.listdir(work_dir)
                if os.path.splitext(filename)[1].lower() in self.IMAGE_EXTENSIONS
                and os.path.isfile(os.path.join(work_dir, filename))
            ]
            if not image_files:
                self.log_renamer("在指定目录中没有找到任何图像文件", "warning")
                return

            image_files.sort(key=self._renamer_image_sort_key)
            self.log_renamer(f"找到 {len(image_files)} 个图像文件，开始按自然顺序重命名...", "info")
            self.log_renamer("")

            success_count = 0
            skip_count = 0
            error_count = 0

            for index, old_name in enumerate(image_files):
                group_num = start_num + (index // group_size)
                item_in_group = (index % group_size) + 1
                _, ext = os.path.splitext(old_name)
                if group_size == 1:
                    new_name = f"{prefix}{format_str.format(group_num)}{ext}"
                else:
                    new_name = f"{prefix}{format_str.format(group_num)}_({item_in_group}){ext}"

                old_path = os.path.join(work_dir, old_name)
                new_path = os.path.join(work_dir, new_name)
                display_index = index + 1

                try:
                    if os.path.exists(new_path) and not self._renamer_paths_match(old_path, new_path):
                        self.log_renamer(
                            f"[{display_index}] 跳过 '{old_name}' -> '{new_name}'（目标文件已存在）",
                            "warning",
                        )
                        skip_count += 1
                    else:
                        os.rename(old_path, new_path)
                        self.log_renamer(f"[{display_index}] '{old_name}' -> '{new_name}'", "success")
                        success_count += 1
                except OSError as exc:
                    self.log_renamer(f"[{display_index}] 重命名 '{old_name}' 失败：{exc}", "error")
                    error_count += 1

            self.log_renamer("")
            self.log_renamer("=" * 80, "info")
            self.log_renamer(f"图像重命名完成！成功：{success_count}，跳过：{skip_count}，失败：{error_count}", "info")
            self.log_renamer("=" * 80, "info")
        except Exception as exc:
            self.log_renamer(f"执行过程中发生错误：{exc}", "error")

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

    def _split_expression_candidates(self, value):
        candidates = [
            candidate.strip()
            for candidate in re.split(r"\s*[、，,\/|]\s*", value.strip())
            if candidate.strip()
        ]
        if not candidates:
            raise ValueError("具体表情不能为空")
        return candidates

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

    def _validate_expression_name(self, library, polarity, expression_name):
        polarity_map = library.get(polarity, {})
        if expression_name not in polarity_map:
            other_polarity = "负向" if polarity == "正向" else "正向"
            if expression_name in library.get(other_polarity, {}):
                raise ValueError(f"极性与表情类别错配：{expression_name} 属于{other_polarity}")
            raise ValueError(f"表情类别不存在：{expression_name}")

    def _choose_expression_name(self, library, polarity, audience, value):
        expression_candidates = self._split_expression_candidates(
            self._strip_existing_expression_template(value)
        )
        for expression_name in expression_candidates:
            self._validate_expression_name(library, polarity, expression_name)
        pool_key = self._make_expression_category_pool_key(polarity, audience)
        if len(expression_candidates) == 1:
            return expression_candidates[0], pool_key
        used_counts = self._get_expression_pool_counts(pool_key)
        return self._choose_weighted_history_value(expression_candidates, used_counts), pool_key

    def _select_expression_template(self, library, polarity, expression_name, audience, template_index=None, random_template=False):
        self._validate_expression_name(library, polarity, expression_name)
        polarity_map = library.get(polarity, {})

        valid_indexes = [1, 2, 3, 4] if audience == "单人" else [5, 6, 7, 8]
        pool_key = self._make_expression_template_pool_key(
            polarity,
            audience,
            expression_name,
        )
        if random_template:
            used_counts = self._get_expression_pool_counts(pool_key)
            selected_index = self._choose_weighted_history_value(valid_indexes, used_counts)
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

        return selected_index, polarity_map[expression_name][audience][selected_index], pool_key

    def enhance_expression_text(self, text, template_index=None, random_template=False):
        library = self._load_expression_library()
        blocks = self._parse_expression_blocks(text)
        replacements = []
        history_updates = []

        for block in blocks:
            fields = block["fields"]
            polarity = self._normalize_expression_polarity(fields["极性"]["value"])
            audience = self._normalize_expression_audience(fields["单人/多人"]["value"])
            expression_name, category_pool_key = self._choose_expression_name(
                library,
                polarity,
                audience,
                fields["具体表情"]["value"],
            )

            selected_template_index, template, template_pool_key = self._select_expression_template(
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
            history_updates.append((category_pool_key, expression_name))
            history_updates.append((template_pool_key, selected_template_index))

        enhanced_text = text
        for start, end, replacement in sorted(replacements, reverse=True):
            enhanced_text = f"{enhanced_text[:start]}{replacement}{enhanced_text[end:]}"

        for pool_key, selected_value in history_updates:
            self._record_expression_history(pool_key, selected_value)
        if history_updates:
            self._save_draw_history()

        return enhanced_text
if __name__ == "__main__":
    root = tk.Tk()
    app = BlindBoxExtractor(root)
    root.mainloop()
