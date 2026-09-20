# Game Studio Harness (GSH)

**游戏制作代理的四层编排系统。** 技能、职种、外接、写隔离，一次性部署到 Cursor、Claude Code、Codex、Grok、DeepSeek。

[English](#english) · [安装与部署](#安装与部署) · [设计哲学](#设计哲学) · [第一层：宪法 (L1 Constitution)](#第一层宪法-l1-constitution) · [第二层：定档 (L2 Director)](#第二层定档-l2-director) · [第三层：能力库 (L3 Capability Library)](#第三层能力库-l3-capability-library) · [第四层：档案柜 (L4 Filing Cabinet)](#第四层档案柜-l4-filing-cabinet) · [行为准则](#行为准则) · [许可](#许可)

| 职种支持 | 技能库 | 外接工具 | 适配工具链 |
| :---: | :---: | :---: | :---: |
| 35 | 106 | 36 | Cursor · Claude Code · Codex · Grok · DeepSeek |

> 窗口是稀缺的。正式面是不可逆的。会话会断。
>
> GSH 不是一个提示词集合，也不是一个 DCC 插件。它是大模型在复杂游戏制作流中的**上下文操作系统**。

---

## 安装与部署

Windows，Python 3.11+。克隆本仓，双击 `一键部署.bat`，填写业务根路径（将自动创建 `.harness` 目录结构）。

```powershell
# 部署到指定业务根，默认适配所有工具
.\一键部署.ps1 -Workspace D:\MyStudio

# 仅适配指定工具
.\一键部署.ps1 -Workspace D:\MyStudio -Tools cursor,claude
```

### 隔离试装与架构验证

在不污染真实用户家目录（如 `~/.cursor`）的情况下，使用隔离根进行完整性自检：

```powershell
# 1. 模拟安装到隔离根
python install/install.py --isolate-root D:\probe --workspace D:\probe\ws --tools all

# 2. 运行架构级完整性与安全性验证
python install/verify_install.py --isolate-root D:\probe --workspace D:\probe\ws
```

---

## 设计哲学

### 1. 专注度：第二层对第三层的“握手”

大模型的上下文窗口装不下一条完整的游戏制作流水线。一条流水线从方向（体验支柱、砍范围）、规则与数值（系统、战斗、养成、经济）、体验与资产（叙事、关卡、美术、音频）、工程与验收（客户端、服务端、测试）走到活服运营，涉及的做法（Skills）多达上百种。

如果把所有技能一次性灌入上下文，模型会因为“全能”而陷入混乱：它会同时扮演多个岗位、在修改表结构时使用客户端代码的口径、在策划案未定稿时直接修改引擎资产。

我们不靠提示词里的“请专注”。G GSH 采用**第二层对第三层握手**的机制：
- **按需切片加载**：在会话开始时，由第二层（定档）明确这一轮要扮演的“职种（Craft）”或“事件（Skill）”。
- **职种是路径，不是清单**：点名一个职种（如战斗数值策划），只注入该职种的骨架和**第一步（`craft_open`）**的做法。随着制作推进，走到下一步时，再按步打开对应的技能文件。
- **外接懒加载**：36 条外接工具默认不拉起，只有在真正调用工具时才通过懒加载器激活，防止开场握手吃掉大半窗口。

```text
[用户诉求] -> L2 导演点名 -> 锁定 L3 做法切片 -> 注入有限上下文 -> 代理专注执行
```

### 2. 四层为什么不能合成三层？

| 层级 | 核心职责 | 解决的确定性问题 | 缺席时的崩溃模式 |
| :--- | :--- | :--- | :--- |
| **L1 宪法** | 无论做什么都不能忘的运转规则 | 规范每轮对话的固定税，拦截高危动作与坏档 | 窗口被菜单和做法填满，模型随意重置或强推代码 |
| **L2 定档** | 这一轮点谁、写到哪、怎么收口 | 将“相关性”从模型猜测变成显式、可审计的集合 | 代理串岗、抢写、直接修改正式文件、中途迷失目标 |
| **L3 能力库** | 可复用的做法（Skills）与岗位路径 | 沉淀标准的制作规范，不掺杂当次数字与临时路径 | 每次对话都需要重新发明“怎么改表”和“怎么写用例” |
| **L4 档案柜** | 做到哪、正式面在哪、哪句已批准 | 解决会话中断、换窗口、换工具后的状态连续性 | 换个聊天窗口就忘记进度，把口头讨论当成已批准事实 |

---

## 第一层：宪法 (L1 Constitution)

宪法是每轮对话都会进入窗口的**固定税**。税越重，留给业务制作的窗口预算就越少。因此，L1 的核心设计原则是：**绝对拒绝变厚**。它不包含任何具体业务做法，只管运转不变量。

### 1. 始终生效的规则：`rules/全局.mdc` / `constitution.md`
- **处理的事情**：定义了会话生命周期（定档 → 制作 → 结案）、开场读序、名单语义、写隔离原则和四层封版红线。
- **解决的问题**：防止模型在执行过程中“自我格式化”或发明新的工作流程。它强制模型在开场时必须先读现行卡，再读点名技能，最后读命中的记忆，锁死认知顺序。

### 2. 钩子注册表：`hooks.json`
- **处理的事情**：将静态的规则绑定到 IDE 的运行时事件（`sessionStart`、`beforeShellExecution`、`beforeReadFile`、`stop`）。
- **解决的问题**：没有注册表，规则只是文本；有了注册表，规则变成了确定性的**运行时硬拦截**。

### 3. 开场钩子：`hooks/开场.py` (SessionStart)
- **处理的事情**：在会话唤醒的第一时间，检查菜单是否过期（若过期则后台调用 `刷新菜单.py`），按需对 MCP 进行静默探活，并向标准输出打印**现行卡摘要与点名列表**。
- **解决的问题**：
  - **防止信息过载**：拒绝把 `catalog.json`（包含 100+ 技能的完整菜单）灌进上下文。
  - **环境对齐**：确保模型在说第一句话之前，就知道当前处于哪个会话、上一步做到了哪里、这一轮被点名了哪些技能。

### 4. 工作区定位器：`hooks/工作区.py`
- **处理的事情**：向上逐级递归探测 `.harness` 标记，精确定位业务根路径；读取 `sessions/LATEST` 指针，解析当前激活的会话 ID；将所有路径和状态组装为 `HARNESS_*` 环境变量。
- **解决的问题**：解决多仓、多终端、多工具（如同时开着 Cursor 和 Claude Code）运行时，状态无法共享、路径硬编码、会话指针错位的痛点。

### 5. 读拦截器：`hooks/读文件前.py` (beforeReadFile)
- **处理的事情**：在模型试图读取任何文件进窗口之前，对路径进行正则匹配，拦截 `.env`、`credentials.json`、`secrets.json`、`id_rsa`、`*.pem` 等敏感路径。
- **解决的问题**：**从根源上杜绝密钥和私钥泄露给大模型**。强制要求密钥留在本地密钥管理处，模型只能使用环境变量占位符。

### 6. 命令拦截器：`hooks/命令前.py` (beforeShellExecution)
- **处理的事情**：
  - 解析命令行 token，识别 `git push --force`、`git reset --hard`、`git clean -fdx` 等不可逆的破坏性命令，强制要求用户在终端输入 `confirm`。
  - 拦截关项类命令，检查当前工作项的 `verify-report.json` 是否存在且结论为 `pass`。
- **解决的问题**：
  - 防止代理在试错失败后，静默运行硬重置，毁掉用户的本地未提交改动。
  - 拦截“口头绿”：防止代理在没有跑通测试、没有产出验证报告的情况下，直接宣布任务完成并关闭会话。

### 7. 结束钩子：`hooks/结束.py` (Stop)
- **处理的事情**：在会话结束（completed）时，校验 `verify-report.json` 的 schema 规范。如果报告不合规或结论非 `pass`，向模型输出 followup 消息，阻止其关项，并提示修复路径。
- **解决的问题**：确保每一次交付都具备确定性的闭环证据，防止代理带着未决问题、坏档或未格式化的表格草率交接。

---

## 第二层：定档 (L2 Director)

定档层是**导演**，不是工人。它负责把用户的模糊诉求拆解为确定性的上下文边界、写级别和收口证据。

```text
[用户诉求] 
   │
   ▼
[route-task] ──(对照 catalog.json 选 ID)──> [loadplan.json]
                                                   │
                                                   ▼
[current.md] <──(不预展开 uses_skills)── [生成会话能力名单.py]
```

### 1. 导演技能：`route-task`
- **处理的事情**：
  - 强制复述目标、交付物、范围边界，不清楚则立刻提问。
  - 对照 `catalog.json` 选定本轮真正要用的 `skill`、`craft` 或 `mcp` 的 ID，严禁现场发明。
  - 评估任务风险与规模，定下档位（`tier`：Discuss / T0 / T1 / T2 / T3）与写级别（`write_class`：read / sandbox / promote / destroy）。
  - 将上述决策写入 `loadplan.json`。
- **解决的问题**：
  - 解决模型“拿到诉求直接动手写代码”的坏习惯。
  - 强制在动手前进行范围对齐，防止做无用功或超范围改动。

### 2. 名单生成器：`生成会话能力名单.py`
- **处理的事情**：
  - 读取 `loadplan.json`，验证所有 ID 均在菜单中。
  - **职种不预展开**：如果点名了某个职种（`craft`），读取其 `uses_skills` 序列，但**只把第一个技能**写入 `craft_open`，其余技能在后续步骤中按步打开。
  - 自动将已点名技能的 `needs_mcp` 依赖并入 `mcp_allow`，提示开场握手。
  - 写入 `activated.json` 并调用 `项目库.py` 生成 `current.md`。
- **解决的问题**：
  - 避免一次性加载职种路径上的全部技能，导致模型在第一步就用最后一步的口径说话，造成上下文污染。
  - 确保 `activated.json` 成为本轮会话的“合同切片”，名单可审计。

### 3. 现行卡：`current.md`
- **处理的事情**：由生成器在会话目录中写出。包含：会话 ID、工作项 ID、目标、进度、写级别、正式面、隔离根、禁改红线、下一步。
- **解决的问题**：**解决大模型在长对话、Compaction（上下文压缩）或切换窗口后的“失忆”问题**。它是代理在会话中断后，下一手能无缝接上的唯一事实源。

### 4. 任务排序器：`建议执行单.py` (flow.json)
- **处理的事情**：当计划中包含多个事件时，按照“执行类在前、收口类（如 `artifacts-append`、`verify-gate`、`sync-state`）在后”的推荐序，排出执行单 `flow.json`。
- **解决的问题**：防止代理在核心制作还没做完时，先去跑验证或写交接文档，导致执行顺序混乱。

---

## 第三层：能力库 (L3 Capability Library)

能力库是 GSH 的**工具箱**。它包含 106 份技能、35 条职种和 36 条外接。能力库是静态的、可复用的，它不包含任何当次数字或临时路径。

### 1. 菜单同步器：`刷新菜单.py` (catalog.json)
- **处理的事情**：扫描 `skills/` 和 `agents/` 下所有 Markdown 文件的 frontmatter（解析 `name`、`description`、`needs_mcp`、`uses_skills`），结合 `mcp-tools/` 下的用途桩，在安装后的家目录中生成统一的 `catalog.json`。
- **解决的问题**：确保所有技能和职种都有唯一的、可索引的 ID。模型在定档时只能从这个菜单里选，杜绝了“现场发明技能”的幻觉。

### 2. 外接分档与懒加载：`mcp-tiers.json` / `lazy_stdio.py`
- **处理的事情**：
  - 将 36 条外接划分为：核心直连（当前仅 `excelMCP`）和懒接（其余 35 条）。
  - 对懒接外接，使用 `lazy_stdio.py` 进行包装。在 IDE 启动时，只向模型暴露工具声明，不拉起真实进程。只有当模型第一次真正调用该工具时，才在后台拉起宿主软件。
- **解决的问题**：**彻底解决 IDE 启动时，因为要连接几十个 MCP 服务器而导致的“30秒卡死/超时”问题**。确保开场握手极速完成，且不占用本机内存。

### 3. 技能 (Skills) 与 职种 (Crafts)
- **技能（Markdown）**：专注于解决某一类特定制作问题（如 `damage-formula-pass` 专注于伤害公式通道与运算顺序；`excel-com-write` 专注于表格差量合并）。
- **职种（Markdown）**：定义了一条岗位的标准作业路径（如 `combat-numeric-designer` 串起战斗建模、公式设计、克制矩阵、技能数值、成长曲线、表晋升）。
- **解决的问题**：
  - **职责分离**：技能不当导演，导演不写代码。
  - **多岗位协作**：当一项任务涉及多个岗位时（如既要改数值表，又要写客户端表现），主会话通过定档点名，**优先开出对应的子代理（Subagent）**，每只子代理只读一个职种正文，主会话收口。避免单只代理串岗导致逻辑混乱。

---

## 第四层：档案柜 (L4 Filing Cabinet)

档案柜是 GSH 的**记忆与事实落地层**。它承认大模型不具备长期的、可靠的逻辑推理记忆，因此将所有状态和事实**显式地实体化为文件**。

```text
 L4 档案柜
   ├── state.json ───────> 正在哪次会话，当前进度
   ├── tasks.jsonl ──────> 只追加的任务流水账
   ├── surfaces.json ────> 正式面 ↔ 隔离根的绝对对照地图
   └── canon/ & adr/ ────> 必须被 retrieve_keys 命中才打开的已批准事实
```

### 1. 写隔离机制：`surfaces.json` / `write-isolation`
- **处理的事情**：
  - 读取正式面地图 `surfaces.json`，明确每个业务大类的 `official`（官方根）与 `sandbox`（隔离根）。
  - 默认写级别为 `sandbox`：改表必须落到同级 `沙箱/` 目录并记录 `changeset`；改代码必须落到 `.harness/worktrees/`；改资产必须落到 `_Dev/`。
  - 只有在结案通过、人准晋升（`promote`）时，才运行 `xlsx_merge_changeset` 或 git 合并，**只回写记录集，严禁整文件覆盖正式面**。
- **解决的问题**：
  - **防止正式面被试错毁掉**：代理在隔离根里随意试错、运行测试，即使崩溃也不会污染策划案、主代码仓或引擎资源。
  - **防止沙箱文件入库**：强制要求每个仓的 `.gitignore` 必须包含 `**/沙箱/`，防止临时副本和 changeset 被意外提交。

### 2. 状态与流水账：`state.json` / `tasks.jsonl`
- **处理的事情**：
  - `state.json` 记录当前激活的会话、进度摘要，并保留历史会话的快照。
  - `tasks.jsonl` 是一个**只追加（Append-Only）**的流水账，记录每次会话的激活、改动与关闭事件，带上精确的时间戳。
- **解决的问题**：解决“换个窗口、重开 IDE 就不知道做到哪”的问题。确保所有代理的行为都有迹可循，形成不可篡改的审计日志。

### 3. 已批准事实与决策：`canon/` / `adr/`
- **处理的事情**：
  - `canon/` 存储团队已批准的稳定事实（如 `四层运行口径.md`、`战斗公式表达式规范.md`）。
  - `adr/` 存储架构与技术选型决策。
  - **按键寻址**：只有在定档时，计划中写了 `retrieve_keys` 命中的键，这些事实才会被打开读入窗口。
- **解决的问题**：
  - **防止幻觉污染**：防止代理把口头讨论的想法、临时草稿当成“已批准事实”去指导下游制作。
  - **控制窗口压力**：拒绝在开场时扫描全库。没有键，事实库就保持关闭。

### 4. 验证门：`verify-gate` (verify-report.json)
- **处理的事情**：
  - 根据定档的 `tier` 级别，清点本档位必须核对的**核心证据路径**（Discuss 档不写报告；T0 档核主产物非空；T1 档核主产物+关键约束；T2/T3 档核跨职种接口与构建输出）。
  - 逐个打开证据路径，确认无误后，写出 `verify-report.json`，判定 `verdict` 为 `pass`。
  - 将报告路径追加登记到 `artifacts/index.jsonl` 索引中。
- **解决的问题**：将“测试通过了”从代理的口头保证，变成**可回溯、可机检的文件证据链**。L1 结束钩子只认这份报告。

---

## 行为准则

- **密钥不进仓库**：所有 MCP 配置、环境模板只能使用占位符（如 `${LARK_APP_ID}`）。密钥必须留在本地密钥管理处，严禁提交。
- **写隔离是默认牙齿**：任何正式面的修改必须先落到隔离根。未获人准、未产出验证报告前，严禁直连正式面。
- **四层已封版**：四层架构是 GSH 的底层宪法。严禁在任务执行过程中，通过偷偷新建顶层文件或加层来“顺便”解决问题。修改架构必须先转向、改计划、写决策（ADR）。
- **事实必须晋升**：口头讨论、临时草稿、未关项的产物一律不得作为“已批准事实”引用。只有通过 `promote-canon` 写入 `canon/` 目录的，才是稳定事实。

---

## English

A four-layer context operating system for game-production agents. It orchestrates skills, crafts, MCPs, and write isolation for Cursor, Claude Code, Codex, Grok, and DeepSeek.

### Core Architecture

```text
 L1 Constitution  ──(Enforces read order, blocks secrets, gates closure)──> Thin & Always-on
        │
        ▼
 L2 Director      ──(Clarifies boundaries, maps IDs, writes loadplan)─────> Scopes the round
        │
        ▼
 L3 Capability    ──(106 stateless skills, 35 crafts, 36 lazy MCPs)──────> Stateless toolbox
        │
        ▼
 L4 Filing Cabinet ──(surfaces.json, state.json, tasks.jsonl, canon)─────> Immutable ledger
```

- **L1 Constitution**: Thin & always-on. Enforces boot read order, blocks secrets, intercepts destructive commands, and gates session closure on verified reports.
- **L2 Director**: Scopes the round. Maps user queries to explicit skill/craft/mcp IDs from the catalog. Writes `loadplan.json` and `current.md`. Crafts are loaded sequentially (only `craft_open` first step is active) to prevent context pollution.
- **L3 Capability Library**: Stateless toolbox. 106 skills and 35 crafts. Non-core MCPs are wrapped in `lazy_stdio.py` to prevent 30-second startup hangs.
- **L4 Filing Cabinet**: Immutable ledger. Maps official surfaces to sandbox roots via `surfaces.json`. Writes are isolated to sandboxes/worktrees and promoted only upon human approval by merging changesets. Tracks history in `state.json` and `tasks.jsonl`.

---

## 许可

MIT.
