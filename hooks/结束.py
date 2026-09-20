#!/usr/bin/env python3
"""会话结束：按结案路径检查验证结论；缺会话卡则提示交接。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from 工作区 import (
    find_scripts_dir,
    find_workspace,
    latest_session_id,
    read_activated,
    read_verify_report,
    session_dir,
    verdict_is_pass,
    verify_report_path,
)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}
    if payload.get("status") != "completed":
        print("{}")
        return

    roots = payload.get("workspace_roots") or []
    root = find_workspace(roots[0] if roots else None)
    out: dict = {}
    if root is None:
        print("{}")
        return

    sid = latest_session_id(root)
    if not sid:
        print("{}")
        return

    activated = read_activated(root, sid)
    bead = (activated or {}).get("bead_id")
    if bead:
        report = read_verify_report(root, str(bead))
        path = verify_report_path(root, str(bead))
        if report is not None:
            try:
                from 校验验证报告 import validate_report
            except ImportError:
                scripts = find_scripts_dir(root)
                if scripts is not None and str(scripts) not in sys.path:
                    sys.path.insert(0, str(scripts))
                try:
                    from 校验验证报告 import validate_report  # type: ignore
                except Exception:
                    validate_report = None  # type: ignore
            if validate_report is not None:
                verrs = validate_report(report)
                if verrs:
                    out["followup_message"] = (
                        f"结案未完成：工作项 {bead} 验证报告字段不合规：{verrs}。"
                        f"先修 {path.as_posix()}。"
                    )
                    print(json.dumps(out, ensure_ascii=False))
                    return
        if not verdict_is_pass(report):
            out["followup_message"] = (
                f"工作项 {bead} 还没有通过的验证报告。运行 "
                f"`python -m gsh close --kind smoke --evidence <产物路径>` "
                f"写出 {path.as_posix()} 后再关项。"
            )
            print(json.dumps(out, ensure_ascii=False))
            return

    sdir = session_dir(root, sid)
    card = None if sdir is None else sdir / "current.md"
    if card is not None and not card.is_file():
        out["followup_message"] = (
            "本会话缺现行卡。先生成名单或写出 current.md，再交接或关项。"
        )
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
