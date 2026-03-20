from __future__ import annotations

import io
import json
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from pathlib import Path

from prumo_runtime.commands.config_apple_reminders import run_config_apple_reminders


class ConfigAppleRemindersTests(unittest.TestCase):
    def test_show_configuration_reports_all_when_observed_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            state_dir = workspace / "_state"
            state_dir.mkdir(parents=True, exist_ok=True)
            (state_dir / "workspace-schema.json").write_text(
                '{"user_name":"Batata","agent_name":"Prumo","timezone":"America/Sao_Paulo","briefing_time":"09:00"}',
                encoding="utf-8",
            )
            (state_dir / "apple-reminders-integration.json").write_text(
                '{"status":"connected","strategy":"eventkit-local","lists":["A vida...","Família"],"observed_lists":[]}',
                encoding="utf-8",
            )
            args = Namespace(workspace=str(workspace), observe_lists=None, all_lists=False)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                rc = run_config_apple_reminders(args)
            self.assertEqual(rc, 0)
            rendered = buffer.getvalue()
            self.assertIn("Listas observadas: todas", rendered)
            self.assertIn("A vida..., Família", rendered)

    def test_set_specific_lists(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            state_dir = workspace / "_state"
            state_dir.mkdir(parents=True, exist_ok=True)
            (state_dir / "workspace-schema.json").write_text(
                '{"user_name":"Batata","agent_name":"Prumo","timezone":"America/Sao_Paulo","briefing_time":"09:00"}',
                encoding="utf-8",
            )
            args = Namespace(workspace=str(workspace), observe_lists=["A vida...", "Família"], all_lists=False)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                rc = run_config_apple_reminders(args)
            self.assertEqual(rc, 0)
            payload = json.loads((state_dir / "apple-reminders-integration.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["observed_lists"], ["A vida...", "Família"])

    def test_clear_lists_with_all_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            state_dir = workspace / "_state"
            state_dir.mkdir(parents=True, exist_ok=True)
            (state_dir / "workspace-schema.json").write_text(
                '{"user_name":"Batata","agent_name":"Prumo","timezone":"America/Sao_Paulo","briefing_time":"09:00"}',
                encoding="utf-8",
            )
            (state_dir / "apple-reminders-integration.json").write_text(
                '{"status":"connected","strategy":"eventkit-local","lists":["A vida..."],"observed_lists":["A vida..."]}',
                encoding="utf-8",
            )
            args = Namespace(workspace=str(workspace), observe_lists=None, all_lists=True)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                rc = run_config_apple_reminders(args)
            self.assertEqual(rc, 0)
            payload = (state_dir / "apple-reminders-integration.json").read_text(encoding="utf-8")
            self.assertIn('"observed_lists": []', payload)


if __name__ == "__main__":
    unittest.main()
