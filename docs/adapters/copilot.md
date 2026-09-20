# GitHub Copilot

原生入口：`copilot-instructions.md`、`instructions/gsh.instructions.md`、`prompts/route-task.prompt.md`、`prompts/verify-gate.prompt.md`。技能/职种投影到该家目录。

Copilot 按 instruction 与 prompt 工作。没有事件钩子，密钥拦截与关项闸要人执行。`HOOKS.md` 写同一条回路。

业务根写到 `.github/copilot-instructions.md` 与 `.github/instructions/gsh.instructions.md`。isolate 下落到 `copilot/`。

```bash
python -m gsh setup --tools copilot --profile core --workspace /path/to/studio --yes
```
