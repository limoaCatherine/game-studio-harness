<p align="center">
  <img src="assets/four-layer.svg" alt="Game Studio Harness 四层" width="920" />
</p>

<h1 align="center">Game Studio Harness</h1>

<p align="center">
  <strong>游戏制作代理的四层上下文操作系统。</strong><br/>
  定档 → 切片 → 隔离制作 → 验证晋升。<br/>
  <a href="README.en.md">English</a> ·
  <a href="#安装">安装</a> ·
  <a href="#心智模型">心智模型</a> ·
  <a href="#逐层深讲">逐层深讲</a> ·
  <a href="#platform-support">平台矩阵</a> ·
  <a href="docs/mcp-policy.md">MCP 政策</a>
</p>

<p align="center">

| 职种 | 技能 | MCP 政策 | 适配器 |
| :---: | :---: | :---: | :---: |
| 35 crafts | 106 skills | **0** 条活服务器配送 / 36 用途桩 | Cursor 完整运行时 · 其余降级 |

</p>

> 窗口是稀缺的。正式面是不可逆的。会话会断。
>
> GSH 不是提示词合集，也不是 DCC 插件。它是大模型在复杂游戏制作流里的**上下文操作系统**。

> [!WARNING]
> **只从官方源安装。** 官方仓库：[github.com/limoaCatherine/game-studio-harness](https://github.com/limoaCatherine/game-studio-harness)。第三方打包、网盘镜像、未审查的 zip 不由本项目维护，可能被塞进恶意钩子或带密钥的 `mcp.json`。本仓 MIT，不捆绑 DCC 二进制，不提交工作室绝对路径。

---

## 安装

需要 **Python 3.11+**。Windows 游戏生产环境是一等公民；Linux / macOS 可用于隔离试装与 CI。安装器**不装** Excel、Blender、Unity、FMOD，也**不写**密钥。

> [!IMPORTANT]
> **每个工具只选一条安装路径。** 不要先跑 `setup --tools cursor` 再把手拷一份 `skills/` 进 `~/.cursor/skills`，再从旧的 `cursor/skills` 目录同步。旧的五套全量拷贝已经删除。真相源只有仓库根的 `skills/` `agents/` `rules/` `hooks/` `harness/`。

### 推荐路径：Python CLI

```bash
git clone https://github.com/limoaCatherine/game-studio-harness.git
cd game-studio-harness
python -m gsh setup --guided
```

非交互（CI / 脚本）：

```bash
python -m gsh setup \
  --workspace /path/to/studio-root \
  --tools cursor,claude \
  --profile core \
  --yes
```

等价入口（只选一个，不要叠）：

| 入口 | 命令 |
|---|---|
| 模块 | `python -m gsh setup` |
| Unix | `./install.sh` |
| Windows | `.\install.ps1` 或 `.\一键部署.ps1` |
| 旧路径兼容 | `python install/install.py` → 转给 `gsh setup` |

### 档位

| `--profile` | 装什么 | 适用 |
|---|---|---|
| `minimal` | L1 + 导演/隔离/收口等 12 条技能 + 4 条职种 | 先看清四层，不灌全库 |
| `core` | 日产导演、表格、切片、验收 + 常用职种 | 大多数制作会话 |
| `full`（默认） | 106 技能 + 35 职种 + 全部 MCP 桩 | 要完整菜单 |

改档位后重新 `setup` 或 `sync`。技能文件永远只在仓库根改。

### 按工具表

| `--tools` | 行为 |
|---|---|
| `cursor` | **完整运行时**：hooks + rules + skills + agents + harness + lazy MCP 包装 |
| `claude` | `CLAUDE.md` + 技能/职种投影。无 GSH 钩子 |
| `codex` | `AGENTS.md` + 技能投影（含 `~/.agents/skills`） |
| `grok` / `deepseek` | `AGENTS.md` + 技能投影。无钩子 |
| `windsurf` / `cline` / `opencode` / `gemini` | 指令文件 + 可选技能拷贝 |
| `continue` | `AGENTS.md` + 需手工合并的 snippet |
| `copilot` | **仅** `copilot-instructions.md` |
| `legacy` | 上述五件套：cursor,claude,codex,grok,deepseek |
| `all` | 含文档级适配器。**不是**功能对等 |

### 隔离试装（推荐先做）

不写真实 `~/.cursor`：

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

python -m gsh doctor --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws
```

`verify` 绿表示：菜单可解析、ID 唯一、职种不预展开、无密钥/绝对盘符、Cursor 投影与根 `skills/` 字节一致、仓库里不再有五套 `*/skills` 拷贝。

### 同步与卸载

```bash
# 改了根目录 skills/route-task/SKILL.md 之后
python -m gsh sync --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --yes

python -m gsh uninstall --isolate-root /tmp/gsh-probe --yes
```

卸载按 `install-state.json` 撤投影，**保留**用户已有 `mcp.json`，不碰业务根正式表。

---

## 开始使用

1. 用 Cursor（完整运行时）或其它工具打开**业务根**，不是只打开本仓。
2. 确认业务根有 `.harness/surfaces.json`。把 `<tables-root>` 等占位符改成你的盘，但不要把真实盘符提交回 GSH 仓库。
3. 第一句话先定档：读 `skills/route-task/SKILL.md`，写 `loadplan.json`，跑名单生成器。
4. 开场只读现行卡与点名正文。不要把 `catalog.json` 全文贴进对话。
5. 默认写 `sandbox`。晋升须人准，且只回写记录集。
6. 关项前写出 `verify-report.json` 且 `verdict=pass`。

一条完整游戏向例子见 [docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md)。

---

## 心智模型

```text
[用户诉求]
    → L2 导演点名（catalog 里的 id）
    → 锁定 L3 切片（职种只开第一步）
    → 注入有限上下文
    → 隔离根制作
    → 验证报告
    → 人准晋升正式面
```

大模型装不下一条完整制作流水线。把 106 条技能一次性灌进去，它会同时扮演战斗数值、客户端、QA，并在策划案未定稿时改引擎资产。

我们不靠提示词里的「请专注」。GSH 用**第二层对第三层握手**：点名集合是显式文件，职种是路径不是清单，外接默认不拉起。

四层不能合成三层，因为每一层解决的失败模式不同。见下表与[逐层深讲](#逐层深讲)。

---

## 本项目不是什么

- **不是** ECC 换皮。ECC 面向通用软件工程；GSH 面向游戏制作四层（定档、切片、隔离、晋升）。
- **不是** Unity / Unreal / Excel 插件市场。不配送 DCC。
- **不是** 云服务。没有账号、没有必选远程模型。
- **不是** 「36 个 MCP 开箱即用」。见 MCP 政策。
- **不是** 五工具功能对等层。Cursor 有钩子；Copilot 只有 instruction。
- **不是** 提示词角色扮演合集。职种是路径文件，技能是做法文件，闸是脚本。

```mermaid
flowchart LR
  L1[L1 宪法<br/>规则与钩子]
  L2[L2 定档<br/>loadplan 与名单]
  L3[L3 能力库<br/>skills / crafts / 桩]
  L4[L4 档案柜<br/>surfaces 与证据]
  L1 --> L2 --> L3 --> L4
  L4 -->|现行卡| L1
```

---

## What's Inside

```text
game-studio-harness/
├── skills/                 # 唯一真相：106 技能
├── agents/                 # 唯一真相：35 职种
├── rules/                  # L1 规则包
├── hooks/                  # L1 钩子 + hooks.json
├── harness/                # 运行时脚本、mcp-boot、mcp-tools 桩
├── gsh/                    # Python 3.11+ CLI
├── studio/.harness/        # L4 空数据脚手架
├── .cursor/                # 薄适配（无 skills 全树）
├── .claude/ .codex/        # 宪法投影
├── docs/                   # 架构 / 适配器 / 技能 / 职种 / cookbook
└── tests/                  # catalog、唯一 ID、不预展开、无密钥、投影、隔离 CLI
```

旧布局 `cursor/skills`、`claude/skills`、`grok/skills`、`deepseek/skills`、`codex/skills` **已删除**。不要把它们加回来。

---

## Key Concepts

| 概念 | 一句话 |
|---|---|
| 四层 | 宪法 / 定档 / 能力库 / 档案柜。已封版 |
| Agent / 职种 | `agents/<id>.md`。路径，不预展开 |
| Skill / 事件 | `skills/<id>/SKILL.md`。可复用做法，无当次数字 |
| Hook | Cursor 事件上的硬闸。其它工具没有 |
| Rule | 始终生效的薄税 |
| Filing | `.harness` 文件事实，不是知识图谱 |
| Catalog | 安装后生成的 ID 菜单 |
| Profile | minimal / core / full 决定投影哪些技能 |
| Isolate root | 试装树，不写真实家目录 |

---

## 逐层深讲

每一节都写：**处理什么 / 解决什么 / 路径 / 缺席崩溃模式**。

### 第一层：宪法（L1）

宪法是每轮都会进窗口的固定税。原则：**绝对拒绝变厚**。不写具体改表步骤，不管当次 TTK 数字。

```text
L1 始终在
  rules/全局.mdc     读序、名单语义、写隔离、结案
  AGENTS.md          跨工具入口（与 Claude/Codex 宪法同源）
  hooks/hooks.json   把文本绑到 Cursor 事件
  hooks/*.py         开场 / 工作区 / 读前 / 命令前 / 结束
```

#### `rules/全局.mdc`

- **处理什么**：会话生命周期、开场读序、名单四条语义（点名、needs_mcp 并入、职种不预展开、过程中可当场打开）、续/转向/插队/新/并行、定档必填字段、制作时按步打开、结案核证据、第四层表路径、四层封版。
- **解决什么**：模型自我发明流程；把 `catalog.json` 全文当系统提示；把职种 `uses_skills` 一次性读完。
- **路径**：仓库 `rules/全局.mdc` → 安装后 `~/.cursor/rules/全局.mdc`；打开本仓时还有 `.cursor/rules/全局.mdc` 这一份薄投影。
- **缺席**：无「开场读序」、无「不预展开」。代理串岗、预读整条战斗数值路径、用最后一步口径填第一步的锚点表。

#### `AGENTS.md` / `CLAUDE.md`

- **处理什么**：给没有 Cursor 规则引擎的工具一份同样的宪法。
- **解决什么**：Claude / Codex / Grok 打开业务根时至少知道读序与写隔离。
- **路径**：仓库根 `AGENTS.md`、`CLAUDE.md`；`.claude/CLAUDE.md`、`.codex/AGENTS.md` 是投影。
- **缺席**：指令型工具没有任何四层入口，退回成普通聊天。

#### `hooks/hooks.json`

- **处理什么**：注册 `sessionStart`、`beforeShellExecution`、`beforeReadFile`、`stop`。
- **解决什么**：没有注册表，规则只是 Markdown；有了注册表，Cursor 才会跑 Python 闸。
- **路径**：`hooks/hooks.json` → `~/.cursor/hooks.json`。
- **缺席**：钩子脚本躺在磁盘上也不会执行。
- **诚实**：只有 Cursor 认这份文件。Claude Code 的 hooks 是另一套，本仓不假装已经接上。

#### `hooks/开场.py`（sessionStart）

- **处理什么**：菜单过期则后台刷新；按需探活 MCP；向 stdout 打印现行卡摘要与点名列表；写入 `HARNESS_*` 环境。
- **解决什么**：拒绝把 100+ 技能菜单灌进第一轮；对齐「现在是哪次会话、上一步做到哪」。
- **路径**：`hooks/开场.py`，依赖 `工作区.py` 与 `harness/scripts/刷新菜单.py`。
- **缺席**：模型第一句话就猜进度；可能对过期 catalog 发明 ID。

#### `hooks/工作区.py`

- **处理什么**：向上找 `.harness`；读 `sessions/LATEST`；组装 `HARNESS_ROOT`、`HARNESS_SESSION`、`HARNESS_CURRENT_CARD`、写级别、职种下一步。
- **解决什么**：多仓、多终端、Cursor 与 Claude 同时开时路径硬编码、会话指针错位。
- **路径**：`hooks/工作区.py`。尊重 `CURSOR_HOME`、`GSH_ISOLATE_ROOT`。
- **缺席**：开场找不到业务根；现行卡注入失败；关项不知道 `bead_id`。

#### `hooks/读文件前.py`（beforeReadFile）

- **处理什么**：挡 `.env`、`credentials.json`、`secrets.json`、`id_rsa`、`*.pem`、`.ssh` / `.aws` / `.gnupg`。
- **解决什么**：密钥进模型上下文。
- **路径**：`hooks/读文件前.py`。`failClosed: true`。
- **缺席**：代理「为了调试」读进生产密钥。

#### `hooks/命令前.py`（beforeShellExecution）

- **处理什么**：识别 `git push --force`、`git reset --hard`、`git clean -fdx`（含嵌套 bash -c）；关项命令必须已有通过的验证报告。
- **解决什么**：试错失败后静默毁掉未提交改动；口头绿关项。
- **路径**：`hooks/命令前.py` + `校验验证报告.py`。
- **缺席**：硬重置无人确认；`bd close` 不看报告。

#### `hooks/结束.py`（stop）

- **处理什么**：`status=completed` 时校验报告 schema 与 `verdict`；缺现行卡则 followup。
- **解决什么**：带着 fail 或空报告交接。
- **路径**：`hooks/结束.py`。
- **缺席**：会话可以「看起来做完了」而没有证据文件。

#### `hooks/校验验证报告.py`

- **处理什么**：`bead_id` / `verify_kind` / `command` / `exit_code` / `evidence_paths` / `verdict` 字段机检。
- **解决什么**：报告是随便写的一段中文「过了」。
- **缺席**：命令前与结束钩子无法判定通过。

#### `hooks/数据就绪预检.py`

- **处理什么**：按环境变量与 `surfaces.json` 核框架簿是否存在。路径只来自环境与正式面地图，不写死工作室盘符。
- **解决什么**：框架簿缺失时仍开多场景平衡。
- **缺席**：战斗模拟建立在空表上。

#### `hooks/建议执行单.py` / `hooks/生成会话能力名单.py`

- **处理什么**：薄委托，权威实现在 `harness/scripts/`。
- **解决什么**：钩子目录与运行时脚本分叉。
- **缺席**：旧钩子若仍指向不存在的 `~/.cursor/harness/scripts`，定档失败。现已按 `gsh_paths` / 相对位置解析。

---

### 第二层：定档（L2）

定档层是导演。工人是 L3 技能与职种。

```text
诉求 → route-task → loadplan.json → 生成会话能力名单.py
                 → activated.json + current.md
                 → （多事件）建议执行单.py → flow.json
```

#### `skills/route-task/SKILL.md`

- **处理什么**：复述目标/交付/边界；对照 catalog 选 id；定 tier 与 write_class；写 loadplan；决定是否开子代理。
- **解决什么**：拿到诉求就改代码/改表。
- **路径**：`skills/route-task/SKILL.md`。
- **缺席**：无导演面，后续所有握手失去合同。

#### `harness/scripts/生成会话能力名单.py`

- **处理什么**：校验 id；职种不预展开，只写 `craft_open`；已点名 skill 的 `needs_mcp` 并入 `mcp_allow`；写 `activated.json` 与现行卡。
- **解决什么**：职种路径上 8 个技能一次性进窗口，第一步就用晋升口径说话。
- **路径**：`harness/scripts/生成会话能力名单.py <会话>`，cwd = 业务根。
- **缺席**：只有聊天里的「我点了战斗数值」，开场钩子看不到名单。

#### `activated.json`

- **处理什么**：本轮合同切片：skills / crafts / craft_open / mcp_allow / write_class / retrieve_keys。
- **解决什么**：名单可审计。它**不是**运行时防火墙——过程中仍可当场打开未点名技能。
- **路径**：`.harness/sessions/<id>/activated.json`。
- **缺席**：钩子环境变量里没有 `HARNESS_CRAFT_OPEN`。

#### `current.md`

- **处理什么**：会话 id、目标、进度、写级别、正式面、隔离根、禁改、下一步。
- **解决什么**：长对话、compaction、换窗口后的失忆。
- **路径**：`.harness/sessions/<id>/current.md`，由 `项目库.py` 写出。
- **缺席**：下一手靠聊天记录；聊天记录会被截断。

#### `loadplan.json`

- **处理什么**：必填 `session_id` `tier` `items` `verify_kind` `intent` `work_mode`。
- **解决什么**：把范围从「大概改战斗」变成可机读的项列表。
- **缺席**：生成器拒绝工作。

#### `harness/scripts/建议执行单.py`

- **处理什么**：多事件时把执行类排前、收口类（`artifacts-append` `verify-gate` `sync-state`）排后。
- **解决什么**：先写交接再做公式。
- **路径**：`flow.json`。
- **缺席**：顺序靠模型脾气。

---

### 第三层：能力库（L3）

静态、可复用、无当次路径。

#### `harness/scripts/刷新菜单.py` → `catalog.json`

- **处理什么**：扫 skills/agents frontmatter 与 mcp-tools 桩，写统一菜单。
- **解决什么**：现场发明 `skill-id`。
- **路径**：安装后 `~/.gsh/harness/catalog.json`，并拷到 Cursor harness。
- **缺席**：定档无权威 id；doctor 无法对齐。

#### 技能（106）

- **处理什么**：一类制作问题的做法。例如 `damage-formula-pass` 管通道与运算顺序；`excel-com-write` 管沙箱差量合并。
- **解决什么**：每次重发明「怎么改表」。
- **路径**：`skills/<id>/SKILL.md`。索引：[docs/skills/index.md](docs/skills/index.md)。
- **缺席**：该问题只能靠模型记忆，口径漂移。

完整列表按域：

1. **导演与收口**：`route-task` `assemble-craft-flow` `doctor` `verify-gate` `sync-state` `artifacts-append` `handoff-pack` `collab-protocol` `status-digest`
2. **记忆与晋升**：`memory-retrieve` `promote-canon` `promote-adr`
3. **写隔离与目录**：`write-isolation` `file-pack-layout`
4. **表格**：`excel-read` `excel-format` `excel-com-write` `tunable-table-diff` `data-readiness-check` `deliverable-sheets` `personal-server-table-sync`
5. **方向与范围**：`pillar-define` `scope-cut-decision` `feature-gdd-slice` `feature-vertical-slice` `experience-critique` `milestone-plan` `risk-register-update` `dependency-map` `systems-index-map` `rule-feasibility-check`
6. **战斗与数值**：`combat-modeling` `combat-flow-design` `combat-feel-checklist` `skill-kit-design` `skill-numeric-pass` `attribute-framework` `attr-family-sync` `damage-formula-pass` `counter-matrix-pass` `progression-curve`
7. **经济与商业化**：`economy-loop-analysis` `sink-source-map` `price-curve-pass` `inflation-stress` `iap-catalog-check` `monetization-kpi-pass`
8. **叙事关卡体验**：`narrative-beat-sheet` `quest-spec` `dialogue-pass` `lore-consistency-check` `copy-pass` `level-goals-spec` `blockout-pass` `encounter-script` `pacing-pass` `ux-flow-spec` `ux-review-pass` `ui-kit-spec` `ui-screen-pass` `ui-logic-pass`
9. **美术音频技美**：`style-anchor` `concept-key-art` `character-asset-checklist` `env-asset-checklist` `anim-set-checklist` `anim-event-hook` `bind-rig-checklist` `skin-weight-pass` `lod-budget-pass` `shader-budget-note` `vfx-budget-pass` `vfx-skill-hook` `audio-fmod-checklist` `fmod-bank-build` `export-naming-gate` `export-pipeline-fix` `import-validate` `terrain-gaea-pass`
10. **工程与测试**：`client-bugfix` `client-combat-frame-debug` `server-api-contract` `server-combat-authority-check` `anti-cheat-hook-check` `save-schema-pass` `auto-test-scaffold` `case-automation-map` `test-case-from-gdd` `qa-plan` `ci-smoke` `compat-smoke` `regression-pack` `bug-report-write` `build-gate-checklist` `build-acceptance` `device-matrix-pass` `perf-budget-check` `platform-cert-smoke` `release-notes-stub`
11. **活服与外接**：`liveops-calendar` `event-spec` `reward-mail-check` `mcp-autostart` `naming-consistency-check` `diagram-pack` `pipeline-tool-spec`

任一技能缺席：对应制作步骤没有标准做法，模型会现场发明字段名与晋升方式。

#### 职种（35）

- **处理什么**：一条岗位主路径。例如 `combat-numeric-designer` 串建模 → 属性 → 公式/克制/技能表 → 边角 → 表 diff。
- **解决什么**：多岗位协作时主会话串演导致口径混乱。岗位不同应开子代理，主会话点名与收口。
- **路径**：`agents/<id>.md`。索引：[docs/crafts/index.md](docs/crafts/index.md)。
- **缺席**：只能点散装技能，丢失推荐序与职责边界。

职种分组：

- 制作与方向：`producer` `associate-producer` `project-manager` `creative-director`
- 系统与数值：`systems-designer` `combat-designer` `combat-numeric-designer` `economy-numeric-designer` `progression-numeric-designer` `monetization-designer` `liveops-designer`
- 叙事关卡体验：`narrative-designer` `copywriter-designer` `level-designer` `ux-designer`
- 工程：`client-engineer` `client-combat-engineer` `client-ui-engineer` `server-engineer` `server-combat-engineer` `tools-engineer`
- 品质：`qa-lead` `qa-functional` `qa-automation` `qa-compatibility` `qa-performance`
- 美术音频：`character-concept-artist` `environment-concept-artist` `character-artist` `environment-artist` `ui-artist` `tech-artist` `animator` `rigger` `vfx-artist`

#### 外接档位与懒加载

- **处理什么**：`mcp-tiers.json` 把 `excelMCP` 标为 core **档位**；其余懒接；`lazy_stdio.py` 启动时只暴露工具声明。
- **解决什么**：对 36 个服务器做 `tools/list` 导致 Cursor 开场 30 秒卡死。
- **路径**：`harness/mcp-tiers.json`、`harness/mcp-boot/lazy_stdio.py`、`http_bridge.py`、`framer.py`。
- **缺席**：要么不开外接，要么一启动全拉。
- **诚实**：core 不等于「仓库已配送 excel 服务器」。见 [docs/mcp-policy.md](docs/mcp-policy.md)。

#### `harness/mcp-tools/*.json`（36 桩）

- **处理什么**：给菜单一行 purpose 与工具名。
- **解决什么**：catalog 里的 mcp 条目没有人话说明。
- **缺席**：点名外接时模型不知道它能干什么。
- **不是**：可执行 MCP。本仓配送活服务器 = 0。

#### `harness/mcp.json.example`

- **处理什么**：占位启动模板。`${PYTHON}` `${MCP_BOOT}` `${HARNESS_APPS}` `${LARK_APP_ID}`。
- **解决什么**：给出「若你本机要接，命令长什么样」的例子。
- **缺席**：用户只能自己猜 MCP 包装方式。
- **安装器**：默认不覆盖已有 `mcp.json`。`--write-mcp` 只在目标不存在时复制占位文件。

#### `harness/scripts/应用外接档位.py` / `拉起外接.py` / `mcp-autostart`

- **处理什么**：按档位套懒接、灌缓存、探活。
- **解决什么**：手改 `mcp.json` 忘记套 `lazy_stdio.py`。
- **缺席**：直连重型 MCP，开场超时。宿主不在时探活失败是预期，不是 GSH 装坏了。

#### `harness/scripts/握手四层.py` / `回归四层.py` / `接线自检.py` / `整接.py`

- **处理什么**：在业务根跑架构回归：L1 读序、职种不预展开、旧计划仍能生成。
- **解决什么**：改生成器时静默回到「预展开全路径」。
- **路径**：cwd 必须是业务根。尊重 `GSH_ISOLATE_ROOT`。
- **缺席**：只能靠 `python -m gsh verify` 做安装级检查，少一层运行时握手。

---

### 第四层：档案柜（L4）

文件事实。不是知识图谱。示例脚手架：`studio/.harness/`（空数据）。

#### `surfaces.json` / `write-isolation`

- **处理什么**：每个业务大类的 official ↔ sandbox。表 / git / 引擎 / 资产。
- **解决什么**：试错覆盖正式 xlsx、主仓、Content。
- **路径**：业务根 `.harness/surfaces.json`；模板 `harness/surfaces.default.json`；做法 `skills/write-isolation/SKILL.md`。
- **缺席**：默认写级别无处落地；代理直写正式面。

#### `state.json`

- **处理什么**：当前会话、进度、历史会话摘要。
- **解决什么**：换窗口不知道做到哪。
- **路径**：`.harness/state.json`。
- **缺席**：开场钩子没有 `HARNESS_PROGRESS`。

#### `tasks.jsonl`

- **处理什么**：只追加的激活/改动/关闭事件。
- **解决什么**：进度被改写、无法审计。
- **缺席**：没有时间线。

#### `sessions/<id>/`

- **处理什么**：loadplan、activated、current、flow。
- **解决什么**：一次会话一份合同。
- **缺席**：定档产物无处可放。

#### `canon/` / `adr/` / `memory-retrieve` / `promote-canon` / `promote-adr`

- **处理什么**：已批准事实与决策；只有 `retrieve_keys` 命中才打开。
- **解决什么**：口头讨论当 canon；或开场扫全库。
- **路径**：`.harness/memory/canon/`、`adr/`。示例：`studio/.harness/memory/canon/四层运行口径.md`。
- **缺席**：幻觉指导下游，或窗口被圣经灌满。

#### `verify-gate` / `verify-report.json` / `artifacts/index.jsonl`

- **处理什么**：按档位核核心证据，写出可机检报告并登记产物。
- **解决什么**：把「测试过了」从口头变成文件。
- **路径**：`.harness/artifacts/<bead>/verify-report.json`。
- **缺席**：L1 结束钩子不能关项。

#### `harness/scripts/项目库.py` / `目录夹具.py`

- **处理什么**：写现行卡、当前行、流水；测试夹具从菜单现查，不写死项目职种名。
- **解决什么**：脚本里出现工作室专名。
- **缺席**：现行卡无人写；回归夹具绑死某个游戏。

---

## CLI

```text
python -m gsh setup     # 引导或脚本化投影
python -m gsh sync      # 根真相源 → 已安装适配器
python -m gsh verify    # 架构 / ID / 不预展开 / 密钥 / 投影
python -m gsh doctor    # 漂移与假对等诊断
python -m gsh uninstall # 按 install-state 撤投影
```

`~/.gsh/install-state.json`（或 isolate `gsh/install-state.json`）记录 profile、tools、文件列表。

共享运行时在 `~/.gsh`：skills、agents、rules、hooks、harness、宪法。Cursor 家目录是完整运行时投影；其它家目录是指令投影。

---

## Platform Support

**禁止五工具假对等。** Cursor 是唯一完整运行时。

| 能力 | Cursor | Claude Code | Codex | Grok | DeepSeek | Windsurf | Cline | Continue | Copilot | OpenCode | Gemini |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 宪法文件 | 规则 + AGENTS | CLAUDE.md | AGENTS.md | AGENTS.md | AGENTS.md | AGENTS.md | AGENTS.md | snippet | instruction | AGENTS.md | GEMINI.md |
| 技能投影 | 是 | 是 | 是 | 是 | 是 | 可选 | 可选 | 否* | 否 | 可选 | 可选 |
| hooks.json 运行时 | **是** | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 |
| 开场现行卡 | **自动** | 约定 | 约定 | 约定 | 约定 | 约定 | 约定 | 约定 | 约定 | 约定 | 约定 |
| 密钥读拦截 | **是** | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 |
| 关项验证闸 | **是** | 约定 | 约定 | 约定 | 约定 | 约定 | 约定 | 约定 | 约定 | 约定 | 约定 |
| lazy MCP 包装 | **可接线** | 产品自带 MCP | 产品自带 | 通常无 | 通常无 | 产品自带 | 产品自带 | 产品自带 | 无 | 产品自带 | 产品自带 |

\*Continue 需要你把 snippet 合并进自己的 `config.yaml`，GSH 不会覆盖它。

每篇适配说明：[docs/adapters/](docs/adapters/)。跨工具总论：[docs/architecture/cross-harness.md](docs/architecture/cross-harness.md)。

---

## Token / 上下文优化

| 做法 | 省下什么 |
|---|---|
| L1 保持薄 | 每轮固定税 |
| 开场不灌 catalog 全文 | 100+ 条 description |
| 职种不预展开 | 一条职种路径上其余技能 |
| `retrieve_keys` 才打开 canon | 整本世界观圣经 |
| MCP 懒接 | 开场 `tools/list` 与宿主进程 |
| profile=minimal/core | 根本不投影用不到的技能 |
| 现行卡限长注入 | 开场钩子截断 current.md |

反模式：把 `catalog.json` 贴进自定义系统提示；把 35 个职种全文放进 `AGENTS.md`；把 36 条 MCP 全部直连。

---

## Security

- 密钥不进仓库。`mcp.json.example` 只有占位符。
- 安装器不覆盖已有 `mcp.json`。
- Cursor `beforeReadFile` 挡常见密钥路径（仅 Cursor）。
- 破坏性 git 要确认（仅 Cursor）。
- `verify` / `tests/test_no_secrets.py` 扫用户盘符、`Harness-Apps`、`ghp_` / `sk-`。
- 报告漏洞用 GitHub 私密报告，见 [SECURITY.md](SECURITY.md)。

---

## Troubleshooting

| 现象 | 先做什么 |
|---|---|
| `verify` 说 missing catalog | 先 `setup` 再 `verify`，同一 `--isolate-root` |
| 投影和根 skills 不一致 | `python -m gsh sync`，不要手改 `~/.cursor/skills` |
| 还存在 `cursor/skills` 全树 | 你在用旧 clone。拉 0.2 之后的布局 |
| Cursor 钩子没跑 | 确认装了 `--tools cursor`，且 IDE 读的是那个 hooks.json |
| Claude 没自动读现行卡 | 预期行为。先打开 `current.md` |
| MCP 36 条全红 | 预期。本仓不配送活服务器。只接你本机真正有的 |
| excelMCP 在 core 但连不上 | 档位 ≠ 配送。自己装本机服务器 |
| 职种一上来就谈晋升 | `activated.json` 被预展开了。跑 `tests/test_craft_no_preexpand.py` |
| `doctor` 报 Python 旧 | 升级到 3.11+ |
| 卸载删了 mcp.json | 不应发生。若发生，从备份恢复；请开 issue |

---

## Tests

```bash
python -m unittest discover -s tests -v
```

| 测试 | 断言 |
|---|---|
| `test_catalog.py` | ≥100 技能、≥30 职种、MCP 桩诚实 |
| `test_unique_ids.py` | id 非空、目录合法 |
| `test_craft_no_preexpand.py` | 点名职种只打开第一步 |
| `test_no_secrets.py` | 无用户盘符、无活密钥 |
| `test_projection_thin.py` | 无五套拷贝；`.cursor/skills` 不存在 |
| `test_cli_isolate.py` | isolate setup+verify；改根技能后 sync 对齐 |

---

## Contributing

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

硬规则：

1. 技能只改 `skills/<id>/SKILL.md`。不要在适配器目录再写一份。
2. 职种只改 `agents/<id>.md`。`uses_skills` 是序列。
3. 新 MCP 只加用途桩与 example 占位符，不要提交可连服务器或密钥。
4. 改四层先转向、改计划、写 ADR。
5. PR 必须 `python -m gsh verify` 在隔离根绿，以及 `unittest` 绿。

---

## 从 0.1 五树布局迁移

0.1 在仓库里维护了五份几乎相同的 `cursor/skills`、`claude/skills`、`codex/skills`、`grok/skills`、`deepseek/skills`。改一个技能要改五次，且容易假装五工具运行时对等。

0.2 破坏性变更：

| 旧路径 | 新路径 |
|---|---|
| `cursor/skills/` | `skills/` |
| `cursor/agents/` | `agents/` |
| `cursor/rules/` | `rules/` |
| `cursor/hooks/` + `cursor/hooks.json` | `hooks/` |
| `cursor/harness/` | `harness/` |
| `cursor/constitution.md` | `AGENTS.md` |
| `cursor/mcp.json.example` | `harness/mcp.json.example` |
| `claude/` `grok/` `deepseek/` 全树 | 删除；改由 `setup`/`sync` 投影 |
| `python install/install.py` | `python -m gsh setup`（旧入口仍转发） |
| `python install/verify_install.py` | `python -m gsh verify` |

迁移步骤：

1. 拉新布局。不要把旧的五棵树合并回来。
2. 若你曾经手改过 `~/.cursor/skills` 而仓库里没有：把 diff 挪到仓库根 `skills/`，再 `sync`。
3. 用隔离根跑一遍 `setup` + `verify`，确认绿再写真实家目录。
4. 真实家目录执行 `setup --tools … --yes`。已有 `mcp.json` 会被保留。
5. 业务根 `.harness` 只补缺失文件，不会清空你的 sessions。

---

## CLI 参考

### `setup`

| 开关 | 含义 |
|---|---|
| `--workspace PATH` | 业务根，创建/补齐 `.harness` |
| `--cursor-only` | 不建业务根 |
| `--tools LIST` | 见安装表。默认 `legacy` |
| `--profile minimal\|core\|full` | 投影哪些技能/职种 |
| `--isolate-root PATH` | 所有家目录改落到此树 |
| `--write-mcp` | 仅当目标没有 `mcp.json` 时复制占位 |
| `--guided` | 交互选工具与档位 |
| `--yes` | 非交互 |
| `--dry-run` | 只打印将写的路径 |
| `--pack-root PATH` | 仓库根，默认自动探测 |

### `sync`

读 `install-state.json` 里上次的 tools/profile（若存在），从仓库根重拷。这是「改一处技能、所有适配器对齐」的唯一合法方式。

### `verify`

失败码 2。检查包括：

- 仓库根存在 `skills/route-task`，且**不存在** `cursor/skills` 等五树
- `.cursor/skills` 不得存在
- catalog 可解析，技能/职种 id 唯一
- 至少一条职种带 `uses_skills`，且逻辑上不预展开
- 共享运行时与 Cursor 投影的 `route-task` 与仓库根字节一致
- 无本机用户主目录绝对路径、无硬编码宿主根、无 `ghp_` / `sk-` 一类活密钥
- 业务根具备 state / surfaces / 两份 canon 示例 / AGENTS.md / CLAUDE.md

### `doctor`

不修改文件。打印 Python 版本、install-state、菜单计数、MCP 政策、漂移提示。有问题时返回 1。

### `uninstall`

删除状态文件记录的投影目录。不删除 `mcp.json`。不删除业务根正式面。

---

## 会话生命周期（文件合同）

```text
新工作项
  mkdir .harness/sessions/<短名>
  写 loadplan.json
  python harness/scripts/生成会话能力名单.py <短名>
  读 current.md，打开点名正文
  制作（默认 sandbox）
  写 verify-report.json
  sync-state / artifacts-append
  人准 → promote（只回写记录集）
  关项（Cursor 钩子核报告）
```

续：同一聊天且同一未关交付 → 改计划增量，再生成名单。  
转向：口径变了 → 先改计划，禁止沿旧名单做完。  
插队：旧件 progress 写已停，新会话做新件。  
并行：互不依赖则各开会话；岗位不同开子代理。

探测会话名以 `_` 开头（例如 `_wire-check`）不会写入 `LATEST`，避免回归夹具盖住真人会话。

---

## 关键文件 schema（摘要）

### `loadplan.json`

必填：`session_id`、`tier`、`items`、`verify_kind`、`intent`、`work_mode`。  
建议：`write_class`、`retrieve_keys`、`forbid`、`bead_id`。  
`items[].kind`：`skill` | `craft` | `mcp` | `memory_plane` | `formula`。  
`items[].why` ≥ 8 字。

### `activated.json`

生成器写出。`ok` 为假时带 `errors`。`craft_open` 是 `{ craft_id: first_skill }`。`skills` 不得等于该职种全部 `uses_skills`。

### `verify-report.json`

`bead_id`、`verify_kind`（smoke|schema|playtest|build|release）、`command`、`exit_code`（整数）、`evidence_paths`（非空字符串数组）、`verdict`（pass|fail）。

### `surfaces.json`

`surfaces[]`：`id`、`kind`（excel|git|engine|draft）、`official`、`sandbox`、`note`。官方路径用占位符，不要提交 `D:\Studio\...`。

### `mcp-tiers.json`

`core` 是开场握手名单，不是「已安装服务器」名单。`boot.cache` / `boot.lazy_stdio` 由安装器改写成实际路径。

---

## 技能域缺席对照

下面按域写「整组不装时」的崩溃，而不是再抄一遍 description。完整 description 见 [docs/skills/index.md](docs/skills/index.md)。

| 域 | 不装时 |
|---|---|
| 导演与收口 | 无合同、无验证、无交接；会话无法关 |
| 记忆与晋升 | 口头当 canon；决策无法追溯 |
| 写隔离与目录 | 正式面与草稿混放；沙箱进 git |
| 表格 | 整文件覆盖 xlsx；无回读；无 diff 晋升 |
| 方向与范围 | 功能膨胀；支柱无法否决；竖切变成长线 |
| 战斗与数值 | 公式顺序漂移；克制与技能系数各写各的 |
| 经济与商业化 | 产销断裂；物价与 IAP 对不上 KPI |
| 叙事关卡体验 | 节拍与任务门闸脱节；灰盒未验就美术替换 |
| 美术音频技美 | 命名/LOD/挂点无门禁；Bank 与事件对不齐 |
| 工程与测试 | 无契约、无回归包、构建红灯靠感觉 |
| 活服与外接 | 活动撞车；外接全量直连卡死开场 |

`minimal` 档位只保证导演/隔离/收口还能转。要做战斗表，请用 `core` 或 `full`，或在 `minimal` 上再 `sync --profile core`。

---

## 职种缺席对照

| 组 | 不装时 |
|---|---|
| 制作与方向 | 无人拆交付包、无人裁范围、无人写里程碑证据 |
| 系统与数值 | GDD 与表字段脱节；战斗/经济/养成互相偷改主键 |
| 叙事关卡体验 | 任务状态机与 beat、灰盒、UX 五态对不齐 |
| 工程 | 客户端表现当权威；存档迁移无契约 |
| 品质 | 用例与自动化映射断裂；兼容与性能各测各的 |
| 美术音频 | Brief 不能进 3D；绑定/蒙皮/VFX 挂点无主路径 |

职种正文只列 skill id。做法永远读事件文件。不要把当次数字写进 `agents/*.md`。

---

## 运行时脚本清单

| 脚本 | 层 | 处理什么 | 缺席 |
|---|---|---|---|
| `刷新菜单.py` | L3 | 生成 catalog | 定档无菜单 |
| `生成会话能力名单.py` | L2 | 合同切片 | 无 activated / current |
| `建议执行单.py` | L2 | 多事件排序 | 先收口后制作 |
| `项目库.py` | L4 | 现行卡/当前行/流水 | 失忆 |
| `目录夹具.py` | 测试 | 从菜单现查职种 | 测试写死项目名 |
| `gsh_paths.py` | 全部 | 家目录与 isolate | 钩子写死 `~/.cursor` |
| `应用外接档位.py` | L3 | 套懒接 | 直连卡死 |
| `拉起外接.py` | L3 | 探活/自启 | 开场对死进程握手 |
| `握手四层.py` | 回归 | 四层互相看见 | 架构回归靠手工 |
| `回归四层.py` | 回归 | 旧计划灰度 | 新口径打破旧会话 |
| `接线自检.py` | 回归 | 职种不预展开 | 预展开回归 |
| `整接.py` | 回归 | 菜单→名单→钩子→项目库 | 单测绿、集成红 |

---

## 打开本仓库 vs 打开业务根

| 你打开的是 | 应该发生的事 |
|---|---|
| 本仓库 | 改技能/职种/钩子/CLI。规则来自 `.cursor/rules/全局.mdc`。不要在这里填真实表路径 |
| 业务根 | 做游戏。`.harness` 是档案柜。技能从已安装投影或本仓 SSOT 读取 |

把 GSH 仓库当成游戏内容仓会把示例 `surfaces.json` 的占位符和真实盘符混在一起。内容仓请另开目录，用 `setup --workspace` 只补 `.harness`。

---

## Cookbook

游戏向端到端（战斗数值竖切）：[docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md)。

步骤摘要：隔离安装 → 写 loadplan 点 `combat-numeric-designer` → 生成名单并确认未预展开 → 只做 `craft_open` → 沙箱改表 → T1 验证报告 → 人准回写记录格。

若要把同一条路径用在养成或经济：换职种 id（`progression-numeric-designer` / `economy-numeric-designer`），仍然禁止预展开，仍然默认 sandbox。

---

## 文档地图

| 文档 | 内容 |
|---|---|
| [docs/architecture/l1-constitution.md](docs/architecture/l1-constitution.md) | L1 模块级 |
| [docs/architecture/l2-director.md](docs/architecture/l2-director.md) | L2 模块级 |
| [docs/architecture/l3-capability.md](docs/architecture/l3-capability.md) | L3 与 MCP 诚实政策 |
| [docs/architecture/l4-filing.md](docs/architecture/l4-filing.md) | L4 表与写隔离 |
| [docs/architecture/cross-harness.md](docs/architecture/cross-harness.md) | 跨工具 |
| [docs/mcp-policy.md](docs/mcp-policy.md) | 可接线 / 仅桩 / 不配送 |
| [docs/skills/index.md](docs/skills/index.md) | 106 技能表 |
| [docs/crafts/index.md](docs/crafts/index.md) | 35 职种表 |
| [docs/adapters/](docs/adapters/) | 每工具一篇 |
| [docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md) | 端到端 |

---

## 常见错误（游戏制作现场）

1. **把职种当技能清单。** 点了 `combat-numeric-designer` 就把 `uses_skills` 全部读进上下文。生成器若配合你这么做，是 bug。
2. **把 catalog 当系统提示。** 菜单是给导演选 id 的，不是给工人背诵的。
3. **在 GSH 仓库里填真实表路径。** `surfaces.json` 示例必须保持占位符。
4. **声称 36 MCP 已可用。** 用途桩 ≠ 进程。excelMCP 在 core 列表里 ≠ 配送了 COM 桥。
5. **在 Claude 里期待 Cursor 钩子。** 关项闸不会跑。你必须自己看 `verify-report.json`。
6. **手改 `~/.claude/skills` 而不改仓库根。** 下次 `sync` 会被 SSOT 盖掉。先改 `skills/`。
7. **五工具各维护一棵技能树。** 这正是 0.2 要删掉的布局。
8. **未人准整文件覆盖正式 xlsx。** 只回写 changeset 记录格。
9. **探测会话写入 LATEST。** 回归夹具必须以 `_` 开头。
10. **用 Copilot 当完整运行时。** Copilot 只有 instruction。

---

## 环境变量

| 变量 | 作用 |
|---|---|
| `GSH_PACK_ROOT` | 仓库根覆盖 |
| `GSH_ISOLATE_ROOT` | 隔离探测根 |
| `GSH_HOME` | 共享运行时（默认 `~/.gsh`） |
| `CURSOR_HOME` / `CLAUDE_HOME` / `CODEX_HOME` / `GROK_HOME` / `DSH_HOME` | 各工具家目录 |
| `AGENTS_SKILLS` | Codex/DeepSeek 共用的 `~/.agents/skills` |
| `HARNESS_ROOT` | 业务根（钩子也可从 `.harness` 上溯） |
| `HARNESS_SESSION` | 会话短名；`LATEST` 优先 |
| `HARNESS_HOST_PATHS` | 本机宿主路径图（不进仓库） |
| `FRAMEWORK_WORKBOOK` / `BATTLE_SIM_WORKBOOK` | 数据就绪预检 |
| `DATA_READY_SHEETS` | 预检页签名单 |

安装器在 isolate 模式下不依赖这些变量，而是按目录约定放置。

---

## 行为准则与许可

- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [LICENSE](LICENSE) MIT
- [CHANGELOG.md](CHANGELOG.md)

四层已封版。口头讨论不是 canon。写隔离是默认牙齿。密钥不进仓库。官方源只有上面的 GitHub 仓库。

---

## FAQ

**Q. 为什么中文主 README？**  
A. 目标用户是中文游戏制作管线。英文镜像见 [README.en.md](README.en.md)。

**Q. 为什么技能路径里还写 `~/.cursor/...`？**  
A. 那是 Cursor 安装后的运行时落点。仓库真相源是根目录 `skills/`。安装器把同一份文件投影到 `~/.gsh` 与 `~/.cursor`。

**Q. 可以只拷几个技能到 Claude 吗？**  
A. 可以。`--profile minimal` 或 `core`，`--tools claude`。不要再开一棵 `claude/skills` 手维护树。

**Q. 隔离根和业务根有什么区别？**  
A. 隔离根模拟 `~/.gsh` 与各工具家目录。业务根是游戏内容与 `.harness`。`verify` 两者都查。

**Q. 为什么 verify 要查「无五树」？**  
A. 防止回归到 0.1。五树是本重构要消灭的失败模式。

**Q. 钩子能在 Windows 上跑吗？**  
A. 可以。`hooks.json` 用 `python hooks/开场.py`。需要 Python 3.11+ 在 PATH。

**Q. 失败了如何看日志？**  
A. `setup`/`verify` 打印 `error:` 行。`doctor` 给漂移提示。Cursor 钩子自己的 stdout 在 IDE 钩子日志里。

**Q. 我能加第 107 个技能吗？**  
A. 能。落在 `skills/<id>/SKILL.md`，frontmatter 写 `name`/`description`/`needs_mcp`，然后 `sync`，不要复制到适配器目录。

**Q. 四层能加第五层吗？**  
A. 不能顺便加。须转向、改计划、写 ADR。见 `studio/.harness/memory/canon/四层封版.md`。
