# -*- coding: utf-8 -*-
"""按 install-state 撤投影。不删用户已有 mcp.json，不碰业务根正式面。"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from gsh.commands.setup import _homes
from gsh.project import read_install_state


KEEP_NAMES = {"mcp.json"}


def run(*, isolate: Path | None, dry: bool, yes: bool) -> int:
    h = _homes(isolate)
    state = read_install_state(h)
    if not state:
        print(f"no install-state at {h.state_file}", file=sys.stderr)
        return 2
    if not yes and not dry:
        print("uninstall will remove GSH projections under isolate/homes listed in install-state.")
        print("mcp.json is preserved. workspace official files are not touched.")
    roots = [
        h.gsh,
        h.cursor / "skills",
        h.cursor / "agents",
        h.cursor / "hooks",
        h.cursor / "rules",
        h.cursor / "harness",
        h.cursor / "hooks.json",
        h.cursor / "gsh-adapter.json",
        h.cursor / "mcp.json.example",
        h.claude,
        h.codex,
        h.grok,
        h.dsh,
        h.agents_skills,
        h.windsurf,
        h.cline,
        h.continue_dir / "AGENTS.md",
        h.continue_dir / "config.yaml.gsh-snippet",
        h.continue_dir / "gsh-adapter.json",
        h.copilot / "copilot-instructions.md",
        h.copilot / "gsh-adapter.json",
        h.opencode,
        h.gemini,
    ]
    removed = 0
    for path in roots:
        if path.name in KEEP_NAMES:
            continue
        if not path.exists():
            continue
        if dry:
            print("dry remove", path)
            removed += 1
            continue
        if path.is_file():
            path.unlink()
        else:
            shutil.rmtree(path)
        removed += 1
    if not dry and h.state_file.is_file():
        h.state_file.unlink()
    print(f"uninstalled entries={removed} dry={int(dry)}")
    print("ok uninstall")
    return 0
