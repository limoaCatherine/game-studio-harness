# Cline

原生入口：`AGENTS.md` 与 `.clinerules/gsh.md`。技能/职种按 profile 投影到家目录。

Cline 会读 `.clinerules/`。没有 GSH 事件钩子。`HOOKS.md` 要求人先读现行卡，再动手；没有 `verify-report.json` 的 `pass` 不关项。

业务根另有 `.clinerules/gsh.md`。

```bash
python -m gsh setup --tools cline --profile core --workspace /path/to/studio --yes
```
