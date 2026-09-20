# -*- coding: utf-8 -*-
"""stdio MCP 桥：立刻握手并回缓存工具，后台拉 HTTP 宿主。"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from framer import AutoFramer  # noqa: E402


def _ok(rid: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": rid, "result": result}


def _err(rid: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": message}}


def _port_open(host: str, port: int, timeout: float = 0.25) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _load_tools(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        return raw
    return list(raw.get("tools") or [])


def _http_rpc(url: str, payload: dict[str, Any], timeout: float = 20.0) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read()
    text = body.decode("utf-8", errors="replace")
    if text.startswith("event:") or "data:" in text[:32]:
        chunks = []
        for line in text.splitlines():
            if line.startswith("data:"):
                chunks.append(line[5:].strip())
        text = "".join(chunks)
    return json.loads(text)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--tools", required=True)
    p.add_argument("--launch", action="append", default=[])
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    tools = _load_tools(Path(args.tools))
    if args.self_test:
        if not tools:
            print("empty tools cache", file=sys.stderr)
            return 1
        print(f"ok {args.name} tools={len(tools)}")
        return 0

    parsed = urlparse(args.url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    launched = False

    def ensure_host() -> None:
        nonlocal launched
        if _port_open(host, port):
            return
        if launched or not args.launch:
            return
        launched = True
        try:
            subprocess.Popen(
                args.launch,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            launched = False

    threading.Thread(target=ensure_host, daemon=True).start()
    client = AutoFramer(sys.stdin.buffer, sys.stdout.buffer, prefer="ndjson")
    while True:
        try:
            msg = client.read()
        except Exception:
            break
        if msg is None:
            break
        method = msg.get("method")
        rid = msg.get("id")
        if method == "initialize":
            client.write(
                _ok(
                    rid,
                    {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": args.name, "version": "http-bridge"},
                    },
                )
            )
            continue
        if method == "notifications/initialized":
            continue
        if method == "tools/list":
            client.write(_ok(rid, {"tools": tools}))
            continue
        if method == "tools/call":
            ensure_host()
            if not _port_open(host, port, timeout=0.4):
                client.write(
                    _ok(
                        rid,
                        {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"{args.name} host not listening on {host}:{port}",
                                }
                            ],
                            "isError": True,
                        },
                    )
                )
                continue
            try:
                remote = _http_rpc(args.url, msg)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as e:
                client.write(_err(rid, -32000, f"{args.name} HTTP: {e}"))
                continue
            if "result" in remote:
                client.write(_ok(rid, remote["result"]))
            elif "error" in remote:
                client.write({"jsonrpc": "2.0", "id": rid, "error": remote["error"]})
            else:
                client.write(_err(rid, -32000, f"{args.name} empty HTTP result"))
            continue
        if rid is not None:
            client.write(_err(rid, -32601, f"unknown method {method}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
