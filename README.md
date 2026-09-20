# Game Studio Harness

一套可部署的游戏制作操作系统：规定代理**每轮读什么、点谁、写到哪、做完留下什么**。技能正文只存一份，落到 Cursor、Claude Code、OpenAI Codex、Grok Build 和 DeepSeek Harness。

四层已经封版。想先弄懂为什么这样拆，读 [docs/架构.md](docs/架构.md)。

![清单 KPI](docs/图表/清单KPI.svg)

| 职种 | 事件技能 | 制作外接 | 适配工具 | 许可 |
| ---: | ---: | ---: | ---: | :---: |
| **35** | **106** | **36** | **5** | MIT |

[自述](自述.md) · [架构思路](docs/架构.md) · [多工具落点](docs/适配.md) · [外接软件](docs/工具/总览.md) · [一键部署](#一键部署)

---

## 四层在管什么

| 层 | 设计逻辑 | 开场进不进窗口 |
|---|---|---|
| **第一层 宪法** | 只写永远要遵守的运转法：定档→制作→结案、读序、名单语义、写隔离、封版。薄，才能每轮都带。 | 始终在 |
| **第二层 定档** | 导演。复述目标，点名本轮 skill/craft/mcp，定写级别，写下现行卡。不生产业务文件。 | 现行卡 + 计划要点 |
| **第三层 能力** | 技能=一件事，职种=一条主路径，外接=宿主接线。按点名打开；职种不预展开。 | 只注入点名正文 |
| **第四层 档案柜** | 当前行、正式面地图、流水、已批准事实。不是知识图谱。按 `retrieve_keys` 取。 | 只取命中条目 |

开场读序：宪法 → 现行卡 → 点名正文 → 命中的 canon/adr。名单只决定开场先注入谁，**不是**运行时防火墙。缺的做法过程中再打开。

![注入漏斗](docs/图表/注入漏斗.svg)

专注度靠集合可预期，不靠口头「请专注」：

- 一件事一个主事件，或一条职种主路径，二者只取其一。
- 职种只带路径第一步（`craft_open`），做到那步再打开下一份技能。
- 岗位不同时按职种开子代理，主会话收口。
- 外接核心直连、其余懒接。

![上下文占用](docs/图表/上下文占用.svg)

![冷启动时延](docs/图表/冷启动时延.svg)

![正式面风险](docs/图表/正式面风险.svg)

默认写隔离根，晋升须人准且只回写记录集。三条曲线都是架构模型，用来说明这几道闸在压什么，不是某工作室实测 SLA。

制作面上，职种按流水线铺开，点岗即可走主路径：

![全流程](docs/图表/全流程.svg)

![职种覆盖](docs/图表/职种覆盖.svg)

---

## 一键部署

先决：Windows，[Python 3.11+](https://www.python.org/downloads/) 已加入 PATH。再装你实际使用的 AI 编程工具（可只装其中几个）。

1. 克隆本仓。
2. 双击 `一键部署.bat`。
3. 给出**业务根**绝对路径（将创建 `.harness`）。回车则在本仓上一级生成 `studio-root`。
4. 看到 `ok architecture install`。
5. 用你的工具打开那个业务根，改 `<业务根>/.harness/surfaces.json`。

```powershell
.\一键部署.ps1 -Workspace D:\MyStudio
.\一键部署.ps1 -Workspace D:\MyStudio -Tools cursor,claude
.\一键部署.ps1 -CursorOnly -Tools all
```

| 工具 | 家目录 | 宪法文件 | 技能落点 |
|---|---|---|---|
| Cursor | `~/.cursor` | `rules/全局.mdc` | `~/.cursor/skills` |
| Claude Code | `~/.claude` | `CLAUDE.md` | `~/.claude/skills` |
| OpenAI Codex | `~/.codex` | `AGENTS.md` | `~/.agents/skills` |
| Grok Build | `~/.grok` | `AGENTS.md` | `~/.grok/skills` |
| DeepSeek Harness | `~/.dsh` | `AGENTS.md` | `~/.dsh/skills` |

共享运行时进 `~/.gsh`。已有的 `mcp.json` **不会被覆盖**。本包装架构文件，不装 Excel / Unity / Blender / FMOD。软件清单见 [docs/工具/总览.md](docs/工具/总览.md)。

```powershell
python install.py --isolate-root D:\probe --workspace D:\probe\ws --tools all
python verify_install.py --isolate-root D:\probe --workspace D:\probe\ws
```

---

## 仓内树

```text
cursor/                 唯一正文：规则、技能、职种、钩子、菜单
adapters/               五套工具的落点注册
workspace-scaffold/     业务根 .harness 档案柜
docs/架构.md            四层设计逻辑
docs/图表/              注入、隔离、覆盖示意
docs/工具/              36 条外接要装什么、怎么用
```

## 不进本仓

- DCC / 引擎 / MCP 后端软件、venv、Node 包
- 现网 `mcp.json` 里的绝对路径、账号、密钥
- 任何工作室的表、文案、工程

## 许可

MIT。见 `LICENSE`。
