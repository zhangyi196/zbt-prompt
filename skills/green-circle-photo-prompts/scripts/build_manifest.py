#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="为绿圈洗图 skill 生成稳定的分组清单。",
    )
    parser.add_argument("folder", help="包含源图片的根目录。")
    parser.add_argument(
        "--group-size",
        type=int,
        default=3,
        help="每组图片数量，默认 3。",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="每轮并行 worker 数量，默认 4。",
    )
    parser.add_argument(
        "--groups-per-worker",
        type=int,
        default=3,
        help="每个 worker 在单轮内最多处理的组数，默认 3。",
    )
    parser.add_argument(
        "--output",
        help="可选的 JSON 输出路径；不填则打印到标准输出。",
    )
    parser.add_argument(
        "--non-recursive",
        action="store_true",
        help="只扫描当前目录，不递归子目录。",
    )
    return parser.parse_args()


def discover_images(root: Path, recursive: bool) -> list[Path]:
    pattern = "**/*" if recursive else "*"
    images = [
        path
        for path in root.glob(pattern)
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(images, key=lambda path: path.relative_to(root).as_posix().lower())


def chunked(items: list[Path], size: int) -> list[list[Path]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def build_group(root: Path, group_index: int, images: list[Path]) -> dict:
    group_images = []
    for image_index, image_path in enumerate(images, start=1):
        relative_path = image_path.relative_to(root)
        text_path = image_path.with_suffix(".txt")
        group_images.append(
            {
                "image_index": image_index,
                "image_path": str(image_path.resolve()),
                "relative_image_path": relative_path.as_posix(),
                "text_path": str(text_path.resolve()),
                "relative_text_path": text_path.relative_to(root).as_posix(),
                "text_exists": text_path.exists(),
            }
        )

    return {
        "group_index": group_index,
        "image_count": len(group_images),
        "images": group_images,
    }


def build_manifest(
    root: Path,
    group_size: int,
    workers: int,
    groups_per_worker: int,
    recursive: bool,
) -> dict:
    if group_size <= 0:
        raise ValueError("group_size 必须大于 0")
    if workers <= 0:
        raise ValueError("workers 必须大于 0")
    if groups_per_worker <= 0:
        raise ValueError("groups_per_worker 必须大于 0")

    images = discover_images(root, recursive=recursive)
    group_paths = chunked(images, group_size)
    groups = [
        build_group(root=root, group_index=group_index, images=group_images)
        for group_index, group_images in enumerate(group_paths, start=1)
    ]

    wave_capacity = workers * groups_per_worker
    waves = []
    for wave_offset in range(0, len(groups), wave_capacity):
        wave_groups = groups[wave_offset : wave_offset + wave_capacity]
        assignment_buckets = [[] for _ in range(workers)]
        for group_index, group in enumerate(wave_groups):
            worker_index = group_index % workers
            assignment_buckets[worker_index].append(group)

        worker_assignments = []
        for worker_index, assigned_groups in enumerate(assignment_buckets, start=1):
            if len(assigned_groups) > groups_per_worker:
                raise ValueError("worker 分配结果超出了 groups_per_worker 上限")
            assigned_image_count = sum(group["image_count"] for group in assigned_groups)
            worker_assignments.append(
                {
                    "worker_index": worker_index,
                    "group_count": len(assigned_groups),
                    "image_count": assigned_image_count,
                    "groups": assigned_groups,
                }
            )

        wave_index = (wave_offset // wave_capacity) + 1
        active_workers = sum(1 for assignment in worker_assignments if assignment["group_count"])
        waves.append(
            {
                "wave_index": wave_index,
                "group_count": len(wave_groups),
                "image_count": sum(group["image_count"] for group in wave_groups),
                "active_workers": active_workers,
                "worker_assignments": worker_assignments,
            }
        )

    return {
        "root": str(root.resolve()),
        "recursive": recursive,
        "supported_extensions": sorted(SUPPORTED_EXTENSIONS),
        "group_size": group_size,
        "workers": workers,
        "groups_per_worker": groups_per_worker,
        "wave_capacity": wave_capacity,
        "image_count": len(images),
        "group_count": len(groups),
        "wave_count": math.ceil(len(groups) / wave_capacity) if groups else 0,
        "waves": waves,
    }


def main() -> int:
    args = parse_args()
    root = Path(args.folder).expanduser()
    if not root.exists():
        raise SystemExit(f"未找到目录：{root}")
    if not root.is_dir():
        raise SystemExit(f"路径不是目录：{root}")

    manifest = build_manifest(
        root=root,
        group_size=args.group_size,
        workers=args.workers,
        groups_per_worker=args.groups_per_worker,
        recursive=not args.non_recursive,
    )

    output_text = json.dumps(manifest, ensure_ascii=False, indent=2)
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text + "\n", encoding="utf-8")
    else:
        print(output_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
