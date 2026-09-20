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
  <a href="#layer-deep-dives">Layer deep dives</a> ·
  <a href="#platform-support">Platform support</a> ·
  <a href="docs/mcp-policy.md">MCP policy</a>
</p>

<p align="center">

| Crafts | Skills | MCP policy | Adapters |
| :---: | :---: | :---: | :---: |
| 35 crafts | 106 skills | **0** live servers shipped / 36 purpose stubs | Cursor full runtime · everyone else degraded |

</p>

> Context windows are scarce. Official surfaces are irreversible. Sessions die.
>
> GSH is not a prompt pack and not a DCC plugin. It is a **context OS** for LLM agents inside a real game-production pipeline.

> [!WARNING]
> **Official sources only.** Install from [github.com/limoaCatherine/game-studio-harness](https://github.com/limoaCatherine/game-studio-harness). Third-party zips and mirrors are unreviewed and may ship hostile hooks or a live `mcp.json`. This repo is MIT. It does not vendor DCC binaries or studio absolute paths.

---

## Install

**Python 3.11+**. Windows game-production machines are first-class; Linux/macOS are for isolate probes and CI. The installer **does not** install Excel, Blender, Unity, or FMOD, and **does not** write secrets.

> [!IMPORTANT]
> **Pick one install path per harness.** Do not run setup and then hand-copy `skills/` into five tool trees. The five full copies are gone. The only source of truth is repo-root `skills/`, `agents/`, `rules/`, `hooks/`, `harness/`.

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

| `--tools` | Behavior |
|---|---|
| `cursor` | **Full runtime**: hooks + rules + skills + agents + harness + lazy MCP wrappers |
| `claude` | `CLAUDE.md` + skill/craft projection. No GSH hooks |
| `codex` | `AGENTS.md` + skill projection (including `~/.agents/skills`) |
| `grok` / `deepseek` | `AGENTS.md` + skill projection. No hooks |
| `windsurf` / `cline` / `opencode` / `gemini` | Instruction file + optional skill copy |
| `continue` | `AGENTS.md` + a snippet you merge yourself |
| `copilot` | **Instructions only** |
| `legacy` | cursor,claude,codex,grok,deepseek |
| `all` | Includes doc-level adapters. **Not** feature parity |

### Isolate probe (do this first)

```bash
python -m gsh setup \
  --isolate-root /tmp/gsh-probe \
  --workspace /tmp/gsh-probe/ws \
  --tools legacy \
  --profile full \
  --yes

python -m gsh verify \
  --isolate-root /tmp/gsh-probe \
  --workspace /tmp/gsh-probe/ws \
  --tools legacy
```

Green `verify` means: catalog parses, IDs are unique, crafts are not pre-expanded, no secrets or machine paths, Cursor projection matches root `skills/` byte-for-byte, and the pack no longer contains five `*/skills` trees.

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

GSH does not rely on "please focus". L2 handshakes L3 with an explicit file contract. Crafts are paths, not checklists. MCPs stay lazy.

The four layers do not collapse to three. Each layer exists because of a distinct crash mode.

---

## What this is not

- Not an ECC reskin. ECC is general software engineering. GSH is a game-production four-layer OS.
- Not a Unity / Unreal / Excel marketplace. No DCC binaries.
- Not a cloud service. No account. No required remote model.
- Not "36 MCPs ready to go". See the MCP policy.
- Not feature parity across five tools. Cursor has hooks. Copilot has instructions.
- Not a roleplay prompt pack. Crafts are path files. Skills are procedure files. Gates are scripts.

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
├── .cursor/                                 # thin adapter (no skills tree)
├── .claude/ .codex/                         # constitution projections
├── docs/ tests/
```

The old `cursor/skills`, `claude/skills`, `grok/skills`, `deepseek/skills`, `codex/skills` trees are **deleted**. Do not bring them back.

---

## Key concepts

| Concept | One line |
|---|---|
| Four layers | Constitution / director / capability / filing. Frozen |
| Craft | `agents/<id>.md`. A path. Do not pre-expand |
| Skill | `skills/<id>/SKILL.md`. Reusable procedure. No session numbers |
| Hook | Hard gate on Cursor events. Other tools do not run them |
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

#### `AGENTS.md` / `CLAUDE.md`

- **Handles:** the same constitution for tools without Cursor rules.
- **Solves:** Claude/Codex/Grok opening a studio root with zero GSH entry.
- **Paths:** repo root plus `.claude/` and `.codex/` projections.
- **If absent:** instruction-only tools become generic chat.

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

Exit 2 on failure. Checks SSOT, thin adapters, unique IDs, no pre-expand, projection bytes, secret scan, workspace scaffold.

### `doctor`

Read-only drift report. Exit 1 if issues.

### `uninstall`

Removes projections. Keeps `mcp.json`. Does not delete official surfaces.

---

## Platform support

**No fake parity.**

| Capability | Cursor | Claude | Codex | Grok | DeepSeek | Windsurf | Cline | Continue | Copilot | OpenCode | Gemini |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Constitution | rules + AGENTS | CLAUDE.md | AGENTS.md | AGENTS.md | AGENTS.md | AGENTS.md | AGENTS.md | snippet | instruction | AGENTS.md | GEMINI.md |
| Skill projection | yes | yes | yes | yes | yes | optional | optional | no* | no | optional | optional |
| `hooks.json` runtime | **yes** | no | no | no | no | no | no | no | no | no | no |
| Boot current card | **auto** | convention | convention | convention | convention | convention | convention | convention | convention | convention | convention |
| Secret read gate | **yes** | no | no | no | no | no | no | no | no | no | no |
| Close verify gate | **yes** | convention | convention | convention | convention | convention | convention | convention | convention | convention | convention |
| lazy MCP wrapper | **wireable** | product MCP | product MCP | usually none | usually none | product MCP | product MCP | product MCP | none | product MCP | product MCP |

\*Continue: merge the snippet yourself. GSH will not overwrite your `config.yaml`.

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
| Cursor hooks silent | you did not install `--tools cursor` |
| Claude skips the current card | expected; open `current.md` yourself |
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

`test_catalog`, `test_unique_ids`, `test_craft_no_preexpand`, `test_no_secrets`, `test_projection_thin`, `test_cli_isolate`.

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

`GSH_PACK_ROOT`, `GSH_ISOLATE_ROOT`, `GSH_HOME`, `CURSOR_HOME`, `CLAUDE_HOME`, `CODEX_HOME`, `GROK_HOME`, `DSH_HOME`, `AGENTS_SKILLS`, `HARNESS_ROOT`, `HARNESS_SESSION`, `HARNESS_HOST_PATHS`, `FRAMEWORK_WORKBOOK`, `BATTLE_SIM_WORKBOOK`, `DATA_READY_SHEETS`.

Isolate mode uses directory convention and does not require these.

---

## Common production mistakes

1. Treating a craft as a skill dump.
2. Pasting `catalog.json` into a system prompt.
3. Committing real studio paths into GSH.
4. Claiming 36 live MCPs.
5. Expecting Cursor hooks inside Claude.
6. Editing `~/.claude/skills` instead of repo-root `skills/`.
7. Reintroducing five maintained trees.
8. Whole-file overwrite of official xlsx.
9. Probe sessions writing `LATEST`.
10. Treating Copilot as a full runtime.

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

**Why does verify fail if `cursor/skills` exists?**  
That is the 0.1 failure mode this refactor removes.

**Do hooks run on Windows?**  
Yes, if Python 3.11+ is on PATH.

**May I add skill 107?**  
Yes, at `skills/<id>/SKILL.md`, then sync. Never copy it into adapters by hand.

**May I add a fifth layer?**  
Not casually. Steer, replan, write an ADR. See the freeze canon file.

**Does my tool run GSH hooks?**  
Only Cursor. If the matrix cell is not Cursor, open `current.md` yourself and refuse to close without a `verify-report.json`.

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

Cursor then receives a full projection under `~/.cursor`. Claude/Codex/Grok/DeepSeek receive a constitution file plus copied skills/agents. Copilot receives instructions only.

`install-state.json` is how `sync` and `uninstall` know what this machine asked for. If you delete it, `sync` falls back to the CLI flags you pass.

Do not treat `~/.cursor/skills` as a second source of truth. If it drifted, overwrite it from the pack with `sync`. If you meant the edit, move it to repo-root `skills/` first.

If you are unsure whether a tool has GSH hooks: it does not, unless the matrix cell says Cursor. When in doubt, open `current.md` yourself and refuse to close without a `verify-report.json`.

## License

[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · [LICENSE](LICENSE) MIT · [CHANGELOG.md](CHANGELOG.md)

The four layers are frozen. Hallway talk is not canon. Write isolation is the default tooth. Secrets stay out of git.

The only official source is the GitHub repository
[limoaCatherine/game-studio-harness](https://github.com/limoaCatherine/game-studio-harness).

Third-party re-uploads are not reviewed.
