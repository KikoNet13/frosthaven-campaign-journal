from __future__ import annotations

from datetime import datetime, timezone
import unittest

from tests.main_shell_test_support import install_data_stub

install_data_stub()

from frosthaven_campaign_journal.ui.main_shell.view.session_timing import (
    build_active_session_subtitle,
    format_session_duration_hms,
    format_session_summary_date,
    format_session_summary_range,
)


class SessionTimingFormattingTests(unittest.TestCase):
    def test_format_session_duration_hms_uses_live_now_for_active_session(self) -> None:
        started = datetime(2026, 3, 6, 20, 0, 0, tzinfo=timezone.utc)
        now = datetime(2026, 3, 6, 22, 24, 31, tzinfo=timezone.utc)

        value = format_session_duration_hms(started_at_utc=started, now=now)

        self.assertEqual("02:24:31", value)

    def test_build_active_session_subtitle_includes_week_number(self) -> None:
        value = build_active_session_subtitle(
            entry_label="Escenario 12",
            week_number=7,
        )

        self.assertEqual("Escenario 12 · Semana 7", value)

    def test_build_active_session_subtitle_falls_back_when_label_missing(self) -> None:
        value = build_active_session_subtitle(
            entry_label=None,
            week_number=5,
        )

        self.assertEqual("Entrada activa · Semana 5", value)

    def test_format_session_summary_for_finished_session(self) -> None:
        started = datetime(2026, 2, 9, 21, 41, 0, tzinfo=timezone.utc)
        ended = datetime(2026, 2, 10, 0, 5, 31, tzinfo=timezone.utc)

        self.assertEqual("09/02/26", format_session_summary_date(started))
        self.assertEqual(
            f"{started.astimezone().strftime('%H:%M')} - {ended.astimezone().strftime('%H:%M')}",
            format_session_summary_range(
                started_at_utc=started,
                ended_at_utc=ended,
            ),
        )
        self.assertEqual(
            "02:24:31",
            format_session_duration_hms(
                started_at_utc=started,
                ended_at_utc=ended,
            ),
        )

    def test_format_session_summary_for_active_session(self) -> None:
        started = datetime(2026, 2, 9, 21, 41, 0, tzinfo=timezone.utc)
        now = datetime(2026, 2, 10, 0, 5, 31, tzinfo=timezone.utc)

        self.assertEqual(
            f"{started.astimezone().strftime('%H:%M')} - activa",
            format_session_summary_range(started_at_utc=started),
        )
        self.assertEqual(
            "02:24:31",
            format_session_duration_hms(started_at_utc=started, now=now),
        )


if __name__ == "__main__":
    unittest.main()
