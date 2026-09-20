# 安装

需要 **Python 3.11+**。Windows 是游戏生产环境的一等目标；Linux / macOS 用于隔离试装与 CI。安装器只投影架构文件与技能，不附带制作软件，不写入密钥。

只从官方仓库或该仓库的 GitHub Release 安装：[github.com/limoaCatherine/game-studio-harness](https://github.com/limoaCatherine/game-studio-harness)。

内容只在仓库根修改：`skills/` `agents/` `rules/` `hooks/` `harness/`。`gsh setup` / `gsh sync` 将同一份内容写成各工具的完整原生目录。wheel 把上述目录打进 `gsh/pack_data/`，因此 `pipx install .` 之后不必保持 clone 在 PATH 上。

## pip / pipx（推荐）

在 clone 根目录：

```bash
python -m pip install .
# 或隔离 CLI，写入用户 PATH
pipx install .
gsh --version
gsh setup --workspace /path/to/studio-root --yes
```

Windows：

```bat
py -3.11 -m pip install .
gsh setup --workspace D:\studio-root --yes
```

可编辑安装（改 SSOT 的贡献者）：

```bash
python -m pip install -e ".[dev]"
```

覆盖 pack 根（例如一份未安装的检出）：

```bash
set GSH_PACK_ROOT=D:\src\game-studio-harness
gsh setup --yes
```

POSIX：`export GSH_PACK_ROOT=/path/to/game-studio-harness`。

## 从 GitHub Release 的 wheel

下载 `game_studio_harness-X.Y.Z-py3-none-any.whl` 与 `SHA256SUMS`，校验后再装：

```bash
pipx install ./game_studio_harness-X.Y.Z-py3-none-any.whl
```

PyPI 尚未发布。`pip install game-studio-harness` 在 Trusted Publisher 就绪前会失败。见 [release.md](release.md)。

## 检出内脚本

不经过 pip 时，在仓库根：

```bash
git clone https://github.com/limoaCatherine/game-studio-harness.git
cd game-studio-harness
python -m gsh setup --guided
```

| 入口 | 命令 |
|---|---|
| 已安装控制台脚本 | `gsh setup` |
| 模块 | `python -m gsh setup` |
| Unix | `./install.sh` |
| Windows | `.\install.ps1` 或 `.\一键部署.ps1` |

## 档位与工具

| `--profile` | 投影内容 | 适用 |
|---|---|---|
| `minimal` | 导演 / 隔离 / 关项 12 技能 + 4 职种 | 先完成一次四层回路 |
| `core` | 日产导演、表格、切片、验收 | 多数制作会话 |
| `full`（默认） | 106 技能 + 35 职种 | 完整菜单落盘 |

`--tools all`（默认）为 19 个客户端各写一套完整原生树。`legacy` = cursor,claude,codex,grok,deepseek。

## 隔离试装

不写入真实用户家目录：

```bash
gsh setup --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --tools all --profile full --yes
gsh verify --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws
gsh sync --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --yes
gsh uninstall --isolate-root /tmp/gsh-probe --yes
```

Windows：`--isolate-root %TEMP%\gsh-probe`。
