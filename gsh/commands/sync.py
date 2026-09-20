# -*- coding: utf-8 -*-
"""从仓库根真相源重投影。改 skills/ 一处，这里把适配器拉齐。"""
from __future__ import annotations

import sys
from pathlib import Path

from gsh.adapters import land_selected
from gsh.commands.setup import _homes
from gsh.paths_cli import resolve_pack
from gsh.profiles import parse_profile, parse_tools
from gsh.project import (
    land_shared,
    land_workspace,
    read_install_state,
    refresh_catalog,
    write_install_state,
)


def run(
    *,
    workspace: Path | None,
    tools_raw: str,
    profile: str,
    isolate: Path | None,
    cursor_only: bool,
    dry: bool,
    pack: Path | None,
) -> int:
    pack_root = resolve_pack(pack)
    h = _homes(isolate)
    state = read_install_state(h)
    if state:
        tools_raw = tools_raw if tools_raw not in {"legacy", "all"} or not state.get("tools") else ",".join(state["tools"])
        if tools_raw in {"legacy", "all"} and state.get("tools"):
            tools_raw = ",".join(state["tools"])
        profile = state.get("profile") or profile
        if workspace is None and state.get("workspace"):
            workspace = Path(state["workspace"])
    try:
        tools = parse_tools(tools_raw)
        profile = parse_profile(profile)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    copied: list[str] = []
    land_shared(pack_root, h, profile, dry, copied)
    land_selected(pack_root, h, tools, profile, False, dry, copied)
    print(refresh_catalog(pack_root, h, dry))
    if workspace is not None and not cursor_only:
        land_workspace(pack_root, workspace, dry, copied)
    write_install_state(h, pack_root, tools, profile, workspace, isolate, copied, dry)
    print(f"synced files={len(copied)} profile={profile} tools={','.join(tools)}")
    print("ok sync")
    return 0
