# -*- coding: utf-8 -*-
"""stdio 自动认帧：首字节 { 走换行 JSON，否则走 Content-Length。"""
from __future__ import annotations

import json
import threading
from typing import Any


class AutoFramer:
    def __init__(self, inp, out, prefer: str = "ndjson"):
        self.inp = inp
        self.out = out
        self.prefer = prefer
        self.mode: str | None = None
        self.lock = threading.Lock()

    def read(self) -> dict[str, Any] | None:
        ch = self.inp.read(1)
        if not ch:
            return None
        while ch in b" \t\r\n":
            ch = self.inp.read(1)
            if not ch:
                return None
        if ch == b"{":
            self.mode = "ndjson"
            rest = self.inp.readline()
            text = (ch + rest).decode("utf-8", errors="replace").lstrip("\ufeff").strip()
            if not text:
                return self.read()
            return json.loads(text)
        header = ch
        while True:
            nxt = self.inp.read(1)
            if not nxt:
                return None
            header += nxt
            if header.endswith(b"\r\n\r\n"):
                break
            if len(header) > 65536:
                raise RuntimeError("header too large")
        self.mode = "lsp"
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
        mode = self.mode or self.prefer
        with self.lock:
            if mode == "lsp":
                self.out.write(f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii") + raw)
            else:
                self.out.write(raw + b"\n")
            self.out.flush()
