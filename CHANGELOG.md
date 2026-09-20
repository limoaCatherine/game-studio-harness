# Changelog

## 0.3.0

- Craft paths are a runnable pipeline: `activated.json` now stores `craft_path`, and `python -m gsh next` advances the current step.
- Session continuity: `python -m gsh status` / `resume` read `current.md`, `state.json`, and the latest verify report.
- Close workflow: `python -m gsh close` writes `verify-report.json` from a template and appends the audit log.
- Director menu: `python -m gsh menu` looks up craft/skill ids. Boot context refuses a dumped catalog.
- `python -m gsh activate <session>` generates the roster from a loadplan.
- README / architecture rewritten capability-first (install → start using → what's inside → concepts → philosophy → guides → platform → MCP → security). No hero image. No defect-catalog chapters.

## 0.2.1

- Each selected tool home is a complete native tree.
- 19 adapters. Claude Code `settings.json` invokes the same Python hooks.
- Default `--tools all`.

## 0.2.0

Layout refactor: one content source, generated projections.

- Single source of truth at repo root: `skills/`, `agents/`, `rules/`, `hooks/`, `harness/`.
- Python 3.11+ CLI: setup / sync / verify / doctor / uninstall.
- Honest MCP policy (0 live servers shipped).

## 0.1.0

- Four-layer freeze and a one-shot installer.
