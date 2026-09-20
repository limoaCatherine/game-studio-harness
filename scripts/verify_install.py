# -*- coding: utf-8 -*-
"""Accept that the architecture landed on the selected tool homes. Hosts are not required."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
if str(PACK / "cursor" / "harness" / "scripts") not in sys.path:
    sys.path.insert(0, str(PACK / "cursor" / "harness" / "scripts"))
from gsh_paths import homes_from_env  # noqa: E402

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
    "gsh_paths.py",
)
USER_PATH = re.compile(r"[A-Za-z]:\\Users\\(?!\$\{)[A-Za-z0-9._-]+")
DRIVE_HOST = re.compile(r"[A-Za-z]:\\Harness-Apps|[A-Za-z]:/Harness-Apps")
SECRET_A = re.compile(r'"-a",\s*"[A-Za-z0-9]{16,}"')
SECRET_LIKE = re.compile(r"\b(ghp_|github_pat_|sk-)[A-Za-z0-9_\-]{16,}")
ALL_TOOLS = ("cursor", "claude", "codex", "grok", "deepseek")


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def parse_tools(raw: str) -> list[str]:
    if raw.strip().lower() in {"all", "*"}:
        return list(ALL_TOOLS)
    out = []
    aliases = {
        "claudecode": "claude",
        "claude-code": "claude",
        "grokbot": "grok",
        "deepseekharness": "deepseek",
        "dsh": "deepseek",
    }
    for part in raw.replace(";", ",").split(","):
        name = aliases.get(part.strip().lower(), part.strip().lower())
        if name in ALL_TOOLS and name not in out:
            out.append(name)
    return out or list(ALL_TOOLS)


def check_skill_tree(root: Path, errors: list[str], label: str) -> None:
    for sid in NEED_SKILLS:
        if not (root / sid / "SKILL.md").is_file():
            fail(errors, f"{label} missing skill {sid}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--workspace")
    p.add_argument("--tools", default="all")
    p.add_argument("--isolate-root")
    p.add_argument("--cursor-home")
    p.add_argument("--cursor-only", action="store_true")
    p.add_argument("--pack-root", default=str(PACK))
    args = p.parse_args()
    if not args.cursor_only and not args.workspace:
        print("need --workspace or --cursor-only", file=sys.stderr)
        return 2

    isolate = Path(args.isolate_root) if args.isolate_root else None
    h = homes_from_env(isolate)
    tools = parse_tools(args.tools)
    errors: list[str] = []

    if not (h.gsh / "AGENTS.md").is_file():
        fail(errors, f"missing shared constitution {h.gsh / 'AGENTS.md'}")
    check_skill_tree(h.gsh_skills, errors, "gsh")
    if not list(h.gsh_agents.glob("*.md")):
        fail(errors, "missing crafts in ~/.gsh/agents")
    for name in NEED_SCRIPTS:
        if not (h.gsh_harness / "scripts" / name).is_file():
            fail(errors, f"missing script {name}")
    if not (h.gsh_harness / "mcp-boot" / "lazy_stdio.py").is_file():
        fail(errors, "missing mcp-boot/lazy_stdio.py")
    tiers = h.gsh_harness / "mcp-tiers.json"
    if not tiers.is_file():
        fail(errors, "missing mcp-tiers.json")
    else:
        data = json.loads(tiers.read_text(encoding="utf-8"))
        if "excelMCP" not in (data.get("core") or []):
            fail(errors, "mcp-tiers core 缺 excelMCP")

    catalog = h.gsh_harness / "catalog.json"
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

    if "cursor" in tools:
        l1 = h.cursor / "rules" / "全局.mdc"
        if not l1.is_file():
            fail(errors, f"missing {l1}")
        else:
            text = l1.read_text(encoding="utf-8")
            if "开场读序" not in text:
                fail(errors, "L1 未写开场读序")
            if "不预展开" not in text:
                fail(errors, "L1 未写不预展开")
        check_skill_tree(h.cursor / "skills", errors, "cursor")
        for name in NEED_HOOKS:
            if not (h.cursor / "hooks" / name).is_file():
                fail(errors, f"missing hook {name}")
        if not (h.cursor / "hooks.json").is_file():
            fail(errors, "missing hooks.json")
    if "claude" in tools:
        if not (h.claude / "CLAUDE.md").is_file():
            fail(errors, "missing Claude CLAUDE.md")
        check_skill_tree(h.claude / "skills", errors, "claude")
    if "codex" in tools:
        if not (h.codex / "AGENTS.md").is_file():
            fail(errors, "missing Codex AGENTS.md")
        check_skill_tree(h.agents_skills, errors, "codex/.agents/skills")
    if "grok" in tools:
        if not (h.grok / "AGENTS.md").is_file():
            fail(errors, "missing Grok AGENTS.md")
        check_skill_tree(h.grok / "skills", errors, "grok")
    if "deepseek" in tools:
        if not (h.dsh / "AGENTS.md").is_file():
            fail(errors, "missing DeepSeek ~/.dsh/AGENTS.md")
        check_skill_tree(h.dsh / "skills", errors, "deepseek")

    pack = Path(args.pack_root)
    for name in ALL_TOOLS:
        skill = pack / name / "skills" / "route-task" / "SKILL.md"
        if not skill.is_file():
            fail(errors, f"pack {name}/ is not complete (missing skills/route-task)")

    scan_roots = [
        pack / "cursor",
        pack / "claude",
        pack / "codex",
        pack / "grok",
        pack / "deepseek",
        pack / "docs",
        pack / "scripts" / "install.py",
        pack / "scripts" / "verify_install.py",
        pack / "README.md",
    ]
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

    example = pack / "cursor" / "mcp.json.example"
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
            "AGENTS.md",
            "CLAUDE.md",
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
