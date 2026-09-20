#!/usr/bin/env python3
"""委托 ~/.cursor/harness/scripts/建议执行单.py（权威，steps 口径）。"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

HARNESS_SCRIPT = Path.home() / ".cursor" / "harness" / "scripts" / "建议执行单.py"


def main() -> None:
    if not HARNESS_SCRIPT.is_file():
        raise SystemExit(f"missing {HARNESS_SCRIPT}")
    ns = runpy.run_path(str(HARNESS_SCRIPT), run_name="not_main")
    raise SystemExit(int(ns["main"](sys.argv)))


if __name__ == "__main__":
    main()
