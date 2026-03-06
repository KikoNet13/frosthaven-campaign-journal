from __future__ import annotations

import unittest
from typing import Iterator

import flet as ft

from frosthaven_campaign_journal.models import WeekSummary
from frosthaven_campaign_journal.ui.main_shell.state.shell_state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.view.center_panel import build_center_panel


def _build_state(*, selected_week: int | None) -> MainShellState:
    state = MainShellState()
    state.local_state.selected_year = 1
    state.local_state.selected_week = selected_week
    state.read_state.years = [1]
    state.read_state.weeks_by_year = {
        1: [
            WeekSummary(
                year_number=1,
                week_number=1,
                is_closed=False,
                status_label="open",
            )
        ]
    }
    return state


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
    return [item.value for item in _iter_controls(control) if isinstance(item, ft.Text)]


class MainShellCenterPanelTests(unittest.TestCase):
    def test_empty_state_without_selected_week_uses_plain_full_viewer_message(self) -> None:
        state = _build_state(selected_week=None)

        panel = build_center_panel(state.build_view_data(), state)

        self.assertIsInstance(panel.content, ft.Column)
        focus_wrapper = panel.content.controls[-1]
        self.assertIsInstance(focus_wrapper, ft.Container)
        self.assertTrue(focus_wrapper.expand)

        focus_control = focus_wrapper.content
        self.assertIsInstance(focus_control, ft.Container)
        self.assertTrue(focus_control.expand)
        self.assertIsInstance(focus_control.content, ft.Text)
        self.assertEqual("Selecciona una semana.", focus_control.content.value)

        text_values = _text_values(panel)
        self.assertIn("Selecciona una semana.", text_values)
        self.assertNotIn("Sin semana seleccionada", text_values)
        self.assertFalse(any(value.startswith("Navegación actual:") for value in text_values))

    def test_selected_week_without_entries_keeps_week_mode_card(self) -> None:
        state = _build_state(selected_week=1)

        panel = build_center_panel(state.build_view_data(), state)

        text_values = _text_values(panel)
        self.assertIn("Entradas de la semana", text_values)
        self.assertNotIn("Selecciona una semana.", text_values)


if __name__ == "__main__":
    unittest.main()
