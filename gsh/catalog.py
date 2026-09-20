# -*- coding: utf-8 -*-
"""从仓库根 skills/ agents/ 解析菜单（不依赖已安装家目录）。"""
from __future__ import annotations

import json
import re
from pathlib import Path

FM = re.compile(r"^---\s*\n(.*?)\n---", re.S)
TICK = re.compile(r"`([a-z][a-z0-9-]*)`")


def frontmatter(text: str) -> dict[str, str]:
    m = FM.match(text)
    if not m:
        return {}
    data: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def parse_list(raw: str) -> list[str]:
    v = (raw or "").strip()
    if not v:
        return []
    if v.startswith("[") and v.endswith("]"):
        return [x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()]
    return [v]


def iter_skills(skills_root: Path) -> list[dict]:
    rows: list[dict] = []
    if not skills_root.is_dir():
        return rows
    for skill_md in sorted(skills_root.glob("*/SKILL.md")):
        if ".bak" in skill_md.name:
            continue
        text = skill_md.read_text(encoding="utf-8")
        fm = frontmatter(text)
        sid = skill_md.parent.name
        display = fm.get("name") or sid
        row = {
            "id": sid,
            "name": display,
            "description": fm.get("description", ""),
            "path": str(skill_md),
        }
        if display != sid:
            row["alias"] = display
        needs = parse_list(fm.get("needs_mcp", ""))
        if needs:
            row["needs_mcp"] = needs
        rows.append(row)
    return rows


def collect_uses_skills(text: str, skill_ids: set[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    declared = parse_list(frontmatter(text).get("uses_skills", ""))
    for sid in declared + TICK.findall(text):
        if sid in skill_ids and sid not in seen:
            seen.add(sid)
            out.append(sid)
    return out


def iter_crafts(agents_root: Path, skill_ids: set[str]) -> list[dict]:
    rows: list[dict] = []
    if not agents_root.is_dir():
        return rows
    for agent in sorted(agents_root.glob("*.md")):
        if "bak" in agent.name.lower():
            continue
        text = agent.read_text(encoding="utf-8")
        fm = frontmatter(text)
        sid = agent.stem
        display = fm.get("name") or sid
        row = {
            "id": sid,
            "name": display,
            "description": fm.get("description", ""),
            "path": str(agent),
        }
        if display != sid:
            row["alias"] = display
        uses = collect_uses_skills(text, skill_ids)
        if uses:
            row["uses_skills"] = uses
        rows.append(row)
    return rows


def iter_mcp_stubs(tools_root: Path) -> list[dict]:
    rows: list[dict] = []
    if not tools_root.is_dir():
        return rows
    for path in sorted(tools_root.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        row = {"id": payload.get("id") or path.stem, "name": path.stem, "status": "stub"}
        if payload.get("purpose"):
            row["purpose"] = payload["purpose"]
        if payload.get("tools"):
            row["tools"] = payload["tools"]
        rows.append(row)
    return rows


def build_catalog(pack: Path) -> dict:
    skills = iter_skills(pack / "skills")
    skill_ids = {x["id"] for x in skills}
    crafts = iter_crafts(pack / "agents", skill_ids)
    mcps = iter_mcp_stubs(pack / "harness" / "mcp-tools")
    return {
        "version": 1,
        "source": {
            "skills": str(pack / "skills"),
            "agents": str(pack / "agents"),
            "mcp": str(pack / "harness" / "mcp-tools"),
        },
        "skills": skills,
        "crafts": crafts,
        "mcp": mcps,
        "policy": {
            "mcp": "stubs-and-placeholders",
            "live_servers_shipped": 0,
            "note": "mcp-tools/*.json 是用途桩；mcp.json.example 是占位启动模板。本仓不配送可连的 MCP 进程。",
        },
    }
