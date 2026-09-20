# 给部署代理

先读本文件，再跑 `一键部署.ps1` 或 `scripts/install.py`。不要先改业务仓，不要装 DCC。

- 正文只在 `core/`。
- 各工具只碰 `adapters/<工具>/`。
- 架构是否落地以 `scripts/verify_install.py` 输出 `ok architecture install` 为准。
- 禁止 `--write-mcp` 覆盖已有 `mcp.json`。
- 验收用 `--isolate-root`。
