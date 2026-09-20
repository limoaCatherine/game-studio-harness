> [!WARNING]
> **Official sources only.** Install from [github.com/limoaCatherine/game-studio-harness](https://github.com/limoaCatherine/game-studio-harness). Third-party zips are unreviewed. This repo is MIT. It does not vendor production-software installers or studio absolute paths.

# Game Studio Harness

A context OS that can finish a game-production vertical slice: scope the round, walk a craft one step at a time, write in a sandbox, close with a verify report, and promote official surfaces only after a human says so.

```text
scope → slice → isolate → verify → promote
```

Install once. Then `gsh menu` names an id, `gsh next` walks the craft path, `gsh close` files the report. The window holds only this turn's working set.

[中文](README.md) · [Install](#install) · [Start using](#start-using) · [What you can run](#what-you-can-run) · [Guides](#guides)

| Crafts | Skills | Native adapters | MCP |
| :---: | :---: | :---: | :---: |
| 35 crafts | 106 skills | 19 complete native trees | 0 live servers / 36 purpose stubs |

| You get | Count | For |
|---|---:|---|
| Craft paths | 35 | Production, numeric, level, engineering, QA, art/audio |
| Skill procedures | 106 | Scope, tables, formulas, acceptance, handoff |
| Hook runtime | Cursor + Claude Code | Boot the current card, read gates, close |
| Director / resume / close CLI | `menu` `status` `resume` `next` `close` | One file contract across tools |

---

## Install

**Python 3.11+**. Windows production machines are first-class; Linux/macOS are for isolate probes and CI. The installer projects architecture files and skills.

> [!IMPORTANT]
> Edit content only at repo-root `skills/`, `agents/`, `rules/`, `hooks/`, `harness/`. `gsh setup` / `gsh sync` write that same content into each tool's complete native tree.

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

| Entry | Command |
|---|---|
| Module | `python -m gsh setup` |
| Unix | `./install.sh` |
| Windows | `.\install.ps1` or `.\一键部署.ps1` |

### Profiles

| `--profile` | Lands | Use when |
|---|---|---|
| `minimal` | 12 director/isolation/close skills + 4 crafts | Learn the four layers |
| `core` | Daily director, tables, slice, acceptance | Most production sessions |
| `full` (default) | 106 skills + 35 crafts | Full catalog on disk |

### Tools

`--tools all` (default) lands 19 complete native trees. `legacy` = cursor,claude,codex,grok,deepseek. See [Platform support](#platform-support).

### Isolate probe

```bash
python -m gsh setup \
  --isolate-root /tmp/gsh-probe \
  --workspace /tmp/gsh-probe/ws \
  --tools all \
  --profile full \
  --yes

python -m gsh verify \
  --isolate-root /tmp/gsh-probe \
  --workspace /tmp/gsh-probe/ws
```

```bash
python -m gsh sync --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --yes
python -m gsh uninstall --isolate-root /tmp/gsh-probe --yes
```

---

## Start using

Open the **studio root**, not only this repo. Fill `.harness/surfaces.json` placeholders on your machine. Do not commit real drive letters back to GSH.

| What you are doing | Start here |
|---|---|
| Scope a vertical slice | `python -m gsh menu --kind craft -q slice`, then `skills/route-task/SKILL.md` |
| Combat numeric / TTK | Name `combat-numeric-designer`, `gsh activate`, walk with `gsh next` |
| Economy / progression | `economy-numeric-designer` / `progression-numeric-designer` |
| Level blockout | `level-designer` |
| Client / server | `client-engineer` / `server-engineer` |
| QA acceptance | `qa-lead` or `qa-functional`, close with `gsh close` |
| Liveops calendar | `liveops-designer` |
| Resume after a tool switch | `python -m gsh resume` |
| See progress | `python -m gsh status` |
| Close an item | `python -m gsh close --kind smoke --evidence <artifact>` |

Daily loop:

```text
gsh menu -q ttk
  → write loadplan.json (name a craft id)
  → gsh activate <session>
  → read current.md, do the current step
  → gsh next
  → gsh close --evidence <sandbox artifact>
  → human promote of record cells
```

End-to-end: [docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md).

---

## What's inside

```text
game-studio-harness/
├── skills/                 # 106 procedures
├── agents/                 # 35 craft paths
├── rules/ hooks/ harness/  # constitution, hooks, runtime, catalog
├── gsh/                    # setup sync verify menu status next close
├── studio/.harness/        # studio scaffold
├── .cursor/ .claude/ …     # native conventions (no skill forest in the pack)
└── docs/ tests/
```

After setup the shared runtime lives at `~/.gsh` (or isolate `gsh/`). Each selected tool home gets its own complete native tree.

---

## Key concepts

| Concept | What you do with it |
|---|---|
| Four layers | Constitution always on; director names ids; capability opens on demand; filing keeps progress and evidence |
| Craft | `agents/<id>.md`. A walkable path. `gsh next` advances `craft_open` |
| Skill | `skills/<id>/SKILL.md`. The procedure for this step. No session numbers |
| Director menu | `gsh menu` looks up ids. `catalog.json` is a menu file, not a system prompt |
| Current card | `.harness/sessions/<id>/current.md`. Read it after a tool switch |
| Close | `gsh close` writes `verify-report.json` and appends the audit log |
| Isolation | Default `sandbox`. Official writes need a human and a changeset |
| Profile | minimal / core / full decide what lands on disk |
| Isolate | Probe tree that does not write real homedirs |

```text
[request]
  → gsh menu names an id
  → loadplan + activate
  → current-step skill
  → sandbox
  → gsh close
  → human promote
```

---

## Design philosophy

Written for the people in the production room. The goal is one job in the next hour, and a file the next person can resume.

**The window stays on production.** Boot reads the constitution, the current card, and named bodies. Look up the other 106 skills with `gsh menu`.

**A craft is a runnable path.** Naming `combat-numeric-designer` opens step one. `gsh next` rewrites the card to the next skill. The rest of the path stays closed until you get there.

**Official surfaces have a sandbox.** Default writes go to isolation roots. Promote is a human plus a record-cell changeset. The model can move fast on drafts.

**Progress lives in files.** `current.md`, `state.json`, and `tasks.jsonl` survive a client switch. `gsh status` / `gsh resume` read the same cabinet.

**Close is one command.** `gsh close` writes the report from a template, appends the index, and updates the card. Cursor `stop` and Claude `Stop` check that file.

**Hosts stay lazy.** Boot only handshakes the `core` tier keys. This pack ships no live servers. See [MCP](#mcp).

**Secrets and destructive shell have gates.** Cursor and Claude Code intercept common secret paths and ask before `git reset --hard`.

---

## What you can run

These are walkable production paths, not roleplay prompts.

### Scope a vertical slice

A producer says this milestone only has to prove a 3-second melee TTK. The director reads `route-task`, confirms the craft id with `gsh menu -q ttk`, writes `loadplan.json`, and runs `gsh activate`. The current card freezes the goal, write class, and first step.

### Combat numeric

`combat-numeric-designer` walks: anchors → attributes → formula / counter / skill coefficients → table write → corners → diff. `gsh next` moves the worker from `combat-modeling` to `attribute-framework` without loading the later coefficient tables.

### Economy and progression

`economy-numeric-designer` walks sources, sinks, prices, inflation, and table promote. `progression-numeric-designer` walks curves, unlocks, and attribute hooks. Same loop: one skill per step, sandbox tables, close with evidence.

### Levels and experience

`level-designer` walks goal chains, blockout, encounters, pacing. `narrative-designer` walks beats, quest gates, dialogue. `ux-designer` walks IA and five-states. Name one craft and stay on blockout or beats.

### Client / server

`client-engineer`, `server-engineer`, and the combat/UI variants split contract, slice, and save migration into steps. Official git still goes sandbox → human. Engineering skills keep unfrozen designer numbers out of code constants.

### QA and release

`qa-lead` owns the plan; `qa-functional` owns cases and bugs; automation / compat / perf have their own paths. Close with `gsh close --kind playtest` or `build` and attach a case pack or build log.

### Liveops

`liveops-designer` walks the calendar, event spec, and reward-mail checks. Calendar collisions live in the skill; schedule numbers live in sandbox tables.

### Cross-craft handoff

`handoff-pack` + `collab-protocol` + `gsh status`. The next shift opens the studio root, runs `gsh resume`, and sees the card and the next skill.

Craft index: [docs/crafts/index.md](docs/crafts/index.md). Skill index: [docs/skills/index.md](docs/skills/index.md).

---

## Guides

### Combat numeric slice (shortest green path)

```bash
python -m gsh setup --workspace /path/to/studio --tools cursor --profile core --yes
cd /path/to/studio
python -m gsh menu --kind craft -q combat
```

Write `.harness/sessions/combat-ttk/loadplan.json` naming `combat-numeric-designer`. Then:

```bash
python -m gsh activate combat-ttk
python -m gsh resume
# open the skill in craft_open; edit sandbox tables
python -m gsh next --craft combat-numeric-designer
python -m gsh close --kind schema --evidence .harness/sandbox/ttk-notes.md
```

`activated.json` `craft_path` shows progress such as `2/9`. The current card and `state.json` stay aligned. A human still promotes official record cells.

Longer walkthrough: [docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md).

### Resume in another client

Scope in Cursor at noon, open the same studio root in Claude Code at night:

```bash
python -m gsh status --workspace /path/to/studio
python -m gsh resume --workspace /path/to/studio
```

Both clients read the same `.harness`. Cursor injects the card on `sessionStart`. Claude Code `settings.json` calls the same `hooks/开场.py`.

### Director names ids; the menu stays a menu

```bash
python -m gsh menu --kind skill -q excel
python -m gsh menu --kind craft -q qa
```

Output is an id plus one-line description. Do not paste `catalog.json` into a system prompt. The boot hook rewrites a dumped catalog into a reminder to use `gsh menu`.

---

## Platform support

Every selected tool receives a complete skill/craft tree and the entry files that tool already opens.

| Tool | Entry | Hooks / automation | Other |
|---|---|---|---|
| Cursor | `rules/全局.mdc` | runs `hooks.json` | harness, lazy MCP |
| Claude Code | `CLAUDE.md` | runs `settings.json` → same `hooks/*.py` | `HOOKS.md` |
| Codex | `AGENTS.md` | `HOOKS.md` + `gsh status/next/close` | `~/.agents/skills` |
| Windsurf | `.windsurfrules` | same CLI | `.windsurf/rules` |
| Cline | `.clinerules/` | same CLI | — |
| Roo Code | `.roo/rules` | `.roomodes` director / maker / closer | — |
| Continue.dev | `config.yaml` | prompts for route-task / close / status / next | — |
| GitHub Copilot | instructions + prompts | same | — |
| OpenCode | `opencode.json` | `HOOKS.md` + CLI | — |
| Gemini CLI | `GEMINI.md` | same | — |
| Aider | `CONVENTIONS.md` | `.aider.conf.yml` read-only constitution | — |
| Zed | `AGENTS.md` + `.rules` | same | — |
| Amazon Q / Trae / Junie | rules / guidelines | same | — |
| Grok / DeepSeek / Kimi / Qwen | `AGENTS.md` / `QWEN.md` | same | — |

The CLI runs on every tool. Event hooks are wired for Cursor and Claude Code.

Per-tool notes: [docs/adapters/](docs/adapters/).

---

## MCP

This pack ships **0** live servers, 36 purpose stubs, and `mcp.json.example`. `mcp-tiers.json` `core` is a handshake list. excelMCP in core is a tier key for the table pipeline; you still install the host. Real start goes through `lazy_stdio`.

Policy: [docs/mcp-policy.md](docs/mcp-policy.md).

---

## Token / context

| Practice | Saves |
|---|---|
| Short L1 | per-turn tax |
| `gsh menu` | 100+ descriptions |
| `gsh next` opens one step | the rest of a craft |
| `retrieve_keys` for canon | the lore bible |
| Lazy MCP | boot `tools/list` |
| minimal / core | skills you will not use |

---

## Security

- No secrets in git. Example MCP files are placeholders.
- Setup does not overwrite `mcp.json`.
- Cursor / Claude Code block common secret paths.
- Destructive git asks for confirm.
- `verify` and `tests/test_no_secrets.py` scan user-profile paths, `Harness-Apps`, `ghp_` / `sk-`.
- Private advisories: [SECURITY.md](SECURITY.md).

---

## Troubleshooting

| Symptom | First move |
|---|---|
| verify: missing catalog | setup, same isolate root |
| projection drifted | `python -m gsh sync` |
| lost the current step | `python -m gsh status` |
| craft will not advance | `python -m gsh next --craft <id>` |
| close hook waiting | `python -m gsh close --evidence <path>` |
| catalog too large | `gsh menu -q …` |
| all MCPs red | expected; zero live servers shipped |
| doctor: old Python | install 3.11+ |

---

## Tests

```bash
python -m unittest discover -s tests -v
```

Catalog parse, no craft pre-expand, secret scan, native-tree projection, isolate CLI, and the `menu` / `activate` / `next` / `close` loop.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

1. Edit skills only under `skills/<id>/SKILL.md`.
2. Edit crafts only under `agents/<id>.md`. `uses_skills` is a sequence that `gsh next` walks.
3. New MCP: purpose stub + placeholders.
4. Architecture changes need a steer and an ADR.
5. PRs need isolate `verify` green and `unittest` green.

---

## CLI

```text
python -m gsh setup | sync | verify | doctor | uninstall
python -m gsh menu [--kind craft|skill] [-q query]
python -m gsh activate <session>
python -m gsh status | resume
python -m gsh next [--craft <id>]
python -m gsh close --kind smoke --evidence <path>
```

---

## License

[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · [LICENSE](LICENSE) MIT · [CHANGELOG.md](CHANGELOG.md)

The four layers are frozen. Progress lives in `.harness`. The only official source is the GitHub repository above.
