from __future__ import annotations

import unittest
from typing import Iterator

import flet as ft

from tests.main_shell_test_support import install_data_stub

install_data_stub()

from frosthaven_campaign_journal.data import EntryWriteResult
from frosthaven_campaign_journal.models import EntryRef, EntrySummary, WeekSummary
from frosthaven_campaign_journal.ui.main_shell.state.shell_state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.state.types import (
    EntryFormState,
    EntryNotesEditorState,
    SessionFormState,
)
from frosthaven_campaign_journal.ui.main_shell.view.center_forms import (
    build_form_modal_overlay,
)


def _build_state(*, selected_week: int | None = 1) -> MainShellState:
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


def _build_entry(*, entry_id: str, label: str, notes: str | None = None) -> EntrySummary:
    return EntrySummary(
        ref=EntryRef(year_number=1, week_number=1, entry_id=entry_id),
        label=label,
        entry_type="scenario",
        scenario_ref=1,
        notes=notes,
        resource_deltas={},
    )


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


def _text_field_values(control: ft.Control) -> list[str]:
    return [item.value for item in _iter_controls(control) if isinstance(item, ft.TextField)]


def _tooltips(control: ft.Control) -> list[str]:
    values: list[str] = []
    for item in _iter_controls(control):
        tooltip = getattr(item, "tooltip", None)
        if isinstance(tooltip, str) and tooltip:
            values.append(tooltip)
    return values


class MainShellModalOverlayTests(unittest.TestCase):
    def test_build_form_modal_overlay_returns_none_without_active_form(self) -> None:
        state = _build_state()

        self.assertIsNone(build_form_modal_overlay(state.build_view_data(), state))

    def test_notes_modal_renders_loaded_value_and_close_action(self) -> None:
        state = _build_state()
        entry = _build_entry(entry_id="entry-1", label="Escenario 1", notes="Notas ya guardadas")
        state.entry_panel_state.entries_for_selected_week = [entry]

        state.on_open_entry_notes_editor(entry.ref)
        overlay = build_form_modal_overlay(state.build_view_data(), state)

        self.assertIsNotNone(overlay)
        assert overlay is not None
        self.assertIn("Editar notas de entry: Escenario 1", _text_values(overlay))
        self.assertIn("Notas ya guardadas", _text_field_values(overlay))
        self.assertIn("Cerrar diálogo", _tooltips(overlay))

        state.on_cancel_entry_notes_editor()
        self.assertIsNone(build_form_modal_overlay(state.build_view_data(), state))

    def test_only_one_modal_state_is_active_at_a_time_and_overlay_tracks_current_form(self) -> None:
        state = _build_state()
        entry = _build_entry(entry_id="entry-1", label="Escenario 1", notes="Notas")
        state.entry_panel_state.entries_for_selected_week = [entry]
        state.entry_panel_state.sessions_by_entry_ref = {entry.ref: []}

        state.on_open_entry_add_modal()
        overlay = build_form_modal_overlay(state.build_view_data(), state)
        self.assertIsNotNone(state.entry_form_state)
        self.assertIsNone(state.entry_notes_editor_state)
        self.assertIsNone(state.session_form_state)
        assert overlay is not None
        self.assertIn("Crear entrada", _text_values(overlay))

        state.on_open_entry_notes_editor(entry.ref)
        overlay = build_form_modal_overlay(state.build_view_data(), state)
        self.assertIsNone(state.entry_form_state)
        self.assertIsNotNone(state.entry_notes_editor_state)
        self.assertIsNone(state.session_form_state)
        assert overlay is not None
        self.assertIn("Editar notas de entry: Escenario 1", _text_values(overlay))

        state.on_open_manual_create_session_for_entry(entry.ref)
        overlay = build_form_modal_overlay(state.build_view_data(), state)
        self.assertIsNone(state.entry_form_state)
        self.assertIsNone(state.entry_notes_editor_state)
        self.assertIsNotNone(state.session_form_state)
        assert overlay is not None
        self.assertIn("Crear sesión manual", _text_values(overlay))

    def test_context_change_clears_active_modal_states(self) -> None:
        state = _build_state()
        entry = _build_entry(entry_id="entry-1", label="Escenario 1", notes="Notas")
        next_entry_ref = EntryRef(year_number=1, week_number=1, entry_id="entry-2")
        state.entry_form_state = EntryFormState(
            mode="edit",
            entry_type="scenario",
            scenario_ref_text="1",
        )
        state.entry_notes_editor_state = EntryNotesEditorState(
            entry_ref=entry.ref,
            entry_label=entry.label,
            notes_value="Notas",
        )
        state.session_form_state = SessionFormState(
            mode="create",
            entry_ref=entry.ref,
            session_id=None,
            started_date_local="2026-03-09",
            started_time_local="10:00",
            ended_date_local="",
            ended_time_local="",
            active_without_end=False,
        )
        state._run_or_confirm_resource_draft_before_context_change = lambda action, action_label: action()
        state._load_viewer_entry_and_sessions = lambda: None

        state.on_select_entry(next_entry_ref)

        self.assertEqual(next_entry_ref, state.local_state.viewer_entry_ref)
        self.assertIsNone(state.entry_form_state)
        self.assertIsNone(state.entry_notes_editor_state)
        self.assertIsNone(state.session_form_state)

    def test_delete_entry_clears_active_modal_states(self) -> None:
        state = _build_state()
        entry = _build_entry(entry_id="entry-1", label="Escenario 1", notes="Notas")
        state.local_state.viewer_entry_ref = entry.ref
        state.entry_form_state = EntryFormState(
            mode="edit",
            entry_type="scenario",
            scenario_ref_text="1",
        )
        state.entry_notes_editor_state = EntryNotesEditorState(
            entry_ref=entry.ref,
            entry_label=entry.label,
            notes_value="Notas",
        )
        state.session_form_state = SessionFormState(
            mode="edit",
            entry_ref=entry.ref,
            session_id="sess-1",
            started_date_local="2026-03-09",
            started_time_local="10:00",
            ended_date_local="2026-03-09",
            ended_time_local="11:00",
            active_without_end=False,
        )

        def _fake_run_entry_write(_action, **kwargs):
            before_refresh = kwargs.get("before_refresh")
            if before_refresh is not None:
                before_refresh(EntryWriteResult(entry_ref=entry.ref))
            return EntryWriteResult(entry_ref=entry.ref)

        state._run_entry_write = _fake_run_entry_write

        state._confirm_delete_entry(entry.ref)

        self.assertIsNone(state.entry_form_state)
        self.assertIsNone(state.entry_notes_editor_state)
        self.assertIsNone(state.session_form_state)


if __name__ == "__main__":
    unittest.main()
