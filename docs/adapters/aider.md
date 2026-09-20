# Aider

原生入口：`CONVENTIONS.md`、`AGENTS.md`、`.aider.conf.yml`（只读加载前两份）。技能/职种按 profile 投影，方便人按 id 打开，Aider 本身没有技能加载器。

没有事件钩子。`HOOKS.md` 写读序、写隔离、关项证据。业务根另有 `.aider.conf.yml` 与 `CONVENTIONS.md`。

```bash
python -m gsh setup --tools aider --profile core --workspace /path/to/studio --yes
```
