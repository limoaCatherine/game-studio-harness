# -*- coding: utf-8 -*-
"""安装档位：minimal / core / full。技能与职种都从仓库根真相源筛选。"""
from __future__ import annotations

PROFILES = ("minimal", "core", "full")

# 缺了这些，定档/隔离/收口会立刻塌。
MINIMAL_SKILLS = (
    "route-task",
    "write-isolation",
    "doctor",
    "verify-gate",
    "mcp-autostart",
    "sync-state",
    "artifacts-append",
    "handoff-pack",
    "collab-protocol",
    "memory-retrieve",
    "promote-canon",
    "file-pack-layout",
)

# 日产核心：导演 + 表 + 切片 + 验收，不含全套美术/音频/DCC 做法。
CORE_SKILLS = MINIMAL_SKILLS + (
    "excel-read",
    "excel-format",
    "excel-com-write",
    "tunable-table-diff",
    "assemble-craft-flow",
    "feature-gdd-slice",
    "feature-vertical-slice",
    "pillar-define",
    "scope-cut-decision",
    "data-readiness-check",
    "status-digest",
    "promote-adr",
    "deliverable-sheets",
    "naming-consistency-check",
    "risk-register-update",
    "milestone-plan",
    "qa-plan",
    "build-acceptance",
    "bug-report-write",
    "test-case-from-gdd",
    "combat-modeling",
    "damage-formula-pass",
    "attribute-framework",
    "skill-kit-design",
    "progression-curve",
    "economy-loop-analysis",
)

MINIMAL_CRAFTS = (
    "producer",
    "systems-designer",
    "combat-numeric-designer",
    "qa-lead",
)

CORE_CRAFTS = MINIMAL_CRAFTS + (
    "associate-producer",
    "project-manager",
    "creative-director",
    "combat-designer",
    "economy-numeric-designer",
    "progression-numeric-designer",
    "client-engineer",
    "server-engineer",
    "qa-functional",
    "narrative-designer",
    "level-designer",
    "ux-designer",
    "tools-engineer",
)

# Cursor 执行 hooks.json；Claude Code 用 settings.json 调用同一组 Python 钩子。
HOOK_RUNTIME_TOOLS = frozenset({"cursor", "claude"})
ALL_TOOLS = (
    "cursor",
    "claude",
    "codex",
    "windsurf",
    "cline",
    "roo",
    "continue",
    "copilot",
    "opencode",
    "gemini",
    "aider",
    "zed",
    "amazonq",
    "trae",
    "junie",
    "grok",
    "deepseek",
    "kimi",
    "qwen",
)

ALIASES = {
    "claudecode": "claude",
    "claude-code": "claude",
    "openai": "codex",
    "grokbot": "grok",
    "grok-build": "grok",
    "deepseekharness": "deepseek",
    "dsh": "deepseek",
    "github-copilot": "copilot",
    "gh-copilot": "copilot",
    "codeium": "windsurf",
    "roo-code": "roo",
    "roocode": "roo",
    "continue-dev": "continue",
    "amazon-q": "amazonq",
    "amazon-q-developer": "amazonq",
    "jetbrains": "junie",
    "jetbrains-ai": "junie",
    "kimi-code": "kimi",
    "moonshot": "kimi",
    "qwen-code": "qwen",
    "gemini-cli": "gemini",
}


def parse_tools(raw: str) -> list[str]:
    text = (raw or "").strip().lower()
    if text in {"all", "*"}:
        return list(ALL_TOOLS)
    if text in {"legacy", "original5"}:
        return ["cursor", "claude", "codex", "grok", "deepseek"]
    out: list[str] = []
    for part in text.replace(";", ",").split(","):
        name = ALIASES.get(part.strip(), part.strip())
        if name not in ALL_TOOLS:
            raise ValueError(f"unknown tool {part!r}; choose from {', '.join(ALL_TOOLS)}")
        if name not in out:
            out.append(name)
    if not out:
        raise ValueError("need at least one --tools value")
    return out


def parse_profile(raw: str) -> str:
    name = (raw or "full").strip().lower()
    if name not in PROFILES:
        raise ValueError(f"unknown profile {raw!r}; choose from {', '.join(PROFILES)}")
    return name


def select_skills(profile: str, available: list[str]) -> list[str]:
    if profile == "full":
        return list(available)
    wanted = CORE_SKILLS if profile == "core" else MINIMAL_SKILLS
    have = set(available)
    return [s for s in wanted if s in have]


def select_crafts(profile: str, available: list[str]) -> list[str]:
    if profile == "full":
        return list(available)
    wanted = CORE_CRAFTS if profile == "core" else MINIMAL_CRAFTS
    have = set(available)
    return [c for c in wanted if c in have]
