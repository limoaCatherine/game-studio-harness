# -*- coding: utf-8 -*-
"""诊断：Python 版本、漂移、缺文件、密钥痕迹、各工具原生能力。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from gsh.adapters import SPECS, home_for
from gsh.catalog import build_catalog
from gsh.commands.setup import _homes
from gsh.commands.verify import BANNED_PACK_TREES, NEED_HOOKS, NEED_SCRIPTS, NEED_SKILLS
from gsh.paths_cli import resolve_pack
from gsh.profiles import parse_tools
from gsh.project import read_install_state


def run(*, workspace: Path | None, tools_raw: str, isolate: Path | None, pack: Path | None) -> int:
    pack_root = resolve_pack(pack)
    h = _homes(isolate)
    print(f"python={sys.version.split()[0]} pack={pack_root}")
    if sys.version_info < (3, 11):
        print("warn: GSH CLI requires Python 3.11+")
    state = read_install_state(h)
    if state:
        print(f"install-state profile={state.get('profile')} tools={state.get('tools')}")
    else:
        print("install-state: missing (run setup)")

    catalog = build_catalog(pack_root)
    print(f"pack skills={len(catalog['skills'])} crafts={len(catalog['crafts'])} mcp_stubs={len(catalog['mcp'])}")
    print("mcp_policy:", catalog["policy"]["note"])

    issues: list[str] = []
    for rel in BANNED_PACK_TREES:
        if (pack_root / rel).is_dir():
            issues.append(f"duplicated tree still present: {rel}")
    for sid in NEED_SKILLS:
        if not (pack_root / "skills" / sid / "SKILL.md").is_file():
            issues.append(f"pack missing {sid}")
    for name in NEED_SCRIPTS:
        if not (pack_root / "harness" / "scripts" / name).is_file():
            issues.append(f"pack missing script {name}")
    for name in NEED_HOOKS:
        if not (pack_root / "hooks" / name).is_file():
            issues.append(f"pack missing hook {name}")

    if (h.gsh_harness / "catalog.json").is_file():
        data = json.loads((h.gsh_harness / "catalog.json").read_text(encoding="utf-8"))
        print(f"installed catalog skills={len(data.get('skills') or [])}")
        src = Path((data.get("source") or {}).get("skills") or "")
        if src and src.is_dir() and (h.gsh_skills / "route-task" / "SKILL.md").is_file():
            pack_txt = (pack_root / "skills" / "route-task" / "SKILL.md").read_text(encoding="utf-8")
            inst_txt = (h.gsh_skills / "route-task" / "SKILL.md").read_text(encoding="utf-8")
            if pack_txt != inst_txt:
                issues.append("shared runtime drifted from pack skills/route-task — run sync")
    else:
        issues.append("no installed catalog — run setup")

    if workspace:
        if not (Path(workspace) / ".harness" / "surfaces.json").is_file():
            issues.append(f"workspace {workspace} missing .harness/surfaces.json")

    if state and state.get("tools") and tools_raw in {"all", "legacy"}:
        tools_raw = ",".join(state["tools"])
    try:
        tools = parse_tools(tools_raw)
    except ValueError:
        tools = []
    print("native adapters:")
    for spec in SPECS:
        dest = home_for(h, spec)
        cap = dest / "gsh-capability.json"
        mark = "installed" if cap.is_file() else "absent"
        selected = "selected" if spec.id in tools else "idle"
        print(f"  {spec.id:10} {spec.runtime:14} hooks={spec.hooks:7} {mark}/{selected}")
    if issues:
        print("doctor found issues:")
        for item in issues:
            print(" -", item)
        return 1
    print("ok doctor")
    return 0
