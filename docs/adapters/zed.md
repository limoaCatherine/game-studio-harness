# Zed

原生入口：`AGENTS.md`、`.rules`、`settings.json`（agent 段）。技能/职种按 profile 投影。

Zed 会读 `AGENTS.md` 与 `.rules`。没有 GSH 事件钩子。`HOOKS.md` 补开场与关项。isolate 下落到 `zed/`；本机默认 `~/.config/zed`。

```bash
python -m gsh setup --tools zed --profile core --workspace /path/to/studio --yes
```
