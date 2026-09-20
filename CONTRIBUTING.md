# Contributing

## Single source of truth

Edit capability files **once**, at the repository root:

| Kind | Path |
|---|---|
| Skill | `skills/<id>/SKILL.md` |
| Craft | `agents/<id>.md` |
| Rule | `rules/*.mdc` |
| Hook | `hooks/` |
| Runtime | `harness/` |
| CLI | `gsh/` |

Do **not** add `cursor/skills`, `claude/skills`, or `.cursor/skills`. After you change the root, run:

```bash
python -m gsh sync --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --yes
python -m gsh verify --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --tools all
python -m unittest discover -s tests -v
```

## Skills

Frontmatter must include `name` and `description`. Common hosts go in `needs_mcp` as catalog ids, not as invented names. Session numbers and machine paths stay out of the body.

## Crafts

`uses_skills` is a sequence. The roster generator must open only the first skill. Do not paste session TTK numbers into a craft file.

## MCP

Add a purpose stub under `harness/mcp-tools/<id>.json` and a placeholder block in `harness/mcp.json.example`. New hosts default to lazy. Do not commit a live server, a secret, or a Windows user-profile absolute path.

## Architecture

The four layers are frozen. Changing them requires a steer, a new loadplan, and an ADR under the studio filing cabinet — not a drive-by new top-level folder.

## Commit style

`feat:` / `fix:` / `docs:` / `chore:`.
