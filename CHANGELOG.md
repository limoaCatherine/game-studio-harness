# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Version is single-sourced from [`gsh/__init__.py`](gsh/__init__.py).

## [Unreleased]

### Changed

- README / README.en: purpose restated as the full game-production pipeline; added “three things to understand first” (coverage, human–AI boundaries, cited capability curve) before the department map. The map now names all 35 crafts. Architecture index has an English twin.

### Fixed

- CLI reconfigures stdout/stderr to UTF-8 so `gsh menu` / status / next survive Windows cp1252 consoles (CI `tests (windows-latest, py3.11)`).

### Changed

- GitHub Actions: `actions/checkout@v5` and `actions/setup-python@v6` (Node 24 runtime).

## [0.4.0] - 2026-09-20

### Added

- Installable Python package `game-studio-harness` (hatchling, Python ≥3.11) with console script `gsh`.
- Wheel ships `skills/`, `agents/`, `rules/`, `hooks/`, `harness/`, and the studio scaffold so `pip install .` / `pipx install .` works without a live clone.
- `gsh` resolves pack data from `--pack-root`, `GSH_PACK_ROOT`, a git checkout, then bundled `gsh/pack_data`.
- GitHub Actions CI on pull requests: unittest, isolate `gsh verify --tools all`, advisory ruff, and a wheel-install probe from an empty working directory.
- Release workflow: tag `v*.*.*` builds sdist/wheel, writes `SHA256SUMS`, uploads artifacts, and attaches them to the GitHub Release. PyPI publish is a manual OIDC-ready job.
- [docs/release.md](docs/release.md), [.github/RELEASES.md](.github/RELEASES.md), [docs/install.md](docs/install.md), [docs/README.md](docs/README.md), [SUPPORT.md](SUPPORT.md).
- Issue and pull-request templates.

### Changed

- Version moved to `0.4.0` and is read by hatchling from `gsh/__init__.py`.
- README / README.en: working shields.io badges (license, Python, CI, version); install documents pip/pipx after platform support.
- SECURITY, CONTRIBUTING, and CODE_OF_CONDUCT updated for packaged distribution.

## [0.3.1] - 2026-09-20

### Changed

- README / README.en restructured: purpose first, then inventory, capabilities, problem statements, design philosophy (separate), concepts, guides, platform, then install.
- Register: 上下文预算 / context budget; removed oral phrasing and unused `assets/four-layer.svg`.
- MCP policy table restated as 说明 / 边界 (no negative-definition list).

## [0.3.0] - 2026-09-20

### Added

- Craft paths are a runnable pipeline: `activated.json` now stores `craft_path`, and `gsh next` advances the current step.
- Session continuity: `gsh status` / `resume` read `current.md`, `state.json`, and the latest verify report.
- Close workflow: `gsh close` writes `verify-report.json` from a template and appends the audit log.
- Director menu: `gsh menu` looks up craft/skill ids. Boot context refuses a dumped catalog.
- `gsh activate <session>` generates the roster from a loadplan.

### Changed

- README / architecture rewritten capability-first. No hero image. No defect-catalog chapters.

## [0.2.1]

### Added

- Each selected tool home is a complete native tree.
- 19 adapters. Claude Code `settings.json` invokes the same Python hooks.

### Changed

- Default `--tools all`.

## [0.2.0]

### Changed

- Layout refactor: one content source, generated projections.
- Single source of truth at repo root: `skills/`, `agents/`, `rules/`, `hooks/`, `harness/`.
- Python 3.11+ CLI: setup / sync / verify / doctor / uninstall.
- Honest MCP policy (0 live servers shipped).

## [0.1.0]

### Added

- Four-layer freeze and a one-shot installer.

[Unreleased]: https://github.com/limoaCatherine/game-studio-harness/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/limoaCatherine/game-studio-harness/releases/tag/v0.4.0
[0.3.1]: https://github.com/limoaCatherine/game-studio-harness/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/limoaCatherine/game-studio-harness/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/limoaCatherine/game-studio-harness/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/limoaCatherine/game-studio-harness/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/limoaCatherine/game-studio-harness/releases/tag/v0.1.0
