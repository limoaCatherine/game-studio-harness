# Claude Code

Claude Code 读 `CLAUDE.md`。GSH 同时写入 `settings.json`，把 `SessionStart` / `PreToolUse` / `Stop` 指到与 Cursor 同一组 Python 钩子。事件名与 Cursor `hooks.json` 不同，脚本相同。

## 家目录

| 路径 | 内容 |
|---|---|
| `~/.claude/CLAUDE.md` | 宪法 |
| `~/.claude/rules/gsh.md` | L1 正文 |
| `~/.claude/settings.json` | 钩子映射 |
| `~/.claude/hooks/*.py` | 开场 / 命令前 / 读前 / 结束 |
| `~/.claude/skills/` `agents/` | 按 profile 投影 |
| `~/.claude/HOOKS.md` | 事件名差异与人要补的步骤 |
| `~/.claude/gsh-capability.json` | `runtime: claude-hooks` |

业务根另有 `.claude/settings.json` 与 `.claude/rules/gsh.md`。

```bash
python -m gsh setup --tools claude --profile core --workspace /path/to/studio --yes
```
