# -*- coding: utf-8 -*-
"""职种路径：把 uses_skills 做成可前进的流水线，而不是一次性清单。"""
from __future__ import annotations

from typing import Any


def steps_for(catalog: dict, craft_id: str) -> list[str]:
    for row in catalog.get("crafts") or []:
        if row.get("id") == craft_id:
            return [str(x) for x in (row.get("uses_skills") or []) if str(x).strip()]
    return []


def path_row(steps: list[str], current: str | None = None, opened: list[str] | None = None) -> dict[str, Any]:
    if not steps:
        return {"steps": [], "index": 0, "current": None, "next": None, "opened": [], "done": True}
    cur = current if current in steps else steps[0]
    idx = steps.index(cur)
    seen = list(opened or [])
    if cur not in seen:
        seen.append(cur)
    nxt = steps[idx + 1] if idx + 1 < len(steps) else None
    return {
        "steps": steps,
        "index": idx,
        "current": cur,
        "next": nxt,
        "opened": seen,
        "done": nxt is None,
    }


def build_paths(catalog: dict, crafts: list[str], craft_open: dict) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for cid in crafts:
        steps = steps_for(catalog, cid)
        out[cid] = path_row(steps, craft_open.get(cid))
    return out


def advance(path: dict) -> dict:
    steps = list(path.get("steps") or [])
    if not steps:
        return path_row([])
    idx = int(path.get("index") or 0)
    if idx + 1 >= len(steps):
        row = path_row(steps, steps[-1], list(path.get("opened") or []))
        row["done"] = True
        row["next"] = None
        return row
    nxt = steps[idx + 1]
    opened = list(path.get("opened") or [])
    return path_row(steps, nxt, opened)


def render_progress(paths: dict) -> str:
    bits = []
    for cid, row in paths.items():
        steps = row.get("steps") or []
        if not steps:
            bits.append(f"{cid}: 无路径")
            continue
        n = int(row.get("index") or 0) + 1
        cur = row.get("current") or steps[0]
        nxt = row.get("next")
        tail = "完成" if row.get("done") else f"下一步 {nxt}"
        bits.append(f"{cid} {n}/{len(steps)} 当前 {cur} · {tail}")
    return "; ".join(bits) if bits else "无职种路径"
