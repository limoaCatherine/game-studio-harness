# OpenAI Codex

Codex 读 `~/.codex/AGENTS.md`，技能落在 `~/.agents/skills/`（官方技能链）。宪法已压短，避开默认约 32KiB 的项目说明上限。

## 安装器会写

| 目标 | 来源 |
|---|---|
| `~/.codex/AGENTS.md` | `core/constitution.md` |
| `~/.agents/skills/` | `core/skills/` |
| `~/.codex/agents/` | `core/agents/` |

业务根写 `AGENTS.md`。不代写 `~/.codex/config.toml`，避免改你的模型与权限。

只装 Codex：`.\一键部署.ps1 -Workspace D:\MyStudio -Tools codex`
