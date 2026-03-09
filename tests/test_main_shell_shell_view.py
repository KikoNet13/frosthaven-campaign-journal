from __future__ import annotations

import unittest

import flet as ft

from tests.main_shell_test_support import install_data_stub

install_data_stub()

from frosthaven_campaign_journal.models import WeekSummary
from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_WEEK_TILE_BG,
    COLOR_WEEK_TILE_SELECTED_BG,
)
from frosthaven_campaign_journal.ui.main_shell.state.shell_state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.view.shell_view import (
    _FAB_DOCK_MARGIN_BOTTOM,
    _FAB_DOCK_MARGIN_RIGHT,
    _FAB_TRIGGER_SIZE,
    build_main_shell_view,
)
from frosthaven_campaign_journal.ui.main_shell.view.temporal_bar import build_top_temporal_bar


def _iter_controls(control: ft.Control | None):
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


def _find_control_by_key(control: ft.Control, key: str) -> ft.Control | None:
    for item in _iter_controls(control):
        if getattr(item, "key", None) == key:
            return item
    return None


def _build_state(*, selected_week: int) -> MainShellState:
    state = MainShellState()
    state.notify = lambda: None
    state.local_state.selected_year = 1
    state.local_state.selected_week = selected_week
    state.read_state.years = [1]
    state.read_state.weeks_by_year = {
        1: [
            WeekSummary(year_number=1, week_number=1, is_closed=False, status_label="open"),
            WeekSummary(year_number=1, week_number=2, is_closed=False, status_label="open"),
        ]
    }
    return state


class MainShellShellViewTests(unittest.TestCase):
    def test_top_temporal_bar_marks_selected_week_tile_with_selected_color(self) -> None:
        state = _build_state(selected_week=2)

        temporal_bar = build_top_temporal_bar(state.build_view_data(), state)

        selected_tile = _find_control_by_key(temporal_bar, "week-2")
        unselected_tile = _find_control_by_key(temporal_bar, "week-1")

        self.assertIsNotNone(selected_tile)
        self.assertIsNotNone(unselected_tile)
        self.assertEqual(COLOR_WEEK_TILE_SELECTED_BG, selected_tile.bgcolor)
        self.assertEqual(COLOR_WEEK_TILE_BG, unselected_tile.bgcolor)

    def test_main_shell_view_uses_stack_layout_for_reactive_bars(self) -> None:
        state = _build_state(selected_week=2)

        shell_view = build_main_shell_view(state, data=state.build_view_data())
        fab_layer = _find_control_by_key(shell_view, "main-shell-fab-layer")

        self.assertIsInstance(shell_view, ft.Stack)
        self.assertFalse(any(isinstance(item, ft.Pagelet) for item in _iter_controls(shell_view)))
        self.assertIsNotNone(_find_control_by_key(shell_view, "main-shell-top-bar"))
        self.assertIsNotNone(_find_control_by_key(shell_view, "main-shell-center-panel"))
        self.assertIsNotNone(_find_control_by_key(shell_view, "main-shell-bottom-bar"))
        self.assertIsNotNone(fab_layer)
        assert isinstance(fab_layer, ft.Container)
        self.assertIsNone(fab_layer.expand)
        self.assertEqual(_FAB_TRIGGER_SIZE, fab_layer.width)
        self.assertEqual(_FAB_TRIGGER_SIZE, fab_layer.height)
        self.assertEqual(_FAB_DOCK_MARGIN_RIGHT, fab_layer.right)
        self.assertEqual(_FAB_DOCK_MARGIN_BOTTOM, fab_layer.bottom)


if __name__ == "__main__":
    unittest.main()
