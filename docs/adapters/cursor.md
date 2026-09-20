# Cursor

**运行时：完整。** 这是 GSH 唯一把钩子、规则、技能、职种、懒 MCP 都接进 IDE 事件的适配器。

## 投影

| 用户级路径 | 来源 |
|---|---|
| `~/.cursor/rules/全局.mdc` | `rules/全局.mdc` |
| `~/.cursor/hooks.json` + `hooks/*.py` | `hooks/` |
| `~/.cursor/skills/` | `skills/`（按 profile 筛选） |
| `~/.cursor/agents/` | `agents/` |
| `~/.cursor/harness/` | `harness/`（含 catalog、mcp-boot） |

仓库内 `.cursor/` **没有** `skills/` 全树。打开本仓时读根目录 `skills/`。

## 缺席

不装 Cursor 适配器：没有 sessionStart 现行卡、没有读文件挡密钥、没有关项闸。其它工具不能补上这些牙齿。

## 安装

```bash
python -m gsh setup --tools cursor --profile full --workspace /path/to/studio --yes
```
