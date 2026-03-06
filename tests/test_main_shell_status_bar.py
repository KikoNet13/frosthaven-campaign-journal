from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterator
import unittest

import flet as ft

from tests.main_shell_test_support import install_data_stub

install_data_stub()

from frosthaven_campaign_journal.models import EntryRef
from frosthaven_campaign_journal.ui.main_shell.state.shell_state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.view.status_bar import build_status_bar


def _iter_controls(control: ft.Control | None) -> Iterator[ft.Control]:
    if control is None:
        return

    yield control

    content = getattr(control, "content", None)
    if isinstance(content, ft.Control):
        yield from _iter_controls(content)

    controls = getattr(control, "controls", None)
    if controls is not None:
        for child in controls:
            yield from _iter_controls(child)


def _text_values(control: ft.Control) -> list[str]:
    values: list[str] = []
    for item in _iter_controls(control):
        if isinstance(item, ft.Text):
            values.append(item.value)
    return values


class MainShellStatusBarTests(unittest.TestCase):
    def test_status_bar_shows_active_session_subtitle_when_global_session_exists(self) -> None:
        state = MainShellState()
        state.read_state.active_entry_ref = EntryRef(year_number=1, week_number=6, entry_id="entry-1")
        state.read_state.active_entry_label = "Escenario 12"
        state.read_state.active_session_started_at_utc = datetime.now(timezone.utc) - timedelta(hours=1)

        status_bar = build_status_bar(state.build_view_data())

        self.assertIn("Escenario 12 · Semana 6", _text_values(status_bar))

    def test_status_bar_hides_active_session_box_without_active_session(self) -> None:
        state = MainShellState()

        status_bar = build_status_bar(state.build_view_data())

        self.assertNotIn("Entrada activa", " ".join(_text_values(status_bar)))


if __name__ == "__main__":
    unittest.main()
