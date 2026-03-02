from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.models import (
    ENTRY_RESOURCE_KEYS,
    WeekSummary,
    entry_ref_matches_selected_week,
)
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.view.center_helpers import (
    _build_card,
    _format_duration,
    _format_navigation_line,
    _format_session_line,
    _format_week_status_label,
    _sum_finished_sessions_duration,
)
from frosthaven_campaign_journal.ui.main_shell.view.theme import (
    COLOR_ERROR_TEXT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
)


def _build_focus_empty_mode(data: MainShellViewData) -> ft.Control:
    return _build_card(
        title="Sin semana seleccionada",
        body=(
            "Navega por las semanas del año visible y selecciona una entrada para mostrarla en el visor.\n"
            + _format_navigation_line(data)
        ),
    )


def _build_focus_week_mode(data: MainShellViewData, state: MainShellState, week: WeekSummary) -> ft.Control:
    action_buttons: list[ft.Control] = [
        ft.FilledButton("Nueva entrada", on_click=state.on_open_entry_add_modal, disabled=data.entry_write_pending, height=32),
        ft.OutlinedButton("Editar notas", on_click=state.on_open_week_notes_modal, disabled=data.week_write_pending, height=32),
    ]
    if week.is_closed:
        action_buttons.append(
            ft.FilledButton("Reabrir", on_click=state.on_request_week_reopen, disabled=data.week_write_pending, height=32)
        )
    else:
        action_buttons.extend(
            [
                ft.FilledButton("Cerrar", on_click=state.on_request_week_close, disabled=data.week_write_pending, height=32),
                ft.OutlinedButton("Recerrar", on_click=state.on_request_week_reclose, disabled=data.week_write_pending, height=32),
            ]
        )

    body_lines = [f"Estado: {_format_week_status_label(week.status_label)}", f"Notas: {week.notes_preview or 'Sin notas'}"]
    if data.week_write_error_message:
        body_lines.append(f"Error de semana: {data.week_write_error_message}")
    if data.entry_write_error_message:
        body_lines.append(f"Error de entrada: {data.entry_write_error_message}")
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border=ft.Border.all(1, "#D6D6D6"),
        border_radius=8,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(f"Semana {week.week_number}", size=22, weight=ft.FontWeight.BOLD),
                ft.Row(spacing=8, wrap=True, controls=action_buttons),
                ft.Text("\n".join(body_lines), size=13, color=COLOR_TEXT_MUTED),
            ],
        ),
    )


def _build_focus_entry_mode(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.viewer_entry is not None
    viewer_entry = data.viewer_entry
    viewer_matches_selected_week = entry_ref_matches_selected_week(data.state, viewer_entry.ref)
    active_here = data.active_entry_ref is not None and data.active_entry_ref == viewer_entry.ref

    context_lines = [
        f"Viendo: {viewer_entry.label} · Semana {viewer_entry.ref.week_number} · Año {viewer_entry.ref.year_number}",
        _format_navigation_line(data),
    ]
    if not viewer_matches_selected_week:
        context_lines.append("Visor sticky: la entrada visible no coincide con la semana navegada.")

    detail_lines = [f"Tipo: {viewer_entry.entry_type}"]
    if viewer_entry.scenario_ref is not None:
        detail_lines.append(f"Referencia de escenario: {viewer_entry.scenario_ref}")
    if viewer_entry.order_index is not None:
        detail_lines.append(f"Índice de orden: {viewer_entry.order_index}")
    if viewer_entry.resource_deltas:
        detail_lines.append(
            "Deltas de recursos: "
            + ", ".join(f"{k}={v}" for k, v in sorted(viewer_entry.resource_deltas.items(), key=lambda item: item[0]))
        )
    else:
        detail_lines.append("Deltas de recursos: sin cambios")

    return ft.Column(
        spacing=12,
        controls=[
            _build_card(
                title=f"Semana {viewer_entry.ref.week_number} · {viewer_entry.label}",
                body="\n".join(context_lines),
            ),
            _build_card(
                title="Detalle de entrada",
                body="\n".join(detail_lines),
            ),
            _build_entry_actions_card(data, state),
            _build_sessions_card(data, state, active_here=active_here),
            _build_resources_card(data, state),
        ],
    )


def _build_entry_actions_card(data: MainShellViewData, state: MainShellState) -> ft.Control:
    info_lines: list[str] = ["Crear usa la semana seleccionada; editar/reordenar/borrar operan sobre la entrada visible."]
    if data.entry_write_error_message:
        info_lines.append(f"Error: {data.entry_write_error_message}")
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border_radius=8,
        border=ft.Border.all(1, "#D6D6D6"),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text("Acciones de entrada", size=14, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                ft.Text("\n".join(info_lines), size=12, color=COLOR_TEXT_MUTED),
                ft.Row(
                    spacing=8,
                    wrap=True,
                    controls=[
                        ft.FilledButton("Nueva", on_click=state.on_open_entry_add_modal, disabled=data.entry_write_pending, height=32),
                        ft.OutlinedButton("Editar", on_click=state.on_open_edit_entry_modal, disabled=data.entry_write_pending, height=32),
                        ft.OutlinedButton("Borrar", on_click=state.on_open_entry_delete_confirm, disabled=data.entry_write_pending, height=32),
                        ft.OutlinedButton("Subir", on_click=state.on_reorder_entry_up, disabled=data.entry_write_pending, height=32),
                        ft.OutlinedButton("Bajar", on_click=state.on_reorder_entry_down, disabled=data.entry_write_pending, height=32),
                    ],
                ),
            ],
        ),
    )


