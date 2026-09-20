# Game Studio Harness

A **Cursor-based game production platform**: four sealed layers that turn a studio workspace into named skills, crafts (roles), MCP wiring, and a project filing cabinet. Other teams can clone this repo and deploy the architecture without copying any studio project data.

这是一套可部署的游戏制作平台架构包：只含规则、技能、职种、外接注册逻辑与业务根脚手架。**不含 DCC / 引擎 / MCP 后端软件，不含密钥，不含任何业务表或策划案。**

## What you get

| Layer | Role | Lands at |
|---|---|---|
| L1 Constitution | Always-on rules | `~/.cursor/rules/` |
| L2 Routing | Session plan, current card, write class | `route-task` + `<workspace>/.harness/sessions/` |
| L3 Capabilities | Event skills, crafts, MCP tool stubs | `~/.cursor/skills/` `agents/` `harness/mcp-tools/` |
| L4 Filing cabinet | Current row, surface map, append-only logs | `<workspace>/.harness/` |

`activated.json` only decides **which bodies are injected at session start**. It is not a runtime firewall. Crafts do **not** pre-expand their skill paths.

## Requirements

- Python 3.11+ on `PATH` (`python`)
- [Cursor](https://cursor.com) with a writable user directory (default `~/.cursor`)
- A workspace root that will hold `.harness` (create an empty folder if you do not have one)

Optional later: Excel, Unity, Blender, FMOD, and other hosts. Missing hosts make MCP health red; that is **not** an architecture failure.

## Deploy

From the repository root:

```bash
python install.py --workspace /absolute/path/to/your/studio-root
python verify_install.py --workspace /absolute/path/to/your/studio-root
```

User-level files only, no workspace yet:

```bash
python install.py --cursor-only
python verify_install.py --cursor-only
```

`--dry-run` prints copy targets. Same-name files from this pack overwrite; extra skills/crafts already on the machine are kept.

**Do not** pass `--write-mcp` if the machine already has `~/.cursor/mcp.json`. That flag only writes a placeholder skeleton when the file is missing.

Then edit `<workspace>/.harness/surfaces.json` so `official` / `sandbox` match **this** project. Do not keep the placeholders.

## First session

1. Opening read order: L1 rule → current card → named skill/craft bodies → canon/adr hit by `retrieve_keys`.
2. New work item: write `.harness/sessions/<short-id>/loadplan.json` with `session_id`, `tier`, `items`, `verify_kind`, `intent`, `work_mode`.
3. From the workspace root: `python ~/.cursor/harness/scripts/生成会话能力名单.py <short-id>`
4. Confirm `activated.json` has `ok=true` and crafts did not pre-expand `skills`.
5. Default write class is `sandbox`. Promotion needs a human yes, and only writes the recorded set.

Agent-oriented steps: `READ_ME_AGENT.md`. Machine steps: `DEPLOY_STEPS.json`. Architecture: `docs/ARCHITECTURE.md`.

## MCP (logic only)

See `payload/L3-mcp/mcp-registry.json` and the `mcp-autostart` skill.

1. Server ids must exist as keys under `mcpServers` in `~/.cursor/mcp.json`.
2. Tiers live in `mcp-tiers.json`: **core** connects immediately (default: `excelMCP`); everything else is **lazy**. `miro` stays a URL. `cascadeur` is an HTTP bridge.
3. After hosts exist: copy `mcp.json.example`, replace `${PYTHON}` `${NPX}` `${HARNESS_APPS}` and secret placeholders, then run `应用外接档位.py`.
4. Secrets stay in the local secret store or local `mcp.json`. Never commit them back here.

## Not in this repository

- Excel / Unity / Blender / FMOD / DCC / Node packages / Python venvs / MCP backend binaries
- Live `mcp.json` absolute paths, accounts, or keys
- Runtime `catalog.json` and `mcp-health.json` (generated after install)
- Any studio workbook, GDD, engine project, or player-facing content

## Verify

`verify_install.py` checks that L1–L4 files landed, the catalog can be built, and the pack still contains no machine-user paths or literal secrets.

```bash
python verify_install.py --workspace /absolute/path/to/your/studio-root
```

Expected last line: `ok architecture install`.

## License

MIT. See `LICENSE`.
