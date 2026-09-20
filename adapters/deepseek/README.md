# DeepSeek Harness

DeepSeek Harness 用户目录默认 `~/.dsh`（`DSH_HOME`）。读 `~/.dsh/AGENTS.md`，技能同时落到 `~/.dsh/skills/` 与 `~/.agents/skills/`（与 Codex 技能链共用后者）。

## 安装器会写

| 目标 | 来源 |
|---|---|
| `~/.dsh/AGENTS.md` | `core/constitution.md` |
| `~/.dsh/skills/` | `core/skills/` |
| `~/.agents/skills/` | `core/skills/` |

业务根的 `AGENTS.md` / `CLAUDE.md` 都会被 DSH 的默认候选文件名读到。不代写 DSH 插件配置。

只装 DeepSeek：`.\一键部署.ps1 -Workspace D:\MyStudio -Tools deepseek`
