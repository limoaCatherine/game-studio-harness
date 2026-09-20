# -*- coding: utf-8 -*-
"""核名单点名注入：职种不预展开路径。"""
from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path

try:
    from gsh_paths import find_catalog, homes_from_env, harness_scripts

    _h = homes_from_env()
    CURSOR = _h.cursor
    CATALOG = find_catalog(_h)
    WORKSPACE = _h.cursor / "hooks" / "工作区.py"
    GENERATE = harness_scripts(_h) / "生成会话能力名单.py"
    FIXTURE = harness_scripts(_h) / "目录夹具.py"
except Exception:
    CURSOR = Path.home() / ".cursor"
    CATALOG = CURSOR / "harness" / "catalog.json"
    WORKSPACE = CURSOR / "hooks" / "工作区.py"
    GENERATE = CURSOR / "harness" / "scripts" / "生成会话能力名单.py"
    FIXTURE = CURSOR / "harness" / "scripts" / "目录夹具.py"
PROBE = "_wire-check"


def main() -> int:
    errors: list[str] = []
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    sys.path.insert(0, str(FIXTURE.parent))
    from 目录夹具 import first_craft_path, path_mcps

    cid, uses = first_craft_path(catalog)
    if not cid:
        errors.append("菜单没有任何带 uses_skills 的职种")
        _done(errors)
        return 2
    first = uses[0]
    hidden = path_mcps(catalog, uses)

    ws = WORKSPACE.read_text(encoding="utf-8")
    if "stack.yaml" in ws or "read_stack" in ws:
        errors.append("工作区.py 仍引用 stack.yaml")

    root = Path.cwd()
    if (root / "stack.yaml").is_file():
        errors.append("业务根仍有 stack.yaml")

    sess = root / ".harness" / "sessions" / PROBE
    sess.mkdir(parents=True, exist_ok=True)
    (sess / "loadplan.json").write_text(
        json.dumps(
            {
                "session_id": PROBE,
                "tier": "T0",
                "verify_kind": "none",
                "write_class": "sandbox",
                "items": [
                    {
                        "kind": "craft",
                        "id": cid,
                        "why": "只点职种时不得预展开全路径技能与外接。",
                    }
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    ns = runpy.run_path(str(GENERATE), run_name="not_main")
    rc = int(ns["main"]([str(GENERATE), PROBE]))
    if rc != 0:
        errors.append(f"生成名单失败 rc={rc}")
    else:
        act = json.loads((sess / "activated.json").read_text(encoding="utf-8"))
        if act.get("skills"):
            errors.append(f"只点职种时 skills 应为空，实际={act.get('skills')}")
        leaked = set(hidden) & set(act.get("mcp_allow") or [])
        if leaked:
            errors.append(f"只点职种时不应预展开 {sorted(leaked)}")
        opened = (act.get("craft_open") or {}).get(cid)
        if opened != first:
            errors.append(f"craft_open 应为 {first}，实际={opened}")
        if not (sess / "current.md").is_file():
            errors.append("探测会话缺 current.md")

    return _done(errors)


def _done(errors: list[str]) -> int:
    if errors:
        for e in errors:
            print("error:", e, file=sys.stderr)
        return 2
    print("ok craft named not pre-expanded + current card")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
