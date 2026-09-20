# -*- coding: utf-8 -*-
"""Accept that the architecture landed. Hosts and MCP health are not required."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NEED_SKILLS = ("route-task", "write-isolation", "doctor", "verify-gate", "mcp-autostart")
NEED_HOOKS = ("开场.py", "结束.py", "工作区.py", "命令前.py", "读文件前.py")
NEED_SCRIPTS = (
    "刷新菜单.py",
    "生成会话能力名单.py",
    "项目库.py",
    "目录夹具.py",
    "接线自检.py",
    "应用外接档位.py",
    "拉起外接.py",
)
USER_PATH = re.compile(r"[A-Za-z]:\\Users\\(?!\$\{)[A-Za-z0-9._-]+")
DRIVE_HOST = re.compile(r"[A-Za-z]:\\Harness-Apps|[A-Za-z]:/Harness-Apps")
SECRET_A = re.compile(r'"-a",\s*"[A-Za-z0-9]{16,}"')
SECRET_LIKE = re.compile(r"\b(ghp_|github_pat_|sk-)[A-Za-z0-9_\-]{16,}")


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--workspace")
    p.add_argument("--cursor-home", default=str(Path.home() / ".cursor"))
    p.add_argument("--cursor-only", action="store_true")
    p.add_argument("--pack-root", default=str(Path(__file__).resolve().parent))
    args = p.parse_args()
    if not args.cursor_only and not args.workspace:
        print("need --workspace or --cursor-only", file=sys.stderr)
        return 2

    cursor = Path(args.cursor_home)
    errors: list[str] = []

    l1 = cursor / "rules" / "全局.mdc"
    if not l1.is_file():
        fail(errors, f"missing {l1}")
    else:
        text = l1.read_text(encoding="utf-8")
        if "开场读序" not in text:
            fail(errors, "L1 未写开场读序")
        if "不预展开" not in text:
            fail(errors, "L1 未写不预展开")

    for sid in NEED_SKILLS:
        path = cursor / "skills" / sid / "SKILL.md"
        if not path.is_file():
            fail(errors, f"missing skill {sid}")

    crafts = list((cursor / "agents").glob("*.md")) if (cursor / "agents").is_dir() else []
    if len(crafts) < 1:
        fail(errors, "missing crafts in agents/")

    for name in NEED_HOOKS:
        if not (cursor / "hooks" / name).is_file():
            fail(errors, f"missing hook {name}")
    if not (cursor / "hooks.json").is_file():
        fail(errors, "missing hooks.json")

    for name in NEED_SCRIPTS:
        if not (cursor / "harness" / "scripts" / name).is_file():
            fail(errors, f"missing script {name}")

    if not (cursor / "harness" / "mcp-boot" / "lazy_stdio.py").is_file():
        fail(errors, "missing mcp-boot/lazy_stdio.py")
    if not (cursor / "harness" / "mcp-tiers.json").is_file():
        fail(errors, "missing mcp-tiers.json")
    else:
        tiers = json.loads((cursor / "harness" / "mcp-tiers.json").read_text(encoding="utf-8"))
        if "excelMCP" not in (tiers.get("core") or []):
            fail(errors, "mcp-tiers core 缺 excelMCP")
        lazy = Path((tiers.get("boot") or {}).get("lazy_stdio") or "")
        if lazy.as_posix() and not lazy.is_file():
            fail(errors, f"boot.lazy_stdio missing {lazy}")

    catalog = cursor / "harness" / "catalog.json"
    if not catalog.is_file():
        fail(errors, "missing catalog.json；先跑安装器或 刷新菜单.py")
    else:
        data = json.loads(catalog.read_text(encoding="utf-8"))
        skills = {x["id"] for x in data.get("skills") or []}
        for sid in NEED_SKILLS:
            if sid not in skills:
                fail(errors, f"catalog 缺 skill {sid}")
        if not any((x.get("uses_skills") or []) for x in data.get("crafts") or []):
            fail(errors, "catalog 没有任何带 uses_skills 的职种")

    pack = Path(args.pack_root)
    scan_roots = [pack / "payload", pack / "install.py", pack / "verify_install.py", pack / "README.md"]
    for root in scan_roots:
        paths = [root] if root.is_file() else list(root.rglob("*")) if root.is_dir() else []
        for path in paths:
            if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".py", ".mdc", ".example"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if USER_PATH.search(text):
                fail(errors, f"{path.as_posix()} still has a machine user path")
            if DRIVE_HOST.search(text):
                fail(errors, f"{path.as_posix()} still has a hard-coded host root")
            if SECRET_A.search(text) or SECRET_LIKE.search(text):
                fail(errors, f"{path.as_posix()} still looks like a live secret")

    example = pack / "payload" / "L3-mcp" / "mcp.json.example"
    if example.is_file():
        text = example.read_text(encoding="utf-8")
        if "-a" in text and "${LARK_APP_ID}" not in text:
            fail(errors, "mcp.json.example 的 -a 未换成占位符")

    if args.workspace:
        root = Path(args.workspace)
        for rel in (
            ".harness/state.json",
            ".harness/surfaces.json",
            ".harness/memory/canon/四层运行口径.md",
            ".harness/memory/canon/四层封版.md",
        ):
            if not (root / rel).is_file():
                fail(errors, f"workspace missing {rel}")

    if errors:
        for e in errors:
            print("error:", e, file=sys.stderr)
        return 2
    print("ok architecture install")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
