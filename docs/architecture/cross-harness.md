# 跨工具运行时

GSH 的真相源只有一份。各工具家目录是投影。**禁止假装五工具功能对等。**

## 能力矩阵

| 能力 | Cursor | Claude Code | Codex | Grok / DeepSeek | Windsurf / Cline / Continue / OpenCode / Gemini | GitHub Copilot |
|---|---|---|---|---|---|---|
| 读 `AGENTS.md` / 宪法 | 规则 + 投影 | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | 指令文件 | `copilot-instructions.md` |
| 项目级 / 用户级 skills | 完整投影 | 可拷技能目录 | 可拷到 `.agents/skills` | 可拷技能目录 | 视产品而定 | 无原生 skill 树 |
| `hooks.json` 运行时 | **有** | 无 GSH 钩子 | 无 | 无 | 无 | 无 |
| 开场注入现行卡 | **有** | 靠人/约定先读卡 | 靠约定 | 靠约定 | 靠约定 | 靠约定 |
| 读文件挡密钥 | **有** | 无硬闸 | 无 | 无 | 无 | 无 |
| 关项验证闸 | **有** | 约定 | 约定 | 约定 | 约定 | 约定 |
| 懒 MCP (`lazy_stdio`) | **可接线** | 各产品自己的 MCP | 各产品自己的 MCP | 通常无 | 各产品自己的 MCP | 无 GSH 懒接 |
| 子代理按职种切开 | Cursor Task 可用 | Claude 子代理 | 视版本 | 弱 | 弱 | 弱 |

## 安装投影

`python -m gsh setup` 把根目录 `skills/` `agents/` `rules/` `hooks/` `harness/` 写到共享 `~/.gsh`（或 isolate `gsh/`），再按工具投影：

- Cursor：完整运行时（hooks + rules + skills + agents + harness）
- Claude / Codex / Grok / DeepSeek：宪法文件 + 技能/职种拷贝
- Copilot：只写 instruction
- Continue：只写 snippet + `AGENTS.md`
- 其余：指令文件 + 可选技能拷贝

改根目录一处，再 `python -m gsh sync`。不要手改五棵树。

## 打开本仓库

把本仓当作 Cursor 项目打开时：

- 规则：`.cursor/rules/全局.mdc`（从 `rules/` 同步的单文件）
- 技能：读仓库根 `skills/`，不要在 `.cursor/skills/` 再复制一份
- 钩子：`.cursor/hooks.json` 调用仓库根 `hooks/*.py`（cwd = 仓库根）
