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
    ".claude/skills/route-task/SKILL.md",
    ".roo/skills/route-task/SKILL.md",
)

REPO_NATIVES = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "CONVENTIONS.md",
    "QWEN.md",
    ".windsurfrules",
    ".rules",
    ".clinerules/gsh.md",
    ".windsurf/rules/gsh.md",
    ".roo/rules/gsh.md",
    ".roomodes",
    ".continue/config.yaml",
    ".aider.conf.yml",
    ".amazonq/rules/gsh.md",
    ".trae/rules/gsh.md",
    ".junie/guidelines.md",
    ".kimi-code/AGENTS.md",
    ".qwen/QWEN.md",
    ".opencode/opencode.json",
    ".claude/settings.json",
    ".github/copilot-instructions.md",
    ".github/instructions/gsh.instructions.md",
    ".cursor/hooks.json",
    ".cursor/rules/全局.mdc",
)


class SsotAndNativeConventionTests(unittest.TestCase):
    def test_no_five_full_copies(self) -> None:
        for rel in BANNED:
            self.assertFalse((ROOT / rel).is_file(), rel)

    def test_ssot_exists(self) -> None:
        self.assertTrue((ROOT / "skills" / "route-task" / "SKILL.md").is_file())
        self.assertGreaterEqual(len(list((ROOT / "agents").glob("*.md"))), 30)
        self.assertTrue((ROOT / "rules" / "全局.mdc").is_file())
        self.assertTrue((ROOT / "hooks" / "hooks.json").is_file())
        self.assertTrue((ROOT / "harness" / "scripts" / "刷新菜单.py").is_file())

    def test_repo_natives_are_convention_files(self) -> None:
        for rel in REPO_NATIVES:
            self.assertTrue((ROOT / rel).is_file(), rel)
        self.assertFalse((ROOT / ".cursor" / "skills").is_dir())
        adapter = json.loads((ROOT / ".cursor" / "adapter.json").read_text(encoding="utf-8"))
        self.assertEqual(adapter["runtime"], "full")
        self.assertEqual(adapter["source"]["skills"], "../skills")
        claude = json.loads((ROOT / ".claude" / "adapter.json").read_text(encoding="utf-8"))
        self.assertTrue((ROOT / ".claude" / "settings.json").is_file())
        self.assertIn("settings.json", claude["notes"])
        settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertIn("SessionStart", settings["hooks"])
