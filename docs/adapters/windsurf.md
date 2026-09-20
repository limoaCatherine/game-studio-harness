# Windsurf

原生入口：`AGENTS.md`、`.windsurfrules`、`.windsurf/rules/gsh.md`。技能同时落到 `skills/` 与 `.windsurf/skills/`。

Windsurf 的级联规则会读这些文件。GSH `hooks.json` 不会在这里执行。`HOOKS.md` 写明开场读现行卡、关项核报告、密钥不进模型。

业务根另有 `.windsurfrules` 与 `.windsurf/rules/gsh.md`。

```bash
python -m gsh setup --tools windsurf --profile core --workspace /path/to/studio --yes
```
