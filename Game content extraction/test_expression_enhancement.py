import importlib.util
import pathlib
import sys
import unittest
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

EXPECTED_TEMPLATE_4 = (
    "眉：一侧眉尾抬起，另一侧眉尾压平；"
    "眼：一侧眼撑开看着[目标物]，另一侧眼半垂；"
    "嘴：一侧嘴巴闭住下压，另一侧嘴角收紧。"
)


class ExpressionEnhancementTests(unittest.TestCase):
    def make_extractor(self):
        return content_extractor.BlindBoxExtractor.__new__(content_extractor.BlindBoxExtractor)

    def test_single_expression_category_keeps_existing_behavior(self):
        result = self.make_extractor().enhance_expression_text(NEGATIVE_SAMPLE, template_index=4)

        self.assertIn(f"具体表情: 困惑，{EXPECTED_TEMPLATE_4}", result)
        self.assertIn("人物定位: 画面中间人物", result)

    def test_multi_candidate_expression_uses_random_selected_category(self):
        extractor = self.make_extractor()
        with mock.patch.object(content_extractor.random, "choice", side_effect=["尴尬"]):
            result = extractor.enhance_expression_text(MULTI_CANDIDATE_SAMPLE, template_index=4)

        self.assertIn("具体表情: 尴尬，", result)
        self.assertNotIn("具体表情: 困惑、委屈|失落 / 尴尬", result)

    def test_multi_candidate_expression_validates_all_candidates_exist(self):
        sample = MULTI_CANDIDATE_SAMPLE.replace("困惑、委屈|失落 / 尴尬", "困惑,不存在")

        with self.assertRaisesRegex(ValueError, "表情类别不存在：不存在"):
            self.make_extractor().enhance_expression_text(sample, template_index=4)

    def test_multi_candidate_expression_validates_candidate_polarity(self):
        sample = MULTI_CANDIDATE_SAMPLE.replace("困惑、委屈|失落 / 尴尬", "困惑,偷笑")

        with self.assertRaisesRegex(ValueError, "极性与表情类别错配：偷笑 属于正向"):
            self.make_extractor().enhance_expression_text(sample, template_index=4)

    def test_repeat_enhancement_replaces_existing_template_without_stacking(self):
        extractor = self.make_extractor()
        with mock.patch.object(content_extractor.random, "choice", side_effect=["委屈"]):
            first = extractor.enhance_expression_text(MULTI_CANDIDATE_SAMPLE, template_index=4)

        second = extractor.enhance_expression_text(first, template_index=4)

        self.assertEqual(first, second)
        self.assertEqual(second.count("眉："), 1)
        self.assertEqual(second.count("眼："), 1)
        self.assertEqual(second.count("嘴："), 1)
        self.assertIn("具体表情: 委屈，", second)


if __name__ == "__main__":
    unittest.main()
