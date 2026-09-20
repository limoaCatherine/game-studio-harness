# 适配层

`core/` 是唯一正文。本目录只描述**各 AI 编程工具怎么接到那份正文**。适配不是第五层。

| 目录 | 工具 | 装到 |
|---|---|---|
| [cursor/](cursor/README.md) | Cursor | `~/.cursor` |
| [claude/](claude/README.md) | Claude Code | `~/.claude` |
| [codex/](codex/README.md) | OpenAI Codex | `~/.codex` 与 `~/.agents/skills` |
| [grok/](grok/README.md) | Grok Build | `~/.grok` |
| [deepseek/](deepseek/README.md) | DeepSeek Harness | `~/.dsh` |

共享运行时：`~/.gsh`（技能源拷贝、菜单脚本、catalog）。

安装器：`python scripts/install.py --workspace <业务根> --tools cursor,claude`（或 `all`）。
