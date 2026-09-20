#!/usr/bin/env python3
"""委托 ~/.cursor/harness/scripts/生成会话能力名单.py（权威）。"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

HOOKS = Path(__file__).resolve().parent
sys.path.insert(0, str(HOOKS))
from 工作区 import find_workspace, write_latest  # noqa: E402

HARNESS_SCRIPT = Path.home() / ".cursor" / "harness" / "scripts" / "生成会话能力名单.py"


def main() -> None:
    if len(sys.argv) < 2:
        print("用法: python 生成会话能力名单.py <会话id>", file=sys.stderr)
        raise SystemExit(2)
    sid = sys.argv[1].strip()
    root = find_workspace(Path.cwd())
    if root is None:
        raise SystemExit(f"找不到业务根（缺 .harness）: {Path.cwd()}")
    if not HARNESS_SCRIPT.is_file():
        raise SystemExit(f"missing {HARNESS_SCRIPT}")
    import os

    os.chdir(root)
    code = runpy.run_path(str(HARNESS_SCRIPT), run_name="not_main")
    rc = int(code["main"]([str(HARNESS_SCRIPT), sid]))
    write_latest(root, sid)
    raise SystemExit(rc)


if __name__ == "__main__":
    main()
