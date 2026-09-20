# -*- coding: utf-8 -*-
"""兼容旧路径：python install/verify_install.py → gsh verify。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gsh.cli import main

if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv and argv[0] not in {"setup", "sync", "verify", "doctor", "uninstall"}:
        argv = ["verify", *argv]
    elif not argv:
        argv = ["verify"]
    raise SystemExit(main(argv))
