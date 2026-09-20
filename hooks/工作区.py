#!/usr/bin/env python3
"""任务根与会话路口（加载计划 / 会话能力名单 / 验证结论）。"""
from __future__ import annotations

import json
import os
from pathlib import Path

MARKERS = (".harness",)


def find_workspace(cwd: str | Path | None = None) -> Path | None:
    candidates: list[Path] = []
    if cwd:
        candidates.append(Path(cwd))
    candidates.append(Path.cwd())
    env = os.environ.get("CURSOR_PROJECT_DIR") or os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        candidates.append(Path(env))
    root_env = os.environ.get("HARNESS_ROOT")
    if root_env:
        candidates.append(Path(root_env))
    for cur in candidates:
        try:
            cur = cur.resolve()
        except OSError:
            continue
        if cur.is_file():
            cur = cur.parent
        for p in [cur, *cur.parents]:
            if any((p / m).exists() for m in MARKERS):
                return p
    return None


def _cursor_home() -> Path:
    env = os.environ.get("CURSOR_HOME")
    if env:
        return Path(env)
    isolate = os.environ.get("GSH_ISOLATE_ROOT")
    if isolate:
        return Path(isolate) / "cursor"
    return Path.home() / ".cursor"


CURSOR_HOME = _cursor_home()


def latest_session_id(root: Path) -> str | None:
    """以 LATEST 为准，避免 Cursor 冻结的 HARNESS_SESSION 盖住当前会话。探测会话不进指针。"""
    latest = root / ".harness" / "sessions" / "LATEST"
    if latest.is_file():
        sid = latest.read_text(encoding="utf-8").strip()
        if sid and not sid.startswith("_"):
            return sid
    env_sid = (os.environ.get("HARNESS_SESSION") or "").strip()
    if env_sid and not env_sid.startswith("_"):
        return env_sid
    return None


def session_dir(root: Path, session_id: str | None = None) -> Path | None:
    sid = session_id or latest_session_id(root)
    if not sid:
        return None
    return root / ".harness" / "sessions" / sid


def loadplan_path(root: Path, session_id: str | None = None) -> Path | None:
    d = session_dir(root, session_id)
    return None if d is None else d / "loadplan.json"


def activated_path(root: Path, session_id: str | None = None) -> Path | None:
    d = session_dir(root, session_id)
    return None if d is None else d / "activated.json"


def read_activated(root: Path, session_id: str | None = None) -> dict | None:
    path = activated_path(root, session_id)
    if path is None or not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def verify_report_path(root: Path, bead_id: str) -> Path:
    return root / ".harness" / "artifacts" / bead_id / "verify-report.json"


def read_verify_report(root: Path, bead_id: str) -> dict | None:
    path = verify_report_path(root, bead_id)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def verdict_is_pass(report: dict | None) -> bool:
    if not report:
        return False
    raw = report.get("verdict")
    if raw is None and "结论" in report:
        raw = report.get("结论")
    text = str(raw or "").strip().lower()
    return text in {"pass", "通过", "ok", "true"}


