from __future__ import annotations

from datetime import datetime, timedelta, timezone
import unittest
from typing import Iterator

import flet as ft

from tests.main_shell_test_support import install_data_stub

install_data_stub()

from frosthaven_campaign_journal.models import (
    EntryRef,
    EntrySummary,
    ViewerSessionItem,
    WeekSummary,
)
from frosthaven_campaign_journal.ui.common.resources.resource_delta_row import (
    ResourceDeltaRow,
)
from frosthaven_campaign_journal.ui.main_shell.state.shell_state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.view.center_panel import (
    build_center_panel,
)


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


def _set_single_entry_resources(
    state: MainShellState,
    *,
    persisted_resource_deltas: dict[str, int],
    campaign_resource_totals: dict[str, int] | None,
    draft_resource_deltas: dict[str, int] | None = None,
) -> EntryRef:
    entry_ref = EntryRef(year_number=1, week_number=1, entry_id="entry-1")
    state.entry_panel_state.entries_for_selected_week = [
        EntrySummary(
            ref=entry_ref,
            label="Entrada 1",
            entry_type="scenario",
            resource_deltas=dict(persisted_resource_deltas),
        )
    ]
    state.read_state.campaign_resource_totals = (
        None if campaign_resource_totals is None else dict(campaign_resource_totals)
    )
    if draft_resource_deltas is not None:
        state.entry_panel_state.resource_draft_by_entry_ref[entry_ref] = dict(
            draft_resource_deltas
        )
    return entry_ref


def _build_entry(*, entry_id: str, label: str) -> EntrySummary:
    return EntrySummary(
        ref=EntryRef(year_number=1, week_number=1, entry_id=entry_id),
        label=label,
        entry_type="scenario",
        scenario_ref=1,
        resource_deltas={},
    )


