# Grok Build

Grok 用户目录默认 `~/.grok`（`GROK_HOME`）。读 `AGENTS.md`，技能在 `~/.grok/skills/`。官方也能扫 Cursor / Claude 目录；本仓仍单独落一份，避免依赖兼容开关。

## 安装器会写

| 目标 | 来源 |
|---|---|
| `~/.grok/AGENTS.md` | `core/constitution.md` |
| `~/.grok/skills/` | `core/skills/` |
| `~/.grok/agents/` | `core/agents/` |

不代写 `~/.grok/config.toml`。

只装 Grok：`.\一键部署.ps1 -Workspace D:\MyStudio -Tools grok`