def session_env(root: Path | None) -> dict[str, str]:
    env = {"HARNESS_L1": "1"}
    if root is None:
        return env
    env["HARNESS_ROOT"] = str(root)
    sid = latest_session_id(root)
    if not sid:
        env["HARNESS_ACTIVATED_OK"] = "0"
        return env
    env["HARNESS_SESSION"] = sid
    sdir = session_dir(root, sid)
    if sdir is not None:
        env["HARNESS_SESSION_DIR"] = str(sdir)
        env["HARNESS_LOADPLAN"] = str(sdir / "loadplan.json")
        env["HARNESS_ACTIVATED"] = str(sdir / "activated.json")
        card = sdir / "current.md"
        if card.is_file():
            env["HARNESS_CURRENT_CARD"] = str(card)
    surfaces = root / ".harness" / "surfaces.json"
    if surfaces.is_file():
        env["HARNESS_SURFACES"] = str(surfaces)
    env["HARNESS_READ_ORDER"] = "l1,current-card,named-skills"
    activated = read_activated(root, sid)
    env["HARNESS_ACTIVATED_OK"] = "1" if activated and activated.get("ok") is not False else "0"
    if activated and activated.get("write_class"):
        env["HARNESS_WRITE_CLASS"] = str(activated["write_class"])
    bead = (activated or {}).get("bead_id")
    if bead:
        env["HARNESS_BEAD"] = str(bead)
        env["HARNESS_VERIFY_REPORT"] = str(verify_report_path(root, str(bead)))
    crafts = (activated or {}).get("crafts") or []
    if crafts:
        env["HARNESS_CRAFTS"] = ",".join(str(x) for x in crafts)
    opened = (activated or {}).get("craft_open") or {}
    if opened:
        env["HARNESS_CRAFT_OPEN"] = ",".join(f"{k}->{v}" for k, v in opened.items())
    state = root / ".harness" / "state.json"
    env["HARNESS_STATE"] = str(state)
    if state.is_file():
        try:
            row = json.loads(state.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            row = {}
        if isinstance(row, dict) and row.get("progress"):
            env["HARNESS_PROGRESS"] = str(row["progress"])
    return env


def session_boot_context(root: Path | None, limit: int = 1800) -> str:
    """开场注入：读序 + 现行卡正文，不灌菜单全文。"""
    lines = [
        "开场读序：第一层规则 → 现行卡 → 点名技能/职种正文。",
        "catalog.json 是导演点名菜单，用 `python -m gsh menu` 查 id，不要把菜单全文贴进对话。",
        "续上：`python -m gsh status` / `python -m gsh resume`。职种前进：`python -m gsh next`。收口：`python -m gsh close`。",
        "写正式面前先走隔离根。",
    ]
    if root is None:
        lines.append("业务根未找到，先定档。")
        return "\n".join(lines)
    sid = latest_session_id(root)
    surfaces = root / ".harness" / "surfaces.json"
    if surfaces.is_file():
        lines.append(f"正式面地图: {surfaces}")
    if not sid:
        lines.append("无现行会话。先写加载计划并生成名单。")
        return "\n".join(lines)
    lines.append(f"现行会话: {sid}")
    sdir = session_dir(root, sid)
    card = None if sdir is None else sdir / "current.md"
    if card is not None and card.is_file():
        text = card.read_text(encoding="utf-8").strip()
        if len(text) > limit:
            text = text[:limit] + "\n…"
        lines.append("现行卡:")
        lines.append(text)
    else:
        lines.append("缺现行卡 current.md。先生成名单或手写后再制作。")
    activated = read_activated(root, sid) or {}
    named = []
    for key in ("skills", "crafts"):
        for iid in activated.get(key) or []:
            named.append(f"{key}:{iid}")
    if named:
        lines.append("已点名: " + ", ".join(named))
    opened = activated.get("craft_open") or {}
    if opened:
        lines.append("职种当前步: " + ", ".join(f"{k}→{v}" for k, v in opened.items()))
    paths = activated.get("craft_path") or {}
    if isinstance(paths, dict) and paths:
        bits = []
        for cid, row in paths.items():
            if not isinstance(row, dict):
                continue
            steps = row.get("steps") or []
            if not steps:
                continue
            n = int(row.get("index") or 0) + 1
            bits.append(f"{cid} {n}/{len(steps)}")
        if bits:
            lines.append("职种进度: " + ", ".join(bits))
    keys = activated.get("retrieve_keys") or []
    if keys:
        lines.append("记忆键: " + ", ".join(str(x) for x in keys))
    return "\n".join(lines)


def write_latest(root: Path, session_id: str) -> None:
    d = root / ".harness" / "sessions"
    d.mkdir(parents=True, exist_ok=True)
    (d / "LATEST").write_text(session_id.strip() + "\n", encoding="utf-8")


def list_skill_ids() -> list[str]:
    root = CURSOR_HOME / "skills"
    if not root.is_dir():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())


def list_agent_ids() -> list[str]:
    root = CURSOR_HOME / "agents"
    if not root.is_dir():
        return []
    return sorted(p.stem for p in root.iterdir() if p.is_file() and p.suffix.lower() == ".md")


def list_mcp_json_ids() -> list[str]:
    path = CURSOR_HOME / "mcp.json"
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    servers = data.get("mcpServers") or data.get("servers") or {}
    return sorted(servers) if isinstance(servers, dict) else []


def find_scripts_dir(root: Path | None = None) -> Path | None:
    """定位闸/名单脚本：本 hooks 目录 → HARNESS_SCRIPTS → ~/.cursor/scripts → 业务仓 scripts。"""
    marker = "校验验证报告.py"
    hooks = Path(__file__).resolve().parent
    if (hooks / marker).is_file():
        return hooks
    env = (os.environ.get("HARNESS_SCRIPTS") or "").strip()
    if env:
        p = Path(env)
        if (p / marker).is_file():
            return p
    user_scripts = CURSOR_HOME / "scripts"
    if (user_scripts / marker).is_file():
        return user_scripts
    if root is not None:
        for cand in (root / ".harness" / "scripts", root / "scripts"):
            if (cand / marker).is_file():
                return cand
    return None
