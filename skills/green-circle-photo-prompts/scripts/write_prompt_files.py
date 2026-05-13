#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="把绿圈洗图结果写成 txt 文件。",
    )
    parser.add_argument(
        "result_json",
        help="包含主 agent 汇总结果的 JSON 文件。",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="覆盖已有 txt；不传则遇到重名文件时跳过。",
    )
    return parser.parse_args()


def load_items(result_path: Path) -> list[dict]:
    data = json.loads(result_path.read_text(encoding="utf-8-sig"))
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        if isinstance(data.get("results"), list):
            items = data["results"]
        else:
            raise ValueError("JSON 对象必须包含 'results' 列表。")
    else:
        raise ValueError("结果 JSON 必须是列表，或包含 'results' 列表的对象。")

    if not all(isinstance(item, dict) for item in items):
        raise ValueError("结果中的每一项都必须是对象。")
    return items


def normalize_text_path(item: dict) -> Path:
    text_path = item.get("text_path")
    if isinstance(text_path, str) and text_path.strip():
        return Path(text_path)

    image_path = item.get("image_path")
    if not isinstance(image_path, str) or not image_path.strip():
        raise ValueError("缺少 'text_path' 时，每项都必须提供 'image_path'。")
    return Path(image_path).with_suffix(".txt")


def main() -> int:
    args = parse_args()
    result_path = Path(args.result_json).expanduser()
    if not result_path.exists():
        raise SystemExit(f"未找到结果 JSON：{result_path}")

    items = load_items(result_path)
    written = []
    skipped = []

    for item in items:
        prompt = item.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("每一项都必须包含非空的 'prompt' 字符串。")

        text_path = normalize_text_path(item).expanduser()
        text_path.parent.mkdir(parents=True, exist_ok=True)

        if text_path.exists() and not args.overwrite:
            skipped.append(str(text_path.resolve()))
            continue

        text_path.write_text(prompt.strip() + "\n", encoding="utf-8")
        written.append(str(text_path.resolve()))

    summary = {
        "written_count": len(written),
        "skipped_count": len(skipped),
        "written": written,
        "skipped": skipped,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not skipped or args.overwrite else 1


if __name__ == "__main__":
    raise SystemExit(main())
