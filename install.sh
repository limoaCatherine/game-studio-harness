#!/usr/bin/env bash
# Game Studio Harness — 一键入口。不装 DCC，不写密钥。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if command -v python3 >/dev/null 2>&1; then
  PY=python3
else
  PY=python
fi
ver="$($PY -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")')"
major="${ver%%.*}"
minor="${ver#*.}"
if [ "$major" -lt 3 ] || { [ "$major" -eq 3 ] && [ "$minor" -lt 11 ]; }; then
  echo "Need Python 3.11+, found $ver" >&2
  exit 2
fi
if [ $# -eq 0 ]; then
  exec "$PY" -m gsh setup --guided
fi
case "$1" in
  setup|sync|verify|doctor|uninstall)
    exec "$PY" -m gsh "$@"
    ;;
  *)
    exec "$PY" -m gsh setup "$@"
    ;;
esac
