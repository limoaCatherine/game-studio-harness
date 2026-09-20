# -*- coding: utf-8 -*-
"""第四层项目库：当前行、任务流水、现行卡。"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

TZ = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def harness_dir(root: Path) -> Path:
    return Path(root) / ".harness"


def state_path(root: Path) -> Path:
    return harness_dir(root) / "state.json"


def tasks_path(root: Path) -> Path:
    return harness_dir(root) / "memory" / "tasks.jsonl"


def surfaces_path(root: Path) -> Path:
    return harness_dir(root) / "surfaces.json"


def current_card_path(root: Path, session_id: str) -> Path:
    return harness_dir(root) / "sessions" / session_id / "current.md"


def read_state(root: Path | None) -> dict:
    if root is None:
        return {}
    path = state_path(root)
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def write_state(root: Path, patch: dict) -> Path:
    cur = read_state(root)
    if not isinstance(cur.get("sessions"), dict) and cur.get("session_id"):
        cur["sessions"] = {
            str(cur["session_id"]): {
                "bead_id": cur.get("bead_id"),
                "progress": cur.get("progress"),
                "status": cur.get("status"),
                "updated_at": cur.get("updated_at"),
            }
        }
    sid = patch.get("session_id")
    for key, value in patch.items():
        if value is not None and key != "sessions":
            cur[key] = value
    if sid:
        rows = cur.get("sessions") if isinstance(cur.get("sessions"), dict) else {}
        prev = rows.get(sid) if isinstance(rows.get(sid), dict) else {}
        rows[str(sid)] = {
            "bead_id": patch.get("bead_id") if patch.get("bead_id") is not None else prev.get("bead_id"),
            "progress": patch.get("progress") if patch.get("progress") is not None else prev.get("progress"),
            "status": patch.get("status") if patch.get("status") is not None else prev.get("status"),
            "updated_at": now_iso(),
        }
        cur["sessions"] = rows
    cur["updated_at"] = now_iso()
    dest = state_path(root)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(cur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest


def append_task(root: Path, event: str, summary: str, **extra) -> Path:
    rec = {"ts": now_iso(), "event": event, "summary": summary}
    for key, value in extra.items():
        if value is not None:
            rec[key] = value
    dest = tasks_path(root)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return dest


def read_surfaces(root: Path) -> dict:
    path = surfaces_path(root)
    if not path.is_file():
        fallback = Path.home() / ".cursor" / "harness" / "surfaces.default.json"
        if fallback.is_file():
            path = fallback
        else:
            return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _goal_from_plan(plan: dict) -> str:
    items = plan.get("items") or []
    bits = []
    for item in items:
        why = str(item.get("why") or "").strip()
        if why:
            bits.append(why)
    if bits:
        return bits[0]
    return str(plan.get("session_id") or "未写目标")


def write_current_card(
    root: Path,
    session_id: str,
    plan: dict,
    activated: dict | None = None,
    progress: str | None = None,
) -> Path:
    act = activated or {}
    surfaces = read_surfaces(root)
    rows = surfaces.get("surfaces") or []
    official = []
    sandbox = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        oid = row.get("id") or "?"
        if row.get("official"):
            official.append(f"{oid}={row.get('official')}")
        if row.get("sandbox"):
            sandbox.append(f"{oid}={row.get('sandbox')}")
    named = []
    for kind in ("skills", "crafts", "mcp_allow"):
        for iid in act.get(kind) or []:
            named.append(f"{kind}:{iid}")
    craft_open = act.get("craft_open") or {}
    next_open = ", ".join(f"{k}→{v}" for k, v in craft_open.items()) or "无"
    forbid = plan.get("forbid") or []
    write_class = plan.get("write_class") or act.get("write_class") or "sandbox"
    lines = [
        "# 现行卡",
        "",
        f"- 会话: {session_id}",
        f"- 工作项: {plan.get('bead_id') or session_id}",
        f"- 目标: {_goal_from_plan(plan)}",
        f"- 进度: {progress or '名单已生成'}",
        f"- 写级别: {write_class}",
        f"- 正式面: {'; '.join(official) or '见 surfaces.json'}",
        f"- 隔离根: {'; '.join(sandbox) or '见 surfaces.json'}",
        f"- 已点名: {', '.join(named) or '无'}",
        f"- 职种下一步: {next_open}",
        f"- 禁改: {', '.join(str(x) for x in forbid) or '无'}",
        f"- 下一手: 按职种下一步打开技能，或按计划制作",
        "",
    ]
    dest = current_card_path(root, session_id)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines), encoding="utf-8")
    return dest
