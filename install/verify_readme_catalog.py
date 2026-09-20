# -*- coding: utf-8 -*-
"""Assert README.md and README.en.md mention every craft and skill id."""
from __future__ import annotations

import re
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
AGENTS = PACK / "agents"
SKILLS = PACK / "skills"
READMES = (PACK / "README.md", PACK / "README.en.md")


def catalog() -> tuple[set[str], set[str]]:
    agents = {p.stem for p in AGENTS.glob("*.md")}
    skills = {p.name for p in SKILLS.iterdir() if p.is_dir()}
    return agents, skills


def missing(text: str, ids: set[str]) -> list[str]:
    out = []
    for iid in sorted(ids):
        if f"`{iid}`" not in text and not re.search(
            rf"(?<![A-Za-z0-9_-]){re.escape(iid)}(?![A-Za-z0-9_-])", text
        ):
            out.append(iid)
    return out


def main() -> int:
    agents, skills = catalog()
    errors: list[str] = []
    if len(agents) != 35:
        errors.append(f"agent tree count {len(agents)} != 35")
    if len(skills) != 106:
        errors.append(f"skill tree count {len(skills)} != 106")
    for path in READMES:
        if not path.is_file():
            errors.append(f"missing {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        ma = missing(text, agents)
        ms = missing(text, skills)
        if ma:
            errors.append(f"{path.name} missing crafts: {', '.join(ma)}")
        if ms:
            errors.append(f"{path.name} missing skills: {', '.join(ms)}")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print(f"ok {len(agents)}/35 crafts, {len(skills)}/106 skills in README.md and README.en.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
