from __future__ import annotations

from concurrent.futures import Future
from datetime import datetime, timezone
import unittest
from unittest.mock import Mock, PropertyMock, patch

import flet as ft

from tests.main_shell_test_support import install_data_stub

install_data_stub()

from frosthaven_campaign_journal.ui.main_shell.view.session_timing import (
    SessionDurationText,
    build_active_session_subtitle,
    build_session_duration_text,
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

    def test_build_session_duration_text_returns_live_text_control(self) -> None:
        started = datetime(2026, 2, 9, 21, 41, 0, tzinfo=timezone.utc)
        ended = datetime(2026, 2, 10, 0, 5, 31, tzinfo=timezone.utc)

        control = build_session_duration_text(
            started_at_utc=started,
            ended_at_utc=ended,
            size=18,
            color="#ffffff",
        )

        self.assertIsInstance(control, SessionDurationText)
        self.assertIsInstance(control, ft.Text)
        self.assertEqual("02:24:31", control.value)
        self.assertEqual(18, control.size)
        self.assertFalse(control.is_isolated())


class SessionTimingTickerTests(unittest.TestCase):
    def test_live_session_starts_ticker_on_mount(self) -> None:
        control = SessionDurationText(
            started_at_utc=datetime(2026, 2, 9, 21, 41, 0, tzinfo=timezone.utc),
            size=18,
            color="#ffffff",
        )
        page = Mock()
        ticker_future = Mock(spec=Future)
        ticker_future.done.return_value = False
        page.run_task.return_value = ticker_future

        with patch.object(SessionDurationText, "page", new_callable=PropertyMock, return_value=page):
            control.did_mount()

        page.run_task.assert_called_once()
        self.assertIs(control._ticker_future, ticker_future)
        self.assertTrue(control._ticker_running)

    def test_finished_session_does_not_start_ticker_on_mount(self) -> None:
        control = SessionDurationText(
            started_at_utc=datetime(2026, 2, 9, 21, 41, 0, tzinfo=timezone.utc),
            ended_at_utc=datetime(2026, 2, 10, 0, 5, 31, tzinfo=timezone.utc),
            size=18,
            color="#ffffff",
        )

        with patch.object(control, "_is_attached_to_page", return_value=True):
            control.did_mount()

        self.assertIsNone(control._ticker_future)
        self.assertFalse(control._ticker_running)

    def test_migrate_state_restarts_ticker_for_live_session(self) -> None:
        started = datetime(2026, 2, 9, 21, 41, 0, tzinfo=timezone.utc)
        previous_control = SessionDurationText(
            started_at_utc=started,
            size=18,
            color="#ffffff",
        )
        previous_future = Mock(spec=Future)
        previous_future.done.return_value = False
        previous_control._ticker_future = previous_future
        previous_control._ticker_running = True

        migrated_control = SessionDurationText(
            started_at_utc=started,
            size=18,
            color="#ffffff",
        )
        page = Mock()
        new_future = Mock(spec=Future)
        new_future.done.return_value = False
        page.run_task.return_value = new_future

        with patch.object(SessionDurationText, "page", new_callable=PropertyMock, return_value=page):
            migrated_control._migrate_state(previous_control)
            migrated_control.before_update()

        previous_future.cancel.assert_called_once()
        page.run_task.assert_called_once()
        self.assertEqual(previous_control._i, migrated_control._i)
        self.assertFalse(previous_control._ticker_running)
        self.assertTrue(migrated_control._ticker_running)
        self.assertIs(migrated_control._ticker_future, new_future)


if __name__ == "__main__":
    unittest.main()
