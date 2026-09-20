# Cursor adapter (thin)

This directory is a **projection**, not a second copy of the capability library.

| Cursor surface | Source of truth |
|---|---|
| Project skills (if the repo is opened as a workspace) | [`../skills/`](../skills/) |
| Project agents | [`../agents/`](../agents/) |
| Always-on rule | [`../rules/全局.mdc`](../rules/全局.mdc) → synced into `.cursor/rules/` |
| Hooks registry | [`../hooks/hooks.json`](../hooks/hooks.json) |
| Hook scripts | [`../hooks/`](../hooks/) |
| Runtime / MCP boot | [`../harness/`](../harness/) |

Do not add a `.cursor/skills/` tree. Edit `skills/<id>/SKILL.md` at the repo root, then:

```bash
python -m gsh sync --isolate-root <probe> --workspace <ws> --yes
```

After `setup`, the **user-level** Cursor home (`~/.cursor` or an isolate root) receives a full runtime projection: hooks, rules, skills, agents, lazy MCP wrappers. That copy is generated. The repo must not keep five hand-maintained trees.

See [docs/adapters/cursor.md](../docs/adapters/cursor.md).
