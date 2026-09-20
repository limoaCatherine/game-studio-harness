# Claude Code

Claude Code 读用户级 `~/.claude/CLAUDE.md`，技能在 `~/.claude/skills/`，子代理在 `~/.claude/agents/`。

## 安装器会写

| 目标 | 来源 |
|---|---|
| `~/.claude/CLAUDE.md` | `core/constitution.md` |
| `~/.claude/skills/` | `core/skills/` |
| `~/.claude/agents/` | `core/agents/` |

业务根另写 `CLAUDE.md`（同一份短宪法）。项目级 `.claude/settings.json` 不代写，避免覆盖你的权限集。

## 和 Cursor 的差别

宪法与技能相同。没有 Cursor 那套 `hooks.json` 与 `mcp-tiers` 懒接。MCP 用 Claude 自己的 `.mcp.json` / 用户设置接入同一批宿主。

只装 Claude：`.\一键部署.ps1 -Workspace D:\MyStudio -Tools claude`
