import importlib.util
import json
import pathlib
import shutil
import sys
import unittest
import uuid
from unittest import mock


MODULE_PATH = pathlib.Path(__file__).with_name("内容抽取.py")
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("content_extractor", MODULE_PATH)
content_extractor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(content_extractor)


NEGATIVE_SAMPLE = (
    "极性: 负向\n"
    "剧情: [目标物]突然变得不对劲\n"
    "单人/多人: 单人\n"
    "具体表情: 困惑\n"
    "人物定位: 画面中间人物\n"
    "表情功能: 困惑\n"
    "适配提示: 眼神回指[目标物]\n"
    "禁用区域: 姿态不变\n"
)

MULTI_CANDIDATE_SAMPLE = (
    "极性: 负向\n"
    "剧情: [目标物]突然变得不对劲\n"
    "单人/多人: 单人\n"
    "具体表情: 困惑、委屈|失落 / 尴尬\n"
    "人物定位: 画面中间人物\n"
    "表情功能: 困惑\n"
    "适配提示: 眼神回指[目标物]\n"
    "禁用区域: 姿态不变\n"
)

MULTI_AUDIENCE_SAMPLE = (
    "极性: 负向\n"
    "剧情: [目标物]突然变得不对劲\n"
    "单人/多人: 多人\n"
    "具体表情: 困惑\n"
    "人物定位: 画面中间两个人物\n"
    "表情功能: 困惑\n"
    "适配提示: 眼神回指[目标物]\n"
    "禁用区域: 姿态不变\n"
)


class ExpressionEnhancementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        inspector = content_extractor.BlindBoxExtractor.__new__(content_extractor.BlindBoxExtractor)
        cls.library = inspector._load_expression_library()
        cls.expected_template_4 = cls.library["负向"]["困惑"]["单人"][4]

    def make_extractor(self, history_data=None):
        extractor = content_extractor.BlindBoxExtractor.__new__(content_extractor.BlindBoxExtractor)
        temp_dir = MODULE_PATH.parent / f"_tmp_history_test_{uuid.uuid4().hex}"
        temp_dir.mkdir()
        self.addCleanup(shutil.rmtree, temp_dir, True)
        extractor.history_file = str(temp_dir / "draw_history.json")

        if history_data is not None:
            pathlib.Path(extractor.history_file).write_text(
                json.dumps(history_data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        extractor.draw_history = extractor._load_draw_history()
        return extractor

    def test_single_expression_category_keeps_existing_behavior(self):
        result = self.make_extractor().enhance_expression_text(NEGATIVE_SAMPLE, template_index=4)

        self.assertIn(f"具体表情: 困惑，{self.expected_template_4}", result)
        self.assertIn("人物定位: 画面中间人物", result)

    def test_multi_candidate_expression_uses_history_weighted_selection(self):
        extractor = self.make_extractor(
            {
                "version": 2,
                "item_pools": {},
                "animal_pools": {},
                "expression_pools": {
                    "expression_category:负向:单人": {
                        "困惑": 3,
                        "委屈": 0,
                        "失落": 1,
                        "尴尬": 0,
                    }
                },
            }
        )
        captured = {}

        def fake_choices(options, weights, k):
            captured["options"] = options
            captured["weights"] = weights
            captured["k"] = k
            return ["尴尬"]

        with mock.patch.object(content_extractor.random, "choices", side_effect=fake_choices):
            result = extractor.enhance_expression_text(MULTI_CANDIDATE_SAMPLE, template_index=4)

        self.assertEqual(captured["options"], ["困惑", "委屈", "失落", "尴尬"])
        self.assertEqual(captured["k"], 1)
        self.assertEqual(captured["weights"], [0.25, 1.0, 0.5, 1.0])
        self.assertIn("具体表情: 尴尬，", result)
        self.assertNotIn("具体表情: 困惑、委屈|失落 / 尴尬", result)
        self.assertEqual(
            extractor.draw_history["expression_pools"]["expression_category:负向:单人"]["尴尬"],
            1,
        )

    def test_multi_candidate_expression_validates_all_candidates_exist(self):
        sample = MULTI_CANDIDATE_SAMPLE.replace("困惑、委屈|失落 / 尴尬", "困惑,不存在")

        with self.assertRaisesRegex(ValueError, "表情类别不存在：不存在"):
            self.make_extractor().enhance_expression_text(sample, template_index=4)

    def test_multi_candidate_expression_validates_candidate_polarity(self):
        sample = MULTI_CANDIDATE_SAMPLE.replace("困惑、委屈|失落 / 尴尬", "困惑,偷笑")

        with self.assertRaisesRegex(ValueError, "极性与表情类别错配：偷笑 属于正向"):
            self.make_extractor().enhance_expression_text(sample, template_index=4)

    def test_single_expression_category_records_history_after_success(self):
        extractor = self.make_extractor()

        extractor.enhance_expression_text(NEGATIVE_SAMPLE, template_index=4)

        self.assertEqual(
            extractor.draw_history["expression_pools"]["expression_category:负向:单人"],
            {"困惑": 1},
        )

    def test_random_template_uses_history_weighting(self):
        extractor = self.make_extractor(
            {
                "version": 2,
                "item_pools": {},
                "animal_pools": {},
                "expression_pools": {
                    "expression_template:负向:单人:困惑": {
                        "1": 2,
                        "2": 0,
                        "3": 1,
                        "4": 0,
                    }
                },
            }
        )
        captured = {}
        expected_template = self.library["负向"]["困惑"]["单人"][2]

        def fake_choices(options, weights, k):
            captured["options"] = options
            captured["weights"] = weights
            captured["k"] = k
            return [2]

        with mock.patch.object(content_extractor.random, "choices", side_effect=fake_choices):
            result = extractor.enhance_expression_text(NEGATIVE_SAMPLE, random_template=True)

        self.assertEqual(captured["options"], [1, 2, 3, 4])
        self.assertEqual(captured["k"], 1)
        self.assertAlmostEqual(captured["weights"][0], 1 / 3)
        self.assertAlmostEqual(captured["weights"][1], 1.0)
        self.assertAlmostEqual(captured["weights"][2], 0.5)
        self.assertAlmostEqual(captured["weights"][3], 1.0)
        self.assertIn(f"具体表情: 困惑，{expected_template}", result)
        self.assertEqual(
            extractor.draw_history["expression_pools"]["expression_template:负向:单人:困惑"]["2"],
            1,
        )

    def test_random_template_uses_multi_audience_history_weighting(self):
        extractor = self.make_extractor(
            {
                "version": 2,
                "item_pools": {},
                "animal_pools": {},
                "expression_pools": {
                    "expression_template:负向:多人:困惑": {
                        "5": 2,
                        "6": 0,
                        "7": 1,
                        "8": 0,
                    }
                },
            }
        )
        captured = {}
        expected_template = self.library["负向"]["困惑"]["多人"][6]

        def fake_choices(options, weights, k):
            captured["options"] = options
            captured["weights"] = weights
            captured["k"] = k
            return [6]

        with mock.patch.object(content_extractor.random, "choices", side_effect=fake_choices):
            result = extractor.enhance_expression_text(MULTI_AUDIENCE_SAMPLE, random_template=True)

        self.assertEqual(captured["options"], [5, 6, 7, 8])
        self.assertEqual(captured["k"], 1)
        self.assertAlmostEqual(captured["weights"][0], 1 / 3)
        self.assertAlmostEqual(captured["weights"][1], 1.0)
        self.assertAlmostEqual(captured["weights"][2], 0.5)
        self.assertAlmostEqual(captured["weights"][3], 1.0)
        self.assertIn(f"具体表情: 困惑，{expected_template}", result)
        self.assertEqual(
            extractor.draw_history["expression_pools"]["expression_template:负向:多人:困惑"]["6"],
            1,
        )

    def test_specified_template_number_still_records_history(self):
        extractor = self.make_extractor()

        result = extractor.enhance_expression_text(NEGATIVE_SAMPLE, template_index=4)

        self.assertIn(f"具体表情: 困惑，{self.expected_template_4}", result)
        self.assertEqual(
            extractor.draw_history["expression_pools"]["expression_template:负向:单人:困惑"],
            {"4": 1},
        )

    def test_repeat_enhancement_replaces_existing_template_without_stacking(self):
        extractor = self.make_extractor()
        first = extractor.enhance_expression_text(MULTI_CANDIDATE_SAMPLE, template_index=4)

        second = extractor.enhance_expression_text(first, template_index=4)

        self.assertEqual(first, second)
        self.assertEqual(second.count("眉："), 1)
        self.assertEqual(second.count("眼："), 1)
        self.assertEqual(second.count("嘴："), 1)

    def test_old_draw_history_is_upgraded_with_expression_pools(self):
        legacy_history = {
            "version": 1,
            "item_pools": {"box:1:large": {"seen_in_cycle": ["杯子"], "cooldown": {"杯子": 2}}},
            "animal_pools": {"animal:地面动物:动物本体": {"seen_in_cycle": [], "cooldown": {}}},
        }
        extractor = self.make_extractor(legacy_history)

        self.assertEqual(extractor.draw_history["version"], 2)
        self.assertEqual(extractor.draw_history["expression_pools"], {})
        saved_history = json.loads(pathlib.Path(extractor.history_file).read_text(encoding="utf-8"))
        self.assertIn("expression_pools", saved_history)
        self.assertEqual(saved_history["expression_pools"], {})

    def test_expression_history_does_not_affect_item_or_animal_pools(self):
        history_data = {
            "version": 2,
            "item_pools": {"box:1:large": {"seen_in_cycle": ["杯子"], "cooldown": {"杯子": 2}}},
            "animal_pools": {
                "animal:地面动物:动物本体": {"seen_in_cycle": ["小猫"], "cooldown": {"小猫": 1}}
            },
            "expression_pools": {},
        }
        extractor = self.make_extractor(history_data)

        extractor.enhance_expression_text(NEGATIVE_SAMPLE, template_index=4)

        self.assertEqual(extractor.draw_history["item_pools"], history_data["item_pools"])
        self.assertEqual(extractor.draw_history["animal_pools"], history_data["animal_pools"])
        self.assertIn("expression_category:负向:单人", extractor.draw_history["expression_pools"])


if __name__ == "__main__":
    unittest.main()
