# Game Studio Harness (GSH)

**游戏工作室的上下文操作系统。** 35 条职种路径、106 份技能做法、36 条外接与写隔离，一次性部署到 Cursor、Claude Code、Codex、Grok、DeepSeek。本仓不附带引擎或 DCC，附带的是制作会话的编排：这一轮读什么、写到哪、何时关项、如何把试错变成可晋升的记录集。

[English](README.en.md) · [文档索引](docs/README.md) · [库存盘点](#库存盘点) · [部门能力地图](#部门能力地图) · [安装与部署](#安装与部署)

| 职种 Crafts | 技能 Skills | 外接 MCP | 适配工具链 |
| :---: | :---: | :---: | :---: |
| 35 | 106 | 36 | Cursor · Claude Code · Codex · Grok · DeepSeek |

---

## 仓库目的

Game Studio Harness（GSH）是给游戏工作室用的**上下文操作系统**。它把大模型在制作里真正缺的东西做成四层可审计机制：始终生效的运转规则、本轮加载合同、可复用的职种/技能库、以及跨会话不断线的档案柜。GSH 不是提示词合集，也不是美术/引擎插件。它回答的是制作人每天都要面对的问题：**这一轮代理该扮演哪条岗、打开哪几份做法、允许写到哪一层表面、用什么证据才能关项。**

### 谁在用

| 角色 | 在 GSH 里做什么 |
| :--- | :--- |
| 制作人 / 执行制作人 / 项目管理 | 定里程碑与交付包、点名职种、对齐依赖与风险、推动验收与发版口径 |
| 创意总监 | 冻结体验支柱、批注垂直切片、裁决 fantasy 冲突、批准 Canon |
| 主策（系统 / 战斗 / 数值 / 商业化 / 活服） | 把规则、公式、表、活动与付费点写成可引用规格，再按配方改表 |
| 主程（客户端 / 服务端 / 工具） | 按契约做竖切、权威结算、存档迁移、管线工具与 CI 冒烟 |
| 主美 / 技术美术 | 从风格锚与 Brief 走到可导入资产，过命名/LOD/Shader/VFX 预算门禁 |
| QA 负责人与各专项 | 定验收口径、写用例与回归包、跑兼容/性能/自动化，签发带证据的结论 |

同一诉求里岗位不同时，主会话只负责点名与收口，优先按职种各开子代理。专注度的边界是岗位，不是「请同时当数值策划和客户端」。

### 「跑一条垂直切片」指什么

垂直切片不是把整条流水线灌进一轮对话。它是一次**有边界的制作会话**：锁定一个可在 3～5 分钟内试玩裁决的问题（例如「这套技能循环在灰盒里是否可读、是否可结算」），然后：

1. **定档** — `route-task` 对照 `catalog.json` 点名本轮 `craft` / `skill` / `mcp`，写入 `.harness/sessions/<会话>/loadplan.json`（档位、写级别、禁改、`retrieve_keys`）。
2. **激活** — `生成会话能力名单.py` 写出 `activated.json` 与现行卡 `current.md`。点了职种只注入职种正文和路径第一步（`craft_open`），其余技能做到那一步再打开。
3. **制作** — 按职种步骤打开技能文件；正式面改动先落到隔离根（表沙箱、代码 worktree、引擎 Sandbox、资产 `_Dev`）。
4. **关项** — `verify-gate` 按档位只核核心证据，写出 `verify-report.json`；人准后只回写记录集，禁止整文件覆盖正式面。

成功的切片长这样：名单可审计、试错进沙箱、验证报告 `verdict=pass`、晋升有人准与可回滚 diff。会话会断、工具会换；下一手读现行卡而不是聊天记录。

### 四层如何配合

上下文预算是硬约束。宪法必须每轮都在，所以必须薄；做法必须可复用，所以必须厚。这两件事不能写在同一层。加载计划也不能并进能力库：库回答「这件事怎么做」，导演回答「这一轮点谁」。档案柜承认自己不会推理，只记做到哪、正式面在哪、哪句已经批准。

| 层 | 英文 | 本轮职责 | 关键文件 |
| :--- | :--- | :--- | :--- |
| 宪法 | Constitution | 每轮固定税：读序、写隔离、密钥拦截、关项只认验证报告 | `constitution.md`、`rules/全局.mdc`、`hooks.json` |
| 加载计划 | Load-plan | 把诉求收成可审计的点名集合、档位与写级别 | `loadplan.json` → `activated.json` → `current.md` |
| 能力库 | Capability library | 35 职种路径 + 106 技能正文 + 36 外接用途桩；不含当次数字 | `agents/<id>.md`、`skills/<id>/SKILL.md`、`catalog.json` |
| 档案柜 | Filing cabinet | 会话状态、正式面地图、已批准事实、产物索引 | `.harness/state.json`、`surfaces.json`、`canon/`、`adr/`、`artifacts/` |

四层已封版。改架构须转向、改计划并写决策（`promote-adr`）。口头讨论、未关项草稿不得冒充 Canon。

### 成功长什么样

- **激活集合**：`activated.json` 只含本轮点名的 skill / craft / mcp；职种未预展开全路径；`craft_open` 指向当前步。
- **沙箱写入**：改表进正式表同级 `沙箱/`，改代码进 `.harness/worktrees/`，改资产进 `_Dev/`；`**/沙箱/` 进入 `.gitignore`。
- **验证报告**：`.harness/artifacts/<工作项>/verify-report.json` 的 `verdict` 为 `pass`，路径已登记到 `artifacts/index.jsonl`。
- **晋升**：人准后只合并 changeset / 记录集；禁改列未动；回读抽样通过。结束钩子不认口头绿。

---

## 库存盘点

权威来源是安装后由 `刷新菜单.py` 扫描 `agents/` 与 `skills/` frontmatter 生成的 `catalog.json`。本仓五套工具目录各自齐套；下列清单与 `cursor/agents/`（35）和 `cursor/skills/`（106）一致。

### 职种 35

| 部门 | 职种 id |
| :--- | :--- |
| 制作与项目管理 | `producer` · `associate-producer` · `project-manager` · `creative-director` |
| 系统设计与数值策划 | `systems-designer` · `combat-designer` · `combat-numeric-designer` · `economy-numeric-designer` · `progression-numeric-designer` · `monetization-designer` · `liveops-designer` |
| 关卡、叙事、文案与交互 | `level-designer` · `narrative-designer` · `copywriter-designer` · `ux-designer` |
| 客户端与服务端工程 | `client-engineer` · `client-combat-engineer` · `client-ui-engineer` · `server-engineer` · `server-combat-engineer` · `tools-engineer` |
| 美术与技术美术 | `character-concept-artist` · `character-artist` · `environment-concept-artist` · `environment-artist` · `ui-artist` · `vfx-artist` · `animator` · `rigger` · `tech-artist` |
| 品质保障 QA | `qa-lead` · `qa-functional` · `qa-automation` · `qa-compatibility` · `qa-performance` |

### 技能 106

职种 `uses_skills` 覆盖 85 个事件技能。其余 21 个不挂在任何职种路径上，放在 [横切能力](#7-横切能力--运行时与档案)：`assemble-craft-flow`、`attr-family-sync`、`audio-fmod-checklist`、`build-acceptance`、`build-gate-checklist`、`collab-protocol`、`data-readiness-check`、`deliverable-sheets`、`diagram-pack`、`doctor`、`excel-format`、`excel-read`、`fmod-bank-build`、`mcp-autostart`、`memory-retrieve`、`naming-consistency-check`、`personal-server-table-sync`、`promote-adr`、`terrain-gaea-pass`、`verify-gate`、`write-isolation`。

完整 id 见下方各部门技能表；能力地图保证 **35/35 职种、106/106 技能各至少出现一次**。

### 外接 36

`accurig` · `audacity` · `blender-mcp` · `cascadeur` · `chrome-devtools` · `cloudcompare` · `docker-mcp` · `everything-search` · `excalidraw` · `excelMCP` · `ffmpeg` · `fmod-cli` · `fmod-studio` · `gaea` · `gamedev-mcp` · `gimp` · `imagemagick` · `inkscape` · `instant-meshes` · `krita-mcp` · `lark-mcp` · `ldtk` · `magicavoxel` · `materialize` · `materialpilot` · `meshlab` · `meshroom` · `miro` · `pureref` · `renderdoc` · `rokoko` · `roslyn-mcp` · `tiled` · `treeit` · `xmind` · `xnormal`

核心档默认直连 `excelMCP`；其余懒接，第一次调用再拉子进程。见 [外接 MCP](#外接-mcp)。

---

## 部门能力地图

能力地图按工作室部门分块。每个模块包含：（1）该部门在制作管线中的位置；（2）全部职种路径——每一步意图与打开的技能；（3）相关技能的做法、时机与输入输出；（4）一条典型竖切如何用 `menu` / `activate` / `next` / `close` 穿过这些文件。

会话命令与脚本对应关系：

| 命令 | 脚本 / 技能 | 写出 |
| :--- | :--- | :--- |
| `menu` | `~/.cursor/harness/scripts/刷新菜单.py` | `catalog.json` |
| `activate` | `route-task` → `生成会话能力名单.py <会话>` | `loadplan.json`、`activated.json`、`current.md` |
| `next` | 打开 `craft_open` 指向的技能；多事件时 `assemble-craft-flow` → `建议执行单.py` | 下一步技能正文、`flow.json` |
| `close` | `verify-gate`（必要时 `artifacts-append` / `sync-state` / `handoff-pack`） | `verify-report.json`、产物索引、状态回写 |

---

### 1. 制作与项目管理

制作部门把方向、容量、依赖和验收收成可跟踪的合同。制作人定目标与发版口径；执行制作人拆包催收；项目管理维护风险与依赖图；创意总监冻结支柱并裁决体验冲突。没有这一层，下游职种会在未批准的范围内改正式面。

#### 职种路径

**`producer`（制作人）** — 里程碑目标、构建验收推动、发版说明与跨职种制作推动。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 定档与成功标准 | 复述目标/约束/可观察成功标准，指定主责职种与档位 | `route-task` |
| 2. 里程碑计划 | 进出标准、交付物、关键路径、缓冲与砍范围触发 | `milestone-plan` |
| 3. 构建验收推动 | 证据槽、豁免路径、倒排催收；不微观代做交付包 | （验收清单；可协作 `build-acceptance`） |
| 4. 阻塞升级与范围纠偏 | 阻塞写 Owner 与时限；范围膨胀交 CD 出 `scope-cut-decision` | — |
| 5. 发版说明与复盘 | 玩家可见 vs 内部，与验收证据一致后回写状态 | `release-notes-stub` → `sync-state` / `handoff-pack` |

常挂：`route-task` · `milestone-plan` · `release-notes-stub` · `sync-state` · `handoff-pack` · `file-pack-layout`。

**`associate-producer`（执行制作人）** — 拆交付包、跨组协调、阻塞闭环、验收前齐套催收。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 接里程碑拆包 | 拆成稳定 id、Owner、日期、验收点 | `milestone-plan` |
| 2. 对依赖 | 与 PM 对齐关键路径与缓冲，环依赖升裁 | `dependency-map` |
| 3. 日周跟进 | 事实进度与红灯计数，会议只决下次动作 | `status-digest` |
| 4. 闭环阻塞 | 关闭条件可观察；方向问题升制作人/CD | — |
| 5. 齐套催收与回写 | 催证据不催空口；不擅自改里程碑目标 | `sync-state`；布局用 `file-pack-layout` |

**`project-manager`（项目管理）** — 风险台账、依赖图、定期状态摘要与纠偏选项。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 建/更风险台账 | 概率×影响、观测信号、缓解、复查日 | `risk-register-update` |
| 2. 依赖图 | 职种/交付物边表、环检测、关键路径 | `dependency-map` |
| 3. 状态摘要 | 红灯/需决策/关键路径健康三行计数器 | `status-digest` |
| 4. 纠偏建议 | 2～4 选项（缓冲/砍包/加人）；批准后才改计划 | `sync-state` |
| 5. 闭环归档 | 关闭风险写结果；路径不变、版本递增 | — |

**`creative-director`（创意总监）** — 体验支柱、切片批注、fantasy 冲突裁决、scope-cut 原则。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 收冲突与底线 | 玩法/美术/商业主张附证据，分类互斥/抢资源/语气漂移 | — |
| 2. 定支柱 | 3～5 条可检验支柱与像/不像反例 | `pillar-define` |
| 3. 体验批注 | 对垂直切片打保/砍/改，指向具体物件 | `experience-critique` |
| 4. 砍范围 | 保/砍/延后表，利弊、回滚、影响职种 | `scope-cut-decision` |
| 5. 沉淀 Canon | 已批准支柱/裁决写入决策库 | `promote-canon` |

#### 相关技能

| 技能 | 做什么 | 何时用 | 输入 → 输出 |
| :--- | :--- | :--- | :--- |
| `route-task` | 对照菜单点名 skill/craft/mcp，写加载计划与现行卡 | 新会话、转向、插队、并行、点名 | 用户诉求 → `loadplan.json` + 触发 `activate` |
| `milestone-plan` | 用容量、依赖与日历排里程碑：成功证据、关键路径、缓冲、中段预演 | 定档后排期、拆交付包 | 进出标准/容量 → 里程碑页与砍范围触发表 |
| `release-notes-stub` | 从 git log / 表 diff / 裁剪决议转写玩家说明并抽检 | 发版前、补丁公告 | 变更源 → 分类更新说明 |
| `sync-state` | 对齐工作项、会话卡、计划与产物索引 | 日周跟进、关项前、换手 | 分散状态 → 单一事实源与 `state.json` |
| `handoff-pack` | 打包目标、已做决策、产物路径、未决项、建议下一手 | 换职种或换会话 | 现行卡 + 产物 → 交接包 |
| `file-pack-layout` | 规划工作区/资源分包，隔离第三方与草稿 | 目录混乱、找不到文件、开仓布局 | 现状树 → 搬家清单与对照表 |
| `dependency-map` | 边表映射依赖，跑环检测，输出并行组与裁剪扇出 | 跨组互等、关键路径不清 | 交付包/系统节点 → 依赖图版本 |
| `status-digest` | 汇总事实进度、阻塞与需决策项 | 周报、日会、红灯计数 | 交付包表 → 可引用状态摘要 |
| `risk-register-update` | 识别/重估风险，写信号、缓解与复查日 | 风险台账过期、新外部依赖 | 台账表 → 按级排序的风险行 |
| `pillar-define` | 定 3～5 条可检验体验支柱与反例 | 项目启动、方向冲突、支柱空话 | 主张与参考 → 可引用支柱文档 |
| `experience-critique` | 按支柱对切片打可执行批注 | 垂直切片试玩、fantasy 冲突 | 切片构建 + 支柱 → 保/砍/改表 |
| `scope-cut-decision` | 在支柱约束下出保/砍/延后 | 里程碑超载、范围膨胀 | 容量与支柱 → 决策表与回滚条件 |
| `promote-canon` | 把已批准稳定事实写入决策库 | 支柱/规则冻结后 | 批准记录 → `canon/` 条目 |

#### 典型竖切

里程碑「可玩战斗灰盒」开项：`menu` 刷新 `catalog.json`。制作人 `activate` 点名 `producer` + `creative-director`（岗位不同则开子代理），`route-task` 写入 T2/`sandbox`。`next` 先走 `pillar-define`，再 `milestone-plan` 拆包给执行制作人；PM 子代理跑 `risk-register-update` 与 `dependency-map`。齐套日 `status-digest` + `sync-state`。`close` 核里程碑页、支柱文档与齐套核对表，写 `verify-report.json`；发版周再激活 `release-notes-stub`。

---

### 2. 系统设计与数值策划

本部门把玩法收成可设计顺序的系统索引、可实装的 GDD 切片、可结算的战斗对象，以及可晋升的数值表。系统策划锁规则与接口；战斗策划锁流程与技能组；三路数值分别主笔战斗公式、经济循环与养成曲线；商业化与活服把付费点、活动日历接到同一套实体与开关上。改表一律走读取 → 沙箱写入 → 格式 → diff → 人准晋升。

#### 职种路径

**`systems-designer`（系统策划）** — 系统索引、功能 GDD 切片、规则可行性预检、Canon 提案。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 更新系统索引 | 显式/隐式系统分层，队首指针，环依赖处理 | `systems-index-map` |
| 2. 切功能 GDD | 八节骨架逐节 Context/Options/Draft，状态机作唯一源 | `feature-gdd-slice` |
| 3. 规则可行性预检 | 对照引擎/联机/工具链，给可行或降级 | `rule-feasibility-check` |
| 4. 对齐下游 | 事件名、错误码、存档键与 UI 入口一致 | — |
| 5. Canon 与修订 | 已批准规则入库，冲突先并列 | `promote-canon` |

**`combat-designer`（战斗策划）** — 战斗流程、技能组、手感验收清单。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 定战斗流程 | 步骤 id、时间模型、资源轴、胜负条件 | `combat-flow-design` |
| 2. 设计技能组 | 定位、槽位职责、资源与冷却；冻 `slots_version` | `skill-kit-design` |
| 3. 写手感清单 | Hit/Cancel/受击/镜头/震动可勾项并冻版本 | `combat-feel-checklist` |
| 4. 落 GDD 与制作对齐 | 事件帧期望交数值/动画/特效/程序 | `feature-gdd-slice`（协作 `anim-event-hook`、`vfx-skill-hook`） |
| 5. 试玩批注 | 对照清单实机勾；改流程不改数值主表 | — |

**`combat-numeric-designer`（战斗数值策划）** — 属性、公式、克制、技能数值；改表走写入配方。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 建模目标与冻结锚点 | TTK/职业带宽、边角用例、与 kit 禁改分栏 | `combat-modeling` |
| 2. 定属性框架 | 主键、派生 DAG、快照与上下限 | `attribute-framework`（加属性族挂 `attr-family-sync`） |
| 3. 公式、克制、技能表 | 运算顺序、矩阵、系数档位 | `damage-formula-pass` → `counter-matrix-pass` → `skill-numeric-pass` |
| 4. 验边角 | 0 防、暴击上限、溢出治疗等 | — |
| 5. 写表 diff 与交接 | 沙箱写入、风险分级、回读抽样 | `excel-com-write` → `tunable-table-diff` |

重型模拟前先跑 `data-readiness-check`。

**`economy-numeric-designer`（经济数值策划）** — 产销循环、物价、通胀、表晋升。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 分析循环 | 玩→获得→花→再玩，标断裂与滞留 | `economy-loop-analysis` |
| 2. 产销地图 | 实体 Source/Sink、净流量、上限字段 | `sink-source-map` |
| 3. 物价曲线 | 锚、档位价带、永不值/唯一解 | `price-curve-pass`（沙箱挂 `excel-com-write`） |
| 4. 通胀压力 | 多情景投影购买力，设计熔断 | `inflation-stress` |
| 5. 表 diff 晋升 | 结构化 diff、禁改列、回读 | `tunable-table-diff` / `excel-com-write` |

**`progression-numeric-designer`（养成数值策划）** — 成长曲线、解锁节奏、产销接口、属性挂接。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 定曲线目标 | 时长/战力/章节锚，累计差分验算 | `progression-curve` |
| 2. 解锁节奏标定 | 系统/关卡/养成线条件与失败提示键 | — |
| 3. 投入产出与产销接口 | 养成线消耗/产出对齐实体 | `sink-source-map` |
| 4. 属性挂接 | 成长输出主键与战斗表一致 | `attribute-framework` |
| 5. 落表抽样 | 写入配方、风险分级、N 日战力抽样 | `excel-com-write` / `tunable-table-diff` |

**`monetization-designer`（商业化策划）** — 付费点、IAP/礼包/通行证目录、商业化 KPI 口径。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 定 KPI 与底线 | 冻结口径、观测窗口、不伤支柱的禁区 | `monetization-kpi-pass` |
| 2. 设计付费点 | 看见→理解→支付→兑现；P2W 风险升级 | — |
| 3. IAP 目录 | SKU、价格档、内容物、限购、商店 ID | `iap-catalog-check` |
| 4. 协同活动规格 | 与活服日历错峰，预审发奖邮件 | 协作 `liveops-calendar` / `reward-mail-check` |
| 5. 验收与修订 | 对照 KPI 检查误导购买与难兑现 | — |

**`liveops-designer`（活服策划）** — 活动日历、活动规格、奖励邮件安全检查。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 排日历 | 日/周/季节奏、撞车消解、维护窗 | `liveops-calendar` |
| 2. 写活动规格 | 目标/玩法/奖励/开关/埋点/失败补发 | `event-spec` |
| 3. 奖励邮件审计 | 模板、附件校验、补发、过期、去重 | `reward-mail-check` |
| 4. 对齐实现 | 服侧发放权威与幂等、客户端红点/过期 | — |
| 5. 上线前闭合 | 配置 diff、回滚执行人、埋点齐全 | — |

#### 相关技能

| 技能 | 做什么 | 何时用 | 输入 → 输出 |
| :--- | :--- | :--- | :--- |
| `systems-index-map` | 枚举显式/隐式系统，分层依赖，产出可设计顺序的索引 | 队首该设计谁、隐式系统漏列 | 概念清单 → `systems_index` 表（含 `next_design`） |
| `feature-gdd-slice` | 按八节共写单功能 GDD，冲突扫描与验收证据 | 写规则、补空洞节、retrofit | 范围卡 → 可开做切片 |
| `rule-feasibility-check` | 规则拆能力点，对照引擎/联机/工具链 | 「能不能做」、联机权威灰区 | GDD 规则 → 可行/条件/不可行 + 降级 |
| `combat-flow-design` | 定可入库战斗流程骨架与判定公式语法 | 战斗步骤名标准化、接代码 | 支柱与节奏意图 → flow brief + 稳定 id |
| `skill-kit-design` | 定定位、槽位、资源与冷却结构 | 新职业/技能组、槽职责重叠 | 幻想定位 → 可填系数的技能包骨架 |
| `combat-feel-checklist` | 用帧预览、缓冲窗、Hitstop、镜头震动检查手感 | 手感验收、打击感争议 | 清单版本 → 短片证据与勾选表 |
| `anim-event-hook` | 建事件字典，在关键帧植入 Notify 并对齐逻辑/特效 | Hit 帧、攻击判定帧、AnimNotify | Clip + 事件名 → 字典版本与帧表 |
| `vfx-skill-hook` | 按 Timeline/Notify/Socket 挂技能特效并处理打断清理 | 技能 VFX 对帧 | 事件名 + Socket → 特效映射表 |
| `combat-modeling` | 建对象生命周期、状态机、事件载荷，冻结算顺序 | 战斗实体建模、端权威对齐 | 锚点 → 模型表与管线顺序 |
| `attribute-framework` | 定义属性主键、派生、快照与上下限 | 属性表、一二级属性 | 主键集 → 供公式与成长引用的框架 |
| `damage-formula-pass` | 选定伤害/治疗通道，冻运算顺序与钳制 | 伤害公式、结算式 | 通道与顺序 → 可解析表达式 + 验算槽 |
| `counter-matrix-pass` | 定义克制轴、填矩阵、检查循环并映射修饰 | 属性相克 | 轴定义 → 矩阵与公式插入点 |
| `skill-numeric-pass` | 按技能包填系数，档位对照与异常扫描 | 技能系数、CD/资源 | kit 骨架 → 系数表抽样 |
| `economy-loop-analysis` | 把产销循环拆成节点与有向边 | 循环断裂、新货币 | 玩法循环 → 改哪些表字段的结论 |
| `sink-source-map` | 枚举货币/材料 Source/Sink，算净流量 | 产销地图、水龙头水槽 | 实体清单 → 净流量与上限对齐 |
| `price-curve-pass` | 选锚、建价带、扫永不值/唯一解 | 商店定价、Teq | 实体地图 → 调价字段映射 |
| `inflation-stress` | 多情景投影库存/购买力，设计熔断 | 大活动前、购买力投诉 | 情景参数 → 可复述结论与熔断键 |
| `progression-curve` | 定成长锚与曲线形状，落累计/差分验算槽 | 成长曲线、肝度投诉 | 锚点 → 曲线版本与消耗表 |
| `tunable-table-diff` | 对比沙盒与正式数值表，分级风险并晋升或回滚 | 表 diff、数值晋升 | 沙箱簿 + 正式簿 → 可回滚 diff |
| `excel-com-write` | 确认范围→沙盒改值/公式/插删行→排版→diff 只合记录格→晋升→回读 | 改产品表 | 正式表路径 → `沙箱/*.xlsx` + changeset |
| `monetization-kpi-pass` | 冻结商业化 KPI 口径、观测窗口与禁区 | ARPU/转化率口径未冻 | 制作方口径 → 可观察验收指标 |
| `iap-catalog-check` | 核对 IAP/礼包/通行证 SKU 与商店 ID | 上架目录、限购刷新 | 目录表 → SKU 对照与价值解释 |
| `liveops-calendar` | 排日/周/季节奏并消解撞车 | 档期、赛季、运营节奏 | 里程碑与产能 → 日历与备档 |
| `event-spec` | 写活动目标/玩法/奖励/开关/埋点与失败补发 | 限时活动案 | 玩法意图 → 可实装规格 |
| `reward-mail-check` | 检查发奖邮件模板、附件、补发与过期，防重复领取 | 奖励邮件、补发 | 奖励清单 → 审计通过或停发 |

#### 典型竖切

「新职业技能组可结算」：`menu` 后 `activate` 点名 `combat-designer` 与 `combat-numeric-designer`（两只子代理），T2/`sandbox`，`retrieve_keys` 指向公式 Canon。战斗策划 `next`：`combat-flow-design` → `skill-kit-design` → `combat-feel-checklist`。数值策划 `next`：`combat-modeling` → `attribute-framework` → `damage-formula-pass` → `skill-numeric-pass`，写入走 `excel-com-write`。会签后 `tunable-table-diff`。`close` 核 kit `slots_version`、公式 `order_version`、沙箱 diff 与试玩短片。经济/养成改表同一配方，另开会话点 `economy-numeric-designer` 或 `progression-numeric-designer`。

---

### 3. 关卡、叙事、文案与交互

本部门把「玩家在空间与故事里经历什么」写成可检测目标、可挂门闸的节拍、可绑定的任务状态机、以及带五态的 UX 流图。关卡策划主笔目标链与遭遇；叙事策划主笔 beat 与 lore；文案策划统一术语与字数；交互策划把系统状态机翻译成可走查的信息架构。灰盒尺度与场景美术共享，文案键与 UI/错误码预留。

#### 职种路径

**`level-designer`（关卡策划）** — 关卡目标链、灰盒动线、遭遇编排、节奏峰谷。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 写关卡目标 | 主/可选/失败条件、教学点、时长预算，挂钩叙事 beat | `level-goals-spec` |
| 2. 灰盒动线 | 尺度、门控、视线；未通过不换高模 | 协作 `blockout-pass` |
| 3. 遭遇编排 | 波次/触发/重置/教学序，同屏预算 | `encounter-script` |
| 4. 节奏 Pass | 峰谷图对照战斗/解谜/叙事密度 | `pacing-pass` |
| 5. 协作替换与修订 | 给场景美术可替换块；脚本事件名给程序 | — |

**`narrative-designer`（叙事策划）** — 节拍表、任务规格、对白规格、世界观一致性。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 节拍表 | 章/beat：目标、转折、情绪、玩法挂钩与门闸 | `narrative-beat-sheet` |
| 2. 任务规格 | 状态机、目标键、奖励、失败回滚、本地化键 | `quest-spec` |
| 3. Lore 一致性 | 对照圣经扫设定冲突、命名漂移、时间线 | `lore-consistency-check` |
| 4. 对白规格协作 | 节点意图、字数、分支变量；润色可交文案 | `dialogue-pass` |
| 5. 落地修订 | 与关卡/系统对触发；抽测跳过仍知关键信息 | — |

**`copywriter-designer`（文案策划）** — 系统/引导文案、对白润色、命名一致性、字数适配。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 收语气锚 | 世界观语气、禁词、声口样本、字数上限 | — |
| 2. 过命名一致 | 一名一义；冲突给改名选项与影响面 | 有则挂 `naming-consistency-check` |
| 3. 润系统文案 | 引导/错误/空态/确认框，控字数与禁词 | `copy-pass` |
| 4. 润对白 | 按节点意图润色，可跳过策略与字幕字数 | `dialogue-pass` |
| 5. 适配与回修 | 真机截断、禁词扫描、键表交接 | — |

**`ux-designer`（交互策划）** — 信息架构、UX 流图、可用性走查。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 信息架构 | 任务列表、导航层级、与系统状态机对齐 | — |
| 2. 流图规格 | 进入/操作/反馈/离开，含五态与异常流节点 ID | `ux-flow-spec` |
| 3. 可用性评审 | 迷失/误触/反馈弱，热区与连点 | `ux-review-pass` |
| 4. 组件选用说明 | 映射 UI Kit；缺件提新增申请 | 协作 `ui-kit-spec` |
| 5. 修订交付 | 闭阻塞；流图版本与债列表 | 实现侧协作 `ui-logic-pass` |

#### 相关技能

| 技能 | 做什么 | 何时用 | 输入 → 输出 |
| :--- | :--- | :--- | :--- |
| `level-goals-spec` | 写清主/可选/失败目标、教学点与时长预算 | 关卡开案、胜负条件不可测 | 支柱 + beat → 目标链与检测器表述 |
| `encounter-script` | 编排波次/触发/重置/教学序，控制同屏与失败可读 | 遭遇脚本、脱战重置 | 目标链 + 技能组期望 → 波次表 |
| `pacing-pass` | 用峰谷图对照密度，实测时长并插入喘息 | 连续高压、一局过长 | 灰盒路径 → 节奏图与安全区 |
| `blockout-pass` | 用灰盒验证尺度/动线/门控/视线 | 白盒、graybox、尺度校验 | 目标链 → 可走通灰盒分区 |
| `narrative-beat-sheet` | 把故事节拍落成可挂门闸的 beat 表 | 叙事结构、幕与 beat | 支柱 tone → beat 表 + quest/dialogue 挂点 |
| `quest-spec` | 写任务状态机、目标键、奖励、失败与回滚 | 任务案、接取完成条件 | beat + 经济会签 → 可实装任务规格 |
| `lore-consistency-check` | 对照世界观圣经扫冲突与时间线矛盾 | Canon 冲突、设定打架 | 人名地名势力表 → 冲突卡或升级项 |
| `dialogue-pass` | 按节点意图润色对白，控字数/声口/可跳过 | 对白润色、字幕字数 | 节点规格 → 可上库对白 |
| `copy-pass` | 统一 UI/物品/系统短文案的术语、长度与语气 | 系统提示、空态、错误码文案 | 语气锚 + 字数上限 → 分场景文案文件 |
| `ux-flow-spec` | 画关键用户流，含五态与异常流节点 ID | UX 流图、信息架构 | 任务列表 + 状态机 → 稳定节点 ID 流图 |
| `ux-review-pass` | 对照流图走查迷失/误触/反馈弱 | 可用性评审、热区 | 流图 + 真机 → 阻塞/抛光分级 |

#### 典型竖切

「第一章可教战斗门闸」：`activate` 点名 `level-designer` 与 `narrative-designer`。`next`：`narrative-beat-sheet` 给出门闸 beat → `level-goals-spec` 写可测目标 → `blockout-pass` 验证尺度 → `encounter-script` + `pacing-pass`。叙事侧 `quest-spec` 接检测器，`lore-consistency-check` 扫命名。文案子代理 `copy-pass` / `dialogue-pass`。UX 子代理 `ux-flow-spec` → `ux-review-pass`。`close` 核目标链、beat 挂点、灰盒可走通记录与流图五态。

---

### 4. 客户端与服务端工程

工程部门把已冻结的接口做成可构建的竖切：客户端打通主路径与失败态，战斗客户端对齐帧与预测回滚，UI 客户端维护导航栈与红点，服务端冻契约/存档/反作弊，战斗服务端守结算权威，工具工程把导出与校验收成可 CI 的 CLI。权威数字不在客户端回调里终裁。

#### 职种路径

**`client-engineer`（客户端开发工程师）** — 非战斗功能竖切、缺陷修复、通用 UI 逻辑协作。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 对契约 | 读 API/状态机/错误码；缺字段开问题单 | — |
| 2. 竖切实现 | 主路径可构建可点，失败态可复现 | `feature-vertical-slice` |
| 3. 绑 UI 逻辑 | 简单界面状态；复杂栈交 UI 工程师 | `ui-logic-pass` |
| 4. 修缺陷 | 复现→取证→假说→最小改动→回归点 | `client-bugfix` |
| 5. 接冒烟 | 关键路径进 CI，flaky 先隔离 | `ci-smoke` |
| 6. 补日志与交付 | 关键字分层；变更面/风险/回滚 | 布局用 `file-pack-layout` |

**`client-combat-engineer`（客户端战斗开发工程师）** — 帧同步/判定表现、技能接入、预测回滚。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 读规格与权威边界 | 哪些必须等服、预测窗口、事件名字典 | 对照 `server-combat-authority-check`；对齐 `anim-event-hook` |
| 2. 接技能表现 | 放技能→见反馈→收招；失败态各一条 | `feature-vertical-slice` |
| 3. 调试帧与预测回滚 | 四轨时间线，只修表现 | `client-combat-frame-debug` |
| 4. 对判定框与多段 Hit | 调试 HUD 量化早/晚 N tick | 协作 `anim-event-hook` |
| 5. 修缺陷、冒烟与交付 | 最小复现 + 种子；冒烟进 CI | `client-bugfix` · `ci-smoke` |

**`client-ui-engineer`（客户端 UI 开发工程师）** — 界面逻辑、导航栈、红点。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 读流图与五态 | 对照 UX 流程、弹窗层级、返回期望 | — |
| 2. 建导航栈 | 压栈/弹栈/Replace，防死栈与穿透 | `ui-logic-pass` |
| 3. 绑数据与红点 | 空/错/加载必绑；聚合与清点时机 | — |
| 4. 竖切屏幕与缺陷冒烟 | 三档分辨率、弱网一条 | `feature-vertical-slice` / `client-bugfix` / `ci-smoke` |
| 5. 完成核对与交接 | 绑定字段表、视觉债标给 UI 美术 | — |

**`server-engineer`（服务端开发工程师）** — 契约 → 实现校验 → 存档迁移 → 反作弊挂点 → 冒烟。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 定契约 | 字段/错误码/幂等/版本；测试骨架先于实现膨胀 | `server-api-contract` |
| 2. 实现与校验 | 入口权威在服；奖励/扣费成对；幂等不双花 | — |
| 3. 存档 Schema 与迁移 | 版本、迁移、坏档隔离；先在副本跑 | `save-schema-pass` |
| 4. 反作弊挂点 | 非战斗写入口的校验/速率/取证 | `anti-cheat-hook-check` |
| 5. 冒烟与交付 | 契约/集成冒烟 | `ci-smoke` |

**`server-combat-engineer`（服务端战斗开发工程师）** — 战斗权威、结算校验、反作弊协作。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 定权威边界并会签 | 伤害/胜负/掉落/CD 必须服裁 | `server-combat-authority-check` |
| 2. 结算实现与复算 | 按公式顺序复算；种子可复现 | — |
| 3. 契约、日志与回放 | 非法包驳回，回放偏差分类 | `server-api-contract` |
| 4. 反作弊协作 | 关键写路径校验与误杀评估 | `anti-cheat-hook-check` |
| 5. 冒烟、压测与交付 | 结算单测 + CI | `ci-smoke` |

**`tools-engineer`（工具开发工程师）** — 管线工具规格、导出修复、CI 工具入口。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 写工具规格 | 职责、IO、退出码、干跑、回滚、权限 | `pipeline-tool-spec` |
| 2. 实现核心路径 | Happy path 可本地跑；错误指向修复动作 | — |
| 3. 导出修复夹具 | 好坏金样、幂等、失败可读 | `export-pipeline-fix` |
| 4. CI 入口 | 工具冒烟进 CI，产物路径稳定 | `ci-smoke` |
| 5. 交付与培训要点 | 怎么跑/干跑/回滚；会签技美 | — |

#### 相关技能

| 技能 | 做什么 | 何时用 | 输入 → 输出 |
| :--- | :--- | :--- | :--- |
| `feature-vertical-slice` | 锁定验证问题与 3～5 分钟范围，打通主路径+失败态 | 竖切、最小可玩、切片演示 | 契约/GDD → 可试玩构建 |
| `ui-logic-pass` | 定义屏的状态机、事件、数据绑定与错误处理 | UI 逻辑、导航栈、界面绑定 | 流图节点 ID → 状态机与绑定表 |
| `client-bugfix` | 复现→取证→假说→最小改动→回归点 | 修 bug、崩溃、客户端修复 | 缺陷单 → 最小 diff + before/after |
| `ci-smoke` | 探测测试命令，跑自动冒烟子集与手工核心批 | 提测前自动检、红灯定位 | 仓库测试入口 → 冒烟结论与日志归档 |
| `client-combat-frame-debug` | 对齐动画事件/判定窗/VFX 时间线，只修表现 | 战斗帧、判定窗、预测回滚 | 四轨时间线 → HUD 偏差与帧日志 |
| `server-api-contract` | 冻端点字段/错误码/幂等与版本规则，并写契约测 | API 定稿、协议变更 | 字段表 → OpenAPI/等价物 + 契约测 |
| `save-schema-pass` | 冻存档字段与版本，写迁移、加载校验，坏档隔离 | 存档、迁移、坏档 | Schema → 迁移脚本与演练记录 |
| `anti-cheat-hook-check` | 圈关键写路径，查校验/速率/幂等，测绕过与误杀 | 反作弊挂点、篡改 | 写入口清单 → 取证日志与补点 |
| `server-combat-authority-check` | 划权威边界，查结算输入/种子，测非法包与回放偏差 | 战斗权威、技能同步 | 会签清单 → 权威 vs 预测冻结表 |
| `pipeline-tool-spec` | 定义工具职责、IO/退出码、幂等配置与 CI 钩 | 新管线 CLI、批处理 | 用户与权限 → 规格页 |
| `export-pipeline-fix` | 用好坏金样跑导出器，查依赖/命名失败可读性与幂等 | 导出校验失败、资源管线 | 金样哈希 → 修复 + 回归夹具 |

#### 典型竖切

「技能可放、可结算、可回放」：`activate` 点名 `client-combat-engineer` 与 `server-combat-engineer`。服先 `server-combat-authority-check` + `server-api-contract`；端 `next` `feature-vertical-slice` 再 `client-combat-frame-debug`。工具侧若导出阻断，另开会话点 `tools-engineer` 走 `export-pipeline-fix`。`close` 核权威清单、契约测、竖切失败态、结算单测与 `ci-smoke` 日志。非战斗功能竖切改点 `client-engineer` + `server-engineer`（`save-schema-pass`）。

---

### 5. 美术与技术美术

美术部门从可检验的风格锚走到可引用的引擎路径。原画交可制作 Brief；角色/场景生产过清单与命名门禁；UI 维护 Kit 合同与四态屏；绑定与动画把骨架、权重、事件帧交给战斗与特效；技美把导入、LOD、Shader、VFX 预算收成可抽检的规范。概念未批不开生产模；灰盒未过不换高模。

#### 职种路径

**`character-concept-artist`（角色原画师）** — 角色视觉设定与可制作 Brief。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 锁风格锚 | 色/光/剪影语言与远距可辨特征 | `style-anchor` |
| 2. 出概念多方案 | 2～4 个剪影差异方案，未选不进生产设定 | — |
| 3. 生产设定 | 三视图、材质分区、挂点期望 | `concept-key-art` |
| 4. Key Art 与生产分流 | 宣发与生产稿分轨；3D 只跟生产稿 | — |
| 5. 写 Brief 与评审 | 禁改记忆点、面数档；交 `character-artist` | — |

**`character-artist`（角色美术）** — 角色资产清单与导出规范。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 接设定锁档 | 已批概念/三视图；锁面数/贴图/LOD | 对照 `style-anchor` |
| 2. 执行角色资产清单 | 建模 UV 贴图 LOD；超档立刻暴露 | `character-asset-checklist` |
| 3. 命名导出与导入 | 映射表齐全，引擎内查粉材质与尺度 | `export-naming-gate` → `import-validate` · `lod-budget-pass` |
| 4. 协作收口 | 拓扑注意交接绑定；风格抽检对照锚点 | — |

**`environment-concept-artist`（场景原画师）** — 场景/道具概念与空间气质。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 锁气质与锚点 | 场景 Brief：主题、时段、导向色 | `style-anchor` |
| 2. 氛围图与关键道具 | 进入/战斗/兑现区关键帧；模块化暗示 | — |
| 3. 可制作交接 | 色形材边界与尺度表对照 | `blockout-pass` · `env-asset-checklist`；交接职种 `environment-artist` |
| 4. 跟产抽检 | 试摆后对照氛围图查漂移 | — |

**`environment-artist`（场景美术）** — 场景资产清单与空间表现。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 接灰盒与气质 | 灰盒已通过分区才换高模 | `blockout-pass` |
| 2. 模块生产与试摆 | 尺寸枢轴、接缝碰撞、材质复用 | `env-asset-checklist` |
| 3. 空间表现与预算 | 远景板、导向色；参与 LOD/Shader 抽检 | `lod-budget-pass`（超标走 `shader-budget-note`） |
| 4. 命名入库交接 | 分区替换映射表交给关卡 | `export-naming-gate` → `import-validate` |

**`ui-artist`（UI 美术）** — UI Kit 与界面视觉 Pass。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 对齐锚点与流程 | 色板 token、本迭代屏列表、Kit 缺口 | `style-anchor` |
| 2. 维护 Kit 合同 | 变体×尺寸×状态；破坏性变更公告 | `ui-kit-spec` |
| 3. 单屏 pass | 信息层级、四态、跳转 | `ui-screen-pass` |
| 4. 跟产与回归 | 多分辨率抽检；切图命名 | `export-naming-gate` · `file-pack-layout` |
| 5. 完成核对与交接 | token 与合同版本 | — |

**`vfx-artist`（特效）** — 特效预算与技能挂点对齐。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 接技能与挂点 | 只要事件名与 Socket，不要逻辑全文 | — |
| 2. 制作与挂点对齐 | 按帧触发；打断清理 | `vfx-skill-hook` |
| 3. 预算测量与降级 | Overdraw/粒子上限；降级仍可读 | `vfx-budget-pass` |
| 4. 交付与回归 | 映射表交战斗装配；改动画事件必回归 | `import-validate` |

**`animator`（动画）** — 动画集完整度与事件挂点。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 接需求并锁范围 | 最小可玩四类 vs 完整集；只挂事件名清单 | — |
| 2. 跑动画集清单 | 列清单→对仓库→统一约束→收包 | `anim-set-checklist` |
| 3. 挂事件帧 | 命中/取消/脚步/施法释放，与特效对帧 | `anim-event-hook` |
| 4. 入库校验与交接 | 路径冻结；债务显式分期 | `import-validate` |

**`rigger`（绑定师）** — 骨骼绑定、蒙皮权重、变形校验。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 收模与清单 | 对照骨架模板；扩骨写申请 | `bind-rig-checklist` |
| 2. 搭骨架与控制器 | FK/IK、约束无环、挂点命名 | — |
| 3. 蒙皮权重 | 极姿态刷权重，卡影响骨上限 | `skin-weight-pass` |
| 4. 变形校验 | 标准 Pose 库；与动画对测试 Clip | — |
| 5. 导出剥离与导入 | 运行时骨数量对照动画期望 | `export-naming-gate` → `import-validate` |

**`tech-artist`（技术美术）** — 导入校验、命名门禁、LOD/Shader 与性能预算衔接。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 诊断阻塞资产 | 归属：源资产 / 管线 / 预算 / 工程预设 | — |
| 2. 跑门禁与校验 | 命名扫描、导入、金样回归 | `import-validate` · `export-naming-gate` · `export-pipeline-fix` |
| 3. 预算标定与备忘 | 实机前后数据与截图 | `lod-budget-pass` · `shader-budget-note` · `vfx-budget-pass` |
| 4. 规范沉淀与交接 | 命名段、导入预设、预算上限版本化 | — |

开放世界地形程序化另挂横切技能 `terrain-gaea-pass`（Gaea），不单设职种。

#### 相关技能

| 技能 | 做什么 | 何时用 | 输入 → 输出 |
| :--- | :--- | :--- | :--- |
| `style-anchor` | 用参考板写出一句视觉规则、色形材边界与拒收标准 | 美术风格、Art Bible 切片 | 爱憎参考 → 可版本化锚点 |
| `concept-key-art` | 写 Brief、剪影选型，产出可进 3D 的主视觉与三视图 | 角色设定、关键原画 | 锚点 + 选型 → 生产稿路径 |
| `character-asset-checklist` | 按档位完成建模、UV、贴图、LOD 并导入验收 | 角色模型、高模低模 | Brief + 档位 → 清单勾选与基线姿 |
| `env-asset-checklist` | 按网格定模块尺寸与枢轴，接缝/碰撞/材质复用后试摆 | 模块化场景、环境资产 | 尺度表 → 试摆通过的模块包 |
| `export-naming-gate` | 按 Domain/Type/Name/Variant/LOD 扫描并批量改名 | 命名规范、资源改名 | 导出物 → 映射表与同步引用 |
| `import-validate` | 按导入预设入库，机检缩放/材质/LOD 后固定可引用路径 | FBX 导入、资源入库 | 导出文件 → 冻结路径 |
| `lod-budget-pass` | 订各级面数比与切换距离，实机标定同屏策略 | LOD 预算、减面 | 档位表 → 距离带与抽检证据 |
| `ui-kit-spec` | 盘点控件，定义变体×尺寸×状态合同 | UI Kit、设计系统 | token + 引擎库 → Kit 合同版本 |
| `ui-screen-pass` | 按流程落单屏信息层级、kit 引用、多态与跳转 | 界面稿、screen pass | 流图 + Kit → 四态屏交付包 |
| `vfx-budget-pass` | 订 Overdraw/粒子上限，测热区并做保可读降级 | 特效预算、Fillrate | 画质档 → 降级配置与截图 |
| `anim-set-checklist` | 列出最小可玩与完整动作集，核对片段与技术约束 | 动画集、Locomotion、收包 | 能力边界 → 可冒烟动画包 |
| `bind-rig-checklist` | 对照骨架模板装 IK/约束与 Socket，极端姿验绑定 | 绑定、Rig、挂点 | 生产模 → 骨架/挂点表 |
| `skin-weight-pass` | 按极端姿刷权重，卡影响骨上限与压缩预览 | 蒙皮、飞肉、塌陷 | Rig → 权重通过的极姿态证据 |
| `shader-budget-note` | 盘点变体与关键字，订白名单/指令上限 | Shader 预算、关键字膨胀 | 材质清单 → 白名单与合并方案 |

#### 典型竖切

「主角可进战斗装配」：`activate` 点名 `character-concept-artist` → 批准后另会话点 `character-artist` → `rigger` → `animator` → `vfx-artist`；技美在导入红灯时点 `tech-artist`。`next` 顺序：`style-anchor` → `concept-key-art` → `character-asset-checklist` → `export-naming-gate` / `import-validate` → `bind-rig-checklist` → `skin-weight-pass` → `anim-set-checklist` → `anim-event-hook` → `vfx-skill-hook` / `vfx-budget-pass`。`close` 核 Brief、导入路径、挂点表、事件字典与预算截图。场景线把 `environment-concept-artist` 的 Brief 交给 `environment-artist`，先决 `blockout-pass`。

---

### 6. 品质保障 QA

QA 把「能过」收成可观察的开测/收测条件与证据包。负责人主笔计划与豁免；功能测试从 GDD 抽 GWT；测试开发把高价值用例接到稳定脚手架；兼容测 N/N-1 与机型矩阵；性能对照预算复采。验收当天不改口径装绿。

#### 职种路径

**`qa-lead`（测试负责人）** — 测试计划、验收口径、风险豁免治理。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 定计划 | 范围、环境、可观察开测/收测条件 | `qa-plan` |
| 2. 验收口径与证据映射 | 谁交什么路径；禁止验收日改口径 | — |
| 3. 组织执行与风险滚动 | 分派专项；阻塞有 Owner | — |
| 4. 验收汇总与豁免 | 过/有条件过/不过；豁免含批人/时效/回补 | `artifacts-append` |
| 5. 复盘与模板回灌 | 漏测根因进下版计划 | `bug-report-write`（口径争议样例） |

**`qa-functional`（功能测试工程师）** — 功能用例、缺陷单、回归包。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 读切片定测范围 | 圈主路径/边界/失败态；记下构建号与表版本 | — |
| 2. 写用例与追溯 | 每 AC≥1 条 GWT；建追溯矩阵 | `test-case-from-gdd` |
| 3. 执行与开缺陷 | 步骤可复现；严重度≠优先级 | `bug-report-write` |
| 4. 维回归包 | 已修必有回归条；quarantine 不装绿 | `regression-pack` |
| 5. 助验收与边界 | 证据包给 Lead；不代写自动化框架 | — |

**`qa-automation`（测试开发工程师）** — 自动化脚手架、用例-脚本映射、CI 冒烟稳定。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 落地脚手架 | 目录、夹具、CI 非 0 钩、片状 quarantine | `auto-test-scaffold` |
| 2. 用例-脚本映射 | case_id↔脚本；标覆盖缺口与 flake | `case-automation-map` |
| 3. 写稳脚本 | 造数与清理成对；等待抗抖 | — |
| 4. 接 CI 冒烟并维回归自动 | 冒烟集小而稳；红灯责任人清晰 | `regression-pack` |
| 5. 边界与交接 | 手感/真支付默认不计入覆盖率分子 | — |

**`qa-compatibility`（兼容测试工程师）** — N/N-1 存档与协议、机型矩阵、机型特异缺陷。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 定机型执行面 | 必测/抽测/退役；低端与多 GPU 族在列 | `device-matrix-pass` |
| 2. N/N-1 兼容冒烟 | 旧档升级、协议/资源失败可读且不脏写 | `compat-smoke` |
| 3. 机型特异缺陷 | 驱动/API 线索 vs 全机可复现 | `bug-report-write` |
| 4. 认证协作与矩阵维护 | 条款短项截图含机型 | `platform-cert-smoke` |
| 5. 职种边界自检 | 多分辨率 UI 裁切不是兼容主干 | — |

**`qa-performance`（性能测试工程师）** — 性能预算实测与报告；认证仅协作条款短项。

| 步骤 | 意图 | 打开的技能 |
| :--- | :--- | :--- |
| 1. 收预算并冻场景 | 目标机与帧率/内存/加载档；路线图进版本库 | `perf-budget-check` |
| 2. 搭场景跑测与出报告 | 固定路线、冷热启动、p50/p95 | — |
| 3. 性能缺陷与改法协作 | 热点到模块/资产类型；2～3 改法选项 | `bug-report-write` |
| 4. 认证性能抽检协作 | 只跑条款要求的性能短项 | `platform-cert-smoke` |
| 5. 回归基线与边界 | 样本可复采；Shader 终裁不在本职 | — |

#### 相关技能

| 技能 | 做什么 | 何时用 | 输入 → 输出 |
| :--- | :--- | :--- | :--- |
| `qa-plan` | 用风险矩阵定本迭代用例量级与环境，写开测/收测条件 | 测试计划、开测收测 | 里程碑进出 → 批准版计划 |
| `artifacts-append` | 把本任务产物路径和摘要追加进索引 | 产物登记、验证引用路径 | 产物路径 → `artifacts/index.jsonl` |
| `test-case-from-gdd` | 从 GDD/AC 抽可测点写 GWT，建追溯矩阵 | 写用例、GDD 用例 | 切片 + AC → 用例包与追溯表 |
| `bug-report-write` | 把现象写成可复现缺陷单 | 提单、缺陷报告 | 环境+步骤+证据 → 缺陷单 |
| `regression-pack` | 按变更影响与历史缺陷组回归包 | 版本回跑、影响组包 | 变更面 → 可检索执行队列 |
| `auto-test-scaffold` | 搭测试目录、可注入夹具、CI 失败非 0 钩 | 测试脚手架、CI 接线 | 仓库约定 → 可本地跑通的样例 |
| `case-automation-map` | 把 GWT/回归用例映射到自动化 id | 覆盖缺口、flake | 用例包 → 映射表与排期 |
| `device-matrix-pass` | 按高中低档必测机跑功能冒烟、热与帧稳 | 设备矩阵、低端机、降级开关 | 份额来源 → 版本化矩阵 |
| `compat-smoke` | 定 N/N-1 矩阵，实测旧档升级与失败可读 | 兼容、热更、迁移 | 版本格 → 结果行与坏档隔离记录 |
| `platform-cert-smoke` | 按目标店条款要点跑短清单 | 认证、商店审核、提审冒烟 | 条款子集 → 合规截图包 |
| `perf-budget-check` | 选代表场景采可复采样本，对照预算定位超项 | 性能预算、profiler、卡顿 | 预算表 + 路线 → 报告与改法选项 |

#### 典型竖切

版本提测：`activate` 点名 `qa-lead`（T2/`read` 或 `sandbox`）。`next`：`qa-plan` 批准后分派——功能子代理 `test-case-from-gdd` → `bug-report-write` → `regression-pack`；自动化 `auto-test-scaffold` → `case-automation-map`；兼容 `device-matrix-pass` → `compat-smoke`；性能 `perf-budget-check`。Lead `artifacts-append` 收证据索引。`close` 核开测/收测条件、致命缺陷列表、豁免时效与 `verify-report.json`。构建阻断盘点走横切 `build-gate-checklist`，主路径验收走 `build-acceptance`。

---

### 7. 横切能力 / 运行时与档案

下列技能不挂在任何职种 `uses_skills` 上，但制作会话依赖它们才能定档、隔离写入、检索记忆、关项与补齐部署。它们是运行时与档案柜的牙齿，不是「边角工具」。音频与地形暂无专职种，做法仍在能力库中，由制作人在加载计划里显式点名。

#### 模块在管线中的位置

横切技能在四层之间搬运合同：开场拉外接、对照菜单补缺口、按推荐序拼执行单、把正式面写入推进隔离根、按键检索 Canon、关项只核核心证据。数值职种路径会引用 `attr-family-sync` / `data-readiness-check` / `excel-read` / `excel-format`，但这些 id 必须在加载计划里单独点名才会进入开场名单。

#### 职种关系

横切层**没有**独立职种 id。任何职种都可以在 `loadplan.json` 的 `items` 里点这些 skill。制作人常用 `route-task`（职种路径内）配合本层的 `doctor`、`assemble-craft-flow`、`verify-gate`、`write-isolation`。

#### 技能分组

**运行时与菜单**

| 技能 | 做什么 | 何时用 | 输入 → 输出 |
| :--- | :--- | :--- | :--- |
| `doctor` | 扫技能/职种/外接配置缺口，给出最小补齐或可新部署动作 | 激活失败、catalog 不对齐、0 工具 | 安装树 + `catalog.json` → 缺口清单与补齐步骤 |
| `mcp-autostart` | 启动时按档位拉起外接：核心全量，其余懒接 | 外接挂掉、核心档、懒接 | `mcp-tiers.json` → 已握手工具表 |
| `assemble-craft-flow` | 计划里多个执行类事件时，按推荐序排出执行单 | 拼装、flow、执行类 ≥ 3 | `loadplan` → `flow.json`（收口在尾） |

**写隔离与表格配方**

| 技能 | 做什么 | 何时用 | 输入 → 输出 |
| :--- | :--- | :--- | :--- |
| `write-isolation` | 正式面写入先落到隔离根；晋升须人准且只回写记录集 | 任何非 `read` 写级别 | `surfaces.json` → 沙箱/worktree/_Dev 落点 |
| `excel-read` | 只读工作簿：定位区域、取值/公式/样式、截图 | 写前预检、写后回读 | 正式或沙箱簿 → 值/公式/截图（不保存） |
| `excel-format` | 定级、列角色、小数与占位、对齐；写完必跑 | 颜色、排版、层级 | 已改区域 → 格式层通过 |
| `attr-family-sync` | 新增或重排一层属性时，按读→改→格式→读覆盖受影响表 | 加属性、多层主键同步 | 属性框架变更 → 下游主键已同步的表 |
| `data-readiness-check` | 数值框架簿与战斗模拟数据就绪硬闸 | 多场景平衡、dry-run、表工具重跑 | 框架簿路径 → `data-readiness.json` |
| `personal-server-table-sync` | 改完配表后导表到本机个人服并重载 | 同步个人服、Luban、改表后开服 | 沙箱/正式表 → 本机服已重载 |

**记忆、协作与通用表**

| 技能 | 做什么 | 何时用 | 输入 → 输出 |
| :--- | :--- | :--- | :--- |
| `memory-retrieve` | 开工前按问题检索已批准决策、既往产物和会话记录 | 读 Canon、找既往结论 | `retrieve_keys` → 命中条目列表 |
| `promote-adr` | 把技术选型写成决策记录：背景、选项、选择、后果 | ADR、架构决策、晋升决策记录 | 选型讨论 → `adr/` 文件 |
| `collab-protocol` | 问清目标、关键分叉给选项、分段推进、正式路径写入前先获准 | 先问再写、分段批准 | 模糊诉求 → 已批准选项 |
| `naming-consistency-check` | 扫描实体/字段/UI 键命名冲突与漂移 | 术语统一、rename | 命名表 → 规范名与替换序 |
| `deliverable-sheets` | 按需填写决策、开放问题、进度、交接摘要等通用表 | 决策表、开放问题、进度表 | 会话事实 → 已登记通用表 |
| `diagram-pack` | 按图种选工具落盘：Mermaid / xmind / excalidraw / miro | 流程图、系统循环、架构图 | 图种意图 → 仓库内图文件 |

**构建、验收与关项**

| 技能 | 做什么 | 何时用 | 输入 → 输出 |
| :--- | :--- | :--- | :--- |
| `verify-gate` | 关项前按档位只核核心证据并写验证报告 | 关项、收口 | 档位 + 证据路径 → `verify-report.json` |
| `build-acceptance` | 对目标构建跑主路径验收，对齐版本号，清点已知缺陷处置 | 验收、提测构建核对 | 构建号 → 验收记录 |
| `build-gate-checklist` | 盘点 CI job、产物路径、崩溃签名与已知问题预算 | 构建阻断、CI 红灯盘点 | CI/产物现状 → 可修阻断清单 |

**音频与地形（无专职种，显式点名）**

| 技能 | 做什么 | 何时用 | 输入 → 输出 |
| :--- | :--- | :--- | :--- |
| `audio-fmod-checklist` | 用 FMOD Studio / Audacity / ffmpeg 完成音频事件入库与试听 | 音效、BGM、混音、入库 | 事件表 → 试听通过的事件 |
| `fmod-bank-build` | 用 FMOD Studio / fmodstudiocl 做工程诊断、Bank 构建与 GUID 导出 | Bank、声音打包 | FMOD 工程 → Bank + GUID |
| `terrain-gaea-pass` | 用 Gaea 程序化地形并导出供场景模块衔接 | 地形、heightmap、开放世界地块 | 气质 Brief → heightmap / 地块导出 |

#### 典型竖切（横切命令本身）

任意部门开项前：`menu`（`刷新菜单.py`，菜单旧于源时开场钩子也会后台刷新）。`activate` 写 `loadplan.json`（含 `write_isolation` 与 `verify-gate` 两项）并生成名单。需要检索既往结论时点 `memory-retrieve`；改正式面前先打开 `write-isolation` 与 `excel-read`。执行类事件 ≥ 3 时 `next` 走 `assemble-craft-flow`。部署或握手失败跑 `doctor` + `mcp-autostart`。`close` 只认 `verify-gate` 报告；架构选型另点 `promote-adr`。

---

## 本仓要解决的问题

短列，与能力地图分开。GSH 针对的是制作代理在长流水线里的确定性行为，而不是某一品类的内容排障手册。

- **相关性猜测**：不经加载计划打开「可能用到」的全部技能，串岗、抢写、口径混用。
- **正式面试错**：直接改产品表、主工作区代码或发包资产，失败不可回滚。
- **口头绿**：未写 `verify-report.json` 就关项；结束钩子会拦截。
- **会话失忆**：换窗口或压缩上下文后丢掉目标、禁改与产物路径；现行卡是下一手的事实源。
- **开场过载**：三十六条外接全量握手拖死发现阶段；核心直连、其余懒接。
- **幻觉事实**：把讨论稿当成 Canon；无 `retrieve_keys` 不打开决策库。

---

## 设计哲学

### 第二层对第三层握手

大模型的上下文预算装不下一条完整制作流水线。若把 106 份技能一次注入，代理会同时扮演多个岗位，并用错误口径改表或改引擎资产。GSH 不靠提示词里的「请专注」。**加载计划对能力库握手**：先选职种或事件，再只取这一轮切片。职种是路径，不是清单——点一条岗，先看第一步，走到哪一步再打开哪一份做法。外接同样：开场只握核心手，其余用到再拉。

```text
[用户诉求] → route-task 对照 catalog.json → loadplan.json
        → 生成会话能力名单.py → activated.json + current.md
        → 只注入点名正文与 craft_open → 按步 next → verify-gate
```

### 四层不能合成三层

| 层级 | 解决的确定性问题 | 缺席时的崩溃模式 |
| :--- | :--- | :--- |
| 宪法 | 每轮固定税；拦截密钥、破坏性命令与口头绿 | 窗口被菜单填满；未验证即关项 |
| 加载计划 | 把「相关性」收成显式集合 | 代理串岗、直连正式面、中途迷失 |
| 能力库 | 标准做法不掺杂当次数字 | 每轮重发明「怎么改表」「怎么写用例」 |
| 档案柜 | 会话中断后的状态连续性 | 换窗口忘记进度；口头想法当已批准 |

五套编程工具目录是同一套四层的五份齐套拷贝，不是第五层。落点会变，运转法不该变。

---

## 关键概念

| 概念 | 含义 |
| :--- | :--- |
| 职种 Craft | `agents/<id>.md` 上的岗位路径。`uses_skills` 是序列，开场不预展开。 |
| 技能 Skill | `skills/<id>/SKILL.md` 上的一件事做法。当次数字与当次路径不进正文。 |
| 菜单 catalog | `刷新菜单.py` 从 frontmatter 生成的唯一 id 表。定档禁止现场发明 id。 |
| 加载计划 | `.harness/sessions/<会话>/loadplan.json`：`tier`、`items`、`write_class`、`retrieve_keys`、`forbid`。 |
| 激活名单 | `activated.json`：开场注入哪些正文。不是运行时防火墙。过程中缺技能可当场打开。 |
| 现行卡 | `current.md`：目标、进度、写级别、正式面、隔离根、禁改、下一步。 |
| 写级别 | `read` / `sandbox` / `promote` / `destroy`。默认 `sandbox`。 |
| 正式面 / 隔离根 | `surfaces.json` 里每类业务的 `official` 与 `sandbox`。 |
| 档位 tier | Discuss / T0 / T1 / T2 / T3，决定 `verify-gate` 核多少核心证据。 |
| Canon / ADR | 已批准事实与架构决策；必须被 `retrieve_keys` 命中才打开。 |
| 子代理 | 岗位不同时按职种各开一只；主会话点名与收口。 |

---

## 使用指南

1. 用适配工具打开业务根（含 `.harness/`）。
2. 开场钩子打印现行卡摘要与点名列表；不要把 `catalog.json` 全文灌进上下文。
3. 新交付：复述目标后走 `route-task`，写 `loadplan.json`，执行 `activate`。
4. 点了职种：只读职种正文 + 当前 `craft_open` 技能；`next` 再打开下一步。
5. 写入前读 `write-isolation` 与 `surfaces.json`；改表先 `excel-read`。
6. 多事件且执行类 ≥ 3：`assemble-craft-flow`。
7. 关项：`verify-gate` 写报告；钩子校验 schema 与 `pass`。
8. 换岗：`handoff-pack` + `sync-state`，必要时新会话。

意图与工作模式见 `skills/route-task/SKILL.md`（`continue` / `steer` / `park` / `new` / `parallel` / `discuss`；`work_mode` 为 `agent` 或 `plan`）。

---

## 平台适配

| 目录 | 工具 | 宪法落点 |
| :--- | :--- | :--- |
| `cursor/` | Cursor | `constitution.md`、`rules/`、`hooks/`、`hooks.json` |
| `claude/` | Claude Code | 同构齐套 |
| `codex/` | Codex | 同构齐套 |
| `grok/` | Grok | 同构齐套 |
| `deepseek/` | DeepSeek | 同构齐套 |

安装器把共享运行时落到 `~/.gsh`，再适配各工具家目录。已有 `mcp.json` 不会被覆盖。本包装架构，不装宿主软件。`studio/` 是业务根 `.harness` 模板（`surfaces.json`、`state.json`、Canon 样例）。

---

## 安装与部署

Windows，Python 3.11+。克隆本仓，双击 `一键部署.bat`，填写业务根路径（将创建 `.harness`）。

```powershell
# 部署到指定业务根，默认适配所有工具
.\一键部署.ps1 -Workspace D:\MyStudio

# 仅适配指定工具
.\一键部署.ps1 -Workspace D:\MyStudio -Tools cursor,claude
```

隔离试装（不写真实用户家目录）：

```powershell
python install/install.py --isolate-root D:\probe --workspace D:\probe\ws --tools all
python install/verify_install.py --isolate-root D:\probe --workspace D:\probe\ws
```

入口：`一键部署.bat`、`一键部署.ps1`、`install/install.py`。`install/pack.json` 声明五套齐套根。

---

## CLI 与会话命令

没有单独的 `gsh` 二进制。会话命令对应用户级脚本（Cursor 示例路径；共享运行时亦在 `~/.gsh/harness/scripts/`）：

```text
# menu — 从 skills/ agents/ mcp.json 重建菜单
python %USERPROFILE%\.cursor\harness\scripts\刷新菜单.py

# activate — 校验 loadplan 中的 id，写 activated.json 与 current.md
python %USERPROFILE%\.cursor\harness\scripts\生成会话能力名单.py <会话短名>

# next — 多事件推荐序（执行类在前，收口类在后）
python %USERPROFILE%\.cursor\harness\scripts\建议执行单.py <会话短名> --force

# close — 技能 verify-gate 写报告；结束钩子 hooks/结束.py 校验 verdict
```

收口类 id（执行单链尾）：`verify-gate`、`artifacts-append`、`handoff-pack`、`sync-state`。

其他脚本：`项目库.py`（现行卡）、`接线自检.py`、`握手四层.py`、`整接.py`、`回归四层.py`、`应用外接档位.py`、`拉起外接.py`、`目录夹具.py`、`gsh_paths.py`。

---

## 外接 MCP

外接不设运行时 deny 闸。名单里的外接列表只是开场提示：点名技能声明的 `needs_mcp`，加上计划里显式点的 mcp。职种点名不预展开路径上的外接。做到那一步再打开对应技能。过程中直接调用未点名外接是允许的。

档位见 `harness/mcp-tiers.json`：核心启动即握手（当前仅 `excelMCP`），其余 35 条懒接，第一次调用再拉子进程。默认按换行 JSON 帧。`lazy_stdio.py` 在 IDE 启动时只暴露工具声明。URL 直通（如 `miro`）不套本机包装。拉起脚本在用户级 `harness/scripts/`。用途桩在 `harness/mcp-tools/<id>.json`。

各工具目录内的调度说明：`cursor/harness/docs/MCP调度.md`（claude / codex / grok / deepseek 各有同构副本）。

三十六条外接 id：`accurig` · `audacity` · `blender-mcp` · `cascadeur` · `chrome-devtools` · `cloudcompare` · `docker-mcp` · `everything-search` · `excalidraw` · `excelMCP` · `ffmpeg` · `fmod-cli` · `fmod-studio` · `gaea` · `gamedev-mcp` · `gimp` · `imagemagick` · `inkscape` · `instant-meshes` · `krita-mcp` · `lark-mcp` · `ldtk` · `magicavoxel` · `materialize` · `materialpilot` · `meshlab` · `meshroom` · `miro` · `pureref` · `renderdoc` · `rokoko` · `roslyn-mcp` · `tiled` · `treeit` · `xmind` · `xnormal`。

---

## 安全

- 密钥不进仓库。`mcp.json.example` 只放占位符（如 `${LARK_APP_ID}`）。安装器不会覆盖已有 `mcp.json`。
- 读拦截器 `hooks/读文件前.py` 拦截 `.env`、`credentials.json`、`secrets.json`、`id_rsa`、`*.pem`。
- 命令拦截器 `hooks/命令前.py` 对 `git push --force`、`git reset --hard`、`git clean -fdx` 要求终端确认；关项命令核 `verify-report.json`。
- 若密钥误提交：立即轮换，再重写历史，不要只 revert。
- 漏洞请用 GitHub 私密报告，不要开公开 issue。范围见 [SECURITY.md](SECURITY.md)。

---

## 故障排除

| 现象 | 先查什么 |
| :--- | :--- |
| 激活失败 / 名单报 unknown id | `menu` 刷新；跑 `doctor`；对照 `catalog.json` 与 `agents/`、`skills/` |
| 开场 0 工具或外接挂掉 | `mcp-autostart`；`mcp-tiers.json`；已有 `mcp.json` 是否缺核心键 |
| 现行卡与聊天不一致 | 读 `.harness/sessions/<会话>/current.md` 与 `LATEST`；跑 `sync-state` |
| 改表打到正式簿 | `write-isolation` + `surfaces.json`；沙箱应在正式表同级 `沙箱/` |
| 关项被结束钩子拦住 | 补 `verify-report.json` 且 `verdict=pass`；Discuss 档且无交付则不要写报告 |
| 职种第一步就用最后一步口径 | 名单是否预展开了 `uses_skills`；应只注入 `craft_open` |
| 隔离试装失败 | `install/verify_install.py --isolate-root …` 的缺项列表 |

---

## 测试

架构验收不依赖宿主 DCC：

```powershell
python install/verify_install.py --isolate-root D:\probe --workspace D:\probe\ws
```

四层灰度与回归（业务根 cwd，脚本已部署到用户级 harness）：

```text
python ~/.cursor/harness/scripts/接线自检.py
python ~/.cursor/harness/scripts/握手四层.py
python ~/.cursor/harness/scripts/整接.py
python ~/.cursor/harness/scripts/回归四层.py
```

`verify_install.py` 核验必要技能（`route-task`、`write-isolation`、`doctor`、`verify-gate`、`mcp-autostart`）、钩子与脚本是否落地，并扫描密钥形态路径。README 职种/技能覆盖由 `install/verify_readme_catalog.py` 核对（35/35、106/106）。

---

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

- 技能落在 `skills/<id>/SKILL.md`，frontmatter 写 `name`、`description`，常用外接写 `needs_mcp`。当次数字不进正文。
- 职种落在 `agents/<id>.md`。`uses_skills` 是序列，不是开场必读清单。
- 外接键写进 `mcp.json` 示例，刷新菜单补用途桩。新外接默认懒接。
- 五套工具目录各自齐套。改一套，其余四套同步。
- 提交前缀：`feat:` / `fix:` / `docs:` / `chore:`。改架构先写 `promote-adr`。
- 新增职种或技能后，必须同时更新 `README.md` 与 `README.en.md` 的部门能力地图，保证 35/35、106/106 仍全覆盖。

---

## 许可

[MIT](LICENSE)。Copyright (c) 2026 Game Studio Harness contributors。
