# -*- coding: utf-8 -*-
"""兼容入口：把仓库根加入 sys.path 后转给 python -m gsh。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gsh.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
