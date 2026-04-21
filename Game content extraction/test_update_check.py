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
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return self.payload


class FakeButton:
    def __init__(self):
        self.pack_forget_called = False

    def pack_forget(self):
        self.pack_forget_called = True


class UpdateCheckTests(unittest.TestCase):
    def setUp(self):
        self.original_urlopen = content_extractor.urllib.request.urlopen

    def tearDown(self):
        content_extractor.urllib.request.urlopen = self.original_urlopen

    def make_extractor(self):
        return content_extractor.BlindBoxExtractor.__new__(content_extractor.BlindBoxExtractor)

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
                        "tag_name": "v0.1.2",
                        "html_url": "https://example.test/releases/v0.1.2",
                        "body": "next",
                        "draft": False,
                    },
                ])
            raise AssertionError(f"unexpected URL: {request.full_url}")

        content_extractor.urllib.request.urlopen = fake_urlopen

        result = self.make_extractor()._fetch_latest_release()

        self.assertEqual(result["status"], "update_available")
        self.assertEqual(result["latest_version"], "0.1.2")
        self.assertEqual(result["url"], "https://example.test/releases/v0.1.2")

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

    def test_non_update_result_hides_update_button(self):
        extractor = self.make_extractor()
        extractor.update_check_in_progress = True
        extractor.latest_update_result = {"status": "update_available"}
        extractor.update_button_visible = True
        extractor.update_button = FakeButton()

        extractor._handle_update_result({"status": "up_to_date"}, silent=True)

        self.assertFalse(extractor.update_check_in_progress)
        self.assertIsNone(extractor.latest_update_result)
        self.assertFalse(extractor.update_button_visible)
        self.assertTrue(extractor.update_button.pack_forget_called)


if __name__ == "__main__":
    unittest.main()
