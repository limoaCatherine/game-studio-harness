# -*- coding: utf-8 -*-
"""四层灰度 + 回归：旧计划仍能生成，新口径不预展开。"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

try:
    from gsh_paths import homes_from_env, harness_scripts

    _h = homes_from_env()
    CURSOR = _h.cursor
    HARNESS = _h.gsh_harness if (_h.gsh_harness / "scripts").is_dir() else _h.cursor / "harness"
    SCRIPTS = harness_scripts(_h)
    HOOKS = _h.cursor / "hooks"
except Exception:
    CURSOR = Path.home() / ".cursor"
    HARNESS = CURSOR / "harness"
    SCRIPTS = HARNESS / "scripts"
    HOOKS = CURSOR / "hooks"
PY = sys.executable
GRAY = "_gray-old"
NAMED = "_named-excel"


def run_py(script: Path, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(script), *args],
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )


def main() -> int:
    errors: list[str] = []
    root = Path.cwd()

    for script in ("接线自检.py", "握手四层.py", "整接.py"):
        rc = run_py(SCRIPTS / script, [], root)
        if rc.returncode != 0:
            errors.append(f"{script} rc={rc.returncode} {rc.stderr.strip()}")

    # 灰度：旧计划无 write_class / retrieve_keys 仍能生成
    gray = root / ".harness" / "sessions" / GRAY
    gray.mkdir(parents=True, exist_ok=True)
    (gray / "loadplan.json").write_text(
        json.dumps(
            {
                "session_id": GRAY,
                "tier": "T0",
                "verify_kind": "none",
                "items": [
                    {
                        "kind": "skill",
                        "id": "route-task",
                        "why": "旧计划缺新字段也应能生成名单。",
                    }
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    rc = run_py(SCRIPTS / "生成会话能力名单.py", [GRAY], root)
    if rc.returncode != 0:
        errors.append(f"灰度旧计划 rc={rc.returncode} {rc.stderr.strip()}")
    else:
        act = json.loads((gray / "activated.json").read_text(encoding="utf-8"))
        if not act.get("ok"):
            errors.append(f"灰度旧计划 errors={act.get('errors')}")
        if act.get("write_class") != "sandbox":
            errors.append(f"灰度默认 write_class={act.get('write_class')}")
        if not (gray / "current.md").is_file():
            errors.append("灰度旧计划缺 current.md")
        latest = (root / ".harness" / "sessions" / "LATEST").read_text(encoding="utf-8").strip()
        if latest == GRAY:
            errors.append("探测会话不应写入 LATEST")

    alias_probe = root / ".harness" / "sessions" / "_alias-handoff"
    alias_probe.mkdir(parents=True, exist_ok=True)
    (alias_probe / "loadplan.json").write_text(
        json.dumps(
            {
                "session_id": "_alias-handoff",
                "tier": "T0",
                "verify_kind": "none",
                "items": [
                    {
                        "kind": "skill",
                        "id": "交接",
                        "why": "旧中文 id 应解析到 handoff-pack。",
                    }
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    rc = run_py(SCRIPTS / "生成会话能力名单.py", ["_alias-handoff"], root)
    if rc.returncode != 0:
        errors.append(f"别名交接 rc={rc.returncode} {rc.stderr.strip()}")
    else:
        act = json.loads((alias_probe / "activated.json").read_text(encoding="utf-8"))
        if "handoff-pack" not in (act.get("skills") or []):
            errors.append(f"别名交接未解析 skills={act.get('skills')}")

    sys.path.insert(0, str(SCRIPTS))
    from 目录夹具 import first_skill_mcp

    catalog = json.loads((HARNESS / "catalog.json").read_text(encoding="utf-8"))
    skill_id, mcp_id = first_skill_mcp(catalog)
    named = root / ".harness" / "sessions" / NAMED
    named.mkdir(parents=True, exist_ok=True)
    (named / "loadplan.json").write_text(
        json.dumps(
            {
                "session_id": NAMED,
                "tier": "T0",
                "verify_kind": "none",
                "items": [
                    {
                        "kind": "skill",
                        "id": skill_id,
                        "why": "点名带外接的技能后才提示对应 mcp。",
                    }
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    rc = run_py(SCRIPTS / "生成会话能力名单.py", [NAMED], root)
    if rc.returncode != 0:
        errors.append(f"点名技能 rc={rc.returncode} {rc.stderr.strip()}")
    else:
        act = json.loads((named / "activated.json").read_text(encoding="utf-8"))
        if mcp_id not in (act.get("mcp_allow") or []):
            errors.append(f"点名 {skill_id} 后 mcp_allow={act.get('mcp_allow')}")

    surfaces = json.loads((root / ".harness" / "surfaces.json").read_text(encoding="utf-8"))
    if surfaces.get("version") != 1 or not surfaces.get("surfaces"):
        errors.append("surfaces.json 结构无效")

    sys.path.insert(0, str(HOOKS))
    from 工作区 import latest_session_id, session_boot_context, session_env

    sid = latest_session_id(root)
    if sid and sid.startswith("_"):
        errors.append(f"latest_session_id 落到探测会话 {sid}")
    env = session_env(root)
    if env.get("HARNESS_L1") != "1":
        errors.append("session_env 缺 HARNESS_L1")
    if sid and not env.get("HARNESS_CURRENT_CARD"):
        errors.append(f"{sid} 开场缺现行卡")
    ctx = session_boot_context(root)
    if "开场读序" not in ctx or "现行卡" not in ctx:
        errors.append("开场摘要未含现行卡")

    stop_src = (HOOKS / "结束.py").read_text(encoding="utf-8")
    if "session-card.json" in stop_src:
        errors.append("结束钩仍要 session-card.json")
    if "current.md" not in stop_src:
        errors.append("结束钩未认 current.md")

    stop = subprocess.run(
        [PY, str(HOOKS / "结束.py")],
        cwd=str(root),
        input=json.dumps({"status": "completed", "workspace_roots": [str(root)]}),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    if stop.returncode != 0:
        errors.append(f"结束钩 rc={stop.returncode} {stop.stderr.strip()}")
    elif "session-card" in (stop.stdout or ""):
        errors.append(f"结束钩仍提旧会话卡 {stop.stdout!r}")

    state = json.loads((root / ".harness" / "state.json").read_text(encoding="utf-8"))
    sessions = state.get("sessions") or {}
    if sid and sid not in sessions:
        errors.append(f"当前行 sessions 未保留 {sid}")

    if errors:
        for e in errors:
            print("error:", e, file=sys.stderr)
        return 2
    print("ok four-layer gray + regression")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
