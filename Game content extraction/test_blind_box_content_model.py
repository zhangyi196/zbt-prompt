import importlib.util
import pathlib
import sys
import unittest


MODULE_PATH = pathlib.Path(__file__).with_name("内容抽取.py")
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("content_extractor", MODULE_PATH)
content_extractor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(content_extractor)

from data.blind_boxes import (  # noqa: E402
    BLIND_BOX_COMPATIBILITY_MAPPING,
    BLIND_BOX_ITEM_POOL_BUNDLES,
    BLIND_BOX_PILOT_BOX_IDS,
    BLIND_BOX_RUNTIME_ID_BY_SCENE,
    BLIND_BOX_SCENE_ENTRIES,
    BLIND_BOXES,
)
from data.item_states import ITEM_STATE_GROUPS, ITEM_STATE_GROUP_WEIGHTS  # noqa: E402


FOUR_POOL_KEYS = {
    "core_items",
    "support_items",
    "visible_small_items",
    "scene_expansion_items",
}

BLOCKED_ITEM_PATTERNS = (
    "折线",
    "擦痕",
    "气泡",
    "阴影",
    "边线",
    "碎叶点",
    "细小石子",
    "微小沙粒",
    "微小污点",
    "风吹纸片边缘",
    "漂浮细海草丝",
    "水面高光",
    "显示器下方",
    "白板磁吸",
    "伞杆",
    "挂点",
    "桌侧",
    "细绳",
    "流苏",
    "透明",
    "反光",
    "发光",
    "动物本体",
    "微小",
)

MEDIUM_SCENE_FRAGMENT_ALLOWED_PATTERNS = (
    "板",
    "垫",
    "盘",
    "盆",
    "桶",
    "盒",
    "包",
    "卷",
    "册",
    "本",
    "夹",
    "袋",
    "筒",
    "器",
    "机",
    "座",
    "架",
    "篮",
    "刷",
    "尺",
    "擦",
    "钟",
    "历",
    "词典",
    "录音笔",
    "显微镜",
    "书立",
    "笔袋",
    "笔筒",
    "页",
    "图",
    "组合",
    "阵列",
    "样本",
    "半成品",
    "拼贴",
    "布面",
    "毯面",
    "席面",
    "托盘",
    "分区",
    "套组",
    "包裹",
    "操作面",
    "展示面",
    "记录面",
)

OVERSIZED_SCENE_EXPANSION_PATTERNS = (
    "推车",
    "整理车",
    "周转车",
    "餐车",
    "置物车",
    "收纳柜",
    "抽屉柜",
    "文件柜",
    "储物柜",
    "边柜",
    "衣柜",
    "展示柜",
    "陈列柜",
    "书柜",
    "货架",
    "落地架",
    "陈列架",
    "展示架",
    "收纳架",
    "书报架",
    "报刊架",
    "置物架",
    "书架",
    "边桌",
    "书桌",
    "工作台",
    "操作台",
)

TINY_SCENE_EXPANSION_PATTERNS = (
    "小卡片",
    "卡片",
    "标签",
    "价格签",
    "编号牌",
    "铭牌",
    "名牌",
    "小票",
    "票卡",
    "书签",
    "贴纸",
    "贴签",
    "签条",
    "单张",
    "单枚",
)

UPGRADED_INFORMATION_SURFACE_PATTERNS = (
    "信息展示板",
    "菜单展示板",
    "课程记录板",
    "标签排版板",
    "导览说明板",
    "流程说明板",
)


def _contains_any(item_name, patterns):
    return any(pattern in item_name for pattern in patterns)


def _is_upgraded_information_surface(item_name):
    return _contains_any(item_name, UPGRADED_INFORMATION_SURFACE_PATTERNS)


def _is_medium_scene_fragment_item(item_name):
    if _contains_any(item_name, OVERSIZED_SCENE_EXPANSION_PATTERNS):
        return False
    if _contains_any(item_name, TINY_SCENE_EXPANSION_PATTERNS) and not _is_upgraded_information_surface(item_name):
        return False
    return _contains_any(item_name, MEDIUM_SCENE_FRAGMENT_ALLOWED_PATTERNS)


