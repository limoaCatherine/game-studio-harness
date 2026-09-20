# OpenCode

原生入口：`AGENTS.md`、`rules/gsh.md`、`opencode.json`（`instructions` 指向这两份文件）。技能/职种按 profile 投影。

没有事件钩子。`HOOKS.md` 要求开场读现行卡、关项核报告。

业务根另有 `.opencode/opencode.json`。

```bash
python -m gsh setup --tools opencode --profile core --workspace /path/to/studio --yes
```
