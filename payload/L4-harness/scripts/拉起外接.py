# -*- coding: utf-8 -*-
"""按 mcp.json 探活；可自启的 HTTP/宿主在 Cursor 发现前拉起。"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

CURSOR = Path.home() / ".cursor"
MCP_JSON = CURSOR / "mcp.json"
HEALTH = CURSOR / "harness" / "mcp-health.json"
HOST_PATHS = Path(
    os.environ.get("HARNESS_HOST_PATHS")
    or (Path.home() / ".cursor" / "harness" / "host-paths.json")
)
GAMEDEV_EXE = Path(os.environ.get("GAMEDEV_MCP_EXE") or "")
TZ = timezone(timedelta(hours=8))

# 0 全过；1 有条目失败；2 配置不可读
EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 2


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def port_open(host: str, port: int, timeout: float = 0.25) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def process_running(name: str) -> bool:
    try:
        out = subprocess.check_output(
            ["tasklist", "/FI", f"IMAGENAME eq {name}", "/FO", "CSV", "/NH"],
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.CalledProcessError):
        return False
    return name.lower() in out.lower() and "No tasks" not in out and "没有运行" not in out


def spawn(cmd: list[str]) -> tuple[bool, str]:
    try:
        subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(Path(cmd[0]).parent) if Path(cmd[0]).parent.is_dir() else None,
        )
        return True, "started"
    except OSError as e:
        return False, str(e)


def host_exe(app: str) -> Path | None:
    if not HOST_PATHS.is_file():
        return None
    try:
        data = load_json(HOST_PATHS)
    except (OSError, json.JSONDecodeError):
        return None
    row = (data.get("hosts") or {}).get(app)
    if not isinstance(row, dict):
        return None
    exe = row.get("exe") or row.get("path")
    return Path(exe) if exe else None


def servers() -> dict[str, dict]:
    raw = load_json(MCP_JSON)
    return raw.get("mcpServers") or {}


def command_path(cfg: dict) -> Path | None:
    cmd = cfg.get("command")
    if not cmd:
        return None
    return Path(os.path.expandvars(str(cmd)))


def url_host_port(cfg: dict) -> tuple[str, int] | None:
    url = cfg.get("url")
    if not url:
        return None
    parsed = urlparse(str(url))
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return host, port


def ensure_gamedev() -> dict:
    rec = {"id": "gamedev-mcp", "kind": "http-or-stdio", "ok": False, "detail": ""}
    if port_open("127.0.0.1", 28080) or process_running("gamedev-mcp-server.exe"):
        rec["ok"] = True
        rec["detail"] = "already up"
        return rec
    if not GAMEDEV_EXE.is_file():
        rec["detail"] = f"missing {GAMEDEV_EXE}"
        return rec
    ok, detail = spawn([str(GAMEDEV_EXE), "--port=28080"])
    rec["ok"] = ok
    rec["detail"] = detail
    if ok:
        for _ in range(20):
            if port_open("127.0.0.1", 28080):
                rec["detail"] = "listening"
                return rec
            time.sleep(0.15)
        rec["detail"] = "started, port not yet open"
    return rec


def ensure_cascadeur() -> dict:
    rec = {"id": "cascadeur", "kind": "host", "ok": False, "detail": ""}
    if port_open("127.0.0.1", 8765) or process_running("cascadeur.exe"):
        rec["ok"] = True
        rec["detail"] = "already up"
        return rec
    rec["detail"] = "idle (do not auto-launch GUI)"
    rec["ok"] = True
    return rec


def check_stdio(name: str, cfg: dict) -> dict:
    rec = {"id": name, "kind": "stdio", "ok": False, "detail": ""}
    path = command_path(cfg)
    if path is None:
        rec["detail"] = "no command"
        return rec
    if path.is_file():
        rec["ok"] = True
        rec["detail"] = str(path)
        return rec
    found = shutil.which(str(path))
    if found:
        rec["ok"] = True
        rec["detail"] = found
        return rec
    rec["detail"] = f"missing {path}"
    return rec


def check_url(name: str, cfg: dict) -> dict:
    rec = {"id": name, "kind": "url", "ok": False, "detail": ""}
    hp = url_host_port(cfg)
    if hp is None:
        rec["detail"] = "no url"
        return rec
    host, port = hp
    rec["detail"] = f"{host}:{port}"
    if host not in {"127.0.0.1", "localhost", "::1"}:
        rec["ok"] = True
        rec["detail"] = f"remote {host}:{port}"
        return rec
    rec["ok"] = port_open(host, port)
    if not rec["ok"]:
        rec["detail"] += " not listening"
    return rec


def boot(no_host: bool) -> list[dict]:
    rows: list[dict] = []
    if not MCP_JSON.is_file():
        return [{"id": "mcp.json", "kind": "config", "ok": False, "detail": f"missing {MCP_JSON}"}]
    try:
        items = servers()
    except (OSError, json.JSONDecodeError) as e:
        return [{"id": "mcp.json", "kind": "config", "ok": False, "detail": str(e)}]

    for name, cfg in items.items():
        if cfg.get("url") and not cfg.get("command"):
            rows.append(check_url(name, cfg))
        elif cfg.get("command"):
            rows.append(check_stdio(name, cfg))
        else:
            rows.append({"id": name, "kind": "unknown", "ok": False, "detail": "no command/url"})

    extra = []
    gamedev_cfg = items.get("gamedev-mcp") or {}
    if gamedev_cfg.get("url") and not gamedev_cfg.get("command"):
        extra.append(ensure_gamedev())
    if not no_host:
        extra.append(ensure_cascadeur())
    # 去重：同 id 以 extra 覆盖探活结果
    by_id = {r["id"]: r for r in rows}
    for rec in extra:
        prev = by_id.get(rec["id"])
        if prev and prev.get("ok") and rec.get("ok"):
            continue
        if prev and prev.get("ok") and not rec.get("ok"):
            continue
        by_id[rec["id"]] = rec
    return list(by_id.values())


def write_health(rows: list[dict], mode: str) -> None:
    HEALTH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "ts": now_iso(),
        "mode": mode,
        "ok": all(r.get("ok") for r in rows),
        "rows": rows,
    }
    HEALTH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--boot", action="store_true", help="拉起可自启项")
    p.add_argument("--no-host", action="store_true", help="不拉 DCC 宿主，仅核命令/端口")
    p.add_argument("--check", action="store_true", help="只探活不拉起")
    args = p.parse_args(argv)
    if not MCP_JSON.is_file():
        print(f"missing {MCP_JSON}", file=sys.stderr)
        return EXIT_USAGE
    mode = "check" if args.check or not args.boot else ("boot-no-host" if args.no_host else "boot")
    if args.check or not args.boot:
        rows = []
        items = servers()
        for name, cfg in items.items():
            if cfg.get("command"):
                rows.append(check_stdio(name, cfg))
            elif cfg.get("url"):
                rows.append(check_url(name, cfg))
            else:
                rows.append({"id": name, "kind": "unknown", "ok": False, "detail": "no command/url"})
        # gamedev 命令文件也核
        if GAMEDEV_EXE.is_file():
            rows.append({"id": "gamedev-mcp-server.exe", "kind": "bin", "ok": True, "detail": str(GAMEDEV_EXE)})
        else:
            rows.append({"id": "gamedev-mcp-server.exe", "kind": "bin", "ok": False, "detail": f"missing {GAMEDEV_EXE}"})
    else:
        rows = boot(no_host=args.no_host)
    write_health(rows, mode)
    failed = [r for r in rows if not r.get("ok")]
    print(f"wrote {HEALTH} mode={mode} ok={len(rows) - len(failed)}/{len(rows)}")
    for r in failed:
        print(f"fail {r['id']}: {r.get('detail')}", file=sys.stderr)
    return EXIT_OK if not failed else EXIT_FAIL


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
