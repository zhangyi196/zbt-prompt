import importlib.util
import json
import os
import pathlib
import types
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
        self.original_ctypes = content_extractor.ctypes
        self.original_environ = os.environ.copy()
        self.had_meipass = hasattr(content_extractor.sys, "_MEIPASS")
        self.original_meipass = getattr(content_extractor.sys, "_MEIPASS", None)
        self.showinfo_calls = []
        content_extractor.messagebox.showinfo = self.fake_showinfo

    def tearDown(self):
        content_extractor.urllib.request.urlopen = self.original_urlopen
        content_extractor.messagebox.showinfo = self.original_showinfo
        content_extractor.ctypes = self.original_ctypes
        os.environ.clear()
        os.environ.update(self.original_environ)
        if self.had_meipass:
            content_extractor.sys._MEIPASS = self.original_meipass
        elif hasattr(content_extractor.sys, "_MEIPASS"):
            delattr(content_extractor.sys, "_MEIPASS")

    def make_extractor(self):
        return content_extractor.BlindBoxExtractor.__new__(content_extractor.BlindBoxExtractor)

    def fake_showinfo(self, title, message):
        self.showinfo_calls.append((title, message))

    def make_release_payload(self, version="0.1.6", assets=None, **overrides):
        payload = {
            "tag_name": f"v{version}",
            "html_url": f"https://example.test/releases/v{version}",
            "body": f"release {version}",
            "draft": False,
        }
        if assets is not None:
            payload["assets"] = assets
        payload.update(overrides)
        return payload

    def make_asset(self, name, url=None, **overrides):
        asset = {
            "name": name,
            "browser_download_url": url or f"https://example.test/downloads/{name}",
            "size": 123456,
            "content_type": "application/octet-stream",
        }
        asset.update(overrides)
        return asset

    def get_installer_metadata(self, result):
        dict_keys = (
            "installer_asset",
            "installer",
            "download_asset",
            "asset",
        )
        for key in dict_keys:
            value = result.get(key)
            if isinstance(value, dict):
                return {
                    "name": value.get("name"),
                    "url": (
                        value.get("url")
                        or value.get("download_url")
                        or value.get("browser_download_url")
                    ),
                    "size": value.get("size"),
                }

        name = (
            result.get("installer_name")
            or result.get("installer_asset_name")
            or result.get("asset_name")
        )
        url = (
            result.get("installer_url")
            or result.get("installer_download_url")
            or result.get("download_url")
            or result.get("browser_download_url")
        )
        size = (
            result.get("installer_size")
            if "installer_size" in result
            else result.get("asset_size")
        )

        if name is None and url is None and size is None:
            return None

        return {
            "name": name,
            "url": url,
            "size": size,
        }

    def assert_installer_metadata(self, result, *, name, url, size):
        installer = self.get_installer_metadata(result)
        self.assertIsNotNone(installer, "expected installer metadata in update result")
        self.assertEqual(installer["name"], name)
        self.assertEqual(installer["url"], url)
        self.assertEqual(installer["size"], size)

    def assert_manual_download_required(self, result, *, version="0.1.6", url):
        self.assertEqual(result["status"], "update_available")
        self.assertEqual(result["latest_version"], version)
        self.assertEqual(result["url"], url)
        self.assertIsNone(self.get_installer_metadata(result))
        self.assertEqual(
            result["installer_error"],
            "GitHub Release 未提供安装包元数据，无法直接下载安装。",
        )

    def test_latest_404_falls_back_to_releases_list(self):
        def fake_urlopen(request, timeout):
            if request.full_url == content_extractor.UPDATE_API_URL:
                raise urllib.error.HTTPError(request.full_url, 404, "Not Found", None, None)
            if request.full_url == content_extractor.UPDATE_RELEASES_LIST_API_URL:
                return FakeResponse(
                    [
                        self.make_release_payload("0.1.1", body="current"),
                        self.make_release_payload(
                            "0.1.6",
                            body="next",
                            assets=[
                                self.make_asset("zbt-prompt-source-20260509.zip"),
                                self.make_asset(
                                    "GameContentExtraction-Setup-v0.1.6.exe",
                                    url="https://example.test/downloads/installer-v0.1.6.exe",
                                    size=456789,
                                ),
                            ],
                        ),
                    ]
                )
            raise AssertionError(f"unexpected URL: {request.full_url}")

        content_extractor.urllib.request.urlopen = fake_urlopen

        result = self.make_extractor()._fetch_latest_release()

        self.assertEqual(result["status"], "update_available")
        self.assertEqual(result["latest_version"], "0.1.6")
        self.assertEqual(result["url"], "https://example.test/releases/v0.1.6")
        self.assert_installer_metadata(
            result,
            name="GameContentExtraction-Setup-v0.1.6.exe",
            url="https://example.test/downloads/installer-v0.1.6.exe",
            size=456789,
        )

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

    def test_latest_403_and_429_fall_back_to_latest_release_redirect(self):
        redirect_url = "https://github.com/zhangyi196/zbt-prompt/releases/tag/v0.1.6"

        for status_code in (403, 429):
            with self.subTest(status_code=status_code):
                def fake_urlopen(request, timeout):
                    if request.full_url == content_extractor.UPDATE_API_URL:
                        raise urllib.error.HTTPError(
                            request.full_url,
                            status_code,
                            "Forbidden",
                            None,
                            None,
                        )
                    if request.full_url == content_extractor.UPDATE_RELEASES_LATEST_URL:
                        return FakeResponse({"ignored": True}, final_url=redirect_url)
                    raise AssertionError(f"unexpected URL: {request.full_url}")

                content_extractor.urllib.request.urlopen = fake_urlopen

                result = self.make_extractor()._fetch_latest_release()

                self.assert_manual_download_required(result, url=redirect_url)

    def test_build_update_result_selects_installer_asset_metadata(self):
        extractor = self.make_extractor()

        result = extractor._build_update_result(
            self.make_release_payload(
                "0.1.6",
                assets=[
                    self.make_asset("checksums.txt"),
                    self.make_asset("zbt-prompt-source-20260509.zip"),
                    self.make_asset(
                        "GameContentExtraction-Setup-v0.1.6.exe",
                        url="https://example.test/downloads/setup-v0.1.6.exe",
                        size=987654,
                    ),
                ],
            )
        )

        self.assertEqual(result["status"], "update_available")
        self.assertEqual(result["latest_version"], "0.1.6")
        self.assert_installer_metadata(
            result,
            name="GameContentExtraction-Setup-v0.1.6.exe",
            url="https://example.test/downloads/setup-v0.1.6.exe",
            size=987654,
        )

    def test_build_update_result_without_installer_asset_keeps_update_available(self):
        extractor = self.make_extractor()

        result = extractor._build_update_result(
            self.make_release_payload(
                "0.1.6",
                assets=[
                    self.make_asset("zbt-prompt-source-20260509.zip"),
                    self.make_asset("checksums.txt"),
                ],
            )
        )

        self.assertEqual(result["status"], "update_available")
        self.assertEqual(result["latest_version"], "0.1.6")
        self.assertIsNone(self.get_installer_metadata(result))
        self.assertTrue(result["installer_error"])

    def test_extract_installer_asset_prefers_setup_executable(self):
        extractor = self.make_extractor()
        selected, error = extractor._extract_installer_asset(
            self.make_release_payload(
                "0.1.6",
                assets=[
                    self.make_asset("zbt-prompt-source-20260509.zip"),
                    self.make_asset("notes.txt"),
                    self.make_asset(
                        "GameContentExtraction-Setup-v0.1.6.exe",
                        url="https://example.test/downloads/setup-v0.1.6.exe",
                        size=654321,
                    ),
                ],
            )
        )

        self.assertIsNotNone(selected)
        self.assertIsNone(error)
        self.assertEqual(selected["name"], "GameContentExtraction-Setup-v0.1.6.exe")
        self.assertEqual(
            selected.get("download_url") or selected.get("browser_download_url") or selected.get("url"),
            "https://example.test/downloads/setup-v0.1.6.exe",
        )
        self.assertEqual(selected["size"], 654321)

    def test_extract_installer_asset_without_assets_reports_manual_download(self):
        extractor = self.make_extractor()

        selected, error = extractor._extract_installer_asset(
            self.make_release_payload("0.1.6")
        )

        self.assertIsNone(selected)
        self.assertEqual(
            error,
            "GitHub Release 未提供安装包元数据，无法直接下载安装。",
        )

    def test_select_installer_asset_metadata_prefers_setup_exe_and_skips_invalid_candidates(self):
        extractor = self.make_extractor()

        selected = extractor._select_installer_asset_metadata(
            [
                self.make_asset("notes.txt"),
                self.make_asset(
                    "GameContentExtraction-v0.1.6.exe",
                    url="https://example.test/downloads/generic-v0.1.6.exe",
                ),
                self.make_asset(
                    "GameContentExtraction-Setup-v0.1.6.exe",
                    url="https://example.test/downloads/setup-v0.1.6.exe",
                ),
                self.make_asset(
                    "GameContentExtraction-portable-v0.1.6.exe",
                    url="https://example.test/downloads/portable-v0.1.6.exe",
                ),
                self.make_asset(
                    "GameContentExtraction-v0.1.6.msi",
                    url="https://example.test/downloads/setup-v0.1.6.msi",
                ),
                self.make_asset(
                    "GameContentExtraction-Setup-v0.1.6.exe",
                    browser_download_url="",
                ),
            ]
        )

        self.assertIsNotNone(selected)
        self.assertEqual(selected["name"], "GameContentExtraction-Setup-v0.1.6.exe")
        self.assertEqual(
            selected["browser_download_url"],
            "https://example.test/downloads/setup-v0.1.6.exe",
        )

    def test_score_installer_asset_prefers_setup_exe_over_portable_msi(self):
        extractor = self.make_extractor()

        setup_exe = extractor._score_installer_asset(
            "GameContentExtraction-Setup-v0.1.6.exe",
            ".exe",
        )
        plain_msi = extractor._score_installer_asset(
            "GameContentExtraction-v0.1.6.msi",
            ".msi",
        )
        portable_exe = extractor._score_installer_asset(
            "GameContentExtraction-portable-v0.1.6.exe",
            ".exe",
        )

        self.assertGreater(setup_exe, plain_msi)
        self.assertGreater(plain_msi, portable_exe)

    def test_sanitize_environment_for_external_process_launch_clears_pyinstaller_state(self):
        extractor = self.make_extractor()
        fake_calls = []

        class FakeKernel32:
            def SetDllDirectoryW(self, value):
                fake_calls.append(value)
                return 1

        content_extractor.ctypes = types.SimpleNamespace(
            windll=types.SimpleNamespace(kernel32=FakeKernel32())
        )
        content_extractor.sys._MEIPASS = r"C:\Users\Administrator\AppData\Local\Temp\_MEI12345"
        os.environ["PATH"] = os.pathsep.join(
            [
                r"C:\Windows\System32",
                r"C:\Users\Administrator\AppData\Local\Temp\_MEI12345",
                r"C:\Users\Administrator\AppData\Local\Temp\_MEI12345\Scripts",
                r"D:\Tools",
            ]
        )
        os.environ["TCL_LIBRARY"] = r"C:\Users\Administrator\AppData\Local\Temp\_MEI12345\_tcl_data"
        os.environ["TK_LIBRARY"] = r"C:\Users\Administrator\AppData\Local\Temp\_MEI12345\_tk_data"
        os.environ["_MEIPASS2"] = r"C:\Users\Administrator\AppData\Local\Temp\_MEI12345"
        os.environ["_PYI_APPLICATION_HOME_DIR"] = r"C:\Users\Administrator\AppData\Local\Temp\_MEI12345"
        os.environ["_PYI_PARENT_PROCESS_LEVEL"] = "0"

        extractor._sanitize_environment_for_external_process_launch()

        self.assertEqual(fake_calls, [None])
        self.assertEqual(os.environ["PATH"], os.pathsep.join([r"C:\Windows\System32", r"D:\Tools"]))
        self.assertNotIn("TCL_LIBRARY", os.environ)
        self.assertNotIn("TK_LIBRARY", os.environ)
        self.assertNotIn("_MEIPASS2", os.environ)
        self.assertNotIn("_PYI_APPLICATION_HOME_DIR", os.environ)
        self.assertNotIn("_PYI_PARENT_PROCESS_LEVEL", os.environ)

    def test_sanitize_environment_for_external_process_launch_without_meipass_keeps_normal_path(self):
        extractor = self.make_extractor()
        fake_calls = []

        class FakeKernel32:
            def SetDllDirectoryW(self, value):
                fake_calls.append(value)
                return 1

        content_extractor.ctypes = types.SimpleNamespace(
            windll=types.SimpleNamespace(kernel32=FakeKernel32())
        )
        if hasattr(content_extractor.sys, "_MEIPASS"):
            delattr(content_extractor.sys, "_MEIPASS")
        os.environ["PATH"] = os.pathsep.join([r"C:\Windows\System32", r"D:\Tools"])
        os.environ["_MEIPASS2"] = r"C:\Users\Administrator\AppData\Local\Temp\_MEI12345"
        os.environ["_PYI_APPLICATION_HOME_DIR"] = r"C:\Users\Administrator\AppData\Local\Temp\_MEI12345"

        extractor._sanitize_environment_for_external_process_launch()

        self.assertEqual(fake_calls, [None])
        self.assertEqual(os.environ["PATH"], os.pathsep.join([r"C:\Windows\System32", r"D:\Tools"]))
        self.assertNotIn("_MEIPASS2", os.environ)
        self.assertNotIn("_PYI_APPLICATION_HOME_DIR", os.environ)

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
