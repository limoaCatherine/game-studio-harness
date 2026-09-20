# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gsh.cli import main


class IsolateCliTests(unittest.TestCase):
    def test_setup_verify_sync_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            isolate = Path(tmp) / "probe"
            workspace = Path(tmp) / "ws"
            rc = main(
                [
                    "setup",
                    "--isolate-root",
                    str(isolate),
                    "--workspace",
                    str(workspace),
                    "--tools",
                    "legacy",
                    "--profile",
                    "full",
                    "--yes",
                ]
            )
            self.assertEqual(rc, 0, "setup failed")
            rc = main(
                [
                    "verify",
                    "--isolate-root",
                    str(isolate),
                    "--workspace",
                    str(workspace),
                    "--tools",
                    "legacy",
                ]
            )
            self.assertEqual(rc, 0, "verify failed")
            skill = isolate / "gsh" / "skills" / "route-task" / "SKILL.md"
            self.assertTrue(skill.is_file())
            cursor_skill = isolate / "cursor" / "skills" / "route-task" / "SKILL.md"
            self.assertEqual(skill.read_bytes(), cursor_skill.read_bytes())
            claude_skill = isolate / "claude" / "skills" / "route-task" / "SKILL.md"
            self.assertEqual(skill.read_bytes(), claude_skill.read_bytes())

            original = skill.read_text(encoding="utf-8")
            skill.write_text(original + "\n# isolate-sync-marker\n", encoding="utf-8")
            # Edit the pack SSOT, then sync — adapters must follow the pack, not the isolate edit.
            pack_skill = ROOT / "skills" / "route-task" / "SKILL.md"
            pack_original = pack_skill.read_text(encoding="utf-8")
            try:
                pack_skill.write_text(pack_original + "\n# pack-sync-marker\n", encoding="utf-8")
                rc = main(
                    [
                        "sync",
                        "--isolate-root",
                        str(isolate),
                        "--workspace",
                        str(workspace),
                        "--tools",
                        "legacy",
                        "--profile",
                        "full",
                    ]
                )
                self.assertEqual(rc, 0, "sync failed")
                self.assertIn("pack-sync-marker", cursor_skill.read_text(encoding="utf-8"))
                self.assertIn("pack-sync-marker", claude_skill.read_text(encoding="utf-8"))
            finally:
                pack_skill.write_text(pack_original, encoding="utf-8")

            catalog = json.loads((isolate / "gsh" / "harness" / "catalog.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(catalog.get("skills") or []), 100)
            self.assertTrue((workspace / ".harness" / "surfaces.json").is_file())
            self.assertTrue((isolate / "gsh" / "install-state.json").is_file())