class BlindBoxContentModelTests(unittest.TestCase):
    def test_scene_expansion_rule_baseline_accepts_medium_fragments(self):
        accepted_items = (
            "课程记录板",
            "茶歇摆放垫",
            "烘焙步骤板",
            "编织半成品垫",
            "标签排版板",
        )

        for item_name in accepted_items:
            with self.subTest(item_name=item_name):
                self.assertTrue(_is_medium_scene_fragment_item(item_name))

    def test_scene_expansion_rule_baseline_rejects_wrong_scale_examples(self):
        rejected_items = (
            "学习资料推车",
            "桌面抽屉柜",
            "甜点陈列架",
            "课程小卡片",
            "单张价格签",
            "零食贴纸",
        )

        for item_name in rejected_items:
            with self.subTest(item_name=item_name):
                self.assertFalse(_is_medium_scene_fragment_item(item_name))

    def test_scene_entries_define_twenty_categories_and_pilot_markers(self):
        self.assertEqual(len(BLIND_BOX_SCENE_ENTRIES), 20)

        names = {entry["name_zh"] for entry in BLIND_BOX_SCENE_ENTRIES}
        self.assertEqual(names, set(BLIND_BOX_ITEM_POOL_BUNDLES))
        self.assertEqual(names, set(BLIND_BOX_RUNTIME_ID_BY_SCENE))

        pilots = {entry["name_zh"] for entry in BLIND_BOX_SCENE_ENTRIES if entry["pilot"]}
        self.assertEqual(pilots, set(BLIND_BOX_PILOT_BOX_IDS))
        self.assertEqual(BLIND_BOX_PILOT_BOX_IDS["桌面+学习"], 1)
        self.assertEqual(BLIND_BOX_PILOT_BOX_IDS["公园+野餐"], 12)
        self.assertEqual(BLIND_BOX_PILOT_BOX_IDS["海底+潜水"], 16)

    def test_all_scene_bundles_have_complete_four_pool_schema(self):
        for scene_name, bundle in BLIND_BOX_ITEM_POOL_BUNDLES.items():
            with self.subTest(scene_name=scene_name):
                self.assertEqual(set(bundle), FOUR_POOL_KEYS)
                self.assertNotIn("conditional_items", bundle)
                self.assertNotIn("anchor_required_items", bundle)
                self.assertNotIn("blocked_or_risky", bundle)
                for key in FOUR_POOL_KEYS:
                    self.assertIsInstance(bundle[key], list)
                    self.assertGreater(len(bundle[key]), 0)

                self.assertGreaterEqual(len(bundle["core_items"]), 6)
                self.assertGreaterEqual(len(bundle["support_items"]), 6)

    def test_all_scene_bundles_expand_each_pool_to_fifty_unique_items(self):
        for scene_name, bundle in BLIND_BOX_ITEM_POOL_BUNDLES.items():
            for key in FOUR_POOL_KEYS:
                with self.subTest(scene_name=scene_name, pool=key):
                    self.assertEqual(len(bundle[key]), 50)
                    self.assertEqual(len(bundle[key]), len(set(bundle[key])))

    def test_scene_expansion_items_keep_medium_scene_fragment_boundary(self):
        for scene_name, bundle in BLIND_BOX_ITEM_POOL_BUNDLES.items():
            for item_name in bundle["scene_expansion_items"]:
                with self.subTest(scene_name=scene_name, item_name=item_name):
                    self.assertTrue(_is_medium_scene_fragment_item(item_name))
                    self.assertFalse(_contains_any(item_name, OVERSIZED_SCENE_EXPANSION_PATTERNS))
                    if _contains_any(item_name, TINY_SCENE_EXPANSION_PATTERNS):
                        self.assertTrue(_is_upgraded_information_surface(item_name))

    def test_scene_expansion_items_do_not_duplicate_other_pool_entries(self):
        for scene_name, bundle in BLIND_BOX_ITEM_POOL_BUNDLES.items():
            scene_items = set(bundle["scene_expansion_items"])
            other_pool_items = (
                set(bundle["core_items"])
                | set(bundle["support_items"])
                | set(bundle["visible_small_items"])
            )

            with self.subTest(scene_name=scene_name):
                self.assertFalse(scene_items & other_pool_items)

    def test_runtime_entries_keep_four_bucket_contract_for_all_twenty_boxes(self):
        self.assertEqual(
            set(BLIND_BOXES),
            set(BLIND_BOX_RUNTIME_ID_BY_SCENE.values()),
        )

        for scene_name, box_id in BLIND_BOX_RUNTIME_ID_BY_SCENE.items():
            with self.subTest(scene_name=scene_name, box_id=box_id):
                box = BLIND_BOXES[box_id]
                self.assertEqual(box["name"], scene_name)
                self.assertEqual(
                    {"name", "large", "medium", "small", "hanging"},
                    set(box),
                )
                for key in ("large", "medium", "small", "hanging"):
                    self.assertIsInstance(box[key], list)
                for key in ("large", "medium", "small"):
                    self.assertGreater(len(box[key]), 0)

    def test_compatibility_mapping_covers_all_runtime_boxes(self):
        self.assertEqual(
            set(BLIND_BOX_COMPATIBILITY_MAPPING),
            set(BLIND_BOX_RUNTIME_ID_BY_SCENE),
        )

        for scene_name, mapping in BLIND_BOX_COMPATIBILITY_MAPPING.items():
            with self.subTest(scene_name=scene_name):
                self.assertEqual(
                    mapping["box_id"],
                    BLIND_BOX_RUNTIME_ID_BY_SCENE[scene_name],
                )
                self.assertEqual(
                    mapping["large_sources"],
                    ["core_items", "scene_expansion_items"],
                )
                self.assertEqual(
                    mapping["medium_sources"],
                    ["support_items", "core_items:first_6"],
                )
                self.assertEqual(mapping["small_sources"], ["visible_small_items"])
                self.assertEqual(mapping["hanging_sources"], [])
                self.assertIn("blocked_patterns", mapping["excluded_sources"])
                self.assertNotIn("conditional_items", mapping["excluded_sources"])
                self.assertNotIn("anchor_required_items", mapping["excluded_sources"])
                self.assertNotIn("blocked_or_risky", mapping["excluded_sources"])

    def test_default_item_pools_do_not_contain_blocked_patterns(self):
        for scene_name, bundle in BLIND_BOX_ITEM_POOL_BUNDLES.items():
            for layer_name in FOUR_POOL_KEYS:
                for item_name in bundle[layer_name]:
                    with self.subTest(scene_name=scene_name, layer_name=layer_name, item_name=item_name):
                        for pattern in BLOCKED_ITEM_PATTERNS:
                            self.assertNotIn(pattern, item_name)

    def test_existing_input_override_syntax_accepts_new_runtime_box_ids(self):
        extractor = content_extractor.BlindBoxExtractor.__new__(content_extractor.BlindBoxExtractor)
        extractor.blind_boxes = BLIND_BOXES
        extractor.blind_box_item_pool_bundles = BLIND_BOX_ITEM_POOL_BUNDLES
        extractor.animals = {"地面动物": {}, "空中动物": {}, "水中动物": {}}
        extractor.category_info = [
            ("core_items", "核心物品"),
            ("support_items", "配套物品"),
            ("visible_small_items", "散落小型物品"),
            ("scene_expansion_items", "场景扩展物"),
        ]
        extractor.animal_info = [
            ("动物本体", "动物本体"),
            ("动物用品", "动物用品"),
            ("动物痕迹", "动物痕迹"),
        ]
        extractor.input_override_targets = extractor._build_input_override_targets()

        numbers, animal_type, overrides = extractor._parse_input("1,无大型物品,场景扩展物+1")

        self.assertEqual(numbers, [1])
        self.assertEqual(animal_type, "无动物")
        self.assertIn("core_items", overrides["category"]["disabled"])
        self.assertEqual(overrides["category"]["count_delta"]["scene_expansion_items"], 1)

    def test_box_item_sources_prefer_four_pool_bundle(self):
        extractor = content_extractor.BlindBoxExtractor.__new__(content_extractor.BlindBoxExtractor)
        extractor.category_info = [
            ("core_items", "核心物品"),
            ("support_items", "配套物品"),
            ("visible_small_items", "散落小型物品"),
            ("scene_expansion_items", "场景扩展物"),
        ]
        extractor.blind_box_item_pool_bundles = BLIND_BOX_ITEM_POOL_BUNDLES

        box = BLIND_BOXES[1]
        sources = extractor._get_box_item_sources(box)
        bundle = BLIND_BOX_ITEM_POOL_BUNDLES[box["name"]]

        self.assertEqual(sources["core_items"], bundle["core_items"])
        self.assertEqual(sources["scene_expansion_items"], bundle["scene_expansion_items"])
        self.assertNotEqual(sources["scene_expansion_items"], box["hanging"])

    def test_extract_box_items_can_draw_scene_expansion_items(self):
        extractor = content_extractor.BlindBoxExtractor.__new__(content_extractor.BlindBoxExtractor)
        extractor.category_info = [
            ("core_items", "核心物品"),
            ("support_items", "配套物品"),
            ("visible_small_items", "散落小型物品"),
            ("scene_expansion_items", "场景扩展物"),
        ]
        extractor.blind_box_item_pool_bundles = BLIND_BOX_ITEM_POOL_BUNDLES
        extractor.draw_history = {
            "version": 2,
            "item_pools": {},
            "animal_pools": {},
            "expression_pools": {},
        }
        extractor._format_item = lambda item, _use_state: item

        box = BLIND_BOXES[1]
        bundle = BLIND_BOX_ITEM_POOL_BUNDLES[box["name"]]
        enabled_map = {
            "core_items": False,
            "support_items": False,
            "visible_small_items": False,
            "scene_expansion_items": True,
        }
        count_map = {
            "core_items": 0,
            "support_items": 0,
            "visible_small_items": 0,
            "scene_expansion_items": 1,
        }

        lines = extractor._extract_box_items(
            1,
            box,
            False,
            enabled_map,
            count_map,
        )

        self.assertEqual(len(lines), 1)
        self.assertIn(lines[0], bundle["scene_expansion_items"])

    def test_risky_item_states_are_filtered(self):
        extractor = content_extractor.BlindBoxExtractor.__new__(content_extractor.BlindBoxExtractor)
        extractor.item_state_groups = ITEM_STATE_GROUPS
        extractor.item_state_group_weights = ITEM_STATE_GROUP_WEIGHTS
        extractor.blocked_item_state_keywords = ("半透明", "高光反光", "带有光泽")

        self.assertFalse(extractor._is_safe_item_state("半透明的"))
        self.assertFalse(extractor._is_safe_item_state("带有高光反光的"))
        self.assertFalse(extractor._is_safe_item_state("带有光泽的"))
        self.assertTrue(extractor._is_safe_item_state("带有木纹的"))


if __name__ == "__main__":
    unittest.main()
