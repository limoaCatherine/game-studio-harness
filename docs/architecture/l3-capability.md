# L3 能力库

第三层是静态工具箱：技能、职种、外接用途桩。它不包含当次数字或临时路径。

## 处理什么

- 扫描 `skills/` 与 `agents/` 的 frontmatter，生成 `catalog.json`
- 职种用 `uses_skills` 声明主路径，供 L2 按步打开
- 外接用途写在 `harness/mcp-tools/*.json`
- 懒加载包装在 `harness/mcp-boot/lazy_stdio.py`

## 解决什么

没有能力库，每次对话都要重发明「怎么改表」「怎么写用例」。没有菜单，模型会发明技能 ID。没有懒加载，Cursor 启动时对几十个 MCP 做 `tools/list` 会卡死。

## 路径

| 模块 | 路径 | 状态 |
|---|---|---|
| 技能 | `skills/<id>/SKILL.md` | 唯一真相，106 条 |
| 职种 | `agents/<id>.md` | 唯一真相，35 条 |
| 刷新菜单 | `harness/scripts/刷新菜单.py` | 安装后写到 `~/.gsh/harness/catalog.json` |
| 用途桩 | `harness/mcp-tools/*.json` | **桩**，不是活服务器 |
| 档位 | `harness/mcp-tiers.json` | excelMCP 标为 core **档位**，不表示已配送 |
| 懒接 | `harness/mcp-boot/lazy_stdio.py` | 真实包装器；子进程由本机宿主决定 |
| HTTP 桥 | `harness/mcp-boot/http_bridge.py` | 给已有 HTTP MCP 用 |
| 启动模板 | `harness/mcp.json.example` | 占位符；安装器默认不覆盖已有 `mcp.json` |

## 缺席崩溃模式

| 模块 | 缺席时 |
|---|---|
| `skills/` | 定档无事件可点；制作无做法 |
| `agents/` | 无职种路径；多岗位只能串演 |
| `刷新菜单.py` / `catalog.json` | 点名无权威 ID；doctor 无法对齐 |
| `mcp-tools/` | 菜单里的外接没有用途说明 |
| `lazy_stdio.py` | 若强行把 36 条都写成直连，开场握手超时 |
| `mcp-tiers.json` | 无法区分「启动就握手」与「用到再拉」 |

## MCP 政策（必须诚实）

本仓**不配送**可连的 MCP 进程，也没有 36 条活服务器。

- `mcp-tools/*.json`：用途与工具名桩，供菜单展示
- `mcp.json.example`：启动模板，全部环境变量都是 `${PLACEHOLDER}`
- `excelMCP` 在 `mcp-tiers.json` 的 `core` 列表里，意思是「如果你在本机接上了，开场就握手」。**仓库里没有 excel MCP 服务器实现**
- DCC（Blender、FMOD、Cascadeur、Unity/`gamedev-mcp` 等）需要你自己安装宿主与对应 MCP
- 远程口（如 `miro`）保持 URL 直通，本仓不托管

详见 [mcp-policy.md](../mcp-policy.md)。
