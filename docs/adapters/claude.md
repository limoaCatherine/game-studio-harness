# Claude Code

**运行时：指令 + 可拷技能。** Claude 读 `CLAUDE.md`。GSH 不把 `hooks.json` 说成 Claude 原生钩子。

安装后：`~/.claude/CLAUDE.md`、`~/.claude/skills/`、`~/.claude/agents/`。

缺席：无开场硬注入、无 beforeReadFile、无关项硬闸。必须靠约定先读现行卡，再动手。

```bash
python -m gsh setup --tools claude --profile core --workspace /path/to/studio --yes
```
