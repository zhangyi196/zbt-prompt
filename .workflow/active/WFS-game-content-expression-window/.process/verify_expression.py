import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
APP_DIR = ROOT / "Game content extraction"
MODULE_PATH = APP_DIR / "内容抽取.py"

sys.path.insert(0, str(APP_DIR))
spec = importlib.util.spec_from_file_location("content_extract", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

app = object.__new__(module.BlindBoxExtractor)

EXPECTED = (
    "眉：一侧眉尾抬起，另一侧眉尾压平；"
    "眼：一侧眼撑开看着[目标物]，另一侧眼半垂；"
    "嘴：一侧嘴巴闭住下压，另一侧嘴角收紧。"
)

library = app._load_expression_library()
assert library["负向"]["困惑"]["单人"][4] == EXPECTED
assert set(library["负向"]["困惑"]["单人"]) == {1, 2, 3, 4}
assert set(library["负向"]["困惑"]["多人"]) == {5, 6, 7, 8}

sample = (
    "极性: 负向 剧情: 手中茶杯 → 突然变成粉色甜甜圈 → 感到不解与迟疑 → "
    "手端甜甜圈发愣 [备选情绪反差方案] 单人/多人: 单人 具体表情: 困惑 "
    "人物定位: 画面中央穿粉色裙子的女士 表情功能: 困惑 "
    "适配提示: 眼神向下回指手中突然出现的粉色甜甜圈，嘴部表现出不解的微张或抿嘴，不可改变手部端托的动作。 "
    "禁用区域: 若采用该人物面部表情，该人物衣领/领带/颈部区、头发/头饰区、耳饰/耳侧饰品区不再建议修改；"
    "身体与姿态不变，头部朝向不变，四肢动作不变。"
)

result = app.enhance_expression_text(sample, template_index=4)
assert EXPECTED in result
assert "具体表情: 困惑，" + EXPECTED in result
assert "人物定位: 画面中央穿粉色裙子的女士" in result
assert "[目标物]" in result

multi_candidate_sample = sample.replace("具体表情: 困惑 ", "具体表情: 困惑、委屈|失落 / 尴尬 ")
original_random_choice = module.random.choice
module.random.choice = lambda options: "委屈" if "委屈" in options else options[0]
try:
    multi_candidate = app.enhance_expression_text(multi_candidate_sample, template_index=4)
finally:
    module.random.choice = original_random_choice
assert "具体表情: 委屈，" in multi_candidate
assert "具体表情: 困惑、委屈|不安 / 迟疑" not in multi_candidate

second = app.enhance_expression_text(result, template_index=4)
assert second.count("眉：") == 1
assert second == result

sample_positive = (
    "极性: 正向 剧情: 目标物恢复正常 单人/多人: 单人 具体表情: 偷笑 "
    "人物定位: 画面右侧人物 表情功能: 偷笑 适配提示: 眼神回指目标物。 禁用区域: 身体与姿态不变。"
)
multi = app.enhance_expression_text(sample + "\n" + sample_positive, template_index=4)
assert multi.count("眉：") == 2
assert "具体表情: 偷笑，" in multi

for bad_text in [
    "剧情: 缺少关键字段 具体表情: 困惑",
    "极性: 正向 单人/多人: 单人 具体表情: 困惑",
    "极性: 负向 单人/多人: 单人 具体表情: 不存在",
]:
    try:
        app.enhance_expression_text(bad_text, template_index=4)
    except ValueError:
        pass
    else:
        raise AssertionError(f"bad text did not raise: {bad_text}")

try:
    app.enhance_expression_text(sample, template_index=5)
except ValueError as exc:
    assert "单人模板编号必须在 1-4" in str(exc)
else:
    raise AssertionError("template range did not raise")

app2 = object.__new__(module.BlindBoxExtractor)
app2.blind_boxes = module.BLIND_BOXES
app2.animals = module.ANIMALS
app2.category_info = [
    ("large", "大型物品"),
    ("medium", "中型物品"),
    ("small", "散落小型物品"),
    ("hanging", "悬挂物品"),
]
app2.animal_info = [
    ("动物本体", "动物本体"),
    ("动物用品", "动物用品"),
    ("动物痕迹", "动物痕迹"),
]
app2.input_override_targets = {label: ("category", key) for key, label in app2.category_info}
app2.input_override_targets.update({label: ("animal", key) for key, label in app2.animal_info})
numbers, animal_type, overrides = app2._parse_input("1,5,地面动物,无大型物品,中型物品+1")
assert numbers == [1, 5]
assert animal_type == "地面动物"
assert "large" in overrides["category"]["disabled"]
assert overrides["category"]["count_delta"]["medium"] == 1

print("expression acceptance checks passed")
