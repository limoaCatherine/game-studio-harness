# 维护者发版清单

完整说明见 [docs/release.md](../docs/release.md)。

## 切版本

- [ ] `__version__` 只改 `gsh/__init__.py`
- [ ] `CHANGELOG.md` 增加 dated `## [X.Y.Z]`
- [ ] README 静态 version badge 与 `__version__` 一致
- [ ] `main` CI 绿色
- [ ] `git tag -a vX.Y.Z` 并 push tag
- [ ] 确认 GitHub Release 挂上 wheel、sdist、`SHA256SUMS`

## 资产期望

- `game_studio_harness-X.Y.Z-py3-none-any.whl`
- `game_studio_harness-X.Y.Z.tar.gz`
- `SHA256SUMS`

Wheel 必须能在**空目录**里 `gsh setup` + `gsh verify`（pack 数据打进包内，不依赖 clone）。

## PyPI

默认不上。Trusted Publisher + `release.yml` 的 `workflow_dispatch` → Publish to PyPI。不要提交 token。本地可用 `twine check dist/*`。
