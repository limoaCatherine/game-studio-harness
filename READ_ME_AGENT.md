# 接收方必读（部署代理）

先读本文件，再跑 `一键部署.ps1` 或 `install.py`。不要先改业务仓，不要安装任何 DCC / Excel / MCP 后端软件。

本仓只含 **skill、mcp、rule 的部署逻辑**，外加四层要跑起来所必须的接线。软件本体不进仓。给人看的说明在 `README.md` 与 `自述.md`。

## 目录对照

仓内按 Cursor 用户目录分档，不再使用 `payload/L1` 这种搬运编号。

| 仓内 | 目标 |
|---|---|
| `cursor/rules/全局.mdc` | `~/.cursor/rules/全局.mdc` |
| `cursor/skills/<id>/` | `~/.cursor/skills/<id>/` |
| `cursor/agents/<id>.md` | `~/.cursor/agents/<id>.md` |
| `cursor/hooks/` + `hooks.json` | `~/.cursor/hooks/` |
| `cursor/harness/scripts/` | `~/.cursor/harness/scripts/` |
| `cursor/harness/mcp-tools/` | `~/.cursor/harness/mcp-tools/` |
| `cursor/harness/mcp-tiers.json` | `~/.cursor/harness/mcp-tiers.json`（boot 改成本机） |
| `cursor/harness/mcp-boot/` | `~/.cursor/harness/mcp-boot/` |
| `cursor/mcp.json.example` | `~/.cursor/mcp.json.example` |
| `workspace-scaffold/.harness/` | `<业务根>/.harness/`（已有文件不覆盖） |

## 一步部署

```text
一键部署.bat
```

或：

```text
python install.py --workspace <业务根绝对路径>
python verify_install.py --workspace <业务根绝对路径>
```

禁止用 `--write-mcp` 覆盖对方已有的现网 `mcp.json`。

## 装完立刻做

1. 改 `<业务根>/.harness/surfaces.json`。
2. 写 `loadplan.json`，跑 `生成会话能力名单.py`。
3. 确认 `activated.json` 的 `ok=true`，职种未预展开。
4. 外接软件另见 `docs/工具/总览.md`。无宿主时忽略健康红灯。

架构是否落地以 `verify_install.py` 输出 `ok architecture install` 为准。
