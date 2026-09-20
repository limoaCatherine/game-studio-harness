# -*- coding: utf-8 -*-
"""Locate the GSH pack (skills / agents / rules / hooks / harness).

Resolution order:

1. ``--pack-root`` (explicit argument)
2. ``GSH_PACK_ROOT``
3. A git checkout that contains the source trees next to this module or cwd
4. Pack data bundled in the installed wheel (``gsh/pack_data``)

Checkout wins when you edit SSOT in a clone. A ``pipx install .`` / ``pip install``
from another working directory uses the bundled copy so ``gsh setup`` works
without a live git tree.
"""
from __future__ import annotations

import os
from pathlib import Path


def is_pack_root(path: Path) -> bool:
    root = Path(path)
    return (root / "skills" / "route-task" / "SKILL.md").is_file() and (
        root / "harness" / "scripts"
    ).is_dir()


def bundled_pack() -> Path | None:
    """Pack data shipped inside the wheel (``gsh/pack_data``)."""
    cand = Path(__file__).resolve().parent / "pack_data"
    if is_pack_root(cand):
        return cand
    return None


def _walk_pack(start: Path) -> Path | None:
    cur = Path(start).resolve()
    if cur.is_file():
        cur = cur.parent
    for path in [cur, *cur.parents]:
        if is_pack_root(path):
            return path
    return None


def resolve_pack(explicit: Path | None = None) -> Path:
    if explicit is not None:
        return Path(explicit).resolve()
    env = (os.environ.get("GSH_PACK_ROOT") or "").strip()
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve()
    near_module = _walk_pack(here.parent.parent)
    if near_module is not None:
        return near_module
    near_cwd = _walk_pack(Path.cwd())
    if near_cwd is not None:
        return near_cwd
    bundled = bundled_pack()
    if bundled is not None:
        return bundled
    return Path.cwd().resolve()


def studio_scaffold(pack: Path) -> Path:
    """Studio ``.harness`` scaffold. Checkout uses ``studio/.harness``; the wheel
    ships the same files under ``studio_harness`` so hidden dirs are not required.
    """
    hidden = Path(pack) / "studio" / ".harness"
    if hidden.is_dir():
        return hidden
    return Path(pack) / "studio_harness"
