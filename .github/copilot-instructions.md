# Game Studio Harness (GitHub Copilot)

Copilot is **instruction-only**. There is no GSH hook runtime, no sessionStart card, and no beforeShellExecution gate.

Follow the four-layer loop:

1. Scope the round (`route-task`) before editing official tables, code, or assets.
2. Load one craft or one skill at a time. Do not pre-expand a craft's `uses_skills`.
3. Default write class is `sandbox`. Promote only with human approval and changeset merge.
4. Close a work item only after `verify-report.json` exists and `verdict` is `pass`.

Canonical files live at the repository root: `skills/`, `agents/`, `rules/`, `hooks/`, `harness/`. Read `AGENTS.md` first.
