# -*- coding: utf-8 -*-
"""四层互相握手：宪法 → 定档名单 → 菜单职种 → 现行卡/当前行/开场。"""
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
    HOOKS = _h.cursor / "hooks"
    SCRIPTS = harness_scripts(_h)
except Exception:
    CURSOR = Path.home() / ".cursor"
    HARNESS = CURSOR / "harness"
    HOOKS = CURSOR / "hooks"
    SCRIPTS = HARNESS / "scripts"
PY = sys.executable
PROBE = "_hs-craft"


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

    l1 = (CURSOR / "rules" / "全局.mdc").read_text(encoding="utf-8")
    if "开场读序" not in l1 or "不预展开" not in l1:
        errors.append("L1 未写开场读序或不预展开")
    banned = ("<studio-project>", "<tables-root>", "<FRAMEWORK_ROOT>", "<user-slug>")
    for path in (
        CURSOR / "rules" / "全局.mdc",
        CURSOR / "skills" / "route-task" / "SKILL.md",
        CURSOR / "skills" / "write-isolation" / "SKILL.md",
        CURSOR / "skills" / "file-pack-layout" / "SKILL.md",
        CURSOR / "skills" / "mcp-autostart" / "SKILL.md",
        CURSOR / "skills" / "data-readiness-check" / "SKILL.md",
    ):
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        hit = [b for b in banned if b in text]
        if hit:
            errors.append(f"{path.name} 仍含项目专名 {hit}")
    if (HOOKS / "外接前.py").is_file():
        errors.append("废弃钩子 外接前.py 仍在")
    if ".beads" in (HOOKS / "工作区.py").read_text(encoding="utf-8").split("MARKERS", 1)[-1][:80]:
        errors.append("工作区仍以 .beads 为业务根标记")
    hook_flow = (HOOKS / "建议执行单.py").read_text(encoding="utf-8")
    if '"stages"' in hook_flow:
        errors.append("hooks/建议执行单.py 仍是旧 stages 口径")

    rc = run_py(SCRIPTS / "刷新菜单.py", [], root)
    if rc.returncode != 0:
        errors.append(f"刷新菜单 rc={rc.returncode}")
        _done(errors)
        return 2
    catalog = json.loads((HARNESS / "catalog.json").read_text(encoding="utf-8"))
    sys.path.insert(0, str(SCRIPTS))
    from 目录夹具 import first_craft_path, path_mcps

    skills = {x["id"] for x in catalog.get("skills") or []}
    for need in ("route-task", "write-isolation", "doctor", "verify-gate"):
        if need not in skills:
            errors.append(f"L3 菜单缺 {need}")
    cid, uses = first_craft_path(catalog)
    if not cid:
        errors.append("菜单缺带 uses_skills 的职种")
        _done(errors)
        return 2
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
                "items": [
                    {
                        "kind": "craft",
                        "id": cid,
                        "why": "握手：职种点名不得预展开路径。",
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
        errors.append(f"生成探测名单 rc={rc.returncode} {rc.stderr.strip()}")
    else:
        act = json.loads((probe / "activated.json").read_text(encoding="utf-8"))
        leaked = set(hidden) & set(act.get("mcp_allow") or [])
        if act.get("skills") or leaked:
            errors.append("L2→L3 握手失败：职种被预展开")
        if first and (act.get("craft_open") or {}).get(cid) != first:
            errors.append("L2→L3 握手失败：craft_open 不是路径第一步")
        if not (probe / "current.md").is_file():
            errors.append("L2→L4 握手失败：未写现行卡")

    latest = (root / ".harness" / "sessions" / "LATEST").read_text(encoding="utf-8").strip()
    if latest.startswith("_"):
        errors.append(f"探测会话写入了 LATEST={latest}")
    live_card = root / ".harness" / "sessions" / latest / "current.md"
    if latest and not live_card.is_file():
        errors.append(f"L4 现行卡缺失 {latest}")

    boot = run_py(
        HOOKS / "开场.py",
        [],
        root,
        stdin=json.dumps({"workspace_roots": [str(root)]}),
    )
    if boot.returncode != 0:
        errors.append(f"开场 rc={boot.returncode}")
    else:
        line = [ln for ln in (boot.stdout or "").splitlines() if ln.startswith("{")]
        try:
            payload = json.loads(line[-1] if line else boot.stdout)
        except (json.JSONDecodeError, IndexError):
            errors.append("开场输出不是 JSON")
        else:
            env = payload.get("env") or {}
            ctx = payload.get("additional_context") or ""
            if env.get("HARNESS_L1") != "1":
                errors.append("L1→开场 未标 HARNESS_L1")
            if env.get("HARNESS_SESSION") != latest:
                errors.append(f"开场会话 {env.get('HARNESS_SESSION')} 与 LATEST {latest} 不一致")
            if "现行卡" not in ctx or latest not in ctx:
                errors.append("开场未注入现行卡（L4→开场 握手失败）")
            if not env.get("HARNESS_SURFACES"):
                errors.append("开场未指向正式面地图")

    surfaces = json.loads((root / ".harness" / "surfaces.json").read_text(encoding="utf-8"))
    if not surfaces.get("surfaces"):
        errors.append("L4 surfaces 空")
    state = json.loads((root / ".harness" / "state.json").read_text(encoding="utf-8"))
    if latest and latest not in (state.get("sessions") or {}) and state.get("session_id") != latest:
        errors.append("当前行未记录现行会话")
    canon = root / ".harness" / "memory" / "canon" / "四层运行口径.md"
    if not canon.is_file():
        errors.append("缺已批准四层口径")

    health = HARNESS / "mcp-health.json"
    if health.is_file():
        rows = json.loads(health.read_text(encoding="utf-8")).get("rows") or []
        bad = [r.get("id") for r in rows if r.get("ok") is False]
        if bad:
            errors.append(f"外接健康失败: {bad}")

    return _done(errors)


def _done(errors: list[str]) -> int:
    if errors:
        for e in errors:
            print("error:", e, file=sys.stderr)
        return 2
    print("ok four-layer handshake")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
