# MCP 政策

GSH 把「外接」分成三档。**本仓不声称 36 条全部可用。**

## 本仓配送什么

| 物件 | 是什么 | 不是什么 |
|---|---|---|
| `harness/mcp-tools/*.json`（36） | 用途桩：id、purpose、工具名列表 | 可执行服务器 |
| `harness/mcp.json.example` | 占位启动模板，环境变量全是 `${…}` | 带密钥的活配置 |
| `harness/mcp-tiers.json` | 哪些键若已接线则开场握手，哪些懒接 | 可用性保证 |
| `harness/mcp-boot/lazy_stdio.py` | 发现走缓存、第一次 `tools/call` 再拉子进程 | 子进程本身 |
| `harness/mcp-boot/http_bridge.py` | 把本机 HTTP MCP 桥成 stdio | 远程 SaaS |
| `harness/mcp-boot/cache/*.tools.json` | 工具声明缓存，避免启动时 `tools/list` | 对宿主在线的证明 |

**可接线活服务器配送数量：0。**

## 档位含义

`mcp-tiers.json` 的 `core: ["excelMCP"]` 表示：

> 如果你在本机把 excel 统一 MCP 接进 `mcp.json`，开场就握手。

它**不**表示仓库里有一份 excel MCP 实现，也不表示安装器会下载 `sbroenne` / `haris` / 任何 COM 桥。

其余 35 个键默认懒接或 URL 直通。没有宿主、没有 `${HARNESS_APPS}`、没有本机 MCP 可执行文件时，调用会失败——这是预期，不是安装缺陷。

## 分类

### 可接线（本机自备）

用户自行安装宿主与 MCP 后，把命令写进**本机** `mcp.json`（安装器默认不覆盖已有文件）：

- 表格：`excelMCP`（本机 Python 服务器 + 可选 COM）
- DCC / 中间件：`blender-mcp`、`fmod-studio`、`fmod-cli`、`cascadeur`、`gamedev-mcp`、`krita-mcp`、`gaea`、`rokoko`、`audacity` 等
- 工程：`roslyn-mcp`、`docker-mcp`、`chrome-devtools`
- 搜索 / 图：`everything-search`、`xmind`、`excalidraw`、`miro`

### 仅桩

`mcp-tools/<id>.json` 只有 purpose。菜单刷新会把这些用途挂到 `catalog.mcp[]`。没有对应进程时，点名只能当「提醒本轮可能要用到」。

### 不配送

- 任何 DCC 安装包或许可证
- Unity / Unreal / Excel / FMOD 二进制
- 云账号、Lark / Miro token
- 工作室绝对路径（`${HARNESS_APPS}` 必须由本机填写）

## 密钥

`mcp.json.example` 里的 Lark 参数使用 `${LARK_APP_ID}` / `${LARK_APP_SECRET}`。安装器若写入 `mcp.json`，仍然只是占位符。密钥留在本机密钥管理处。
