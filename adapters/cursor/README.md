# Cursor

Cursor 是五套里运行时最完整的一落：规则始终生效、钩子能注入现行卡、MCP 可按档位懒接。

## 本目录有什么

| 文件 | 装到 |
|---|---|
| `rules/全局.mdc` | `~/.cursor/rules/` |
| `hooks.json` | `~/.cursor/hooks.json` |
| `mcp.json.example` | `~/.cursor/mcp.json.example`（已有 `mcp.json` 不覆盖） |

技能、职种、钩子脚本、菜单来自 `core/`，不在本目录复制一份。

## 装完

1. 用 Cursor 打开业务根。
2. 改 `.harness/surfaces.json`。
3. 写 `loadplan.json`，跑 `~/.gsh/harness/scripts/生成会话能力名单.py`。

只装 Cursor：`.\一键部署.ps1 -Workspace D:\MyStudio -Tools cursor`
