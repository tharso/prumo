from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from prumo_runtime.cli import main


class CliDefaultInvocationTests(unittest.TestCase):
    def test_prumo_without_subcommand_behaves_like_start_in_workspace(self) -> None:
        previous_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            state_dir = workspace / "_state"
            state_dir.mkdir(parents=True, exist_ok=True)
            (workspace / "AGENT.md").write_text("# AGENT\n", encoding="utf-8")
            (workspace / "PRUMO-CORE.md").write_text("> **prumo_version: 4.15.1**\n", encoding="utf-8")
            (workspace / "PAUTA.md").write_text("# Pauta\n", encoding="utf-8")
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
            os.chdir(workspace)
            try:
                buffer = io.StringIO()
                with redirect_stdout(buffer):
                    rc = main([])
            finally:
                os.chdir(previous_cwd)
        self.assertEqual(rc, 0)
        rendered = buffer.getvalue()
        self.assertIn("o Prumo está de pé no workspace", rendered)
        self.assertIn("Minha sugestão:", rendered)

    def test_prumo_without_subcommand_in_random_directory_explains_next_step(self) -> None:
        previous_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                buffer = io.StringIO()
                with redirect_stdout(buffer):
                    rc = main([])
            finally:
                os.chdir(previous_cwd)
        self.assertEqual(rc, 0)
        rendered = buffer.getvalue()
        self.assertIn("não parece workspace do Prumo", rendered)
        self.assertIn("prumo setup", rendered)