def _build_sessions_card(data: MainShellViewData, state: MainShellState, *, active_here: bool) -> ft.Control:
    total_duration = _sum_finished_sessions_duration(data.viewer_sessions)
    total_text = _format_duration(total_duration) if total_duration is not None else "0 min"
    has_active_session = any(session.ended_at_utc is None for session in data.viewer_sessions)

    session_status_text: str
    if data.active_entry_ref is None:
        session_status_text = "Sin sesión activa real."
    elif active_here:
        session_status_text = f"Con sesión activa aquí: {data.active_entry_label or 'Entrada activa'}."
    else:
        session_status_text = f"Con sesión activa en otra entrada: {data.active_entry_label or 'Entrada activa'}."

    rows: list[ft.Control] = []
    for session in data.viewer_sessions[:8]:
        rows.append(
            ft.Container(
                padding=ft.Padding(left=8, top=6, right=8, bottom=6),
                bgcolor="#FFFFFF",
                border=ft.Border.all(1, "#E2E2E2"),
                border_radius=6,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(_format_session_line(session), size=12, color=COLOR_TEXT_PRIMARY),
                        ft.Row(
                            spacing=4,
                            controls=[
                                ft.OutlinedButton(
                                    "Editar",
                                    data=session.session_id,
                                    on_click=state.on_open_manual_edit_session_click,
                                    disabled=data.session_write_pending,
                                    height=30,
                                ),
                                ft.OutlinedButton(
                                    "Borrar",
                                    data=session.session_id,
                                    on_click=state.on_open_manual_delete_session_click,
                                    disabled=data.session_write_pending,
                                    height=30,
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )
    if len(data.viewer_sessions) > 8:
        rows.append(ft.Text(f"… y {len(data.viewer_sessions) - 8} sesión(es) más", size=11, color=COLOR_TEXT_MUTED))

    if data.viewer_sessions_error_message:
        rows.insert(0, ft.Text(f"Error Q8: {data.viewer_sessions_error_message}", size=12, color=COLOR_ERROR_TEXT))
    if data.session_write_error_message:
        rows.insert(0, ft.Text(data.session_write_error_message, size=12, color=COLOR_ERROR_TEXT))

    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border_radius=8,
        border=ft.Border.all(1, "#D6D6D6"),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text("Sesiones", size=14, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                ft.Text(session_status_text, size=12, color=COLOR_TEXT_MUTED),
                ft.Text(f"Total jugado (Q8): {total_text}", size=12, color=COLOR_TEXT_MUTED),
                ft.Row(
                    spacing=8,
                    wrap=True,
                    controls=[
                        ft.FilledButton("Iniciar", on_click=state.on_begin_session, disabled=data.session_write_pending, height=32),
                        ft.OutlinedButton(
                            "Detener",
                            on_click=state.on_end_session,
                            disabled=data.session_write_pending or not has_active_session,
                            height=32,
                        ),
                        ft.OutlinedButton(
                            "Nueva sesión",
                            on_click=state.on_open_manual_create_session,
                            disabled=data.session_write_pending,
                            height=32,
                        ),
                    ],
                ),
                *rows,
            ],
        ),
    )


def _build_resources_card(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.viewer_entry is not None
    effective_draft = (
        dict(data.resource_draft_values)
        if data.resource_draft_attached_to_viewer and data.resource_draft_values is not None
        else dict(data.viewer_entry.resource_deltas)
    )
    draft_controls_disabled = data.resource_write_pending or not data.resource_draft_attached_to_viewer

    rows: list[ft.Control] = []
    for resource_key in ENTRY_RESOURCE_KEYS:
        current_value = effective_draft.get(resource_key, 0)
        persisted_value = data.viewer_entry.resource_deltas.get(resource_key, 0)
        labels: list[ft.Control] = [
            ft.Text(resource_key, size=13, weight=ft.FontWeight.W_600, color=COLOR_TEXT_PRIMARY),
            ft.Text(f"Delta neto de entrada (edición): {current_value}", size=11, color=COLOR_TEXT_MUTED),
        ]
        if data.resource_draft_dirty and current_value != persisted_value:
            labels.append(ft.Text(f"Guardado: {persisted_value}", size=11, color="#7D5700"))

        rows.append(
            ft.Container(
                padding=ft.Padding(left=8, top=6, right=8, bottom=6),
                bgcolor="#FFFFFF",
                border=ft.Border.all(1, "#E2E2E2"),
                border_radius=6,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(expand=True, spacing=2, controls=labels),
                        ft.Row(
                            spacing=6,
                            controls=[
                                ft.OutlinedButton(
                                    "-1",
                                    data=(resource_key, -1),
                                    on_click=state.on_adjust_resource_draft_delta_click,
                                    disabled=draft_controls_disabled,
                                    height=30,
                                ),
                                ft.Text(
                                    str(current_value),
                                    size=13,
                                    weight=ft.FontWeight.W_600,
                                    color=COLOR_TEXT_PRIMARY,
                                ),
                                ft.OutlinedButton(
                                    "+1",
                                    data=(resource_key, 1),
                                    on_click=state.on_adjust_resource_draft_delta_click,
                                    disabled=draft_controls_disabled,
                                    height=30,
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )

    header_lines: list[str] = []
    if data.resource_write_error_message:
        header_lines.append(data.resource_write_error_message)
    if data.resource_draft_attached_to_viewer:
        header_lines.append(
            "Borrador en edición."
            if data.resource_draft_dirty
            else "Borrador sincronizado con recursos persistidos."
        )
    else:
        header_lines.append("Borrador no disponible para la entrada visible.")

    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border_radius=8,
        border=ft.Border.all(1, "#D6D6D6"),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text("Recursos de la entrada", size=14, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                ft.Text(" ".join(header_lines), size=12, color=COLOR_TEXT_MUTED),
                ft.Row(
                    spacing=8,
                    wrap=True,
                    controls=[
                        ft.FilledButton(
                            "Guardar recursos",
                            on_click=state.on_save_resource_draft,
                            disabled=(
                                data.resource_write_pending
                                or not data.resource_draft_attached_to_viewer
                                or not data.resource_draft_dirty
                            ),
                            height=32,
                        ),
                        ft.OutlinedButton(
                            "Descartar cambios",
                            on_click=state.on_discard_resource_draft,
                            disabled=(
                                data.resource_write_pending
                                or not data.resource_draft_attached_to_viewer
                                or not data.resource_draft_dirty
                            ),
                            height=32,
                        ),
                    ],
                ),
                *rows,
            ],
        ),
    )
