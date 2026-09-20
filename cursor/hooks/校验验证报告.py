#!/usr/bin/env python3
"""校验 .harness/artifacts/<工作项>/verify-report.json 字段。"""
from __future__ import annotations

KINDS = {"smoke", "schema", "playtest", "build", "release"}
VERDICTS = {"pass", "fail"}
REQUIRED = ("bead_id", "verify_kind", "command", "exit_code", "evidence_paths", "verdict")


def validate_report(data: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(data, dict):
        return ["验证报告须为对象"]
    for key in REQUIRED:
        if key not in data:
            errs.append(f"缺字段 {key}")
    bead = data.get("bead_id")
    if bead is not None and (not isinstance(bead, str) or not bead.strip()):
        errs.append("bead_id 须非空字符串")
    kind = data.get("verify_kind")
    if kind is not None and kind not in KINDS:
        errs.append(f"verify_kind 非法: {kind!r}")
    cmd = data.get("command")
    if cmd is not None and (not isinstance(cmd, str) or not cmd.strip()):
        errs.append("command 须非空字符串")
    code = data.get("exit_code")
    if code is not None and not isinstance(code, int):
        errs.append("exit_code 须为整数")
    paths = data.get("evidence_paths")
    if paths is not None:
        if not isinstance(paths, list) or not paths:
            errs.append("evidence_paths 须为非空字符串数组")
        elif any(not isinstance(p, str) or not p.strip() for p in paths):
            errs.append("evidence_paths 含空项")
    verdict = data.get("verdict")
    if verdict is not None and verdict not in VERDICTS:
        errs.append(f"verdict 非法: {verdict!r}")
    return errs
