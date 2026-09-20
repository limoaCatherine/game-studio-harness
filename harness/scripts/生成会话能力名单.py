# -*- coding: utf-8 -*-
"""生成 activated.json 与现行卡。职种不预展开路径。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import os


def resolve_catalog() -> Path:
    env = (os.environ.get("GSH_CATALOG") or "").strip()
    if env and Path(env).is_file():
        return Path(env)
    try:
        from gsh_paths import find_catalog, find_pack_root

        found = find_catalog()
        if found.is_file():
            return found
        pack = find_pack_root()
        cand = pack / "harness" / "catalog.json"
        if cand.is_file():
            return cand
        return found
    except Exception:
        return Path.home() / ".cursor" / "harness" / "catalog.json"


CATALOG = resolve_catalog()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def catalog_ids(catalog: dict) -> dict[str, set[str]]:
    return {
        "skill": {x["id"] for x in catalog.get("skills") or []},
        "craft": {x["id"] for x in catalog.get("crafts") or []},
        "mcp": {x["id"] for x in catalog.get("mcp") or []},
    }


def catalog_alias_map(catalog: dict) -> dict[str, dict[str, str]]:
    out = {"skill": {}, "craft": {}, "mcp": {}}
    groups = {
        "skill": catalog.get("skills") or [],
        "craft": catalog.get("crafts") or [],
        "mcp": catalog.get("mcp") or [],
    }
    for kind, rows in groups.items():
        for row in rows:
            cid = row.get("id")
            if not cid:
                continue
            out[kind][cid] = cid
            for key in ("alias", "name"):
                alt = row.get(key)
                if alt:
                    out[kind][str(alt)] = cid
    return out


def resolve_id(kind: str, iid: str, aliases: dict[str, dict[str, str]]) -> str | None:
    return aliases.get(kind, {}).get(iid)


def uniq(seq):
    seen = set()
    out = []
    for x in seq:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: 生成会话能力名单.py <会话>", file=sys.stderr)
        return 1
    session = argv[1]
    root = Path.cwd()
    plan_path = root / ".harness" / "sessions" / session / "loadplan.json"
    if not plan_path.is_file():
        print(f"missing loadplan: {plan_path}", file=sys.stderr)
        return 2
    catalog_path = CATALOG if CATALOG.is_file() else resolve_catalog()
    if not catalog_path.is_file():
        print(f"missing catalog: {catalog_path} (run 刷新菜单.py or gsh setup)", file=sys.stderr)
        return 2

    plan = load_json(plan_path)
    catalog = load_json(catalog_path)
    ids = catalog_ids(catalog)
    aliases = catalog_alias_map(catalog)

    skills, crafts, mcps = [], [], []
    errors = []
    for item in plan.get("items") or []:
        kind = item.get("kind")
        iid = item.get("id")
        if kind not in {"skill", "craft", "mcp"}:
            continue
        resolved = resolve_id(kind, iid, aliases)
        if not resolved:
            errors.append(f"{kind}:{iid} not in catalog")
            continue
        iid = resolved
        if iid not in ids.get(kind, set()):
            errors.append(f"{kind}:{iid} not in catalog")
            continue
        if kind == "skill":
            skills.append(iid)
        elif kind == "craft":
            crafts.append(iid)
        else:
            mcps.append(iid)

    skills, crafts, mcps = uniq(skills), uniq(crafts), uniq(mcps)
    skill_rows = {x["id"]: x for x in catalog.get("skills") or []}
    craft_rows = {x["id"]: x for x in catalog.get("crafts") or []}
    expanded = []

    def absorb(src: str, sid: str) -> None:
        for mid in skill_rows.get(sid, {}).get("needs_mcp") or []:
            mid = str(mid).strip()
            if not mid:
                continue
            if mid not in ids.get("mcp", set()):
                errors.append(f"needs_mcp {src}->{mid} not in catalog")
                continue
            if mid not in mcps:
                mcps.append(mid)
                expanded.append(f"{src}->{mid}")

    for sid in skills:
        absorb(sid, sid)

    craft_open = {}
    for cid in crafts:
        uses = [str(x) for x in (craft_rows.get(cid, {}).get("uses_skills") or []) if str(x).strip()]
        if uses:
            craft_open[cid] = uses[0]

    from 职种路径 import build_paths  # type: ignore

    craft_path = build_paths(catalog, crafts, craft_open)

    mcp_tools = {}
    for row in catalog.get("mcp") or []:
        if row.get("id") in mcps and row.get("tools"):
            mcp_tools[row["id"]] = row["tools"]

    write_class = plan.get("write_class") or "sandbox"
    out = {
        "session_id": plan.get("session_id", session),
        "bead_id": plan.get("bead_id"),
        "verify_kind": plan.get("verify_kind"),
        "intent": plan.get("intent"),
        "work_mode": plan.get("work_mode"),
        "write_class": write_class,
        "retrieve_keys": plan.get("retrieve_keys") or [],
        "forbid": plan.get("forbid") or [],
        "source": "生成会话能力名单.py",
        "catalog": str(catalog_path),
        "ok": len(errors) == 0,
        "skills": skills,
        "crafts": crafts,
        "craft_open": craft_open,
        "craft_path": craft_path,
        "mcp_allow": mcps,
        "mcp_expanded": expanded,
        "mcp_tools": mcp_tools,
        "errors": errors,
    }
    dest = plan_path.parent / "activated.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    scripts = Path(__file__).resolve().parent
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    from 项目库 import append_task, write_current_card, write_state

    write_current_card(
        root,
        session,
        plan,
        activated=out,
        progress=f"名单已生成 {session}",
    )

    if not session.startswith("_"):
        latest = plan_path.parent.parent / "LATEST"
        latest.write_text(session + "\n", encoding="utf-8")
        write_state(
            root,
            {
                "session_id": session,
                "bead_id": plan.get("bead_id"),
                "progress": f"名单已生成 {session}",
                "current_card": str(plan_path.parent / "current.md"),
            },
        )
        append_task(
            root,
            "activate",
            f"生成名单 {session}",
            session_id=session,
            bead_id=plan.get("bead_id"),
        )
    print(f"wrote {dest}")
    if errors:
        for e in errors:
            print("error:", e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
