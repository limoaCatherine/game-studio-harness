# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gsh import __version__
from gsh.paths_cli import bundled_pack, is_pack_root, resolve_pack, studio_scaffold


class PackagingTests(unittest.TestCase):
    def test_version_is_semver(self) -> None:
        parts = __version__.split(".")
        self.assertEqual(len(parts), 3)
        self.assertTrue(all(p.isdigit() for p in parts))

    def test_pyproject_does_not_hardcode_version(self) -> None:
        text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn("dynamic = [\"version\"]", text)
        self.assertNotIn("\nversion = ", text.split("[tool.hatch.version]", 1)[0])
        self.assertIn('gsh = "gsh.cli:main"', text)
        self.assertIn('requires-python = ">=3.11"', text)
        self.assertIn("hatchling", text)

    def test_readme_version_badge_matches(self) -> None:
        needle = f"version-{__version__}"
        for name in ("README.md", "README.en.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn(needle, text, name)
            self.assertIn("img.shields.io", text)
            self.assertNotIn("assets/", text)

    def test_resolve_pack_finds_checkout_ssot(self) -> None:
        pack = resolve_pack()
        self.assertTrue(is_pack_root(pack))
        self.assertTrue((pack / "agents").is_dir())
        self.assertTrue((pack / "rules" / "全局.mdc").is_file())
        self.assertTrue((pack / "hooks" / "hooks.json").is_file())

    def test_explicit_and_env_pack_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "pack"
            (fake / "skills" / "route-task").mkdir(parents=True)
            (fake / "harness" / "scripts").mkdir(parents=True)
            (fake / "skills" / "route-task" / "SKILL.md").write_text("# t\n", encoding="utf-8")
            self.assertEqual(resolve_pack(fake), fake.resolve())
            self.assertTrue(is_pack_root(fake))

    def test_studio_scaffold_in_checkout(self) -> None:
        path = studio_scaffold(ROOT)
        self.assertTrue((path / "surfaces.json").is_file())
        self.assertTrue((path / "templates" / "verify-report.json").is_file())

    def test_bundled_pack_absent_in_checkout(self) -> None:
        self.assertIsNone(bundled_pack())
        self.assertFalse((ROOT / "gsh" / "pack_data").exists())
