# -*- coding: utf-8 -*-
"""业务根上的导演菜单、会话续上、职种下一步、关项。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from gsh.catalog import build_catalog
from gsh.paths_cli import resolve_pack


def find_studio(explicit: Path | None = None) -> Path | None:
    if explicit is not None:
        return Path(explicit).resolve()
    cur = Path.cwd().resolve()
    for p in [cur, *cur.parents]:
        if (p / ".harness" / "surfaces.json").is_file() or (p / ".harness" / "state.json").is_file():
            return p
    return None


def _scripts(pack: Path | None = None) -> Path:
    root = resolve_pack(pack)
    return root / "harness" / "scripts"


def _load_scripts(pack: Path | None = None):
    scripts = _scripts(pack)
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    import 职种路径  # type: ignore
    import 项目库  # type: ignore

    return 职种路径, 项目库


def _read_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def latest_session(root: Path, session: str | None = None) -> str | None:
    if session:
        return session
    latest = root / ".harness" / "sessions" / "LATEST"
    if latest.is_file():
        sid = latest.read_text(encoding="utf-8").strip()
        if sid and not sid.startswith("_"):
            return sid
    state = _read_json(root / ".harness" / "state.json")
    sid = str(state.get("session_id") or "").strip()
    return sid or None


def session_dir(root: Path, session: str) -> Path:
    return root / ".harness" / "sessions" / session


def load_catalog(pack: Path | None = None, isolate_gsh: Path | None = None) -> dict:
    if isolate_gsh and (isolate_gsh / "harness" / "catalog.json").is_file():
        return _read_json(isolate_gsh / "harness" / "catalog.json")
    pack_root = resolve_pack(pack)
    installed = pack_root / "harness" / "catalog.json"
    if installed.is_file():
        return _read_json(installed)
    return build_catalog(pack_root)


def menu(*, kind: str, query: str, pack: Path | None, limit: int = 24) -> list[dict]:
    catalog = load_catalog(pack)
    q = (query or "").strip().lower()
    key = "crafts" if kind == "craft" else "skills" if kind == "skill" else kind
    if key == "all":
        rows = [("craft", x) for x in catalog.get("crafts") or []] + [
            ("skill", x) for x in catalog.get("skills") or []
        ]
    else:
        rows = [(kind, x) for x in catalog.get(key) or []]
    out = []
    for row_kind, row in rows:
        blob = " ".join(
            str(row.get(k) or "")
            for k in ("id", "name", "description", "alias")
        ).lower()
        if q and q not in blob:
            continue
        item = {
            "kind": row_kind,
            "id": row.get("id"),
            "name": row.get("name") or row.get("id"),
            "description": (row.get("description") or "")[:160],
        }
        if row.get("uses_skills"):
            item["steps"] = len(row["uses_skills"])
            item["first"] = row["uses_skills"][0]
        out.append(item)
        if len(out) >= limit:
            break
    return out


def print_menu(rows: list[dict]) -> None:
    if not rows:
        print("no matches. try --q ttk or --kind craft")
        return
    print("director menu (ids only; do not paste catalog.json into the thread)")
    for row in rows:
        extra = ""
        if row.get("steps"):
            extra = f"  path={row['steps']} first={row.get('first')}"
        print(f"{row['kind']:6} {row['id']:32} {row['description']}{extra}")


def status_payload(root: Path, session: str | None, pack: Path | None) -> dict:
    paths_mod, lib = _load_scripts(pack)
    sid = latest_session(root, session)
    state = _read_json(root / ".harness" / "state.json")
    out = {
        "workspace": str(root),
        "session": sid,
        "bead_id": state.get("bead_id"),
        "progress": state.get("progress"),
        "write_class": None,
        "card": None,
        "craft_path": {},
        "verify": None,
        "resume": None,
    }
    if not sid:
        out["resume"] = "python -m gsh menu --kind craft --q 竖切"
        return out
    sdir = session_dir(root, sid)
    plan = _read_json(sdir / "loadplan.json")
    activated = _read_json(sdir / "activated.json")
    catalog = load_catalog(pack)
    crafts = list(activated.get("crafts") or [])
    craft_open = dict(activated.get("craft_open") or {})
    stored = activated.get("craft_path") if isinstance(activated.get("craft_path"), dict) else {}
    paths = stored or paths_mod.build_paths(catalog, crafts, craft_open)
    out["write_class"] = activated.get("write_class") or plan.get("write_class") or "sandbox"
    out["bead_id"] = activated.get("bead_id") or plan.get("bead_id") or out["bead_id"]
    out["craft_path"] = paths
    out["named"] = {
        "skills": activated.get("skills") or [],
        "crafts": crafts,
    }
    card = sdir / "current.md"
    if card.is_file():
        out["card"] = str(card)
        out["card_text"] = card.read_text(encoding="utf-8")
    bead = out.get("bead_id")
    if bead:
        report_path = root / ".harness" / "artifacts" / str(bead) / "verify-report.json"
        if report_path.is_file():
            report = _read_json(report_path)
            out["verify"] = {
                "path": str(report_path),
                "verdict": report.get("verdict"),
                "kind": report.get("verify_kind"),
            }
        else:
            out["verify"] = {"path": str(report_path), "verdict": None}
    nxt = None
    for cid, row in paths.items():
        if row.get("current"):
            nxt = f"open skills/{row['current']}/SKILL.md"
            if row.get("next"):
                nxt += f" ; later: python -m gsh next --craft {cid}"
            break
    out["resume"] = nxt or "python -m gsh menu --kind craft"
    tasks = root / ".harness" / "memory" / "tasks.jsonl"
    if tasks.is_file():
        lines = [ln for ln in tasks.read_text(encoding="utf-8").splitlines() if ln.strip()]
        out["recent_tasks"] = lines[-5:]
    _ = lib
    return out


def print_status(payload: dict) -> None:
    print(f"workspace={payload.get('workspace')}")
    print(f"session={payload.get('session') or '-'}")
    print(f"bead={payload.get('bead_id') or '-'}")
    print(f"write_class={payload.get('write_class') or '-'}")
    print(f"progress={payload.get('progress') or '-'}")
    paths = payload.get("craft_path") or {}
    if paths:
        from importlib import import_module

        sys.path.insert(0, str(_scripts()))
        paths_mod = import_module("职种路径")
        print(f"craft_path={paths_mod.render_progress(paths)}")
    verify = payload.get("verify")
    if verify:
        print(f"verify={verify.get('verdict') or 'open'} {verify.get('path')}")
    print(f"resume={payload.get('resume')}")
    if payload.get("card"):
        print(f"card={payload['card']}")


def print_resume(payload: dict) -> None:
    text = payload.get("card_text")
    if text:
        print(text.rstrip())
        print()
    print(f"resume: {payload.get('resume')}")
    print("close:  python -m gsh close --kind smoke --evidence <path>")


def activate_roster(root: Path, session: str, pack: Path | None) -> int:
    import os

    scripts = _scripts(pack)
    pack_root = resolve_pack(pack)
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    from 生成会话能力名单 import main as gen  # type: ignore

    catalog = pack_root / "harness" / "catalog.json"
    if not catalog.is_file():
        from gsh.catalog import build_catalog

        catalog.parent.mkdir(parents=True, exist_ok=True)
        catalog.write_text(
            json.dumps(build_catalog(pack_root), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    old = Path.cwd()
    prev_cat = os.environ.get("GSH_CATALOG")
    prev_pack = os.environ.get("GSH_PACK_ROOT")
    try:
        os.environ["GSH_CATALOG"] = str(catalog)
        os.environ["GSH_PACK_ROOT"] = str(pack_root)
        os.chdir(root)
        return int(gen([str(scripts / "生成会话能力名单.py"), session]))
    finally:
        os.chdir(old)
        if prev_cat is None:
            os.environ.pop("GSH_CATALOG", None)
        else:
            os.environ["GSH_CATALOG"] = prev_cat
        if prev_pack is None:
            os.environ.pop("GSH_PACK_ROOT", None)
        else:
            os.environ["GSH_PACK_ROOT"] = prev_pack


def advance_craft(root: Path, session: str | None, craft: str | None, pack: Path | None) -> dict:
    paths_mod, lib = _load_scripts(pack)
    sid = latest_session(root, session)
    if not sid:
        raise ValueError("no current session; write a loadplan and run the roster first")
    sdir = session_dir(root, sid)
    activated = _read_json(sdir / "activated.json")
    if not activated:
        raise ValueError(f"missing {sdir / 'activated.json'}")
    catalog = load_catalog(pack)
    crafts = list(activated.get("crafts") or [])
    if not crafts:
        raise ValueError("no craft on this session")
    cid = craft or crafts[0]
    if cid not in crafts:
        raise ValueError(f"craft {cid} is not named on this session")
    stored = activated.get("craft_path") if isinstance(activated.get("craft_path"), dict) else {}
    paths = stored or paths_mod.build_paths(catalog, crafts, dict(activated.get("craft_open") or {}))
    current = paths.get(cid) or paths_mod.path_row(paths_mod.steps_for(catalog, cid))
    nxt = paths_mod.advance(current)
    paths[cid] = nxt
    opened = dict(activated.get("craft_open") or {})
    if nxt.get("current"):
        opened[cid] = nxt["current"]
    activated["craft_open"] = opened
    activated["craft_path"] = paths
    skills = list(activated.get("skills") or [])
    if nxt.get("current") and nxt["current"] not in skills:
        skills.append(nxt["current"])
        activated["skills"] = skills
    dest = sdir / "activated.json"
    dest.write_text(json.dumps(activated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    plan = _read_json(sdir / "loadplan.json")
    progress = paths_mod.render_progress(paths)
    lib.write_current_card(root, sid, plan or activated, activated=activated, progress=progress)
    if not sid.startswith("_"):
        lib.write_state(
            root,
            {
                "session_id": sid,
                "bead_id": activated.get("bead_id"),
                "progress": progress,
                "current_card": str(sdir / "current.md"),
            },
        )
        lib.append_task(root, "craft-next", progress, session_id=sid, craft=cid)
    return {"session": sid, "craft": cid, "path": nxt, "progress": progress}


def close_item(
    root: Path,
    *,
    session: str | None,
    kind: str,
    evidence: list[str],
    command: str,
    notes: str,
    verdict: str,
    pack: Path | None,
) -> Path:
    _, lib = _load_scripts(pack)
    sid = latest_session(root, session)
    if not sid:
        raise ValueError("no current session")
    sdir = session_dir(root, sid)
    activated = _read_json(sdir / "activated.json")
    plan = _read_json(sdir / "loadplan.json")
    bead = str(
        activated.get("bead_id")
        or plan.get("bead_id")
        or sid
    )
    verify_kind = kind or activated.get("verify_kind") or plan.get("verify_kind") or "smoke"
    if verify_kind in {"none", None, ""}:
        verify_kind = "smoke"
    paths = [p for p in evidence if p.strip()]
    if not paths:
        card = sdir / "current.md"
        paths = [str(card) if card.is_file() else str(sdir / "activated.json")]
    report = {
        "bead_id": bead,
        "verify_kind": verify_kind,
        "command": command or "python -m gsh close",
        "exit_code": 0 if verdict == "pass" else 1,
        "evidence_paths": paths,
        "verdict": verdict,
        "notes": notes,
    }
    dest = root / ".harness" / "artifacts" / bead / "verify-report.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    index = root / ".harness" / "artifacts" / "index.jsonl"
    index.parent.mkdir(parents=True, exist_ok=True)
    rec = {
        "bead_id": bead,
        "skill": "verify-gate",
        "path": str(dest),
        "summary": f"close {verdict} {verify_kind}",
    }
    with index.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    progress = f"关项 {bead} {verdict}"
    lib.write_current_card(root, sid, plan or activated, activated=activated, progress=progress)
    if not sid.startswith("_"):
        lib.write_state(
            root,
            {
                "session_id": sid,
                "bead_id": bead,
                "progress": progress,
                "status": "closed" if verdict == "pass" else "rework",
            },
        )
        lib.append_task(root, "close", progress, session_id=sid, bead_id=bead, verdict=verdict)
    return dest
