from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.common.theme.colors import COLOR_ERROR_TEXT
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState


def build_entry_form_dialog_body(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.entry_form is not None
    is_scenario = data.entry_form.entry_type == "scenario"
    controls: list[ft.Control] = [
        ft.Dropdown(
            value=data.entry_form.entry_type,
            options=[
                ft.dropdown.Option(key="scenario", text="Escenario"),
                ft.dropdown.Option(key="outpost", text="Puesto fronterizo"),
            ],
            on_select=state.on_entry_form_set_type,
        ),
        ft.TextField(
            label="Referencia de escenario",
            value=data.entry_form.scenario_ref_text,
            on_change=state.on_entry_form_set_scenario_ref,
            disabled=not is_scenario,
            hint_text="Entero positivo" if is_scenario else "No aplica para puesto avanzado",
        ),
    ]
    if data.entry_form.error_message:
        controls.append(ft.Text(data.entry_form.error_message, size=12, color=COLOR_ERROR_TEXT))
    return ft.Column(spacing=12, tight=True, controls=controls)


def build_entry_notes_dialog_body(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.entry_notes_editor is not None
    controls: list[ft.Control] = [
        ft.TextField(
            value=data.entry_notes_editor.notes_value,
            multiline=True,
            expand=True,
            on_change=state.on_entry_notes_change,
        )
    ]
    if data.entry_notes_editor.error_message:
        controls.append(ft.Text(data.entry_notes_editor.error_message, size=12, color=COLOR_ERROR_TEXT))
    return ft.Column(expand=True, spacing=12, controls=controls)


def build_session_form_dialog_body(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.session_form is not None
    controls: list[ft.Control] = [
        ft.Row(
            spacing=8,
            controls=[
                ft.TextField(
                    label="Inicio (fecha)",
                    hint_text="YYYY-MM-DD",
                    value=data.session_form.started_date_local,
                    on_change=state.on_session_form_set_started_date,
                    width=180,
                ),
                ft.TextField(
                    label="Inicio (hora)",
                    hint_text="HH:MM",
                    value=data.session_form.started_time_local,
                    on_change=state.on_session_form_set_started_time,
                    width=140,
                ),
            ],
        ),
        ft.Row(
            spacing=8,
            controls=[
                ft.TextField(
                    label="Fin (fecha)",
                    hint_text="YYYY-MM-DD",
                    value=data.session_form.ended_date_local,
                    on_change=state.on_session_form_set_ended_date,
                    width=180,
                    disabled=data.session_form.active_without_end,
                ),
                ft.TextField(
                    label="Fin (hora)",
                    hint_text="HH:MM",
                    value=data.session_form.ended_time_local,
                    on_change=state.on_session_form_set_ended_time,
                    width=140,
                    disabled=data.session_form.active_without_end,
                ),
            ],
        ),
        ft.Checkbox(
            label="Sesión activa (sin fin)",
            value=data.session_form.active_without_end,
            on_change=state.on_session_form_toggle_active,
        ),
    ]
    if data.session_form.error_message:
        controls.append(ft.Text(data.session_form.error_message, size=12, color=COLOR_ERROR_TEXT))
    return ft.Column(spacing=12, tight=True, controls=controls)
