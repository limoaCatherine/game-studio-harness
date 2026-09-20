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

## What not to commit

Do not add any of the following to git, issues, pull requests, chat, or Release assets:

- `.env`, live `mcp.json`, live `host-paths.json`, `credentials.json`, `secrets.json`, `.pypirc`, `.npmrc` with tokens
- `*.pem`, `*.pfx`, `*.p12`, `*.key`, SSH private keys (`id_rsa`, `id_ed25519`, `id_ecdsa`)
- API keys, access tokens, passwords, private keys, webhook URLs
- User-profile absolute paths (`C:\Users\<you>\...`, `/Users/<you>/...`) and host `C:\Program Files\...` binaries
- Personal emails, phone numbers, studio-only internal numbers
- Unpublished game IP, live table dumps, internal-only URLs
- Cloud credential dirs (`.aws/`, `.gcloud/`), `service-account*.json`, `.claude/settings.local.json`

Copy the labeled examples instead:

- `harness/mcp.json.example` and `.cursor/mcp.json.example` — `${PLACEHOLDER}` only (`${NODE}`, `${LARK_APP_ID}`, …)
- `harness/host-paths.example.json` — copy to a local `host-paths.json`
- `.env.example` — empty optional keys

`.gitignore` already ignores live `mcp.json`, `host-paths.json`, `.env`, key material, and local `.harness` session/artifact dumps. The shipped `studio/.harness/` scaffold (state, surfaces, canon) stays tracked.

## Secrets

- Secrets do not belong in git or in a Release asset.
- Setup never overwrites an existing `mcp.json`.
- Cursor `beforeReadFile` denies common secret paths (live `mcp.json`, `.env`, `*.pem`, credential filenames). Other tools do not get that gate — do not assume they do.
- `gsh verify` and `tests/test_no_secrets.py` share `gsh/secret_scan.py` (user paths, token prefixes, private-key armor, webhooks, non-example emails).
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
