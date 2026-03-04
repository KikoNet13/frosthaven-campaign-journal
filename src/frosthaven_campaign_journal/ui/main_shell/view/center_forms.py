from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.common.components.surfaces import build_panel
from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_ERROR_TEXT,
    COLOR_TEXT_HEADING,
    COLOR_TEXT_PRIMARY,
)
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState


def _build_confirmation_card(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.confirmation is not None
    return build_panel(
        controls=[
            ft.Text(data.confirmation.title, size=15, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_HEADING),
            ft.Text(data.confirmation.body, size=13, color=COLOR_TEXT_PRIMARY),
            ft.Row(
                spacing=8,
                controls=[
                    ft.TextButton("Cancelar", on_click=state.on_cancel_pending_action),
                    ft.FilledButton(data.confirmation.confirm_label, on_click=state.on_confirm_pending_action),
                ],
            ),
        ],
    )


def _build_week_notes_editor(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.week_notes_editor is not None
    return build_panel(
        controls=[
            ft.Text("Editar notas de semana", size=14, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_HEADING),
            ft.TextField(
                value=data.week_notes_editor.notes_value,
                multiline=True,
                min_lines=3,
                max_lines=6,
                on_change=state.on_week_notes_change,
            ),
            ft.Row(
                spacing=8,
                controls=[
                    ft.TextButton("Cancelar", on_click=state.on_cancel_week_notes_editor),
                    ft.FilledButton("Guardar notas", on_click=state.on_submit_week_notes),
                ],
            ),
            ft.Text(data.week_notes_editor.error_message or "", size=12, color=COLOR_ERROR_TEXT),
        ],
    )


def _build_entry_form_editor(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.entry_form is not None
    is_scenario = data.entry_form.entry_type == "scenario"
    return build_panel(
        controls=[
            ft.Text(
                "Crear entrada" if data.entry_form.mode == "create" else "Editar entrada",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT_HEADING,
            ),
            ft.Dropdown(
                value=data.entry_form.entry_type,
                options=[
                    ft.dropdown.Option(key="scenario", text="Escenario"),
                    ft.dropdown.Option(key="outpost", text="Puesto fronterizo"),
                ],
                on_change=state.on_entry_form_set_type,
            ),
            ft.TextField(
                label="Referencia de escenario",
                value=data.entry_form.scenario_ref_text,
                on_change=state.on_entry_form_set_scenario_ref,
                disabled=not is_scenario,
                hint_text="Entero positivo" if is_scenario else "No aplica para puesto avanzado",
            ),
            ft.Row(
                spacing=8,
                controls=[
                    ft.TextButton("Cancelar", on_click=state.on_cancel_entry_form),
                    ft.FilledButton("Guardar", on_click=state.on_submit_entry_form),
                ],
            ),
            ft.Text(data.entry_form.error_message or "", size=12, color=COLOR_ERROR_TEXT),
        ],
    )


def _build_entry_notes_editor(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.entry_notes_editor is not None
    return build_panel(
        controls=[
            ft.Text(
                f"Editar notas de entry: {data.entry_notes_editor.entry_label}",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT_HEADING,
            ),
            ft.TextField(
                value=data.entry_notes_editor.notes_value,
                multiline=True,
                min_lines=3,
                max_lines=6,
                on_change=state.on_entry_notes_change,
            ),
            ft.Row(
                spacing=8,
                controls=[
                    ft.TextButton("Cancelar", on_click=state.on_cancel_entry_notes_editor),
                    ft.FilledButton("Guardar notas", on_click=state.on_submit_entry_notes),
                ],
            ),
            ft.Text(data.entry_notes_editor.error_message or "", size=12, color=COLOR_ERROR_TEXT),
        ],
    )


def _build_session_form_editor(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.session_form is not None
    return build_panel(
        controls=[
            ft.Text(
                "Crear sesión manual" if data.session_form.mode == "create" else "Editar sesión",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT_HEADING,
            ),
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
            ft.Row(
                spacing=8,
                controls=[
                    ft.TextButton("Cancelar", on_click=state.on_cancel_session_form),
                    ft.FilledButton("Guardar", on_click=state.on_submit_session_form),
                ],
            ),
            ft.Text(data.session_form.error_message or "", size=12, color=COLOR_ERROR_TEXT),
        ],
    )
