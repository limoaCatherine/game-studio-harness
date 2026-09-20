# Game Studio Harness (GSH)

**A context operating system for game studios.** Thirty-five craft paths, 106 skill procedures, 36 MCP connectors, and write isolation — deployed once to Cursor, Claude Code, Codex, Grok, and DeepSeek. This repository does not ship an engine or a DCC. It ships session orchestration: what to read this round, where writes may land, when a work item may close, and how trial-and-error becomes a promotable record set.

[中文](README.md) · [Docs index](docs/README.md) · [Inventory](#inventory) · [Department capability map](#department-capability-map) · [Install](#install-and-deployment)

| Crafts | Skills | MCP | Toolchains |
| :---: | :---: | :---: | :---: |
| 35 | 106 | 36 | Cursor · Claude Code · Codex · Grok · DeepSeek |

---

## Purpose

Game Studio Harness (GSH) is a **context operating system** for game studios. It turns what large-language-model agents actually lack in production — durable operating rules, a per-round load contract, a reusable craft/skill library, and a filing cabinet that survives session breaks — into four auditable layers. GSH is not a prompt pack and not an art or engine plugin. It answers the question a producer faces every day: **which craft this agent should play, which procedures to open, which surface it may write, and which evidence is required before close.**

### Who uses it

| Role | What they do in GSH |
| :--- | :--- |
| Producer / associate producer / project manager | Set milestones and delivery packs, name crafts, align dependencies and risk, drive acceptance and release notes |
| Creative director | Freeze experience pillars, critique vertical slices, adjudicate fantasy conflicts, approve Canon |
| Lead design (systems / combat / numeric / monetization / liveops) | Write rules, formulas, tables, events, and pay points as citable specs, then edit tables through the write recipe |
| Lead engineering (client / server / tools) | Implement vertical slices from contracts, authoritative combat resolution, save migrations, pipeline tools, and CI smoke |
| Art direction / technical art | Move from a style anchor and a makeable brief to importable assets, through naming, LOD, shader, and VFX budget gates |
| QA lead and specialists | Set acceptance criteria, write cases and regression packs, run compatibility / performance / automation, sign conclusions with evidence |

When one request spans different jobs, the parent session only names and closes. Prefer one subagent per craft. The boundary of focus is the job, not “please be the numeric designer and the client engineer at once.”

### What “running a vertical slice” means

A vertical slice is not the entire pipeline poured into one chat. It is a **bounded production session** that answers one question playable in about three to five minutes (for example: “is this skill loop readable in graybox and resolvable on the server?”):

1. **Scope** — `route-task` names this round’s `craft` / `skill` / `mcp` ids from `catalog.json` and writes `.harness/sessions/<session>/loadplan.json` (tier, write class, forbids, `retrieve_keys`).
2. **Activate** — `生成会话能力名单.py` writes `activated.json` and the current card `current.md`. A named craft injects only the craft body plus the first path step (`craft_open`). Later skills open when that step is reached.
3. **Produce** — Open skill files in craft order. Official-surface edits land first on isolation roots (table sandbox, code worktree, engine Sandbox, asset `_Dev`).
4. **Close** — `verify-gate` checks only core evidence for the tier and writes `verify-report.json`. After human approval, only the record set is written back. Whole-file overwrite of an official surface is forbidden.

A successful slice looks like this: the activated set is auditable, trial writes stay in the sandbox, the verify report’s `verdict` is `pass`, and promotion has a human approval plus a rollbackable diff. Sessions break and tools change. The next hand reads the current card, not the chat log.

### How the four layers cooperate

Context budget is a hard constraint. The constitution must enter every round, so it must stay thin. Procedures must be reusable, so they must be thick. Those two jobs cannot share a layer. The load-plan also cannot merge into the capability library: the library answers “how this kind of work is done”; the director answers “who is named this round.” The filing cabinet does not reason. It records where work stands, where official surfaces live, and which sentences are already approved.

| Layer | Role this round | Key files |
| :--- | :--- | :--- |
| Constitution | Always-on tax: read order, write isolation, secret interception, close only on a verify report | `constitution.md`, `rules/全局.mdc`, `hooks.json` |
| Load-plan | Collapse the request into an auditable named set, tier, and write class | `loadplan.json` → `activated.json` → `current.md` |
| Capability library | 35 craft paths + 106 skill bodies + 36 MCP purpose stubs; no per-session numbers | `agents/<id>.md`, `skills/<id>/SKILL.md`, `catalog.json` |
| Filing cabinet | Session state, official-surface map, approved facts, artifact index | `.harness/state.json`, `surfaces.json`, `canon/`, `adr/`, `artifacts/` |

The four layers are sealed. Architecture changes require a steer, a plan edit, and a decision record (`promote-adr`). Oral discussion and unclosed drafts must not impersonate Canon.

### What success looks like

- **Activated set**: `activated.json` contains only named skills, crafts, and MCPs. Craft paths are not pre-expanded. `craft_open` points at the current step.
- **Sandbox writes**: tables go to a sibling `沙箱/` folder, code to `.harness/worktrees/`, assets to `_Dev/`. `**/沙箱/` belongs in `.gitignore`.
- **Verify report**: `.harness/artifacts/<work-item>/verify-report.json` has `verdict=pass` and is registered in `artifacts/index.jsonl`.
- **Promotion**: after human approval, only the changeset / record set is merged. Forbidden columns are untouched. Read-back sampling passes. The stop hook does not accept an oral green.

---

## Inventory

The authoritative source is `catalog.json`, generated after install by `刷新菜单.py` from `agents/` and `skills/` frontmatter. Each of the five toolchain folders is a complete copy. The lists below match `cursor/agents/` (35) and `cursor/skills/` (106).

### 35 crafts

| Department | Craft ids |
| :--- | :--- |
| Production and project management | `producer` · `associate-producer` · `project-manager` · `creative-director` |
| Systems and numeric design | `systems-designer` · `combat-designer` · `combat-numeric-designer` · `economy-numeric-designer` · `progression-numeric-designer` · `monetization-designer` · `liveops-designer` |
| Level, narrative, copy, and UX | `level-designer` · `narrative-designer` · `copywriter-designer` · `ux-designer` |
| Client and server engineering | `client-engineer` · `client-combat-engineer` · `client-ui-engineer` · `server-engineer` · `server-combat-engineer` · `tools-engineer` |
| Art and technical art | `character-concept-artist` · `character-artist` · `environment-concept-artist` · `environment-artist` · `ui-artist` · `vfx-artist` · `animator` · `rigger` · `tech-artist` |
| Quality assurance | `qa-lead` · `qa-functional` · `qa-automation` · `qa-compatibility` · `qa-performance` |

### 106 skills

Craft `uses_skills` lists cover 85 event skills. The remaining 21 are not attached to any craft path and live in [Cross-cutting capabilities](#7-cross-cutting-capabilities--runtime-and-filing-cabinet): `assemble-craft-flow`, `attr-family-sync`, `audio-fmod-checklist`, `build-acceptance`, `build-gate-checklist`, `collab-protocol`, `data-readiness-check`, `deliverable-sheets`, `diagram-pack`, `doctor`, `excel-format`, `excel-read`, `fmod-bank-build`, `mcp-autostart`, `memory-retrieve`, `naming-consistency-check`, `personal-server-table-sync`, `promote-adr`, `terrain-gaea-pass`, `verify-gate`, `write-isolation`.

Every id appears in the department tables below. The capability map covers **35/35 crafts and 106/106 skills**.

### 36 MCP connectors

`accurig` · `audacity` · `blender-mcp` · `cascadeur` · `chrome-devtools` · `cloudcompare` · `docker-mcp` · `everything-search` · `excalidraw` · `excelMCP` · `ffmpeg` · `fmod-cli` · `fmod-studio` · `gaea` · `gamedev-mcp` · `gimp` · `imagemagick` · `inkscape` · `instant-meshes` · `krita-mcp` · `lark-mcp` · `ldtk` · `magicavoxel` · `materialize` · `materialpilot` · `meshlab` · `meshroom` · `miro` · `pureref` · `renderdoc` · `rokoko` · `roslyn-mcp` · `tiled` · `treeit` · `xmind` · `xnormal`

The core tier connects `excelMCP` at startup. The rest are lazy and spawn a child process on first call. See [MCP](#mcp).

---

## Department capability map

The map is organized by studio department. Each module includes: (1) where the department sits in the production pipeline; (2) every craft path — step intent and which skills it opens; (3) related skills with purpose, timing, and inputs/outputs; (4) how a typical vertical slice walks these files with `menu` / `activate` / `next` / `close`.

Session commands map to scripts as follows:

| Command | Script / skill | Writes |
| :--- | :--- | :--- |
| `menu` | `~/.cursor/harness/scripts/刷新菜单.py` | `catalog.json` |
| `activate` | `route-task` → `生成会话能力名单.py <session>` | `loadplan.json`, `activated.json`, `current.md` |
| `next` | Open the skill in `craft_open`; if many events, `assemble-craft-flow` → `建议执行单.py` | Next skill body, `flow.json` |
| `close` | `verify-gate` (plus `artifacts-append` / `sync-state` / `handoff-pack` when needed) | `verify-report.json`, artifact index, state write-back |

---

### 1. Production and project management

Production turns direction, capacity, dependencies, and acceptance into a trackable contract. The producer sets goals and release language. The associate producer splits packs and chases completeness. Project management keeps the risk register and dependency graph. The creative director freezes pillars and adjudicates experience conflicts. Without this layer, downstream crafts edit official surfaces inside an unapproved scope.

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

### 2. Systems and numeric design

This department turns play into a designable systems index, implementable GDD slices, resolvable combat objects, and promotable numeric tables. Systems design locks rules and interfaces. Combat design locks flow and kits. Three numeric crafts own combat formulas, economy loops, and progression curves. Monetization and liveops attach pay points and event calendars to the same entities and switches. Table edits always follow read → sandbox write → format → diff → human-approved promotion.

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

### 3. Level, narrative, copy, and UX

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

### 4. Client and server engineering

Engineering turns frozen interfaces into a buildable vertical slice. Client opens the happy path and fail states. Combat client aligns frames and prediction/rollback. UI client owns navigation stack and red dots. Server freezes contracts, saves, and anti-cheat hooks. Combat server owns settle authority. Tools engineering turns export and validation into a CI-able CLI. Authoritative numbers are not finalized in a client Notify callback.

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

### 5. Art and technical art

Art moves from a testable style anchor to a citable engine path. Concept delivers a makeable brief. Character and environment production pass checklists and naming gates. UI maintains the kit contract and four-state screens. Rig and animation hand skeleton, weights, and event frames to combat and VFX. Technical art turns import, LOD, shader, and VFX budgets into sampleable specs. Unapproved concepts do not enter production meshes. Failed graybox does not receive hero meshes.

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

### 6. Quality assurance

QA turns “good enough” into observable start/stop conditions and an evidence pack. The lead owns the plan and exemptions. Functional QA extracts GWT from the GDD. Automation wires high-value cases to a stable scaffold. Compatibility runs N/N-1 and the device matrix. Performance resamples against a budget. Acceptance day does not rewrite criteria to paint green.

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

### 7. Cross-cutting capabilities / runtime and filing cabinet

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

## Problems this repository addresses

A short list, separate from the capability map. GSH targets determinate agent behavior on a long production pipeline, not a genre-specific playbook of content bugs.

- **Guessed relevance**: opening every “maybe useful” skill without a load-plan, then mixing jobs, writes, and dialects.
- **Official-surface trial-and-error**: editing product tables, the main working tree, or ship assets with no rollback.
- **Oral green**: closing without `verify-report.json`. The stop hook intercepts.
- **Session amnesia**: losing goal, forbids, and artifact paths after a window change or compaction. The current card is the next hand’s source of truth.
- **Boot overload**: handshaking all thirty-six connectors during discovery. Core connects eagerly; the rest are lazy.
- **Hallucinated facts**: treating discussion drafts as Canon. The decision library stays closed unless `retrieve_keys` hits.

---

## Design philosophy

### Layer-two handshake with layer three

A model’s context budget cannot hold a full production pipeline. Injecting all 106 skills at once makes the agent play several jobs and edit tables or engine assets in the wrong dialect. GSH does not rely on “please focus” in a prompt. **The load-plan handshakes the capability library**: pick a craft or event first, then take only this round’s slice. A craft is a path, not a checklist — name a job, read step one, open the matching procedure when that step is reached. Connectors work the same way: handshake only the core at boot; attach the rest on first use.

```text
[request] → route-task vs catalog.json → loadplan.json
        → 生成会话能力名单.py → activated.json + current.md
        → inject named bodies and craft_open only → next by step → verify-gate
```

### Why four layers cannot become three

| Layer | Determinate problem it solves | Failure if absent |
| :--- | :--- | :--- |
| Constitution | Per-round tax; intercept secrets, destructive commands, oral green | Context filled by the menu; close without verification |
| Load-plan | Relevance becomes an explicit set | Mixed jobs, direct official writes, lost goal |
| Capability library | Standard procedures without per-session numbers | Re-inventing “how to edit a table” and “how to write a case” every round |
| Filing cabinet | Continuity after a session break | Forgotten progress after a window change; oral ideas treated as approved |

The five toolchain folders are five complete copies of the same four layers, not a fifth layer. Landing paths may change. The operating method should not.

---

## Key concepts

| Concept | Meaning |
| :--- | :--- |
| Craft | A job path in `agents/<id>.md`. `uses_skills` is a sequence, not an opening must-read list. |
| Skill | One procedure in `skills/<id>/SKILL.md`. Per-session numbers and paths stay out of the body. |
| Catalog | Unique id table generated by `刷新菜单.py` from frontmatter. Scoping must not invent ids. |
| Load-plan | `.harness/sessions/<session>/loadplan.json`: `tier`, `items`, `write_class`, `retrieve_keys`, `forbid`. |
| Activated set | `activated.json`: which bodies enter at boot. Not a runtime firewall. Missing skills may be opened mid-session. |
| Current card | `current.md`: goal, progress, write class, official surfaces, isolation roots, forbids, next step. |
| Write class | `read` / `sandbox` / `promote` / `destroy`. Default `sandbox`. |
| Official / isolation | `official` and `sandbox` per business kind in `surfaces.json`. |
| Tier | Discuss / T0 / T1 / T2 / T3 — how many core evidence items `verify-gate` checks. |
| Canon / ADR | Approved facts and architecture decisions; opened only when `retrieve_keys` hits. |
| Subagent | One craft per subagent when jobs differ; the parent session names and closes. |

---

## Guides

1. Open the studio root (with `.harness/`) in an adapted tool.
2. The session-start hook prints the current-card summary and named list. Do not pour the full `catalog.json` into context.
3. New delivery: restate the goal, run `route-task`, write `loadplan.json`, run `activate`.
4. Named craft: read only the craft body plus the current `craft_open` skill; `next` opens the following step.
5. Before writes, read `write-isolation` and `surfaces.json`. Table edits start with `excel-read`.
6. Many events and execute count ≥ 3: `assemble-craft-flow`.
7. Close: `verify-gate` writes the report; the hook validates schema and `pass`.
8. Job change: `handoff-pack` + `sync-state`, new session if needed.

Intent and work mode live in `skills/route-task/SKILL.md` (`continue` / `steer` / `park` / `new` / `parallel` / `discuss`; `work_mode` is `agent` or `plan`).

---

## Platform

| Folder | Tool | Constitution landing |
| :--- | :--- | :--- |
| `cursor/` | Cursor | `constitution.md`, `rules/`, `hooks/`, `hooks.json` |
| `claude/` | Claude Code | Isomorphic complete copy |
| `codex/` | Codex | Isomorphic complete copy |
| `grok/` | Grok | Isomorphic complete copy |
| `deepseek/` | DeepSeek | Isomorphic complete copy |

The installer lands a shared runtime at `~/.gsh`, then adapts each tool home. An existing `mcp.json` is not overwritten. The pack installs architecture, not host software. `studio/` is the studio-root `.harness` template (`surfaces.json`, `state.json`, sample Canon).

---

## Install and deployment

Windows, Python 3.11+. Clone this repository, double-click `一键部署.bat`, and enter a studio-root path (this creates `.harness`).

```powershell
# Deploy to a studio root; adapt all tools by default
.\一键部署.ps1 -Workspace D:\MyStudio

# Adapt selected tools only
.\一键部署.ps1 -Workspace D:\MyStudio -Tools cursor,claude
```

Isolated probe (does not write a real user home):

```powershell
python install/install.py --isolate-root D:\probe --workspace D:\probe\ws --tools all
python install/verify_install.py --isolate-root D:\probe --workspace D:\probe\ws
```

Entry points: `一键部署.bat`, `一键部署.ps1`, `install/install.py`. `install/pack.json` declares the five complete roots.

---

## CLI and session commands

There is no standalone `gsh` binary. Session commands map to user-level scripts (Cursor paths shown; the shared runtime also lives at `~/.gsh/harness/scripts/`):

```text
# menu — rebuild the catalog from skills/ agents/ mcp.json
python %USERPROFILE%\.cursor\harness\scripts\刷新菜单.py

# activate — validate loadplan ids; write activated.json and current.md
python %USERPROFILE%\.cursor\harness\scripts\生成会话能力名单.py <session-short-name>

# next — recommended order (execute first, close last)
python %USERPROFILE%\.cursor\harness\scripts\建议执行单.py <session-short-name> --force

# close — skill verify-gate writes the report; hooks/结束.py checks verdict
```

Close-class ids (tail of the execution sheet): `verify-gate`, `artifacts-append`, `handoff-pack`, `sync-state`.

Other scripts: `项目库.py` (current card), `接线自检.py`, `握手四层.py`, `整接.py`, `回归四层.py`, `应用外接档位.py`, `拉起外接.py`, `目录夹具.py`, `gsh_paths.py`.

---

## MCP

There is no runtime deny gate on connectors. The named MCP list is an opening hint: `needs_mcp` on named skills plus MCPs named on the plan. Naming a craft does not pre-expand connectors on its path. Open the matching skill when that step is reached. Calling an unnamed connector mid-session is allowed.

Tiers live in `harness/mcp-tiers.json`: core handshakes at boot (currently `excelMCP` only); the other 35 are lazy and spawn a child process on first call. Default framing is newline-delimited JSON. `lazy_stdio.py` exposes only tool declarations at IDE startup. URL passthrough (for example `miro`) is not wrapped locally. Launch scripts live in the user-level `harness/scripts/`. Purpose stubs live in `harness/mcp-tools/<id>.json`.

Per-tool dispatch notes: `cursor/harness/docs/MCP调度.md` (isomorphic copies under claude / codex / grok / deepseek).

The thirty-six connector ids: `accurig` · `audacity` · `blender-mcp` · `cascadeur` · `chrome-devtools` · `cloudcompare` · `docker-mcp` · `everything-search` · `excalidraw` · `excelMCP` · `ffmpeg` · `fmod-cli` · `fmod-studio` · `gaea` · `gamedev-mcp` · `gimp` · `imagemagick` · `inkscape` · `instant-meshes` · `krita-mcp` · `lark-mcp` · `ldtk` · `magicavoxel` · `materialize` · `materialpilot` · `meshlab` · `meshroom` · `miro` · `pureref` · `renderdoc` · `rokoko` · `roslyn-mcp` · `tiled` · `treeit` · `xmind` · `xnormal`.

---

## Security

- Secrets do not enter the repository. `mcp.json.example` holds placeholders only (for example `${LARK_APP_ID}`). The installer does not overwrite an existing `mcp.json`.
- The read interceptor `hooks/读文件前.py` blocks `.env`, `credentials.json`, `secrets.json`, `id_rsa`, `*.pem`.
- The command interceptor `hooks/命令前.py` requires a terminal confirm for `git push --force`, `git reset --hard`, and `git clean -fdx`. Close commands check `verify-report.json`.
- If a secret is committed: rotate immediately, then rewrite history. Do not revert only.
- Report vulnerabilities with a GitHub private advisory, not a public issue. Scope: [SECURITY.md](SECURITY.md).

---

## Troubleshooting

| Symptom | Check first |
| :--- | :--- |
| Activate fail / unknown id | `menu` refresh; run `doctor`; compare `catalog.json` with `agents/` and `skills/` |
| Zero tools at boot, or a dead connector | `mcp-autostart`; `mcp-tiers.json`; whether existing `mcp.json` is missing the core key |
| Current card disagrees with chat | Read `.harness/sessions/<session>/current.md` and `LATEST`; run `sync-state` |
| Table edit hit the official book | `write-isolation` + `surfaces.json`; sandbox should be sibling `沙箱/` |
| Close blocked by the stop hook | Add `verify-report.json` with `verdict=pass`; Discuss with no delivery should not write a report |
| Craft step one already speaks in last-step dialect | The set pre-expanded `uses_skills`; only `craft_open` should be injected |
| Isolated probe failed | Missing-item list from `install/verify_install.py --isolate-root …` |

---

## Tests

Architecture acceptance does not require host DCC:

```powershell
python install/verify_install.py --isolate-root D:\probe --workspace D:\probe\ws
```

Four-layer gray and regression (cwd = studio root; scripts already deployed to the user-level harness):

```text
python ~/.cursor/harness/scripts/接线自检.py
python ~/.cursor/harness/scripts/握手四层.py
python ~/.cursor/harness/scripts/整接.py
python ~/.cursor/harness/scripts/回归四层.py
```

`verify_install.py` checks required skills (`route-task`, `write-isolation`, `doctor`, `verify-gate`, `mcp-autostart`), hooks, and scripts, and scans secret-shaped paths. README craft/skill coverage is checked by `install/verify_readme_catalog.py` (35/35, 106/106).

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

- Skills live at `skills/<id>/SKILL.md` with `name`, `description`, and `needs_mcp` for common connectors. Per-session numbers stay out of the body.
- Crafts live at `agents/<id>.md`. `uses_skills` is a sequence, not an opening must-read list.
- Connector keys go in the `mcp.json` example; refresh the catalog to attach purpose stubs. New connectors default to lazy.
- Keep all five toolchain folders complete. Change one, sync the other four.
- Commit prefixes: `feat:` / `fix:` / `docs:` / `chore:`. Architecture changes write `promote-adr` first.
- After adding a craft or skill, update the department capability map in both `README.md` and `README.en.md` so coverage stays 35/35 and 106/106.

---

## License

[MIT](LICENSE). Copyright (c) 2026 Game Studio Harness contributors.
