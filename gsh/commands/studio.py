# -*- coding: utf-8 -*-
"""menu / status / resume / next / close。"""
from __future__ import annotations

import sys
from pathlib import Path

from gsh.paths_cli import resolve_pack
from gsh.studio import (
    activate_roster,
    advance_craft,
    close_item,
    find_studio,
    menu,
    print_menu,
    print_resume,
    print_status,
    status_payload,
)


def _root(workspace: Path | None) -> Path:
    root = find_studio(workspace)
    if root is None:
        print("need --workspace or a directory that contains .harness", file=sys.stderr)
        raise SystemExit(2)
    return root


def run_menu(*, kind: str, query: str, pack: Path | None) -> int:
    print_menu(menu(kind=kind, query=query, pack=resolve_pack(pack)))
    return 0


def run_status(*, workspace: Path | None, session: str | None, pack: Path | None) -> int:
    payload = status_payload(_root(workspace), session, resolve_pack(pack))
    print_status(payload)
    return 0


def run_resume(*, workspace: Path | None, session: str | None, pack: Path | None) -> int:
    payload = status_payload(_root(workspace), session, resolve_pack(pack))
    print_resume(payload)
    return 0


def run_next(*, workspace: Path | None, session: str | None, craft: str | None, pack: Path | None) -> int:
    try:
        result = advance_craft(_root(workspace), session, craft, resolve_pack(pack))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(result["progress"])
    print(f"session={result['session']} craft={result['craft']} current={result['path'].get('current')} next={result['path'].get('next')}")
    return 0


def run_close(
    *,
    workspace: Path | None,
    session: str | None,
    kind: str,
    evidence: str,
    command: str,
    notes: str,
    verdict: str,
    pack: Path | None,
) -> int:
    paths = [p.strip() for p in (evidence or "").replace(";", ",").split(",") if p.strip()]
    try:
        dest = close_item(
            _root(workspace),
            session=session,
            kind=kind,
            evidence=paths,
            command=command,
            notes=notes,
            verdict=verdict,
            pack=resolve_pack(pack),
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"wrote {dest}")
    print("ok close")
    return 0


def run_activate(*, workspace: Path | None, session: str, pack: Path | None) -> int:
    root = _root(workspace)
    return activate_roster(root, session, resolve_pack(pack))
