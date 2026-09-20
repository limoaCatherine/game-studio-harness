# Architecture

Four layers are sealed. Changing the architecture requires a steer, a plan edit, and a decision record. Do not add a fifth layer along an old session list.

## Why four layers

A game studio workspace is not one prompt. It needs:

1. Rules that always apply (do not wait for a skill to be named).
2. A director that names only what this session will inject.
3. Reusable how-to bodies for events, roles, and external tools.
4. A per-project filing cabinet so the next session does not live in chat.

## Layer map

```text
~/.cursor/rules/全局.mdc          L1  always on
~/.cursor/skills/<id>/SKILL.md    L3  event how-to
~/.cursor/agents/<id>.md          L3  craft / role path
~/.cursor/harness/                L3+L4 user-level scripts, MCP stubs, catalog
<workspace>/.harness/             L4  current row, surfaces, sessions, memory
```

### L1 Constitution

Always-on Cursor rule. Opening order, session kinds (continue / steer / park / new / parallel / discuss), write isolation, and the sealed four-layer clause.

### L2 Routing

`route-task` writes `loadplan.json` and the current card, then `生成会话能力名单.py` writes `activated.json`.

Required plan fields: `session_id`, `tier`, `items`, `verify_kind`, `intent`, `work_mode`. Suggested: `write_class`, `retrieve_keys`, `forbid`.

### L3 Capabilities

- **Skills**: one event, one folder, reusable procedure.
- **Crafts**: role main path. Naming a craft injects the craft body plus `craft_open` (first step only).
- **MCP**: keys in `mcp.json`, purpose stubs in `harness/mcp-tools/<id>.json`, tiers in `mcp-tiers.json`.

### L4 Filing cabinet

Not a knowledge graph. Read the current row; write the current row; logs only append.

| Table | Path |
|---|---|
| Current row | `.harness/state.json` |
| Current card | `.harness/sessions/<session>/current.md` |
| Official surfaces | `.harness/surfaces.json` |
| Task log | `.harness/memory/tasks.jsonl` |
| Approved facts | `.harness/memory/canon/` |
| Decisions | `.harness/memory/adr/` |
| Artifact index | `.harness/artifacts/index.jsonl` |

## Write isolation

Default `write_class=sandbox`. Tables, code, engine trials, and drafts land on the sandbox root from `surfaces.json`. Promotion needs a human yes and writes only the recorded set — never overwrite an official surface with a whole file.

## Naming rules

- One open delivery per session directory.
- Same delivery, same chat, same `bead_id` → continue or steer.
- A different delivery → new session directory.
- Parallel independent deliveries → separate sessions; spawn subagents as needed.

## What receivers must change

1. `surfaces.json` official/sandbox paths.
2. `mcp.json` host commands after software exists.
3. Optional: which MCP ids sit in `mcp-tiers.json` `core`.
