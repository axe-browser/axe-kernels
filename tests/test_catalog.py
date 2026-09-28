"""Release catalogs preserve publication state and independent asset tags."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tools.build_catalog import GITHUB_ASSET_LIMIT_BYTES, METADATA_MAX_BYTES, build_catalog


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.output = self.root / "output/catalog.json"
        self.metadata = {
            "schema_version": 1, "archive": "AxeChromium 154 mac-arm64.tar.gz", "format": "tar.gz",
            "sha256": "A" * 64, "size_bytes": 1234, "unpacked_size_bytes": 5678,
            "kernel": {"schema_version": 1, "id": "chromium-154", "version": "154.0.8037.17",
                       "platform": "mac", "architecture": "arm64", "launch_protocol": "axe-chromium-features-v1",
                       "executable": "Chromium.app/Contents/MacOS/Chromium"},
            "release_tag": "chromium-154.0.8037.17-r7-mac-arm64", "status": "published",
        }

    def manifest(self, metadata=None, name="release.json"):
        path = self.root / name
        path.write_text(json.dumps(self.metadata if metadata is None else metadata), encoding="utf-8")
        return path

    def read_catalog(self, *paths):
        build_catalog("test-owner/axe-kernels", list(paths), self.output)
        return json.loads(self.output.read_text())

    def test_versions_use_their_own_fixed_release_tags(self):
        older = deepcopy(self.metadata)
        older.update(archive="AxeChromium-153.tar.gz", release_tag="chromium-153.0.8001.2-r3-mac-arm64")
        older["kernel"].update(id="chromium-153", version="153.0.8001.2")
        catalog = self.read_catalog(self.manifest(older, "153.json"), self.manifest())
        self.assertEqual(catalog["schema_version"], 1)
        newest, previous = catalog["kernels"]
        self.assertEqual(newest["id"], "chromium-154")
        self.assertEqual(newest["download_url"],
                         "https://github.com/test-owner/axe-kernels/releases/download/"
                         "chromium-154.0.8037.17-r7-mac-arm64/AxeChromium%20154%20mac-arm64.tar.gz")
        self.assertEqual(previous["download_url"],
                         "https://github.com/test-owner/axe-kernels/releases/download/"
                         "chromium-153.0.8001.2-r3-mac-arm64/AxeChromium-153.tar.gz")
        self.assertEqual(newest["sha256"], "a" * 64)
        self.assertEqual(newest["size_bytes"], 1234)
        self.assertEqual(newest["unpacked_size_bytes"], 5678)

    def test_candidate_does_not_expose_download_fields(self):
        self.metadata["status"] = "not_published"
        entry = self.read_catalog(self.manifest())["kernels"][0]
        self.assertEqual(entry["status"], "not_published")
        self.assertEqual(entry["version"], "154.0.8037.17")
        self.assertEqual(entry["download_url"], "")
        self.assertEqual(entry["sha256"], "")
        self.assertEqual((entry["size_bytes"], entry["unpacked_size_bytes"]), (0, 0))

    def test_archive_filename_is_encoded_as_one_url_segment(self):
        self.metadata["archive"] = "AxeChromium#154?build=2%.tar.gz"
        entry = self.read_catalog(self.manifest())["kernels"][0]
        self.assertTrue(entry["download_url"].endswith("/AxeChromium%23154%3Fbuild%3D2%25.tar.gz"))

    def test_invalid_repository_and_tag_are_rejected(self):
        manifest = self.manifest()
        for repository in ("owner", "https://github.com/owner/axe-kernels", "owner/../axe-kernels",
                           "owner/..", "-owner/axe-kernels", "owner/axe-kernels?token=x", "owner /axe-kernels"):
            with self.subTest(repository=repository), self.assertRaises(ValueError):
                build_catalog(repository, [manifest], self.output)
        for tag in ("", "latest/tag", "../tag", "v154..r1", "v154.", "v154.lock", "tag?secret", "tag\n", "a" * 129):
            with self.subTest(tag=tag):
                self.metadata["release_tag"] = tag
                with self.assertRaises(ValueError):
                    self.read_catalog(self.manifest())
        self.assertFalse(self.output.exists())

    def test_invalid_metadata_and_platform_are_rejected(self):
        mutations = [
            ("schema_version", True), ("format", "zip"), ("status", "ready"), ("status", []),
            ("archive", "../kernel.tar.gz"), ("archive", "kernel\\package.tar.gz"),
            ("archive", "kernel.tar.gz\n"), ("archive", "kernel.zip"),
            ("sha256", "0" * 63), ("sha256", "g" * 64),
            ("size_bytes", True), ("size_bytes", 0), ("size_bytes", GITHUB_ASSET_LIMIT_BYTES),
            ("unpacked_size_bytes", -1), ("unpacked_size_bytes", 8 * 1024 ** 3 + 1),
        ]
        for field, value in mutations:
            with self.subTest(field=field, value=value):
                changed = deepcopy(self.metadata)
                changed[field] = value
                with self.assertRaises(ValueError):
                    self.read_catalog(self.manifest(changed))
        for field, value in (("schema_version", True), ("id", "chromium-153"), ("version", "154.0"),
                             ("platform", "linux"), ("architecture", "x64"),
                             ("launch_protocol", "unsupported-features-v1"),
                             ("executable", "../Chromium"), ("executable", "/Chromium")):
            with self.subTest(kernel_field=field):
                changed = deepcopy(self.metadata)
                changed["kernel"][field] = value
                with self.assertRaises(ValueError):
                    self.read_catalog(self.manifest(changed))
        self.assertFalse(self.output.exists())

    def test_candidate_metadata_is_still_checked(self):
        self.metadata.update(status="not_published", sha256="invalid")
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            self.read_catalog(self.manifest())

    def test_same_major_version_cannot_be_published_twice(self):
        other = deepcopy(self.metadata)
        other["kernel"]["version"] = "154.0.8037.18"
        other["status"] = "not_published"
        with self.assertRaisesRegex(ValueError, "每个 Chromium 主版本"):
            self.read_catalog(self.manifest(), self.manifest(other, "other.json"))

    def test_existing_catalog_and_symlink_are_never_overwritten(self):
        manifest = self.manifest()
        self.output.parent.mkdir()
        self.output.write_text("existing", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            self.read_catalog(manifest)
        self.assertEqual(self.output.read_text(), "existing")
        self.output.unlink()
        target = self.root / "target.json"
        target.write_text("preserved", encoding="utf-8")
        self.output.symlink_to(target)
        with self.assertRaises(FileExistsError):
            self.read_catalog(manifest)
        self.assertTrue(self.output.is_symlink())
        self.assertEqual(target.read_text(), "preserved")
        self.assertEqual(list(self.output.parent.glob(".axe-catalog-*")), [])

    def test_oversized_malformed_or_missing_metadata_cannot_create_catalog(self):
        path = self.root / "input.json"
        path.write_bytes(b" " * (METADATA_MAX_BYTES + 1))
        with self.assertRaisesRegex(ValueError, "1 MiB"):
            self.read_catalog(path)
        path.write_text("not JSON", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.read_catalog(path)
        path.unlink()
        with self.assertRaises(FileNotFoundError):
            self.read_catalog(path)
        self.assertFalse(self.output.exists())

    def test_empty_release_list_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "1–256"):
            self.read_catalog()


if __name__ == "__main__":
    unittest.main()
