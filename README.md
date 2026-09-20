> [!WARNING]
> **只从官方源安装。** 官方仓库：[github.com/limoaCatherine/game-studio-harness](https://github.com/limoaCatherine/game-studio-harness)。第三方打包与网盘镜像不由本项目维护。本仓 MIT，不捆绑制作软件安装包，不提交工作室绝对路径。

# Game Studio Harness

给游戏制作代理一套能跑完竖切的上下文操作系统：先定档，再按职种一步一步做，默认写在隔离根，收口时留下验证报告，人准后再回写正式面。

```text
定档 → 切片 → 隔离制作 → 验证 → 晋升
```

装一次，之后用 `gsh menu` 点名、`gsh next` 走职种路径、`gsh close` 关项。窗口里只留这一轮用得上的正文。

[English](README.en.md) · [安装](#安装) · [开始使用](#开始使用) · [能做什么](#能做什么) · [指南](#指南)

| 职种 | 技能 | 原生适配器 | MCP |
| :---: | :---: | :---: | :---: |
| 35 crafts | 106 skills | 19 套完整原生目录 | 0 条活服务器 / 36 用途桩 |

| 你得到什么 | 数量 | 用途 |
|---|---:|---|
| 职种路径 | 35 | 制作、数值、关卡、工程、QA、美术音频 |
| 技能做法 | 106 | 定档、表格、公式、验收、交接 |
| 钩子运行时 | Cursor + Claude Code | 开场读现行卡、读拦截、关项收口 |
| 导演 / 续上 / 收口 CLI | `menu` `status` `resume` `next` `close` | 跨工具同一套文件合同 |

---

## 安装

需要 **Python 3.11+**。Windows 游戏生产环境是一等公民；Linux / macOS 用于隔离试装与 CI。安装器只投影架构文件与技能。

> [!IMPORTANT]
> 内容只改仓库根 `skills/` `agents/` `rules/` `hooks/` `harness/`。`gsh setup` / `gsh sync` 把同一份内容写成每个工具自己的完整原生目录。

```bash
git clone https://github.com/limoaCatherine/game-studio-harness.git
cd game-studio-harness
python -m gsh setup --guided
```

非交互：

```bash
python -m gsh setup \
  --workspace /path/to/studio-root \
  --tools cursor,claude \
  --profile core \
  --yes
```

| 入口 | 命令 |
|---|---|
| 模块 | `python -m gsh setup` |
| Unix | `./install.sh` |
| Windows | `.\install.ps1` 或 `.\一键部署.ps1` |

### 档位

| `--profile` | 装什么 | 适用 |
|---|---|---|
| `minimal` | 导演 / 隔离 / 收口 12 技能 + 4 职种 | 先把四层跑通 |
| `core` | 日产导演、表格、切片、验收 | 大多数制作会话 |
| `full`（默认） | 106 技能 + 35 职种 | 完整菜单 |

### 工具

`--tools all`（默认）给 19 个客户端各写一套完整原生树。`legacy` = cursor,claude,codex,grok,deepseek。详见 [平台](#platform-support)。

### 隔离试装

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

## 开始使用

打开**业务根**，不是只打开本仓。把 `.harness/surfaces.json` 的占位符改成你本机路径，不要把真实盘符提交回 GSH。

| 你要做的事 | 从这里开始 |
|---|---|
| 定一轮竖切 | `python -m gsh menu --kind craft -q 竖切`，再读 `skills/route-task/SKILL.md` |
| 战斗数值 / TTK | 点 `combat-numeric-designer`，`gsh activate`，按 `gsh next` 走路径 |
| 经济 / 养成 | `economy-numeric-designer` / `progression-numeric-designer` |
| 关卡灰盒 | `level-designer` |
| 客户端 / 服务端 | `client-engineer` / `server-engineer` |
| QA 验收 | `qa-lead` 或 `qa-functional`，收口 `gsh close` |
| 活服档期 | `liveops-designer` |
| 换工具后续上 | `python -m gsh resume` |
| 看进度 | `python -m gsh status` |
| 关项 | `python -m gsh close --kind smoke --evidence <产物>` |

日常回路：

```text
gsh menu -q ttk
  → 写 loadplan.json（点职种 id）
  → gsh activate <会话>
  → 读 current.md，只做当前步
  → gsh next
  → gsh close --evidence <沙箱产物>
  → 人准后回写正式面记录格
```

端到端例子：[docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md)。

---

## What's Inside

```text
game-studio-harness/
├── skills/                 # 106 技能做法
├── agents/                 # 35 职种路径
├── rules/ hooks/ harness/  # 宪法、钩子、运行时、菜单
├── gsh/                    # setup sync verify menu status next close
├── studio/.harness/        # 业务根脚手架
├── .cursor/ .claude/ …     # 各工具原生约定（仓库里不拷技能全树）
└── docs/ tests/
```

安装后共享运行时在 `~/.gsh`（或 isolate `gsh/`）。每个选中的工具家目录再得到一份完整原生树。

---

## Key Concepts

| 概念 | 你用它做什么 |
|---|---|
| 四层 | 宪法始终在；导演点名；能力库按需打开；档案柜记下进度与证据 |
| 职种 | `agents/<id>.md`。一条可前进的路径。`gsh next` 把 `craft_open` 推到下一步 |
| 技能 | `skills/<id>/SKILL.md`。当前这一步的做法，不含当次数字 |
| 导演菜单 | `gsh menu` 按关键词查 id。`catalog.json` 是菜单文件，不是系统提示 |
| 现行卡 | `.harness/sessions/<id>/current.md`。换窗口、换工具先读它 |
| 关项 | `gsh close` 写出 `verify-report.json` 并登记流水 |
| 写隔离 | 默认 `sandbox`。正式面回写要人准，且只回写记录集 |
| 档位 | minimal / core / full 决定家里装哪些文件 |
| Isolate | 试装树，不写真实家目录 |

```text
[诉求]
  → gsh menu 点名
  → loadplan + activate
  → 当前步技能
  → sandbox
  → gsh close
  → 人准晋升
```

---

## 设计哲学

写给制作会里的人：制作人、TD、主策、主程。目标是让模型在下一小时只做这一件事，并且换人换工具还能接上。

**窗口留给制作。** 开场只读宪法、现行卡、点名正文。106 条技能的菜单用 `gsh menu` 检索，不贴进对话。

**职种是可跑的路径。** 点名 `combat-numeric-designer` 时，名单只打开第一步。做完跑 `gsh next`，现行卡改成下一步技能。路径不会在开场被一次读完。

**正式面有隔离层。** 默认写 sandbox。晋升是人准 + changeset 回写记录格。模型可以大胆改草稿，正式表仍由制作方收口。

**进度在文件里。** `current.md`、`state.json`、`tasks.jsonl` 是跨会话档案。`gsh status` / `gsh resume` 在任何客户端上读同一份。

**关项是一条命令。** `gsh close` 按模板写出报告、登记索引、更新现行卡。Cursor `stop` 与 Claude `Stop` 会核这份文件。

**外接按需握手。** 开场只碰 `mcp-tiers.json` 的 core 档位键。本仓不配送活服务器；真正启动走 `lazy_stdio`。详见 [MCP](#mcp)。

**密钥与破坏性命令有闸。** Cursor / Claude Code 在读文件和 shell 前拦截常见密钥路径，并要求确认 `git reset --hard` 一类命令。

---

## 能做什么

GSH 覆盖一条游戏制作竖切里常见的工种。下面每条都是可以照着跑的路径，不是角色扮演提示词。

### 定档竖切

制作人说「这期只要能证明近战 3 秒 TTK」。导演读 `route-task`，用 `gsh menu -q ttk` 确认职种 id，写 `loadplan.json`，`gsh activate`。窗口里出现现行卡：目标、写级别、职种第一步。范围被冻在文件里，而不是聊天里。

### 战斗数值

`combat-numeric-designer` 的路径是：建模锚点 → 属性框架 → 公式 / 克制 / 技能系数 → 表写入 → 边角 → diff。每一步有对应技能。`gsh next` 把工人从 `combat-modeling` 推进到 `attribute-framework`，不会把后面的系数表提前灌进上下文。

### 经济与养成

`economy-numeric-designer` 串产销、物价、通胀与表晋升。`progression-numeric-designer` 串成长曲线、解锁节奏与属性挂接。做法与战斗数值相同：一步一技能，沙箱改表，关项带证据。

### 关卡与体验

`level-designer` 走路目标链、灰盒动线、遭遇与节奏。`narrative-designer` 走节拍、任务门闸、对白。`ux-designer` 走信息架构与五态。点名职种后，只做灰盒或只做 beat，不会同时改文案主键。

### 客户端 / 服务端

`client-engineer`、`server-engineer` 以及战斗/UI 细分职种，把契约、竖切、存档迁移拆成步骤。正式 git 面仍然走 sandbox → 人准。工程技能负责契约与回归包，不把策划未冻的数字写进代码常量。

### QA 与发版

`qa-lead` 出计划与验收口径；`qa-functional` 写用例与缺陷；自动化 / 兼容 / 性能各有路径。收口用 `gsh close --kind playtest` 或 `build`，证据是用例包或构建日志，不是「感觉能过」。

### 活服运营

`liveops-designer` 走活动日历、活动规格、奖励邮件检查。日历碰撞与补发规则写在技能里，档期数字写在沙箱表，不写进职种正文。

### 跨职种交接

`handoff-pack` + `collab-protocol` + `gsh status`。下一班打开业务根，先 `gsh resume`，看到现行卡与下一步技能。不必翻聊天记录。

完整职种表：[docs/crafts/index.md](docs/crafts/index.md)。技能表：[docs/skills/index.md](docs/skills/index.md)。

---

## 指南

### 战斗数值竖切（最短可跑通）

```bash
python -m gsh setup --workspace /path/to/studio --tools cursor --profile core --yes
cd /path/to/studio
python -m gsh menu --kind craft -q 战斗数值
```

写 `.harness/sessions/combat-ttk/loadplan.json`，`items` 里点 `combat-numeric-designer`。然后：

```bash
python -m gsh activate combat-ttk
python -m gsh resume
# 打开 craft_open 指出的技能，在 sandbox 改表
python -m gsh next --craft combat-numeric-designer
python -m gsh close --kind schema --evidence .harness/sandbox/ttk-notes.md
```

`activated.json` 里 `craft_path` 会显示 `2/9` 这类进度。现行卡与 `state.json` 同步。人准之后再回写正式表的记录格。

更完整的步骤：[docs/cookbook/combat-numeric-slice.md](docs/cookbook/combat-numeric-slice.md)。

### 换工具续上

中午在 Cursor 定档，晚上在 Claude Code 打开同一业务根：

```bash
python -m gsh status --workspace /path/to/studio
python -m gsh resume --workspace /path/to/studio
```

两份客户端读同一套 `.harness`。Cursor 开场钩子会注入现行卡摘要；Claude Code 的 `settings.json` 同样调用 `hooks/开场.py`。

### 导演只点名、不灌菜单

```bash
python -m gsh menu --kind skill -q excel
python -m gsh menu --kind craft -q qa
```

输出是 id + 一行 description。不要把 `catalog.json` 贴进系统提示。开场钩子若发现菜单正文被塞进上下文，会改成提醒你用 `gsh menu`。

---

## Platform Support

每个选中的工具都拿到完整技能/职种树和该工具认的入口文件。

| 工具 | 入口 | 钩子 / 自动化 | 其它 |
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

CLI 在所有工具上都能跑。钩子事件运行时目前接在 Cursor 与 Claude Code。

每篇：[docs/adapters/](docs/adapters/)。

---

## MCP

本仓配送 **0** 条活服务器、36 条用途桩、一份 `mcp.json.example`。`mcp-tiers.json` 的 `core` 是开场握手名单。excelMCP 出现在 core 里，表示表格管线需要这个档位键；本机服务器仍要你自己装。真正拉起走 `lazy_stdio`。

政策全文：[docs/mcp-policy.md](docs/mcp-policy.md)。

---

## Token / 上下文

| 做法 | 省下什么 |
|---|---|
| L1 保持短 | 每轮固定税 |
| `gsh menu` 点名 | 100+ 条 description |
| `gsh next` 只打开一步 | 职种后半段做法 |
| `retrieve_keys` 才打开 canon | 整本世界观 |
| MCP 懒接 | 开场 `tools/list` |
| minimal / core | 磁盘上也不装用不到的技能 |

---

## Security

- 密钥不进仓库。`mcp.json.example` 只有占位符。
- 安装器不覆盖已有 `mcp.json`。
- Cursor / Claude Code 读拦截常见密钥路径。
- 破坏性 git 要确认。
- `verify` 与 `tests/test_no_secrets.py` 扫用户主目录绝对路径、`Harness-Apps`、`ghp_` / `sk-`。
- 漏洞用 GitHub 私密报告，见 [SECURITY.md](SECURITY.md)。

---

## Troubleshooting

| 现象 | 先做什么 |
|---|---|
| `verify` 说 missing catalog | 先 `setup`，同一 `--isolate-root` |
| 投影和根 skills 不一致 | `python -m gsh sync` |
| 不知道当前做到哪 | `python -m gsh status` |
| 职种走不动 | `python -m gsh next --craft <id>` |
| 关项钩子还在等报告 | `python -m gsh close --evidence <路径>` |
| 菜单太大不想贴 | `gsh menu -q …`，不要打开 `catalog.json` 当提示 |
| MCP 全红 | 预期：本仓不配送活服务器 |
| `doctor` 报 Python 旧 | 升级到 3.11+ |

---

## Tests

```bash
python -m unittest discover -s tests -v
```

覆盖菜单解析、职种不预展开、密钥扫描、原生树投影、隔离 CLI，以及 `menu` / `activate` / `next` / `close` 回路。

---

## Contributing

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

1. 技能只改 `skills/<id>/SKILL.md`。
2. 职种只改 `agents/<id>.md`。`uses_skills` 是序列，由 `gsh next` 前进。
3. 新 MCP：用途桩 + 占位符。不提交可连服务器或密钥。
4. 改四层先转向、写 ADR。
5. PR 必须隔离根 `verify` 绿，以及 `unittest` 绿。

从 0.1 五树布局迁到根目录 SSOT：旧的 `cursor/skills` 等已删除，改根目录一处再 `sync`。

---

## CLI 速查

```text
python -m gsh setup | sync | verify | doctor | uninstall
python -m gsh menu [--kind craft|skill] [-q 词]
python -m gsh activate <会话>
python -m gsh status | resume
python -m gsh next [--craft <id>]
python -m gsh close --kind smoke --evidence <路径>
```

---

## License

[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · [LICENSE](LICENSE) MIT · [CHANGELOG.md](CHANGELOG.md)

四层已封版。进度写在 `.harness`。官方源只有上面的 GitHub 仓库。
