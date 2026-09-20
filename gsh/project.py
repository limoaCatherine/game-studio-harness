# -*- coding: utf-8 -*-
"""把仓库根真相源投影到共享运行时与各工具家目录。禁止再维护五套全量拷贝。"""
from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from gsh.profiles import (
    FULL_RUNTIME_TOOLS,
    select_crafts,
    select_skills,
)


def copy_file(src: Path, dst: Path, dry: bool, copied: list[str]) -> None:
    if not src.is_file():
        return
    if not dry:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    copied.append(f"{src.as_posix()} -> {dst.as_posix()}")


def copy_tree(src: Path, dst: Path, dry: bool, copied: list[str]) -> None:
    if not src.exists():
        return
    if src.is_file():
        copy_file(src, dst, dry, copied)
        return
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        if path.name == ".gitkeep":
            target = dst / path.relative_to(src).parent
            if not dry:
                target.mkdir(parents=True, exist_ok=True)
            continue
        copy_file(path, dst / path.relative_to(src), dry, copied)


def merge_missing(src: Path, dst: Path, dry: bool, copied: list[str]) -> None:
    if not src.exists():
        return
    for path in src.rglob("*"):
        if path.is_dir():
            if not dry:
                (dst / path.relative_to(src)).mkdir(parents=True, exist_ok=True)
            continue
        if path.name == ".gitkeep":
            if not dry:
                (dst / path.relative_to(src).parent).mkdir(parents=True, exist_ok=True)
            continue
        target = dst / path.relative_to(src)
        if target.exists():
            continue
        copy_file(path, target, dry, copied)


def write_text(path: Path, text: str, dry: bool, copied: list[str]) -> None:
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    copied.append(f"write {path.as_posix()}")


def write_json(path: Path, payload: object, dry: bool, copied: list[str]) -> None:
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n", dry, copied)


def list_skill_ids(root: Path) -> list[str]:
    if not root.is_dir():
        return []
    return sorted(
        p.name for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()
    )


def list_craft_ids(root: Path) -> list[str]:
    if not root.is_dir():
        return []
    return sorted(p.stem for p in root.glob("*.md") if "bak" not in p.name.lower())


def project_skills(pack: Path, dest: Path, profile: str, dry: bool, copied: list[str]) -> list[str]:
    available = list_skill_ids(pack / "skills")
    chosen = select_skills(profile, available)
    dest.mkdir(parents=True, exist_ok=True) if not dry else None
    for sid in chosen:
        copy_tree(pack / "skills" / sid, dest / sid, dry, copied)
    return chosen


def project_crafts(pack: Path, dest: Path, profile: str, dry: bool, copied: list[str]) -> list[str]:
    available = list_craft_ids(pack / "agents")
    chosen = select_crafts(profile, available)
    if not dry:
        dest.mkdir(parents=True, exist_ok=True)
    for cid in chosen:
        copy_file(pack / "agents" / f"{cid}.md", dest / f"{cid}.md", dry, copied)
    return chosen


def write_adapter_pointer(dest: Path, kind: str, source: str, dry: bool, copied: list[str]) -> None:
    write_json(
        dest / "gsh-adapter.json",
        {
            "kind": kind,
            "source_of_truth": source,
            "note": "This directory is a projection. Edit skills/agents/rules/hooks/harness at the pack root, then run `python -m gsh sync`.",
        },
        dry,
        copied,
    )


def constitution_text(pack: Path) -> str:
    for cand in (pack / "AGENTS.md", pack / "rules" / "全局.mdc"):
        if cand.is_file():
            text = cand.read_text(encoding="utf-8")
            if cand.name.endswith(".mdc") and text.startswith("---"):
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    return "# Game Studio Harness\n" + parts[2].lstrip()
            return text
    return "# Game Studio Harness\n"


def write_tiers(pack: Path, harness_dst: Path, dry: bool) -> None:
    src = pack / "harness" / "mcp-tiers.json"
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


def land_shared(pack: Path, h, profile: str, dry: bool, copied: list[str]) -> dict:
    skills = project_skills(pack, h.gsh_skills, profile, dry, copied)
    crafts = project_crafts(pack, h.gsh_agents, profile, dry, copied)
    copy_tree(pack / "harness" / "scripts", h.gsh_harness / "scripts", dry, copied)
    copy_file(
        pack / "harness" / "surfaces.default.json",
        h.gsh_harness / "surfaces.default.json",
        dry,
        copied,
    )
    copy_tree(pack / "harness" / "mcp-tools", h.gsh_harness / "mcp-tools", dry, copied)
    copy_tree(pack / "harness" / "docs", h.gsh_harness / "docs", dry, copied)
    copy_tree(pack / "harness" / "mcp-boot", h.gsh_harness / "mcp-boot", dry, copied)
    copy_file(
        pack / "harness" / "host-paths.example.json",
        h.gsh_harness / "host-paths.example.json",
        dry,
        copied,
    )
    example = pack / "harness" / "mcp.json.example"
    if example.is_file():
        copy_file(example, h.gsh / "mcp.json.example", dry, copied)
    copy_tree(pack / "rules", h.gsh_rules, dry, copied)
    copy_tree(pack / "hooks", h.gsh_hooks, dry, copied)
    write_tiers(pack, h.gsh_harness, dry)
    write_text(h.gsh / "AGENTS.md", constitution_text(pack), dry, copied)
    write_adapter_pointer(h.gsh, "shared-runtime", str(pack), dry, copied)
    return {"skills": skills, "crafts": crafts}


