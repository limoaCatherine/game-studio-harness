# Changelog

## 0.2.1

- Each selected tool home is now a complete native tree: entry files, rules, skills, crafts, hooks or `HOOKS.md`, MCP example, `gsh-capability.json`.
- 19 adapters: Cursor, Claude Code, Codex, Windsurf, Cline, Roo Code, Continue.dev, GitHub Copilot, OpenCode, Gemini CLI, Aider, Zed, Amazon Q Developer, Trae, JetBrains Junie, Grok, DeepSeek, Kimi Code, Qwen Code.
- Claude Code `settings.json` invokes the same Python hooks (`开场.py` / `命令前.py` / `读文件前.py` / `结束.py`).
- Studio roots receive native convention files for those tools (no second 106-skill copy in the pack).
- README / README.en design philosophy rewritten in GSH's own voice. Negative-definition lists removed.
- Default `--tools` is `all`. `legacy` still means cursor+claude+codex+grok+deepseek.

## 0.2.0

Layout refactor: one content source, generated projections, GSH game-production semantics.

- Single source of truth at repo root: `skills/`, `agents/`, `rules/`, `hooks/`, `harness/`.
- Removed the in-repo copies under `cursor/`, `claude/`, `codex/`, `grok/`, `deepseek/`.
- Python 3.11+ CLI: `python -m gsh setup|sync|verify|doctor|uninstall` with profiles and isolate root.
- Honest MCP policy (0 live servers shipped).
- Bilingual README + architecture / adapter / cookbook docs.
- Tests for catalog, unique IDs, no craft pre-expand, secret scan, SSOT layout, isolate CLI.

## 0.1.0

- Four-layer freeze: constitution, director, capability library, filing cabinet.
- Five complete tool trees and a one-shot installer.
