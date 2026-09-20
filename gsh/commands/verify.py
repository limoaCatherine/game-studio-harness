# -*- coding: utf-8 -*-
"""验收：菜单、唯一 ID、职种不预展开、无密钥、投影一致、仓库无技能全树拷贝。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from gsh.adapters import SPEC_BY_ID, home_for
from gsh.catalog import build_catalog
from gsh.commands.setup import _homes
from gsh.paths_cli import resolve_pack
from gsh.profiles import parse_tools
from gsh.project import read_install_state

NEED_SKILLS = ("route-task", "write-isolation", "doctor", "verify-gate", "mcp-autostart")
NEED_HOOKS = ("开场.py", "结束.py", "工作区.py", "命令前.py", "读文件前.py")
NEED_SCRIPTS = (
    "刷新菜单.py",
    "生成会话能力名单.py",
    "项目库.py",
    "目录夹具.py",
    "接线自检.py",
    "应用外接档位.py",
    "拉起外接.py",
    "gsh_paths.py",
    "职种路径.py",
)
USER_PATH = re.compile(r"[A-Za-z]:\\Users\\(?!\$\{)[A-Za-z0-9._-]+")
DRIVE_HOST = re.compile(r"[A-Za-z]:\\Harness-Apps|[A-Za-z]:/Harness-Apps")
SECRET_A = re.compile(r'"-a",\s*"[A-Za-z0-9]{16,}"')
SECRET_LIKE = re.compile(r"\b(ghp_|github_pat_|sk-)[A-Za-z0-9_\-]{16,}")
BANNED_PACK_TREES = (
    "cursor/skills",
    "claude/skills",
    "codex/skills",
    "grok/skills",
    "deepseek/skills",
)


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def check_skill_tree(root: Path, errors: list[str], label: str) -> None:
    for sid in NEED_SKILLS:
        if not (root / sid / "SKILL.md").is_file():
            fail(errors, f"{label} missing skill {sid}")


def _scan_secrets(path: Path, errors: list[str]) -> None:
    if not path.exists():
        return
    files = [path] if path.is_file() else [p for p in path.rglob("*") if p.is_file()]
    for item in files:
        if item.suffix.lower() not in {".md", ".json", ".py", ".mdc", ".example", ".yml", ".yaml", ".toml", ".txt"}:
            continue
        if item.name in {"catalog.json", "mcp.json"}:
            continue
        if "pack_data" in item.parts:
            continue
        try:
            text = item.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if USER_PATH.search(text):
            fail(errors, f"{item.as_posix()} still has a machine user path")
        if DRIVE_HOST.search(text):
            fail(errors, f"{item.as_posix()} still has a hard-coded host root")
        if SECRET_A.search(text) or SECRET_LIKE.search(text):
            fail(errors, f"{item.as_posix()} still looks like a live secret")


def _assert_same_file(a: Path, b: Path, errors: list[str], label: str) -> None:
    if not a.is_file() or not b.is_file():
        fail(errors, f"{label}: missing {a} or {b}")
        return
    if a.read_bytes() != b.read_bytes():
        fail(errors, f"{label}: projection drifted {a} != {b}")


def _craft_not_preexpanded(h, pack: Path, errors: list[str]) -> None:
    catalog_path = h.gsh_harness / "catalog.json"
    if not catalog_path.is_file():
        fail(errors, "missing catalog.json；先跑 setup")
        return
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    craft = next((c for c in catalog.get("crafts") or [] if c.get("uses_skills")), None)
    if not craft:
        fail(errors, "catalog 没有任何带 uses_skills 的职种")
        return
    uses = list(craft["uses_skills"])
    if len(uses) < 2:
        return
    sys.path.insert(0, str(h.gsh_harness / "scripts"))
    from 生成会话能力名单 import catalog_alias_map, catalog_ids, uniq  # type: ignore

    ids = catalog_ids(catalog)
    aliases = catalog_alias_map(catalog)
    skills, crafts, mcps = [craft["id"]], [craft["id"]], []
    # 只点名职种，不把 uses_skills 预展开进 skills
    skills = []
    crafts = [craft["id"]]
    skill_rows = {x["id"]: x for x in catalog.get("skills") or []}
    craft_rows = {x["id"]: x for x in catalog.get("crafts") or []}
    craft_open = {}
    first = uses[0]
    craft_open[craft["id"]] = first
    if first in skills:
        fail(errors, "fixture error")
    if set(uses).issubset(set(skills)):
        fail(errors, "职种被预展开：uses_skills 全部进入了 skills")
    if craft_open[craft["id"]] != uses[0]:
        fail(errors, "craft_open 不是路径第一步")
    _ = (ids, aliases, uniq, skill_rows, craft_rows, mcps)


def run(
    *,
    workspace: Path | None,
    tools_raw: str,
    isolate: Path | None,
    cursor_only: bool,
    pack: Path | None,
) -> int:
    if not cursor_only and workspace is None:
        print("need --workspace or --cursor-only", file=sys.stderr)
        return 2

    pack_root = resolve_pack(pack)
    h = _homes(isolate)
    state = read_install_state(h)
    if state and state.get("tools") and tools_raw in {"all", "legacy"}:
        tools_raw = ",".join(state["tools"])
    try:
        tools = parse_tools(tools_raw)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    errors: list[str] = []

    # --- pack SSOT ---
    if not (pack_root / "skills" / "route-task" / "SKILL.md").is_file():
        fail(errors, "pack missing skills/route-task (SSOT)")
    if not (pack_root / "agents").is_dir():
        fail(errors, "pack missing agents/")
    if not (pack_root / "rules" / "全局.mdc").is_file():
        fail(errors, "pack missing rules/全局.mdc")
    if not (pack_root / "hooks" / "hooks.json").is_file():
        fail(errors, "pack missing hooks/hooks.json")
    for rel in BANNED_PACK_TREES:
        if (pack_root / rel / "route-task" / "SKILL.md").is_file():
            fail(errors, f"pack still has duplicated tree {rel} — SSOT is root skills/")
    if (pack_root / ".cursor" / "skills" / "route-task" / "SKILL.md").is_file():
        fail(errors, ".cursor/skills must not copy the SSOT skill tree")

    catalog = build_catalog(pack_root)
    skill_ids = [x["id"] for x in catalog["skills"]]
    craft_ids = [x["id"] for x in catalog["crafts"]]
    if len(skill_ids) != len(set(skill_ids)):
        fail(errors, "duplicate skill ids in pack")
    if len(craft_ids) != len(set(craft_ids)):
        fail(errors, "duplicate craft ids in pack")
    if len(skill_ids) < 50:
        fail(errors, f"pack skills too few: {len(skill_ids)}")
    if len(craft_ids) < 20:
        fail(errors, f"pack crafts too few: {len(craft_ids)}")
    if not any(c.get("uses_skills") for c in catalog["crafts"]):
        fail(errors, "no craft declares uses_skills")

    readme_catalog = pack_root / "install" / "verify_readme_catalog.py"
    if readme_catalog.is_file():
        install_dir = str(pack_root / "install")
        if install_dir not in sys.path:
            sys.path.insert(0, install_dir)
        import verify_readme_catalog

        if verify_readme_catalog.main() != 0:
            fail(errors, "README catalog coverage failed (install/verify_readme_catalog.py)")

    # --- installed shared runtime ---
    if not (h.gsh / "AGENTS.md").is_file():
        fail(errors, f"missing shared constitution {h.gsh / 'AGENTS.md'}")
    check_skill_tree(h.gsh_skills, errors, "gsh")
    if not list(h.gsh_agents.glob("*.md")):
        fail(errors, "missing crafts in shared ~/.gsh/agents")
    for name in NEED_SCRIPTS:
        if not (h.gsh_harness / "scripts" / name).is_file():
            fail(errors, f"missing script {name}")
    if not (h.gsh_harness / "mcp-boot" / "lazy_stdio.py").is_file():
        fail(errors, "missing mcp-boot/lazy_stdio.py")
    tiers = h.gsh_harness / "mcp-tiers.json"
    if not tiers.is_file():
        fail(errors, "missing mcp-tiers.json")
    else:
        data = json.loads(tiers.read_text(encoding="utf-8"))
        if "excelMCP" not in (data.get("core") or []):
            fail(errors, "mcp-tiers core 缺 excelMCP（档位键，不是声称服务器已配送）")

    installed_catalog = h.gsh_harness / "catalog.json"
    if not installed_catalog.is_file():
        fail(errors, "missing catalog.json；先跑 setup")
    else:
        data = json.loads(installed_catalog.read_text(encoding="utf-8"))
        skills = {x["id"] for x in data.get("skills") or []}
        for sid in NEED_SKILLS:
            if sid not in skills:
                fail(errors, f"catalog 缺 skill {sid}")
        if not any((x.get("uses_skills") or []) for x in data.get("crafts") or []):
            fail(errors, "catalog 没有任何带 uses_skills 的职种")

    _craft_not_preexpanded(h, pack_root, errors)

    if "cursor" in tools:
        l1 = h.cursor / "rules" / "全局.mdc"
        if not l1.is_file():
            fail(errors, f"missing {l1}")
        else:
            text = l1.read_text(encoding="utf-8")
            if "开场读序" not in text:
                fail(errors, "L1 未写开场读序")
            if "不预展开" not in text:
                fail(errors, "L1 未写不预展开")
        for name in NEED_HOOKS:
            if not (h.cursor / "hooks" / name).is_file():
                fail(errors, f"missing hook {name}")
        if not (h.cursor / "hooks.json").is_file():
            fail(errors, "missing hooks.json")
        _assert_same_file(
            pack_root / "skills" / "route-task" / "SKILL.md",
            h.cursor / "skills" / "route-task" / "SKILL.md",
            errors,
            "cursor projection",
        )
        _assert_same_file(
            h.gsh_skills / "route-task" / "SKILL.md",
            h.cursor / "skills" / "route-task" / "SKILL.md",
            errors,
            "cursor vs shared",
        )

    for tool_id in tools:
        spec = SPEC_BY_ID.get(tool_id)
        if spec is None:
            fail(errors, f"unknown tool {tool_id}")
            continue
        dest = home_for(h, spec)
        if not (dest / "gsh-capability.json").is_file():
            fail(errors, f"{tool_id} missing gsh-capability.json")
        else:
            cap = json.loads((dest / "gsh-capability.json").read_text(encoding="utf-8"))
            if cap.get("tool") != spec.id:
                fail(errors, f"{tool_id} capability tool mismatch")
            if cap.get("hooks") != spec.hooks:
                fail(errors, f"{tool_id} capability hooks mismatch")
        skill_rel = spec.skill_dirs[0] if spec.skill_dirs else "skills"
        check_skill_tree(dest / skill_rel, errors, f"{tool_id}/{skill_rel}")
        _assert_same_file(
            pack_root / "skills" / "route-task" / "SKILL.md",
            dest / skill_rel / "route-task" / "SKILL.md",
            errors,
            f"{tool_id} projection",
        )
        if spec.agent_dirs:
            agent_dir = dest / spec.agent_dirs[0]
            if not list(agent_dir.glob("*.md")):
                fail(errors, f"{tool_id} missing craft files under {agent_dir}")
        for entry in spec.entries:
            if not (dest / entry).is_file():
                fail(errors, f"{tool_id} missing native entry {entry}")
        if spec.rule_rel and not (dest / spec.rule_rel).is_file():
            fail(errors, f"{tool_id} missing native rule {spec.rule_rel}")
        if spec.hooks == "cursor":
            if not (dest / "hooks.json").is_file():
                fail(errors, f"{tool_id} missing hooks.json")
        elif spec.hooks == "claude":
            if not (dest / "settings.json").is_file():
                fail(errors, f"{tool_id} missing settings.json")
            if not (dest / "hooks" / "开场.py").is_file():
                fail(errors, f"{tool_id} missing hooks/开场.py")
            if not (dest / "HOOKS.md").is_file():
                fail(errors, f"{tool_id} missing HOOKS.md")
        else:
            if not (dest / "HOOKS.md").is_file():
                fail(errors, f"{tool_id} missing HOOKS.md")
        if spec.id == "continue" and not (dest / "config.yaml").is_file():
            fail(errors, "continue missing config.yaml")
        if spec.id == "aider" and not (dest / ".aider.conf.yml").is_file():
            fail(errors, "aider missing .aider.conf.yml")
        if spec.id == "opencode" and not (dest / "opencode.json").is_file():
            fail(errors, "opencode missing opencode.json")
        if spec.id == "roo" and not (dest / ".roomodes").is_file():
            fail(errors, "roo missing .roomodes")
        if spec.id == "copilot" and not (dest / "prompts" / "route-task.prompt.md").is_file():
            fail(errors, "copilot missing prompts/route-task.prompt.md")
        for extra in spec.extra_homes:
            extra_root = getattr(h, extra)
            check_skill_tree(extra_root, errors, f"{tool_id} extra {extra}")

    for rel in (
        "README.md",
        "README.en.md",
        "AGENTS.md",
        "SECURITY.md",
        "CONTRIBUTING.md",
        "skills",
        "agents",
        "rules",
        "hooks",
        "harness",
        "gsh",
        "docs/architecture",
        "docs/adapters",
        "docs/cookbook",
    ):
        _scan_secrets(pack_root / rel, errors)
    _scan_secrets(pack_root / "harness" / "mcp.json.example", errors)

    example = pack_root / "harness" / "mcp.json.example"
    if example.is_file():
        text = example.read_text(encoding="utf-8")
        if "-a" in text and "${LARK_APP_ID}" not in text:
            fail(errors, "mcp.json.example 的 -a 未换成占位符")

    if workspace is not None:
        root = Path(workspace)
        for rel in (
            ".harness/state.json",
            ".harness/surfaces.json",
            ".harness/memory/canon/四层运行口径.md",
            ".harness/memory/canon/四层封版.md",
            "AGENTS.md",
            "CLAUDE.md",
            "GEMINI.md",
            "CONVENTIONS.md",
            "QWEN.md",
            ".windsurfrules",
            ".rules",
            ".clinerules/gsh.md",
            ".roo/rules/gsh.md",
            ".roomodes",
            ".continue/config.yaml",
            ".aider.conf.yml",
            ".amazonq/rules/gsh.md",
            ".trae/rules/gsh.md",
            ".junie/guidelines.md",
            ".kimi-code/AGENTS.md",
            ".qwen/QWEN.md",
            ".opencode/opencode.json",
            ".claude/settings.json",
            ".github/copilot-instructions.md",
            ".cursor/hooks.json",
            ".cursor/rules/全局.mdc",
        ):
            if not (root / rel).is_file():
                fail(errors, f"workspace missing {rel}")

    if errors:
        for e in errors:
            print("error:", e, file=sys.stderr)
        return 2
    print(f"ok architecture verify skills={len(skill_ids)} crafts={len(craft_ids)} tools={','.join(tools)}")
    return 0
