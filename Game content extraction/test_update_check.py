import importlib.util
import json
import pathlib
import unittest
import urllib.error


MODULE_PATH = pathlib.Path(__file__).with_name("内容抽取.py")
SPEC = importlib.util.spec_from_file_location("content_extractor", MODULE_PATH)
content_extractor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(content_extractor)


class FakeResponse:
    def __init__(self, payload, final_url=None):
        self.payload = json.dumps(payload).encode("utf-8")
        self.final_url = final_url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return self.payload

    def geturl(self):
        return self.final_url or "https://example.test/releases/latest"


class FakeButton:
    def __init__(self):
        self.pack_calls = []
        self.configure_calls = []

    def pack(self, **kwargs):
        self.pack_calls.append(kwargs)

    def configure(self, **kwargs):
        self.configure_calls.append(kwargs)


class UpdateCheckTests(unittest.TestCase):
    def setUp(self):
        self.original_urlopen = content_extractor.urllib.request.urlopen
        self.original_showinfo = content_extractor.messagebox.showinfo
        self.showinfo_calls = []
        content_extractor.messagebox.showinfo = self.fake_showinfo

    def tearDown(self):
        content_extractor.urllib.request.urlopen = self.original_urlopen
        content_extractor.messagebox.showinfo = self.original_showinfo

    def make_extractor(self):
        return content_extractor.BlindBoxExtractor.__new__(content_extractor.BlindBoxExtractor)

    def fake_showinfo(self, title, message):
        self.showinfo_calls.append((title, message))

    def test_latest_404_falls_back_to_releases_list(self):
        def fake_urlopen(request, timeout):
            if request.full_url == content_extractor.UPDATE_API_URL:
                raise urllib.error.HTTPError(request.full_url, 404, "Not Found", None, None)
            if request.full_url == content_extractor.UPDATE_RELEASES_LIST_API_URL:
                return FakeResponse([
                    {
                        "tag_name": "v0.1.1",
                        "html_url": "https://example.test/releases/v0.1.1",
                        "body": "current",
                        "draft": False,
                    },
                    {
                        "tag_name": "v0.1.5",
                        "html_url": "https://example.test/releases/v0.1.5",
                        "body": "next",
                        "draft": False,
                    },
                ])
            raise AssertionError(f"unexpected URL: {request.full_url}")

        content_extractor.urllib.request.urlopen = fake_urlopen

        result = self.make_extractor()._fetch_latest_release()

        self.assertEqual(result["status"], "update_available")
        self.assertEqual(result["latest_version"], "0.1.5")
        self.assertEqual(result["url"], "https://example.test/releases/v0.1.5")

    def test_latest_404_with_empty_releases_list_returns_no_release(self):
        def fake_urlopen(request, timeout):
            if request.full_url == content_extractor.UPDATE_API_URL:
                raise urllib.error.HTTPError(request.full_url, 404, "Not Found", None, None)
            if request.full_url == content_extractor.UPDATE_RELEASES_LIST_API_URL:
                return FakeResponse([])
            raise AssertionError(f"unexpected URL: {request.full_url}")

        content_extractor.urllib.request.urlopen = fake_urlopen

        result = self.make_extractor()._fetch_latest_release()

        self.assertEqual(result["status"], "no_release")

    def test_latest_403_falls_back_to_latest_release_redirect(self):
        def fake_urlopen(request, timeout):
            if request.full_url == content_extractor.UPDATE_API_URL:
                raise urllib.error.HTTPError(request.full_url, 403, "Forbidden", None, None)
            if request.full_url == content_extractor.UPDATE_RELEASES_LATEST_URL:
                return FakeResponse(
                    {"ignored": True},
                    final_url="https://github.com/zhangyi196/zbt-prompt/releases/tag/v0.1.6",
                )
            raise AssertionError(f"unexpected URL: {request.full_url}")

        content_extractor.urllib.request.urlopen = fake_urlopen

        result = self.make_extractor()._fetch_latest_release()

        self.assertEqual(result["status"], "update_available")
        self.assertEqual(result["latest_version"], "0.1.6")
        self.assertEqual(
            result["url"],
            "https://github.com/zhangyi196/zbt-prompt/releases/tag/v0.1.6",
        )

    def test_non_update_result_keeps_manual_check_button_visible(self):
        extractor = self.make_extractor()
        extractor.update_check_in_progress = True
        extractor.latest_update_result = {"status": "update_available"}
        extractor.update_button_visible = True
        extractor.update_button = FakeButton()

        extractor._handle_update_result({"status": "up_to_date"}, silent=True)

        self.assertFalse(extractor.update_check_in_progress)
        self.assertIsNone(extractor.latest_update_result)
        self.assertTrue(extractor.update_button_visible)
        self.assertEqual(
            extractor.update_button.configure_calls[-1],
            {"text": "检查更新", "state": content_extractor.tk.NORMAL},
        )
        self.assertEqual(self.showinfo_calls, [])

    def test_manual_up_to_date_result_shows_latest_version_message(self):
        extractor = self.make_extractor()
        extractor.update_check_in_progress = True
        extractor.latest_update_result = {"status": "update_available"}
        extractor.update_button_visible = True
        extractor.update_button = FakeButton()

        extractor._handle_update_result({"status": "up_to_date"}, silent=False)

        self.assertFalse(extractor.update_check_in_progress)
        self.assertIsNone(extractor.latest_update_result)
        self.assertTrue(extractor.update_button_visible)
        self.assertEqual(
            extractor.update_button.configure_calls[-1],
            {"text": "检查更新", "state": content_extractor.tk.NORMAL},
        )
        self.assertEqual(
            self.showinfo_calls,
            [("检查更新", "当前已是最新版本。")],
        )


if __name__ == "__main__":
    unittest.main()
