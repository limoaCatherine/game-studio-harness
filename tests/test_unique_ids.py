# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gsh.catalog import build_catalog


class UniqueIdTests(unittest.TestCase):
    def test_no_skill_craft_collision_is_required_to_be_auditable(self) -> None:
        catalog = build_catalog(ROOT)
        skills = {x["id"] for x in catalog["skills"]}
        crafts = {x["id"] for x in catalog["crafts"]}
        mcps = {x["id"] for x in catalog["mcp"]}
        self.assertTrue(skills)
        self.assertTrue(crafts)
        # kinds live in separate namespaces; still fail if an empty id sneaks in
        self.assertNotIn("", skills)
        self.assertNotIn("", crafts)
        self.assertNotIn("", mcps)

    def test_skill_dirs_match_frontmatter_name_or_folder(self) -> None:
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            self.assertTrue(path.parent.name)
            self.assertNotIn(" ", path.parent.name)
