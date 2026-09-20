# Contributing

## Environment

Python 3.11+. From a clone:

```bash
python -m pip install -e ".[dev]"
gsh --version
```

Runtime has no third-party dependencies. `requirements.txt` is a pointer; `requirements-dev.txt` pins contributor tools.

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

Do **not** add `cursor/skills`, `claude/skills`, or `.cursor/skills`. Do **not** commit `gsh/pack_data/` — hatchling copies the root trees into the wheel at build time.

After you change the root:

```bash
gsh sync --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --yes
gsh verify --isolate-root /tmp/gsh-probe --workspace /tmp/gsh-probe/ws --tools all
gsh menu --kind craft -q ttk
python -m unittest discover -s tests -v
```

Optional: `ruff check gsh tests`.

A pull request that changes `gsh/` or pack layout should also survive `python -m build` and `pip install` of the wheel from an empty working directory (see `.github/workflows/ci.yml` job `pack`).

## Skills

Frontmatter must include `name` and `description`. Common hosts go in `needs_mcp` as catalog ids, not as invented names. Session numbers and machine paths stay out of the body.

## Crafts

`uses_skills` is a sequence. The roster generator must open only the first skill. Do not paste session TTK numbers into a craft file.

## MCP

Add a purpose stub under `harness/mcp-tools/<id>.json` and a placeholder block in `harness/mcp.json.example`. New hosts default to lazy. Do not commit a live server, a secret, or a Windows user-profile absolute path.

## Architecture

The four layers are frozen. Changing them requires a steer, a new loadplan, and an ADR under the studio filing cabinet — not a drive-by new top-level folder.

## Docs

Depth lives under `docs/`. README keeps the purpose → design philosophy → three framing notes (full pipeline / human–AI boundaries / capability curve) → inventory → department map → skill origin → problems → concepts → guides → platform → install order. Do not add decorative images; badges must be absolute shields.io URLs. Do not invent studio success percentages. Design crafts stay named (11 paths); do not collapse 策划 to combat plus economy.

Public docs are bilingual: [README.md](README.md) and [README.en.md](README.en.md). After adding a craft or skill, both department capability maps must mention the id (35/35 crafts, 106/106 skills). `python install/verify_readme_catalog.py` checks this.

## Releases

Maintainers cut versions per [docs/release.md](docs/release.md). Contributors do not push tags.

## Commit style

`feat:` / `fix:` / `docs:` / `chore:`.
