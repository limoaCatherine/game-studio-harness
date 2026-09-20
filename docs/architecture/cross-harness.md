# 跨工具运行时

GSH 的内容只有一份：仓库根 `skills/` `agents/` `rules/` `hooks/` `harness/`。`python -m gsh setup` 把这份内容写成每个工具自己认的完整原生目录。改根目录一处，再 `python -m gsh sync`。

## 装上之后有什么

| 工具 | 家目录（isolate 下为同名文件夹） | 入口 | 钩子 |
|---|---|---|---|
| Cursor | `~/.cursor` | `rules/全局.mdc` | 执行 `hooks.json` |
| Claude Code | `~/.claude` | `CLAUDE.md` | 执行 `settings.json` → `hooks/*.py` |
| Codex | `~/.codex` + `~/.agents/skills` | `AGENTS.md` | `HOOKS.md` |
| Windsurf | `~/.codeium/windsurf` | `AGENTS.md` + `.windsurfrules` | `HOOKS.md` |
| Cline | `~/.cline` | `AGENTS.md` + `.clinerules/` | `HOOKS.md` |
| Roo Code | `~/.roo` | `AGENTS.md` + `.roo/rules` + `.roomodes` | `HOOKS.md` |
| Continue.dev | `~/.continue` | `AGENTS.md` + `config.yaml` | `HOOKS.md` |
| GitHub Copilot | `~/.github` | `copilot-instructions.md` + prompts | `HOOKS.md` |
| OpenCode | `~/.opencode` | `AGENTS.md` + `opencode.json` | `HOOKS.md` |
| Gemini CLI | `~/.gemini` | `GEMINI.md` | `HOOKS.md` |
| Aider | `~/.aider` | `CONVENTIONS.md` + `.aider.conf.yml` | `HOOKS.md` |
| Zed | `~/.config/zed` | `AGENTS.md` + `.rules` | `HOOKS.md` |
| Amazon Q | `~/.amazonq` | `AGENTS.md` + `rules/` | `HOOKS.md` |
| Trae | `~/.trae` | `AGENTS.md` + `rules/` | `HOOKS.md` |
| Junie | `~/.junie` | `guidelines.md` | `HOOKS.md` |
| Grok | `~/.grok` | `AGENTS.md` | `HOOKS.md` |
| DeepSeek | `~/.dsh` | `AGENTS.md` | `HOOKS.md` |
| Kimi Code | `~/.kimi-code` | `AGENTS.md` | `HOOKS.md` |
| Qwen Code | `~/.qwen` | `QWEN.md` | `HOOKS.md` |

每个家目录都包含按 profile 筛选的 `skills/` 与 `agents/`、`mcp.json.example`、`gsh-capability.json`。

## 打开本仓库

把本仓当作项目打开时：

- 规则：`.cursor/rules/全局.mdc`、`.claude/rules/gsh.md`、`.roo/rules/gsh.md` 等约定文件
- 技能：读仓库根 `skills/`，不要在 `.cursor/skills/` 再复制一份
- Cursor 钩子：`.cursor/hooks.json` 调用仓库根 `hooks/*.py`（cwd = 仓库根）
- Claude 钩子：`.claude/settings.json` 调用同一组脚本

## 打开业务根

`setup --workspace` 只补 `.harness` 与各工具会读的入口/规则文件，不把 106 条技能拷进工作室。技能从已安装家目录或本仓 SSOT 读取。
