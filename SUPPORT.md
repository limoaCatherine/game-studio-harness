# Support

## Where to ask

- **Bugs and verify failures:** [GitHub Issues](https://github.com/limoaCatherine/game-studio-harness/issues). Use the bug template.
- **Adapter or craft-path questions:** an issue with the tool id and the catalog id.
- **Vulnerabilities and hook bypasses:** [SECURITY.md](SECURITY.md). Do not open a public issue.

This project does not provide vendor support for DCC hosts, engine licenses, or third-party MCP servers that you install locally.

## What to include

1. OS and `python --version` (3.11+ required).
2. `gsh --version` or `python -m gsh --version`.
3. The exact command, including `--isolate-root` / `--workspace` / `--tools` / `--profile`.
4. Output of:

   ```bash
   gsh doctor --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws
   gsh verify --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws
   ```

5. Whether you installed from a git checkout (`pip install -e .`) or from a Release wheel.

Do not paste `mcp.json`, API keys, studio absolute paths, or live table dumps.

## First checks

| Symptom | Action |
|---|---|
| `gsh` not found | `python -m gsh` or `pipx install .` so the console script is on PATH |
| missing skills at pack root | install the wheel or set `GSH_PACK_ROOT` to a checkout |
| `verify` missing catalog | run `gsh setup` with the same isolate and workspace |
| projection drifted | `gsh sync` |
| all MCP hosts unavailable | expected: this pack ships no live servers |

More: [docs/install.md](docs/install.md), [README troubleshooting](README.md#排障).
