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

from gsh.catalog import build_catalog


class CraftNoPreexpandTests(unittest.TestCase):
    def test_generator_opens_first_skill_only(self) -> None:
        catalog = build_catalog(ROOT)
        craft = next(c for c in catalog["crafts"] if len(c.get("uses_skills") or []) >= 2)
        uses = list(craft["uses_skills"])
        sys.path.insert(0, str(ROOT / "harness" / "scripts"))
        from 生成会话能力名单 import main as gen_main  # type: ignore

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sid = "_craft-preexpand"
            sess = root / ".harness" / "sessions" / sid
            sess.mkdir(parents=True)
            (sess / "loadplan.json").write_text(
                json.dumps(
                    {
                        "session_id": sid,
                        "tier": "T1",
                        "verify_kind": "none",
                        "intent": "new",
                        "work_mode": "agent",
                        "items": [
                            {
                                "kind": "craft",
                                "id": craft["id"],
                                "why": "职种不预展开路径的夹具测试。",
                            }
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            # Point the generator at an in-memory catalog file
            cat_path = root / "catalog.json"
            cat_path.write_text(json.dumps(catalog, ensure_ascii=False), encoding="utf-8")
            import 生成会话能力名单 as gen  # type: ignore

            gen.CATALOG = cat_path
            old = Path.cwd()
            try:
                import os

                os.chdir(root)
                rc = gen_main(["生成会话能力名单.py", sid])
            finally:
                os.chdir(old)
            self.assertEqual(rc, 0)
            activated = json.loads((sess / "activated.json").read_text(encoding="utf-8"))
            self.assertTrue(activated.get("ok"))
            self.assertEqual(activated.get("crafts"), [craft["id"]])
            opened = (activated.get("craft_open") or {}).get(craft["id"])
            self.assertEqual(opened, uses[0])
            named_skills = set(activated.get("skills") or [])
            self.assertFalse(set(uses).issubset(named_skills), "craft path was pre-expanded into skills")
            self.assertTrue((sess / "current.md").is_file())
