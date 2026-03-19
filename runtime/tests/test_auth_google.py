from __future__ import annotations

import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from prumo_runtime.commands.auth_google import resolve_client_config
from prumo_runtime.workspace import WorkspaceError


class AuthGoogleTests(unittest.TestCase):
    def test_resolve_client_config_accepts_inline_credentials(self) -> None:
        args = Namespace(
            client_id="client-id.apps.googleusercontent.com",
            client_secret="secret-value",
            project_id="prumo-local",
            auth_uri=None,
            token_uri=None,
            client_secrets=None,
        )
        payload = resolve_client_config(args)
        self.assertEqual(payload["client_id"], "client-id.apps.googleusercontent.com")
        self.assertEqual(payload["client_secret"], "secret-value")
        self.assertEqual(payload["project_id"], "prumo-local")
        self.assertEqual(payload["source_path"], "inline-flags")

    def test_resolve_client_config_rejects_lonely_client_id(self) -> None:
        args = Namespace(
            client_id="client-id.apps.googleusercontent.com",
            client_secret=None,
            project_id=None,
            auth_uri=None,
            token_uri=None,
            client_secrets=None,
        )
        with self.assertRaises(WorkspaceError):
            resolve_client_config(args)

    def test_resolve_client_config_loads_json_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "client_secret.json"
            path.write_text(
                json.dumps(
                    {
                        "installed": {
                            "client_id": "file-client-id.apps.googleusercontent.com",
                            "client_secret": "file-secret",
                            "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "project_id": "prumo-local",
                        }
                    }
                ),
                encoding="utf-8",
            )
            args = Namespace(
                client_id=None,
                client_secret=None,
                project_id=None,
                auth_uri=None,
                token_uri=None,
                client_secrets=str(path),
            )
            payload = resolve_client_config(args)
            self.assertEqual(payload["client_id"], "file-client-id.apps.googleusercontent.com")
            self.assertEqual(payload["client_secret"], "file-secret")
            self.assertEqual(payload["source_path"], str(path.resolve()))


if __name__ == "__main__":
    unittest.main()
