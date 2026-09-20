# L3 能力库

第三层是做法库：106 条技能、35 条职种路径、MCP 用途桩，覆盖完整制作流水线而不是少数竖切。安装后生成 `catalog.json` 给导演点名。点名一条只打开当前步；未点名的仍留在菜单里。

| 物件 | 路径 | 怎么用 |
|---|---|---|
| 技能 | `skills/<id>/SKILL.md` | 当前步打开 |
| 职种 | `agents/<id>.md` | 路径说明；前进用 `gsh next` |
| 菜单 | `harness/catalog.json` | `gsh menu -q …` |
| 路径运行时 | `harness/scripts/职种路径.py` | 记录步号、当前、下一步 |
| MCP 桩 | `harness/mcp-tools/*.json` | 用途说明，不是活进程 |

`gsh menu` 只打印 id 与一行 description。不要把 `catalog.json` 当作系统提示。

MCP 政策见 [docs/mcp-policy.md](../mcp-policy.md)。本仓 0 条活服务器。
