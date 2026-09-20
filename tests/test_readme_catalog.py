# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "install") not in sys.path:
    sys.path.insert(0, str(ROOT / "install"))

import verify_readme_catalog


class ReadmeCatalogTests(unittest.TestCase):
    def test_bilingual_readme_covers_every_craft_and_skill(self) -> None:
        self.assertEqual(verify_readme_catalog.main(), 0)


if __name__ == "__main__":
    unittest.main()
