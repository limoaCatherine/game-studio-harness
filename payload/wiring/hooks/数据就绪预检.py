#!/usr/bin/env python3
"""框架簿就绪硬闸。路径只来自环境变量与正式面地图。"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HOOKS = Path(__file__).resolve().parent
sys.path.insert(0, str(HOOKS))
from 工作区 import find_workspace, latest_session_id, read_activated  # noqa: E402

ENV_BOOKS = ("FRAMEWORK_WORKBOOK", "BATTLE_SIM_WORKBOOK")


def _required_sheets() -> list[str]:
    raw = (os.environ.get("DATA_READY_SHEETS") or "").strip()
    if not raw:
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]


def _from_surfaces(root: Path | None) -> list[Path]:
    if root is None:
        return []
    path = root / ".harness" / "surfaces.json"
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    out: list[Path] = []
    for row in data.get("surfaces") or []:
        if not isinstance(row, dict) or row.get("kind") != "excel":
            continue
        official = row.get("official")
        if not official:
            continue
        p = Path(official)
        if not p.is_absolute():
            p = root / p
        if p.is_file():
            out.append(p)
        elif p.is_dir():
            out.extend(sorted(p.glob("*.xlsx")))
    return out


def _candidates(root: Path | None) -> list[Path]:
    out: list[Path] = []
    for key in ENV_BOOKS:
        raw = (os.environ.get(key) or "").strip()
        if raw:
            out.append(Path(raw))
    out.extend(_from_surfaces(root))
    seen: set[str] = set()
    uniq: list[Path] = []
    for p in out:
        key = str(p)
        if key not in seen:
            seen.add(key)
            uniq.append(p)
    return uniq


def main() -> None:
    args = sys.argv[1:]
    root_arg = None
    if "--root" in args:
        i = args.index("--root")
        if i + 1 < len(args):
            root_arg = Path(args[i + 1])
    cwd = root_arg or Path.cwd()
    root = find_workspace(cwd) or (cwd if cwd.is_dir() else cwd.parent)

    findings: list[dict] = []
    tried = [str(p) for p in _candidates(root)]
    workbook = next((p for p in _candidates(root) if p.is_file()), None)

    try:
        import openpyxl  # type: ignore
    except ImportError:
        findings.append({
            "code": "openpyxl_missing",
            "next_actions": ["安装 openpyxl 后重跑，不改正式簿"],
        })
        _write(root, False, None, tried, findings)
        raise SystemExit(1)

    if workbook is None:
        findings.append({
            "code": "workbook_missing",
            "next_actions": [
                "设 FRAMEWORK_WORKBOOK，或在 surfaces.json 标 excel 官方根",
                f"已试路径: {tried}",
            ],
        })
        _write(root, False, None, tried, findings)
        raise SystemExit(2)

    try:
        wb = openpyxl.load_workbook(workbook, read_only=True, data_only=False)
        names = set(wb.sheetnames)
        wb.close()
    except Exception as e:
        findings.append({
            "code": "workbook_unreadable",
            "next_actions": [f"打开失败: {e}"],
        })
        _write(root, False, str(workbook), tried, findings)
        raise SystemExit(2)

    missing = [s for s in _required_sheets() if s not in names]
    if missing:
        findings.append({
            "code": "sheet_missing",
            "next_actions": [f"补齐页签: {missing}；现有 {sorted(names)}"],
        })
        _write(root, False, str(workbook), tried, findings)
        raise SystemExit(2)

    _write(root, True, str(workbook), tried, findings)
    raise SystemExit(0)


def _write(root: Path, ok: bool, workbook: str | None, tried: list[str], findings: list[dict]) -> None:
    act = read_activated(root)
    bead = (act or {}).get("bead_id") or latest_session_id(root) or "data-readiness"
    dest = root / ".harness" / "artifacts" / str(bead)
    dest.mkdir(parents=True, exist_ok=True)
    payload = {
        "ok": ok,
        "workbook": workbook,
        "tried_paths": tried,
        "findings": findings,
    }
    path = dest / "data-readiness.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
