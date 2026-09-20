# -*- coding: utf-8 -*-
"""按加载计划排出执行类在前、收口类在后的 flow.json。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

CLOSE_IDS = {
    "artifacts-append",
    "verify-gate",
    "handoff-pack",
    "sync-state",
}


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: 建议执行单.py <会话> [--force]", file=sys.stderr)
        return 1
    session = argv[1]
    force = "--force" in argv
    root = Path.cwd()
    sess = root / ".harness" / "sessions" / session
    plan_path = sess / "loadplan.json"
    dest = sess / "flow.json"
    if not plan_path.is_file():
        print(f"missing loadplan: {plan_path}", file=sys.stderr)
        return 2
    if dest.is_file() and not force:
        print(f"exists {dest} (pass --force to overwrite)")
        return 0
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    execute, close = [], []
    for item in plan.get("items") or []:
        if item.get("kind") not in {"skill", "craft"}:
            continue
        row = {
            "id": item.get("id"),
            "kind": "close" if item.get("id") in CLOSE_IDS else "execute",
            "why": item.get("why", ""),
        }
        (close if row["kind"] == "close" else execute).append(row)
    dest.write_text(
        json.dumps(
            {"session_id": plan.get("session_id", session), "steps": execute + close},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
