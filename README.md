# Game Studio Harness

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![CI](https://img.shields.io/github/actions/workflow/status/limoaCatherine/game-studio-harness/ci.yml?branch=main)](https://github.com/limoaCatherine/game-studio-harness/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.4.0-informational.svg)](CHANGELOG.md)

Game Studio Harness（GSH）是面向游戏制作流水线的**四层上下文操作系统**。它把大模型代理接入定档、职种路径、隔离制作与验收晋升：用文件合同约束本轮范围，按步骤打开技能，默认写入隔离面，验收通过后再由制作方批准回写正式面。

适用对象：制作人、技术总监、主策划、主程序，以及在同一业务根上协作的 AI 编程工具。

```text
定档 → 切片 → 隔离制作 → 验收 → 晋升
```

[English](README.en.md) ·
[仓库内容](#仓库内容) ·
[能承接的工作](#能承接的工作) ·
[要解决的问题](#要解决的问题) ·
[设计哲学](#设计哲学) ·
[关键概念](#关键概念) ·
[指南](#指南) ·
[平台支持](#平台支持) ·
[文档](docs/README.md) ·
[安装](#安装)

---

## 仓库内容

| 类别 | 数量 | 说明 |
|---|---:|---|
| 职种路径（crafts） | 35 | 制作、系统数值、关卡体验、工程、品质、美术音频 |
| 技能做法（skills） | 106 | 定档、表格、公式、验收、交接等可复用程序 |
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

## 能承接的工作

GSH 承接的是一条游戏竖切里需要跨职种、跨会话、跨客户端完成的制作工作。下列路径均可按 catalog id 指定、按步骤执行。

### 定档与范围冻结

将「本里程碑只需证明近战 3 秒 TTK」一类诉求写成 `loadplan.json`：指定职种或技能 id、写级别（默认 `sandbox`）、验收种类。`python -m gsh menu` 检索 id；`python -m gsh activate <会话>` 生成 `activated.json` 与现行卡。范围保存在文件中，供后续会话与其他工具读取。

### 战斗数值

`combat-numeric-designer` 路径：建模锚点 → 属性框架 → 公式 / 克制 / 技能系数 → 表写入 → 边角用例 → 表 diff。每一步对应一条技能。`python -m gsh next` 将 `craft_open` 从 `combat-modeling` 推进到 `attribute-framework`，后半段系数表不进入本轮上下文。

### 经济与养成

`economy-numeric-designer`：产销循环、物价、通胀压力、表晋升。  
`progression-numeric-designer`：成长曲线、解锁节奏、属性挂接。  
执行方式与战斗数值相同：一步一技能，在隔离面改表，关项时附上证据路径。

### 关卡、叙事与交互

`level-designer`：目标链、灰盒动线、遭遇与节奏。  
`narrative-designer`：节拍表、任务门闸、对白。  
`ux-designer`：信息架构与界面五态。  
指定一条职种后，本轮只执行当前步骤（例如仅灰盒，或仅 beat），不并行改写文案主键。

### 客户端与服务端

`client-engineer`、`server-engineer` 及战斗 / UI 细分职种，将契约、功能竖切、存档迁移拆成步骤。正式 Git 面仍经隔离面与制作方批准。工程技能约束未冻结的策划数字不得写入代码常量。

### 品质与发版

`qa-lead`：测试计划与验收口径。  
`qa-functional`：用例与缺陷。  
自动化、兼容、性能各有独立路径。关项使用 `python -m gsh close --kind playtest` 或 `--kind build`，证据为用例包或构建日志。

### 活服运营

`liveops-designer`：活动日历、活动规格、奖励邮件检查。日历冲突与补发规则写在技能中；档期数字写在隔离表，不写入职种正文。

### 跨职种交接

`handoff-pack`、`collab-protocol` 与 `python -m gsh status`。下一班次打开业务根后执行 `python -m gsh resume`，读取现行卡与下一步技能，无需依赖即时通讯记录。

完整职种表见 [docs/crafts/index.md](docs/crafts/index.md)，技能表见 [docs/skills/index.md](docs/skills/index.md)。

---

## 要解决的问题

以下是制作现场反复出现、且无法靠单次提示词稳定处理的问题。GSH 用四层文件合同与 CLI 处理它们。

**上下文预算被菜单占满。** 一次把 106 条技能与 35 条职种全文注入对话后，模型会在同一步同时改公式、谈存档、改正式表。GSH 将 `catalog.json` 作为导演检索菜单（`gsh menu`），开场只注入宪法、现行卡与已指定正文。

**多工种路径被一次性展开。** 战斗数值从锚点到系数表有固定顺序。若点名职种即读完全部 `uses_skills`，第一步会按最后一步的口径填表。GSH 只打开 `craft_open`，由 `gsh next` 前进。

**正式面与草稿混写。** 策划表、引擎资产与已提交历史回滚成本由制作方承担。GSH 默认 `write_class=sandbox`，正式面回写需制作方批准，且只回写记录集。

**会话中断、客户端切换后丢失进度。** 聊天记录不是档案。进度写在 `current.md`、`state.json`、`tasks.jsonl`；任意已安装工具上可用 `gsh status` / `gsh resume` 读取。

**缺少可归档的验收记录。** 「感觉可以」无法进入发版材料。`gsh close` 按模板写出 `verify-report.json`（`verify_kind`、`evidence_paths`、`verdict`），并追加审计流水。

**外接进程在 IDE 启动时全部握手。** 数十个 MCP 的 `tools/list` 会拖垮启动并占用上下文。GSH 只对 `mcp-tiers.json` 的 core 档位键做开场握手，其余懒加载。本仓不配送活服务器。

**密钥进入模型上下文；破坏性命令缺少确认。** Cursor 与 Claude Code 在读取与 Shell 前拦截常见密钥路径，并对 `git reset --hard` 等操作要求确认。

---

## 设计哲学

原则与「要解决的问题」分开陈述。下列条目说明**为什么这样设计、制作方得到什么**。

**上下文预算（context window / context budget）。** 每轮固定税保持简短：宪法、现行卡、已指定技能或职种正文。其余技能在执行到该步时再打开。`minimal` / `core` / `full` 决定磁盘投影范围，不决定本轮注入量。

**职种路径。** 职种文件是步骤序列（`uses_skills`），技能文件是单步程序。`activated.json` 的 `craft_path` 记录步号、当前技能与下一步；`gsh next` 推进并回写现行卡。

**正式面与隔离面。** 隔离根由 `.harness/surfaces.json` 声明。模型在隔离面执行；晋升正式面是制作流程，不是模型默认权限。

**会话连续性。** 业务根 `.harness` 是跨工具档案柜。探测会话以 `_` 开头，不覆盖 `LATEST`。

**验收证据。** 关项命令是 `gsh close`。Cursor `stop` 与 Claude Code `Stop` 核验同一份报告。其他工具通过 CLI 与 `HOOKS.md` 执行同一流程。

**MCP 懒加载。** `core` 是握手名单，不是「已安装服务器」名单。`lazy_stdio` 在首次 `tools/call` 时再拉起子进程。

**密钥隔离。** 密钥不得进入仓库，也不得进入模型上下文。`mcp.json.example` 仅含占位符；安装器不覆盖已有 `mcp.json`。

**危险操作确认。** 不可逆的 Git 与批量删除需要人工确认后执行。

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

### 战斗数值竖切

```bash
python -m gsh setup --workspace /path/to/studio --tools cursor --profile core --yes
cd /path/to/studio
python -m gsh menu --kind craft -q 战斗数值
```

编写 `.harness/sessions/combat-ttk/loadplan.json`，在 `items` 中指定 `combat-numeric-designer`。然后：

```bash
python -m gsh activate combat-ttk
python -m gsh resume
# 打开 craft_open 所指技能，在隔离面修改表格
python -m gsh next --craft combat-numeric-designer
python -m gsh close --kind schema --evidence .harness/sandbox/ttk-notes.md
```

`activated.json` 中的 `craft_path` 显示如 `2/9` 的进度。现行卡与 `state.json` 保持同步。制作方批准后再回写正式表记录格。

完整步骤：[docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md)。文档地图：[docs/README.md](docs/README.md)（架构、适配器、cookbook、发版）。

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
| 定档一轮竖切 | `python -m gsh menu --kind craft -q 竖切`，阅读 `skills/route-task/SKILL.md` |
| 战斗数值 / TTK | 指定 `combat-numeric-designer`，`gsh activate`，以 `gsh next` 前进 |
| 经济 / 养成 | `economy-numeric-designer` / `progression-numeric-designer` |
| 关卡灰盒 | `level-designer` |
| 客户端 / 服务端 | `client-engineer` / `server-engineer` |
| QA 验收 | `qa-lead` 或 `qa-functional`，`gsh close` |
| 活服档期 | `liveops-designer` |
| 续作当前会话 | `python -m gsh resume` |
| 查看进度 | `python -m gsh status` |
| 关项 | `python -m gsh close --kind smoke --evidence <产物>` |

```text
gsh menu -q ttk
  → 编写 loadplan.json（指定职种 id）
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
- `verify` 与 `tests/test_no_secrets.py` 扫描用户主目录绝对路径、`Harness-Apps`、`ghp_` / `sk-`。
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
4. 变更四层须先转向并撰写 ADR。
5. PR 须在隔离根上 `verify` 通过，且 `unittest` 通过。

0.1 布局中的 `cursor/skills` 等重复树已删除。在仓库根修改后执行 `sync`。

---

## 许可

[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · [LICENSE](LICENSE) MIT · [CHANGELOG.md](CHANGELOG.md) · [SECURITY.md](SECURITY.md)

四层已封版。进度写入 `.harness`。官方源仅为上述 GitHub 仓库。
