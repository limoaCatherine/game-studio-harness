# 发版

Game Studio Harness 使用 [SemVer](https://semver.org/lang/zh-CN/)：`MAJOR.MINOR.PATCH`。版本只写在 [`gsh/__init__.py`](../gsh/__init__.py) 的 `__version__`；`pyproject.toml` 由 hatchling 读取该字段。

变更写入 [CHANGELOG.md](../CHANGELOG.md)，格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## 切一个版本

1. 在主分支上确认 CI 绿色：`unittest`、隔离根 `gsh verify --tools all`、wheel 空目录安装探测。
2. 把 `__version__` 改为下一个 SemVer（例如 `0.4.1`）。
3. 在 `CHANGELOG.md` 把 `## [Unreleased]` 下的条目移到 `## [0.4.1] - YYYY-MM-DD`。
4. 若 README 使用静态 version badge，把 `version-0.4.0` 改成新版本（`tests/test_packaging.py` 会核对）。
5. 合并到 `main`。
6. 打 annotated tag 并推送：

   ```bash
   git tag -a v0.4.1 -m "Game Studio Harness 0.4.1"
   git push origin v0.4.1
   ```

7. `.github/workflows/release.yml` 在 `v*.*.*` tag 上构建 sdist / wheel，计算 `SHA256SUMS`，并挂到 GitHub Release。

不要用手打包上传未经 checksum 的 zip。不要把 `mcp.json`、密钥或本机盘符写进发行物。

## GitHub Release 资产

每个 tag 的 Release 应包含：

| 资产 | 说明 |
|---|---|
| `game_studio_harness-X.Y.Z-py3-none-any.whl` | 可 `pip install` / `pipx install`；内含 `gsh` 控制台入口与 pack 数据 |
| `game_studio_harness-X.Y.Z.tar.gz` | sdist，含源码树与测试 |
| `SHA256SUMS` | 上述文件的 SHA-256 |

Wheel 内必须带：`skills/`、`agents/`、`rules/`、`hooks/`、`harness/`、`AGENTS.md`、业务根脚手架。装上后在**任意工作目录**执行 `gsh setup` 即可投影，不必再 clone。

校验：

```bash
pipx install ./game_studio_harness-X.Y.Z-py3-none-any.whl
gsh --version
gsh setup --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --yes
gsh verify --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws
```

Windows（`py` launcher）：

```bat
py -3.11 -m pip install game_studio_harness-X.Y.Z-py3-none-any.whl
gsh --version
```

## 尚未发布到 PyPI

当前发行通道是 **GitHub Releases**。`pip install game-studio-harness` 在 PyPI 上线之前会失败，这是预期。

上线步骤（维护者）：

1. 在 PyPI 创建项目 `game-studio-harness`，配置 Trusted Publisher：GitHub org/user `limoaCatherine`，仓库 `game-studio-harness`，workflow `release.yml`，environment `pypi`。
2. 在仓库 Settings → Environments 增加 `pypi`，限制为维护者。
3. 在已构建的 tag 上（或 `workflow_dispatch`）勾选 **Publish the built distributions to PyPI**。
4. 工作流使用 OIDC（`id-token: write`），**不要**把 PyPI token 写进仓库或 Actions secrets。
5. 本地等价：`python -m build && twine check dist/*`。`twine upload` 仅在 Trusted Publisher 尚未就绪时由维护者本机执行。

发布后可将 README 的 version badge 换成：

`https://img.shields.io/pypi/v/game-studio-harness`

在此之前不要使用 PyPI badge，避免裂图。

## 支持的安装方式

| 方式 | 命令 | 适用 |
|---|---|---|
| 从 clone 可编辑安装 | `python -m pip install -e .` | 改 SSOT 的贡献者 |
| 从 clone 用户安装 | `python -m pip install .` 或 `pipx install .` | 制作方本机 CLI |
| 从 Release wheel | `pipx install ./game_studio_harness-*.whl` | 不保留 git 树 |
| 未来 PyPI | `pipx install game-studio-harness` | 见上 |

`pipx` 把 `gsh.exe` / `gsh` 放到用户 PATH，Windows 与 POSIX 行为一致。`python -m gsh` 始终可用。
