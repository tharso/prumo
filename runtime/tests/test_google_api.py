from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

from prumo_runtime.google_api import (
    compact_message_time,
    compact_sender,
    fetch_calendar_events,
    fetch_gmail_triage,
    format_event_time,
    gmail_since_query,
    header_map,
    is_actionable_subject,
    is_low_signal_sender,
)


class GoogleApiParsingTests(unittest.TestCase):
    def test_header_map_normalizes_names(self) -> None:
        payload = {
            "payload": {
                "headers": [
                    {"name": "Subject", "value": "Teste"},
                    {"name": "From", "value": "Batata <batata@example.com>"},
                ]
            }
        }
        self.assertEqual(
            header_map(payload),
            {"subject": "Teste", "from": "Batata <batata@example.com>"},
        )

    def test_compact_sender_prefers_display_name(self) -> None:
        self.assertEqual(compact_sender('"Batata" <batata@example.com>'), "Batata")
        self.assertEqual(compact_sender("batata@example.com"), "batata@example.com")

    def test_low_signal_sender_detects_newsletters(self) -> None:
        self.assertTrue(
            is_low_signal_sender(
                "News Bot <newsletter@example.com>",
                "Resumo semanal",
                {"list-id": "newsletter.example.com"},
            )
        )
        self.assertFalse(
            is_low_signal_sender(
                "Danilo <danilo@example.com>",
                "Ajuste urgente no site",
                {},
            )
        )

    def test_actionable_subject_detects_real_action_language(self) -> None:
        self.assertTrue(is_actionable_subject("Ajuste urgente no site", "precisa revisar hoje"))
        self.assertFalse(is_actionable_subject("You have upgraded to a paid Google Cloud account", "Explore full access"))

    def test_compact_message_time_uses_internal_date(self) -> None:
        detail = {"internalDate": "1768870800000", "payload": {"headers": []}}
        rendered = compact_message_time(detail, "America/Sao_Paulo")
        self.assertRegex(rendered, r"^\d{2}:\d{2}$")

    def test_compact_message_time_falls_back_to_date_header(self) -> None:
        detail = {
            "payload": {
                "headers": [
                    {"name": "Date", "value": "Thu, 19 Mar 2026 10:00:00 -0300"},
                ]
            }
        }
        self.assertEqual(compact_message_time(detail, "America/Sao_Paulo"), "10:00")

    def test_format_event_time_supports_datetime_and_all_day(self) -> None:
        timed_label, timed_dt = format_event_time(
            {
                "start": {"dateTime": "2026-03-19T10:00:00-03:00"},
                "end": {"dateTime": "2026-03-19T11:30:00-03:00"},
            },
            "America/Sao_Paulo",
        )
        self.assertEqual(timed_label, "10:00-11:30")
        self.assertEqual(timed_dt.hour, 10)

        all_day_label, _ = format_event_time(
            {"start": {"date": "2026-03-20"}},
            "America/Sao_Paulo",
        )
        self.assertEqual(all_day_label, "dia inteiro")

    @patch("prumo_runtime.google_api.google_api_get_json")
    def test_fetch_calendar_events_sorts_today_and_tomorrow(self, mock_get_json) -> None:
        tz = ZoneInfo("America/Sao_Paulo")
        today = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        mock_get_json.return_value = {
            "items": [
                {
                    "summary": "Jantar",
                    "start": {"dateTime": today.replace(hour=20).isoformat()},
                    "end": {"dateTime": today.replace(hour=22).isoformat()},
                },
                {
                    "summary": "Escola",
                    "start": {"dateTime": today.replace(hour=7).isoformat()},
                    "end": {"dateTime": today.replace(hour=7, minute=30).isoformat()},
                },
                {
                    "summary": "Exame",
                    "start": {"dateTime": tomorrow.replace(hour=9).isoformat()},
                    "end": {"dateTime": tomorrow.replace(hour=10).isoformat()},
                },
            ]
        }
        agenda_today, agenda_tomorrow = fetch_calendar_events("token", "America/Sao_Paulo", "pessoal")
        self.assertEqual(agenda_today[0], "07:00-07:30 | pessoal | Escola")
        self.assertEqual(agenda_today[1], "20:00-22:00 | pessoal | Jantar")
        self.assertEqual(agenda_tomorrow, ["09:00-10:00 | pessoal | Exame"])

    def test_gmail_since_query_uses_last_briefing_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            (workspace / "_state").mkdir(parents=True, exist_ok=True)
            (workspace / "_state" / "briefing-state.json").write_text(
                '{\n  "last_briefing_at": "2026-03-19T10:00:00-03:00"\n}\n',
                encoding="utf-8",
            )
            query = gmail_since_query(workspace, "America/Sao_Paulo")
            self.assertIn("after:", query)
            self.assertIn("in:inbox", query)

    @patch("prumo_runtime.google_api.google_api_get_json")
    def test_fetch_gmail_triage_classifies_message_signal(self, mock_get_json) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            (workspace / "_state").mkdir(parents=True, exist_ok=True)
            (workspace / "_state" / "briefing-state.json").write_text(
                '{\n  "last_briefing_at": ""\n}\n',
                encoding="utf-8",
            )

            def fake_get_json(url: str, access_token: str, timeout: int = 20) -> dict:
                if "format=metadata" not in url:
                    return {"messages": [{"id": "m1"}, {"id": "m2"}]}
                if "/m1?" in url:
                    return {
                        "internalDate": "1768870800000",
                        "snippet": "Confirmar ajuste no site",
                        "payload": {
                            "headers": [
                                {"name": "Subject", "value": "Ajuste urgente no site"},
                                {"name": "From", "value": "Danilo <danilo@example.com>"},
                                {"name": "Date", "value": "Thu, 19 Mar 2026 10:00:00 -0300"},
                            ]
                        },
                    }
                return {
                    "internalDate": "1768874400000",
                    "snippet": "Resumo semanal",
                    "payload": {
                        "headers": [
                            {"name": "Subject", "value": "Newsletter semanal"},
                            {"name": "From", "value": "News Bot <newsletter@example.com>"},
                            {"name": "Date", "value": "Thu, 19 Mar 2026 11:00:00 -0300"},
                            {"name": "List-Id", "value": "newsletter.example.com"},
                        ]
                    },
                }

            mock_get_json.side_effect = fake_get_json
            total, reply_items, view_items, no_action_items, email_note = fetch_gmail_triage(
                "token",
                workspace,
                "America/Sao_Paulo",
            )

            self.assertEqual(total, 2)
            self.assertEqual(reply_items, [])
            self.assertEqual(len(view_items), 1)
            self.assertEqual(len(no_action_items), 1)
            self.assertIn("Ajuste urgente no site", view_items[0])
            self.assertTrue(view_items[0].startswith("P1 |"))
            self.assertIn("Gmail API", email_note)


if __name__ == "__main__":
    unittest.main()
