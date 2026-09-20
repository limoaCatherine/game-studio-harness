# -*- coding: utf-8 -*-
"""把本仓落到共享运行时 ~/.gsh，并适配 Cursor / Claude Code / Codex / Grok / DeepSeek Harness。
不安装任何 DCC，不写密钥，不覆盖已有 mcp.json。
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parent
CURSOR_SRC = PACK / "cursor"
WORKSPACE_SRC = PACK / "workspace-scaffold"
CONSTITUTION = PACK / "adapters" / "_shared" / "CONSTITUTION.md"
ALL_TOOLS = ("cursor", "claude", "codex", "grok", "deepseek")

if str(CURSOR_SRC / "harness" / "scripts") not in sys.path:
    sys.path.insert(0, str(CURSOR_SRC / "harness" / "scripts"))
from gsh_paths import Homes, homes_from_env  # noqa: E402


def copy_tree(src: Path, dst: Path, dry: bool, copied: list[str]) -> None:
    if not src.exists():
        return
    if src.is_file():
        if not dry:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        copied.append(f"{src.as_posix()} -> {dst.as_posix()}")
        return
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        if path.name == ".gitkeep":
            rel = path.relative_to(src)
            target = dst / rel.parent
            if not dry:
                target.mkdir(parents=True, exist_ok=True)
            continue
        rel = path.relative_to(src)
        target = dst / rel
        if not dry:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        copied.append(f"{path.as_posix()} -> {target.as_posix()}")


def merge_missing(src: Path, dst: Path, dry: bool, copied: list[str]) -> None:
    if not src.exists():
        return
    for path in src.rglob("*"):
        if path.is_dir() or path.name == ".gitkeep":
            if path.is_dir() and not dry:
                (dst / path.relative_to(src)).mkdir(parents=True, exist_ok=True)
            continue
        rel = path.relative_to(src)
        target = dst / rel
        if target.exists():
            continue
        if not dry:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        copied.append(f"new {path.as_posix()} -> {target.as_posix()}")


def write_text(path: Path, text: str, dry: bool, copied: list[str]) -> None:
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    copied.append(f"write {path.as_posix()}")


def constitution_text() -> str:
    return CONSTITUTION.read_text(encoding="utf-8")


def write_tiers(harness_dst: Path, dry: bool) -> None:
    src = CURSOR_SRC / "harness" / "mcp-tiers.json"
    raw = json.loads(src.read_text(encoding="utf-8"))
    boot_dir = harness_dst / "mcp-boot"
    raw["boot"] = {
        "cache": str(boot_dir / "cache"),
        "lazy_stdio": str(boot_dir / "lazy_stdio.py"),
    }
    dest = harness_dst / "mcp-tiers.json"
    if not dry:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def maybe_write_mcp(cursor: Path, write_mcp: bool, dry: bool) -> str:
    example = CURSOR_SRC / "mcp.json.example"
    dest_example = cursor / "mcp.json.example"
    if not dry:
        cursor.mkdir(parents=True, exist_ok=True)
        shutil.copy2(example, dest_example)
    live = cursor / "mcp.json"
    if live.is_file():
        return "kept existing mcp.json"
    if not write_mcp:
        return "wrote mcp.json.example only (pass --write-mcp to create empty-machine mcp.json)"
    if not dry:
        shutil.copy2(example, live)
    return "wrote mcp.json from example (no secrets, placeholders only)"


def refresh_catalog(h: Homes, dry: bool) -> str:
    script = h.gsh_harness / "scripts" / "刷新菜单.py"
    if dry:
        return "dry-run skip 刷新菜单"
    if not script.is_file():
        return "missing 刷新菜单.py"
    import importlib.util

    spec = importlib.util.spec_from_file_location("harness_refresh_catalog", script)
    if spec is None or spec.loader is None:
        return "cannot load 刷新菜单.py"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.CURSOR = h.cursor
    mod.SKILLS = h.gsh_skills
    mod.AGENTS = h.gsh_agents
    mod.HARNESS = h.gsh_harness
    mod.TOOLS = h.gsh_harness / "mcp-tools"
    mod.OUT = h.gsh_harness / "catalog.json"
    mcp_live = h.cursor / "mcp.json"
    mcp_example = h.gsh / "mcp.json.example"
    mod.MCP_JSON = mcp_live if mcp_live.is_file() else mcp_example
    rc = int(mod.main())
    if rc != 0:
        return f"刷新菜单 failed rc={rc}"
    catalog = h.gsh_harness / "catalog.json"
    if not catalog.is_file():
        return "刷新菜单 未写 catalog.json"
    cursor_out = h.cursor / "harness" / "catalog.json"
    if h.cursor.joinpath("harness").is_dir():
        cursor_out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(catalog, cursor_out)
    return f"wrote {catalog}"


def parse_tools(raw: str) -> list[str]:
    if raw.strip().lower() in {"all", "*"}:
        return list(ALL_TOOLS)
    out = []
    for part in raw.replace(";", ",").split(","):
        name = part.strip().lower()
        aliases = {
            "claudecode": "claude",
            "claude-code": "claude",
            "openai": "codex",
            "grokbot": "grok",
            "grok-build": "grok",
            "deepseekharness": "deepseek",
            "dsh": "deepseek",
        }
        name = aliases.get(name, name)
        if name not in ALL_TOOLS:
            raise SystemExit(f"unknown tool {part!r}; choose from {', '.join(ALL_TOOLS)}")
        if name not in out:
            out.append(name)
    if not out:
        raise SystemExit("need at least one --tools value")
    return out


def land_shared(h: Homes, dry: bool, copied: list[str]) -> None:
    copy_tree(CURSOR_SRC / "skills", h.gsh_skills, dry, copied)
    copy_tree(CURSOR_SRC / "agents", h.gsh_agents, dry, copied)
    copy_tree(CURSOR_SRC / "harness" / "scripts", h.gsh_harness / "scripts", dry, copied)
    copy_tree(CURSOR_SRC / "harness" / "surfaces.default.json", h.gsh_harness / "surfaces.default.json", dry, copied)
    copy_tree(CURSOR_SRC / "harness" / "mcp-tools", h.gsh_harness / "mcp-tools", dry, copied)
    copy_tree(CURSOR_SRC / "harness" / "docs", h.gsh_harness / "docs", dry, copied)
    copy_tree(CURSOR_SRC / "harness" / "mcp-boot", h.gsh_harness / "mcp-boot", dry, copied)
    copy_tree(CURSOR_SRC / "harness" / "host-paths.example.json", h.gsh_harness / "host-paths.example.json", dry, copied)
    copy_tree(CURSOR_SRC / "mcp.json.example", h.gsh / "mcp.json.example", dry, copied)
    write_tiers(h.gsh_harness, dry)
    write_text(h.gsh / "AGENTS.md", constitution_text(), dry, copied)


def land_cursor(h: Homes, write_mcp: bool, dry: bool, copied: list[str]) -> str:
    copy_tree(CURSOR_SRC / "rules", h.cursor / "rules", dry, copied)
    copy_tree(CURSOR_SRC / "skills", h.cursor / "skills", dry, copied)
    copy_tree(CURSOR_SRC / "agents", h.cursor / "agents", dry, copied)
    copy_tree(CURSOR_SRC / "hooks", h.cursor / "hooks", dry, copied)
    copy_tree(CURSOR_SRC / "hooks.json", h.cursor / "hooks.json", dry, copied)
    copy_tree(h.gsh_harness, h.cursor / "harness", dry, copied)
    return maybe_write_mcp(h.cursor, write_mcp, dry)


def land_instruction(path: Path, dry: bool, copied: list[str]) -> None:
    write_text(path, constitution_text(), dry, copied)


def land_other(h: Homes, tools: list[str], dry: bool, copied: list[str]) -> None:
    if "claude" in tools:
        copy_tree(h.gsh_skills, h.claude / "skills", dry, copied)
        copy_tree(h.gsh_agents, h.claude / "agents", dry, copied)
        land_instruction(h.claude / "CLAUDE.md", dry, copied)
    if "codex" in tools:
        copy_tree(h.gsh_skills, h.agents_skills, dry, copied)
        copy_tree(h.gsh_agents, h.codex / "agents", dry, copied)
        land_instruction(h.codex / "AGENTS.md", dry, copied)
    if "grok" in tools:
        copy_tree(h.gsh_skills, h.grok / "skills", dry, copied)
        copy_tree(h.gsh_agents, h.grok / "agents", dry, copied)
        land_instruction(h.grok / "AGENTS.md", dry, copied)
    if "deepseek" in tools:
        copy_tree(h.gsh_skills, h.dsh / "skills", dry, copied)
        copy_tree(h.gsh_skills, h.agents_skills, dry, copied)
        land_instruction(h.dsh / "AGENTS.md", dry, copied)


def land_workspace(root: Path, dry: bool, copied: list[str]) -> str:
    if not dry:
        root.mkdir(parents=True, exist_ok=True)
    merge_missing(WORKSPACE_SRC / ".harness", root / ".harness", dry, copied)
    text = constitution_text()
    write_text(root / "AGENTS.md", text, dry, copied)
    write_text(root / "CLAUDE.md", text, dry, copied)
    return f"scaffolded missing files under {root / '.harness'}"


def main() -> int:
    p = argparse.ArgumentParser(description="一键把 Game Studio Harness 落到多套 AI 编程工具")
    p.add_argument("--workspace", help="业务根（将放 .harness）")
    p.add_argument("--tools", default="all", help="cursor,claude,codex,grok,deepseek 或 all")
    p.add_argument("--cursor-home", help="兼容旧开关；请改用 --isolate-root")
    p.add_argument("--isolate-root", help="探测根：所有家目录改落到此树下，不写真实 ~/.cursor 等")
    p.add_argument("--cursor-only", action="store_true", help="不建业务根")
    p.add_argument("--write-mcp", action="store_true", help="仅当目标没有 mcp.json 时从示例创建")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if not CURSOR_SRC.is_dir():
        print("missing cursor/; clone the repo root and run from there", file=sys.stderr)
        return 2
    if not args.cursor_only and not args.workspace:
        print("need --workspace or --cursor-only", file=sys.stderr)
        return 2

    isolate = Path(args.isolate_root) if args.isolate_root else None
    if isolate is None and args.cursor_home:
        isolate = Path(args.cursor_home).parent / "_isolate_from_cursor_home"
        print("warning: --cursor-home is legacy; prefer --isolate-root", file=sys.stderr)
    h = homes_from_env(isolate)
    tools = parse_tools(args.tools)
    copied: list[str] = []
    dry = args.dry_run

    land_shared(h, dry, copied)
    mcp_msg = "skipped cursor mcp"
    if "cursor" in tools:
        mcp_msg = land_cursor(h, args.write_mcp, dry, copied)
    land_other(h, tools, dry, copied)
    catalog_msg = refresh_catalog(h, dry)

    ws_msg = "skipped workspace"
    if args.workspace:
        ws_msg = land_workspace(Path(args.workspace), dry, copied)

    print(f"files={len(copied)}")
    print(f"tools={','.join(tools)}")
    print(f"gsh={h.gsh}")
    print(mcp_msg)
    print(catalog_msg)
    print(ws_msg)
    if dry:
        for line in copied[:20]:
            print("dry", line)
        if len(copied) > 20:
            print(f"dry ... {len(copied) - 20} more")
        print("ok dry-run")
        return 0
    print("ok architecture files installed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
