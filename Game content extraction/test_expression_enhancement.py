import importlib.util
import json
import pathlib
import re
import shutil
import sys
import unittest
import uuid
from unittest import mock


MODULE_PATH = pathlib.Path(__file__).with_name("内容抽取.py")
REPO_ROOT = MODULE_PATH.parent.parent
FRONT_PROMPT_PATH = REPO_ROOT / "prompts" / "2.group-image" / "组图 23 表情前置.md"
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

NEW_FORMAT_NEGATIVE_SAMPLE = (
    "极性: 负向\n"
    "剧情: [目标物]突然让人生气\n"
    "单人/多人: 单人\n"
    "具体表情: 生气\n"
    "人物定位: 画面中间人物\n"
    "表情功能: 生气\n"
    "适配提示: 眼神回指[目标物]\n"
    "禁用区域: 姿态不变\n"
)

NEW_FORMAT_LIBRARY = """# 测试表情库

## 一、正向表情

### 1. 喜欢

**单人模板 1-8**
1. 爱心眼心动；眉：双眉舒展；眼：双眼变成爱心形看向[目标物]；脸颊：双颊泛红；嘴：小弧口开心张开。
2. 偷看脸红；眉：一侧眉尾轻抬；眼：一眼偷看[目标物]，另一眼半垂；脸颊：靠近偷看方向更红；嘴：嘴角藏着小笑。
3. 亮眼惊喜；眉：眉尾微微上抬；眼：双眼圆亮看向[目标物]；嘴：半开成惊喜小口。
4. 甜到眯眼；眉：双眉柔和放低；眼：双眼舒服眯起；脸颊：脸颊鼓出甜弧；嘴：嘴角软软上弯。
5. 露齿捧场；眉：一侧眉峰高高抬起；眼：双眼弯成笑眼；牙齿：露出整齐大白牙；嘴：咧开成捧场大笑。
6. 舌尖期待；眉：一侧眉尾期待抬起；眼：一眼盯住[目标物]；舌头：舌尖轻轻露出；嘴：张成小期待口。
7. 口水心动；眉：双眉明显上拱；眼：双眼黏住[目标物]；口边：嘴角挂一滴小口水；嘴：半张并上扬。
8. 脸颊开花笑；眉：双眉高低展开；眼：一眼看住[目标物]，另一眼开心弯起；脸颊：红晕像圆形贴片；嘴：张开成饱满笑弧。

**多人模板 1-8**
1. 爱心眼心动；眉：双眉舒展；眼：双眼变成爱心形看向[对方人物]；脸颊：双颊泛红；嘴：小弧口开心张开。
2. 偷看脸红；眉：一侧眉尾轻抬；眼：一眼偷看[对方人物]，另一眼半垂；脸颊：靠近偷看方向更红；嘴：嘴角藏着小笑。
3. 亮眼惊喜；眉：眉尾微微上抬；眼：双眼圆亮看向[对方人物]；嘴：半开成惊喜小口。
4. 甜到眯眼；眉：双眉柔和放低；眼：双眼舒服眯起回应[对方人物]；脸颊：脸颊鼓出甜弧；嘴：嘴角软软上弯。
5. 露齿捧场；眉：一侧眉峰高高抬起；眼：双眼弯成笑眼看向[对方人物]；牙齿：露出整齐大白牙；嘴：咧开成捧场大笑。
6. 舌尖期待；眉：一侧眉尾期待抬起；眼：一眼盯住[对方人物]；舌头：舌尖轻轻露出；嘴：张成小期待口。
7. 口水心动；眉：双眉明显上拱；眼：双眼在[对方人物]和[目标物]之间发亮；口边：嘴角挂一滴小口水；嘴：半张并上扬。
8. 脸颊开花笑；眉：双眉高低展开；眼：一眼看住[对方人物]，另一眼开心弯起；脸颊：红晕像圆形贴片；嘴：张开成饱满笑弧。

## 二、负向表情

### 1. 生气

**单人模板 1-8**
1. 气到脸红；眉：一侧眉头压低，另一侧眉尾挑起；眼：一侧眼瞪住[目标物]，另一侧眼收窄；脸颊：两侧脸颊明显涨红；嘴：嘴巴抿紧成下压斜线。
2. 咬牙爆筋；眉：双眉向眉心挤紧；眼：双眼怒视[目标物]；额头：额角鼓起一小段卡通青筋；牙齿：上下牙咬成锯齿线。
3. 鼓脸憋气；眉：一侧眉尾下压；眼：一眼盯住[目标物]，另一眼半眯；脸颊：双颊鼓成气包；嘴：闭紧成圆鼓形。
4. 气到冒烟；眉：双眉低压成尖角；眼：双眼瞪向[目标物]；额头：额头上方冒两段短烟线；嘴：嘴角向下绷住。
5. 单边咬牙；眉：一侧眉心深压；眼：一侧眼锁住[目标物]；牙齿：一侧露出咬紧的牙齿；嘴：嘴角向一边拉紧。
6. 憋到发抖；眉：眉头向下挤住；眼：双眼憋红般瞪住[目标物]；脸颊：脸颊鼓起并泛红；嘴：嘴巴闭紧。
7. 气到吐血短线；眉：双眉大幅下压；眼：双眼怒瞪[目标物]；嘴：嘴巴猛地张开，吐出一小股卡通红色短线；口边：红色短线只停在嘴边。
8. 笑不出来的怒脸；眉：一侧眉峰高挑，另一侧眉头压低；眼：一眼冷冷盯着[目标物]；牙齿：露出一小段怒笑齿线；嘴：嘴角想笑却僵住。

**多人模板 1-8**
1. 气到脸红；眉：一侧眉头压低，另一侧眉尾挑起；眼：一侧眼瞪住[对方人物]，另一侧眼扫向[目标物]；脸颊：两侧脸颊明显涨红；嘴：嘴巴抿紧成下压斜线。
2. 咬牙爆筋；眉：双眉向眉心挤紧；眼：双眼怒视[对方人物]；额头：额角鼓起一小段卡通青筋；牙齿：上下牙咬成锯齿线。
3. 鼓脸憋气；眉：一侧眉尾下压；眼：一眼盯住[对方人物]，另一眼半眯；脸颊：双颊鼓成气包；嘴：闭紧成圆鼓形。
4. 气到冒烟；眉：双眉低压成尖角；眼：双眼瞪向[对方人物]；额头：额头上方冒两段短烟线；嘴：嘴角向下绷住。
5. 单边咬牙；眉：一侧眉心深压；眼：一侧眼锁住[对方人物]；牙齿：一侧露出咬紧的牙齿；嘴：嘴角向一边拉紧。
6. 憋到发抖；眉：眉头向下挤住；眼：双眼憋红般瞪住[对方人物]；脸颊：脸颊鼓起并泛红；嘴：嘴巴闭紧。
7. 气到吐血短线；眉：双眉大幅下压；眼：双眼怒瞪[对方人物]；嘴：嘴巴猛地张开，吐出一小股卡通红色短线；口边：红色短线只停在嘴边。
8. 笑不出来的怒脸；眉：一侧眉峰高挑，另一侧眉头压低；眼：一眼冷冷盯着[对方人物]；牙齿：露出一小段怒笑齿线；嘴：嘴角想笑却僵住。
"""

