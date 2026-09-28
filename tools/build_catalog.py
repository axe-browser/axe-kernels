#!/usr/bin/env python3
"""Build a download catalog from release metadata without uploading assets."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile
from urllib.parse import quote


METADATA_MAX_BYTES = 1024 * 1024
GITHUB_ASSET_LIMIT_BYTES = 2 * 1024 ** 3
MAX_UNPACKED_BYTES = 8 * 1024 ** 3
MAX_CATALOG_ENTRIES = 256
LAUNCH_PROTOCOL = "axe-chromium-features-v1"
VERSION = re.compile(r"([1-9][0-9]{0,3})\.[0-9]+\.[0-9]+\.[0-9]+")
SHA256 = re.compile(r"[a-fA-F0-9]{64}")
OWNER = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?")
REPOSITORY = re.compile(r"[A-Za-z0-9._-]{1,100}")
RELEASE_TAG = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")


def repository_parts(value: str) -> tuple[str, str]:
    if not isinstance(value, str) or value.count("/") != 1:
        raise ValueError("仓库必须使用 OWNER/REPO 格式。")
    owner, repository = value.split("/")
    if (not OWNER.fullmatch(owner) or not REPOSITORY.fullmatch(repository)
            or repository in {".", ".."}):
        raise ValueError("GitHub 仓库名称无效。")
    return owner, repository


def release_tag(value: object) -> str:
    if (not isinstance(value, str) or not RELEASE_TAG.fullmatch(value)
            or ".." in value or value.endswith((".", ".lock"))):
        raise ValueError("Release tag 必须为 1–128 字符的字母、数字、点、下划线或连字符，且为有效固定 tag。")
    return value


def _archive_name(value: object) -> str:
    if (not isinstance(value, str) or len(value.encode("utf-8")) > 255
            or not value.endswith(".tar.gz") or value == ".tar.gz"
            or "/" in value or "\\" in value
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        raise ValueError("归档必须是无目录路径的 .tar.gz 文件名。")
    return value


def _executable(value: object) -> None:
    if (not isinstance(value, str) or not value or len(value) > 4096
            or "\\" in value or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        raise ValueError("内核元数据缺少有效的包内入口。")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() == ".":
        raise ValueError("内核入口必须是包内相对路径。")


def catalog_entry(metadata: object, repository: tuple[str, str]) -> dict[str, object]:
    if (not isinstance(metadata, dict) or type(metadata.get("schema_version")) is not int
            or metadata["schema_version"] != 1 or metadata.get("format") != "tar.gz"):
        raise ValueError("归档元数据格式无效，要求 schema_version: 1 和 tar.gz。")
    archive = _archive_name(metadata.get("archive"))
    tag = release_tag(metadata.get("release_tag"))
    status = metadata.get("status")
    if not isinstance(status, str) or status not in {"published", "not_published"}:
        raise ValueError("发布状态必须是 published 或 not_published。")
    kernel = metadata.get("kernel")
    if not isinstance(kernel, dict):
        raise ValueError("归档缺少完整内核身份信息。")
    version = kernel.get("version")
    match = VERSION.fullmatch(version) if isinstance(version, str) and len(version) <= 80 else None
    if (not match or type(kernel.get("schema_version")) is not int or kernel["schema_version"] != 1
            or kernel.get("id") != "chromium-" + match[1]
            or (kernel.get("platform"), kernel.get("architecture"), kernel.get("launch_protocol"))
            != ("mac", "arm64", LAUNCH_PROTOCOL)):
        raise ValueError("内核版本、身份、平台或启动协议无效；仅支持 mac-arm64 新协议。")
    _executable(kernel.get("executable"))
    checksum = metadata.get("sha256")
    if not isinstance(checksum, str) or not SHA256.fullmatch(checksum):
        raise ValueError("归档必须提供有效的 SHA-256。")
    size, unpacked = metadata.get("size_bytes"), metadata.get("unpacked_size_bytes")
    if type(size) is not int or not 0 < size < GITHUB_ASSET_LIMIT_BYTES:
        raise ValueError("GitHub Release 归档大小必须大于 0 且小于 2 GiB。")
    if type(unpacked) is not int or not 0 < unpacked <= MAX_UNPACKED_BYTES:
        raise ValueError("内核解包大小必须大于 0 且不超过 8 GiB。")
    entry = {field: kernel[field] for field in ("id", "version", "platform", "architecture", "launch_protocol")}
    entry.update(status=status, download_url="", sha256="", size_bytes=0, unpacked_size_bytes=0)
    if status == "published":
        owner, name = repository
        segments = [owner, name, "releases", "download", tag, archive]
        entry.update(download_url="https://github.com/" + "/".join(quote(segment, safe="") for segment in segments),
                     sha256=checksum.lower(), size_bytes=size, unpacked_size_bytes=unpacked)
    return entry


def read_release(path: Path) -> object:
    with path.expanduser().open("rb") as stream:
        raw = stream.read(METADATA_MAX_BYTES + 1)
    if len(raw) > METADATA_MAX_BYTES:
        raise ValueError(f"发布元数据超过 1 MiB：{path.name}")
    return json.loads(raw)


def build_catalog(repo: str, releases: list[Path], output: Path) -> Path:
    repository = repository_parts(repo)
    if not releases or len(releases) > MAX_CATALOG_ENTRIES:
        raise ValueError("请选择 1–256 份发布元数据。")
    entries = [catalog_entry(read_release(path), repository) for path in releases]
    if len({entry["id"] for entry in entries}) != len(entries):
        raise ValueError("每个 Chromium 主版本只能提供一个当前条目。")
    entries.sort(key=lambda item: tuple(int(part) for part in str(item["version"]).split(".")), reverse=True)
    output = output.expanduser().absolute()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".catalog_", dir=output.parent) as folder:
        staged = Path(folder) / "catalog.json"
        staged.write_text(json.dumps({"schema_version": 1, "kernels": entries}, indent=2) + "\n", encoding="utf-8")
        os.link(staged, output)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="GitHub 仓库，例如 OWNER/axe-kernels")
    parser.add_argument("--release", type=Path, action="append", required=True, help="带 release_tag/status 的归档元数据，可重复")
    parser.add_argument("--output", type=Path, required=True, help="新建目录 JSON，不覆盖已有文件")
    args = parser.parse_args(argv)
    try:
        print(build_catalog(args.repo, args.release, args.output))
        return 0
    except (OSError, ValueError, TypeError, RecursionError) as exc:
        parser.exit(1, f"生成内核目录失败：{exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
