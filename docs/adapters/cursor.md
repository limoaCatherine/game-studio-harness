# Cursor

Cursor 执行 GSH `hooks.json`。这是把开场读序、密钥拦截、破坏性命令确认、关项核报告绑到 IDE 事件上的运行时。

## 家目录

| 路径 | 来源 |
|---|---|
| `~/.cursor/rules/全局.mdc` | `rules/全局.mdc` |
| `~/.cursor/hooks.json` + `hooks/*.py` | `hooks/` |
| `~/.cursor/skills/` | `skills/`（按 profile） |
| `~/.cursor/agents/` | `agents/` |
| `~/.cursor/harness/` | `harness/`（含 catalog、mcp-boot） |
| `~/.cursor/mcp.json.example` | `harness/mcp.json.example` |
| `~/.cursor/gsh-capability.json` | 安装器写入 |

仓库内 `.cursor/` 只有 hooks/rules 约定，没有 `skills/` 全树。打开本仓时读根目录 `skills/`。

## 钩子

`sessionStart` → `hooks/开场.py`  
`beforeReadFile` → `hooks/读文件前.py`  
`beforeShellExecution` → `hooks/命令前.py`  
`stop` → `hooks/结束.py`

## 缺席

不装 Cursor 适配器：没有 sessionStart 现行卡、没有读文件挡密钥、没有关项闸。其它工具的 `HOOKS.md` 或 Claude `settings.json` 补的是同一条回路的其它入口，不是这份 `hooks.json`。

```bash
python -m gsh setup --tools cursor --profile full --workspace /path/to/studio --yes
```
