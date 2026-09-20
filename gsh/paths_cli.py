# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from pathlib import Path


def resolve_pack(explicit: Path | None = None) -> Path:
    if explicit is not None:
        return Path(explicit).resolve()
    env = (os.environ.get("GSH_PACK_ROOT") or "").strip()
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve()
    for p in [here.parent.parent, *here.parents]:
        if (p / "skills" / "route-task" / "SKILL.md").is_file() and (p / "harness" / "scripts").is_dir():
            return p
    return Path.cwd().resolve()
