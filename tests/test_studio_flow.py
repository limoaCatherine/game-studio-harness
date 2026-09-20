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


class StudioFlowTests(unittest.TestCase):
    def test_menu_status_next_close(self) -> None:
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
                    "cursor",
                    "--profile",
                    "full",
                    "--yes",
                ]
            )
            self.assertEqual(rc, 0)
            rc = main(["menu", "--kind", "craft", "-q", "战斗数值", "--pack-root", str(ROOT)])
            self.assertEqual(rc, 0)

            sess = workspace / ".harness" / "sessions" / "combat-ttk"
            sess.mkdir(parents=True, exist_ok=True)
            (sess / "loadplan.json").write_text(
                json.dumps(
                    {
                        "session_id": "combat-ttk",
                        "bead_id": "bead-ttk",
                        "tier": "T1",
                        "verify_kind": "schema",
                        "intent": "new",
                        "work_mode": "agent",
                        "write_class": "sandbox",
                        "items": [
                            {
                                "kind": "craft",
                                "id": "combat-numeric-designer",
                                "why": "本轮只定 TTK 锚点与公式顺序。",
                            }
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            rc = main(
                [
                    "activate",
                    "combat-ttk",
                    "--workspace",
                    str(workspace),
                    "--pack-root",
                    str(ROOT),
                    "--isolate-root",
                    str(isolate),
                ]
            )
            self.assertEqual(rc, 0, "activate failed")
            activated = json.loads((sess / "activated.json").read_text(encoding="utf-8"))
            self.assertIn("combat-numeric-designer", activated.get("crafts") or [])
            first = activated["craft_open"]["combat-numeric-designer"]
            self.assertTrue(first)
            self.assertNotEqual(set(activated.get("skills") or []), set(activated["craft_path"]["combat-numeric-designer"]["steps"]))
            self.assertTrue((sess / "current.md").is_file())

            rc = main(["status", "--workspace", str(workspace), "--pack-root", str(ROOT)])
            self.assertEqual(rc, 0)
            rc = main(["resume", "--workspace", str(workspace), "--pack-root", str(ROOT)])
            self.assertEqual(rc, 0)
            rc = main(
                [
                    "next",
                    "--workspace",
                    str(workspace),
                    "--pack-root",
                    str(ROOT),
                    "--craft",
                    "combat-numeric-designer",
                ]
            )
            self.assertEqual(rc, 0)
            moved = json.loads((sess / "activated.json").read_text(encoding="utf-8"))
            self.assertNotEqual(moved["craft_open"]["combat-numeric-designer"], first)
            self.assertGreater(moved["craft_path"]["combat-numeric-designer"]["index"], 0)

            evidence = workspace / ".harness" / "sandbox" / "ttk.md"
            evidence.parent.mkdir(parents=True, exist_ok=True)
            evidence.write_text("TTK 锚点草稿\n", encoding="utf-8")
            rc = main(
                [
                    "close",
                    "--workspace",
                    str(workspace),
                    "--pack-root",
                    str(ROOT),
                    "--kind",
                    "schema",
                    "--evidence",
                    str(evidence),
                    "--notes",
                    "sandbox ttk card exists",
                ]
            )
            self.assertEqual(rc, 0)
            report = json.loads(
                (workspace / ".harness" / "artifacts" / "bead-ttk" / "verify-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(report["verdict"], "pass")
            self.assertEqual(report["verify_kind"], "schema")
            self.assertEqual(report["bead_id"], "bead-ttk")
