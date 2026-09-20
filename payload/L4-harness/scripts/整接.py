# -*- coding: utf-8 -*-
"""四层整接：菜单 → 点名名单 → 现行卡 → 钩子 → 项目库。"""
from __future__ import annotations

import json
import runpy
import subprocess
import sys
from pathlib import Path

CURSOR = Path.home() / ".cursor"
HARNESS = CURSOR / "harness"
HOOKS = CURSOR / "hooks"
SCRIPTS = HARNESS / "scripts"
PY = sys.executable
PROBE = "_join-craft"


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def run_py(script: Path, args: list[str], cwd: Path, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(script), *args],
        cwd=str(cwd),
        input=stdin,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )


def main() -> int:
    errors: list[str] = []
    root = Path.cwd()
    if not (root / ".harness").is_dir():
        print("cwd 须为业务根", file=sys.stderr)
        return 2

    l1 = [
        CURSOR / "rules" / "全局.mdc",
        CURSOR / "skills" / "route-task" / "SKILL.md",
        CURSOR / "skills" / "write-isolation" / "SKILL.md",
        CURSOR / "skills" / "doctor" / "SKILL.md",
        CURSOR / "skills" / "verify-gate" / "SKILL.md",
        HARNESS / "catalog.json",
        HARNESS / "surfaces.default.json",
        SCRIPTS / "刷新菜单.py",
        SCRIPTS / "生成会话能力名单.py",
        SCRIPTS / "项目库.py",
        HOOKS / "开场.py",
        HOOKS / "结束.py",
        HOOKS / "工作区.py",
        root / ".harness" / "surfaces.json",
    ]
    for path in l1:
        if not path.is_file():
            fail(errors, f"缺路口 {path}")

    if (root / "stack.yaml").is_file():
        fail(errors, "业务根仍有 stack.yaml")

    ws = (HOOKS / "工作区.py").read_text(encoding="utf-8")
    if "stack.yaml" in ws:
        fail(errors, "工作区.py 仍引用 stack.yaml")

    constitution = (CURSOR / "rules" / "全局.mdc").read_text(encoding="utf-8")
    if "不预展开" not in constitution:
        fail(errors, "全局.mdc 未写职种不预展开")
    if "current.md" not in constitution:
        fail(errors, "全局.mdc 未写现行卡")

    rc = run_py(SCRIPTS / "刷新菜单.py", [], root)
    if rc.returncode != 0:
        fail(errors, f"刷新菜单 rc={rc.returncode} {rc.stderr.strip()}")
        _done(errors)
        return 2

    catalog = json.loads((HARNESS / "catalog.json").read_text(encoding="utf-8"))
    if "generated_at" in catalog:
        fail(errors, "菜单含 generated_at")
    sys.path.insert(0, str(SCRIPTS))
    from 目录夹具 import first_craft_path, first_skill_mcp, path_mcps

    skills = {x["id"]: x for x in catalog.get("skills") or []}
    mcps = {x["id"] for x in catalog.get("mcp") or []}
    if "write-isolation" not in skills:
        fail(errors, "菜单无 write-isolation")
    sid, mid = first_skill_mcp(catalog)
    if not sid or mid not in mcps:
        fail(errors, "菜单缺带 needs_mcp 的技能或外接")
    cid, uses = first_craft_path(catalog)
    if not cid:
        fail(errors, "菜单缺带 uses_skills 的职种")
    first = uses[0]
    hidden = path_mcps(catalog, uses)

    probe = root / ".harness" / "sessions" / PROBE
    probe.mkdir(parents=True, exist_ok=True)
    (probe / "loadplan.json").write_text(
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
                        "why": "整接：只点职种时不得预展开路径外接。",
                    }
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    rc = run_py(SCRIPTS / "生成会话能力名单.py", [PROBE], root)
    if rc.returncode != 0:
        fail(errors, f"生成名单 {PROBE} rc={rc.returncode} {rc.stderr.strip()}")
    else:
        act = json.loads((probe / "activated.json").read_text(encoding="utf-8"))
        if act.get("skills"):
            fail(errors, f"职种点名不应预展开 skills={act.get('skills')}")
        leaked = set(hidden) & set(act.get("mcp_allow") or [])
        if leaked:
            fail(errors, f"职种点名不应预展开 {sorted(leaked)}")
        opened = (act.get("craft_open") or {}).get(cid)
        if first and opened != first:
            fail(errors, f"craft_open={opened} 期望 {first}")
        if not (probe / "current.md").is_file():
            fail(errors, "探测会话缺 current.md")

    live = ""
    latest = root / ".harness" / "sessions" / "LATEST"
    if latest.is_file():
        live = latest.read_text(encoding="utf-8").strip()
    if live.startswith("_") or not (root / ".harness" / "sessions" / live / "loadplan.json").is_file():
        live = ""
        sessions = root / ".harness" / "sessions"
        if sessions.is_dir():
            for child in sorted(sessions.iterdir()):
                if child.is_dir() and not child.name.startswith("_") and (child / "loadplan.json").is_file():
                    live = child.name
    live_plan = root / ".harness" / "sessions" / live / "loadplan.json" if live else Path()
    if not live_plan.is_file():
        fail(errors, "缺正式会话 loadplan（LATEST 或非探测会话）")
    else:
        rc = run_py(SCRIPTS / "生成会话能力名单.py", [live], root)
        if rc.returncode != 0:
            fail(errors, f"生成名单 {live} rc={rc.returncode} {rc.stderr.strip()}")
        else:
            act = json.loads((live_plan.parent / "activated.json").read_text(encoding="utf-8"))
            if not act.get("ok"):
                fail(errors, f"名单 errors={act.get('errors')}")
            if not (live_plan.parent / "current.md").is_file():
                fail(errors, "正式会话缺 current.md")
            state = json.loads((root / ".harness" / "state.json").read_text(encoding="utf-8"))
            if state.get("session_id") != live:
                fail(errors, f"当前行 session_id={state.get('session_id')}")
            tasks = (root / ".harness" / "memory" / "tasks.jsonl").read_text(encoding="utf-8")
            if live not in tasks:
                fail(errors, "任务流水未记本会话")
            rc = run_py(SCRIPTS / "建议执行单.py", [live, "--force"], root)
            if rc.returncode != 0:
                fail(errors, f"建议执行单 rc={rc.returncode} {rc.stderr.strip()}")
            elif not (live_plan.parent / "flow.json").is_file():
                fail(errors, "缺 flow.json")

    boot = run_py(
        HOOKS / "开场.py",
        [],
        root,
        stdin=json.dumps({"workspace_roots": [str(root)]}),
    )
    if boot.returncode != 0:
        fail(errors, f"开场 rc={boot.returncode} {boot.stderr.strip()}")
    else:
        try:
            line = [ln for ln in (boot.stdout or "").splitlines() if ln.startswith("{")]
            payload = json.loads(line[-1] if line else boot.stdout)
            env = payload.get("env") or {}
            ctx = payload.get("additional_context") or ""
        except (json.JSONDecodeError, IndexError):
            fail(errors, f"开场输出无效 {boot.stdout!r}")
        else:
            if env.get("HARNESS_L1") != "1":
                fail(errors, "开场未标 HARNESS_L1")
            if not env.get("HARNESS_STATE"):
                fail(errors, "开场未给 HARNESS_STATE")
            if env.get("HARNESS_SESSION") != live:
                fail(errors, f"开场会话={env.get('HARNESS_SESSION')} 期望 {live}")
            if not env.get("HARNESS_CURRENT_CARD"):
                fail(errors, "开场未给 HARNESS_CURRENT_CARD")
            if not env.get("HARNESS_SURFACES"):
                fail(errors, "开场未给 HARNESS_SURFACES")
            if "开场读序" not in ctx or "现行卡" not in ctx:
                fail(errors, "开场未注入现行卡摘要")

    for sub in ("canon", "adr", "status"):
        (root / ".harness" / "memory" / sub).mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(HOOKS))
    from 工作区 import find_workspace
    from 校验验证报告 import validate_report

    if find_workspace(root) != root.resolve():
        fail(errors, "find_workspace 未落到业务根")
    sample = {
        "bead_id": live or "session",
        "verify_kind": "schema",
        "command": "整接",
        "exit_code": 0,
        "evidence_paths": ["x"],
        "verdict": "pass",
    }
    verrs = validate_report(sample)
    if verrs:
        fail(errors, f"验证报告校验 {verrs}")

    return _done(errors)


def _done(errors: list[str]) -> int:
    if errors:
        for e in errors:
            print("error:", e, file=sys.stderr)
        return 2
    print("ok L1-L4 join")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
