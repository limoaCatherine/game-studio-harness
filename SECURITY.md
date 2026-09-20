# Security

## Report

Use a GitHub private vulnerability report. Do not open a public issue for secrets or hook bypasses.

## Scope

This repository, the `gsh` CLI, hook scripts, and generated projections. Host DCC processes and third-party MCP servers that you install locally are **out of scope** for GSH itself.

## Secrets

- Secrets do not belong in git. `harness/mcp.json.example` uses `${PLACEHOLDER}` only.
- Setup never overwrites an existing `mcp.json`.
- Cursor `beforeReadFile` denies common secret paths. Other tools do not get that gate — do not assume they do.
- If a secret is committed: rotate it, then rewrite history. A revert commit is not enough.

## Supply chain

- Install only from this GitHub repository.
- Treat unofficial zips and mirrors as untrusted.
- This pack ships **zero** live MCP servers. A file under `harness/mcp-tools/` is a purpose stub.

## Isolate before real homedirs

```bash
python -m gsh setup --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --yes
python -m gsh verify --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws
```
