# Game Studio Harness

游戏制作里，代理缺的不是更多技能文件，而是三件事被管住：**窗口预算、正式面不可逆、会话会断**。

本仓用封版的四层来管这三件事。技能正文只在 `core/` 存一份，再落到五套 AI 编程工具。

**先读 [架构拆解](docs/architecture.md)。** 那篇写的是为什么这样拆，不是目录说明。

```mermaid
flowchart LR
  L1[宪法 · 固定税必须薄]
  L2[定档 · 相关性改成集合]
  L3[能力 · 按点名打开]
  L4[档案柜 · 状态在文件里]
  L1 --> L2 --> L3 --> L4 --> L1
```

| 职种 | 技能 | 外接 | 适配 |
| ---: | ---: | ---: | ---: |
| 35 | 106 | 36 | 5 |

---

## 仓库怎么排

根上只留入口。正文、落点、说明、安装器分开。

```text
core/                 唯一正文：宪法、技能、职种、钩子、菜单脚本
adapters/
  README.md           五套总表
  cursor/             Cursor 规则 / 钩子 / mcp 示例
  claude/             Claude Code 落点说明
  codex/              Codex 落点说明
  grok/               Grok Build 落点说明
  deepseek/           DeepSeek Harness 落点说明
studio/               业务根 .harness 模板
docs/architecture.md  思路拆解
docs/deploy.md        怎么装
docs/tools/           外接要装哪些软件
scripts/              install.py / verify_install.py
一键部署.bat
```

不要在根目录再堆说明副本。各工具怎么接到 `core/`，进对应的 `adapters/<工具>/`。

---

## 一键部署

Windows + Python 3.11+。再装你实际用的工具（可只装一部分）。

```powershell
.\一键部署.ps1 -Workspace D:\MyStudio
.\一键部署.ps1 -Workspace D:\MyStudio -Tools cursor,claude
```

| 开关 | 落到 |
|---|---|
| `cursor` | `~/.cursor` |
| `claude` | `~/.claude` |
| `codex` | `~/.codex`、`~/.agents/skills` |
| `grok` | `~/.grok` |
| `deepseek` | `~/.dsh` |

共享运行时：`~/.gsh`。已有 `mcp.json` 不覆盖。不装 Excel / Unity / DCC。软件见 [docs/tools/总览.md](docs/tools/总览.md)。步骤见 [docs/deploy.md](docs/deploy.md)。

---

## 许可

MIT。
