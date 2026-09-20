---
name: mcp-autostart
description: "启动时按档位拉起外接：核心全量，其余懒接。触发：外接拉起、MCP 挂掉、0 工具、核心档、懒接。"
---

# 外接怎么按档拉起

## 何时用

- Cursor 启动后外接 error / loading / 工具数为 0
- 要定哪些启动就连、哪些用到再拉进程

## 档位

名单在 `~/.cursor/harness/mcp-tiers.json`。

**核心（启动全量）**：每日必用、握手快、不等人开宿主。

- `excelMCP`：改表

**懒接**：发现走缓存，第一次 `tools/call` 再起真实进程。

- 空等宿主会堵全场的：`gamedev-mcp`（等 Unity）、`cascadeur`（已有 HTTP 桥）
- 工具表过百的：`docker-mcp`、`fmod-studio`、`materialpilot`
- 其余 DCC / 媒体 / 关卡 / 远程：用到再拉

`miro` 保持 URL，不套本机包装。

## 怎么做

1. 改档位先改 `mcp-tiers.json`，再跑 `~/.cursor/harness/scripts/应用外接档位.py`。
2. 核心条目的 `command` 必须是真实后端，不得套 `lazy_stdio.py`。
3. 懒接包装：`lazy_stdio.py --name <id> --cache ... --framing ndjson -- <原命令>`。对 Cursor 自动认帧；子进程默认换行 JSON，握手失败再试 Content-Length。
4. 启动探活仍走 `拉起外接.py`。用本机约定的编辑器启动器，不把绝对路径写进技能。
5. 会空等的后端不得挡 `initialize` / `tools/list`。

**做到**：核心直连可握手；懒接启动只回缓存；档位文件与 `mcp.json` 一致。
