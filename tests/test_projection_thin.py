# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BANNED = (
    "cursor/skills/route-task/SKILL.md",
    "claude/skills/route-task/SKILL.md",
    "codex/skills/route-task/SKILL.md",
    "grok/skills/route-task/SKILL.md",
    "deepseek/skills/route-task/SKILL.md",
    ".cursor/skills/route-task/SKILL.md",
)


class ThinAdapterTests(unittest.TestCase):
    def test_no_five_full_copies(self) -> None:
        for rel in BANNED:
            self.assertFalse((ROOT / rel).is_file(), rel)

    def test_ssot_exists(self) -> None:
        self.assertTrue((ROOT / "skills" / "route-task" / "SKILL.md").is_file())
        self.assertGreaterEqual(len(list((ROOT / "agents").glob("*.md"))), 30)
        self.assertTrue((ROOT / "rules" / "全局.mdc").is_file())
        self.assertTrue((ROOT / "hooks" / "hooks.json").is_file())
        self.assertTrue((ROOT / "harness" / "scripts" / "刷新菜单.py").is_file())

    def test_cursor_adapter_is_pointer(self) -> None:
        adapter = json.loads((ROOT / ".cursor" / "adapter.json").read_text(encoding="utf-8"))
        self.assertEqual(adapter["runtime"], "full")
        self.assertEqual(adapter["source"]["skills"], "../skills")
        self.assertTrue((ROOT / ".cursor" / "hooks.json").is_file())
        self.assertFalse((ROOT / ".cursor" / "skills").is_dir())

    def test_other_adapters_are_instruction(self) -> None:
        claude = json.loads((ROOT / ".claude" / "adapter.json").read_text(encoding="utf-8"))
        self.assertEqual(claude["runtime"], "instruction")
        self.assertTrue((ROOT / "CLAUDE.md").is_file())
        self.assertTrue((ROOT / ".codex" / "AGENTS.md").is_file())
        self.assertTrue((ROOT / ".github" / "copilot-instructions.md").is_file())
