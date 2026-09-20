# L1 宪法

第一层是每轮对话都会进入窗口的**固定税**。税越重，留给业务制作的窗口越少。因此 L1 只写运转不变量：读序、名单语义、写隔离默认、结案闸、密钥拦截。

## 处理什么

- 会话生命周期：定档 → 制作 → 结案
- 开场读序：规则 → 现行卡 → 点名正文 → 命中的 canon/adr
- 钩子把文本规则绑到 IDE 事件
- 密钥路径与破坏性 git 命令的硬拦截
- 关项必须有 `verify-report.json` 且 `verdict=pass`

## 解决什么

没有 L1，模型会自我格式化工作流、把菜单全文灌进上下文、读进 `.env`、在口头绿之后关项、对未提交改动 `git reset --hard`。

## 路径

| 模块 | 仓库路径 | 安装后（Cursor 完整运行时） |
|---|---|---|
| 始终生效规则 | `rules/全局.mdc` | `~/.cursor/rules/全局.mdc` 或 isolate `cursor/rules/` |
| 跨工具宪法 | `AGENTS.md` | `~/.gsh/AGENTS.md`、业务根 `AGENTS.md` |
| 钩子注册表 | `hooks/hooks.json` | `~/.cursor/hooks.json` |
| 开场 | `hooks/开场.py` | `~/.cursor/hooks/开场.py` |
| 工作区定位 | `hooks/工作区.py` | 同上 |
| 读拦截 | `hooks/读文件前.py` | 同上 |
| 命令拦截 | `hooks/命令前.py` | 同上 |
| 结束闸 | `hooks/结束.py` | 同上 |
| 验证报告字段 | `hooks/校验验证报告.py` | 同上 |
| 数据就绪预检 | `hooks/数据就绪预检.py` | 同上 |

## 各模块缺席崩溃模式

| 模块 | 缺席时 |
|---|---|
| `rules/全局.mdc` | 无读序、无「职种不预展开」、无写隔离默认；模型串岗并直写正式面 |
| `AGENTS.md` | Claude/Codex/Grok 等指令型工具没有任何宪法入口 |
| `hooks.json` | 规则只是文本；Cursor 不会在 sessionStart / beforeReadFile / stop 上执行闸 |
| `开场.py` | 不刷过期菜单、不注入现行卡摘要；模型第一句话就猜进度 |
| `工作区.py` | 找不到 `.harness`，路径靠猜，多工具无法共享会话指针 |
| `读文件前.py` | `.env` / 私钥 / `credentials.json` 可能被读进模型 |
| `命令前.py` | 硬重置与强推无人确认；关项不看验证报告 |
| `结束.py` | 代理可带着 fail 或缺失报告宣称完成 |
| `校验验证报告.py` | 报告字段无法机检，口头绿重新出现 |

## 诚实限制

钩子是 **Cursor 原生运行时**。Claude Code、Codex、Copilot、Grok Bot 不会执行 `hooks.json`。那些工具只靠 `AGENTS.md` / `CLAUDE.md` 约定。详见 [cross-harness.md](cross-harness.md)。
