# -*- coding: utf-8 -*-
"""各工具原生文件正文。内容来自宪法与 L1，不另写一套做法。"""
from __future__ import annotations

from pathlib import Path


def strip_mdc(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip()
    return text


def constitution(pack: Path) -> str:
    for cand in (pack / "AGENTS.md", pack / "rules" / "全局.mdc"):
        if cand.is_file():
            return strip_mdc(cand.read_text(encoding="utf-8")) if cand.suffix == ".mdc" else cand.read_text(
                encoding="utf-8"
            )
    return "# Game Studio Harness\n"


def l1_body(pack: Path) -> str:
    path = pack / "rules" / "全局.mdc"
    if path.is_file():
        return strip_mdc(path.read_text(encoding="utf-8"))
    return constitution(pack)


def gsh_rule_markdown(pack: Path, title: str = "Game Studio Harness") -> str:
    return f"# {title}\n\n{l1_body(pack).rstrip()}\n"


def hook_gap_markdown(tool: str, closest: str) -> str:
    return (
        f"# GSH hooks on {tool}\n\n"
        f"{tool} does not execute Cursor `hooks.json`.\n\n"
        f"Closest equivalent shipped here: **{closest}**.\n\n"
        "You still follow the same loop: scope → isolate → verify-report → human promote.\n"
        "Open `.harness/sessions/<id>/current.md` yourself at session start.\n"
        "Do not close a work item without `.harness/artifacts/<bead>/verify-report.json` "
        "and `verdict: pass`.\n"
        "Do not read `.env`, `credentials.json`, or private keys into the model.\n"
        "Do not run `git reset --hard` or force-push without a human confirm.\n"
    )


def claude_settings() -> dict:
    return {
        "hooks": {
            "SessionStart": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python hooks/开场.py",
                            "timeout": 25,
                        }
                    ]
                }
            ],
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python hooks/命令前.py",
                            "timeout": 15,
                        }
                    ],
                },
                {
                    "matcher": "Read",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python hooks/读文件前.py",
                            "timeout": 10,
                        }
                    ],
                },
            ],
            "Stop": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python hooks/结束.py",
                            "timeout": 10,
                        }
                    ]
                }
            ],
        }
    }


def continue_config() -> str:
    return """name: Game Studio Harness
version: 0.2.1
schema: v1
rules:
  - uses: file
    name: gsh-constitution
    rule: AGENTS.md
  - uses: file
    name: gsh-l1
    rule: rules/gsh.md
prompts:
  - name: route-task
    description: Scope a GSH session
    prompt: Open skills/route-task/SKILL.md. Write loadplan.json. Do not invent ids.
  - name: verify-gate
    description: Close the current work item
    prompt: Run python -m gsh close --kind smoke --evidence <path>. Open skills/verify-gate/SKILL.md if you need the field meaning.
  - name: gsh-status
    description: Resume the current GSH session
    prompt: Run python -m gsh status and python -m gsh resume. Open the current skill only.
  - name: gsh-next
    description: Advance the current craft path
    prompt: Run python -m gsh next. Then open the skill named in craft_open.
"""


def aider_conf() -> str:
    return """# GSH — always load the constitution as read-only context.
read:
  - CONVENTIONS.md
  - AGENTS.md
"""


def opencode_json() -> dict:
    return {
        "$schema": "https://opencode.ai/config.json",
        "instructions": ["AGENTS.md", "rules/gsh.md"],
    }


def zed_settings() -> dict:
    return {
        "agent": {
            "preferred_completion_mode": "normal"
        }
    }


def roo_modes() -> dict:
    return {
        "customModes": [
            {
                "slug": "gsh-director",
                "name": "GSH Director",
                "description": "Scope the round. Write loadplan. Do not implement official surfaces.",
                "roleDefinition": "You are the GSH director. Restate goal, pick catalog ids, write loadplan.json, generate the roster. Default write_class is sandbox.",
                "groups": ["read", "edit", "command"],
                "customInstructions": "Open skills/route-task/SKILL.md. Do not pre-expand crafts.",
            },
            {
                "slug": "gsh-maker",
                "name": "GSH Maker",
                "description": "Execute one named skill or the current craft_open step in sandbox.",
                "roleDefinition": "You execute one named GSH skill in isolation. Do not promote official surfaces.",
                "groups": ["read", "edit", "command"],
                "customInstructions": "Run python -m gsh resume. Open only the current craft step. Stay in sandbox.",
            },
            {
                "slug": "gsh-closer",
                "name": "GSH Closer",
                "description": "Close the current work item with gsh close.",
                "roleDefinition": "You close a GSH work item by running python -m gsh close and attaching evidence paths.",
                "groups": ["read", "edit", "command"],
                "customInstructions": "Run python -m gsh close --kind smoke --evidence <path>. Read skills/verify-gate/SKILL.md for field meaning.",
            },
        ]
    }


def copilot_prompt(name: str, body: str) -> str:
    return f"---\ndescription: {name}\n---\n\n{body}\n"
