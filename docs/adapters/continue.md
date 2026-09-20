# Continue.dev

原生入口：`AGENTS.md`、`rules/gsh.md`、`config.yaml`。`config.yaml` 引用宪法与 L1，并带 `route-task` / `verify-gate` 两条 prompt。

若 `~/.continue/config.yaml` 已有你自己的配置，把 GSH 这份当作合并源，先看 diff 再决定是否覆盖。技能/职种仍投影到该家目录。

没有事件钩子。`HOOKS.md` 写人要补的步骤。

```bash
python -m gsh setup --tools continue --profile core --workspace /path/to/studio --yes
```
