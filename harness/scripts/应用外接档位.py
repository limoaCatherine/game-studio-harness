# -*- coding: utf-8 -*-
"""按 mcp-tiers.json 给非核心标准输入输出外接套懒接，并灌缓存。"""
from __future__ import annotations

import json
import os
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from gsh_paths import homes_from_env

    _h = homes_from_env()
    CURSOR = _h.cursor
    MCP_JSON = CURSOR / "mcp.json"
    TIERS = (
        _h.gsh_harness / "mcp-tiers.json"
        if (_h.gsh_harness / "mcp-tiers.json").is_file()
        else CURSOR / "harness" / "mcp-tiers.json"
    )
except Exception:
    CURSOR = Path.home() / ".cursor"
    MCP_JSON = CURSOR / "mcp.json"
    TIERS = CURSOR / "harness" / "mcp-tiers.json"
PY = Path(sys.executable)
TZ = timezone(timedelta(hours=8))


def boot_paths(tiers: dict) -> tuple[Path, Path]:
    boot = tiers.get("boot") or {}
    cache = Path(os.environ.get("HARNESS_MCP_CACHE") or boot.get("cache") or "")
    lazy = Path(os.environ.get("HARNESS_LAZY_STDIO") or boot.get("lazy_stdio") or "")
    return cache, lazy


def project_mcps_dirs() -> list[Path]:
    root = CURSOR / "projects"
    if not root.is_dir():
        return []
    return [p / "mcps" for p in root.iterdir() if (p / "mcps").is_dir()]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def already_wrapped(cfg: dict) -> bool:
    args = [str(x) for x in (cfg.get("args") or [])]
    joined = " ".join(args)
    return "lazy_stdio.py" in joined or "http_bridge.py" in joined


def seed_from_project(name: str) -> list[dict]:
    tools_dir = None
    for mcps in project_mcps_dirs():
        cand = mcps / f"user-{name}" / "tools"
        if cand.is_dir():
            tools_dir = cand
            break
    if tools_dir is None:
        return []
    rows = []
    for path in sorted(tools_dir.glob("*.json")):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rows.append(
            {
                "name": raw.get("name") or path.stem,
                "description": raw.get("description") or "",
                "inputSchema": raw.get("inputSchema") or raw.get("arguments") or {"type": "object"},
            }
        )
    return rows


def ensure_cache(name: str, cache: Path) -> Path:
    dest = cache / f"{name}.tools.json"
    if dest.is_file() and dest.stat().st_size > 2:
        return dest
    rows = seed_from_project(name)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest


def wrap(name: str, cfg: dict, framing: str, cache: Path, lazy: Path) -> dict:
    cache_file = ensure_cache(name, cache)
    cmd = cfg.get("command")
    args = list(cfg.get("args") or [])
    env = dict(cfg.get("env") or {})
    env.setdefault("PYTHONUNBUFFERED", "1")
    lazy_args = [str(lazy), "--name", name, "--cache", str(cache_file), "--framing", framing, "--", str(cmd), *args]
    out = {"command": str(PY), "args": lazy_args, "env": env}
    return out


def main() -> int:
    if not MCP_JSON.is_file() or not TIERS.is_file():
        print("missing mcp.json or mcp-tiers.json")
        return 2
    tiers = load(TIERS)
    cache, lazy = boot_paths(tiers)
    if not cache.as_posix() or not lazy.is_file():
        print("missing boot.cache / boot.lazy_stdio（mcp-tiers 或环境变量）")
        return 2
    core = set(tiers.get("core") or [])
    skip = set(tiers.get("already_lazy") or []) | set(tiers.get("url_passthrough") or [])
    framing_map = tiers.get("framing") or {}
    raw = load(MCP_JSON)
    servers = raw.get("mcpServers") or {}
    bak = MCP_JSON.with_suffix(".json.bak-" + datetime.now(TZ).strftime("%Y%m%d%H%M%S"))
    shutil.copy2(MCP_JSON, bak)
    changed = []
    for name, cfg in servers.items():
        if name in core or name in skip:
            continue
        if not cfg.get("command"):
            continue
        want = framing_map.get(name) or tiers.get("default_framing") or "ndjson"
        if already_wrapped(cfg):
            ensure_cache(name, cache)
            args = list(cfg.get("args") or [])
            if "--framing" in args:
                i = args.index("--framing")
                if i + 1 < len(args) and args[i + 1] != want:
                    args[i + 1] = want
                    cfg["args"] = args
                    changed.append(name + ":framing")
            continue
        servers[name] = wrap(name, cfg, want, cache, lazy)
        changed.append(name)
    raw["mcpServers"] = servers
    MCP_JSON.write_text(json.dumps(raw, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")
    print(f"backup {bak}")
    print(f"wrapped {len(changed)}: {', '.join(changed) if changed else '(none)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
