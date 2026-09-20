# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gsh.catalog import build_catalog


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = build_catalog(ROOT)

    def test_skill_count(self) -> None:
        ids = [x["id"] for x in self.catalog["skills"]]
        self.assertGreaterEqual(len(ids), 100)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("route-task", ids)
        self.assertIn("write-isolation", ids)
        self.assertIn("verify-gate", ids)

    def test_craft_count_and_paths(self) -> None:
        ids = [x["id"] for x in self.catalog["crafts"]]
        self.assertGreaterEqual(len(ids), 30)
        self.assertEqual(len(ids), len(set(ids)))
        pathed = [c for c in self.catalog["crafts"] if c.get("uses_skills")]
        self.assertTrue(pathed, "at least one craft must declare uses_skills")

    def test_mcp_stubs_are_honest(self) -> None:
        self.assertEqual(self.catalog["policy"]["live_servers_shipped"], 0)
        self.assertGreaterEqual(len(self.catalog["mcp"]), 30)
        ids = [x["id"] for x in self.catalog["mcp"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("excelMCP", ids)


if __name__ == "__main__":
    unittest.main()
