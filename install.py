# -*- coding: utf-8 -*-
"""把本包落到 ~/.cursor 与业务根。不安装任何软件，不写密钥。"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parent
PAYLOAD = PACK / "payload"


def copy_tree(src: Path, dst: Path, dry: bool, copied: list[str]) -> None:
    if not src.exists():
        return
    if src.is_file():
        if not dry:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        copied.append(f"{src.as_posix()} -> {dst.as_posix()}")
        return
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        if path.name == ".gitkeep":
            rel = path.relative_to(src)
            target = dst / rel.parent
            if not dry:
                target.mkdir(parents=True, exist_ok=True)
            continue
        rel = path.relative_to(src)
        target = dst / rel
        if not dry:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        copied.append(f"{path.as_posix()} -> {target.as_posix()}")


def merge_missing(src: Path, dst: Path, dry: bool, copied: list[str]) -> None:
    if not src.exists():
        return
    for path in src.rglob("*"):
        if path.is_dir() or path.name == ".gitkeep":
            if path.is_dir() and not dry:
                (dst / path.relative_to(src)).mkdir(parents=True, exist_ok=True)
            continue
        rel = path.relative_to(src)
        target = dst / rel
        if target.exists():
            continue
        if not dry:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        copied.append(f"new {path.as_posix()} -> {target.as_posix()}")


def write_tiers(cursor: Path, dry: bool) -> None:
    src = PAYLOAD / "L3-mcp" / "mcp-tiers.json"
    raw = json.loads(src.read_text(encoding="utf-8"))
    boot_dir = cursor / "harness" / "mcp-boot"
    raw["boot"] = {
        "cache": str(boot_dir / "cache"),
        "lazy_stdio": str(boot_dir / "lazy_stdio.py"),
    }
    dest = cursor / "harness" / "mcp-tiers.json"
    if not dry:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def maybe_write_mcp(cursor: Path, write_mcp: bool, dry: bool) -> str:
    example = PAYLOAD / "L3-mcp" / "mcp.json.example"
    dest_example = cursor / "mcp.json.example"
    if not dry:
        shutil.copy2(example, dest_example)
    live = cursor / "mcp.json"
    if live.is_file():
        return "kept existing mcp.json"
    if not write_mcp:
        return "wrote mcp.json.example only (pass --write-mcp to create empty-machine mcp.json)"
    if not dry:
        shutil.copy2(example, live)
    return "wrote mcp.json from example (no secrets, placeholders only)"


def refresh_catalog(cursor: Path, dry: bool) -> str:
    script = cursor / "harness" / "scripts" / "刷新菜单.py"
    if dry:
        return "dry-run skip 刷新菜单"
    if not script.is_file():
        return "missing 刷新菜单.py"
    import importlib.util

    spec = importlib.util.spec_from_file_location("harness_refresh_catalog", script)
    if spec is None or spec.loader is None:
        return "cannot load 刷新菜单.py"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.CURSOR = cursor
    mod.HARNESS = cursor / "harness"
    mod.SKILLS = cursor / "skills"
    mod.AGENTS = cursor / "agents"
    mod.MCP_JSON = cursor / "mcp.json"
    mod.TOOLS = cursor / "harness" / "mcp-tools"
    mod.OUT = cursor / "harness" / "catalog.json"
    rc = int(mod.main())
    if rc != 0:
        return f"刷新菜单 failed rc={rc}"
    out = cursor / "harness" / "catalog.json"
    if not out.is_file():
        return "刷新菜单 未写 catalog.json"
    return f"wrote {out}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--workspace", help="业务根（将放 .harness）")
    p.add_argument("--cursor-home", default=str(Path.home() / ".cursor"))
    p.add_argument("--cursor-only", action="store_true")
    p.add_argument("--write-mcp", action="store_true", help="仅当目标没有 mcp.json 时从示例创建")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if not PAYLOAD.is_dir():
        print("missing payload/; run from pack root after build", file=sys.stderr)
        return 2
    if not args.cursor_only and not args.workspace:
        print("need --workspace or --cursor-only", file=sys.stderr)
        return 2

    cursor = Path(args.cursor_home)
    copied: list[str] = []
    dry = args.dry_run

    copy_tree(PAYLOAD / "L1-rules", cursor / "rules", dry, copied)
    copy_tree(PAYLOAD / "L2-skills", cursor / "skills", dry, copied)
    copy_tree(PAYLOAD / "L2-crafts", cursor / "agents", dry, copied)
    copy_tree(PAYLOAD / "wiring" / "hooks", cursor / "hooks", dry, copied)
    copy_tree(PAYLOAD / "wiring" / "hooks.json", cursor / "hooks.json", dry, copied)
    copy_tree(PAYLOAD / "L4-harness" / "scripts", cursor / "harness" / "scripts", dry, copied)
    copy_tree(PAYLOAD / "L4-harness" / "surfaces.default.json", cursor / "harness" / "surfaces.default.json", dry, copied)
    copy_tree(PAYLOAD / "L3-mcp" / "mcp-tools", cursor / "harness" / "mcp-tools", dry, copied)
    copy_tree(PAYLOAD / "L3-mcp" / "MCP调度.md", cursor / "harness" / "docs" / "MCP调度.md", dry, copied)
    copy_tree(PAYLOAD / "L3-mcp" / "mcp-boot", cursor / "harness" / "mcp-boot", dry, copied)
    write_tiers(cursor, dry)
    mcp_msg = maybe_write_mcp(cursor, args.write_mcp, dry)
    catalog_msg = refresh_catalog(cursor, dry)

    ws_msg = "skipped workspace"
    if args.workspace:
        root = Path(args.workspace)
        if not dry:
            root.mkdir(parents=True, exist_ok=True)
        merge_missing(PAYLOAD / "workspace-scaffold" / ".harness", root / ".harness", dry, copied)
        ws_msg = f"scaffolded missing files under {root / '.harness'}"

    print(f"files={len(copied)}")
    print(mcp_msg)
    print(catalog_msg)
    print(ws_msg)
    if dry:
        for line in copied[:20]:
            print("dry", line)
        if len(copied) > 20:
            print(f"dry ... {len(copied) - 20} more")
        print("ok dry-run")
        return 0
    print("ok architecture files installed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
