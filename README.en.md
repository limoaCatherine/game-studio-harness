# Game Studio Harness

Game Studio Harness (GSH) is a **four-layer context operating system** for game-production pipelines. It connects LLM agents to scoping, craft paths, isolated execution, and evidence-based promotion: a file contract bounds the current round, skills open one step at a time, writes default to the isolation surface, and official surfaces are updated only after human approval.

Intended readers: producers, technical directors, lead designers, lead engineers, and the AI coding tools that share one studio root.

```text
scope → slice → isolate → verify → promote
```

[中文](README.md) ·
[What's inside](#whats-inside) ·
[What work it handles](#what-work-it-handles) ·
[Problems it addresses](#problems-it-addresses) ·
[Design philosophy](#design-philosophy) ·
[Key concepts](#key-concepts) ·
[Guides](#guides) ·
[Platform support](#platform-support) ·
[Install](#install)

---

## What's inside

| Kind | Count | Role |
|---|---:|---|
| Craft paths | 35 | Production, systems/numeric, level/UX, engineering, QA, art/audio |
| Skill procedures | 106 | Scoping, tables, formulas, acceptance, handoff |
| Native adapters | 19 | Complete per-tool trees: entry, rules, skills/crafts, hooks or equivalent |
| MCP | 0 live servers / 36 purpose stubs | This pack does not ship connectable processes |

```text
game-studio-harness/
├── skills/                 # 106 skills (single content source)
├── agents/                 # 35 craft paths (single content source)
├── rules/ hooks/ harness/  # constitution, hooks, runtime, catalog
├── gsh/                    # setup / sync / verify / menu / status / next / close
├── studio/.harness/        # studio-root scaffold
├── .cursor/ .claude/ …     # native conventions (no skill forest in the pack)
└── docs/ tests/
```

After setup, the shared runtime lives at `~/.gsh` (or `<isolate>/gsh`). Each selected tool home receives the full native tree that tool already understands.

---

## What work it handles

GSH handles production work that crosses crafts, sessions, and clients on a single vertical slice. Each path below is addressable by catalog id and executable step by step.

### Scoping and freeze

A request such as “this milestone only has to prove a 3-second melee TTK” becomes `loadplan.json`: named craft or skill ids, write class (default `sandbox`), and verify kind. `python -m gsh menu` looks up ids; `python -m gsh activate <session>` writes `activated.json` and the current card. Scope is stored in files so later sessions and other tools can read it.

### Combat numeric

`combat-numeric-designer` walks: anchors → attribute framework → formula / counter / skill coefficients → table write → corner cases → table diff. Each step is one skill. `python -m gsh next` moves `craft_open` from `combat-modeling` to `attribute-framework` so later coefficient tables stay out of this turn’s context.

### Economy and progression

`economy-numeric-designer`: sources and sinks, prices, inflation stress, table promote.  
`progression-numeric-designer`: growth curves, unlock cadence, attribute hooks.  
Same execution model as combat numeric: one skill per step, tables on the isolation surface, evidence paths on close.

### Levels, narrative, and UX

`level-designer`: goal chains, blockout, encounters, pacing.  
`narrative-designer`: beat sheets, quest gates, dialogue.  
`ux-designer`: information architecture and five-states.  
After a craft is named, the round executes only the current step (blockout only, or beats only) and does not rewrite copy keys in parallel.

### Client and server

`client-engineer`, `server-engineer`, and the combat/UI variants split contract, feature slice, and save migration into steps. Official Git surfaces still pass through isolation and human approval. Engineering skills keep unfrozen design numbers out of code constants.

### Quality and release

`qa-lead`: test plan and acceptance criteria.  
`qa-functional`: cases and defects.  
Automation, compatibility, and performance have separate paths. Close with `python -m gsh close --kind playtest` or `--kind build`; evidence is a case pack or a build log.

### Live operations

`liveops-designer`: event calendar, event spec, reward-mail checks. Collision and reissue rules live in the skill; schedule numbers live on isolation tables, not in the craft body.

### Cross-craft handoff

`handoff-pack`, `collab-protocol`, and `python -m gsh status`. The next shift opens the studio root, runs `python -m gsh resume`, and reads the current card and next skill without relying on chat history.

Craft index: [docs/crafts/index.md](docs/crafts/index.md). Skill index: [docs/skills/index.md](docs/skills/index.md).

---

## Problems it addresses

These are recurring production problems that a single prompt does not stabilize. GSH handles them with a four-layer file contract and a CLI.

**The context budget is consumed by the menu.** Injecting 106 skills and 35 crafts in full causes the model to edit formulas, discuss saves, and touch official tables in the same step. GSH treats `catalog.json` as a director lookup (`gsh menu`). Boot injects only the constitution, the current card, and named bodies.

**Multi-craft paths are expanded in one shot.** Combat numeric has a fixed order from anchors to coefficient tables. If naming a craft reads every `uses_skills` body, step one fills tables with step-five language. GSH opens `craft_open` only; `gsh next` advances.

**Official surfaces are mixed with drafts.** Design tables, engine assets, and committed history are expensive to roll back. GSH defaults to `write_class=sandbox`. Official writes require human approval and a record-cell changeset.

**Progress is lost when a session ends or the client changes.** Chat is not the archive. Progress lives in `current.md`, `state.json`, and `tasks.jsonl`. Any installed tool can run `gsh status` / `gsh resume`.

**Acceptance has no durable record.** Informal confirmation cannot enter release materials. `gsh close` writes `verify-report.json` (`verify_kind`, `evidence_paths`, `verdict`) and appends the audit log.

**Every MCP host handshakes at IDE start.** Dozens of `tools/list` calls stall boot and spend the context budget. GSH handshakes only the `core` keys in `mcp-tiers.json`; the rest stay lazy. This pack ships no live servers.

**Secrets enter model context; destructive commands run without confirmation.** Cursor and Claude Code intercept common secret paths on read and shell, and require confirmation for operations such as `git reset --hard`.

---

## Design philosophy

This section is separate from the problem statements. It states **why the design exists and what a studio gains**.

**Context budget (context window).** The per-turn tax stays short: constitution, current card, named skill or craft bodies. Other skills open when that step starts. `minimal` / `core` / `full` decide disk projection, not this turn’s injection.

**Craft paths.** A craft file is a step sequence (`uses_skills`). A skill file is the procedure for one step. `activated.json` `craft_path` stores index, current skill, and next skill. `gsh next` advances and rewrites the current card.

**Official surface and isolation surface.** Isolation roots are declared in `.harness/surfaces.json`. The model executes on the isolation surface. Promotion is a production decision, not a default model privilege.

**Session continuity.** Studio-root `.harness` is the cross-tool filing cabinet. Probe sessions start with `_` and do not overwrite `LATEST`.

**Acceptance evidence.** The close command is `gsh close`. Cursor `stop` and Claude Code `Stop` check the same report. Other tools follow the same flow via the CLI and `HOOKS.md`.

**Lazy MCP.** `core` is a handshake list, not an installed-server list. `lazy_stdio` starts the child on the first `tools/call`.

**Secret isolation.** Secrets must not enter git or the model context. `mcp.json.example` is placeholders only. Setup never overwrites an existing `mcp.json`.

**Confirmation for destructive operations.** Irreversible Git and recursive deletes require human confirmation.

---

## Key concepts

| Concept | Definition and use |
|---|---|
| Four layers | Constitution (always on) → director (names ids) → capability (opens on demand) → filing (progress and evidence) |
| Craft | `agents/<id>.md`. A walkable path. `gsh next` updates `craft_open` |
| Skill | `skills/<id>/SKILL.md`. Procedure for the current step. No session numbers |
| Director menu | `gsh menu` looks up ids. `catalog.json` is a menu file, not a system prompt |
| Current card | `.harness/sessions/<id>/current.md`. Read first after a client switch |
| Close | `gsh close` writes `verify-report.json` and appends `tasks.jsonl` |
| Write isolation | Default `sandbox`. Official writes need human approval and a record-cell changeset |
| Profile | `minimal` / `core` / `full` decide which skills and crafts land in homedirs |
| Isolate | Probe root that does not write real user homedirs |

```text
[production request]
  → gsh menu names an id
  → loadplan + activate
  → current-step skill
  → isolation-surface work
  → gsh close
  → human approval, then promote
```

---

## Guides

### Combat numeric slice

```bash
python -m gsh setup --workspace /path/to/studio --tools cursor --profile core --yes
cd /path/to/studio
python -m gsh menu --kind craft -q combat
```

Write `.harness/sessions/combat-ttk/loadplan.json` naming `combat-numeric-designer`. Then:

```bash
python -m gsh activate combat-ttk
python -m gsh resume
# open the skill in craft_open; edit tables on the isolation surface
python -m gsh next --craft combat-numeric-designer
python -m gsh close --kind schema --evidence .harness/sandbox/ttk-notes.md
```

`activated.json` `craft_path` shows progress such as `2/9`. The current card and `state.json` stay aligned. Official record cells are written only after human approval.

Full walkthrough: [docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md).

### Resume after a client switch

After scoping in Cursor, open the same studio root in another client:

```bash
python -m gsh status --workspace /path/to/studio
python -m gsh resume --workspace /path/to/studio
```

Both clients read the same `.harness`. Cursor injects the card summary on `sessionStart`. Claude Code `settings.json` invokes the same `hooks/开场.py`.

### Director lookup without injecting the catalog

```bash
python -m gsh menu --kind skill -q excel
python -m gsh menu --kind craft -q qa
```

Output is an id plus one-line description. Do not write `catalog.json` into a system prompt. If the boot hook detects a dumped catalog in context, it rewrites the injection to recommend `gsh menu`.

---

## Platform support

Every selected tool receives a complete skill/craft tree and the entry files that tool already opens.

| Tool | Entry | Hooks / automation | Other native files |
|---|---|---|---|
| Cursor | `rules/全局.mdc` | executes `hooks.json` | harness, lazy MCP |
| Claude Code | `CLAUDE.md` | executes `settings.json` → same `hooks/*.py` | `HOOKS.md` |
| Codex | `AGENTS.md` | `HOOKS.md` + `gsh status/next/close` | `~/.agents/skills` |
| Windsurf | `.windsurfrules` | same CLI | `.windsurf/rules` |
| Cline | `.clinerules/` | same CLI | — |
| Roo Code | `.roo/rules` | `.roomodes` director / maker / closer | — |
| Continue.dev | `config.yaml` | prompts: route-task / close / status / next | — |
| GitHub Copilot | instructions + prompts | same | — |
| OpenCode | `opencode.json` | `HOOKS.md` + CLI | — |
| Gemini CLI | `GEMINI.md` | same | — |
| Aider | `CONVENTIONS.md` | `.aider.conf.yml` read-only constitution | — |
| Zed | `AGENTS.md` + `.rules` | same | — |
| Amazon Q / Trae / Junie | rules / guidelines | same | — |
| Grok / DeepSeek / Kimi / Qwen | `AGENTS.md` / `QWEN.md` | same | — |

The CLI runs against the studio root for every tool above. Event-hook runtimes are wired for Cursor and Claude Code.

Per-tool notes: [docs/adapters/](docs/adapters/).

---

## Install

**Python 3.11+**. Windows is a first-class game-production target; Linux/macOS are for isolate probes and CI. The installer projects architecture files and skills. It does not ship production-software installers and does not write secrets.

Install only from the official repository: [github.com/limoaCatherine/game-studio-harness](https://github.com/limoaCatherine/game-studio-harness). Third-party packages are outside this project’s maintenance.

Edit content only at repo root: `skills/`, `agents/`, `rules/`, `hooks/`, `harness/`. `gsh setup` / `gsh sync` write that same content into each tool’s complete native tree.

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

| `--profile` | Projection | Use when |
|---|---|---|
| `minimal` | 12 director/isolation/close skills + 4 crafts | Complete one four-layer loop |
| `core` | Daily director, tables, slice, acceptance | Most production sessions |
| `full` (default) | 106 skills + 35 crafts | Full catalog on disk |

`--tools all` (default) lands 19 complete native trees. `legacy` = cursor,claude,codex,grok,deepseek.

Isolate probe (does not write real homedirs):

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

Open the **studio root**, not only this repository. Replace placeholders in `.harness/surfaces.json` with machine-local paths. Do not commit real drive letters back to the GSH repository.

| Task | Entry |
|---|---|
| Scope a vertical slice | `python -m gsh menu --kind craft -q slice`, then `skills/route-task/SKILL.md` |
| Combat numeric / TTK | Name `combat-numeric-designer`, `gsh activate`, advance with `gsh next` |
| Economy / progression | `economy-numeric-designer` / `progression-numeric-designer` |
| Level blockout | `level-designer` |
| Client / server | `client-engineer` / `server-engineer` |
| QA acceptance | `qa-lead` or `qa-functional`, then `gsh close` |
| Liveops calendar | `liveops-designer` |
| Resume the current session | `python -m gsh resume` |
| Inspect progress | `python -m gsh status` |
| Close a work item | `python -m gsh close --kind smoke --evidence <artifact>` |

```text
gsh menu -q ttk
  → write loadplan.json (name a craft id)
  → gsh activate <session>
  → read current.md; execute the current step only
  → gsh next
  → gsh close --evidence <isolation-surface artifact>
  → after human approval, write official record cells
```

### CLI

```text
python -m gsh setup | sync | verify | doctor | uninstall
python -m gsh menu [--kind craft|skill] [-q query]
python -m gsh activate <session>
python -m gsh status | resume
python -m gsh next [--craft <id>]
python -m gsh close --kind smoke --evidence <path>
```

---

## MCP policy

This pack ships **0** live servers, 36 purpose stubs, and `mcp.json.example`. `mcp-tiers.json` `core` is a handshake list. excelMCP in core is a tier key for the table pipeline; the host is still installed locally. Real start goes through `lazy_stdio`.

Full policy: [docs/mcp-policy.md](docs/mcp-policy.md).

---

## Context budget

| Practice | Injection saved |
|---|---|
| Short L1 | per-turn tax |
| `gsh menu` lookup | 100+ descriptions |
| `gsh next` opens one step | the rest of the craft path |
| `retrieve_keys` for canon | the lore corpus |
| Lazy MCP | boot `tools/list` |
| minimal / core | skills not needed this round |

---

## Security

- Secrets do not enter git. `mcp.json.example` is placeholders only.
- Setup does not overwrite an existing `mcp.json`.
- Cursor / Claude Code intercept common secret paths.
- Destructive Git operations require confirmation.
- `verify` and `tests/test_no_secrets.py` scan user-profile absolute paths, `Harness-Apps`, and `ghp_` / `sk-`.
- Report vulnerabilities via GitHub private advisories: [SECURITY.md](SECURITY.md).

---

## Troubleshooting

| Symptom | Action |
|---|---|
| `verify` reports missing catalog | Run `setup` with the same `--isolate-root` |
| Projection drifted from root skills | `python -m gsh sync` |
| Current step unclear | `python -m gsh status` |
| Craft path did not advance | `python -m gsh next --craft <id>` |
| Close hook waiting for a report | `python -m gsh close --evidence <path>` |
| Catalog should not enter the prompt | `gsh menu -q …` |
| All MCP hosts unavailable | Expected: this pack ships no live servers |
| `doctor` reports an old Python | Install 3.11+ |

---

## Tests

```bash
python -m unittest discover -s tests -v
```

Coverage includes catalog parse, craft-path non-expansion, secret scan, native-tree projection, isolate CLI, and the `menu` / `activate` / `next` / `close` loop.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

1. Edit skills only under `skills/<id>/SKILL.md`.
2. Edit crafts only under `agents/<id>.md`. `uses_skills` is a sequence that `gsh next` walks.
3. New MCP: purpose stub plus placeholders. Do not commit a connectable server or a secret.
4. Changes to the four layers require a steer and an ADR.
5. Pull requests require a passing isolate `verify` and a passing `unittest` run.

The 0.1 duplicate trees such as `cursor/skills` are removed. Edit at repo root, then `sync`.

---

## License

[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · [LICENSE](LICENSE) MIT · [CHANGELOG.md](CHANGELOG.md)

The four layers are frozen. Progress is written under `.harness`. The only official source is the GitHub repository above.
