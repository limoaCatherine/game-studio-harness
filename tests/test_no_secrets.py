# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

USER_PATH = re.compile(r"[A-Za-z]:\\Users\\(?!\$\{)[A-Za-z0-9._-]+")
DRIVE_HOST = re.compile(r"[A-Za-z]:\\Harness-Apps|[A-Za-z]:/Harness-Apps")
SECRET_A = re.compile(r'"-a",\s*"[A-Za-z0-9]{16,}"')
SECRET_LIKE = re.compile(r"\b(ghp_|github_pat_|sk-)[A-Za-z0-9_\-]{16,}")
SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules", "dist", "build", ".ruff_cache", ".pytest_cache", "pack_data", ".egg-info"}
SCAN_SUFFIX = {".md", ".json", ".py", ".mdc", ".example", ".yml", ".yaml", ".toml", ".txt", ".ps1", ".sh"}


class SecretScanTests(unittest.TestCase):
    def test_pack_has_no_secrets_or_studio_paths(self) -> None:
        hits: list[str] = []
        for path in ROOT.rglob("*"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIX:
                continue
            if path.name in {"catalog.json", "mcp.json"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if USER_PATH.search(text):
                hits.append(f"{path} user path")
            if DRIVE_HOST.search(text):
                hits.append(f"{path} host root")
            if SECRET_A.search(text) or SECRET_LIKE.search(text):
                hits.append(f"{path} secret-like")
        self.assertEqual(hits, [])

    def test_mcp_example_uses_placeholders(self) -> None:
        example = ROOT / "harness" / "mcp.json.example"
        self.assertTrue(example.is_file())
        text = example.read_text(encoding="utf-8")
        if "-a" in text:
            self.assertIn("${LARK_APP_ID}", text)
