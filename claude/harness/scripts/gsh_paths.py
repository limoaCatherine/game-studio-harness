# -*- coding: utf-8 -*-
"""解析 Game Studio Harness 的共享运行时与各工具家目录。"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Homes:
    gsh: Path
    cursor: Path
    claude: Path
    codex: Path
    grok: Path
    dsh: Path
    agents_skills: Path

    @property
    def gsh_skills(self) -> Path:
        return self.gsh / "skills"

    @property
    def gsh_agents(self) -> Path:
        return self.gsh / "agents"

    @property
    def gsh_harness(self) -> Path:
        return self.gsh / "harness"


def homes_from_env(isolate: Path | None = None) -> Homes:
    if isolate is not None:
        root = Path(isolate)
        return Homes(
            gsh=root / "gsh",
            cursor=root / "cursor",
            claude=root / "claude",
            codex=root / "codex",
            grok=root / "grok",
            dsh=root / "dsh",
            agents_skills=root / "agents" / "skills",
        )
    home = Path.home()
    return Homes(
        gsh=Path(os.environ.get("GSH_HOME") or (home / ".gsh")),
        cursor=Path(os.environ.get("CURSOR_HOME") or (home / ".cursor")),
        claude=Path(os.environ.get("CLAUDE_HOME") or (home / ".claude")),
        codex=Path(os.environ.get("CODEX_HOME") or (home / ".codex")),
        grok=Path(os.environ.get("GROK_HOME") or (home / ".grok")),
        dsh=Path(os.environ.get("DSH_HOME") or (home / ".dsh")),
        agents_skills=Path(os.environ.get("AGENTS_SKILLS") or (home / ".agents" / "skills")),
    )


def catalog_candidates(h: Homes) -> list[Path]:
    return [
        h.gsh_harness / "catalog.json",
        h.cursor / "harness" / "catalog.json",
    ]


def find_catalog(h: Homes | None = None) -> Path:
    homes = h or homes_from_env()
    for path in catalog_candidates(homes):
        if path.is_file():
            return path
    return homes.gsh_harness / "catalog.json"
