# -*- coding: utf-8 -*-
"""把 SSOT 投影成各工具的完整原生目录。仓库根仍只维护一份 skills/agents。"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from gsh import natives
from gsh.project import (
    copy_file,
    copy_tree,
    project_crafts,
    project_skills,
    write_adapter_pointer,
    write_json,
    write_text,
)


@dataclass(frozen=True)
class ToolSpec:
    id: str
    title: str
    runtime: str  # cursor-hooks | claude-hooks | convention
    home_attr: str
    skill_dirs: tuple[str, ...]
    agent_dirs: tuple[str, ...]
    entries: tuple[str, ...]
    rule_rel: str | None
    hooks: str  # cursor | claude | gap
    hook_gap: str
    extra_homes: tuple[str, ...] = field(default_factory=tuple)


SPECS: tuple[ToolSpec, ...] = (
    ToolSpec(
        "cursor",
        "Cursor",
        "cursor-hooks",
        "cursor",
        ("skills",),
        ("agents",),
        (),
        "rules/全局.mdc",
        "cursor",
        "Cursor hooks.json is the native GSH runtime.",
    ),
    ToolSpec(
        "claude",
        "Claude Code",
        "claude-hooks",
        "claude",
        ("skills",),
        ("agents",),
        ("CLAUDE.md",),
        "rules/gsh.md",
        "claude",
        "Claude Code settings.json hooks invoke the same Python scripts; event names differ from Cursor.",
    ),
    ToolSpec(
        "codex",
        "Codex",
        "convention",
        "codex",
        ("skills",),
        ("agents",),
        ("AGENTS.md",),
        "rules/gsh.md",
        "gap",
        "AGENTS.md + ~/.agents/skills. No hook runtime.",
        extra_homes=("agents_skills",),
    ),
    ToolSpec(
        "windsurf",
        "Windsurf",
        "convention",
        "windsurf",
        ("skills", ".windsurf/skills"),
        ("agents",),
        ("AGENTS.md", ".windsurfrules"),
        ".windsurf/rules/gsh.md",
        "gap",
        ".windsurf/rules and .windsurfrules. Cascade/Devin hooks are not GSH hooks.json.",
    ),
    ToolSpec(
        "cline",
        "Cline",
        "convention",
        "cline",
        ("skills",),
        ("agents",),
        ("AGENTS.md",),
        ".clinerules/gsh.md",
        "gap",
        ".clinerules directory. No GSH hook runtime.",
    ),
    ToolSpec(
        "roo",
        "Roo Code",
        "convention",
        "roo",
        ("skills",),
        ("agents",),
        ("AGENTS.md",),
        ".roo/rules/gsh.md",
        "gap",
        ".roo/rules plus .roomodes. No GSH hook runtime.",
    ),
    ToolSpec(
        "continue",
        "Continue.dev",
        "convention",
        "continue_dir",
        ("skills",),
        ("agents",),
        ("AGENTS.md",),
        "rules/gsh.md",
        "gap",
        "config.yaml + rules. Merge carefully if a user config already exists.",
    ),
    ToolSpec(
        "copilot",
        "GitHub Copilot",
        "convention",
        "copilot",
        ("skills",),
        ("agents",),
        ("copilot-instructions.md",),
        "instructions/gsh.instructions.md",
        "gap",
        "copilot-instructions.md and .github/prompts. Instruction-only; no hooks.",
    ),
    ToolSpec(
        "opencode",
        "OpenCode",
        "convention",
        "opencode",
        ("skills",),
        ("agents",),
        ("AGENTS.md",),
        "rules/gsh.md",
        "gap",
        "AGENTS.md + opencode.json instructions. No GSH hook runtime.",
    ),
    ToolSpec(
        "gemini",
        "Gemini CLI",
        "convention",
        "gemini",
        ("skills",),
        ("agents",),
        ("GEMINI.md",),
        "rules/gsh.md",
        "gap",
        "GEMINI.md + ~/.gemini/skills. No GSH hook runtime.",
    ),
    ToolSpec(
        "aider",
        "Aider",
        "convention",
        "aider",
        ("skills",),
        ("agents",),
        ("CONVENTIONS.md", "AGENTS.md"),
        None,
        "gap",
        ".aider.conf.yml reads CONVENTIONS.md. No hooks, no native skill loader.",
    ),
    ToolSpec(
        "zed",
        "Zed",
        "convention",
        "zed",
        ("skills",),
        ("agents",),
        ("AGENTS.md", ".rules"),
        None,
        "gap",
        "AGENTS.md and .rules. No GSH hook runtime.",
    ),
    ToolSpec(
        "amazonq",
        "Amazon Q Developer",
        "convention",
        "amazonq",
        ("skills",),
        ("agents",),
        ("AGENTS.md",),
        "rules/gsh.md",
        "gap",
        ".amazonq/rules/*.md auto-load. No GSH hook runtime.",
    ),
    ToolSpec(
        "trae",
        "Trae",
        "convention",
        "trae",
        ("skills",),
        ("agents",),
        ("AGENTS.md",),
        "rules/gsh.md",
        "gap",
        ".trae/rules. No GSH hook runtime.",
    ),
    ToolSpec(
        "junie",
        "JetBrains Junie",
        "convention",
        "junie",
        ("skills",),
        ("agents",),
        ("AGENTS.md", "guidelines.md"),
        None,
        "gap",
        ".junie/guidelines.md. No GSH hook runtime.",
    ),
    ToolSpec(
        "grok",
        "Grok",
        "convention",
        "grok",
        ("skills",),
        ("agents",),
        ("AGENTS.md",),
        "rules/gsh.md",
        "gap",
        "AGENTS.md + full skill/craft tree. No hook runtime.",
    ),
    ToolSpec(
        "deepseek",
        "DeepSeek",
        "convention",
        "dsh",
        ("skills",),
        ("agents",),
        ("AGENTS.md",),
        "rules/gsh.md",
        "gap",
        "AGENTS.md + full skill/craft tree. No hook runtime.",
        extra_homes=("agents_skills",),
    ),
    ToolSpec(
        "kimi",
        "Kimi Code",
        "convention",
        "kimi",
        ("skills",),
        ("agents",),
        ("AGENTS.md",),
        "rules/gsh.md",
        "gap",
        "~/.kimi-code/skills and AGENTS.md. No GSH hook runtime.",
    ),
    ToolSpec(
        "qwen",
        "Qwen Code",
        "convention",
        "qwen",
        ("skills",),
        ("agents",),
        ("QWEN.md", "AGENTS.md"),
        "rules/gsh.md",
        "gap",
        ".qwen/skills + QWEN.md. No GSH hook runtime.",
    ),
)

SPEC_BY_ID = {s.id: s for s in SPECS}


def spec_for(tool_id: str) -> ToolSpec:
    return SPEC_BY_ID[tool_id]


def home_for(h, spec: ToolSpec) -> Path:
    return getattr(h, spec.home_attr)


def land_tool(pack: Path, h, spec: ToolSpec, profile: str, write_mcp: bool, dry: bool, copied: list[str]) -> str:
    dest = home_for(h, spec)
    text = natives.constitution(pack)
    rule = natives.gsh_rule_markdown(pack)

    for rel in spec.skill_dirs:
        project_skills(pack, dest / rel if rel != "." else dest, profile, dry, copied)
    for extra in spec.extra_homes:
        extra_root = getattr(h, extra)
        project_skills(pack, extra_root, profile, dry, copied)
    for rel in spec.agent_dirs:
        project_crafts(pack, dest / rel, profile, dry, copied)

    for entry in spec.entries:
        payload = text
        if entry.endswith(".windsurfrules") or entry.endswith(".rules"):
            payload = rule
        write_text(dest / entry, payload, dry, copied)

    if spec.rule_rel:
        if spec.rule_rel.endswith(".mdc"):
            copy_file(pack / "rules" / "全局.mdc", dest / spec.rule_rel, dry, copied)
        else:
            write_text(dest / spec.rule_rel, rule, dry, copied)

    if spec.hooks == "cursor":
        copy_tree(pack / "rules", dest / "rules", dry, copied)
        copy_tree(pack / "hooks", dest / "hooks", dry, copied)
        copy_file(pack / "hooks" / "hooks.json", dest / "hooks.json", dry, copied)
        copy_tree(h.gsh_harness, dest / "harness", dry, copied)
    elif spec.hooks == "claude":
        copy_tree(pack / "hooks", dest / "hooks", dry, copied)
        write_json(dest / "settings.json", natives.claude_settings(), dry, copied)
        write_text(dest / "HOOKS.md", natives.hook_gap_markdown(spec.title, spec.hook_gap), dry, copied)
        copy_tree(pack / "harness" / "scripts", dest / "harness" / "scripts", dry, copied)
    else:
        write_text(dest / "HOOKS.md", natives.hook_gap_markdown(spec.title, spec.hook_gap), dry, copied)
        copy_tree(pack / "harness" / "scripts", dest / "harness" / "scripts", dry, copied)

    example = pack / "harness" / "mcp.json.example"
    if example.is_file():
        copy_file(example, dest / "mcp.json.example", dry, copied)

    if spec.id == "continue":
        write_text(dest / "config.yaml", natives.continue_config(), dry, copied)
    if spec.id == "aider":
        write_text(dest / ".aider.conf.yml", natives.aider_conf(), dry, copied)
    if spec.id == "opencode":
        write_json(dest / "opencode.json", natives.opencode_json(), dry, copied)
    if spec.id == "zed":
        write_json(dest / "settings.json", natives.zed_settings(), dry, copied)
    if spec.id == "roo":
        write_json(dest / ".roomodes", natives.roo_modes(), dry, copied)
    if spec.id == "copilot":
        write_text(
            dest / "prompts" / "route-task.prompt.md",
            natives.copilot_prompt("GSH route-task", "Open skills/route-task/SKILL.md. Write loadplan.json."),
            dry,
            copied,
        )
        write_text(
            dest / "prompts" / "verify-gate.prompt.md",
            natives.copilot_prompt(
                "GSH close",
                "Run `python -m gsh close --kind smoke --evidence <path>`. Then read the report path it printed.",
            ),
            dry,
            copied,
        )
        write_text(
            dest / "prompts" / "status.prompt.md",
            natives.copilot_prompt("GSH status", "Run `python -m gsh status` and `python -m gsh resume`."),
            dry,
            copied,
        )
        write_text(
            dest / "prompts" / "next.prompt.md",
            natives.copilot_prompt("GSH next", "Run `python -m gsh next` and open the skill it names."),
            dry,
            copied,
        )

    write_adapter_pointer(dest, f"{spec.id}:{spec.runtime}", str(pack), dry, copied)
    write_json(
        dest / "gsh-capability.json",
        {
            "tool": spec.id,
            "runtime": spec.runtime,
            "hooks": spec.hooks,
            "hook_note": spec.hook_gap,
            "skills": list(spec.skill_dirs),
            "agents": list(spec.agent_dirs),
        },
        dry,
        copied,
    )

    if spec.id == "cursor":
        live = dest / "mcp.json"
        if live.is_file():
            return "kept existing mcp.json"
        if write_mcp and example.is_file() and not dry:
            copy_file(example, live, dry, copied)
            return "wrote mcp.json from example (placeholders only)"
        return "wrote mcp.json.example only (pass --write-mcp to create placeholder mcp.json)"
    return f"landed full native tree for {spec.id}"


def land_selected(pack: Path, h, tools: list[str], profile: str, write_mcp: bool, dry: bool, copied: list[str]) -> str:
    messages: list[str] = []
    for tool in tools:
        spec = SPEC_BY_ID.get(tool)
        if spec is None:
            continue
        messages.append(land_tool(pack, h, spec, profile, write_mcp, dry, copied))
    return "; ".join(messages) if messages else "no tools landed"


def land_project_natives(pack: Path, root: Path, dry: bool, copied: list[str]) -> None:
    """业务根：各工具打开工作室时会读的原生文件（不含 106 技能全拷）。"""
    text = natives.constitution(pack)
    rule = natives.gsh_rule_markdown(pack)
    write_text(root / "AGENTS.md", text, dry, copied)
    write_text(root / "CLAUDE.md", text, dry, copied)
    write_text(root / "GEMINI.md", text, dry, copied)
    write_text(root / "CONVENTIONS.md", text, dry, copied)
    write_text(root / "QWEN.md", text, dry, copied)
    write_text(root / ".windsurfrules", rule, dry, copied)
    write_text(root / ".rules", rule, dry, copied)
    write_text(root / ".clinerules" / "gsh.md", rule, dry, copied)
    write_text(root / ".windsurf" / "rules" / "gsh.md", rule, dry, copied)
    write_text(root / ".roo" / "rules" / "gsh.md", rule, dry, copied)
    write_json(root / ".roomodes", natives.roo_modes(), dry, copied)
    write_text(root / ".continue" / "rules" / "gsh.md", rule, dry, copied)
    write_text(root / ".continue" / "config.yaml", natives.continue_config(), dry, copied)
    write_text(root / ".aider.conf.yml", natives.aider_conf(), dry, copied)
    write_text(root / ".amazonq" / "rules" / "gsh.md", rule, dry, copied)
    write_text(root / ".trae" / "rules" / "gsh.md", rule, dry, copied)
    write_text(root / ".junie" / "guidelines.md", text, dry, copied)
    write_text(root / ".kimi-code" / "AGENTS.md", text, dry, copied)
    write_text(root / ".qwen" / "QWEN.md", text, dry, copied)
    write_json(root / ".opencode" / "opencode.json", natives.opencode_json(), dry, copied)
    write_json(root / ".claude" / "settings.json", natives.claude_settings(), dry, copied)
    write_text(root / ".claude" / "rules" / "gsh.md", rule, dry, copied)
    write_text(root / ".github" / "copilot-instructions.md", text, dry, copied)
    write_text(
        root / ".github" / "instructions" / "gsh.instructions.md",
        "---\napplyTo: '**'\n---\n\n" + rule,
        dry,
        copied,
    )
    copy_file(pack / "hooks" / "hooks.json", root / ".cursor" / "hooks.json", dry, copied)
    copy_file(pack / "rules" / "全局.mdc", root / ".cursor" / "rules" / "全局.mdc", dry, copied)
