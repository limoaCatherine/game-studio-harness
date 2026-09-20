# Amazon Q Developer

原生入口：`AGENTS.md`、`rules/gsh.md`。Amazon Q 会自动加载 `.amazonq/rules/*.md`。技能/职种按 profile 投影。

没有事件钩子。`HOOKS.md` 补开场与关项。业务根另有 `.amazonq/rules/gsh.md`。

```bash
python -m gsh setup --tools amazonq --profile core --workspace /path/to/studio --yes
```
