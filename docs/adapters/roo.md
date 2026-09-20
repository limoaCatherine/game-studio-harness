# Roo Code

原生入口：`AGENTS.md`、`.roo/rules/gsh.md`、`.roomodes`。

`.roomodes` 提供三条 GSH 模式：

- `gsh-director`：定档，写 loadplan，不改正式面
- `gsh-maker`：只做当前 `craft_open` 或点名技能，默认 sandbox
- `gsh-closer`：运行 `python -m gsh close` 并附上证据路径

没有事件钩子。`HOOKS.md` 补开场与关项。

```bash
python -m gsh setup --tools roo --profile full --workspace /path/to/studio --yes
```
