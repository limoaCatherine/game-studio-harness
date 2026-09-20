# -*- coding: utf-8 -*-
"""解析 Game Studio Harness 的共享运行时、各工具家目录与包根。"""
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
    windsurf: Path
    copilot: Path
    continue_dir: Path
    opencode: Path
    gemini: Path
    cline: Path

    @property
    def gsh_skills(self) -> Path:
        return self.gsh / "skills"

    @property
    def gsh_agents(self) -> Path:
        return self.gsh / "agents"

    @property
    def gsh_harness(self) -> Path:
        return self.gsh / "harness"

    @property
    def gsh_rules(self) -> Path:
        return self.gsh / "rules"

    @property
    def gsh_hooks(self) -> Path:
        return self.gsh / "hooks"

    @property
    def state_file(self) -> Path:
        return self.gsh / "install-state.json"


def isolate_root_from_env(explicit: Path | None = None) -> Path | None:
    if explicit is not None:
        return Path(explicit)
    raw = (os.environ.get("GSH_ISOLATE_ROOT") or "").strip()
    return Path(raw) if raw else None


def homes_from_env(isolate: Path | None = None) -> Homes:
    root = isolate_root_from_env(isolate)
    if root is not None:
        return Homes(
            gsh=root / "gsh",
            cursor=root / "cursor",
            claude=root / "claude",
            codex=root / "codex",
            grok=root / "grok",
            dsh=root / "dsh",
            agents_skills=root / "agents" / "skills",
            windsurf=root / "windsurf",
            copilot=root / "copilot",
            continue_dir=root / "continue",
            opencode=root / "opencode",
            gemini=root / "gemini",
            cline=root / "cline",
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
        windsurf=Path(os.environ.get("WINDSURF_HOME") or (home / ".codeium" / "windsurf")),
        copilot=Path(os.environ.get("COPILOT_HOME") or (home / ".github")),
        continue_dir=Path(os.environ.get("CONTINUE_HOME") or (home / ".continue")),
        opencode=Path(os.environ.get("OPENCODE_HOME") or (home / ".opencode")),
        gemini=Path(os.environ.get("GEMINI_HOME") or (home / ".gemini")),
        cline=Path(os.environ.get("CLINE_HOME") or (home / ".cline")),
    )


def homes_near(start: Path) -> Homes:
    """从钩子/脚本文件位置推断：隔离根（含 gsh/ + cursor/）优先，否则走环境。"""
    cur = Path(start).resolve()
    if cur.is_file():
        cur = cur.parent
    for p in [cur, *cur.parents]:
        if (p / "gsh" / "harness" / "scripts").is_dir() and (p / "cursor").is_dir():
            return homes_from_env(p)
        if p.name == "hooks" and (p.parent / "harness").is_dir():
            isolate = p.parent.parent
            if (isolate / "gsh").is_dir():
                return homes_from_env(isolate)
    return homes_from_env()


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


def find_pack_root(start: Path | None = None) -> Path:
    """仓库根：同时具备 skills/、agents/、harness/、rules/。"""
    env = (os.environ.get("GSH_PACK_ROOT") or "").strip()
    if env:
        return Path(env).resolve()
    cur = (start or Path(__file__)).resolve()
    if cur.is_file():
        cur = cur.parent
    for p in [cur, *cur.parents]:
        if (
            (p / "skills" / "route-task" / "SKILL.md").is_file()
            and (p / "agents").is_dir()
            and (p / "harness" / "scripts").is_dir()
            and (p / "rules").is_dir()
        ):
            return p
    return Path(__file__).resolve().parents[2]


def harness_scripts(h: Homes | None = None) -> Path:
    homes = h or homes_from_env()
    for cand in (homes.gsh_harness / "scripts", homes.cursor / "harness" / "scripts"):
        if (cand / "刷新菜单.py").is_file():
            return cand
    return homes.gsh_harness / "scripts"
