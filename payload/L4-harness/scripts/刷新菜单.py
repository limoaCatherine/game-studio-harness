# -*- coding: utf-8 -*-
"""从用户级 skills / agents / mcp.json 生成菜单 catalog.json。"""
from __future__ import annotations

import json
import re
from pathlib import Path

CURSOR = Path.home() / ".cursor"
HARNESS = CURSOR / "harness"
SKILLS = CURSOR / "skills"
AGENTS = CURSOR / "agents"
MCP_JSON = CURSOR / "mcp.json"
TOOLS = HARNESS / "mcp-tools"
OUT = HARNESS / "catalog.json"

FM = re.compile(r"^---\s*\n(.*?)\n---", re.S)


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = FM.match(text)
    if not m:
        return {}
    data = {}
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


def collect_skills() -> list[dict]:
    rows = []
    if not SKILLS.is_dir():
        return rows
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        if ".bak" in skill_md.name:
            continue
        fm = frontmatter(skill_md)
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


TICK = re.compile(r"`([a-z][a-z0-9-]*)`")


def collect_uses_skills(text: str, skill_ids: set[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    declared = parse_list(frontmatter_from_text(text).get("uses_skills", ""))
    for sid in declared + TICK.findall(text):
        if sid in skill_ids and sid not in seen:
            seen.add(sid)
            out.append(sid)
    return out


def frontmatter_from_text(text: str) -> dict:
    m = FM.match(text)
    if not m:
        return {}
    data = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def collect_crafts(skill_ids: set[str]) -> list[dict]:
    rows = []
    if not AGENTS.is_dir():
        return rows
    for agent in sorted(AGENTS.glob("*.md")):
        if "bak" in agent.name.lower():
            continue
        text = agent.read_text(encoding="utf-8")
        fm = frontmatter_from_text(text)
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


def ensure_mcp_stub(mcp_id: str) -> bool:
    TOOLS.mkdir(parents=True, exist_ok=True)
    extra = TOOLS / f"{mcp_id}.json"
    if extra.is_file():
        return False
    extra.write_text(
        json.dumps({"id": mcp_id, "purpose": f"{mcp_id} 外接"}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return True


def collect_mcp() -> tuple[list[dict], int]:
    if not MCP_JSON.is_file():
        return [], 0
    raw = json.loads(MCP_JSON.read_text(encoding="utf-8"))
    servers = raw.get("mcpServers") or {}
    rows = []
    stubs = 0
    for k in servers:
        if ensure_mcp_stub(k):
            stubs += 1
        row = {"id": k, "name": k}
        extra = TOOLS / f"{k}.json"
        if extra.is_file():
            payload = json.loads(extra.read_text(encoding="utf-8"))
            if payload.get("purpose"):
                row["purpose"] = payload["purpose"]
            if payload.get("tools"):
                row["tools"] = payload["tools"]
        rows.append(row)
    return rows, stubs


def sources_mtime() -> float:
    times: list[float] = []
    if MCP_JSON.is_file():
        times.append(MCP_JSON.stat().st_mtime)
    if SKILLS.is_dir():
        times.extend(p.stat().st_mtime for p in SKILLS.glob("*/SKILL.md"))
    if AGENTS.is_dir():
        times.extend(p.stat().st_mtime for p in AGENTS.glob("*.md") if "bak" not in p.name.lower())
    return max(times) if times else 0.0


def catalog_stale() -> bool:
    if not OUT.is_file():
        return True
    return sources_mtime() > OUT.stat().st_mtime


def main() -> int:
    HARNESS.mkdir(parents=True, exist_ok=True)
    skills = collect_skills()
    skill_ids = {x["id"] for x in skills}
    crafts = collect_crafts(skill_ids)
    mcps, stubs = collect_mcp()
    catalog = {
        "version": 1,
        "source": {
            "skills": str(SKILLS),
            "agents": str(AGENTS),
            "mcp": str(MCP_JSON),
        },
        "skills": skills,
        "crafts": crafts,
        "mcp": mcps,
    }
    OUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    used = sum(1 for c in crafts if c.get("uses_skills"))
    print(f"wrote {OUT}")
    print(
        f"skills={len(skills)} crafts={len(crafts)} mcp={len(mcps)} "
        f"craft_paths={used} stubs+={stubs}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
