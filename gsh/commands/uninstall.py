# -*- coding: utf-8 -*-
"""按 install-state 撤投影。不删用户已有 mcp.json，不碰业务根正式面。"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from gsh.adapters import SPECS, home_for
from gsh.commands.setup import _homes
from gsh.project import read_install_state


KEEP_NAMES = {"mcp.json"}


def run(*, isolate: Path | None, dry: bool, yes: bool) -> int:
    h = _homes(isolate)
    state = read_install_state(h)
    if not state:
        print(f"no install-state at {h.state_file}", file=sys.stderr)
        return 2
    if not yes and not dry:
        print("uninstall will remove GSH projections under isolate/homes listed in install-state.")
        print("mcp.json is preserved. workspace official files are not touched.")
    roots = [h.gsh, h.agents_skills]
    for spec in SPECS:
        dest = home_for(h, spec)
        if spec.id == "cursor":
            roots.extend(
                [
                    dest / "skills",
                    dest / "agents",
                    dest / "hooks",
                    dest / "rules",
                    dest / "harness",
                    dest / "hooks.json",
                    dest / "gsh-adapter.json",
                    dest / "gsh-capability.json",
                    dest / "mcp.json.example",
                ]
            )
        else:
            roots.append(dest)
    removed = 0
    for path in roots:
        if path.name in KEEP_NAMES:
            continue
        if not path.exists():
            continue
        if dry:
            print("dry remove", path)
            removed += 1
            continue
        if path.is_file():
            path.unlink()
        else:
            shutil.rmtree(path)
        removed += 1
    if not dry and h.state_file.is_file():
        h.state_file.unlink()
    print(f"uninstalled entries={removed} dry={int(dry)}")
    print("ok uninstall")
    return 0