def land_cursor(pack: Path, h, profile: str, write_mcp: bool, dry: bool, copied: list[str]) -> str:
    copy_tree(pack / "rules", h.cursor / "rules", dry, copied)
    project_skills(pack, h.cursor / "skills", profile, dry, copied)
    project_crafts(pack, h.cursor / "agents", profile, dry, copied)
    copy_tree(pack / "hooks", h.cursor / "hooks", dry, copied)
    copy_file(pack / "hooks" / "hooks.json", h.cursor / "hooks.json", dry, copied)
    copy_tree(h.gsh_harness, h.cursor / "harness", dry, copied)
    write_adapter_pointer(h.cursor, "cursor-full-runtime", str(pack), dry, copied)
    example = pack / "harness" / "mcp.json.example"
    dest_example = h.cursor / "mcp.json.example"
    if example.is_file():
        copy_file(example, dest_example, dry, copied)
    live = h.cursor / "mcp.json"
    if live.is_file():
        return "kept existing mcp.json"
    if not write_mcp:
        return "wrote mcp.json.example only (pass --write-mcp to create placeholder mcp.json)"
    if example.is_file() and not dry:
        shutil.copy2(example, live)
        copied.append(f"{example.as_posix()} -> {live.as_posix()}")
    return "wrote mcp.json from example (placeholders only; no live servers)"


def land_instruction_tool(
    pack: Path,
    dest: Path,
    filename: str,
    profile: str,
    dry: bool,
    copied: list[str],
    extra_skills: Path | None = None,
) -> None:
    write_text(dest / filename, constitution_text(pack), dry, copied)
    project_skills(pack, dest / "skills", profile, dry, copied)
    project_crafts(pack, dest / "agents", profile, dry, copied)
    write_adapter_pointer(dest, f"instruction:{filename}", str(pack), dry, copied)
    if extra_skills is not None:
        project_skills(pack, extra_skills, profile, dry, copied)


def land_other(pack: Path, h, tools: Iterable[str], profile: str, dry: bool, copied: list[str]) -> None:
    tools = list(tools)
    if "claude" in tools:
        land_instruction_tool(pack, h.claude, "CLAUDE.md", profile, dry, copied)
    if "codex" in tools:
        land_instruction_tool(pack, h.codex, "AGENTS.md", profile, dry, copied, extra_skills=h.agents_skills)
    if "grok" in tools:
        land_instruction_tool(pack, h.grok, "AGENTS.md", profile, dry, copied)
    if "deepseek" in tools:
        land_instruction_tool(pack, h.dsh, "AGENTS.md", profile, dry, copied, extra_skills=h.agents_skills)
    if "windsurf" in tools:
        land_instruction_tool(pack, h.windsurf, "AGENTS.md", profile, dry, copied)
    if "cline" in tools:
        land_instruction_tool(pack, h.cline, "AGENTS.md", profile, dry, copied)
    if "continue" in tools:
        write_text(h.continue_dir / "config.yaml.gsh-snippet", continue_snippet(), dry, copied)
        write_text(h.continue_dir / "AGENTS.md", constitution_text(pack), dry, copied)
        write_adapter_pointer(h.continue_dir, "continue-snippet", str(pack), dry, copied)
    if "copilot" in tools:
        write_text(h.copilot / "copilot-instructions.md", constitution_text(pack), dry, copied)
        write_adapter_pointer(h.copilot, "copilot-instructions", str(pack), dry, copied)
    if "opencode" in tools:
        land_instruction_tool(pack, h.opencode, "AGENTS.md", profile, dry, copied)
    if "gemini" in tools:
        land_instruction_tool(pack, h.gemini, "GEMINI.md", profile, dry, copied)


def continue_snippet() -> str:
    return """# GSH projection snippet for Continue.
# Merge rules/systemMessage into your ~/.continue/config.yaml.
# Continue has no GSH hook runtime.
systemMessage: |
  Game Studio Harness: 定档 → 制作 → 结案.
  Read AGENTS.md in this folder. Do not invent skill ids.
  Default write_class is sandbox. Promote only with human approval.
"""


def land_workspace(pack: Path, root: Path, dry: bool, copied: list[str]) -> str:
    if not dry:
        root.mkdir(parents=True, exist_ok=True)
    merge_missing(pack / "studio" / ".harness", root / ".harness", dry, copied)
    text = constitution_text(pack)
    write_text(root / "AGENTS.md", text, dry, copied)
    write_text(root / "CLAUDE.md", text, dry, copied)
    return f"scaffolded missing files under {root / '.harness'}"


def refresh_catalog(pack: Path, h, dry: bool) -> str:
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


def write_install_state(
    h,
    pack: Path,
    tools: list[str],
    profile: str,
    workspace: Path | None,
    isolate: Path | None,
    copied: list[str],
    dry: bool,
) -> None:
    state = {
        "version": 1,
        "pack": str(pack),
        "profile": profile,
        "tools": tools,
        "workspace": str(workspace) if workspace else None,
        "isolate_root": str(isolate) if isolate else None,
        "files": copied,
        "installed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pid": os.getpid(),
    }
    write_json(h.state_file, state, dry, copied)


def read_install_state(h) -> dict | None:
    path = h.state_file
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
