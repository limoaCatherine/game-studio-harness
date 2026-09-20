# -*- coding: utf-8 -*-
from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gsh.cli import main


class LegacyConsoleEncodingTests(unittest.TestCase):
    def test_menu_prints_chinese_on_cp1252_stdout(self) -> None:
        """Windows CI defaults to cp1252; menu descriptions are Chinese."""
        raw_out = io.BytesIO()
        raw_err = io.BytesIO()
        out = io.TextIOWrapper(raw_out, encoding="cp1252", errors="strict", newline="\n")
        err = io.TextIOWrapper(raw_err, encoding="cp1252", errors="strict", newline="\n")
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout = out
            sys.stderr = err
            rc = main(["menu", "--kind", "craft", "-q", "战斗数值", "--pack-root", str(ROOT)])
            out.flush()
            err.flush()
        finally:
            sys.stdout = old_out
            sys.stderr = old_err
        self.assertEqual(rc, 0)
        text = raw_out.getvalue().decode("utf-8")
        self.assertIn("director menu", text)
        self.assertIn("combat-numeric-designer", text)
