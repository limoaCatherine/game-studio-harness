#!/usr/bin/env python3
"""命令执行前：破坏类须确认；关项读验证结论。"""
from __future__ import annotations

import json
import os
import re
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from 工作区 import find_workspace, find_scripts_dir, read_activated, read_verify_report, verdict_is_pass, verify_report_path

CLOSE_PREFIX = {"bd", "just"}
SKIP_CLOSE = {"close", "bd", "just"}
NESTED_RE = re.compile(
    r"(?i)(?:bash|sh|zsh|pwsh|powershell)(?:\.exe)?\s+(?:-c|-Command)\s+(?P<q>[\"'])(?P<body>.*?)(?P=q)"
)


def out(permission: str, user: str = "", agent: str = "") -> None:
    payload = {"permission": permission}
    if user:
        payload["user_message"] = user
    if agent:
        payload["agent_message"] = agent
    print(json.dumps(payload, ensure_ascii=False))


def tokenize(command: str) -> list[str]:
    if not command or not str(command).strip():
        return []
    raw = str(command)
    try:
        posix_argv = shlex.split(raw, posix=True)
    except ValueError:
        posix_argv = None
    try:
        win_argv = shlex.split(raw, posix=False)
    except ValueError:
        win_argv = None
    low = raw.lower()
    if any(k in low for k in ("bash ", "bash\t", "sh ", "zsh ", "git ", "git\t")):
        return posix_argv or win_argv or raw.split()
    return win_argv or posix_argv or raw.split()


def is_git(token: str) -> bool:
    base = Path(token.replace("\\", "/")).name.lower()
    return base in {"git", "git.exe"}


def git_destructive_reason(argv: list[str]) -> str | None:
    lower = [a.lower() for a in argv]
    for i, _tok in enumerate(lower):
        if not is_git(argv[i]):
            continue
        rest = lower[i + 1 :]
        if not rest:
            continue
        if rest[0] == "push" and any(
            x in {"--force", "-f", "--force-with-lease"} or x.startswith("--force-with-lease=")
            for x in rest[1:]
        ):
            return "受保护分支强推：请确认后再执行"
        if rest[0] == "reset" and "--hard" in rest[1:]:
            return "硬重置：请确认后再执行"
        if rest[0] == "clean":
            for flag in rest[1:]:
                if flag.startswith("-") and not flag.startswith("--") and "x" in flag[1:]:
                    return "清空未跟踪：请确认后再执行"
                if flag in {"-x", "-fx", "-xf", "-fdx", "-fxd", "-dfx"}:
                    return "清空未跟踪：请确认后再执行"
    return None


def nested_payloads(argv: list[str], command: str) -> list[str]:
    found: list[str] = []
    for i, tok in enumerate(argv):
        if tok in {"-c", "-Command", "/c", "-EncodedCommand"} and i + 1 < len(argv):
            found.append(argv[i + 1])
    for m in NESTED_RE.finditer(command or ""):
        found.append(m.group("body"))
    seen: set[str] = set()
    uniq: list[str] = []
    for item in found:
        if item not in seen:
            seen.add(item)
            uniq.append(item)
    return uniq


def scan_destructive(command: str, depth: int = 0) -> str | None:
    argv = tokenize(command)
    reason = git_destructive_reason(argv)
    if reason:
        return reason
    if depth >= 2:
        return None
    for payload in nested_payloads(argv, command):
        reason = scan_destructive(payload, depth + 1)
        if reason:
            return reason
    return None


def is_close_command(argv: list[str]) -> bool:
    lower = [a.lower() for a in argv]
    for i, tok in enumerate(lower):
        if tok == "close" and i > 0 and lower[i - 1] in CLOSE_PREFIX:
            return True
        if tok in {"bd-close", "just-close"}:
            return True
    return False


def close_bead_id(argv: list[str], command: str) -> str | None:
    m = re.search(r"(?i)\bBEAD=([^\s]+)", command)
    if m:
        return m.group(1)
    lower = [a.lower() for a in argv]
    for i, tok in enumerate(lower):
        if tok == "close" and i > 0 and lower[i - 1] in CLOSE_PREFIX:
            if i + 1 < len(argv):
                cand = argv[i + 1]
                if cand.lower() not in SKIP_CLOSE and not cand.startswith("-"):
                    return cand
        if tok.startswith("bead="):
            return argv[i].split("=", 1)[1]
    return None


def check_close(cwd: str, argv: list[str], command: str) -> tuple[str, str] | None:
    root = find_workspace(cwd) or Path(cwd).resolve()
    bead = close_bead_id(argv, command)
    if not bead:
        activated = read_activated(root)
        bead = (activated or {}).get("bead_id")
    if not bead:
        msg = "关项须带工作项编号（或会话能力名单里已有 bead_id），并先写出验证结论且为通过"
        return msg, msg
    bead = str(bead)
    report_path = verify_report_path(root, bead)
    data = read_verify_report(root, bead)
    if data is None:
        msg = f"关项前先写出验证结论：{report_path.as_posix()}，且为通过"
        return msg, msg
    try:
        from 校验验证报告 import validate_report
    except ImportError:
        scripts = find_scripts_dir(root if isinstance(root, Path) else Path(str(root)))
        if scripts is not None and str(scripts) not in sys.path:
            sys.path.insert(0, str(scripts))
        try:
            from 校验验证报告 import validate_report  # type: ignore
        except Exception as e:
            msg = f"无法校验验证报告字段（{e}），确认 ~/.cursor/hooks/校验验证报告.py 可用"
            return msg, msg
    verrs = validate_report(data)
    if verrs:
        msg = f"验证报告字段不合规，先修 {report_path.as_posix()}：{verrs}"
        return msg, msg
    if not verdict_is_pass(data):
        msg = f"验证结论须为通过后再关项（当前：{data.get('verdict')!r}）"
        return msg, msg
    return None


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        out("allow")
        return

    command = payload.get("command") or ""
    cwd = payload.get("cwd") or "."
    argv = tokenize(command)

    if is_close_command(argv):
        blocked = check_close(cwd, argv, command)
        if blocked:
            out("deny", blocked[0], blocked[1])
            return

    reason = scan_destructive(command)
    if reason:
        out("ask", reason, reason)
        return

    out("allow")


if __name__ == "__main__":
    main()
