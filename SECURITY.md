# Security

## Report

Use a [GitHub private vulnerability report](https://github.com/limoaCatherine/game-studio-harness/security/advisories/new). Do not open a public issue for secrets, hook bypasses, or a way to skip confirmation on destructive Git operations.

## Supported versions

| Version | Supported |
|---|---|
| 0.4.x | Yes |
| < 0.4 | Best effort on the current `main` only |

## Scope

This repository, the `gsh` CLI, hook scripts, generated projections, and GitHub Release wheels. Host DCC processes and third-party MCP servers that you install locally are **out of scope** for GSH itself.

## Secrets

- Secrets do not belong in git or in a Release asset. `harness/mcp.json.example` uses `${PLACEHOLDER}` only.
- Setup never overwrites an existing `mcp.json`.
- Cursor `beforeReadFile` denies common secret paths. Other tools do not get that gate — do not assume they do.
- If a secret is committed: rotate it, then rewrite history. A revert commit is not enough.

## Supply chain

- Install from this GitHub repository or from its GitHub Release assets (`*.whl`, `*.tar.gz`, `SHA256SUMS`).
- Verify the checksum before `pipx install ./game_studio_harness-*.whl`.
- Treat unofficial zips and mirrors as untrusted.
- PyPI (`game-studio-harness`) is not published yet. When it is, install only that project name from PyPI via Trusted Publisher builds. See [docs/release.md](docs/release.md).
- This pack ships **zero** live MCP servers. A file under `harness/mcp-tools/` is a purpose stub.

## Isolate before real homedirs

```bash
gsh setup --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --yes
gsh verify --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws
```
