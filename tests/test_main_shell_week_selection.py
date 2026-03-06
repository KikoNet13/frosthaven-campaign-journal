from __future__ import annotations

from types import SimpleNamespace
import unittest

from tests.main_shell_test_support import install_data_stub

install_data_stub()

from frosthaven_campaign_journal.models import WeekSummary
from frosthaven_campaign_journal.ui.main_shell.state.shell_state import MainShellState


def _build_control_event_with_data(payload: object) -> SimpleNamespace:
    control = SimpleNamespace(data=payload)
    return SimpleNamespace(control=control)


class MainShellWeekSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = MainShellState()
        self.state.notify = lambda: None
        self.state._load_entries_for_selected_week = lambda: None
        self.state.local_state.selected_year = 1
        self.state.read_state.weeks_by_year = {
            1: [
                WeekSummary(
                    year_number=1,
                    week_number=1,
                    is_closed=False,
                    status_label="open",
                )
            ]
        }

    def test_select_week_click_accepts_int_payload(self) -> None:
        self.state.local_state.selected_week = None

        self.state.on_select_week_click(_build_control_event_with_data(1))

        self.assertEqual(self.state.local_state.selected_week, 1)

    def test_select_week_click_accepts_numeric_string_payload(self) -> None:
        self.state.local_state.selected_week = None

        self.state.on_select_week_click(_build_control_event_with_data("1"))

        self.assertEqual(self.state.local_state.selected_week, 1)

    def test_select_week_click_ignores_invalid_payload(self) -> None:
        self.state.local_state.selected_week = None

        self.state.on_select_week_click(_build_control_event_with_data("week-1"))

        self.assertIsNone(self.state.local_state.selected_week)


if __name__ == "__main__":
    unittest.main()