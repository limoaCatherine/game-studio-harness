# -*- coding: utf-8 -*-
"""懒接：发现走缓存，第一次 tools/call 再拉真实进程。"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from framer import AutoFramer  # noqa: E402


class FixedFramer:
    def __init__(self, inp, out, mode: str):
        self.inp = inp
        self.out = out
        self.mode = mode
        self.lock = threading.Lock()

    def read(self) -> dict[str, Any] | None:
        if self.mode == "ndjson":
            line = self.inp.readline()
            if not line:
                return None
            text = line.decode("utf-8", errors="replace").lstrip("\ufeff").strip()
            if not text:
                return self.read()
            if text[0] != "{":
                return self.read()
            return json.loads(text)
        header = b""
        while True:
            ch = self.inp.read(1)
            if not ch:
                return None
            header += ch
            if header.endswith(b"\r\n\r\n"):
                break
            if len(header) > 65536:
                raise RuntimeError("header too large")
        length = 0
        for line in header.decode("ascii", errors="replace").split("\r\n"):
            if line.lower().startswith("content-length:"):
                length = int(line.split(":", 1)[1].strip())
        if length <= 0:
            return None
        body = self.inp.read(length)
        if not body:
            return None
        return json.loads(body.decode("utf-8"))

    def write(self, msg: dict[str, Any]) -> None:
        raw = json.dumps(msg, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        with self.lock:
            if self.mode == "lsp":
                self.out.write(f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii") + raw)
            else:
                self.out.write(raw + b"\n")
            self.out.flush()


def _ok(rid: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": rid, "result": result}


def _err(rid: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": message}}


def load_tools(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        return raw
    return list(raw.get("tools") or [])


def save_tools(path: Path, tools: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tools, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class Child:
    def __init__(self, cmd: list[str], env: dict[str, str], framing: str):
        self.cmd = cmd
        self.env = env
        self.framing = framing
        self.proc: subprocess.Popen | None = None
        self.io = None
        self.ready = threading.Event()
        self._pending: dict[Any, threading.Event] = {}
        self._results: dict[Any, dict[str, Any]] = {}
        self._next = 20000
        self._lock = threading.Lock()
        self.stderr_tail = ""

    def start(self) -> str | None:
        if self.ready.is_set() and self.proc and self.proc.poll() is None:
            return None
        self._kill()
        order = [self.framing]
        other = "lsp" if self.framing == "ndjson" else "ndjson"
        if other not in order:
            order.append(other)
        last = "child initialize failed"
        for mode in order:
            last = self._boot(mode)
            if last is None:
                self.framing = mode
                return None
            self._kill()
        return last

    def _boot(self, mode: str) -> str | None:
        try:
            self.proc = subprocess.Popen(
                self.cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self.env,
                bufsize=0,
            )
        except OSError as e:
            return str(e)
        if not self.proc.stdin or not self.proc.stdout:
            return "no stdio"
        self.stderr_tail = ""
        threading.Thread(target=self._drain_err, daemon=True).start()
        self.io = FixedFramer(self.proc.stdout, self.proc.stdin, mode)
        threading.Thread(target=self._pump, daemon=True).start()
        init = self.rpc(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "lazy-stdio", "version": "1"},
            },
            timeout=12.0,
        )
        if init and "result" in init:
            try:
                self.io.write({"jsonrpc": "2.0", "method": "notifications/initialized"})
            except Exception:
                pass
            self.ready.set()
            return None
        if self.proc.poll() is not None:
            return f"child exited {self.proc.returncode}: {self.stderr_tail[-240:]}"
        return f"child initialize timeout ({mode}): {self.stderr_tail[-240:]}"

    def _drain_err(self) -> None:
        if not self.proc or not self.proc.stderr:
            return
        chunks: list[str] = []
        try:
            while True:
                buf = self.proc.stderr.read(256)
                if not buf:
                    break
                chunks.append(buf.decode("utf-8", errors="replace"))
                self.stderr_tail = "".join(chunks)[-2000:]
        except Exception:
            return

    def _kill(self) -> None:
        self.ready.clear()
        self.io = None
        self._pending.clear()
        self._results.clear()
        if self.proc:
            try:
                self.proc.kill()
            except Exception:
                pass
        self.proc = None

    def _pump(self) -> None:
        io = self.io
        if io is None:
            return
        while True:
            try:
                msg = io.read()
            except Exception:
                break
            if msg is None:
                break
            rid = msg.get("id")
            if rid in self._pending:
                self._results[rid] = msg
                self._pending[rid].set()

    def _alloc(self) -> int:
        with self._lock:
            self._next += 1
            return self._next

    def rpc(self, method: str, params: dict[str, Any] | None, timeout: float) -> dict[str, Any] | None:
        if not self.io:
            return None
        rid = self._alloc()
        ev = threading.Event()
        self._pending[rid] = ev
        try:
            self.io.write({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}})
        except Exception:
            self._pending.pop(rid, None)
            return None
        if not ev.wait(timeout):
            self._pending.pop(rid, None)
            return None
        self._pending.pop(rid, None)
        return self._results.pop(rid, None)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--cache", required=True)
    p.add_argument("--framing", default="ndjson", choices=("lsp", "ndjson"))
    p.add_argument("--self-test", action="store_true")
    p.add_argument("child", nargs="*")
    args = p.parse_args(argv)
    cache = Path(args.cache)
    tools = load_tools(cache)
    if args.self_test:
        print(f"ok {args.name} cache={len(tools)} framing={args.framing}")
        return 0 if tools or cache.is_file() else 1
    if not args.child:
        print("missing child command after --", file=sys.stderr)
        return 2

    child = Child(args.child, os.environ.copy(), args.framing)
    client = AutoFramer(sys.stdin.buffer, sys.stdout.buffer, prefer="ndjson")

    def listed() -> list[dict[str, Any]]:
        rows = list(tools)
        if not any(t.get("name") == "_lazy_status" for t in rows):
            rows.append(
                {
                    "name": "_lazy_status",
                    "description": f"{args.name} lazy: real process starts on first tool call",
                    "inputSchema": {"type": "object", "properties": {}},
                }
            )
        return rows

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
                        "serverInfo": {"name": args.name, "version": "lazy-stdio"},
                    },
                )
            )
            continue
        if method == "notifications/initialized":
            continue
        if method == "tools/list":
            client.write(_ok(rid, {"tools": listed()}))
            continue
        if method == "tools/call":
            params = msg.get("params") or {}
            name = params.get("name") or ""
            if name == "_lazy_status":
                client.write(
                    _ok(
                        rid,
                        {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(
                                        {
                                            "server": args.name,
                                            "child": bool(child.proc and child.proc.poll() is None),
                                            "ready": child.ready.is_set(),
                                            "framing": child.framing,
                                            "cached": len(tools),
                                        },
                                        ensure_ascii=False,
                                    ),
                                }
                            ],
                            "isError": False,
                        },
                    )
                )
                continue
            err = child.start()
            if err:
                client.write(_err(rid, -32000, f"{args.name} start failed: {err}"))
                continue
            listed_msg = child.rpc("tools/list", {}, timeout=20.0)
            remote_tools = ((listed_msg or {}).get("result") or {}).get("tools")
            if remote_tools:
                tools[:] = list(remote_tools)
                save_tools(cache, tools)
            fwd = child.rpc("tools/call", params, timeout=60.0)
            if fwd and "result" in fwd:
                client.write(_ok(rid, fwd["result"]))
            elif fwd and "error" in fwd:
                client.write({"jsonrpc": "2.0", "id": rid, "error": fwd["error"]})
            else:
                client.write(_err(rid, -32000, f"{args.name} child call timeout"))
            continue
        if rid is not None:
            client.write(_err(rid, -32601, f"unknown method {method}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
