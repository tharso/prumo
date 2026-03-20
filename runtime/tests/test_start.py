from __future__ import annotations

import io
import json
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from pathlib import Path

from prumo_runtime.commands.start import run_start


class StartCommandTests(unittest.TestCase):
    def test_missing_workspace_suggests_setup(self) -> None:
        missing = Path("/tmp/prumo-workspace-que-nao-existe")
        args = Namespace(workspace=str(missing), format="text")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            rc = run_start(args)
        self.assertEqual(rc, 0)
        rendered = buffer.getvalue()
        self.assertIn("Não achei o workspace", rendered)
        self.assertIn("prumo setup", rendered)

    def test_legacy_workspace_suggests_migrate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            (workspace / "CLAUDE.md").write_text("# legado\n", encoding="utf-8")
            args = Namespace(workspace=str(workspace), format="text")
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                rc = run_start(args)
            self.assertEqual(rc, 0)
            rendered = buffer.getvalue()
            self.assertIn("migrate", rendered)
            self.assertIn("workspace legado", rendered)

    def test_healthy_workspace_recommends_briefing_before_first_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            state_dir = workspace / "_state"
            state_dir.mkdir(parents=True, exist_ok=True)
            (workspace / "PAUTA.md").write_text(
                "# Pauta\n\n## Quente (precisa de atenção agora)\n\n- Ajuste urgente no site\n",
                encoding="utf-8",
            )
            (workspace / "AGENT.md").write_text("# AGENT\n", encoding="utf-8")
            (workspace / "PRUMO-CORE.md").write_text("> **prumo_version: 4.13.2**\n", encoding="utf-8")
            (state_dir / "workspace-schema.json").write_text(
                json.dumps(
                    {
                        "user_name": "Batata",
                        "agent_name": "Prumo",
                        "timezone": "America/Sao_Paulo",
                        "briefing_time": "09:00",
                        "files": {"generated": [], "authorial": [], "derived": []},
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "briefing-state.json").write_text('{"last_briefing_at": ""}', encoding="utf-8")
            (state_dir / "google-integration.json").write_text(
                '{"status":"connected","active_profile":"pessoal","profiles":{"pessoal":{"status":"connected","account_email":"tharso@gmail.com"}}}',
                encoding="utf-8",
            )
            (state_dir / "apple-reminders-integration.json").write_text(
                '{"status":"connected","authorization_status":"fullAccess","lists":["A vida..."],"observed_lists":["A vida..."]}',
                encoding="utf-8",
            )
            args = Namespace(workspace=str(workspace), format="text")
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                rc = run_start(args)
            self.assertEqual(rc, 0)
            rendered = buffer.getvalue()
            self.assertIn("Ainda não há briefing registrado hoje", rendered)
            self.assertIn("Rodar o briefing agora", rendered)
            self.assertIn("prumo briefing", rendered)

    def test_json_output_exposes_actions(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            state_dir = workspace / "_state"
            state_dir.mkdir(parents=True, exist_ok=True)
            (workspace / "AGENT.md").write_text("# AGENT\n", encoding="utf-8")
            (workspace / "PRUMO-CORE.md").write_text("> **prumo_version: 4.13.2**\n", encoding="utf-8")
            (workspace / "PAUTA.md").write_text("# Pauta\n\n## Em andamento\n\n- Projeto X\n", encoding="utf-8")
            (state_dir / "workspace-schema.json").write_text(
                json.dumps(
                    {
                        "user_name": "Batata",
                        "agent_name": "Prumo",
                        "timezone": "America/Sao_Paulo",
                        "briefing_time": "09:00",
                        "files": {"generated": [], "authorial": [], "derived": []},
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "briefing-state.json").write_text('{"last_briefing_at": ""}', encoding="utf-8")
            (state_dir / "google-integration.json").write_text("{}", encoding="utf-8")
            (state_dir / "apple-reminders-integration.json").write_text("{}", encoding="utf-8")
            args = Namespace(workspace=str(workspace), format="json")
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                rc = run_start(args)
            self.assertEqual(rc, 0)
            payload = json.loads(buffer.getvalue())
            self.assertEqual(payload["user_name"], "Batata")
            self.assertTrue(payload["actions"])
            self.assertEqual(payload["actions"][0]["id"], "briefing")


if __name__ == "__main__":
    unittest.main()
