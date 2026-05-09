from __future__ import annotations

import argparse
import io
import marshal
import shutil
import struct
import subprocess
import zlib
from pathlib import Path

from PyInstaller.archive.readers import CArchiveReader
from PyInstaller.archive.writers import CArchiveWriter
from PyInstaller.building.utils import replace_filename_in_code_object


REPO_ROOT = Path(__file__).resolve().parents[3]
APP_DIR = REPO_ROOT / "Game content extraction"
SOURCE_SCRIPT = APP_DIR / "内容抽取.py"
DIST_DIR = APP_DIR / "dist"
RELEASE_DIR = APP_DIR / "release"
EXTRACT_DIR = RELEASE_DIR / "extract-v014c"
BASE_INSTALLER_SCRIPT = APP_DIR / "installer.iss"
ISCC_PATH = Path.home() / "AppData/Local/Programs/Inno Setup 6/ISCC.exe"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-version", required=True)
    parser.add_argument("--compile-installer", action="store_true")
    return parser.parse_args()


def find_base_exe() -> Path:
    candidates = sorted(
        (path for path in EXTRACT_DIR.glob("*.exe") if not path.name.lower().startswith("unins")),
        key=lambda path: path.stat().st_size,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(f"No base exe found in {EXTRACT_DIR}")
    return candidates[0]


def find_main_script_key(reader: CArchiveReader) -> str:
    candidates = [
        name
        for name, meta in reader.toc.items()
        if meta[4] in {"s", "s1", "s2"}
        and not name.startswith("pyi")
        and not name.startswith("pyiboot")
    ]
    if len(candidates) != 1:
        raise RuntimeError(f"Expected exactly one main script entry, got {candidates!r}")
    return candidates[0]


def load_cookie_info(base_exe: Path, reader: CArchiveReader) -> tuple[int, str]:
    cookie_length = CArchiveWriter._COOKIE_LENGTH
    cookie_offset = reader._end_offset - cookie_length
    with base_exe.open("rb") as file_handle:
        file_handle.seek(cookie_offset)
        cookie_data = file_handle.read(cookie_length)
    _, _, _, _, pyvers, pylib_name = struct.unpack(CArchiveWriter._COOKIE_FORMAT, cookie_data)
    pylib_name = pylib_name.split(b"\0", 1)[0].decode("ascii")
    return pyvers, pylib_name


def build_replacement_code(source_text: str, original_code, replacement_filename: str, target_version: str):
    current_version_literal = f'APP_VERSION = "{target_version}"'
    if current_version_literal in source_text:
        updated_source = source_text
    else:
        updated_source = source_text.replace('APP_VERSION = "0.1.5"', current_version_literal, 1)
        if updated_source == source_text:
            raise RuntimeError("Failed to replace APP_VERSION in source script.")
    code_object = compile(updated_source, str(SOURCE_SCRIPT), "exec")
    code_object = replace_filename_in_code_object(code_object, replacement_filename)
    if not any(const == target_version for const in code_object.co_consts):
        raise RuntimeError("Patched code object does not contain the target version constant.")
    return code_object


def rebuild_onefile_exe(base_exe: Path, output_exe: Path, target_version: str) -> tuple[str, str]:
    reader = CArchiveReader(str(base_exe))
    main_key = find_main_script_key(reader)
    original_code = marshal.loads(reader.extract(main_key))
    source_text = SOURCE_SCRIPT.read_text(encoding="utf-8")
    replacement_filename = getattr(original_code, "co_filename", f"{main_key}.py")
    replacement_code = build_replacement_code(
        source_text,
        original_code,
        replacement_filename,
        target_version,
    )
    replacement_blob = marshal.dumps(replacement_code)

    pyvers, pylib_name = load_cookie_info(base_exe, reader)
    prefix = base_exe.read_bytes()[: reader._start_offset]

    archive_buffer = io.BytesIO()
    toc_entries = []

    with base_exe.open("rb") as file_handle:
        for name, entry in reader.toc.items():
            data_offset, compressed_length, data_length, compress_flag, typecode = entry
            relative_offset = archive_buffer.tell()

            if name == main_key:
                raw_data = replacement_blob
                if compress_flag:
                    raw_data = zlib.compress(raw_data, level=CArchiveWriter._COMPRESSION_LEVEL)
                archive_buffer.write(raw_data)
                toc_entries.append(
                    (relative_offset, len(raw_data), len(replacement_blob), int(compress_flag), typecode, name)
                )
                continue

            file_handle.seek(reader._start_offset + data_offset)
            raw_data = file_handle.read(compressed_length)
            archive_buffer.write(raw_data)
            toc_entries.append(
                (relative_offset, compressed_length, data_length, int(compress_flag), typecode, name)
            )

    toc_offset = archive_buffer.tell()
    toc_data = CArchiveWriter._serialize_toc(toc_entries)
    archive_buffer.write(toc_data)
    archive_length = archive_buffer.tell() + CArchiveWriter._COOKIE_LENGTH
    cookie_data = struct.pack(
        CArchiveWriter._COOKIE_FORMAT,
        CArchiveWriter._COOKIE_MAGIC_PATTERN,
        archive_length,
        toc_offset,
        len(toc_data),
        pyvers,
        pylib_name.encode("ascii"),
    )
    archive_buffer.write(cookie_data)

    output_exe.parent.mkdir(parents=True, exist_ok=True)
    output_exe.write_bytes(prefix + archive_buffer.getvalue())

    verify_reader = CArchiveReader(str(output_exe))
    verify_code = marshal.loads(verify_reader.extract(main_key))
    if getattr(verify_code, "co_filename", "") != replacement_filename:
        raise RuntimeError("Patched exe verification failed: co_filename mismatch.")
    if not any(const == target_version for const in verify_code.co_consts):
        raise RuntimeError("Patched exe verification failed: target version not found.")

    return main_key, replacement_filename


def build_temp_installer_script(target_version: str) -> Path:
    script_text = BASE_INSTALLER_SCRIPT.read_text(encoding="utf-8")
    replacements = {
        '#define MyAppVersion "0.1.5"': f'#define MyAppVersion "{target_version}"',
        '#define MyOutputName "GameContentExtraction-Setup-v0.1.5"': (
            f'#define MyOutputName "GameContentExtraction-Setup-v{target_version}"'
        ),
    }
    for old_text, new_text in replacements.items():
        if old_text not in script_text:
            raise RuntimeError(f"Expected installer token not found: {old_text}")
        script_text = script_text.replace(old_text, new_text, 1)
    installer_script = APP_DIR / f"installer.v{target_version}-test.iss"
    installer_script.write_text(script_text, encoding="utf-8")
    return installer_script


def compile_installer(installer_script: Path, target_version: str) -> Path:
    if not ISCC_PATH.exists():
        raise FileNotFoundError(f"ISCC.exe not found at {ISCC_PATH}")
    subprocess.run([str(ISCC_PATH), str(installer_script)], cwd=str(APP_DIR), check=True)
    output_installer = RELEASE_DIR / f"GameContentExtraction-Setup-v{target_version}.exe"
    if not output_installer.exists():
        raise FileNotFoundError(f"Installer build output missing: {output_installer}")
    return output_installer


def main() -> None:
    args = parse_args()
    target_version = args.target_version

    base_exe = find_base_exe()
    output_exe = DIST_DIR / "内容抽取.exe"

    main_key, replacement_filename = rebuild_onefile_exe(base_exe, output_exe, target_version)
    installer_script = build_temp_installer_script(target_version)

    print(f"Base exe: {base_exe}")
    print(f"Patched exe: {output_exe}")
    print(f"Main script key: {main_key}")
    print(f"Replacement filename: {replacement_filename}")
    print(f"Installer script: {installer_script}")

    if args.compile_installer:
        output_installer = compile_installer(installer_script, target_version)
        print(f"Installer built: {output_installer}")


if __name__ == "__main__":
    main()
