from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from prumo_runtime.commands.briefing import (
    choose_proposal,
    is_actionworthy_triage_item,
    load_snapshot_cache,
    resolve_snapshot_data,
    summarize_emails,
    write_snapshot_cache,
)


class BriefingSnapshotTests(unittest.TestCase):
    def test_write_and_load_snapshot_cache_preserves_notes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            snapshot = {
                "ok_profiles": 1,
                "profiles": {
                    "pessoal": {
                        "emails_total": 2,
                        "triage_reply": [],
                        "triage_view": ["P2 | 09:00 | Danilo | Assunto | preview"],
                        "triage_no_action": [],
                    }
                },
                "source": "google-direct-api",
                "note": "fonte direta respondeu bem",
                "email_note": "email veio direto da Gmail API",
            }
            write_snapshot_cache(workspace, "America/Sao_Paulo", snapshot)
            payload = load_snapshot_cache(workspace, "America/Sao_Paulo")
            self.assertIsNotNone(payload)
            assert payload is not None
            self.assertEqual(payload["source"], "google-direct-api")
            self.assertIn("fonte direta respondeu bem", payload["note"])
            self.assertEqual(payload["email_note"], "email veio direto da Gmail API")

    @patch("prumo_runtime.commands.briefing.write_snapshot_cache")
    @patch("prumo_runtime.commands.briefing.fetch_google_workspace_snapshot")
    @patch("prumo_runtime.commands.briefing.connected_google_profile", return_value="pessoal")
    def test_resolve_snapshot_data_prefers_direct_google_snapshot(
        self,
        _mock_profile,
        mock_direct_snapshot,
        mock_write_cache,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            mock_direct_snapshot.return_value = {
                "ok_profiles": 1,
                "profiles": {"pessoal": {"emails_total": 1}},
                "source": "google-direct-api",
                "note": "",
                "email_note": "direto",
            }
            payload = resolve_snapshot_data(workspace, repo_root=None, refresh_snapshot=True)
            self.assertEqual(payload["source"], "google-direct-api")
            self.assertEqual(payload["email_note"], "direto")
            self.assertIn("cached_at", payload)
            mock_write_cache.assert_called_once()

    @patch("prumo_runtime.commands.briefing.run_dual_snapshot")
    @patch("prumo_runtime.commands.briefing.fetch_google_workspace_snapshot", side_effect=RuntimeError("boom"))
    @patch("prumo_runtime.commands.briefing.connected_google_profile", return_value="pessoal")
    def test_resolve_snapshot_data_uses_cache_when_direct_api_fails(
        self,
        _mock_profile,
        _mock_direct_snapshot,
        mock_dual_snapshot,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            write_snapshot_cache(
                workspace,
                "America/Sao_Paulo",
                {
                    "ok_profiles": 1,
                    "profiles": {},
                    "source": "google-direct-api",
                    "note": "cache decente",
                    "email_note": "cache email",
                },
            )
            payload = resolve_snapshot_data(workspace, repo_root=None, refresh_snapshot=True)
            self.assertEqual(payload["status"], "cache")
            self.assertIn("Google API falhou (boom); usei cache.", payload["note"])
            mock_dual_snapshot.assert_not_called()

    @patch("prumo_runtime.commands.briefing.run_dual_snapshot")
    @patch("prumo_runtime.commands.briefing.fetch_google_workspace_snapshot", side_effect=RuntimeError("boom"))
    @patch("prumo_runtime.commands.briefing.connected_google_profile", return_value="pessoal")
    def test_resolve_snapshot_data_falls_back_to_dual_snapshot_without_cache(
        self,
        _mock_profile,
        _mock_direct_snapshot,
        mock_dual_snapshot,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            mock_dual_snapshot.return_value = {
                "ok_profiles": 1,
                "profiles": {"pessoal": {"emails_total": 1}},
                "note": "fallback ainda respirava.",
                "email_note": "dual",
                "source": "google-dual-snapshot",
            }
            payload = resolve_snapshot_data(workspace, repo_root=None, refresh_snapshot=True)
            self.assertEqual(payload["source"], "google-dual-snapshot")
            self.assertIn("Google API falhou (boom).", payload["note"])
            mock_dual_snapshot.assert_called_once()

    def test_summarize_emails_uses_email_note_for_empty_snapshot(self) -> None:
        rendered = summarize_emails(
            {
                "ok_profiles": 0,
                "profiles": {},
                "email_note": "email direto ainda nao entrou",
                "note": "sem cache",
            }
        )
        self.assertEqual(rendered, "email direto ainda nao entrou")

    def test_choose_proposal_ignores_low_signal_email_before_andamento(self) -> None:
        proposal = choose_proposal(
            [],
            [],
            ["Decidir abertura de empresa"],
            {
                "profiles": {
                    "pessoal": {
                        "triage_reply": [],
                        "triage_view": [
                            "P2 | 19:23 | Google Cloud | You have upgraded to a paid Google Cloud account | Explore full access"
                        ],
                    }
                }
            },
        )
        self.assertEqual(proposal, "Decidir abertura de empresa")

    def test_actionworthy_triage_item_accepts_p1_and_rejects_billing_noise(self) -> None:
        self.assertTrue(is_actionworthy_triage_item("P1 | 09:00 | Danilo | Ajuste urgente no site | revisar"))
        self.assertFalse(
            is_actionworthy_triage_item(
                "P2 | 19:23 | Google Cloud | You have upgraded to a paid Google Cloud account | Explore full access"
            )
        )


if __name__ == "__main__":
    unittest.main()
