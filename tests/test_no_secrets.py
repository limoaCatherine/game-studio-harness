# -*- coding: utf-8 -*-
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gsh.secret_scan import findings, scan_tree

EXAMPLE_LABEL = "EXAMPLE ONLY"
REQUIRED_GITIGNORE = (
    ".env",
    "!.env.example",
    "*.pem",
    "*.pfx",
    "*.p12",
    "credentials.json",
    "secrets.json",
    "mcp.json",
    "host-paths.json",
    "**/host-paths.json",
    "!**/host-paths.example.json",
    ".aws/",
    ".gcloud/",
    "**/service-account*.json",
    "**/.claude/settings.local.json",
    "**/.harness/sessions/",
    "**/.harness/artifacts/",
    "**/.harness/memory/tasks.jsonl",
)


class SecretScanTests(unittest.TestCase):
    def test_pack_has_no_secrets_or_studio_paths(self) -> None:
        self.assertEqual(scan_tree(ROOT), [])

    def test_mcp_example_uses_placeholders_and_is_labeled(self) -> None:
        for rel in ("harness/mcp.json.example", ".cursor/mcp.json.example"):
            example = ROOT / rel
            self.assertTrue(example.is_file(), rel)
            text = example.read_text(encoding="utf-8")
            self.assertIn(EXAMPLE_LABEL, text)
            data = json.loads(text)
            self.assertIn("$comment", data)
            self.assertIn("mcpServers", data)
            self.assertNotIn("Program Files", text)
            self.assertIn("${NODE}", text)
            if "-a" in text:
                self.assertIn("${LARK_APP_ID}", text)
                self.assertIn("${LARK_APP_SECRET}", text)

    def test_host_paths_example_is_labeled(self) -> None:
        path = ROOT / "harness" / "host-paths.example.json"
        text = path.read_text(encoding="utf-8")
        self.assertIn(EXAMPLE_LABEL, text)
        data = json.loads(text)
        self.assertNotIn("C:\\Users\\", text)
        self.assertNotIn("Program Files", text)
        self.assertEqual(findings(text), [])
        self.assertIn("hosts", data)

    def test_env_example_is_labeled_and_empty(self) -> None:
        path = ROOT / ".env.example"
        text = path.read_text(encoding="utf-8")
        self.assertIn(EXAMPLE_LABEL, text)
        self.assertIn("LARK_APP_ID=", text)
        self.assertNotIn("C:\\Users\\", text)
        self.assertEqual(findings(text), [])

    def test_gitignore_covers_secrets_and_local_harness(self) -> None:
        text = (ROOT / ".gitignore").read_text(encoding="utf-8")
        missing = [line for line in REQUIRED_GITIGNORE if line not in text]
        self.assertEqual(missing, [])

    def test_read_hook_denies_live_secrets_allows_examples(self) -> None:
        hook = ROOT / "hooks" / "读文件前.py"
        spec = importlib.util.spec_from_file_location("gsh_read_hook", hook)
        self.assertIsNotNone(spec)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        deny = ("id_rsa", "secret.pem", "token.p12", "mcp.json", ".env", "credentials.json", "host-paths.json")
        allow = ("mcp.json.example", ".env.example", "host-paths.example.json", "README.md")
        for name in deny:
            self.assertTrue(mod.DENY_NAME.search(name), name)
        for name in allow:
            self.assertIsNone(mod.DENY_NAME.search(Path(name).name), name)

    def test_scanner_catches_known_shapes(self) -> None:
        pem = "-----BEGIN " + "RSA PRIVATE KEY-----"
        hook = "https://hooks.slack.com/services/" + "T000/B000/xxx"
        mail = "reach studio@" + "not-example.test"
        self.assertIn("secret-like", findings("token ghp_" + ("a" * 36)))
        self.assertIn("private key", findings(pem))
        self.assertIn("webhook", findings(hook))
        self.assertTrue(any(k.startswith("email:") for k in findings(mail)))
        self.assertEqual(findings("contact ops@example.com"), [])
