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


class BlindBoxContentModelTests(unittest.TestCase):
    def test_scene_entries_define_twenty_categories_and_three_pilots(self):
        self.assertEqual(len(BLIND_BOX_SCENE_ENTRIES), 20)

        names = {entry["name_zh"] for entry in BLIND_BOX_SCENE_ENTRIES}
        self.assertIn("桌面+学习", names)
        self.assertIn("海底+潜水", names)
        self.assertIn("公园+野餐", names)

        pilots = {entry["name_zh"] for entry in BLIND_BOX_SCENE_ENTRIES if entry["pilot"]}
        self.assertEqual(pilots, {"桌面+学习", "海底+潜水", "公园+野餐"})

    def test_pilot_bundles_have_complete_four_pool_schema(self):
        self.assertEqual(set(BLIND_BOX_ITEM_POOL_BUNDLES), set(BLIND_BOX_PILOT_BOX_IDS))

        for scene_name, bundle in BLIND_BOX_ITEM_POOL_BUNDLES.items():
            with self.subTest(scene_name=scene_name):
                self.assertEqual(set(bundle), FOUR_POOL_KEYS)
                self.assertNotIn("conditional_items", bundle)
                self.assertNotIn("blocked_or_risky", bundle)
                for key in FOUR_POOL_KEYS:
                    self.assertIsInstance(bundle[key], list)
                    self.assertGreater(len(bundle[key]), 0)

    def test_pilot_legacy_view_keeps_runtime_bucket_contract(self):
        for scene_name, box_id in BLIND_BOX_PILOT_BOX_IDS.items():
            with self.subTest(scene_name=scene_name):
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

    def test_removed_candidate_pools_do_not_enter_mapping(self):
        for scene_name, box_id in BLIND_BOX_PILOT_BOX_IDS.items():
            with self.subTest(scene_name=scene_name):
                mapping = BLIND_BOX_COMPATIBILITY_MAPPING[scene_name]
                self.assertNotIn("conditional_items", mapping["large_sources"])
                self.assertNotIn("conditional_items", mapping["medium_sources"])
                self.assertNotIn("conditional_items", mapping["small_sources"])
                self.assertNotIn("conditional_items", mapping["hanging_sources"])
                self.assertNotIn("blocked_or_risky", mapping["excluded_sources"])
                self.assertIn("blocked_patterns", mapping["excluded_sources"])

    def test_pilot_item_pools_do_not_contain_blocked_patterns(self):
        for scene_name, bundle in BLIND_BOX_ITEM_POOL_BUNDLES.items():
            for layer_name in FOUR_POOL_KEYS:
                for item_name in bundle[layer_name]:
                    with self.subTest(scene_name=scene_name, layer_name=layer_name, item_name=item_name):
                        for pattern in BLOCKED_ITEM_PATTERNS:
                            self.assertNotIn(pattern, item_name)

    def test_existing_input_override_syntax_accepts_pilot_box_ids(self):
        extractor = content_extractor.BlindBoxExtractor.__new__(content_extractor.BlindBoxExtractor)
        extractor.blind_boxes = BLIND_BOXES
        extractor.animals = {"地面动物": {}, "空中动物": {}, "水中动物": {}}
        extractor.category_info = [
            ("large", "大型物品"),
            ("medium", "中型物品"),
            ("small", "散落小型物品"),
            ("hanging", "悬挂物品"),
        ]
        extractor.animal_info = [
            ("动物本体", "动物本体"),
            ("动物用品", "动物用品"),
            ("动物痕迹", "动物痕迹"),
        ]
        extractor.input_override_targets = {
            label: ("category", key) for key, label in extractor.category_info
        }
        extractor.input_override_targets.update({
            label: ("animal", key) for key, label in extractor.animal_info
        })

        numbers, animal_type, overrides = extractor._parse_input("15,无大型物品,中型物品+1")

        self.assertEqual(numbers, [15])
        self.assertEqual(animal_type, "无动物")
        self.assertIn("large", overrides["category"]["disabled"])
        self.assertEqual(overrides["category"]["count_delta"]["medium"], 1)

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
