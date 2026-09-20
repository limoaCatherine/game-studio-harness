# Game Studio Harness

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![CI](https://img.shields.io/github/actions/workflow/status/limoaCatherine/game-studio-harness/ci.yml?branch=main)](https://github.com/limoaCatherine/game-studio-harness/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.4.0-informational.svg)](CHANGELOG.md)

Game Studio Harness (GSH) is a four-layer context operating system for the **full game-production pipeline**. It connects LLM agents across production and direction, design, engineering, quality, art and audio, and live operations. The current round is bounded by a file contract. Skills open one step at a time. Writes default to the isolation surface. Official surfaces update only after human approval.

The design logic is **capability-boundary isolation, skill distillation, task orchestration, and context-budget injection**. Human gates and sandbox promotion are mechanisms; see [Engineering practice](#engineering-practice).

Design has **11** crafts in two peer groups: systems, combat, combat numeric, economy numeric, progression numeric, monetization, liveops; and level, narrative, copy, UX.

Intended readers: producers, technical directors, lead designers, lead engineers, QA and art leads, and the AI coding tools that share one studio root.

```text
scope → slice → isolate → verify → promote
```

[中文](README.md) ·
[Design philosophy](#design-philosophy) ·
[Principles, scope, and runtime model](#principles-scope-and-runtime-model) ·
[What's inside](#whats-inside) ·
[Inventory](#inventory) ·
[Department capability map](#department-capability-map) ·
[Where skills come from](#where-skills-come-from) ·
[Engineering practice](#engineering-practice) ·
[Problems it addresses](#problems-it-addresses) ·
[Key concepts](#key-concepts) ·
[Guides](#guides) ·
[Platform support](#platform-support) ·
[Docs](docs/README.md) ·
[Prerequisites](#prerequisites) ·
[Install](#install)

---

## Design philosophy

Four design decisions govern how files are cut, what enters context, and how a round advances. Human gates, isolation surfaces, and sandbox promotion are mechanisms; they live in [Engineering practice](#engineering-practice).

### Capability-boundary isolation

Crafts, skills, and write surfaces declare explicit capability boundaries. A craft file states the step sequence and job duty. A skill file states the single-step procedure and its inputs and outputs. Official and isolation surfaces are declared in `.harness/surfaces.json`.

Work in a round stays inside the named set. Cross-boundary handoff uses `handoff-pack`, the current card, and `loadplan.json`. Downstream crafts read the handoff files. They do not overwrite another craft’s official surface in the same round.

### Skill distillation

Live studio workflows are condensed into reusable `SKILL.md` files: checklists, table-write recipes, blockout and beat acceptance, contracts, and intake criteria. The craft ranks the order. The procedure lives in the skill. Naming a skill opens a program with inputs, outputs, and fail-closed rollback. Origin and coverage: [Where skills come from](#where-skills-come-from).

### Task orchestration

A production round follows a fixed loop: look up an id (`menu`) → write the contract and activate (`activate`) → execute the current step (`next`) → verify and close (`close`). State lives under studio-root `.harness`. After a client switch, read the same current card. Orchestration targets files and commands. Chat history is not the progress source.

### Context-budget injection

The context window is allocated on a budget. Boot injects the constitution, the current card, and activated skill or craft bodies. `catalog.json` is a lookup for `gsh menu`. Canon / adr open only after `retrieve_keys` hits. A craft path opens `craft_open` only; later steps enter context when that step starts. Disk profiles `minimal` / `core` / `full` decide projection, not this turn’s injection.

### Strengths and limits

**Gains.** The promote path is auditable: write on the isolation surface, then merge record cells after human approval. Short steps can be checked against a `verify-report`. Tools share one filing cabinet. Skills are versionable and reusable. The named set limits what this round may rewrite.

**Costs.** The architecture depends on human gates, so there is no unattended ship. Short steps raise session count and handoff cost. Skill quality tracks whether distillation stays current; a stale checklist hardens a wrong procedure. Adapter parity differs by host: Cursor and Claude Code run event hooks; other tools use the CLI and `HOOKS.md`, so boot injection and close-gate completeness vary. This pack ships no connectable MCP process; table hosts and similar connectors are installed locally.

Percentages in the public evaluations belong to those papers. **None is a studio-measured GSH success rate.** Sources: [Threats and limits](#threats-and-limits).

---

## Principles, scope, and runtime model

Read the design logic, then the department map. This section states principles, coverage bounds, the runtime loop, and what published evaluations imply for long-horizon autonomy.

### Core principles

The four-layer contract applies in layers. The constitution sets read order, default write isolation, the close command, and secret / destructive gates. The director writes `loadplan.json` and names ids. The capability library opens skills one step at a time. The filing cabinet keeps progress and evidence.

The named set decides boot injection. A missing skill can be opened mid-round without regenerating the roster.

A craft does not pre-expand `uses_skills`. `gsh next` advances one step and rewrites the current card.

Write class defaults to `sandbox`. Promotion needs a human and writes record cells only.

Secrets stay out of git and out of model context. Irreversible destroy needs explicit authorization this round.

### Scope and non-goals

**Scope.** The full game-production pipeline. Current catalog: **35 / 35** crafts, **106 / 106** skills.

Design has **11** crafts in two peer groups:

- systems, combat, combat numeric, economy numeric, progression numeric, monetization, liveops
- level, narrative, copy, UX

The rest: production and project management 4, engineering 6, art and tech art 9, QA 5. Naming one path opens only the current step. Unnamed crafts stay in the menu until activated.

Craft index: [docs/crafts/index.md](docs/crafts/index.md). Skill index: [docs/skills/index.md](docs/skills/index.md). Audio ingest and Bank build are skills (`audio-fmod-checklist`, `fmod-bank-build`) on the tech-art / pipeline steps.

**Non-goals.** Unattended ship. Shipping a game engine, DCC, or a connectable MCP server. Treating `.harness` as a knowledge graph. Writing `catalog.json` into a system prompt. Third-party packages are outside maintenance.

### Runtime model

Human–AI split is part of the runtime model. Promotion to an official surface is a production process. The agent works inside the activated set. Close must pass the verify gate.

| Human-required | AI-capable under GSH | Co-owned |
|---|---|---|
| Experience pillars / fantasy-tone final call | Scoping: write the loadplan and generate the roster | Milestone-planning options |
| Scope-cut approval | Execute the current `craft_open` step; default writes stay in sandbox | Playtest notes |
| Promote isolation work to official surfaces (record cells only) | Skill checklists; GDD feature-slice drafts | Performance-budget drafts |
| Live economy / IAP pricing final | Isolation-surface table diffs | QA exemption proposals |
| Irreversible destroy; secrets | Bug reports, test cases, API-contract drafts | |
| Legal / compliance | Implement + test loops with `verify-report` evidence | |
| Shipping sign-off | Status / weekly digest drafts | |

Loop: `menu` → `activate` → `next` → `close`. Distinct job duties get separate craft subagents. The parent session names ids and closes.

### Threats and limits

Published evaluations share one shape: as tasks get longer and human gates get fewer, unbounded long-horizon autonomy follows a falling logistic. The same model can differ several-fold across harnesses (about 6× in one cited pair). GSH therefore uses short steps and human gates. Axis numbers below only restate cited intervals.

Success falls as “time a human expert needs for that task” grows. METR fits a logistic. The 50% time horizon has doubled about every seven months since 2019. The 80% horizon is about five times shorter. Messier, under-specified tasks score lower.

```text
success probability (METR public intervals; not a GSH measurement)
~100% │●
      │  ●
 ~50% │     ●········ 50% time horizon (~7-month doubling)
      │        ●
 ~10% │           ●●
      └────────────────────────────→ human expert time for the task
        < ~4 min                   > ~4 h
```

Sources (percentages belong to the papers, not to GSH production KPIs):

1. Anthropic: evaluating an “agent” means harness + model; SWE-bench Verified moved from ~40% to >80% in about a year. <https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
2. SWE-Bench Mobile: best about 12%; same model Cursor ~12% vs OpenCode ~2% (~6×). <https://arxiv.org/abs/2602.09540>
3. Harness ablation: under a tight context window, **context management** dominates (mostly by preventing overflow failures). <https://arxiv.org/abs/2609.20804>
4. METR: ~100% on tasks a human finishes in <~4 min; <~10% on >~4 h; 50% horizon doubling ~7 months. <https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/>
5. LongCLI-Bench: autonomous pass rate <20%; plan injection ~58%; plan + interactive ~62%. <https://arxiv.org/abs/2602.14337>
6. SWE-Marathon: pass@1 <30%; reward-hack attempts in 13.8% of rollouts. <https://www.swe-marathon.org/>
7. Chen et al.: agents vs copilots, about +35 percentage points correctness and about half the user time. <https://arxiv.org/abs/2507.08149>
8. CentaurEval: on collaboration-necessary items, LLM alone ~0.67%, human alone ~18.89%, collaboration ~31.11%. <https://arxiv.org/abs/2512.04111>

---

## What's inside

| Kind | Count | Role |
|---|---:|---|
| Craft paths | 35 | Production 4, design 11 (systems/combat/level/narrative/numeric/UX/copy/liveops/monetization), engineering 6, art 9, QA 5 |
| Skill procedures | 106 | Distilled studio playbooks (scope, tables, blockout, beats, contracts, acceptance, handoff) |
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

## Inventory

The authoritative source is `catalog.json` (`gsh menu` scans root `agents/` and `skills/` frontmatter). The lists below match the single source of truth: `agents/` (35) and `skills/` (106).

### 35 crafts

| Department | Craft ids |
| :--- | :--- |
| Production and project management | `producer` · `associate-producer` · `project-manager` · `creative-director` |
| Design · systems and numeric (7) | `systems-designer` · `combat-designer` · `combat-numeric-designer` · `economy-numeric-designer` · `progression-numeric-designer` · `monetization-designer` · `liveops-designer` |
| Design · level, narrative, copy, UX (4) | `level-designer` · `narrative-designer` · `copywriter-designer` · `ux-designer` |
| Client and server engineering | `client-engineer` · `client-combat-engineer` · `client-ui-engineer` · `server-engineer` · `server-combat-engineer` · `tools-engineer` |
| Art and technical art | `character-concept-artist` · `character-artist` · `environment-concept-artist` · `environment-artist` · `ui-artist` · `vfx-artist` · `animator` · `rigger` · `tech-artist` |
| Quality assurance | `qa-lead` · `qa-functional` · `qa-automation` · `qa-compatibility` · `qa-performance` |

### 106 skills

Craft `uses_skills` lists cover 85 event skills. The remaining 21 are not attached to any craft path and live in [Cross-cutting capabilities](#6-cross-cutting-capabilities--runtime-and-filing-cabinet): `assemble-craft-flow`, `attr-family-sync`, `audio-fmod-checklist`, `build-acceptance`, `build-gate-checklist`, `collab-protocol`, `data-readiness-check`, `deliverable-sheets`, `diagram-pack`, `doctor`, `excel-format`, `excel-read`, `fmod-bank-build`, `mcp-autostart`, `memory-retrieve`, `naming-consistency-check`, `personal-server-table-sync`, `promote-adr`, `terrain-gaea-pass`, `verify-gate`, `write-isolation`.

Every id appears in the department tables below. The capability map covers **35/35 crafts and 106/106 skills**. Distillation is stated after the map in [Where skills come from](#where-skills-come-from).

### 36 MCP connectors

`accurig` · `audacity` · `blender-mcp` · `cascadeur` · `chrome-devtools` · `cloudcompare` · `docker-mcp` · `everything-search` · `excalidraw` · `excelMCP` · `ffmpeg` · `fmod-cli` · `fmod-studio` · `gaea` · `gamedev-mcp` · `gimp` · `imagemagick` · `inkscape` · `instant-meshes` · `krita-mcp` · `lark-mcp` · `ldtk` · `magicavoxel` · `materialize` · `materialpilot` · `meshlab` · `meshroom` · `miro` · `pureref` · `renderdoc` · `rokoko` · `roslyn-mcp` · `tiled` · `treeit` · `xmind` · `xnormal`

The core tier connects `excelMCP` at startup. The rest are lazy and spawn a child process on first call. See [MCP policy](#mcp-policy). This repository ships 0 live servers and 36 purpose stubs.

---

## Department capability map

The map is organized by studio department. Each module includes: (1) where the department sits in the production pipeline; (2) every craft path — step intent and which skills it opens; (3) related skills with purpose, timing, and inputs/outputs; (4) how a typical vertical slice walks these files with `menu` / `activate` / `next` / `close`.

Session commands map to scripts as follows:

| Command | Script / skill | Writes |
| :--- | :--- | :--- |
| `menu` | `gsh menu` / `python -m gsh menu` | `catalog.json` |
| `activate` | `gsh activate <session>` (`route-task` → roster generator) | `loadplan.json`, `activated.json`, `current.md` |
| `next` | `gsh next` (open the skill in `craft_open`; if many events, `assemble-craft-flow`) | Next skill body, `flow.json` |
| `close` | `gsh close` / skill `verify-gate` (plus `artifacts-append` / `sync-state` / `handoff-pack` when needed) | `verify-report.json`, artifact index, state write-back |

---

### 1. Production and project management

Production turns direction, capacity, dependencies, and acceptance into a trackable contract. The producer sets goals and release language. The associate producer splits packs and chases completeness. Project management keeps the risk register and dependency graph. The creative director freezes pillars and adjudicates experience conflicts. Without this layer, downstream crafts edit official surfaces inside an unapproved scope.

| Craft | id |
| :--- | :--- |
| Producer | `producer` |
| Associate producer | `associate-producer` |
| Project manager | `project-manager` |
| Creative director | `creative-director` |

#### Craft paths

**`producer`** — Milestone goals, build-acceptance drive, release-note language, cross-craft production push.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Scope and success criteria | Restate goal, constraints, observable success; name lead crafts and tier | `route-task` |
| 2. Milestone plan | Entry/exit, deliverables, critical path, buffers, scope-cut triggers | `milestone-plan` |
| 3. Build-acceptance drive | Evidence slots, exemption path, reverse-schedule chase; do not micro-own packs | (acceptance list; may collaborate `build-acceptance`) |
| 4. Escalation and scope correction | Blocks get owner and deadline; scope swell goes to CD for `scope-cut-decision` | — |
| 5. Release notes and retro | Player-facing vs internal, consistent with evidence, then sync state | `release-notes-stub` → `sync-state` / `handoff-pack` |

Usually hung: `route-task` · `milestone-plan` · `release-notes-stub` · `sync-state` · `handoff-pack` · `file-pack-layout`.

**`associate-producer`** — Split delivery packs, cross-team coordination, block close-loop, pre-acceptance completeness chase.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Split the milestone | Stable ids, owners, dates, acceptance points | `milestone-plan` |
| 2. Align dependencies | Critical path and buffers with PM; cycles escalate | `dependency-map` |
| 3. Daily / weekly follow-up | Factual progress and red counts; meetings decide next actions only | `status-digest` |
| 4. Close blocks | Observable close conditions; direction issues escalate to producer/CD | — |
| 5. Completeness chase and write-back | Chase evidence, not slogans; do not rewrite milestone goals | `sync-state`; layout via `file-pack-layout` |

**`project-manager`** — Risk register, dependency graph, periodic status digest, correction options.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Build / update risk register | Probability × impact, observable signals, mitigation, review date | `risk-register-update` |
| 2. Dependency graph | Craft/deliverable edges, cycle detection, critical path | `dependency-map` |
| 3. Status digest | Three counters: reds, decisions needed, critical-path health | `status-digest` |
| 4. Correction options | Two to four options (buffer / cut / add people); edit the plan only after approval | `sync-state` |
| 5. Archive | Close risks with outcomes; keep paths, increment versions | — |

**`creative-director`** — Experience pillars, slice critique, fantasy conflict rulings, scope-cut principles.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Collect conflicts and floors | Play / art / live-ops claims with evidence; classify exclusive / resource / tone | — |
| 2. Define pillars | Three to five testable pillars with like / unlike counterexamples | `pillar-define` |
| 3. Experience critique | Keep / cut / change notes that point at concrete objects | `experience-critique` |
| 4. Scope cut | Keep / cut / defer table with tradeoffs, rollback, affected crafts | `scope-cut-decision` |
| 5. Promote Canon | Approved pillars and rulings enter the decision library | `promote-canon` |

#### Related skills

| Skill | What it does | When | Input → output |
| :--- | :--- | :--- | :--- |
| `route-task` | Name skill/craft/mcp ids from the catalog; write the load-plan and current card | New session, steer, interrupt, parallel, naming | Request → `loadplan.json` + `activate` |
| `milestone-plan` | Schedule milestones from capacity, dependencies, and calendar | After scoping, when splitting packs | Entry/exit + capacity → milestone page and cut triggers |
| `release-notes-stub` | Rewrite git log / table diff / cut decisions into player notes | Before ship, patch notes | Change sources → classified notes |
| `sync-state` | Align work items, session cards, plans, and artifact index | Daily follow-up, before close, handoff | Scattered state → single source + `state.json` |
| `handoff-pack` | Pack goal, decisions, artifact paths, open items, suggested next craft | Craft or session change | Current card + artifacts → handoff pack |
| `file-pack-layout` | Plan workspace / asset folders; isolate third-party and drafts | Lost files, repo layout | Current tree → move list and map |
| `dependency-map` | Map edges, detect cycles, emit parallel groups and cut fan-out | Cross-team waits, unclear critical path | Packs / systems → versioned graph |
| `status-digest` | Summarize factual progress, blocks, and decisions needed | Weekly report, stand-up, red counts | Pack table → citable digest |
| `risk-register-update` | Identify / re-score risks with signals, mitigation, review date | Stale register, new external dependency | Register sheet → ranked rows |
| `pillar-define` | Freeze 3–5 testable experience pillars and counterexamples | Kickoff, direction conflict, empty pillars | Claims + refs → citable pillar doc |
| `experience-critique` | Executable notes against pillars on a slice | Slice playtest, fantasy conflict | Build + pillars → keep/cut/change table |
| `scope-cut-decision` | Keep / cut / defer under pillar constraints | Overdue milestone, scope swell | Capacity + pillars → decision table |
| `promote-canon` | Write approved stable facts into the decision library | After pillars or rules freeze | Approval record → `canon/` entry |

#### Typical vertical slice

Opening a “playable combat graybox” milestone: `menu` refreshes `catalog.json`. The producer `activate`s `producer` + `creative-director` (separate subagents), `route-task` writes T2/`sandbox`. `next` runs `pillar-define`, then `milestone-plan` splits packs for the associate producer. A PM subagent runs `risk-register-update` and `dependency-map`. Completeness day uses `status-digest` + `sync-state`. `close` checks the milestone page, pillar doc, and completeness sheet, then writes `verify-report.json`. Release week reactivates `release-notes-stub`.

---

### 2. Design

Design covers all **11** crafts in two peer groups: systems and numeric (7) and level, narrative, copy, UX (4). Growth curves are owned by `progression-numeric-designer` (`progression-curve`). Combat numeric owns attributes, formulas, counters, and skill coefficients.

#### Craft roster (11)

| Craft | id | What it does | Path skills |
| :--- | :--- | :--- | :--- |
| Systems design | `systems-designer` | Systems index, feature GDD slices, rule feasibility | `systems-index-map` · `feature-gdd-slice` · `rule-feasibility-check` · `promote-canon` |
| Combat design | `combat-designer` | Combat flow, skill kits, feel checklists | `combat-flow-design` · `skill-kit-design` · `combat-feel-checklist` · `feature-gdd-slice` |
| Combat numeric | `combat-numeric-designer` | Attributes, formulas, counters, skill coefficients; tables use the write recipe | `combat-modeling` · `attribute-framework` · `damage-formula-pass` · `counter-matrix-pass` · `skill-numeric-pass` · `excel-com-write` · `tunable-table-diff` |
| Economy numeric | `economy-numeric-designer` | Source/sink loops, prices, inflation, table promote | `economy-loop-analysis` · `sink-source-map` · `price-curve-pass` · `inflation-stress` · `excel-com-write` · `tunable-table-diff` |
| Progression numeric | `progression-numeric-designer` | Growth curves, unlock cadence, economy hooks, attribute attach | `progression-curve` · `sink-source-map` · `attribute-framework` · `excel-com-write` · `tunable-table-diff` |
| Monetization | `monetization-designer` | Pay points, IAP / pack / pass catalog, KPI definitions | `monetization-kpi-pass` · `iap-catalog-check` |
| Liveops | `liveops-designer` | Event calendar, event spec, reward-mail checks | `liveops-calendar` · `event-spec` · `reward-mail-check` |
| Level design | `level-designer` | Goal chains, blockout, encounters, pacing | `level-goals-spec` · `blockout-pass` · `encounter-script` · `pacing-pass` |
| Narrative design | `narrative-designer` | Beat sheets, quest specs, dialogue, lore consistency | `narrative-beat-sheet` · `quest-spec` · `lore-consistency-check` · `dialogue-pass` |
| Copy | `copywriter-designer` | System / tutorial copy, dialogue polish, naming and length | `naming-consistency-check` · `copy-pass` · `dialogue-pass` |
| UX | `ux-designer` | Information architecture, UX flows, usability review | `ux-flow-spec` · `ux-review-pass` |

Each craft has a full path table below (step, intent, skills opened).


#### Systems and numeric

Systems design locks rules and interfaces. Combat design locks flow and kits. Three numeric paths own combat formulas, economy loops, and progression curves. Monetization and liveops attach pay points and event calendars to the same entities and switches. Table edits always follow read → sandbox write → format → diff → human-approved promotion.

#### Craft paths

**`systems-designer`** — Systems index, feature GDD slice, rule feasibility, Canon proposal.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Update systems index | Explicit/implicit systems, layers, next-design pointer, cycle handling | `systems-index-map` |
| 2. Cut a feature GDD | Eight-section skeleton, state machine as single source | `feature-gdd-slice` |
| 3. Rule feasibility | Engine / netcode / toolchain; feasible or degrade | `rule-feasibility-check` |
| 4. Align downstream | Event names, error codes, save keys, UI entries | — |
| 5. Canon and revision | Approved rules enter the library; conflicts stay side by side first | `promote-canon` |

**`combat-designer`** — Combat flow, skill kits, feel acceptance checklist.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Combat flow | Step ids, time model, resource axis, win/lose | `combat-flow-design` |
| 2. Skill kit | Role, slot duty, resources and cooldown; freeze `slots_version` | `skill-kit-design` |
| 3. Feel checklist | Hit / cancel / hit-react / camera / shake; freeze version | `combat-feel-checklist` |
| 4. GDD and production align | Event-frame expectations to numeric / anim / VFX / code | `feature-gdd-slice` (with `anim-event-hook`, `vfx-skill-hook`) |
| 5. Playtest notes | Tick the list on device; change flow, not the numeric master table | — |

**`combat-numeric-designer`** — Attributes, formulas, counters, skill numbers; tables use the write recipe.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Model goals and freeze anchors | TTK / role bandwidth, corner cases, kit forbidden columns | `combat-modeling` |
| 2. Attribute framework | Primary keys, derived DAG, snapshots, clamps | `attribute-framework` (`attr-family-sync` when adding a family) |
| 3. Formula, counter, skill table | Evaluation order, matrix, coefficient bands | `damage-formula-pass` → `counter-matrix-pass` → `skill-numeric-pass` |
| 4. Corner cases | Zero defense, crit cap, overheal, and peers | — |
| 5. Table diff and handoff | Sandbox write, risk grade, read-back sample | `excel-com-write` → `tunable-table-diff` |

Run `data-readiness-check` before heavy simulation.

**`economy-numeric-designer`** — Source/sink loop, prices, inflation, table promotion.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Loop analysis | Play → earn → spend → play again; mark breaks and stalls | `economy-loop-analysis` |
| 2. Source/sink map | Entities, net flow, cap fields | `sink-source-map` |
| 3. Price curve | Anchors, bands, never-worth / unique-solution scans | `price-curve-pass` (sandbox via `excel-com-write`) |
| 4. Inflation stress | Multi-scenario purchasing power; circuit breakers | `inflation-stress` |
| 5. Table diff promotion | Structured diff, forbidden columns, read-back | `tunable-table-diff` / `excel-com-write` |

**`progression-numeric-designer`** — Growth curves, unlock pacing, economy interface, attribute hooks.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Curve goals | Time / power / chapter anchors; cumulative and delta checks | `progression-curve` |
| 2. Unlock pacing | System / level / progression conditions and fail-hint keys | — |
| 3. ROI and economy interface | Line costs/outputs aligned to entities | `sink-source-map` |
| 4. Attribute hookup | Growth output keys match the combat table | `attribute-framework` |
| 5. Table sample | Write recipe, risk grade, N-day power sample | `excel-com-write` / `tunable-table-diff` |

**`monetization-designer`** — Pay points, IAP / bundle / battle-pass catalog, monetization KPI definitions.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. KPI and floors | Freeze definitions, observation window, pillar-safe bans | `monetization-kpi-pass` |
| 2. Pay points | See → understand → pay → fulfill; P2W risk escalates | — |
| 3. IAP catalog | SKU, price band, contents, purchase limits, store ids | `iap-catalog-check` |
| 4. Event-spec collaboration | Offset liveops calendar; pre-check reward mail | collaborate `liveops-calendar` / `reward-mail-check` |
| 5. Acceptance and revision | KPI checks for misleading buy and hard fulfillment | — |

**`liveops-designer`** — Live calendar, event spec, reward-mail safety.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Calendar | Day / week / season rhythm, collision resolution, maintenance windows | `liveops-calendar` |
| 2. Event spec | Goals, play, rewards, switches, telemetry, fail-reissue | `event-spec` |
| 3. Reward-mail audit | Templates, attachment checks, reissue, expiry, dedupe | `reward-mail-check` |
| 4. Implementation align | Server grant authority and idempotency; client red-dot / expiry | — |
| 5. Pre-ship close | Config diff, rollback owner, telemetry complete | — |

#### Related skills

| Skill | What it does | When | Input → output |
| :--- | :--- | :--- | :--- |
| `systems-index-map` | Enumerate explicit/implicit systems, layer deps, emit a designable index | “Who designs first?”, missing implicit systems | Concept list → `systems_index` (with `next_design`) |
| `feature-gdd-slice` | Co-write an eight-section feature GDD with conflict scan and acceptance evidence | Rules, hollow sections, retrofit | Scope card → implementable slice |
| `rule-feasibility-check` | Split rules into capability points vs engine / netcode / toolchain | “Can we ship this?”, authority gray zones | GDD rules → feasible / conditional / no + degrade |
| `combat-flow-design` | Ingestible combat-flow skeleton and formula grammar | Standardized step names, code handoff | Pillars + pacing intent → flow brief + stable ids |
| `skill-kit-design` | Role, slots, resource and cooldown structure | New job / kit, overlapping slot duty | Fantasy role → coefficient-ready kit |
| `combat-feel-checklist` | Frame preview, input buffer, hitstop, camera shake | Feel acceptance, impact debate | Checklist version → clip evidence and ticks |
| `anim-event-hook` | Event dictionary; Notify on keyframes; align logic and VFX | Hit frames, attack windows, AnimNotify | Clip + event names → dictionary version and frame table |
| `vfx-skill-hook` | Hook skill VFX on Timeline / Notify / Socket; interrupt cleanup | Skill VFX frame align | Event names + sockets → VFX map |
| `combat-modeling` | Object lifetime, state machine, event payload; freeze settle order | Combat entity model, authority align | Anchors → model table and pipeline order |
| `attribute-framework` | Primary keys, derived attrs, snapshots, clamps | Attribute table, primary/secondary attrs | Key set → framework for formulas and growth |
| `damage-formula-pass` | Damage/heal channels, evaluation order, clamps | Damage formula, settle expression | Channels + order → parseable expression + check slots |
| `counter-matrix-pass` | Counter axes, fill matrix, cycle check, modifier mapping | Elemental / type counters | Axis defs → matrix and formula insert points |
| `skill-numeric-pass` | Fill kit coefficients; band compare and anomaly scan | Skill coefficients, CD / resource | Kit skeleton → sampled coefficient table |
| `economy-loop-analysis` | Split the source/sink loop into nodes and directed edges | Broken loop, new currency | Play loop → which table fields to change |
| `sink-source-map` | Enumerate currency/material sources and sinks; net flow | Economy map | Entity list → net flow and caps |
| `price-curve-pass` | Anchors, bands, never-worth / unique-solution scan | Shop pricing | Entity map → tunable price fields |
| `inflation-stress` | Multi-scenario stock / purchasing power; circuit breakers | Before a large event, buying-power complaints | Scenario params → restatable conclusion + breaker keys |
| `progression-curve` | Growth anchors and curve shape; cumulative/delta check slots | Growth curve, grind complaints | Anchors → curve version and cost table |
| `tunable-table-diff` | Diff sandbox vs official numeric tables; grade risk; promote or roll back | Table promotion | Sandbox + official books → rollbackable diff |
| `excel-com-write` | Confirm range → sandbox values/formulas/rows → format → merge recorded cells only → promote → read back | Product-table edits | Official path → `沙箱/*.xlsx` + changeset |
| `monetization-kpi-pass` | Freeze KPI definitions, observation window, and bans | Unfrozen ARPU / conversion language | Producer definitions → observable acceptance metrics |
| `iap-catalog-check` | Check IAP / bundle / pass SKUs against store ids | Catalog ship, purchase-limit refresh | Catalog table → SKU map and value explanation |
| `liveops-calendar` | Day / week / season rhythm and collision resolution | Season, slotting | Milestone + capacity → calendar and backups |
| `event-spec` | Event goals, play, rewards, switches, telemetry, fail-reissue | Timed event brief | Play intent → implementable spec |
| `reward-mail-check` | Mail templates, attachments, reissue, expiry, duplicate grants | Reward mail | Reward list → audit pass or hold |

#### Typical vertical slice

“New job kit is resolvable”: after `menu`, `activate` names `combat-designer` and `combat-numeric-designer` (two subagents), T2/`sandbox`, `retrieve_keys` pointing at formula Canon. Combat design `next`: `combat-flow-design` → `skill-kit-design` → `combat-feel-checklist`. Numeric `next`: `combat-modeling` → `attribute-framework` → `damage-formula-pass` → `skill-numeric-pass`, writes via `excel-com-write`. After sign-off, `tunable-table-diff`. `close` checks kit `slots_version`, formula `order_version`, sandbox diff, and playtest clip. Economy or progression table work uses a separate session naming `economy-numeric-designer` or `progression-numeric-designer`.

---

#### Level, narrative, copy, and UX

This department writes what the player experiences in space and story as testable goals, gated beats, bindable quest state machines, and five-state UX flows. Level design owns goal chains and encounters. Narrative owns beats and lore. Copy unifies terms and length. UX translates system state machines into walkable information architecture. Graybox scale is shared with environment art. Copy keys are reserved for UI and error codes.

#### Craft paths

**`level-designer`** — Level goal chain, graybox circulation, encounter script, pacing peaks and valleys.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Level goals | Main / optional / fail, teaching points, duration budget; hook narrative beats | `level-goals-spec` |
| 2. Graybox circulation | Scale, gates, sightlines; no hero mesh until pass | collaborate `blockout-pass` |
| 3. Encounter script | Waves, triggers, reset, tutorial order; on-screen budget | `encounter-script` |
| 4. Pacing pass | Peak/valley vs combat / puzzle / story density | `pacing-pass` |
| 5. Replace and revise | Swappable blocks to environment art; event names to engineering | — |

**`narrative-designer`** — Beat sheet, quest spec, dialogue spec, lore consistency.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Beat sheet | Chapter/beat: goal, turn, emotion, play hook, gates | `narrative-beat-sheet` |
| 2. Quest spec | State machine, objective keys, rewards, fail rollback, loc keys | `quest-spec` |
| 3. Lore consistency | Scan bible conflicts, name drift, timeline | `lore-consistency-check` |
| 4. Dialogue spec | Node intent, length, branch variables; polish may go to copy | `dialogue-pass` |
| 5. Land and revise | Align triggers with level/systems; skip still delivers key facts | — |

**`copywriter-designer`** — System/tutorial copy, dialogue polish, naming consistency, length fit.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Tone anchor | World tone, banned words, voice samples, length caps | — |
| 2. Naming consistency | One name, one meaning; rename options and blast radius | hang `naming-consistency-check` when present |
| 3. System copy | Tutorial / error / empty / confirm; length and bans | `copy-pass` |
| 4. Dialogue polish | Node intent, skip policy, subtitle length | `dialogue-pass` |
| 5. Fit and revise | Device truncation, ban scan, key-table handoff | — |

**`ux-designer`** — Information architecture, UX flow spec, usability review.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Information architecture | Task list, nav depth, align to system state machine | — |
| 2. Flow spec | Enter / act / feedback / leave; five states and exception node ids | `ux-flow-spec` |
| 3. Usability review | Lost, mis-tap, weak feedback, hit targets, double-tap | `ux-review-pass` |
| 4. Component mapping | Map to UI Kit; file new-control requests | collaborate `ui-kit-spec` |
| 5. Revise and deliver | Close blockers; flow version and debt list | implementation via `ui-logic-pass` |

#### Related skills

| Skill | What it does | When | Input → output |
| :--- | :--- | :--- | :--- |
| `level-goals-spec` | Main / optional / fail goals, teaching points, duration budget | Level brief, unmeasurable win/lose | Pillars + beats → goal chain and detector wording |
| `encounter-script` | Waves, triggers, reset, tutorial order; on-screen and readable fail | Encounter script, combat reset | Goal chain + kit expectations → wave table |
| `pacing-pass` | Peak/valley vs density; measured duration; rest inserts | Back-to-back pressure, overlong session | Graybox path → pacing chart and safe zones |
| `blockout-pass` | Graybox scale, circulation, gates, sightlines | Whitebox, graybox, scale check | Goal chain → walkable graybox partitions |
| `narrative-beat-sheet` | Story beats as a gateable beat table | Narrative structure, acts and beats | Pillar tone → beat table + quest/dialogue hooks |
| `quest-spec` | Quest state machine, objective keys, rewards, fail and rollback | Quest brief, accept/complete conditions | Beats + economy sign-off → implementable quest spec |
| `lore-consistency-check` | Scan bible conflicts and timeline contradictions | Canon conflict, setting clash | Name tables → conflict cards or escalations |
| `dialogue-pass` | Polish dialogue by node intent; length, voice, skip | Dialogue polish, subtitle length | Node spec → shippable lines |
| `copy-pass` | Unify UI / item / system short copy: terms, length, tone | System prompts, empty states, error copy | Tone anchor + caps → per-scene copy files |
| `ux-flow-spec` | Key user flows with five states and exception node ids | UX flow, information architecture | Task list + state machine → stable-id flow |
| `ux-review-pass` | Walk the flow for lost, mis-tap, weak feedback | Usability review, hit targets | Flow + device → blocker / polish grades |

#### Typical vertical slice

“Chapter one can teach the combat gate”: `activate` names `level-designer` and `narrative-designer`. `next`: `narrative-beat-sheet` emits the gate beat → `level-goals-spec` writes measurable goals → `blockout-pass` proves scale → `encounter-script` + `pacing-pass`. Narrative continues with `quest-spec` on the detectors and `lore-consistency-check` on names. A copy subagent runs `copy-pass` / `dialogue-pass`. A UX subagent runs `ux-flow-spec` → `ux-review-pass`. `close` checks the goal chain, beat hooks, walkable graybox record, and five-state flow.

---

### 3. Client and server engineering

Engineering turns frozen interfaces into a buildable vertical slice. Client opens the happy path and fail states. Combat client aligns frames and prediction/rollback. UI client owns navigation stack and red dots. Server freezes contracts, saves, and anti-cheat hooks. Combat server owns settle authority. Tools engineering turns export and validation into a CI-able CLI. Authoritative numbers are not finalized in a client Notify callback.

| Craft | id |
| :--- | :--- |
| Client engineer | `client-engineer` |
| Client combat engineer | `client-combat-engineer` |
| Client UI engineer | `client-ui-engineer` |
| Server engineer | `server-engineer` |
| Server combat engineer | `server-combat-engineer` |
| Tools engineer | `tools-engineer` |

#### Craft paths

**`client-engineer`** — Non-combat feature slice, bugfix, general UI-logic collaboration.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Align contract | API / state machine / error codes; missing fields become tickets | — |
| 2. Vertical slice | Happy path builds and clicks; fail states reproduce | `feature-vertical-slice` |
| 3. Bind UI logic | Simple screen state; complex stacks go to UI engineer | `ui-logic-pass` |
| 4. Bugfix | Repro → evidence → hypotheses → minimal change → regression point | `client-bugfix` |
| 5. CI smoke | Critical path in CI; isolate flakes first | `ci-smoke` |
| 6. Logs and delivery | Layered keywords; change surface / risk / rollback | layout via `file-pack-layout` |

**`client-combat-engineer`** — Frame sync / hit presentation, skill hookup, prediction/rollback.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Spec and authority boundary | What must wait for server, prediction window, event-name dictionary | vs `server-combat-authority-check`; align `anim-event-hook` |
| 2. Skill presentation | Cast → feedback → recover; one fail state each | `feature-vertical-slice` |
| 3. Frame debug and rollback | Four-track timeline; presentation only | `client-combat-frame-debug` |
| 4. Hitboxes and multi-hit | Debug HUD quantifies early/late N ticks | collaborate `anim-event-hook` |
| 5. Bugfix, smoke, deliver | Minimal repro + seed; smoke in CI | `client-bugfix` · `ci-smoke` |

**`client-ui-engineer`** — Screen logic, navigation stack, red dots.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Read flow and five states | UX flow, modal layers, back expectation | — |
| 2. Navigation stack | Push / pop / replace; no dead stacks or click-through | `ui-logic-pass` |
| 3. Bind data and red dots | Empty / error / loading always bound; aggregate and clear timing | — |
| 4. Screen slice and smoke | Three resolutions; one weak-network case | `feature-vertical-slice` / `client-bugfix` / `ci-smoke` |
| 5. Check and handoff | Binding-field table; visual debt to UI art | — |

**`server-engineer`** — Contract → implementation checks → save migration → anti-cheat hooks → smoke.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Freeze contract | Fields, error codes, idempotency, version; test skeleton before implementation swell | `server-api-contract` |
| 2. Implement and validate | Authority at the server entry; grant/debit paired; no double spend | — |
| 3. Save schema and migration | Version, migrate, isolate bad saves; run on a copy first | `save-schema-pass` |
| 4. Anti-cheat hooks | Validate / rate / evidence on non-combat write entries | `anti-cheat-hook-check` |
| 5. Smoke and deliver | Contract / integration smoke | `ci-smoke` |

**`server-combat-engineer`** — Combat authority, settle validation, anti-cheat collaboration.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Authority boundary sign-off | Damage, win/lose, drops, CD must be server-final | `server-combat-authority-check` |
| 2. Settle and recompute | Recompute in formula order; reproducible seeds | — |
| 3. Contract, logs, replay | Reject illegal packets; classify replay drift | `server-api-contract` |
| 4. Anti-cheat collaboration | Critical write-path checks and false-positive review | `anti-cheat-hook-check` |
| 5. Smoke, stress, deliver | Settle unit tests + CI | `ci-smoke` |

**`tools-engineer`** — Pipeline tool spec, export repair, CI tool entry.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Tool spec | Duty, IO, exit codes, dry-run, rollback, permissions | `pipeline-tool-spec` |
| 2. Core path | Local happy path; errors point at a fix action | — |
| 3. Export-repair fixtures | Good/bad golden samples, idempotency, readable failure | `export-pipeline-fix` |
| 4. CI entry | Tool smoke in CI; stable artifact paths | `ci-smoke` |
| 5. Deliver and teach | How to run / dry-run / roll back; TA sign-off | — |

#### Related skills

| Skill | What it does | When | Input → output |
| :--- | :--- | :--- | :--- |
| `feature-vertical-slice` | Lock the question and a 3–5 minute scope; open happy path + fail states | Vertical slice, min-playable, demo | Contract / GDD → playable build |
| `ui-logic-pass` | Screen state machine, events, data bind, error handling | UI logic, nav stack, screen bind | Flow node ids → state machine and bind table |
| `client-bugfix` | Repro → evidence → hypotheses → minimal change → regression point | Client bugs, crashes | Bug ticket → minimal diff + before/after |
| `ci-smoke` | Probe test commands; run auto smoke subset and manual core batch | Pre-submit auto check, red localization | Repo test entry → smoke conclusion and log archive |
| `client-combat-frame-debug` | Align anim events / hit windows / VFX timeline; presentation only | Combat frames, hit windows, prediction rollback | Four-track timeline → HUD drift and frame log |
| `server-api-contract` | Freeze endpoint fields, error codes, idempotency, version rules; write contract tests | API freeze, protocol change | Field table → OpenAPI-equivalent + contract tests |
| `save-schema-pass` | Freeze save fields and version; migrate, load-validate, isolate bad saves | Saves, migration, corrupt saves | Schema → migration scripts and drill record |
| `anti-cheat-hook-check` | Circle critical write paths; check validate/rate/idempotency; bypass and false-positive tests | Anti-cheat hooks, tamper | Write-entry list → evidence logs and patches |
| `server-combat-authority-check` | Draw authority boundary; check settle inputs/seeds; illegal packets and replay drift | Combat authority, skill sync | Sign-off list → frozen authority vs predict table |
| `pipeline-tool-spec` | Tool duty, IO/exit codes, idempotent config, CI hook | New pipeline CLI, batch | Users + permissions → spec page |
| `export-pipeline-fix` | Run exporter on good/bad goldens; dependency/naming failure readability and idempotency | Export validation fail, asset pipeline | Golden hashes → fix + regression fixture |

#### Typical vertical slice

“Skill can cast, settle, and replay”: `activate` names `client-combat-engineer` and `server-combat-engineer`. Server first: `server-combat-authority-check` + `server-api-contract`. Client `next`: `feature-vertical-slice` then `client-combat-frame-debug`. Export blockers get a separate session naming `tools-engineer` for `export-pipeline-fix`. `close` checks the authority list, contract tests, slice fail states, settle unit tests, and `ci-smoke` logs. Non-combat feature slices name `client-engineer` + `server-engineer` (`save-schema-pass`).

---

### 4. Art and technical art

Art moves from a testable style anchor to a citable engine path. Concept delivers a makeable brief. Character and environment production pass checklists and naming gates. UI maintains the kit contract and four-state screens. Rig and animation hand skeleton, weights, and event frames to combat and VFX. Technical art turns import, LOD, shader, and VFX budgets into sampleable specs. Unapproved concepts do not enter production meshes. Failed graybox does not receive hero meshes.

| Craft | id |
| :--- | :--- |
| Character concept | `character-concept-artist` |
| Character art | `character-artist` |
| Environment concept | `environment-concept-artist` |
| Environment art | `environment-artist` |
| UI art | `ui-artist` |
| VFX | `vfx-artist` |
| Animation | `animator` |
| Rigging | `rigger` |
| Tech art | `tech-artist` |

#### Craft paths

**`character-concept-artist`** — Character visual design and makeable brief.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Lock style anchor | Color / light / silhouette language; readable at distance | `style-anchor` |
| 2. Multiple concepts | Two to four silhouette-different options; no production sheets until pick | — |
| 3. Production sheets | Turnarounds, material zones, socket expectations | `concept-key-art` |
| 4. Key art vs production | Marketing and production on separate tracks; 3D follows production only | — |
| 5. Brief and review | Frozen memory points, poly band; hand to `character-artist` | — |

**`character-artist`** — Character asset checklist and export convention.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Lock approved design | Approved concept / turnaround; lock poly / texture / LOD | vs `style-anchor` |
| 2. Character asset checklist | Model, UV, textures, LOD; expose over-budget immediately | `character-asset-checklist` |
| 3. Name, export, import | Complete remap table; pink materials and scale in-engine | `export-naming-gate` → `import-validate` · `lod-budget-pass` |
| 4. Collaborate and close | Topology notes to rig; style spot-check vs anchor | — |

**`environment-concept-artist`** — Environment / prop concept and spatial tone.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Lock tone and anchor | Scene brief: theme, time of day, guiding color | `style-anchor` |
| 2. Mood and hero props | Entry / combat / reward keyframes; modular hints | — |
| 3. Makeable handoff | Color/form/material bounds vs scale table | `blockout-pass` · `env-asset-checklist`; handoff craft `environment-artist` |
| 4. Production spot-check | After block-in, check drift vs mood | — |

**`environment-artist`** — Environment asset checklist and spatial presentation.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Receive graybox and tone | Hero mesh only after graybox partitions pass | `blockout-pass` |
| 2. Modular produce and dress | Module size, pivot, seams, collision, material reuse | `env-asset-checklist` |
| 3. Spatial presentation and budget | Vista cards, guiding color; join LOD / shader samples | `lod-budget-pass` (overage → `shader-budget-note`) |
| 4. Name, import, handoff | Partition replace map to level design | `export-naming-gate` → `import-validate` |

**`ui-artist`** — UI Kit and screen visual pass.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Align anchor and flows | Token palette, this-iteration screens, kit gaps | `style-anchor` |
| 2. Maintain kit contract | Variant × size × state; announce breaking changes | `ui-kit-spec` |
| 3. Single-screen pass | Information hierarchy, four states, jumps | `ui-screen-pass` |
| 4. Production follow-up | Multi-resolution spot-check; export names | `export-naming-gate` · `file-pack-layout` |
| 5. Check and handoff | Token and contract versions | — |

**`vfx-artist`** — VFX budget and skill-hook alignment.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Receive skills and hooks | Event names and sockets only; no full logic text | — |
| 2. Produce and align hooks | Fire on frame; interrupt cleanup | `vfx-skill-hook` |
| 3. Budget measure and degrade | Overdraw / particle caps; degrade still readable | `vfx-budget-pass` |
| 4. Deliver and regress | Map to combat assembly; animation event changes must regress | `import-validate` |

**`animator`** — Animation-set completeness and event hooks.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Lock set scope | Min-playable four families vs full set; event-name list only | — |
| 2. Animation-set checklist | List → repo → constraints → pack | `anim-set-checklist` |
| 3. Event frames | Hit / cancel / foot / cast release; align VFX | `anim-event-hook` |
| 4. Import and handoff | Freeze paths; debt explicitly scheduled | `import-validate` |

**`rigger`** — Skeleton bind, skin weights, deformation check.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Receive mesh and checklist | Skeleton template; extra bones need an application | `bind-rig-checklist` |
| 2. Skeleton and controls | FK/IK, acyclic constraints, socket names | — |
| 3. Skin weights | Extreme poses; influence-bone cap | `skin-weight-pass` |
| 4. Deformation check | Standard pose library; test clips with animation | — |
| 5. Export strip and import | Runtime bone count vs animation expectation | `export-naming-gate` → `import-validate` |

**`tech-artist`** — Import validation, naming gate, LOD / shader and performance-budget join.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Diagnose blocked assets | Source / pipeline / budget / engine preset | — |
| 2. Run gates | Name scan, import, golden regression | `import-validate` · `export-naming-gate` · `export-pipeline-fix` |
| 3. Budget calibration | Before/after device numbers and screenshots | `lod-budget-pass` · `shader-budget-note` · `vfx-budget-pass` |
| 4. Spec deposit and handoff | Versioned name segments, import presets, budget caps | — |

Procedural open-world terrain uses the cross-cutting skill `terrain-gaea-pass` (Gaea). There is no dedicated terrain craft.

#### Related skills

| Skill | What it does | When | Input → output |
| :--- | :--- | :--- | :--- |
| `style-anchor` | One visual rule, color/form/material bounds, reject criteria | Art style, art-bible slice | Love/hate refs → versioned anchor |
| `concept-key-art` | Brief, silhouette pick, 3D-ready key and turnarounds | Character sheets, key art | Anchor + pick → production-sheet path |
| `character-asset-checklist` | Banded model, UV, textures, LOD; import accept | Character models, high/low | Brief + band → ticked list and baseline pose |
| `env-asset-checklist` | Grid module size and pivot; seams, collision, material reuse, dress | Modular scenes | Scale table → dressed module pack |
| `export-naming-gate` | Scan Domain/Type/Name/Variant/LOD; batch rename; sync refs | Naming convention, asset rename | Exports → remap table |
| `import-validate` | Import with presets; machine-check scale/material/LOD; freeze citable path | FBX import, asset intake | Export files → frozen path |
| `lod-budget-pass` | Per-level poly ratios and switch distances; on-screen strategy | LOD budget, decimation | Band table → distance bands and sample evidence |
| `ui-kit-spec` | Inventory controls; variant × size × state contract | UI Kit, design system | Tokens + engine library → kit contract version |
| `ui-screen-pass` | Single-screen hierarchy, kit refs, polymorphism, jumps | Screen pass | Flow + kit → four-state screen pack |
| `vfx-budget-pass` | Overdraw / particle caps; measure hot spots; readable degrade | VFX budget, fillrate | Quality bands → degrade config and shots |
| `anim-set-checklist` | Min-playable and full action sets; clip presence and tech constraints | Animation set, locomotion, pack | Ability bounds → smokeable anim pack |
| `bind-rig-checklist` | Template skeleton, IK/constraints/sockets; extreme-pose bind check | Bind, rig, sockets | Production mesh → skeleton/socket table |
| `skin-weight-pass` | Extreme-pose weights; influence cap; compression preview | Skinning, collapse, flying verts | Rig → extreme-pose evidence |
| `shader-budget-note` | Variant and keyword inventory; whitelist and instruction caps | Shader budget, keyword explosion | Material list → whitelist and merge plan |

#### Typical vertical slice

“Hero can enter combat assembly”: `activate` names `character-concept-artist`; after approval, later sessions name `character-artist` → `rigger` → `animator` → `vfx-artist`. Import reds name `tech-artist`. `next` order: `style-anchor` → `concept-key-art` → `character-asset-checklist` → `export-naming-gate` / `import-validate` → `bind-rig-checklist` → `skin-weight-pass` → `anim-set-checklist` → `anim-event-hook` → `vfx-skill-hook` / `vfx-budget-pass`. `close` checks brief, import path, socket table, event dictionary, and budget shots. Environment line hands the `environment-concept-artist` brief to `environment-artist` after `blockout-pass`.

---

### 5. Quality assurance

QA turns “good enough” into observable start/stop conditions and an evidence pack. The lead owns the plan and exemptions. Functional QA extracts GWT from the GDD. Automation wires high-value cases to a stable scaffold. Compatibility runs N/N-1 and the device matrix. Performance resamples against a budget. Acceptance day does not rewrite criteria to paint green.

| Craft | id |
| :--- | :--- |
| QA lead | `qa-lead` |
| Functional QA | `qa-functional` |
| Automation QA | `qa-automation` |
| Compatibility QA | `qa-compatibility` |
| Performance QA | `qa-performance` |

#### Craft paths

**`qa-lead`** — Test plan, acceptance language, risk-exemption governance.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Plan | Scope, environments, observable start/stop conditions | `qa-plan` |
| 2. Acceptance language and evidence map | Who submits which path; no day-of rewrite | — |
| 3. Execution and rolling risk | Assign specialists; blocks have owners | — |
| 4. Summary and exemptions | Pass / conditional / fail; exemption has approver, expiry, payback | `artifacts-append` |
| 5. Retro and template feed | Miss-root-causes enter the next plan | `bug-report-write` (criteria-dispute samples) |

**`qa-functional`** — Functional cases, bug tickets, regression pack.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Read slice, lock scope | Happy path / edges / fail states; record build and table version | — |
| 2. Cases and traceability | ≥1 GWT per AC; traceability matrix | `test-case-from-gdd` |
| 3. Execute and file bugs | Repro steps; severity ≠ priority | `bug-report-write` |
| 4. Maintain regression pack | Every fix has a regression row; quarantine is not green | `regression-pack` |
| 5. Help acceptance | Evidence pack to lead; do not own the automation framework | — |

**`qa-automation`** — Automation scaffold, case–script map, stable CI smoke.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Scaffold | Folders, fixtures, non-zero CI hook, flake quarantine | `auto-test-scaffold` |
| 2. Case–script map | case_id ↔ script; coverage gaps and flakes | `case-automation-map` |
| 3. Stable scripts | Paired seed and cleanup; jitter-resistant waits | — |
| 4. CI smoke and auto regression | Small stable smoke set; clear red owner | `regression-pack` |
| 5. Boundary and handoff | Feel / real payment default out of coverage numerator | — |

**`qa-compatibility`** — N/N-1 save and protocol, device matrix, device-specific defects.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Device execution surface | Must / sample / retire; low-end and multi-GPU families listed | `device-matrix-pass` |
| 2. N/N-1 compat smoke | Old-save upgrade; protocol/resource fail is readable and non-dirty | `compat-smoke` |
| 3. Device-specific bugs | Driver/API clues vs all-device repro | `bug-report-write` |
| 4. Cert collaboration and matrix upkeep | Short clause items; screenshots include device | `platform-cert-smoke` |
| 5. Boundary check | Multi-resolution UI crop is not the compat trunk | — |

**`qa-performance`** — Performance-budget measurement and report; cert only collaborates on short clause items.

| Step | Intent | Skills opened |
| :--- | :--- | :--- |
| 1. Collect budget, freeze scenes | Target devices and frame / memory / load bands; routes in VCS | `perf-budget-check` |
| 2. Run and report | Fixed route, cold/warm start, p50/p95 | — |
| 3. Perf bugs and fix options | Hotspot to module/asset type; two or three options | `bug-report-write` |
| 4. Cert performance sample | Only clause-required short items | `platform-cert-smoke` |
| 5. Baseline and boundary | Resamplable; shader final call is not this job | — |

#### Related skills

| Skill | What it does | When | Input → output |
| :--- | :--- | :--- | :--- |
| `qa-plan` | Risk-matrix case volume and environments; observable start/stop | Test plan | Milestone entry/exit → approved plan |
| `artifacts-append` | Append this task’s artifact paths and summaries to the index | Artifact register, verify path refs | Paths → `artifacts/index.jsonl` |
| `test-case-from-gdd` | Extract testable points from GDD/AC as GWT; build a trace matrix | Writing cases | Slice + AC → case pack and matrix |
| `bug-report-write` | Write a reproducible defect | Filing bugs | Env + steps + evidence → ticket |
| `regression-pack` | Pack regression by change impact and historical defects | Version rerun, impact packing | Change surface → searchable queue |
| `auto-test-scaffold` | Test dirs, injectable fixtures, non-zero CI hook | Test scaffold, CI wiring | Repo convention → locally runnable sample |
| `case-automation-map` | Map GWT / regression cases to automation ids | Coverage gaps, flakes | Case pack → map and schedule |
| `device-matrix-pass` | High/mid/low must-test devices: functional smoke, heat, frame stability | Device matrix, low-end, degrade switches | Share source → versioned matrix |
| `compat-smoke` | N/N-1 matrix; old-save upgrade and readable failure | Compat, hot update, migrate | Version cells → result rows and isolated bad saves |
| `platform-cert-smoke` | Short list from target-store clauses | Cert, store review, submit smoke | Clause subset → compliance shot pack |
| `perf-budget-check` | Representative scenes, resamplable captures; locate over-budget items | Perf budget, profiler, hitch | Budget table + route → report and fix options |

#### Typical vertical slice

Version submit: `activate` names `qa-lead` (T2/`read` or `sandbox`). `next`: approved `qa-plan`, then assign — functional subagent `test-case-from-gdd` → `bug-report-write` → `regression-pack`; automation `auto-test-scaffold` → `case-automation-map`; compatibility `device-matrix-pass` → `compat-smoke`; performance `perf-budget-check`. Lead runs `artifacts-append` for the evidence index. `close` checks start/stop conditions, fatal-defect list, exemption expiry, and `verify-report.json`. Build-blocker inventory uses cross-cutting `build-gate-checklist`. Happy-path build acceptance uses `build-acceptance`.

---

### 6. Cross-cutting capabilities / runtime and filing cabinet

These skills are not listed on any craft `uses_skills`, but production sessions depend on them to scope, isolate writes, retrieve memory, close, and repair a deployment. They are the teeth of the runtime and the filing cabinet, not leftover utilities. Audio and terrain have no dedicated craft; their procedures still live in the library and must be named explicitly on the load-plan.

#### Place in the pipeline

Cross-cutting skills move the contract between layers: boot connectors, fill catalog gaps, assemble an execution order, push official writes into isolation roots, retrieve Canon by key, and close on core evidence only. Numeric craft bodies mention `attr-family-sync` / `data-readiness-check` / `excel-read` / `excel-format`, but those ids enter the opening set only when the load-plan names them.

#### Craft relationship

This module has **no** craft id. Any craft may name these skills in `loadplan.json` `items`. Producers commonly pair in-path `route-task` with this layer’s `doctor`, `assemble-craft-flow`, `verify-gate`, and `write-isolation`.

#### Skill groups

**Runtime and catalog**

| Skill | What it does | When | Input → output |
| :--- | :--- | :--- | :--- |
| `doctor` | Scan skill / craft / connector config gaps; emit minimal fill or redeploy actions | Activate fail, catalog mismatch, zero tools | Install tree + `catalog.json` → gap list and fill steps |
| `mcp-autostart` | Boot connectors by tier: core eager, others lazy | Connector down, core tier, lazy attach | `mcp-tiers.json` → handshake tool table |
| `assemble-craft-flow` | When the plan has several execute events, emit recommended order | Assemble, flow, execute events ≥ 3 | `loadplan` → `flow.json` (close steps last) |

**Write isolation and table recipe**

| Skill | What it does | When | Input → output |
| :--- | :--- | :--- | :--- |
| `write-isolation` | Official writes land on isolation roots first; promote only with human approval and record-set merge | Any write class other than `read` | `surfaces.json` → sandbox / worktree / `_Dev` landing |
| `excel-read` | Read-only workbook: locate range, values/formulas/styles, screenshot | Pre-write inspect, post-write read-back | Official or sandbox book → values/formulas/shots (no save) |
| `excel-format` | Hierarchy, column roles, decimals and placeholders, alignment; required after write | Color, layout, levels | Edited range → format-layer pass |
| `attr-family-sync` | When adding or reordering an attribute layer, read → edit → format → read across affected tables | New attribute family, multi-layer key sync | Framework change → downstream keys synced |
| `data-readiness-check` | Hard gate: numeric framework book and combat-sim data are ready | Multi-scenario balance, dry-run, table-tool rerun | Framework path → `data-readiness.json` |
| `personal-server-table-sync` | After table edits, export to the local personal server and reload | Local server sync, Luban, boot after table edit | Sandbox/official tables → reloaded local server |

**Memory, collaboration, and common sheets**

| Skill | What it does | When | Input → output |
| :--- | :--- | :--- | :--- |
| `memory-retrieve` | Before work, retrieve approved decisions, prior artifacts, and session records | Read Canon, find prior conclusions | `retrieve_keys` → hit list |
| `promote-adr` | Write a technical choice as a decision record: context, options, pick, consequences | ADR, architecture choice | Discussion → `adr/` file |
| `collab-protocol` | Clarify goal, offer fork options, advance in stages, get approval before official-path writes | Ask before write, staged approval | Fuzzy request → approved option |
| `naming-consistency-check` | Scan entity / field / UI-key collisions and drift | Term unify, rename | Name table → canonical names and replace order |
| `deliverable-sheets` | Fill decision, open-question, progress, and handoff summary sheets as needed | Decision table, open questions, progress | Session facts → registered common sheets |
| `diagram-pack` | Pick a tool by diagram kind: Mermaid / xmind / excalidraw / miro | Flowcharts, loops, architecture diagrams | Diagram intent → in-repo figure files |

**Build, acceptance, and close**

| Skill | What it does | When | Input → output |
| :--- | :--- | :--- | :--- |
| `verify-gate` | Before close, check only core evidence for the tier and write a verify report | Close | Tier + evidence paths → `verify-report.json` |
| `build-acceptance` | Run happy-path acceptance on the target build; align version; inventory known-issue disposition | Acceptance, submit-build check | Build number → acceptance record |
| `build-gate-checklist` | Inventory CI jobs, artifact paths, crash signatures, known-issue budget | Build blockers, CI red inventory | CI/artifact state → fixable blocker list |

**Audio and terrain (no dedicated craft; name explicitly)**

| Skill | What it does | When | Input → output |
| :--- | :--- | :--- | :--- |
| `audio-fmod-checklist` | FMOD Studio / Audacity / ffmpeg event intake and listen check | SFX, BGM, mix, intake | Event table → listen-passed events |
| `fmod-bank-build` | FMOD Studio / fmodstudiocl diagnose, bank build, GUID export | Banks, audio pack | FMOD project → bank + GUID |
| `terrain-gaea-pass` | Procedural terrain in Gaea; export for environment modules | Terrain, heightmap, open-world tiles | Tone brief → heightmap / tile export |

#### Typical vertical slice (the commands themselves)

Before any department opens work: `menu` (`刷新菜单.py`; the session-start hook also refreshes when the catalog is older than sources). `activate` writes `loadplan.json` (include `write-isolation` and `verify-gate`) and generates the set. Name `memory-retrieve` when prior conclusions matter. Open `write-isolation` and `excel-read` before official-surface edits. When execute events ≥ 3, `next` runs `assemble-craft-flow`. Deploy or handshake failure runs `doctor` + `mcp-autostart`. `close` accepts only a `verify-gate` report. Architecture choices name `promote-adr`.

---

## Where skills come from

Skills are distilled from real studio workflows. Checklists, table-write recipes, blockout and beat acceptance, contracts, and intake criteria already used by production, design, engineering, art, and QA are condensed into `SKILL.md` files with inputs, outputs, and fail-closed rollback. A craft file only ranks the steps; the procedure lives in the skill. Naming a skill opens an executable playbook.

The catalog’s **106** skills are the current distillation. New workflows become a skill first, then attach to a craft path. Full index: [docs/skills/index.md](docs/skills/index.md). Capability-layer note: [docs/architecture/l3-capability.md](docs/architecture/l3-capability.md).

---

## Engineering practice

Human gates and sandbox promotion implement the design logic. They are not the design logic.

### Human gates

These decisions change player experience or commercial outcomes and require a studio signature: experience pillars and fantasy tone, scope cuts, official-surface promotion, live economy and IAP pricing, irreversible destroy, secrets, legal / compliance, and ship. A model signature does not count.

The agent produces options, checklists, and isolation-surface diffs on short steps. The close command is `gsh close`. Cursor `stop` and Claude Code `Stop` check the same `verify-report.json`. Other tools use the CLI and `HOOKS.md`. Probe sessions start with `_` and do not overwrite `LATEST`.

### Sandbox promotion

Default `write_class` is `sandbox`. The model writes only to isolation roots declared in `.harness/surfaces.json`. Design tables, engine assets, and committed history are expensive to roll back.

Promotion is a production process: it needs a human, and it writes record cells only, so the diff stays reviewable. Whole-file overwrite of an official surface is forbidden. A passing `gsh close` is a precondition for promotion. Acceptance is not the same as an official write.

Secrets must not enter git or the model context. `mcp.json.example` is placeholders only. Setup never overwrites an existing `mcp.json`. Irreversible Git and recursive deletes require human confirmation. MCP `core` is a handshake list. `lazy_stdio` starts the child on the first `tools/call`.

---

## Problems it addresses

These are recurring production problems that a single prompt does not stabilize. GSH handles them with a four-layer file contract and a CLI.

**The context budget is consumed by the menu.** Injecting 106 skills and 35 crafts in full causes the model to edit formulas, discuss saves, and touch official tables in the same step. GSH treats `catalog.json` as a director lookup (`gsh menu`). Boot injects only the constitution, the current card, and named bodies.

**Multi-craft paths are expanded in one shot.** Level design has a fixed order from goals to blockout; narrative from beats to quest gates; progression from anchors to growth curves; combat numeric from anchors to coefficient tables. If naming a craft reads every `uses_skills` body, step one fills tables with step-five language. GSH opens `craft_open` only; `gsh next` advances.

**Official surfaces are mixed with drafts.** Design tables, engine assets, and committed history are expensive to roll back. GSH defaults to `write_class=sandbox`. Official writes require human approval and a record-cell changeset.

**Progress is lost when a session ends or the client changes.** Chat is not the archive. Progress lives in `current.md`, `state.json`, and `tasks.jsonl`. Any installed tool can run `gsh status` / `gsh resume`.

**Acceptance has no durable record.** Informal confirmation cannot enter release materials. `gsh close` writes `verify-report.json` (`verify_kind`, `evidence_paths`, `verdict`) and appends the audit log.

**Every MCP host handshakes at IDE start.** Dozens of `tools/list` calls stall boot and spend the context budget. GSH handshakes only the `core` keys in `mcp-tiers.json`; the rest stay lazy. This pack ships no live servers.

**Secrets enter model context; destructive commands run without confirmation.** Cursor and Claude Code intercept common secret paths on read and shell, and require confirmation for operations such as `git reset --hard`.

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

Swap any craft id into the same commands. Full paths live in the [department capability map](#department-capability-map). The combat-numeric cookbook remains one worked example. Level, narrative, progression, economy, systems, and QA use the same `menu` → `activate` → `next` → `close` loop.

### Scope a session and take one step

```bash
python -m gsh setup --workspace /path/to/studio --tools cursor --profile core --yes
cd /path/to/studio
python -m gsh menu --kind craft -q level
# also: systems design / narrative / progression / combat numeric / economy / QA
```

Write `.harness/sessions/<session>/loadplan.json` and name **one** craft in `items`, for example `level-designer`, `systems-designer`, `narrative-designer`, `progression-numeric-designer`, `economy-numeric-designer`, or `combat-numeric-designer`. Growth curves use `progression-numeric-designer` (skill `progression-curve`).

```bash
python -m gsh activate <session>
python -m gsh resume
# open the skill in craft_open; edit tables, blockout notes, or slice drafts on the isolation surface
python -m gsh next --craft <craft-id>
python -m gsh close --kind schema --evidence .harness/sandbox/<notes>.md
```

`activated.json` `craft_path` shows progress such as `2/9`. The current card stays in sync with `state.json`. Official record cells are written only after studio approval.

Combat-numeric walkthrough: [docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md). Docs map: [docs/README.md](docs/README.md) (architecture, adapters, cookbook, release).

### Continue on another client

After scoping in Cursor, open the same studio root in another client:

```bash
python -m gsh status --workspace /path/to/studio
python -m gsh resume --workspace /path/to/studio
```

Both sides read the same `.harness`. Cursor injects the current-card summary on `sessionStart`. Claude Code `settings.json` calls the same `hooks/开场.py`.

### Director lookup, not a full-menu inject

```bash
python -m gsh menu --kind skill -q excel
python -m gsh menu --kind craft -q qa
```

Output is an id plus one-line description. Do not put `catalog.json` in the system prompt. If the boot hook sees a full menu in context, it rewrites the turn to use `gsh menu`.

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

## Start using

Open the **studio root**, not only this repository. Replace placeholders in `.harness/surfaces.json` with machine-local paths. Do not commit real drive letters back to the GSH repository.

| Task | Entry |
|---|---|
| Scope a production round | `python -m gsh menu --kind craft -q milestone`, read `skills/route-task/SKILL.md` |
| Production and project management | `producer` · `associate-producer` · `project-manager` · `creative-director` |
| Design · systems and numeric | `systems-designer` · `combat-designer` · `combat-numeric-designer` · `economy-numeric-designer` · `progression-numeric-designer` · `monetization-designer` · `liveops-designer` |
| Design · level, narrative, copy, UX | `level-designer` · `narrative-designer` · `copywriter-designer` · `ux-designer` |
| Engineering | `client-engineer` · `client-combat-engineer` · `client-ui-engineer` · `server-engineer` · `server-combat-engineer` · `tools-engineer` |
| Art and tech art | `character-concept-artist` · `character-artist` · `environment-concept-artist` · `environment-artist` · `ui-artist` · `vfx-artist` · `animator` · `rigger` · `tech-artist` |
| Quality QA | `qa-lead` · `qa-functional` · `qa-automation` · `qa-compatibility` · `qa-performance` |
| Resume the current session | `python -m gsh resume` |
| Status | `python -m gsh status` |
| Close | `python -m gsh close --kind smoke --evidence <artifact>` |

```text
gsh menu -q level
  # or: systems design / narrative / progression / combat numeric / QA
  → write loadplan.json (name one craft id)
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
- `verify` and `tests/test_no_secrets.py` scan user-profile absolute paths, `Harness-Apps`, token prefixes, private-key armor, webhooks, and non-example emails.
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

See [CONTRIBUTING.md](CONTRIBUTING.md) · [SUPPORT.md](SUPPORT.md).

1. Edit skills only under `skills/<id>/SKILL.md`.
2. Edit crafts only under `agents/<id>.md`. `uses_skills` is a sequence that `gsh next` walks.
3. New MCP: purpose stub plus placeholders. Do not commit a connectable server or a secret.
4. After adding a craft or skill, mention the id in both README department maps (35/35, 106/106).
5. Changes to the four layers require a steer and an ADR.
6. Pull requests require a passing isolate `verify` and a passing `unittest` run.

The 0.1 duplicate trees such as `cursor/skills` are removed. Edit at repo root, then `sync`.

---

## Prerequisites

Environment and toolchain, stated separately from the design logic.

- **Python 3.11+**. Windows is a first-class game-production target. Linux / macOS are for isolate probes and CI.
- Open the **studio root**, not only this repository. Replace placeholders in `.harness/surfaces.json` with machine-local paths. Do not commit real drive letters back to the GSH repository.
- The installer projects architecture files and skills. It does not ship a game engine, DCC, or other production-software installer. It does not write secrets.
- Install only from the official repository or its GitHub Releases: [github.com/limoaCatherine/game-studio-harness](https://github.com/limoaCatherine/game-studio-harness). Third-party packages are outside maintenance. PyPI is not published yet.
- Edit content only at repo root: `skills/`, `agents/`, `rules/`, `hooks/`, `harness/`. The wheel ships those trees, so `pip install .` / `pipx install .` does not require a live clone.

---

## Install

```bash
git clone https://github.com/limoaCatherine/game-studio-harness.git
cd game-studio-harness
python -m pip install .
gsh setup --guided
```

Windows: `py -3.11 -m pip install .`, then `gsh setup --workspace <studio-root> --yes`.

Non-interactive:

```bash
gsh setup \
  --workspace /path/to/studio-root \
  --tools cursor,claude \
  --profile core \
  --yes
```

| Entry | Command |
|---|---|
| CLI on PATH | `gsh setup` |
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
gsh sync --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --yes
gsh uninstall --isolate-root /tmp/gsh-probe --yes
```

pipx, Release wheels, `GSH_PACK_ROOT`, and future PyPI: [docs/install.md](docs/install.md). Cutting a release: [docs/release.md](docs/release.md).

---

## License

[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · [LICENSE](LICENSE) MIT · [CHANGELOG.md](CHANGELOG.md) · [SECURITY.md](SECURITY.md)

The four layers are frozen. Progress is written under `.harness`. The only official source is the GitHub repository above.
