# Receiver notes (for the deploying agent)

Read this file, then run `install.py`. Do not edit the studio repo first. Do not install DCC / Excel / MCP backend software as part of this deploy.

This pack contains **skill, MCP, and rule deploy logic**, plus the wiring required to run the four layers (craft bodies, hooks, harness scripts). **Software binaries are not in the pack.**

## Sealed layers

Changing the architecture requires a steer, a plan edit, and a decision record. Do not add a layer along an old named list.

| Layer | Meaning | Lands at |
|---|---|---|
| L1 Constitution | Always-on rules | `~/.cursor/rules/全局.mdc` |
| L2 Routing | Naming, current card, write class | `route-task` + workspace `.harness/sessions/` |
| L3 Capabilities | Skills, crafts, MCP purpose stubs | `~/.cursor/skills/` `agents/` `harness/mcp-tools/` |
| L4 Filing cabinet | Current row, surface map, logs | workspace `.harness/` |

`activated.json` only decides which bodies are injected at start. It is **not** a runtime firewall. Crafts do **not** pre-expand path skills or MCP.

## Not in the pack

- Excel / Unity / Blender / FMOD / DCC / Node packages / Python venvs / MCP backend exe
- Live `mcp.json` absolute paths, accounts, keys
- Runtime `catalog.json`, `mcp-health.json` (generated after install)
- Any workbook, design doc, or engine project

A machine with no hosts can still land the architecture. Red MCP health without backends is not an architecture failure.

## Prerequisites

- Python 3.11+ on PATH (`python`)
- Writable Cursor user directory (default `~/.cursor`)
- A workspace root that will hold `.harness`. Create an empty directory if needed.

## One-shot deploy

From the **pack root** (this file's directory):

```text
python install.py --workspace <absolute-workspace>
python verify_install.py --workspace <absolute-workspace>
```

User-level only:

```text
python install.py --cursor-only
python verify_install.py --cursor-only
```

`--dry-run` only prints targets. Same-name files from this pack overwrite; extra skills/crafts on the machine stay.

**Do not** use `--write-mcp` to overwrite an existing live `mcp.json`. That flag writes a no-secret skeleton only when the target has no `mcp.json`.

## Land map

| In pack | Target |
|---|---|
| `payload/L1-rules/全局.mdc` | `~/.cursor/rules/全局.mdc` |
| `payload/L2-skills/<id>/` | `~/.cursor/skills/<id>/` |
| `payload/L2-crafts/<id>.md` | `~/.cursor/agents/<id>.md` |
| `payload/L3-mcp/mcp-tools/` | `~/.cursor/harness/mcp-tools/` |
| `payload/L3-mcp/mcp-tiers.json` | `~/.cursor/harness/mcp-tiers.json` (boot paths rewritten to this machine) |
| `payload/L3-mcp/mcp-boot/` | `~/.cursor/harness/mcp-boot/` |
| `payload/L3-mcp/mcp.json.example` | `~/.cursor/mcp.json.example` |
| `payload/L3-mcp/mcp-registry.json` | Read-only: how to register each server, no software |
| `payload/L4-harness/scripts/` | `~/.cursor/harness/scripts/` |
| `payload/L4-harness/surfaces.default.json` | `~/.cursor/harness/surfaces.default.json` |
| `payload/wiring/hooks.json` | `~/.cursor/hooks.json` |
| `payload/wiring/hooks/` | `~/.cursor/hooks/` |
| `payload/workspace-scaffold/.harness/` | `<workspace>/.harness/` (existing files are not overwritten) |

Install ends by running `刷新菜单.py` to write `~/.cursor/harness/catalog.json`.

## MCP logic (no software)

Authority: `payload/L3-mcp/mcp-registry.json` and skill `mcp-autostart`.

1. Ids must be keys in `~/.cursor/mcp.json` `mcpServers`. Missing id → doctor, then refresh the catalog so `mcp-tools/<id>.json` exists.
2. Tiers in `mcp-tiers.json`: **core** is direct (default `excelMCP`); others are **lazy** (`lazy_stdio.py` + tool cache). `miro` is URL passthrough. `cascadeur` is already an HTTP bridge.
3. After backends exist: fill `mcp.json` with local commands, then run `应用外接档位.py`. Core entries must not wrap `lazy_stdio.py`.
4. Secrets stay in the local secret store or local `mcp.json`. Do not write them back into this repository.
5. Probe script `拉起外接.py` reads `HARNESS_HOST_PATHS` / `GAMEDEV_MCP_EXE` or `~/.cursor/harness/host-paths.json`. Ignore MCP health red on a machine with no hosts.

`mcp.json.example` uses placeholders: `${PYTHON}` `${MCP_BOOT}` `${HARNESS_APPS}` `${NPX}` `${NODE}` `${UV}` `${UVX}` `${DOTNET_TOOLS}`. Secret slots are `${LARK_APP_ID}` style, never live values.

## Workspace scaffold

The installer only fills missing files. It does not overwrite an existing `.harness`. A new root needs at least:

- `.harness/state.json`
- `.harness/surfaces.json` (copied from `surfaces.default.json`, then edited)
- `.harness/memory/canon/四层运行口径.md`
- `.harness/memory/canon/四层封版.md`
- `.harness/memory/tasks.jsonl`
- `.harness/artifacts/index.jsonl`
- `.harness/sessions/`

The surface map **must** be rewritten for the receiving project.

## Do this immediately after install

1. Opening order: `全局.mdc` → current card → named bodies → canon/adr hit by `retrieve_keys`.
2. New work item: write `.harness/sessions/<short-id>/loadplan.json` with `session_id` `tier` `items` `verify_kind` `intent` `work_mode`.
3. From the workspace: `python ~/.cursor/harness/scripts/生成会话能力名单.py <short-id>`
4. Confirm `activated.json` `ok=true` and crafts did not pre-expand `skills`.
5. Default `write_class=sandbox`. Promotion needs a human yes; write only the recorded set.

Wire check (cwd = workspace, and a non-probe session exists):

```text
python ~/.cursor/harness/scripts/接线自检.py
```

`握手四层.py` / `整接.py` may fail on `mcp-health.json` when no hosts exist. Architecture landing is judged by `verify_install.py`.

## Failure table

| Symptom | Do |
|---|---|
| Catalog missing an id | Run `刷新菜单.py`; still missing → `doctor` |
| Name list errors `needs_mcp` not in catalog | Add the `mcp.json` key first, or do not name that skill yet |
| Craft pre-expanded path skills | Do not change the generator contract; check L1 still says 不预展开 |
| No current card at open | Workspace missing `.harness` or `sessions/LATEST` |
| Want another layer | Stop. Steer, edit the plan, write a decision |

## Pack index

- `MANIFEST.json` — file list and counts
- `DEPLOY_STEPS.json` — machine-readable steps
- `payload/L3-mcp/mcp-registry.json` — MCP registration logic
- `install.py` / `verify_install.py` — deploy and accept
