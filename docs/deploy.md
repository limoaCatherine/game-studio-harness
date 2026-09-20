# 部署

## 最短路径

1. Python 3.11+ 加入 PATH。
2. 安装要用的 AI 工具（可只装一部分）。
3. 克隆本仓，双击 `一键部署.bat`，填写业务根。
4. 看到 `ok architecture install`。
5. 打开业务根，改 `.harness/surfaces.json`。

```powershell
.\一键部署.ps1 -Workspace D:\MyStudio -Tools all
python scripts/install.py --workspace D:\MyStudio --tools cursor,claude
python scripts/verify_install.py --workspace D:\MyStudio --tools cursor,claude
```

`--write-mcp` 仅当目标还没有 `mcp.json`。已有现网配置不要加。`--isolate-root` 用于验收，不写真实用户目录。

## 装完

1. 改 `.harness/surfaces.json`。
2. 写 `.harness/sessions/<短名>/loadplan.json`。
3. `python %USERPROFILE%\.gsh\harness\scripts\生成会话能力名单.py <短名>`
4. 确认 `activated.json` 的 `ok=true`，职种未预展开。

缺宿主时外接红灯不算架构失败。各工具落点见 [adapters/README.md](../adapters/README.md)。
