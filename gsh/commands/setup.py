# -*- coding: utf-8 -*-
"""引导式 / 脚本化安装。"""
from __future__ import annotations

import sys
from pathlib import Path

from gsh.paths_cli import resolve_pack
from gsh.profiles import ALL_TOOLS, parse_profile, parse_tools
from gsh.project import (
    land_cursor,
    land_other,
    land_shared,
    land_workspace,
    refresh_catalog,
    write_install_state,
)

# 延迟导入，避免与 pack 内 harness 脚本循环
def _homes(isolate):
    sys.path.insert(0, str(resolve_pack() / "harness" / "scripts"))
    from gsh_paths import homes_from_env  # type: ignore

    return homes_from_env(isolate)


def _prompt(msg: str, default: str) -> str:
    try:
        raw = input(f"{msg} [{default}]: ").strip()
    except EOFError:
        return default
    return raw or default


def run(
    *,
    workspace: Path | None,
    tools_raw: str,
    profile: str,
    isolate: Path | None,
    cursor_only: bool,
    write_mcp: bool,
    dry: bool,
    guided: bool,
    yes: bool,
    pack: Path | None,
) -> int:
    pack_root = resolve_pack(pack)
    if not (pack_root / "skills" / "route-task" / "SKILL.md").is_file():
        print("missing skills/ at pack root; clone the repo and run from there", file=sys.stderr)
        return 2

    if guided and not yes:
        print("Game Studio Harness 引导安装")
        print("只选一条安装路径。Cursor = 完整运行时；其它工具 = 约定/指令投影。")
        tools_raw = _prompt(
            "工具（legacy=五件套, all=含文档级适配器, 或逗号列表）",
            tools_raw or "legacy",
        )
        profile = _prompt("档位 minimal|core|full", profile or "full")
        if not cursor_only and workspace is None:
            default_ws = (Path.cwd() / "studio-root").resolve()
            workspace = Path(_prompt("业务根（将创建 .harness）", str(default_ws)))
        write_mcp = _prompt("写入占位 mcp.json？(y/N)", "n").lower() in {"y", "yes"}

    try:
        tools = parse_tools(tools_raw)
        profile = parse_profile(profile)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if not cursor_only and workspace is None and not yes and sys.stdin.isatty():
        default_ws = (Path.cwd() / "studio-root").resolve()
        workspace = Path(_prompt("业务根（将创建 .harness）", str(default_ws)))
    if not cursor_only and workspace is None:
        print("need --workspace or --cursor-only", file=sys.stderr)
        return 2

    h = _homes(isolate)
    copied: list[str] = []

    print(f"pack={pack_root}")
    print(f"profile={profile} tools={','.join(tools)}")
    if isolate:
        print(f"isolate-root={isolate}")
    print(f"gsh={h.gsh}")

    land_shared(pack_root, h, profile, dry, copied)
    mcp_msg = "skipped cursor mcp"
    if "cursor" in tools:
        mcp_msg = land_cursor(pack_root, h, profile, write_mcp, dry, copied)
    land_other(pack_root, h, tools, profile, dry, copied)
    catalog_msg = refresh_catalog(pack_root, h, dry)

    ws_msg = "skipped workspace"
    if workspace is not None:
        ws_msg = land_workspace(pack_root, workspace, dry, copied)

    write_install_state(h, pack_root, tools, profile, workspace, isolate, copied, dry)

    print(f"files={len(copied)}")
    print(mcp_msg)
    print(catalog_msg)
    print(ws_msg)
    if dry:
        for line in copied[:20]:
            print("dry", line)
        if len(copied) > 20:
            print(f"dry ... {len(copied) - 20} more")
        print("ok dry-run")
        return 0
    print("ok architecture files installed")
    return 0