def _build_session(*, session_id: str, active: bool) -> ViewerSessionItem:
    started = datetime.now(timezone.utc) - timedelta(hours=2, minutes=24, seconds=31)
    ended = None if active else started + timedelta(hours=2, minutes=24, seconds=31)
    return ViewerSessionItem(
        session_id=session_id,
        started_at_utc=started,
        ended_at_utc=ended,
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


def _button_labels(control: ft.Control) -> list[str]:
    labels: list[str] = []
    for item in _iter_controls(control):
        content = getattr(item, "content", None)
        if isinstance(content, str):
            labels.append(content)
    return labels


def _tooltips(control: ft.Control) -> list[str]:
    tooltips: list[str] = []
    for item in _iter_controls(control):
        tooltip = getattr(item, "tooltip", None)
        if isinstance(tooltip, str) and tooltip:
            tooltips.append(tooltip)
    return tooltips


def _find_resource_row(control: ft.Control, *, resource_key: str) -> ResourceDeltaRow:
    for item in _iter_controls(control):
        if isinstance(item, ResourceDeltaRow) and item.resource_key == resource_key:
            if not item.controls:
                item.init()
            return item
    raise AssertionError(
        f"No se encontro ResourceDeltaRow para resource_key={resource_key!r}."
    )


def _find_projected_total_text(row: ResourceDeltaRow) -> str:
    for value in _text_values(row):
        if value.startswith("(") and value.endswith(")"):
            return value
    raise AssertionError(
        f"No se encontro texto de total proyectado en la fila {row.resource_key!r}."
    )


class MainShellCenterPanelTests(unittest.TestCase):
    def test_empty_state_without_selected_week_uses_plain_full_viewer_message(
        self,
    ) -> None:
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
        self.assertEqual("Selecciona una semana", focus_control.content.value)

        text_values = _text_values(panel)
        self.assertIn("Selecciona una semana", text_values)
        self.assertNotIn("Sin semana seleccionada", text_values)
        self.assertFalse(
            any(value.startswith("Navegaci\u00f3n actual:") for value in text_values)
        )

    def test_selected_week_without_entries_keeps_week_mode_card(self) -> None:
        state = _build_state(selected_week=1)

        panel = build_center_panel(state.build_view_data(), state)

        text_values = _text_values(panel)
        self.assertIn("Entradas de la semana", text_values)
        self.assertNotIn("Selecciona una semana", text_values)

    def test_center_panel_does_not_render_info_or_confirmation_inline(self) -> None:
        state = _build_state(selected_week=1)
        state._emit_info_toast("Cambios guardados.")
        state._set_confirmation(
            key="week_close",
            title="Cerrar semana",
            body="\u00bfQuieres continuar?",
            confirm_label="Cerrar",
            payload=(1, 1),
        )

        panel = build_center_panel(state.build_view_data(), state)
        text_values = _text_values(panel)

        self.assertNotIn("Informaci\u00f3n", text_values)
        self.assertNotIn("Cambios guardados.", text_values)
        self.assertNotIn("Cerrar semana", text_values)
        self.assertNotIn("\u00bfQuieres continuar?", text_values)

    def test_resource_projected_total_for_new_entry_uses_draft_delta(self) -> None:
        state = _build_state(selected_week=1)
        _set_single_entry_resources(
            state,
            persisted_resource_deltas={},
            campaign_resource_totals={"lumber": 0},
            draft_resource_deltas={"lumber": 2},
        )

        panel = build_center_panel(state.build_view_data(), state)
        row = _find_resource_row(panel, resource_key="lumber")

        self.assertEqual(2, row.delta_value)
        self.assertEqual(2, row.projected_total)
        self.assertEqual("(2)", _find_projected_total_text(row))

    def test_resource_projected_total_does_not_double_count_persisted_delta(self) -> None:
        state = _build_state(selected_week=1)
        _set_single_entry_resources(
            state,
            persisted_resource_deltas={"lumber": 2},
            campaign_resource_totals={"lumber": 2},
        )

        panel = build_center_panel(state.build_view_data(), state)
        row = _find_resource_row(panel, resource_key="lumber")

        self.assertEqual(2, row.delta_value)
        self.assertEqual(2, row.projected_total)
        self.assertEqual("(2)", _find_projected_total_text(row))

    def test_resource_projected_total_updates_when_editing_persisted_delta(self) -> None:
        state = _build_state(selected_week=1)
        _set_single_entry_resources(
            state,
            persisted_resource_deltas={"lumber": 2},
            campaign_resource_totals={"lumber": 2},
            draft_resource_deltas={"lumber": 3},
        )

        panel = build_center_panel(state.build_view_data(), state)
        row = _find_resource_row(panel, resource_key="lumber")

        self.assertEqual(3, row.delta_value)
        self.assertEqual(3, row.projected_total)
        self.assertEqual("(3)", _find_projected_total_text(row))

    def test_resource_projected_total_supports_clearing_persisted_delta(self) -> None:
        state = _build_state(selected_week=1)
        _set_single_entry_resources(
            state,
            persisted_resource_deltas={"lumber": 2},
            campaign_resource_totals={"lumber": 2},
            draft_resource_deltas={},
        )

        panel = build_center_panel(state.build_view_data(), state)
        row = _find_resource_row(panel, resource_key="lumber")

        self.assertEqual(0, row.delta_value)
        self.assertEqual(0, row.projected_total)
        self.assertEqual("(0)", _find_projected_total_text(row))

    def test_resource_projected_total_keeps_nd_when_campaign_totals_are_unavailable(self) -> None:
        state = _build_state(selected_week=1)
        _set_single_entry_resources(
            state,
            persisted_resource_deltas={"lumber": 2},
            campaign_resource_totals=None,
        )

        panel = build_center_panel(state.build_view_data(), state)
        row = _find_resource_row(panel, resource_key="lumber")

        self.assertEqual(2, row.delta_value)
        self.assertIsNone(row.projected_total)
        self.assertEqual("(N/D)", _find_projected_total_text(row))

    def test_entry_cards_show_play_stop_toggle_from_active_entry(self) -> None:
        state = _build_state(selected_week=1)
        first_entry = _build_entry(entry_id="entry-1", label="Escenario 1")
        second_entry = _build_entry(entry_id="entry-2", label="Escenario 2")
        state.entry_panel_state.entries_for_selected_week = [first_entry, second_entry]
        state.entry_panel_state.sessions_by_entry_ref = {
            first_entry.ref: [],
            second_entry.ref: [_build_session(session_id="sess-1", active=True)],
        }
        state.read_state.active_entry_ref = second_entry.ref
        state.read_state.active_entry_label = second_entry.label
        state.read_state.active_session_started_at_utc = (
            datetime.now(timezone.utc) - timedelta(minutes=10)
        )

        panel = build_center_panel(state.build_view_data(), state)

        self.assertEqual(_tooltips(panel).count("Iniciar sesión"), 1)
        self.assertEqual(_tooltips(panel).count("Detener sesión"), 1)

    def test_sessions_card_keeps_manual_actions_and_new_session_button(self) -> None:
        state = _build_state(selected_week=1)
        entry = _build_entry(entry_id="entry-1", label="Escenario 1")
        state.entry_panel_state.entries_for_selected_week = [entry]
        state.entry_panel_state.sessions_by_entry_ref = {
            entry.ref: [_build_session(session_id="sess-1", active=False)],
        }

        panel = build_center_panel(state.build_view_data(), state)
        labels = _button_labels(panel)
        text_values = _text_values(panel)

        self.assertIn("Nueva sesión", labels)
        self.assertIn("Editar", labels)
        self.assertIn("Borrar", labels)
        self.assertIn("Total jugado", text_values)
        self.assertIn("Sesiones", text_values)


if __name__ == "__main__":
    unittest.main()
