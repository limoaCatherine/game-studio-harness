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

from gsh.adapters import SPECS, home_for
from gsh.cli import main
from gsh.profiles import ALL_TOOLS


class NativeHomeTests(unittest.TestCase):
    def test_all_tool_ids_are_specified(self) -> None:
        self.assertEqual(set(ALL_TOOLS), {s.id for s in SPECS})

    def test_setup_all_lands_full_native_trees(self) -> None:
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
                    "all",
                    "--profile",
                    "minimal",
                    "--yes",
                ]
            )
            self.assertEqual(rc, 0, "setup all/minimal failed")
            rc = main(
                [
                    "verify",
                    "--isolate-root",
                    str(isolate),
                    "--workspace",
                    str(workspace),
                    "--tools",
                    "all",
                ]
            )
            self.assertEqual(rc, 0, "verify all/minimal failed")

            sys.path.insert(0, str(ROOT / "harness" / "scripts"))
            from gsh_paths import homes_from_env  # type: ignore

            h = homes_from_env(isolate)
            for spec in SPECS:
                dest = home_for(h, spec)
                cap = json.loads((dest / "gsh-capability.json").read_text(encoding="utf-8"))
                self.assertEqual(cap["tool"], spec.id)
                self.assertEqual(cap["hooks"], spec.hooks)
                skill_rel = spec.skill_dirs[0]
                self.assertTrue(
                    (dest / skill_rel / "route-task" / "SKILL.md").is_file(),
                    f"{spec.id} missing projected route-task",
                )
                for entry in spec.entries:
                    self.assertTrue((dest / entry).is_file(), f"{spec.id} missing {entry}")
                if spec.hooks == "cursor":
                    self.assertTrue((dest / "hooks.json").is_file())
                elif spec.hooks == "claude":
                    self.assertTrue((dest / "settings.json").is_file())
                    self.assertTrue((dest / "hooks" / "开场.py").is_file())
                    self.assertTrue((dest / "HOOKS.md").is_file())
                else:
                    self.assertTrue((dest / "HOOKS.md").is_file(), f"{spec.id} missing HOOKS.md")
            self.assertTrue((workspace / ".claude" / "settings.json").is_file())
            self.assertTrue((workspace / ".roo" / "rules" / "gsh.md").is_file())
            self.assertTrue((workspace / ".junie" / "guidelines.md").is_file())
