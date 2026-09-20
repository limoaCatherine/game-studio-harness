# L1 宪法

第一层是每轮都会进窗口的短规则：读序、写隔离默认、关项命令、密钥与破坏性命令闸。

开场读：规则 → 现行卡 → 点名正文。菜单用 `python -m gsh menu` 检索，不贴进对话。

| 模块 | 仓库路径 | 安装后 |
|---|---|---|
| 始终生效规则 | `rules/全局.mdc` | `~/.cursor/rules/全局.mdc` |
| 跨工具宪法 | `AGENTS.md` | 业务根与各工具入口文件 |
| 钩子 | `hooks/hooks.json` + `hooks/*.py` | Cursor 执行；Claude Code `settings.json` 调同一组脚本 |
| 关项字段 | `hooks/校验验证报告.py` | `gsh close` 写出的报告用同一套字段 |

Cursor `sessionStart` 注入现行卡摘要。Claude Code `SessionStart` 做同一件事。其它工具用 `gsh resume` 得到同一份卡。