FLEXIBLE_ANCHOR_LIBRARY = (
    NEW_FORMAT_LIBRARY
    .replace(
        "1. 气到脸红；眉：一侧眉头压低，另一侧眉尾挑起；眼：一侧眼瞪住[目标物]，另一侧眼收窄；脸颊：两侧脸颊明显涨红；嘴：嘴巴抿紧成下压斜线。",
        "1. 鸭嘴瘪住；嘴：嘴巴向前瘪成小鸭嘴形；眼：双眼湿漉漉看向[目标物]；脸颊：双颊被瘪嘴挤得微微鼓起。",
    )
    .replace(
        "2. 咬牙爆筋；眉：双眉向眉心挤紧；眼：双眼怒视[目标物]；额头：额角鼓起一小段卡通青筋；牙齿：上下牙咬成锯齿线。",
        "2. 空白眼黑线；眼：双眼空白看向[目标物]；额头：额头垂下几条短短卡通黑线；嘴：嘴巴僵成细缝。",
    )
    .replace(
        "3. 鼓脸憋气；眉：一侧眉尾下压；眼：一眼盯住[目标物]，另一眼半眯；脸颊：双颊鼓成气包；嘴：闭紧成圆鼓形。",
        "3. 冷青额头反胃；额头：额头上半部出现一小片冷青色难受阴影；眼：眼皮发软避开[目标物]；口边：嘴边冒出一小段卡通呕吐短线。",
    )
    .replace(
        "1. 气到脸红；眉：一侧眉头压低，另一侧眉尾挑起；眼：一侧眼瞪住[对方人物]，另一侧眼扫向[目标物]；脸颊：两侧脸颊明显涨红；嘴：嘴巴抿紧成下压斜线。",
        "1. 鸭嘴瘪住；嘴：嘴巴向前瘪成小鸭嘴形；眼：双眼湿漉漉看向[对方人物]；脸颊：双颊被瘪嘴挤得微微鼓起。",
    )
    .replace(
        "2. 咬牙爆筋；眉：双眉向眉心挤紧；眼：双眼怒视[对方人物]；额头：额角鼓起一小段卡通青筋；牙齿：上下牙咬成锯齿线。",
        "2. 空白眼黑线；眼：双眼空白看向[对方人物]；额头：额头垂下几条短短卡通黑线；嘴：嘴巴僵成细缝。",
    )
    .replace(
        "3. 鼓脸憋气；眉：一侧眉尾下压；眼：一眼盯住[对方人物]，另一眼半眯；脸颊：双颊鼓成气包；嘴：闭紧成圆鼓形。",
        "3. 冷青额头反胃；额头：额头上半部出现一小片冷青色难受阴影；眼：眼皮发软避开[对方人物]；口边：嘴边冒出一小段卡通呕吐短线。",
    )
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
        extractor.expression_stats_file = str(temp_dir / "expression_stats.json")

        if history_data is not None:
            pathlib.Path(extractor.history_file).write_text(
                json.dumps(history_data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        extractor.draw_history = extractor._load_draw_history()
        extractor.expression_stats = extractor._load_expression_stats()
        return extractor

    def make_extractor_with_library(self, library_text, history_data=None):
        extractor = self.make_extractor(history_data)
        library_path = pathlib.Path(extractor.history_file).with_name("expression_library.md")
        library_path.write_text(library_text, encoding="utf-8")
        extractor._get_expression_library_path = lambda: str(library_path)
        return extractor

    def read_front_prompt_categories(self, polarity):
        prompt_text = FRONT_PROMPT_PATH.read_text(encoding="utf-8")
        match = re.search(rf"^{polarity}类别：(.+)$", prompt_text, flags=re.MULTILINE)
        self.assertIsNotNone(match, f"缺少{polarity}类别行")
        category_text = match.group(1).rstrip("。")
        return [item.strip() for item in re.split(r"[、，,]", category_text) if item.strip()]

    def test_official_expression_library_uses_v2_category_counts(self):
        self.assertEqual(len(self.library["正向"]), 24)
        self.assertEqual(len(self.library["负向"]), 24)

        for polarity, categories in self.library.items():
            for category, templates in categories.items():
                for audience in ("单人", "多人"):
                    with self.subTest(polarity=polarity, category=category, audience=audience):
                        self.assertEqual(len(templates[audience]), 8)

    def test_official_expression_library_templates_use_flexible_face_fields(self):
        face_fields = content_extractor.BlindBoxExtractor.EXPRESSION_FACE_FIELDS
        field_pattern = "|".join(re.escape(field) for field in face_fields)

        for polarity, categories in self.library.items():
            for category, audience_map in categories.items():
                for audience, templates in audience_map.items():
                    for template_index, template in templates.items():
                        with self.subTest(
                            polarity=polarity,
                            category=category,
                            audience=audience,
                            template_index=template_index,
                        ):
                            fields = re.findall(rf"(?:^|[；;])\s*({field_pattern})：", template)
                            self.assertGreaterEqual(len(fields), 3)
                            self.assertLessEqual(len(fields), 5)
                            self.assertTrue({"眼", "嘴"} & set(fields))
                            self.assertEqual(len(fields), len(set(fields)))

    def test_official_expression_library_templates_avoid_body_and_attachment_content(self):
        forbidden_patterns = (
            "身体",
            "姿态",
            "头部朝向",
            "四肢",
            "后退",
            "全身",
            "项链",
            "领角",
            "脖子",
            "衣领",
            "耳饰",
            "头饰",
            "面具",
            "口罩",
            "眼罩",
            "头套",
            "喷溅",
            "衣物",
            "背景",
            "画外",
        )

        for polarity, categories in self.library.items():
            for category, audience_map in categories.items():
                for audience, templates in audience_map.items():
                    for template_index, template in templates.items():
                        detail_text = template.split("；", 1)[1] if "；" in template else template
                        with self.subTest(
                            polarity=polarity,
                            category=category,
                            audience=audience,
                            template_index=template_index,
                        ):
                            for forbidden in forbidden_patterns:
                                self.assertNotIn(forbidden, detail_text)

    def test_front_prompt_categories_match_expression_library(self):
        self.assertEqual(self.read_front_prompt_categories("正向"), list(self.library["正向"].keys()))
        self.assertEqual(self.read_front_prompt_categories("负向"), list(self.library["负向"].keys()))

    def test_official_v2_library_enhances_sample_categories(self):
        samples = (
            ("正向", "喜欢"),
            ("正向", "眯眼坏笑"),
            ("负向", "反胃"),
            ("负向", "犯困睡着"),
        )

        for polarity, category in samples:
            with self.subTest(polarity=polarity, category=category):
                sample = NEW_FORMAT_NEGATIVE_SAMPLE.replace("极性: 负向", f"极性: {polarity}").replace(
                    "具体表情: 生气", f"具体表情: {category}"
                ).replace("表情功能: 生气", f"表情功能: {category}")
                result = self.make_extractor().enhance_expression_text(sample, template_index=1)
                self.assertIn(f"具体表情: {category}，", result)
                self.assertRegex(result, r"；(眉|眼|脸颊|额头|嘴|牙齿|舌头|口边|脸侧)：")

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
        sample = MULTI_CANDIDATE_SAMPLE.replace("困惑、委屈|失落 / 尴尬", "困惑,忍笑")

        with self.assertRaisesRegex(ValueError, "极性与表情类别错配：忍笑 属于正向"):
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
                        "5": 3,
                        "6": 2,
                        "7": 1,
                        "8": 0,
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

        self.assertEqual(captured["options"], [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(captured["k"], 1)
        self.assertAlmostEqual(captured["weights"][0], 1 / 3)
        self.assertAlmostEqual(captured["weights"][1], 1.0)
        self.assertAlmostEqual(captured["weights"][2], 0.5)
        self.assertAlmostEqual(captured["weights"][3], 1.0)
        self.assertAlmostEqual(captured["weights"][4], 0.25)
        self.assertAlmostEqual(captured["weights"][5], 1 / 3)
        self.assertAlmostEqual(captured["weights"][6], 0.5)
        self.assertAlmostEqual(captured["weights"][7], 1.0)
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
                        "1": 2,
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

        self.assertEqual(captured["options"], [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(captured["k"], 1)
        self.assertAlmostEqual(captured["weights"][0], 1 / 3)
        self.assertAlmostEqual(captured["weights"][1], 1.0)
        self.assertAlmostEqual(captured["weights"][2], 1.0)
        self.assertAlmostEqual(captured["weights"][3], 1.0)
        self.assertAlmostEqual(captured["weights"][4], 1.0)
        self.assertAlmostEqual(captured["weights"][5], 1.0)
        self.assertAlmostEqual(captured["weights"][6], 0.5)
        self.assertAlmostEqual(captured["weights"][7], 1.0)
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

    def test_new_format_template_keeps_variant_and_extra_face_fields(self):
        extractor = self.make_extractor_with_library(NEW_FORMAT_LIBRARY)

        result = extractor.enhance_expression_text(NEW_FORMAT_NEGATIVE_SAMPLE, template_index=1)

        self.assertIn("具体表情: 生气，气到脸红；眉：", result)
        self.assertIn("脸颊：两侧脸颊明显涨红", result)
        self.assertIn("嘴：嘴巴抿紧成下压斜线", result)
        self.assertEqual(
            extractor.draw_history["expression_pools"]["expression_template:负向:单人:生气"],
            {"1": 1},
        )

    def test_flexible_anchor_templates_can_start_with_any_face_field(self):
        extractor = self.make_extractor_with_library(FLEXIBLE_ANCHOR_LIBRARY)

        mouth_result = extractor.enhance_expression_text(NEW_FORMAT_NEGATIVE_SAMPLE, template_index=1)
        eye_result = extractor.enhance_expression_text(NEW_FORMAT_NEGATIVE_SAMPLE, template_index=2)
        forehead_result = extractor.enhance_expression_text(NEW_FORMAT_NEGATIVE_SAMPLE, template_index=3)

        self.assertIn("具体表情: 生气，鸭嘴瘪住；嘴：嘴巴向前瘪成小鸭嘴形", mouth_result)
        self.assertIn("具体表情: 生气，空白眼黑线；眼：双眼空白看向[目标物]", eye_result)
        self.assertIn("具体表情: 生气，冷青额头反胃；额头：额头上半部出现一小片冷青色难受阴影", forehead_result)

    def test_repeat_enhancement_replaces_flexible_anchor_without_stacking(self):
        extractor = self.make_extractor_with_library(FLEXIBLE_ANCHOR_LIBRARY)
        first = extractor.enhance_expression_text(NEW_FORMAT_NEGATIVE_SAMPLE, template_index=1)

        second = extractor.enhance_expression_text(first, template_index=1)

        self.assertEqual(first, second)
        self.assertEqual(second.count("鸭嘴瘪住"), 1)
        self.assertEqual(second.count("嘴："), 1)
        self.assertEqual(second.count("眼："), 1)
        self.assertEqual(second.count("脸颊："), 1)

    def test_repeat_enhancement_replaces_new_format_without_stacking(self):
        extractor = self.make_extractor_with_library(NEW_FORMAT_LIBRARY)
        first = extractor.enhance_expression_text(NEW_FORMAT_NEGATIVE_SAMPLE, template_index=7)

        second = extractor.enhance_expression_text(first, template_index=7)

        self.assertEqual(first, second)
        self.assertEqual(second.count("气到吐血短线"), 1)
        self.assertEqual(second.count("眉："), 1)
        self.assertEqual(second.count("眼："), 1)
        self.assertEqual(second.count("嘴："), 1)
        self.assertEqual(second.count("口边："), 1)

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

    def test_expression_stats_summary_groups_categories_by_count(self):
        extractor = self.make_extractor()
        extractor.expression_stats["committed_counts"]["正向"] = {
            "喜欢": 1,
            "崇拜": 2,
            "感动": 3,
            "害羞": 4,
            "开心": 5,
        }
        extractor.expression_stats["committed_counts"]["负向"] = {
            "生气": 1,
            "不耐烦": 2,
            "咬牙硬撑": 3,
            "懊恼": 4,
            "困惑": 6,
        }

        summary = extractor._format_expression_stats_summary()

        self.assertIn("正向：", summary)
        self.assertIn("权重5（0次，优先补齐）：满足", summary)
        self.assertIn("权重4（1次，优先可用）：喜欢 1", summary)
        self.assertIn("权重3（2次，正常可用）：崇拜 2", summary)
        self.assertIn("权重2（3-4次，降权）：感动 3，害羞 4", summary)
        self.assertIn("权重1（5次及以上，强降权）：开心 5", summary)
        self.assertIn("负向：", summary)
        self.assertIn("权重4（1次，优先可用）：生气 1", summary)
        self.assertIn("权重3（2次，正常可用）：不耐烦 2", summary)
        self.assertIn("权重2（3-4次，降权）：咬牙硬撑 3，懊恼 4", summary)
        self.assertIn("权重1（5次及以上，强降权）：困惑 6", summary)
        self.assertIn("统计口径：每组输入只统计最后一次实际使用结果", summary)
        self.assertIn("统计权重只在强贴合候选内排序", summary)
        self.assertIn("权重1-2仅在唯一强匹配或功能明显更贴合时使用", summary)
        self.assertIn("不得为了补低频选择弱相关表情", summary)

    def test_expression_stats_commits_only_latest_result_for_same_input(self):
        extractor = self.make_extractor()
        first = extractor.enhance_expression_text(NEGATIVE_SAMPLE, template_index=4)
        second = extractor.enhance_expression_text(
            NEGATIVE_SAMPLE.replace("具体表情: 困惑", "具体表情: 生气"),
            template_index=4,
        )

        extractor._stage_expression_stats_result(NEGATIVE_SAMPLE, first)
        extractor._stage_expression_stats_result(NEGATIVE_SAMPLE, second)
        extractor._commit_pending_expression_stats()

        counts = extractor.expression_stats["committed_counts"]["负向"]
        self.assertNotIn("困惑", counts)
        self.assertEqual(counts["生气"], 1)

    def test_expression_stats_commits_previous_input_when_input_changes(self):
        extractor = self.make_extractor()
        first = extractor.enhance_expression_text(NEGATIVE_SAMPLE, template_index=4)
        changed_input = NEGATIVE_SAMPLE.replace("具体表情: 困惑", "具体表情: 生气")
        second = extractor.enhance_expression_text(changed_input, template_index=4)

        extractor._stage_expression_stats_result(NEGATIVE_SAMPLE, first)
        extractor._stage_expression_stats_result(changed_input, second)
        extractor._commit_pending_expression_stats()

        counts = extractor.expression_stats["committed_counts"]["负向"]
        self.assertEqual(counts["困惑"], 1)
        self.assertEqual(counts["生气"], 1)

    def test_expression_stats_recommit_replaces_current_committed_result(self):
        extractor = self.make_extractor()
        first = extractor.enhance_expression_text(NEGATIVE_SAMPLE, template_index=4)
        second = extractor.enhance_expression_text(
            NEGATIVE_SAMPLE.replace("具体表情: 困惑", "具体表情: 生气"),
            template_index=4,
        )

        extractor._stage_expression_stats_result(NEGATIVE_SAMPLE, first)
        extractor._commit_pending_expression_stats()
        extractor._stage_expression_stats_result(NEGATIVE_SAMPLE, second)
        extractor._commit_pending_expression_stats()

        counts = extractor.expression_stats["committed_counts"]["负向"]
        self.assertNotIn("困惑", counts)
        self.assertEqual(counts["生气"], 1)

    def test_reduce_expression_stats_for_polarity_reduces_selected_polarity_only(self):
        extractor = self.make_extractor()
        extractor.expression_stats["committed_counts"]["正向"] = {
            "喜欢": 7,
            "崇拜": 2,
            "不存在": 9,
        }
        extractor.expression_stats["committed_counts"]["负向"] = {
            "困惑": 5,
        }

        changed_count = extractor._reduce_expression_stats_for_polarity("正向", 3)

        self.assertEqual(changed_count, 2)
        self.assertEqual(extractor.expression_stats["committed_counts"]["正向"]["喜欢"], 4)
        self.assertNotIn("崇拜", extractor.expression_stats["committed_counts"]["正向"])
        self.assertEqual(extractor.expression_stats["committed_counts"]["正向"]["不存在"], 9)
        self.assertEqual(extractor.expression_stats["committed_counts"]["负向"]["困惑"], 5)

    def test_reduce_expression_stats_for_polarity_preserves_current_tracking_fields(self):
        extractor = self.make_extractor()
        extractor.expression_stats["committed_counts"]["负向"] = {
            "困惑": 5,
        }
        extractor.expression_stats["current_input_hash"] = "abc"
        extractor.expression_stats["current_last_entries"] = [
            {"polarity": "负向", "expression": "困惑"},
        ]
        extractor.expression_stats["current_committed_entries"] = [
            {"polarity": "负向", "expression": "困惑"},
        ]

        extractor._reduce_expression_stats_for_polarity("负向", 2)

        self.assertEqual(extractor.expression_stats["committed_counts"]["负向"]["困惑"], 3)
        self.assertEqual(extractor.expression_stats["current_input_hash"], "abc")
        self.assertEqual(
            extractor.expression_stats["current_last_entries"],
            [{"polarity": "负向", "expression": "困惑"}],
        )
        self.assertEqual(
            extractor.expression_stats["current_committed_entries"],
            [{"polarity": "负向", "expression": "困惑"}],
        )

    def test_reduce_expression_stats_for_polarity_requires_positive_integer(self):
        extractor = self.make_extractor()

        with self.assertRaisesRegex(ValueError, "降低次数必须是正整数"):
            extractor._reduce_expression_stats_for_polarity("正向", 0)
        with self.assertRaisesRegex(ValueError, "降低次数必须是正整数"):
            extractor._reduce_expression_stats_for_polarity("正向", "bad")
        with self.assertRaisesRegex(ValueError, "极性只能选择正向或负向"):
            extractor._reduce_expression_stats_for_polarity("全部", 1)

    def test_expression_detail_summary_extracts_character_and_expression(self):
        extractor = self.make_extractor()
        result = extractor.enhance_expression_text(NEGATIVE_SAMPLE, template_index=4)

        summary = extractor._format_expression_detail_summary(result)

        self.assertIn("1. 人物定位：画面中间人物", summary)
        self.assertIn("具体表情：困惑，", summary)
        self.assertNotIn("表情功能", summary)


if __name__ == "__main__":
    unittest.main()
