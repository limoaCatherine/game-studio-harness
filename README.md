# Game Studio Harness

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![CI](https://img.shields.io/github/actions/workflow/status/limoaCatherine/game-studio-harness/ci.yml?branch=main)](https://github.com/limoaCatherine/game-studio-harness/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.4.0-informational.svg)](CHANGELOG.md)

Game Studio Harness（GSH）是面向**完整游戏制作流水线**的四层上下文操作系统。它把大模型代理接入制作与方向、策划（系统、战斗、关卡、剧情、数值、交互、文案、活动、商业化）、工程、品质、美术音频与活服运营：用文件合同约束本轮范围，按步骤打开技能，默认写入隔离面，验收通过后再由制作方批准回写正式面。

设计主张是**有界自主、可审计 diff、人闸收口**。公开评测把「代理」定义为 Harness 加模型；本仓用点名名单与验收闸，把每一步限制在可核验的短地平线内。

适用对象：制作人、技术总监、主策划、主程序、品质与美术负责人，以及在同一业务根上协作的 AI 编程工具。

```text
定档 → 切片 → 隔离制作 → 验收 → 晋升
```

[English](README.en.md) ·
[设计哲学](#设计哲学) ·
[你需要先了解的三件事](#你需要先了解的三件事) ·
[仓库内容](#仓库内容) ·
[库存盘点](#库存盘点) ·
[部门能力地图](#部门能力地图) ·
[技能从何而来](#技能从何而来) ·
[要解决的问题](#要解决的问题) ·
[关键概念](#关键概念) ·
[指南](#指南) ·
[平台支持](#平台支持) ·
[文档](docs/README.md) ·
[安装](#安装)

---

## 设计哲学

原则说明**为什么这样设计、制作方得到什么**。总口径是有界自主、可审计 diff、人闸收口。

**人闸。** 支柱、砍范围、正式面晋升、活服定价与发版签字会改变玩家体验与商业结果。公开评测显示：任务跨度变长、人闸变少时，无闸长程自主的成功可靠度沿 logistic 下降（依据见「能力曲线」）。GSH 把这些决策留在制作方；代理在短步上产出选项、清单与隔离面 diff，供人审阅后收口。

**隔离面。** 策划表、引擎资产与已提交历史的回滚成本由制作方承担。默认 `write_class=sandbox`，模型只在 `.harness/surfaces.json` 声明的隔离根上执行。晋升是制作流程：须人准，且只回写记录集，便于对照 diff。

**职种路径。** 现场工作有顺序：先冻规则再填系数，先写关卡目标再灰盒，先定节拍再对白，先契约再实现。职种文件是步骤序列（`uses_skills`），技能文件是单步程序。`activated.json` 的 `craft_path` 记录步号与当前技能；`gsh next` 推进一步并回写现行卡，避免第一步按最后一步的口径填写。

**技能蒸馏。** 技能来自真实制作流程：检查表、表配方、灰盒与节拍验收、契约与提测口径被压成可复用的 `SKILL.md`。职种只排顺序；做法正文在技能里。点名一条技能打开的是可执行程序。展开见 [技能从何而来](#技能从何而来)。

**上下文预算。** 每轮固定税保持简短：宪法、现行卡、已指定技能或职种正文。其余技能在执行到该步时再打开。`minimal` / `core` / `full` 决定磁盘投影范围，不决定本轮注入量。

**会话连续性。** 业务根 `.harness` 是跨工具档案柜。探测会话以 `_` 开头，不覆盖 `LATEST`。

**验收证据。** 关项命令是 `gsh close`。Cursor `stop` 与 Claude Code `Stop` 核验同一份报告。其他工具通过 CLI 与 `HOOKS.md` 执行同一流程。

**MCP 懒加载。** `core` 是握手名单。`lazy_stdio` 在首次 `tools/call` 时再拉起子进程。

**密钥隔离与危险操作。** 密钥不得进入仓库，也不得进入模型上下文。`mcp.json.example` 仅含占位符；安装器不覆盖已有 `mcp.json`。不可逆的 Git 与批量删除需要人工确认后执行。

---

## 你需要先了解的三件事

先读这三节，再看职种地图。它们说明 GSH **覆盖整条流水线**、**人机各管什么**、以及**为什么必须把自主边界收紧**。下列百分比全部来自已发表评测，**不是本工作室的实测成功率**。

### 1. 全流程覆盖

GSH 的目标是整条游戏制作流水线。菜单里现有 **35 / 35** 条职种路径与 **106 / 106** 条技能。策划占 **11** 条，两组并列：系统策划、战斗策划、战斗数值、经济数值、养成数值、商业化、活动；以及关卡策划、剧情策划、文案策划、交互策划。其余为制作与项目管理 4、工程 6、美术与技美 9、QA 5。点名一条路径只打开当前步；未点名的职种仍在 catalog 里，需要时再激活。

完整职种表：[docs/crafts/index.md](docs/crafts/index.md)。完整技能表：[docs/skills/index.md](docs/skills/index.md)。音频事件与 Bank 构建是技能（`audio-fmod-checklist`、`fmod-bank-build`），挂在技美 / 管线步骤上，不另造第 36 条职种。

### 2. 人机边界

对齐四层：宪法规定写隔离与破坏闸；导演把诉求写成 `loadplan.json`；能力库按步执行技能；档案柜收下证据。晋升正式面是制作流程，不是模型默认权限。AI 始终在已激活名单内工作，关项必须过验收闸。

| 必须由人 | GSH 约束下 AI 可做 | 共担 |
|---|---|---|
| 体验支柱 / fantasy 调性终裁 | 定档：写 loadplan、生成点名名单 | 里程碑计划选项 |
| 砍范围（scope-cut）批准 | 按 `craft_open` 执行当前步，默认写入隔离面 | 试玩笔记 |
| 隔离面晋升正式面（只回写记录集） | 技能检查表、GDD 功能切片草稿 | 性能预算草案 |
| 活服经济 / IAP 定价终裁 | 隔离面表 diff | QA 豁免提案 |
| 不可逆破坏、密钥保管 | 缺陷单、测试用例、API 契约草稿 | |
| 法务 / 合规 | 实现 + 测试回路，并收集 `verify-report` 证据 | |
| 发版签字 | 状态摘要 / 周报草稿 | |

人闸不得交给模型代签。AI 不得在未激活集合外改正式面，也不得跳过 `gsh close` 把草稿当成已验收。

### 3. 能力曲线

公开评测呈现同一形态：任务变长、人闸变少时，**无闸长程自主的成功可靠度沿 logistic 下降**；加上计划、交互或 Harness 后，同一模型的成绩可以高出数倍（见下表依据，例如同一模型在不同 Harness 上约 6×）。GSH 据此把代理限制在短步（一步一技能）、隔离 diff 与人闸，而不是拉长无人值守地平线。下图左轴数字只复述被引文献的区间；GSH 曲线标为 **ILLUSTRATIVE（示意）**，不是工作室百分比。

**图 A — METR 拟合形态（复述其公开区间）**

成功概率随「人类专家完成该任务所需时间」下降。原文用 logistic 拟合；50% 时间地平线自 2019 年起约每七个月加倍。80% 地平线大约短五倍。杂乱、欠规格任务上成绩更低。

```text
成功概率（METR 公开区间，不是 GSH 实测）
~100% │●
      │  ●
 ~50% │     ●········ 50% 时间地平线（约每 7 个月加倍）
      │        ●
 ~10% │           ●●
      └────────────────────────────→ 人类专家完成该任务所需时间
        < ~4 分钟                 > ~4 小时
```

**图 B — 自主时长 vs 可靠度（ILLUSTRATIVE / 示意）**

形状取自上述评测的共同方向：无闸长程下跌；短步 + 人闸把工作留在高可靠区。**不是本仓基准分数。**

```text
成功可靠度（ILLUSTRATIVE，非实测百分比）
  高 │ ■■■■■■■■■  GSH：短步 + 隔离 diff + 人闸
     │ ■
     │ ●
     │  ●●
     │    ●●●     无闸长程自主（示意 METR 下降形态）
  低 │       ●●
     └────────────────────────────→ 自主时长 / 任务跨度 / 人闸变少
       单技能          多步无闸         长程无人值守
```

依据（百分比均属原文，勿当作 GSH 产线 KPI）：

1. Anthropic：评「代理」= Harness + 模型；SWE-bench Verified 约一年内从 ~40% 到 >80%。<https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
2. SWE-Bench Mobile：最好约 12%；同一模型 Cursor ~12%、OpenCode ~2%（约 6×）。<https://arxiv.org/abs/2602.09540>
3. Harness 消融：收紧上下文窗口时，**上下文管理**贡献最大（主要来自避免溢出失败）。<https://arxiv.org/abs/2609.20804>
4. METR：人类任务 <~4 分钟时成功率约 100%，>~4 小时时 <~10%；50% 地平线约每 7 个月加倍。<https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/>
5. LongCLI-Bench：自主通过率 <20%；注入计划约 58%；计划 + 交互约 62%。<https://arxiv.org/abs/2602.14337>
6. SWE-Marathon：pass@1 <30%；13.8% 的 rollout 出现 reward-hack 尝试。<https://www.swe-marathon.org/>
7. Chen 等：相对副驾驶，代理条件正确率高约 35 个百分点，用户耗时约一半。<https://arxiv.org/abs/2507.08149>
8. CentaurEval：该协作必要题上，LLM 单独 ~0.67%、人单独 ~18.89%、人机协作 ~31.11%。<https://arxiv.org/abs/2512.04111>

---

## 仓库内容

| 类别 | 数量 | 说明 |
|---|---:|---|
| 职种路径（crafts） | 35 | 制作 4、策划 11（系统/战斗/关卡/剧情/数值/交互/文案/活动/商业化）、工程 6、美术 9、QA 5 |
| 技能做法（skills） | 106 | 从真实制作流程蒸馏出的可复用程序（定档、表、灰盒、节拍、契约、验收、交接） |
| 原生适配器 | 19 | 各工具完整原生目录：入口、规则、技能/职种树、钩子或等价文件 |
| MCP | 0 条活服务器 / 36 条用途桩 | 本仓不配送可连接进程 |

```text
game-studio-harness/
├── skills/                 # 106 技能（唯一内容源）
├── agents/                 # 35 职种路径（唯一内容源）
├── rules/ hooks/ harness/  # 宪法、钩子、运行时、菜单
├── gsh/                    # setup / sync / verify / menu / status / next / close
├── studio/.harness/        # 业务根脚手架
├── .cursor/ .claude/ …     # 各工具原生约定（仓库内不复制技能全树）
└── docs/ tests/
```

安装后，共享运行时位于 `~/.gsh`（隔离试装则为 `<isolate>/gsh`）。每个选中的工具家目录再得到一份该工具可识别的完整原生树。

---

## 库存盘点

权威来源是 `catalog.json`（`gsh menu` 扫描仓库根 `agents/` 与 `skills/` frontmatter）。下列清单与唯一内容源 `agents/`（35）和 `skills/`（106）一致。

### 职种 35

| 部门 | 职种 id |
| :--- | :--- |
| 制作与项目管理 | `producer` · `associate-producer` · `project-manager` · `creative-director` |
| 策划 · 系统设计与数值（7） | `systems-designer` · `combat-designer` · `combat-numeric-designer` · `economy-numeric-designer` · `progression-numeric-designer` · `monetization-designer` · `liveops-designer` |
| 策划 · 关卡叙事文案交互（4） | `level-designer` · `narrative-designer` · `copywriter-designer` · `ux-designer` |
| 客户端与服务端工程 | `client-engineer` · `client-combat-engineer` · `client-ui-engineer` · `server-engineer` · `server-combat-engineer` · `tools-engineer` |
| 美术与技术美术 | `character-concept-artist` · `character-artist` · `environment-concept-artist` · `environment-artist` · `ui-artist` · `vfx-artist` · `animator` · `rigger` · `tech-artist` |
| 品质保障 QA | `qa-lead` · `qa-functional` · `qa-automation` · `qa-compatibility` · `qa-performance` |

### 技能 106

职种 `uses_skills` 覆盖 85 个事件技能。其余 21 个不挂在任何职种路径上，放在 [横切能力](#6-横切能力--运行时与档案)：`assemble-craft-flow`、`attr-family-sync`、`audio-fmod-checklist`、`build-acceptance`、`build-gate-checklist`、`collab-protocol`、`data-readiness-check`、`deliverable-sheets`、`diagram-pack`、`doctor`、`excel-format`、`excel-read`、`fmod-bank-build`、`mcp-autostart`、`memory-retrieve`、`naming-consistency-check`、`personal-server-table-sync`、`promote-adr`、`terrain-gaea-pass`、`verify-gate`、`write-isolation`。

完整 id 见下方各部门技能表；能力地图保证 **35/35 职种、106/106 技能各至少出现一次**。蒸馏口径见地图后的 [技能从何而来](#技能从何而来)。

### 外接 36

`accurig` · `audacity` · `blender-mcp` · `cascadeur` · `chrome-devtools` · `cloudcompare` · `docker-mcp` · `everything-search` · `excalidraw` · `excelMCP` · `ffmpeg` · `fmod-cli` · `fmod-studio` · `gaea` · `gamedev-mcp` · `gimp` · `imagemagick` · `inkscape` · `instant-meshes` · `krita-mcp` · `lark-mcp` · `ldtk` · `magicavoxel` · `materialize` · `materialpilot` · `meshlab` · `meshroom` · `miro` · `pureref` · `renderdoc` · `rokoko` · `roslyn-mcp` · `tiled` · `treeit` · `xmind` · `xnormal`

核心档默认直连 `excelMCP`；其余懒接，第一次调用再拉子进程。见 [MCP 政策](#mcp-政策)。本仓配送 0 条活服务器、36 条用途桩。

---

## 部门能力地图

能力地图按工作室部门分块。每个模块包含：（1）该部门在制作管线中的位置；（2）全部职种路径——每一步意图与打开的技能；（3）相关技能的做法、时机与输入输出；（4）一条典型竖切如何用 `menu` / `activate` / `next` / `close` 穿过这些文件。

会话命令与脚本对应关系：

| 命令 | 脚本 / 技能 | 写出 |
| :--- | :--- | :--- |
| `menu` | `gsh menu` / `python -m gsh menu` | `catalog.json` |
| `activate` | `gsh activate <会话>`（`route-task` → 生成会话能力名单） | `loadplan.json`、`activated.json`、`current.md` |
| `next` | `gsh next`（打开 `craft_open` 指向的技能；多事件时 `assemble-craft-flow`） | 下一步技能正文、`flow.json` |
| `close` | `gsh close` / 技能 `verify-gate`（必要时 `artifacts-append` / `sync-state` / `handoff-pack`） | `verify-report.json`、产物索引、状态回写 |

---

### 1. 制作与项目管理

制作部门把方向、容量、依赖和验收收成可跟踪的合同。制作人定目标与发版口径；执行制作人拆包催收；项目管理维护风险与依赖图；创意总监冻结支柱并裁决体验冲突。没有这一层，下游职种会在未批准的范围内改正式面。

| 职种 | id |
| :--- | :--- |
| 制作人 | `producer` |
| 执行制作人 | `associate-producer` |
| 项目管理 | `project-manager` |
| 创意总监 | `creative-director` |

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

### 2. 策划

策划覆盖 catalog 中全部 **11** 条职种，两组并列：系统设计与数值（7）与关卡、叙事、文案、交互（4）。成长曲线由 `progression-numeric-designer` 主笔（`progression-curve`）；战斗数值主笔属性、公式、克制与技能系数。

#### 职种一览（11）

| 职种 | id | 做什么 | 路径技能 |
| :--- | :--- | :--- | :--- |
| 系统策划 | `systems-designer` | 系统索引、功能 GDD 切片、规则可行性 | `systems-index-map` · `feature-gdd-slice` · `rule-feasibility-check` · `promote-canon` |
| 战斗策划 | `combat-designer` | 战斗流程、技能组、手感清单 | `combat-flow-design` · `skill-kit-design` · `combat-feel-checklist` · `feature-gdd-slice` |
| 战斗数值策划 | `combat-numeric-designer` | 属性、公式、克制、技能系数；改表走写入配方 | `combat-modeling` · `attribute-framework` · `damage-formula-pass` · `counter-matrix-pass` · `skill-numeric-pass` · `excel-com-write` · `tunable-table-diff` |
| 经济数值策划 | `economy-numeric-designer` | 产销循环、物价、通胀、表晋升 | `economy-loop-analysis` · `sink-source-map` · `price-curve-pass` · `inflation-stress` · `excel-com-write` · `tunable-table-diff` |
| 养成数值策划 | `progression-numeric-designer` | 成长曲线、解锁节奏、产销接口、属性挂接 | `progression-curve` · `sink-source-map` · `attribute-framework` · `excel-com-write` · `tunable-table-diff` |
| 商业化策划 | `monetization-designer` | 付费点、IAP / 礼包 / 通行证目录、KPI 口径 | `monetization-kpi-pass` · `iap-catalog-check` |
| 活动策划 | `liveops-designer` | 活动日历、活动规格、奖励邮件检查 | `liveops-calendar` · `event-spec` · `reward-mail-check` |
| 关卡策划 | `level-designer` | 关卡目标链、灰盒动线、遭遇、节奏 | `level-goals-spec` · `blockout-pass` · `encounter-script` · `pacing-pass` |
| 剧情策划 | `narrative-designer` | 节拍表、任务规格、对白、世界观一致性 | `narrative-beat-sheet` · `quest-spec` · `lore-consistency-check` · `dialogue-pass` |
| 文案策划 | `copywriter-designer` | 系统 / 引导文案、对白润色、命名与字数 | `naming-consistency-check` · `copy-pass` · `dialogue-pass` |
| 交互策划 | `ux-designer` | 信息架构、UX 流图、可用性走查 | `ux-flow-spec` · `ux-review-pass` |

每条职种在下方有完整路径表（步骤、意图、打开的技能）。


#### 系统设计与数值

系统策划锁规则与接口；战斗策划锁流程与技能组；三路数值分别主笔战斗公式、经济循环与养成曲线；商业化与活动把付费点、活动日历接到同一套实体与开关上。改表一律走读取 → 沙箱写入 → 格式 → diff → 人准晋升。

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

**`liveops-designer`（活动策划）** — 活动日历、活动规格、奖励邮件安全检查。

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

#### 关卡、叙事、文案与交互

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

**`narrative-designer`（剧情策划）** — 节拍表、任务规格、对白规格、世界观一致性。

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

### 3. 客户端与服务端工程

工程部门把已冻结的接口做成可构建的竖切：客户端打通主路径与失败态，战斗客户端对齐帧与预测回滚，UI 客户端维护导航栈与红点，服务端冻契约/存档/反作弊，战斗服务端守结算权威，工具工程把导出与校验收成可 CI 的 CLI。权威数字不在客户端回调里终裁。

| 职种 | id |
| :--- | :--- |
| 客户端开发 | `client-engineer` |
| 客户端战斗开发 | `client-combat-engineer` |
| 客户端 UI 开发 | `client-ui-engineer` |
| 服务端开发 | `server-engineer` |
| 服务端战斗开发 | `server-combat-engineer` |
| 工具开发 | `tools-engineer` |

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

### 4. 美术与技术美术

美术部门从可检验的风格锚走到可引用的引擎路径。原画交可制作 Brief；角色/场景生产过清单与命名门禁；UI 维护 Kit 合同与四态屏；绑定与动画把骨架、权重、事件帧交给战斗与特效；技美把导入、LOD、Shader、VFX 预算收成可抽检的规范。概念未批不开生产模；灰盒未过不换高模。

| 职种 | id |
| :--- | :--- |
| 角色原画 | `character-concept-artist` |
| 角色美术 | `character-artist` |
| 场景原画 | `environment-concept-artist` |
| 场景美术 | `environment-artist` |
| UI 美术 | `ui-artist` |
| 特效 | `vfx-artist` |
| 动画 | `animator` |
| 绑定 | `rigger` |
| 技术美术 | `tech-artist` |

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

### 5. 品质保障 QA

QA 把「能过」收成可观察的开测/收测条件与证据包。负责人主笔计划与豁免；功能测试从 GDD 抽 GWT；测试开发把高价值用例接到稳定脚手架；兼容测 N/N-1 与机型矩阵；性能对照预算复采。验收当天不改口径装绿。

| 职种 | id |
| :--- | :--- |
| 测试负责人 | `qa-lead` |
| 功能测试 | `qa-functional` |
| 测试开发 | `qa-automation` |
| 兼容测试 | `qa-compatibility` |
| 性能测试 | `qa-performance` |

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

### 6. 横切能力 / 运行时与档案

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

## 技能从何而来

技能是从真实工作室流程里蒸馏出来的做法。制作、策划、程序、美术、QA 在产线里已经用过的检查表、表写入配方、灰盒与节拍验收、契约与提测口径，被压成带输入/输出与不合格回退的 `SKILL.md`。职种文件只排步骤顺序；做法正文在技能里。点名一条技能打开的是带输入、输出与不合格回退的可执行程序。

菜单 **106** 条是现行蒸馏结果。新流程先写成技能，再挂进职种路径。完整表见 [docs/skills/index.md](docs/skills/index.md)。能力库层说明见 [docs/architecture/l3-capability.md](docs/architecture/l3-capability.md)。

---

## 要解决的问题

以下是制作现场反复出现、且无法靠单次提示词稳定处理的问题。GSH 用四层文件合同与 CLI 处理它们。

**上下文预算被菜单占满。** 一次把 106 条技能与 35 条职种全文注入对话后，模型会在同一步同时改公式、谈存档、改正式表。GSH 将 `catalog.json` 作为导演检索菜单（`gsh menu`），开场只注入宪法、现行卡与已指定正文。

**多工种路径被一次性展开。** 关卡从目标链到灰盒、剧情从节拍到任务门闸、养成从锚点到成长曲线、战斗数值从锚点到系数表，都有固定顺序。若点名职种即读完全部 `uses_skills`，第一步会按最后一步的口径填表。GSH 只打开 `craft_open`，由 `gsh next` 前进。

**正式面与草稿混写。** 策划表、引擎资产与已提交历史回滚成本由制作方承担。GSH 默认 `write_class=sandbox`，正式面回写需制作方批准，且只回写记录集。

**会话中断、客户端切换后丢失进度。** 聊天记录不是档案。进度写在 `current.md`、`state.json`、`tasks.jsonl`；任意已安装工具上可用 `gsh status` / `gsh resume` 读取。

**缺少可归档的验收记录。** 「感觉可以」无法进入发版材料。`gsh close` 按模板写出 `verify-report.json`（`verify_kind`、`evidence_paths`、`verdict`），并追加审计流水。

**外接进程在 IDE 启动时全部握手。** 数十个 MCP 的 `tools/list` 会拖垮启动并占用上下文。GSH 只对 `mcp-tiers.json` 的 core 档位键做开场握手，其余懒加载。本仓不配送活服务器。

**密钥进入模型上下文；破坏性命令缺少确认。** Cursor 与 Claude Code 在读取与 Shell 前拦截常见密钥路径，并对 `git reset --hard` 等操作要求确认。

---

## 关键概念

| 概念 | 定义与用法 |
|---|---|
| 四层 | 宪法（始终生效）→ 导演（指定 id）→ 能力库（按需打开）→ 档案柜（进度与证据） |
| 职种 | `agents/<id>.md`。可前进的路径。`gsh next` 更新 `craft_open` |
| 技能 | `skills/<id>/SKILL.md`。当前步骤的程序，不含当次数值 |
| 导演菜单 | `gsh menu` 按关键词检索 id。`catalog.json` 是菜单文件，不是系统提示 |
| 现行卡 | `.harness/sessions/<id>/current.md`。更换客户端后首先读取 |
| 关项 | `gsh close` 写出 `verify-report.json` 并追加 `tasks.jsonl` |
| 写隔离 | 默认 `sandbox`。正式面回写需制作方批准，且只回写记录集 |
| 档位 | `minimal` / `core` / `full` 决定投影到家目录的技能与职种 |
| Isolate | 试装根，不写入真实用户家目录 |

```text
[制作诉求]
  → gsh menu 指定 id
  → loadplan + activate
  → 当前步骤技能
  → 隔离面执行
  → gsh close
  → 制作方批准后晋升
```

---

## 指南

下列命令可换成任意职种 id。完整路径见 [部门能力地图](#部门能力地图)。已写成 cookbook 的战斗数值竖切仍可用；关卡、剧情、养成、经济、系统、QA 用同一条 `menu` → `activate` → `next` → `close` 回路。

### 定档并走一步

```bash
python -m gsh setup --workspace /path/to/studio --tools cursor --profile core --yes
cd /path/to/studio
python -m gsh menu --kind craft -q 关卡
# 也可检索：系统策划 / 剧情策划 / 养成数值 / 战斗数值 / 经济 / QA
```

编写 `.harness/sessions/<会话>/loadplan.json`，在 `items` 中指定**一条**职种，例如 `level-designer`、`systems-designer`、`narrative-designer`、`progression-numeric-designer`、`economy-numeric-designer` 或 `combat-numeric-designer`。成长曲线点 `progression-numeric-designer`（技能 `progression-curve`）。

```bash
python -m gsh activate <会话>
python -m gsh resume
# 打开 craft_open 所指技能，在隔离面改表、灰盒笔记或切片草稿
python -m gsh next --craft <职种id>
python -m gsh close --kind schema --evidence .harness/sandbox/<笔记>.md
```

`activated.json` 中的 `craft_path` 显示如 `2/9` 的进度。现行卡与 `state.json` 保持同步。制作方批准后再回写正式面记录格。

战斗数值逐步说明：[docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md)。文档地图：[docs/README.md](docs/README.md)（架构、适配器、cookbook、发版）。

### 更换客户端后续作

在 Cursor 完成定档后，于另一客户端打开同一业务根：

```bash
python -m gsh status --workspace /path/to/studio
python -m gsh resume --workspace /path/to/studio
```

两端读取同一套 `.harness`。Cursor 在 `sessionStart` 注入现行卡摘要；Claude Code 的 `settings.json` 调用同一 `hooks/开场.py`。

### 导演检索，不注入菜单全文

```bash
python -m gsh menu --kind skill -q excel
python -m gsh menu --kind craft -q qa
```

输出为 id 与一行 description。不要将 `catalog.json` 写入系统提示。开场钩子若检测到菜单全文进入上下文，会改写为提示使用 `gsh menu`。

---

## 平台支持

每个选中的工具均获得完整的技能/职种树，以及该工具已支持的入口文件。

| 工具 | 入口 | 钩子 / 自动化 | 其他原生文件 |
|---|---|---|---|
| Cursor | `rules/全局.mdc` | 执行 `hooks.json` | harness、lazy MCP |
| Claude Code | `CLAUDE.md` | 执行 `settings.json` → 同一组 `hooks/*.py` | `HOOKS.md` |
| Codex | `AGENTS.md` | `HOOKS.md` + `gsh status/next/close` | `~/.agents/skills` |
| Windsurf | `.windsurfrules` | 同上 | `.windsurf/rules` |
| Cline | `.clinerules/` | 同上 | — |
| Roo Code | `.roo/rules` | `.roomodes`：director / maker / closer | — |
| Continue.dev | `config.yaml` | prompts：route-task / close / status / next | — |
| GitHub Copilot | instructions + prompts | 同上 | — |
| OpenCode | `opencode.json` | `HOOKS.md` + CLI | — |
| Gemini CLI | `GEMINI.md` | 同上 | — |
| Aider | `CONVENTIONS.md` | `.aider.conf.yml` 只读加载宪法 | — |
| Zed | `AGENTS.md` + `.rules` | 同上 | — |
| Amazon Q / Trae / Junie | 各自 rules / guidelines | 同上 | — |
| Grok / DeepSeek / Kimi / Qwen | `AGENTS.md` / `QWEN.md` | 同上 | — |

CLI 可在上述工具对应的业务根上执行。事件钩子运行时目前接入 Cursor 与 Claude Code。

分篇说明：[docs/adapters/](docs/adapters/)。

---

## 安装

需要 **Python 3.11+**。Windows 为游戏生产环境的一等目标平台；Linux / macOS 用于隔离试装与 CI。安装器只投影架构文件与技能，不附带任何制作软件安装包，不写入密钥。

只从官方仓库或该仓库的 GitHub Release 安装：[github.com/limoaCatherine/game-studio-harness](https://github.com/limoaCatherine/game-studio-harness)。第三方打包不在本项目维护范围内。PyPI 尚未发布。

内容只在仓库根修改：`skills/` `agents/` `rules/` `hooks/` `harness/`。wheel 将这些目录打进包内，因此 `pip install .` / `pipx install .` 之后不必保持 clone。`gsh setup` / `gsh sync` 将同一份内容写成各工具的完整原生目录。

```bash
git clone https://github.com/limoaCatherine/game-studio-harness.git
cd game-studio-harness
python -m pip install .
gsh setup --guided
```

Windows：`py -3.11 -m pip install .`，然后 `gsh setup --workspace D:\studio-root --yes`。

非交互：

```bash
gsh setup \
  --workspace /path/to/studio-root \
  --tools cursor,claude \
  --profile core \
  --yes
```

| 入口 | 命令 |
|---|---|
| PATH 上的 CLI | `gsh setup` |
| 模块 | `python -m gsh setup` |
| Unix | `./install.sh` |
| Windows | `.\install.ps1` 或 `.\一键部署.ps1` |

| `--profile` | 投影内容 | 适用 |
|---|---|---|
| `minimal` | 导演 / 隔离 / 关项 12 技能 + 4 职种 | 先完成一次四层回路 |
| `core` | 日产导演、表格、切片、验收 | 多数制作会话 |
| `full`（默认） | 106 技能 + 35 职种 | 完整菜单落盘 |

`--tools all`（默认）为 19 个客户端各写一套完整原生树。`legacy` = cursor,claude,codex,grok,deepseek。

隔离试装（不写入真实家目录）：

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

pipx、Release wheel、`GSH_PACK_ROOT` 与未来 PyPI：[docs/install.md](docs/install.md)。发版与资产：[docs/release.md](docs/release.md)。

---

## 开始使用

打开**业务根**，不要只打开本仓库。将 `.harness/surfaces.json` 中的占位符改为本机路径；不要把真实盘符提交回 GSH 仓库。

| 任务 | 入口 |
|---|---|
| 定档一轮制作 | `python -m gsh menu --kind craft -q 里程碑`，阅读 `skills/route-task/SKILL.md` |
| 制作与项目管理 | `producer` · `associate-producer` · `project-manager` · `creative-director` |
| 策划 · 系统与数值 | `systems-designer` · `combat-designer` · `combat-numeric-designer` · `economy-numeric-designer` · `progression-numeric-designer` · `monetization-designer` · `liveops-designer` |
| 策划 · 关卡叙事文案交互 | `level-designer` · `narrative-designer` · `copywriter-designer` · `ux-designer` |
| 工程 | `client-engineer` · `client-combat-engineer` · `client-ui-engineer` · `server-engineer` · `server-combat-engineer` · `tools-engineer` |
| 美术与技美 | `character-concept-artist` · `character-artist` · `environment-concept-artist` · `environment-artist` · `ui-artist` · `vfx-artist` · `animator` · `rigger` · `tech-artist` |
| 品质 QA | `qa-lead` · `qa-functional` · `qa-automation` · `qa-compatibility` · `qa-performance` |
| 续作当前会话 | `python -m gsh resume` |
| 查看进度 | `python -m gsh status` |
| 关项 | `python -m gsh close --kind smoke --evidence <产物>` |

```text
gsh menu -q 关卡
  # 或：系统策划 / 剧情 / 养成数值 / 战斗数值 / QA
  → 编写 loadplan.json（指定一条职种 id）
  → gsh activate <会话>
  → 阅读 current.md，只执行当前步骤
  → gsh next
  → gsh close --evidence <隔离面产物>
  → 制作方批准后回写正式面记录格
```

### CLI

```text
python -m gsh setup | sync | verify | doctor | uninstall
python -m gsh menu [--kind craft|skill] [-q 词]
python -m gsh activate <会话>
python -m gsh status | resume
python -m gsh next [--craft <id>]
python -m gsh close --kind smoke --evidence <路径>
```

---

## MCP 政策

本仓配送 **0** 条活服务器、36 条用途桩，以及 `mcp.json.example`。`mcp-tiers.json` 的 `core` 是开场握手名单。excelMCP 出现在 core 中，表示表格管线需要该档位键；本机服务器仍须自行安装。实际拉起走 `lazy_stdio`。

全文：[docs/mcp-policy.md](docs/mcp-policy.md)。

---

## 上下文预算

| 做法 | 节省的注入 |
|---|---|
| L1 保持简短 | 每轮固定税 |
| `gsh menu` 检索 | 100+ 条 description |
| `gsh next` 只打开一步 | 职种路径的后半段 |
| `retrieve_keys` 才打开 canon | 世界观全文 |
| MCP 懒加载 | 开场 `tools/list` |
| minimal / core | 不投影本轮用不到的技能 |

---

## 安全

- 密钥不进入 Git。`mcp.json.example` 仅为占位符。
- 安装器不覆盖已有 `mcp.json`。
- Cursor / Claude Code 拦截常见密钥路径。
- 破坏性 Git 操作需要确认。
- `verify` 与 `tests/test_no_secrets.py` 扫描用户主目录绝对路径、`Harness-Apps`、token 前缀、私钥头、webhook、非示例邮箱。
- 漏洞请使用 GitHub 私密报告，见 [SECURITY.md](SECURITY.md)。

---

## 排障

| 现象 | 处理 |
|---|---|
| `verify` 提示 missing catalog | 先执行 `setup`，使用同一 `--isolate-root` |
| 投影与根目录 skills 不一致 | `python -m gsh sync` |
| 不清楚当前步骤 | `python -m gsh status` |
| 职种路径未前进 | `python -m gsh next --craft <id>` |
| 关项钩子等待报告 | `python -m gsh close --evidence <路径>` |
| 菜单不宜写入提示 | `gsh menu -q …` |
| MCP 全部不可用 | 预期：本仓不配送活服务器 |
| `doctor` 提示 Python 版本过低 | 升级到 3.11+ |

---

## 测试

```bash
python -m unittest discover -s tests -v
```

覆盖菜单解析、职种路径不预展开、密钥扫描、原生树投影、隔离 CLI，以及 `menu` / `activate` / `next` / `close` 回路。

---

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md) · [SUPPORT.md](SUPPORT.md)。

1. 技能只修改 `skills/<id>/SKILL.md`。
2. 职种只修改 `agents/<id>.md`。`uses_skills` 为序列，由 `gsh next` 前进。
3. 新增 MCP：用途桩 + 占位符。不提交可连接服务器或密钥。
4. 新增职种或技能后，两份 README 的部门能力地图都要补上对应 id（35/35、106/106）。
5. 变更四层须先转向并撰写 ADR。
6. PR 须在隔离根上 `verify` 通过，且 `unittest` 通过。

0.1 布局中的 `cursor/skills` 等重复树已删除。在仓库根修改后执行 `sync`。

---

## 许可

[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · [LICENSE](LICENSE) MIT · [CHANGELOG.md](CHANGELOG.md) · [SECURITY.md](SECURITY.md)

四层已封版。进度写入 `.harness`。官方源仅为上述 GitHub 仓库。
