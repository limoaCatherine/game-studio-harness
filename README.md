# Game Studio Harness

一套面向 **Cursor** 的游戏制作平台架构：把工作室日常拆成规则、技能、职种和外接，再落到每个项目自己的档案柜。别人克隆后可以一键部署到本机，**不必拷贝任何业务表、策划案或密钥**。

| 你要做的事 | 打开 |
|---|---|
| 先看用途、目的、优劣势 | [自述.md](自述.md) |
| 一键部署到本机 | 双击 `一键部署.bat`，或见下方 |
| 架构怎么分层、目录怎么分 | [docs/架构.md](docs/架构.md) |
| 每个外接要装什么、怎么用 | [docs/工具/总览.md](docs/工具/总览.md) |
| 给部署代理的步骤 | [READ_ME_AGENT.md](READ_ME_AGENT.md) |

## 一键部署

先决：Windows，[Python 3.11+](https://www.python.org/downloads/) 已加入 PATH，本机已装 [Cursor](https://cursor.com)。

1. 克隆本仓。
2. 双击 `一键部署.bat`。
3. 按提示给出**业务根**绝对路径（将创建 `.harness`）。回车则默认在本仓上一级生成 `studio-root`。
4. 看到 `ok architecture install` 后，用 Cursor 打开那个业务根。
5. 编辑 `<业务根>/.harness/surfaces.json`，把 official / sandbox 改成你的项目路径。

命令行等价：

```bat
一键部署.bat
```

```powershell
.\一键部署.ps1 -Workspace D:\MyStudio
```

只要用户级、暂不建业务根：

```powershell
.\一键部署.ps1 -CursorOnly
```

本包装的是**架构文件**，不装 Excel / Unity / Blender / FMOD。缺宿主时外接健康检查会红，**不算架构失败**。软件清单见 [docs/工具/总览.md](docs/工具/总览.md)。

## 目录（按 AI 编程工具分档）

仓内目录对齐 Cursor 用户目录，而不是按「第几层」堆编号夹：

```text
cursor/                 →  装到 ~/.cursor/
  rules/                始终生效的规则
  skills/               事件技能（一件事一份）
  agents/               职种 / 角色主路径
  hooks/                开场、结束、工作区钩子
  harness/              菜单脚本、MCP 桩、懒接引导
workspace-scaffold/     →  装到 <业务根>/.harness/
docs/                   给人看的说明与曲线图
一键部署.bat / .ps1     本机部署入口
```

概念上仍是四层：宪法 → 定档 → 能力 → 档案柜。见图：

![上下文占用示意](docs/图表/上下文占用.svg)

点名只注入本轮正文，避免把全部技能灌进窗口。对照见 [自述.md](自述.md#优劣势)。

## 装完立刻做什么

1. 开场读序：`全局.mdc` → 现行卡 → 点名正文 → `retrieve_keys` 命中的 canon / adr。
2. 新工作项：写 `.harness/sessions/<短名>/loadplan.json`（必填 `session_id` `tier` `items` `verify_kind` `intent` `work_mode`）。
3. 在业务根执行：`python %USERPROFILE%\.cursor\harness\scripts\生成会话能力名单.py <短名>`
4. 确认 `activated.json` 的 `ok=true`，职种没有预展开整条 `skills`。
5. 默认 `write_class=sandbox`。晋升须人准，只回写记录集。

## 不进本仓

- DCC / 引擎 / MCP 后端软件、venv、Node 包
- 现网 `mcp.json` 里的绝对路径、账号、密钥
- 运行时 `catalog.json`、`mcp-health.json`（安装后生成）
- 任何工作室的表、文案、工程

## 许可

MIT。见 `LICENSE`。
