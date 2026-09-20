# Changelog

## 0.2.0

Destructive layout refactor (ECC-grade packaging, GSH game-production semantics).

- Single source of truth at repo root: `skills/`, `agents/`, `rules/`, `hooks/`, `harness/`.
- Deleted the five full copies under `cursor/`, `claude/`, `codex/`, `grok/`, `deepseek/`.
- Thin adapters only (`.cursor/`, `.claude/`, `.codex/`, instruction files).
- Python 3.11+ CLI: `python -m gsh setup|sync|verify|doctor|uninstall` with profiles and isolate root.
- Honest platform matrix and MCP policy (0 live servers shipped).
- Bilingual README + architecture / adapter / cookbook docs.
- Tests for catalog, unique IDs, no craft pre-expand, secret scan, thin adapters, isolate CLI.

## 0.1.0

- Four-layer freeze: constitution, director, capability library, filing cabinet.
- Five complete tool trees and a one-shot installer.
