# -*- coding: utf-8 -*-
"""从菜单现查测试夹具，不写死项目职种或表名。"""
from __future__ import annotations


def first_craft_path(catalog: dict) -> tuple[str, list[str]]:
    for row in catalog.get("crafts") or []:
        uses = [str(x) for x in (row.get("uses_skills") or []) if str(x).strip()]
        if uses and row.get("id"):
            return str(row["id"]), uses
    return "", []


def first_skill_mcp(catalog: dict) -> tuple[str, str]:
    for row in catalog.get("skills") or []:
        needs = [str(x) for x in (row.get("needs_mcp") or []) if str(x).strip()]
        if needs and row.get("id"):
            return str(row["id"]), needs[0]
    return "", ""


def path_mcps(catalog: dict, uses: list[str]) -> list[str]:
    skills = {x["id"]: x for x in catalog.get("skills") or []}
    out: list[str] = []
    seen: set[str] = set()
    for sid in uses:
        for mid in skills.get(sid, {}).get("needs_mcp") or []:
            mid = str(mid).strip()
            if mid and mid not in seen:
                seen.add(mid)
                out.append(mid)
    return out
