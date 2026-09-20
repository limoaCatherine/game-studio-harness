#!/usr/bin/env python3
"""委托 ~/.cursor/harness/scripts/建议执行单.py（权威，steps 口径）。"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

def _harness_script() -> Path:
    here = Path(__file__).resolve()
    for cand in (
        here.parents[1] / "harness" / "scripts" / "建议执行单.py",
        here.parents[2] / "harness" / "scripts" / "建议执行单.py",
    ):
        if cand.is_file():
            return cand
    try:
        sys.path.insert(0, str(here.parent))
        scripts = here.parents[2] / "harness" / "scripts"
        if (scripts / "gsh_paths.py").is_file():
            sys.path.insert(0, str(scripts))
            from gsh_paths import harness_scripts, homes_from_env  # type: ignore

            return harness_scripts(homes_from_env()) / "建议执行单.py"
    except Exception:
        pass
    return Path.home() / ".cursor" / "harness" / "scripts" / "建议执行单.py"


HARNESS_SCRIPT = _harness_script()


def main() -> None:
    if not HARNESS_SCRIPT.is_file():
        raise SystemExit(f"missing {HARNESS_SCRIPT}")
    ns = runpy.run_path(str(HARNESS_SCRIPT), run_name="not_main")
    raise SystemExit(int(ns["main"](sys.argv)))


if __name__ == "__main__":
    main()
