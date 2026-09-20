<p align="center">
  <img src="assets/four-layer.svg" alt="Game Studio Harness four layers" width="920" />
</p>

<h1 align="center">Game Studio Harness</h1>

<p align="center">
  <strong>A four-layer context operating system for game-production agents.</strong><br/>
  Scope → slice → isolate → verify → promote.<br/>
  <a href="README.md">中文</a> ·
  <a href="#install">Install</a> ·
  <a href="#mental-model">Mental model</a> ·
  <a href="#design-philosophy">Design philosophy</a> ·
  <a href="#layer-deep-dives">Layer deep dives</a> ·
  <a href="#platform-support">Platform support</a> ·
  <a href="docs/mcp-policy.md">MCP policy</a>
</p>

<p align="center">

| Crafts | Skills | MCP policy | Native adapters |
| :---: | :---: | :---: | :---: |
| 35 crafts | 106 skills | **0** live servers shipped / 36 purpose stubs | 19 full native trees · Cursor `hooks.json` · Claude `settings.json` |

</p>

> Context windows are scarce. Official surfaces are irreversible. Sessions die. Verbal "green" cannot close a work item.
>
> GSH is a **four-layer context OS** for LLM agents inside a real game-production pipeline: scope, slice, isolate, verify, promote.

> [!WARNING]
> **Official sources only.** Install from [github.com/limoaCatherine/game-studio-harness](https://github.com/limoaCatherine/game-studio-harness). Third-party zips and mirrors are unreviewed and may ship hostile hooks or a live `mcp.json`. This repo is MIT. It does not vendor DCC binaries or studio absolute paths.

---

## Install

**Python 3.11+**. Windows game-production machines are first-class; Linux/macOS are for isolate probes and CI. The installer projects architecture files and skills only. It does not ship production-software installers and does not write secrets.

> [!IMPORTANT]
> **Edit content only at repo root.** `skills/`, `agents/`, `rules/`, `hooks/`, and `harness/` are the only source of truth. `gsh setup` / `gsh sync` write that same content into each tool's complete native tree. Do not keep a second hand-maintained skill tree in a homedir.

### Recommended: Python CLI

```bash
git clone https://github.com/limoaCatherine/game-studio-harness.git
cd game-studio-harness
python -m gsh setup --guided
```

Non-interactive:

```bash
python -m gsh setup \
  --workspace /path/to/studio-root \
  --tools cursor,claude \
  --profile core \
  --yes
```

Equivalent entries (choose one, do not stack):

| Entry | Command |
|---|---|
| Module | `python -m gsh setup` |
| Unix | `./install.sh` |
| Windows | `.\install.ps1` or `.\一键部署.ps1` |
| Legacy wrapper | `python install/install.py` forwards to `gsh setup` |

### Profiles

| `--profile` | Lands | Use when |
|---|---|---|
| `minimal` | L1 + 12 director/isolation/close skills + 4 crafts | Learn the four layers |
| `core` | Daily director, tables, slice, acceptance + common crafts | Most production sessions |
| `full` (default) | 106 skills + 35 crafts + all MCP stubs | You want the full catalog |

### Tools

| `--tools` | Native files landed in that tool home |
|---|---|
| `cursor` | `hooks.json` + `rules/` + `skills/` + `agents/` + `harness/` + lazy MCP wrappers |
| `claude` | `CLAUDE.md` + `settings.json` (same Python hooks) + `skills/` + `agents/` + `HOOKS.md` |
| `codex` | `AGENTS.md` + `rules/gsh.md` + `skills/` + `~/.agents/skills` + `HOOKS.md` |
| `windsurf` | `AGENTS.md` + `.windsurfrules` + `.windsurf/rules` + `skills/` + `HOOKS.md` |
| `cline` | `AGENTS.md` + `.clinerules/gsh.md` + `skills/` + `HOOKS.md` |
| `roo` | `AGENTS.md` + `.roo/rules` + `.roomodes` + `skills/` + `HOOKS.md` |
| `continue` | `AGENTS.md` + `config.yaml` + `rules/gsh.md` + `skills/` + `HOOKS.md` |
| `copilot` | `copilot-instructions.md` + `instructions/` + `prompts/` + `skills/` + `HOOKS.md` |
| `opencode` | `AGENTS.md` + `opencode.json` + `rules/gsh.md` + `skills/` + `HOOKS.md` |
| `gemini` | `GEMINI.md` + `rules/gsh.md` + `skills/` + `HOOKS.md` |
| `aider` | `CONVENTIONS.md` + `.aider.conf.yml` + `skills/` + `HOOKS.md` |
| `zed` | `AGENTS.md` + `.rules` + `settings.json` + `skills/` + `HOOKS.md` |
| `amazonq` | `AGENTS.md` + `rules/gsh.md` + `skills/` + `HOOKS.md` |
| `trae` | `AGENTS.md` + `rules/gsh.md` + `skills/` + `HOOKS.md` |
| `junie` | `AGENTS.md` + `guidelines.md` + `skills/` + `HOOKS.md` |
| `grok` / `deepseek` | `AGENTS.md` + `rules/gsh.md` + `skills/` + `HOOKS.md` |
| `kimi` | `AGENTS.md` + `rules/gsh.md` + `skills/` + `HOOKS.md` |
| `qwen` | `QWEN.md` + `AGENTS.md` + `rules/gsh.md` + `skills/` + `HOOKS.md` |
| `legacy` | cursor, claude, codex, grok, deepseek |
| `all` (default) | all 19 tools above |

### Isolate probe (do this first)

```bash
python -m gsh setup \
  --isolate-root /tmp/gsh-probe \
  --workspace /tmp/gsh-probe/ws \
  --tools all \
  --profile full \
  --yes

python -m gsh verify \
  --isolate-root /tmp/gsh-probe \
  --workspace /tmp/gsh-probe/ws \
  --tools all
```

Green `verify` means: catalog parses, IDs are unique, crafts are not pre-expanded, no secrets or machine paths, each selected tool home matches root `skills/` byte-for-byte, and the pack no longer stores a second `cursor/skills` tree.

### Sync and uninstall

```bash
python -m gsh sync --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --yes
python -m gsh uninstall --isolate-root /tmp/gsh-probe --yes
```

Uninstall follows `install-state.json`. It keeps a user `mcp.json` and never touches official studio tables.

---

## Start here

1. Open the **studio root**, not only this repo.
2. Fill `.harness/surfaces.json` placeholders on your machine. Do not commit real drive letters back to GSH.
3. Scope first: read `skills/route-task/SKILL.md`, write `loadplan.json`, run the roster generator.
4. Boot only the current card and named bodies. Do not paste `catalog.json` into the thread.
5. Default `write_class` is `sandbox`. Promote only with a human and a changeset merge.
6. Close an item only after `verify-report.json` exists and `verdict` is `pass`.

End-to-end game path: [docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md).

---

## Mental model

```text
[request]
  → L2 director names catalog ids
  → L3 slice (craft opens step one only)
  → limited context
  → sandbox work
  → verify report
  → human promote
```

A model cannot hold a full production pipeline. Dumping 106 skills makes it play combat numeric, client, and QA at once, then touch engine assets before the GDD is frozen.

L2 handshakes L3 with an explicit file contract. Crafts are paths, not checklists. MCPs stay lazy. The four layers stay four because each one blocks a different crash. See [Design philosophy](#design-philosophy) and [Layer deep dives](#layer-deep-dives).

---

## Design philosophy

GSH is written for the people in the production room: producers, TDs, leads. They have to say what this vertical slice must prove, then keep the model on that one job for the next hour. Every rule below comes from an accident that keeps happening on a real floor.

### The window is scarce

A session can hold only a short working set. The catalog has 106 skills, 35 crafts, two canon files, and a pile of ADRs. If boot pastes the whole menu, the craft path, and the lore bible at once, the model cross-plays on step one: it edits a damage formula, talks about save migration, and writes "just for now" into an official table.

Boot therefore reads four things: the constitution, the current card, named bodies, and memory hit by `retrieve_keys`. Other skills open when that step starts. `minimal` / `core` / `full` decide which files land on disk, not what this turn stuffs into the window.

### A craft is a path, not a pre-expanded dump

Game production is a multi-craft pipeline. A combat-numeric path may be: anchor table → formula order → skill coefficients → acceptance. If naming a craft reads every `uses_skills` body, step one fills tables with step-five language before the primary key is frozen.

`activated.json` writes only `craft_open` (the first step). Later skills open when you reach them. The craft file is the map. The skill file is the procedure. The model is the worker for this step, not the whole department.

### Official surfaces are irreversible

Design tables, engine assets, and committed history cost real people to roll back. The model does not feel that cost.

Default `write_class` is `sandbox`. Isolation roots live in `.harness/surfaces.json`. Promote only when a human approves, the changeset merges record cells, and `verify-report.json` has `verdict: pass`. Changing the official table first and "writing the report later" is an incident.

### Sessions die. Tools change.

A producer may scope in Cursor at noon and finish the same slice in another client at night. Chat history is not the archive.

The current card is `.harness/sessions/<id>/current.md`. State is `state.json`. The audit log is `tasks.jsonl` (append-only). The roster is `activated.json`. After a tool switch, open the studio root and read the card. Do not rely on "I remember what we said this morning." Probe sessions start with `_` so fixtures do not overwrite `LATEST`.

### Verbal "green" cannot close an item

"Feels fine", "the hook was quiet", and "I played it a bit" are not acceptance. Close requires a file: `verify-report.json` with `bead_id`, `verify_kind`, `command`, an integer `exit_code`, a non-empty `evidence_paths` list, and `verdict: pass`.

Cursor's `stop` hook checks that report. Claude Code `settings.json` points `Stop` at the same `hooks/结束.py`. Other tools have no event runtime; `HOOKS.md` tells you to open the report yourself. No `pass`, no close.

### Hosts stay asleep

Every MCP handshakes, lists tools, and holds a host process at IDE start. Wiring 36 purposes as eager stdio hangs boot and spends the window on tool descriptions.

`mcp-tiers.json` `core` is a handshake list, not an installed-server list. This pack ships **0** live servers and 36 purpose stubs. Real start goes through `lazy_stdio` and `拉起外接.py`. excelMCP in core means the table pipeline wants that tier key; you still install the host on the machine.

### Secrets never enter the model

Once `.env`, `credentials.json`, or a private key lands in context, it can ride logs, session sync, and prompt caches.

Cursor `beforeReadFile` and Claude `PreToolUse` / `Read` block common secret paths. `mcp.json.example` is placeholders only. Setup never overwrites an existing `mcp.json`. `verify` scans user-profile absolute paths, hard-coded host roots, and live `ghp_` / `sk-` tokens.

### Destructive shell needs friction

`git reset --hard`, force-push, and recursive deletes can erase a human afternoon. Cursor `beforeShellExecution` and Claude `PreToolUse` / `Bash` ask for confirm. Other tools write the same rule into `HOOKS.md`: no human nod, no run.

### One content tree, many complete native installs

A studio will not stay on a single client. Someone opens Cursor, someone opens Claude Code, CI runs Codex, someone else uses Copilot for a one-line fix. Content stays one copy: repo-root skills, crafts, rules, hooks, runtime.

After setup, each tool home is the **full layout that tool already understands**: entry files, rule directories, skill tree, craft tree, hooks or the closest equivalent, an MCP example, and `gsh-capability.json`. The repo does not store a second skill forest. Open this pack and read root `skills/`. Edit once, then `gsh sync` realigns every installed native tree.

```mermaid
flowchart LR
  L1[L1 Constitution<br/>rules and hooks]
  L2[L2 Director<br/>loadplan and roster]
  L3[L3 Capability<br/>skills / crafts / stubs]
  L4[L4 Filing<br/>surfaces and evidence]
  L1 --> L2 --> L3 --> L4
  L4 -->|current card| L1
```

---

## What's inside

```text
game-studio-harness/
├── skills/ agents/ rules/ hooks/ harness/   # single source of truth
├── gsh/                                     # Python 3.11+ CLI
├── studio/.harness/                         # empty L4 scaffold
├── .cursor/                                 # Cursor native conventions (no skills tree)
├── .claude/ .codex/ .roo/ …                 # per-tool native entries and rules
├── GEMINI.md CONVENTIONS.md QWEN.md
├── docs/ tests/
```

The pack does not store a second `cursor/skills` tree. Full skill trees appear only in installed tool homes.

---

## Key concepts

| Concept | One line |
|---|---|
| Four layers | Constitution / director / capability / filing. Frozen |
| Craft | `agents/<id>.md`. A path. Do not pre-expand |
| Skill | `skills/<id>/SKILL.md`. Reusable procedure. No session numbers |
| Hook | Python gates invoked by Cursor `hooks.json` and Claude `settings.json`; other tools ship `HOOKS.md` |
| Rule | Always-on thin tax |
| Filing | `.harness` files, not a knowledge graph |
| Catalog | Generated ID menu after setup |
| Profile | minimal / core / full |
| Isolate root | Probe tree that does not write real homedirs |

---

## Layer deep dives

Every module below: **what it handles / what it solves / paths / crash if absent**.

### L1 Constitution

Always-on tax. Stay thin. No table recipes. No session TTK numbers.

#### `rules/全局.mdc`

- **Handles:** lifecycle, boot read order, roster semantics (named ids, absorb `needs_mcp`, do not pre-expand crafts, allow mid-session opens), continue/steer/park/new/parallel, required loadplan fields, step-by-step craft walking, evidence on close, L4 table map, freeze.
- **Solves:** invented workflows; catalog pasted as a system prompt; reading a whole craft path on boot.
- **Paths:** `rules/全局.mdc` → `~/.cursor/rules/全局.mdc`; repo-local `.cursor/rules/全局.mdc`.
- **If absent:** no read order, no "do not pre-expand". The agent cross-plays roles and fills step-5 tables during step 1.

#### `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` / `CONVENTIONS.md` / `QWEN.md`

- **Handles:** the same constitution under the filename each tool already opens.
- **Solves:** keeping read-order, write isolation, and close evidence after a client switch.
- **Paths:** repo-root entry files; `setup --workspace` writes them onto the studio root.
- **If absent:** the client that opens the studio root has no four-layer entry and becomes generic chat.

#### `hooks/hooks.json`

- **Handles:** `sessionStart`, `beforeShellExecution`, `beforeReadFile`, `stop`.
- **Solves:** rules that never become runtime.
- **Paths:** `hooks/hooks.json` → `~/.cursor/hooks.json`.
- **If absent:** hook scripts never run.
- **Honest:** Cursor only. This is not a Claude hook pack.

#### `hooks/开场.py`

- **Handles:** refresh stale catalog; optional MCP probe; print current-card digest; set `HARNESS_*`.
- **Solves:** dumping 100+ skill blurbs on boot; not knowing the session.
- **If absent:** first reply guesses progress and invents catalog ids.

#### `hooks/工作区.py`

- **Handles:** walk up to `.harness`; read `LATEST`; assemble env.
- **Solves:** hardcoded paths when several IDEs share one studio.
- **If absent:** boot cannot find the studio; close cannot see `bead_id`.

#### `hooks/读文件前.py`

- **Handles:** deny `.env`, credentials, PEM, SSH, AWS, GnuPG paths.
- **Solves:** secrets entering the model.
- **If absent:** "just debugging" reads production keys. Cursor only.

#### `hooks/命令前.py`

- **Handles:** confirm force-push / hard reset / clean -x; block close without a passing report.
- **Solves:** silent destruction of local work; verbal green closes.
- **If absent:** `git reset --hard` after a failed experiment.

#### `hooks/结束.py`

- **Handles:** on `completed`, validate report schema and verdict; follow up if `current.md` is missing.
- **Solves:** handing off a fail as done.
- **If absent:** sessions look finished without evidence.

#### `hooks/校验验证报告.py`

- **Handles:** required fields and enums for `verify-report.json`.
- **Solves:** a Chinese paragraph that says "passed".
- **If absent:** close gates cannot decide.

#### `hooks/数据就绪预检.py`

- **Handles:** framework workbooks from env + `surfaces.json` only. No studio drive letters in source.
- **Solves:** balance passes on missing books.
- **If absent:** combat sim runs on empty sheets.

#### Hook thin delegates

`hooks/建议执行单.py` and `hooks/生成会话能力名单.py` delegate to `harness/scripts/`. They resolve via `gsh_paths` / relative layout so isolate roots work.

---

### L2 Director

The director is not the worker.

#### `skills/route-task/SKILL.md`

- **Handles:** restate goal/deliverable/boundary; pick catalog ids; set tier and write class; write loadplan; decide subagents.
- **Solves:** editing tables on the first token.
- **If absent:** no contract for later layers.

#### `harness/scripts/生成会话能力名单.py`

- **Handles:** validate ids; write `craft_open` only; absorb `needs_mcp`; write `activated.json` and the current card.
- **Solves:** injecting eight craft skills at once.
- **If absent:** boot cannot see a roster.

#### `activated.json` / `current.md` / `loadplan.json`

- **Handles:** the auditable slice, the amnesia card, the machine-readable plan.
- **Solves:** "I named combat numeric" living only in chat.
- **If absent:** hooks have no `HARNESS_CRAFT_OPEN`; compaction wipes the thread.

#### `harness/scripts/建议执行单.py`

- **Handles:** execution skills before close skills.
- **Solves:** writing the handoff before the formula.
- **If absent:** order depends on model mood.

---

### L3 Capability library

#### Catalog

`刷新菜单.py` scans frontmatter and MCP stubs into `catalog.json`. Without it, directors invent ids.

#### Skills (106)

Reusable procedures. No session numbers. Index: [docs/skills/index.md](docs/skills/index.md).

Domains: director/close, memory/promote, isolation/layout, tables, direction/scope, combat/numeric, economy/monetization, narrative/level/UX, art/audio/tech-art, engineering/QA, liveops/MCP.

If a domain is missing, the model invents field names and promote rules for that work.

#### Crafts (35)

Job paths. `combat-numeric-designer` walks model → attributes → formula/counter/skill table → corners → table diff. Index: [docs/crafts/index.md](docs/crafts/index.md).

If crafts are missing you can still name loose skills, but you lose recommended order and duty fences. Different crafts should be different subagents.

#### MCP tiers and lazy stdio

`mcp-tiers.json` lists `excelMCP` as a **core tier key**. That means "handshake on boot *if you wired it locally*". It does **not** mean this repo ships an Excel MCP server.

`lazy_stdio.py` exposes cached tool declarations and starts the child on first `tools/call`. Without it, a 36-server `tools/list` storm freezes Cursor boot.

#### 36 `mcp-tools/*.json` stubs

Purpose text for the catalog. **Live servers shipped: 0.** See [docs/mcp-policy.md](docs/mcp-policy.md).

#### `mcp.json.example`

Placeholder launch templates. `${PYTHON}` `${MCP_BOOT}` `${HARNESS_APPS}` `${LARK_APP_ID}`. Setup never overwrites an existing `mcp.json`.

#### Apply-tiers / boot / handshake scripts

`应用外接档位.py`, `拉起外接.py`, `mcp-autostart`, `握手四层.py`, `回归四层.py`, `接线自检.py`, `整接.py` keep lazy wrapping and four-layer regressions honest. Probe sessions starting with `_` must not write `LATEST`.

---

### L4 Filing cabinet

Files, not a graph. Scaffold: `studio/.harness/` with empty data.

#### `surfaces.json` / `write-isolation`

Official ↔ sandbox for tables, git, engine, assets. Crash if absent: trial writes hit official xlsx / mainline / Content.

#### `state.json` / `tasks.jsonl` / `sessions/`

Current row, append-only ledger, per-session contract. Crash if absent: new windows guess progress.

#### `canon/` / `adr/` / retrieve / promote skills

Approved facts open only on `retrieve_keys`. Crash if absent: hallway talk becomes canon, or boot scans the whole bible.

#### `verify-gate` / `verify-report.json` / `artifacts/index.jsonl`

Tiered evidence. Crash if absent: L1 cannot close.

#### `项目库.py` / `目录夹具.py`

Write the current card and state. Fixtures read the catalog instead of hard-coding a studio craft name.

---

## CLI

```text
python -m gsh setup | sync | verify | doctor | uninstall
```

`install-state.json` records profile, tools, and files.

### `setup` flags

`--workspace`, `--cursor-only`, `--tools`, `--profile`, `--isolate-root`, `--write-mcp`, `--guided`, `--yes`, `--dry-run`, `--pack-root`.

### `sync`

Re-projects from repo root. This is the only legal way to keep adapters aligned after you edit a skill.

### `verify`

Exit 2 on failure. Checks SSOT, unique IDs, no pre-expand, full native trees in selected homes, projection bytes, secret scan, workspace native entries.

### `doctor`

Read-only drift report. Exit 1 if issues.

### `uninstall`

Removes projections. Keeps `mcp.json`. Does not delete official surfaces.

---

## Platform support

This table is what lands on disk and who executes hooks. Every selected tool receives a complete skill/craft tree and its native entry files.

| Tool | Native entry | Skill/craft tree | Hooks | Other native files |
|---|---|---|---|---|
| Cursor | `rules/全局.mdc` | yes | **runs** `hooks.json` | `harness/`, lazy MCP |
| Claude Code | `CLAUDE.md` | yes | **runs** `settings.json` → same `hooks/*.py` | `HOOKS.md` (event names differ) |
| Codex | `AGENTS.md` | yes (plus `~/.agents/skills`) | convention / `HOOKS.md` | `rules/gsh.md` |
| Windsurf | `AGENTS.md` + `.windsurfrules` | yes | convention / `HOOKS.md` | `.windsurf/rules` |
| Cline | `AGENTS.md` | yes | convention / `HOOKS.md` | `.clinerules/` |
| Roo Code | `AGENTS.md` | yes | convention / `HOOKS.md` | `.roo/rules`, `.roomodes` |
| Continue.dev | `AGENTS.md` | yes | convention / `HOOKS.md` | `config.yaml`, `rules/gsh.md` |
| GitHub Copilot | `copilot-instructions.md` | yes | convention / `HOOKS.md` | `instructions/`, `prompts/` |
| OpenCode | `AGENTS.md` | yes | convention / `HOOKS.md` | `opencode.json` |
| Gemini CLI | `GEMINI.md` | yes | convention / `HOOKS.md` | `rules/gsh.md` |
| Aider | `CONVENTIONS.md` | yes | convention / `HOOKS.md` | `.aider.conf.yml` |
| Zed | `AGENTS.md` + `.rules` | yes | convention / `HOOKS.md` | `settings.json` |
| Amazon Q | `AGENTS.md` | yes | convention / `HOOKS.md` | `rules/gsh.md` |
| Trae | `AGENTS.md` | yes | convention / `HOOKS.md` | `rules/gsh.md` |
| JetBrains Junie | `guidelines.md` | yes | convention / `HOOKS.md` | `AGENTS.md` |
| Grok | `AGENTS.md` | yes | convention / `HOOKS.md` | `rules/gsh.md` |
| DeepSeek | `AGENTS.md` | yes | convention / `HOOKS.md` | `rules/gsh.md` |
| Kimi Code | `AGENTS.md` | yes | convention / `HOOKS.md` | `rules/gsh.md` |
| Qwen Code | `QWEN.md` | yes | convention / `HOOKS.md` | `AGENTS.md`, `rules/gsh.md` |

If `~/.continue/config.yaml` already exists, treat the GSH copy as a merge source and read the diff before replacing your file.

Per-tool notes: [docs/adapters/](docs/adapters/). Cross-harness: [docs/architecture/cross-harness.md](docs/architecture/cross-harness.md).

---

## Token / context

| Practice | Saves |
|---|---|
| Thin L1 | per-turn tax |
| No full catalog on boot | 100+ descriptions |
| Crafts not pre-expanded | the rest of a job path |
| `retrieve_keys` for canon | the lore bible |
| Lazy MCP | boot `tools/list` and host processes |
| minimal/core profiles | skills you will not use |
| Truncated current card | boot injection |

Anti-patterns: catalog as system prompt; 35 craft bodies inside `AGENTS.md`; 36 MCPs as eager stdio.

---

## Security

- No secrets in git. Example MCP files are placeholders.
- Setup does not overwrite `mcp.json`.
- Cursor `beforeReadFile` blocks common secret paths (Cursor only).
- Destructive git asks (Cursor only).
- `verify` and `tests/test_no_secrets.py` scan user paths, `Harness-Apps`, `ghp_` / `sk-`.
- Private GitHub advisories: [SECURITY.md](SECURITY.md).

---

## Troubleshooting

| Symptom | First move |
|---|---|
| verify: missing catalog | setup then verify with the same isolate root |
| projection drifted | `python -m gsh sync`; do not hand-edit `~/.cursor/skills` |
| `cursor/skills` still in the repo | you are on the 0.1 layout |
| Cursor hooks silent | `--tools cursor` was not installed, or the IDE is reading another hooks.json |
| Claude hooks silent | confirm `~/.claude/settings.json` and that `hooks/*.py` resolve from the working directory |
| all 36 MCPs red | expected; this repo ships zero live servers |
| excelMCP is core but offline | tier ≠ shipment |
| craft talks promote on step 1 | roster was pre-expanded |
| doctor: old Python | install 3.11+ |
| uninstall deleted mcp.json | should not happen; restore backup and file an issue |

---

## Tests

```bash
python -m unittest discover -s tests -v
```

`test_catalog`, `test_unique_ids`, `test_craft_no_preexpand`, `test_no_secrets`, `test_projection_thin`, `test_native_homes`, `test_cli_isolate`.

---

## Migrating from the 0.1 five-tree layout

| Old | New |
|---|---|
| `cursor/skills/` | `skills/` |
| `cursor/agents/` | `agents/` |
| `cursor/rules/` | `rules/` |
| `cursor/hooks*` | `hooks/` |
| `cursor/harness/` | `harness/` |
| `cursor/constitution.md` | `AGENTS.md` |
| five full tool trees | deleted; projected by setup/sync |
| `install/install.py` | `python -m gsh setup` |

Move any local-only skill edits onto repo-root `skills/`, then sync. Probe in an isolate root before writing real homedirs. Existing `mcp.json` is kept. Studio `.harness` sessions are merged, not wiped.

---

## Session lifecycle

```text
new item → loadplan → generate roster → read current card
→ sandbox work → verify-report → sync-state
→ human promote (changeset only) → close
```

Continue: same chat, same open deliverable, incremental plan.  
Steer: change the plan first.  
Park: stop the old card, new session for the interrupt.  
Parallel: independent sessions; different crafts become subagents.

Sessions whose names start with `_` must not write `LATEST`.

---

## Schemas (summary)

**loadplan.json** — required `session_id`, `tier`, `items`, `verify_kind`, `intent`, `work_mode`. Suggested `write_class`, `retrieve_keys`, `forbid`, `bead_id`. `why` ≥ 8 characters.

**activated.json** — `ok`, `skills`, `crafts`, `craft_open`, `mcp_allow`. `skills` must not equal the full `uses_skills` of a named craft.

**verify-report.json** — `bead_id`, `verify_kind`, `command`, integer `exit_code`, non-empty `evidence_paths`, `verdict` pass|fail.

**surfaces.json** — `id`, `kind`, `official`, `sandbox`, `note`. Placeholders only in this repo.

**mcp-tiers.json** — `core` is a handshake list, not an availability list.

---

## Domain crash table

| Domain uninstalled | Crash |
|---|---|
| Director / close | no contract, no close |
| Memory / promote | hallway talk becomes canon |
| Isolation / layout | official mixed with drafts |
| Tables | whole-file xlsx overwrite |
| Direction / scope | features bloat; pillars cannot veto |
| Combat / numeric | formula order drifts |
| Economy / IAP | sources and sinks break |
| Narrative / level / UX | beats and quests desync |
| Art / audio / tech-art | naming and sockets ungated |
| Engineering / QA | no contract, no regression pack |
| Liveops / MCP | calendar collisions; eager MCP boot hang |

`minimal` only guarantees director/isolation/close. Combat tables need `core` or `full`.

---

## Craft-group crash table

| Group uninstalled | Crash |
|---|---|
| Production / direction | no packages, no cuts, no milestone evidence |
| Systems / numeric | GDD and table keys diverge |
| Narrative / level / UX | quest SM, beats, blockout, five-states desync |
| Engineering | client presentation treated as authority |
| QA | cases and automation maps break |
| Art / audio | briefs cannot enter 3D; bind/VFX paths missing |

Craft bodies list skill ids only. Session numbers do not belong in `agents/*.md`.

---

## Runtime script table

| Script | Layer | If absent |
|---|---|---|
| `刷新菜单.py` | L3 | no catalog |
| `生成会话能力名单.py` | L2 | no activated/current |
| `建议执行单.py` | L2 | close before work |
| `项目库.py` | L4 | amnesia |
| `目录夹具.py` | tests | fixtures hard-code a game |
| `gsh_paths.py` | all | hooks hard-code `~/.cursor` |
| `应用外接档位.py` | L3 | eager MCP |
| `拉起外接.py` | L3 | handshake with a dead host |
| four-layer regressions | tests | pre-expand returns silently |

---

## Open this repo vs open a studio root

This repo is for editing skills, hooks, and the CLI. Do not put real table roots here. A studio root is for making the game; `.harness` is the filing cabinet. `setup --workspace` only fills missing L4 files.

---

## Environment variables

`GSH_PACK_ROOT`, `GSH_ISOLATE_ROOT`, `GSH_HOME`, `CURSOR_HOME`, `CLAUDE_HOME`, `CODEX_HOME`, `GROK_HOME`, `DSH_HOME`, `ROO_HOME`, `AIDER_HOME`, `ZED_HOME`, `AMAZONQ_HOME`, `TRAE_HOME`, `JUNIE_HOME`, `KIMI_HOME`, `QWEN_HOME`, `AGENTS_SKILLS`, `HARNESS_ROOT`, `HARNESS_SESSION`, `HARNESS_HOST_PATHS`, `FRAMEWORK_WORKBOOK`, `BATTLE_SIM_WORKBOOK`, `DATA_READY_SHEETS`.

Isolate mode uses directory convention and does not require these.

---

## Common production mistakes

1. Treating a craft as a skill dump.
2. Pasting `catalog.json` into a system prompt.
3. Committing real studio paths into GSH.
4. Claiming 36 live MCPs.
5. Skipping `current.md` and `verify-report.json` on a tool that only ships `HOOKS.md`.
6. Editing `~/.claude/skills` instead of repo-root `skills/`.
7. Copying a second `cursor/skills` tree into the pack.
8. Whole-file overwrite of official xlsx.
9. Probe sessions writing `LATEST`.
10. Treating Copilot instructions as a secret-read hook. Copilot still gets a full skill tree and prompts; a human must read `verify-report.json`.

---

## Cookbook

[docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md): isolate install → loadplan names `combat-numeric-designer` → confirm no pre-expand → do `craft_open` only → sandbox tables → T1 report → human promote.

Swap the craft id for progression or economy. Isolation and no-pre-expand stay mandatory.

---

## Doc map

Architecture L1–L4, cross-harness, MCP policy, skill index, craft index, per-adapter pages, cookbook: all under [docs/](docs/).

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

1. Edit skills only under `skills/<id>/SKILL.md`.
2. Edit crafts only under `agents/<id>.md`.
3. New MCP: purpose stub + placeholders. No live server, no secret.
4. Architecture changes need a steer, a new plan, and an ADR.
5. PRs need isolate `verify` green and `unittest` green.

---

## FAQ

**Why is Chinese the primary README?**  
Because the production audience is a Chinese game pipeline. This file is the English twin.

**Why do skill files still mention `~/.cursor/...`?**  
That is the Cursor runtime landing zone after setup. Source of truth is repo-root `skills/`.

**Can I install only a few skills into Claude?**  
Yes: `--profile minimal|core --tools claude`. Do not maintain a second tree.

**Isolate root vs workspace?**  
Isolate fakes homedirs. Workspace holds the game and `.harness`. Verify checks both.

**Why does verify fail if `cursor/skills` exists in the pack?**  
Skill bodies belong at repo-root `skills/` and in installed homes. A second tree in the pack makes `sync` lose its single door.

**Do hooks run on Windows?**  
Yes, if Python 3.11+ is on PATH.

**May I add skill 107?**  
Yes, at `skills/<id>/SKILL.md`, then sync. Never copy it into adapters by hand.

**May I add a fifth layer?**  
Not casually. Steer, replan, write an ADR. See the freeze canon file.

**Does my tool run GSH hooks?**  
Cursor executes `hooks.json`. Claude Code executes `settings.json` against the same Python scripts. Every other tool ships `HOOKS.md`: open `current.md` yourself and refuse to close without a `verify-report.json`.

---

## Install-state and shared runtime

After setup, the shared runtime lives at `~/.gsh` (or `<isolate>/gsh`):

```text
gsh/
  AGENTS.md
  install-state.json
  gsh-adapter.json
  skills/ agents/ rules/ hooks/
  harness/          # scripts, catalog.json, mcp-tools, mcp-boot, mcp-tiers.json
  mcp.json.example
```

Each selected tool then receives its own complete native tree under that tool's home. Cursor executes `hooks.json`. Claude Code executes `settings.json`. The others land entry files, rules, skills, crafts, and `HOOKS.md`.

`install-state.json` is how `sync` and `uninstall` know what this machine asked for. If you delete it, `sync` falls back to the CLI flags you pass.

Do not treat `~/.cursor/skills` as a second source of truth. If it drifted, overwrite it from the pack with `sync`. If you meant the edit, move it to repo-root `skills/` first.

When in doubt, open `current.md` yourself and refuse to close without a `verify-report.json`.

## License

[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · [LICENSE](LICENSE) MIT · [CHANGELOG.md](CHANGELOG.md)

The four layers are frozen. Hallway talk is not canon. Write isolation is the default tooth. Secrets stay out of git.

The only official source is the GitHub repository
[limoaCatherine/game-studio-harness](https://github.com/limoaCatherine/game-studio-harness).

Third-party re-uploads are not reviewed.
