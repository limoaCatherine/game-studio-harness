#!/usr/bin/env python3
"""会话开始：菜单过期则刷新，再写入路口环境。"""
from __future__ import annotations

import json
import runpy
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from 工作区 import find_workspace, session_boot_context, session_env

REFRESH = Path.home() / ".cursor" / "harness" / "scripts" / "刷新菜单.py"
BOOT = Path.home() / ".cursor" / "harness" / "scripts" / "拉起外接.py"


def refresh_if_stale() -> None:
    if not REFRESH.is_file():
        return
    ns = runpy.run_path(str(REFRESH), run_name="not_main")
    stale = ns.get("catalog_stale")
    main = ns.get("main")
    if callable(stale) and callable(main) and stale():
        import contextlib
        import io

        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            main()


def boot_mcps() -> None:
    if not BOOT.is_file():
        return
    try:
        subprocess.run(
            [sys.executable, str(BOOT), "--boot", "--no-host"],
            timeout=12,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except Exception:
        pass


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}
    try:
        refresh_if_stale()
        boot_mcps()
    except Exception:
        pass
    roots = payload.get("workspace_roots") or []
    cwd = roots[0] if roots else Path.cwd()
    root = find_workspace(cwd)
    print(
        json.dumps(
            {
                "env": session_env(root),
                "additional_context": session_boot_context(root),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
