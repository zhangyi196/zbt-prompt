import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).with_name("内容抽取.py")
SPEC = importlib.util.spec_from_file_location("content_extractor", MODULE_PATH)
content_extractor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(content_extractor)


class FakeVar:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value


class FakeRoot:
    def __init__(self, clipboard_text="", raises=False):
        self.clipboard_text = clipboard_text
        self.raises = raises

    def clipboard_get(self):
        if self.raises:
            raise content_extractor.tk.TclError("clipboard unavailable")
        return self.clipboard_text


class FakeEntry:
    def __init__(self, initial="seed"):
        self.content = initial

    def delete(self, start, end):
        self.content = ""

    def insert(self, index, value):
        self.content = value


class FakeText:
    def __init__(self, initial="seed"):
        self.content = initial

    def delete(self, start, end):
        self.content = ""

    def insert(self, index, value):
        self.content = value


class ClearInputBehaviorTests(unittest.TestCase):
    def make_extractor(self, auto_paste=True, clipboard_text="from-clipboard", raises=False):
        extractor = content_extractor.BlindBoxExtractor.__new__(content_extractor.BlindBoxExtractor)
        extractor.root = FakeRoot(clipboard_text=clipboard_text, raises=raises)
        extractor.auto_paste_var = FakeVar(auto_paste)
        return extractor

    def test_clear_input_rehydrates_entry_from_clipboard_when_auto_paste_enabled(self):
        extractor = self.make_extractor(auto_paste=True, clipboard_text="123,地面动物")
        extractor.input_entry = FakeEntry(initial="old")

        extractor.clear_input()

        self.assertEqual(extractor.input_entry.content, "123,地面动物")

    def test_clear_expression_input_rehydrates_text_from_clipboard_when_auto_paste_enabled(self):
        extractor = self.make_extractor(auto_paste=True, clipboard_text="极性: 正向")
        extractor.expression_input_text = FakeText(initial="old")

        extractor.clear_expression_input()

        self.assertEqual(extractor.expression_input_text.content, "极性: 正向")

    def test_clear_expression_input_only_clears_when_auto_paste_disabled(self):
        extractor = self.make_extractor(auto_paste=False, clipboard_text="ignored")
        extractor.expression_input_text = FakeText(initial="old")

        extractor.clear_expression_input()

        self.assertEqual(extractor.expression_input_text.content, "")


if __name__ == "__main__":
    unittest.main()
