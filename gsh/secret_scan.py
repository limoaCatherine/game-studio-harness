# -*- coding: utf-8 -*-
"""Shared secret / private-payload scanners for verify and unit tests."""
from __future__ import annotations

import re
from pathlib import Path

USER_PATH = re.compile(r"[A-Za-z]:\\Users\\(?!\$\{)[A-Za-z0-9._-]+")
POSIX_USER = re.compile(r"(?<![\w.-])/Users/(?!shared|Shared)[A-Za-z0-9._-]+")
DRIVE_HOST = re.compile(r"[A-Za-z]:\\Harness-Apps|[A-Za-z]:/Harness-Apps")
HARD_NODE = re.compile(r"nodejs\\\\node\.exe|nodejs\\node\.exe")
SECRET_A = re.compile(r'"-a",\s*"[A-Za-z0-9]{16,}"')
SECRET_LIKE = re.compile(
    r"\b(?:"
    r"ghp_[A-Za-z0-9]{20,}"
    r"|github_pat_[A-Za-z0-9_]{20,}"
    r"|sk-(?:proj-|ant-)?[A-Za-z0-9_\-]{16,}"
    r"|xox[baprs]-[A-Za-z0-9-]{16,}"
    r"|glpat-[A-Za-z0-9_\-]{16,}"
    r"|AKIA[0-9A-Z]{16}"
    r"|AIza[0-9A-Za-z_\-]{20,}"
    r")\b"
)
PRIVATE_KEY = re.compile(r"-----BEGIN (?:[A-Z0-9 ]+)?PRIVATE KEY-----")
WEBHOOK = re.compile(
    r"https://hooks\.slack\.com/services/[A-Za-z0-9/_-]+"
    r"|https://discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_-]+"
    r"|https://qyapi\.weixin\.qq\.com/cgi-bin/webhook/"
)
EMAIL = re.compile(r"(?<![/\\@])\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
EMAIL_ALLOW_DOMAINS = frozenset({"example.com", "example.org", "example.net", "invalid", "localhost"})

SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "node_modules",
    "dist",
    "build",
    ".ruff_cache",
    ".pytest_cache",
    "pack_data",
    ".egg-info",
}
SKIP_NAMES = frozenset({"catalog.json", "mcp.json"})
SCAN_SUFFIX = {
    ".md",
    ".json",
    ".py",
    ".mdc",
    ".example",
    ".yml",
    ".yaml",
    ".toml",
    ".txt",
    ".ps1",
    ".sh",
    ".bat",
    ".cfg",
    ".ini",
}


def _email_hits(text: str) -> list[str]:
    hits: list[str] = []
    for match in EMAIL.finditer(text):
        addr = match.group(0)
        domain = addr.rsplit("@", 1)[-1].lower()
        if domain in EMAIL_ALLOW_DOMAINS or domain.endswith(".example"):
            continue
        hits.append(addr)
    return hits


def findings(text: str) -> list[str]:
    """Return human-readable hit kinds for one file body."""
    out: list[str] = []
    if USER_PATH.search(text):
        out.append("user path")
    if POSIX_USER.search(text):
        out.append("posix user path")
    if DRIVE_HOST.search(text):
        out.append("host root")
    if HARD_NODE.search(text):
        out.append("hard-coded node host")
    if SECRET_A.search(text) or SECRET_LIKE.search(text):
        out.append("secret-like")
    if PRIVATE_KEY.search(text):
        out.append("private key")
    if WEBHOOK.search(text):
        out.append("webhook")
    emails = _email_hits(text)
    if emails:
        out.append("email:" + ",".join(emails))
    return out


def should_scan_file(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if not path.is_file():
        return False
    if path.name in SKIP_NAMES:
        return False
    if path.name == ".env.example":
        return True
    return path.suffix.lower() in SCAN_SUFFIX


def scan_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    return [f"{path} {kind}" for kind in findings(text)]


def scan_tree(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*"):
        if not should_scan_file(path):
            continue
        hits.extend(scan_file(path))
    return hits
