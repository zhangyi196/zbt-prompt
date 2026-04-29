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


FIVE_LAYER_KEYS = {
    "core_items",
    "support_items",
    "visible_small_items",
    "conditional_items",
    "blocked_or_risky",
}


class BlindBoxContentModelTests(unittest.TestCase):
    def test_scene_entries_define_twenty_categories_and_three_pilots(self):
        self.assertEqual(len(BLIND_BOX_SCENE_ENTRIES), 20)

        names = {entry["name_zh"] for entry in BLIND_BOX_SCENE_ENTRIES}
        self.assertIn("桌面+学习", names)
        self.assertIn("海底+潜水", names)
        self.assertIn("公园+野餐", names)

        pilots = {entry["name_zh"] for entry in BLIND_BOX_SCENE_ENTRIES if entry["pilot"]}
        self.assertEqual(pilots, {"桌面+学习", "海底+潜水", "公园+野餐"})

    def test_pilot_bundles_have_complete_five_layer_schema(self):
        self.assertEqual(set(BLIND_BOX_ITEM_POOL_BUNDLES), set(BLIND_BOX_PILOT_BOX_IDS))

        for scene_name, bundle in BLIND_BOX_ITEM_POOL_BUNDLES.items():
            with self.subTest(scene_name=scene_name):
                self.assertEqual(set(bundle), FIVE_LAYER_KEYS)
                for key in FIVE_LAYER_KEYS:
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
                    self.assertGreater(len(box[key]), 0)

    def test_blocked_or_risky_items_do_not_enter_default_buckets(self):
        for scene_name, box_id in BLIND_BOX_PILOT_BOX_IDS.items():
            with self.subTest(scene_name=scene_name):
                blocked_items = set(BLIND_BOX_ITEM_POOL_BUNDLES[scene_name]["blocked_or_risky"])
                default_items = set()
                for key in ("large", "medium", "small", "hanging"):
                    default_items.update(BLIND_BOXES[box_id][key])
                self.assertTrue(blocked_items.isdisjoint(default_items))
                self.assertIn("blocked_or_risky", BLIND_BOX_COMPATIBILITY_MAPPING[scene_name]["excluded_sources"])

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
