#!/usr/bin/env python3
"""读文件进模型前：挡常见密钥路径。"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

DENY_NAME = re.compile(
    r"("
    r"^\.env$"
    r"|^\.env\.(?!example$)"
    r"|^mcp\.json$"
    r"|credentials\.json"
    r"|secrets?\.json"
    r"|id_rsa"
    r"|id_ed25519"
    r"|id_ecdsa"
    r"|\.pem$"
    r"|\.pfx$"
    r"|\.p12$"
    r"|appsettings\..*secrets"
    r")",
    re.I,
)
DENY_PART = re.compile(r"[\\/]\.ssh[\\/]|[\\/]\.aws[\\/]|[\\/]\.gnupg[\\/]", re.I)

def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({"permission": "allow"}))
        return
    path = payload.get("file_path") or ""
    name = Path(path).name
    if DENY_NAME.search(name) or DENY_PART.search(path.replace("/", "\\")):
        msg = f"密钥类文件留在密钥管理处：{name}"
        print(json.dumps({
            "permission": "deny",
            "user_message": msg,
            "agent_message": msg,
        }, ensure_ascii=False))
        return
    print(json.dumps({"permission": "allow"}))

if __name__ == "__main__":
    main()
