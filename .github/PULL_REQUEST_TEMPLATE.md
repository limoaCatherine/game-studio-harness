## Summary

<!-- What production loop or pack/CLI path this changes. -->

## Checks

- [ ] `python -m unittest discover -s tests -v`
- [ ] `gsh verify --isolate-root <probe> --workspace <probe>/ws --tools all` (or the tools this PR touches)
- [ ] No secrets, live `mcp.json`, or user-profile absolute paths
- [ ] Skills/crafts/rules/hooks/harness edited only at repo root (no new `cursor/skills` trees)
- [ ] Docs stay capability-first; README order is purpose → design philosophy → three framing notes → inventory/map → skill origin → problems → … (install stays after platform). Design crafts stay named (11); do not collapse 策划 to combat plus economy.

## Packaging (if `gsh/`, pack trees, or `pyproject.toml` changed)

- [ ] `python -m build` succeeds
- [ ] Wheel `gsh setup` works from an empty working directory
