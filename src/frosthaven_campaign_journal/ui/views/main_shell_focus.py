from __future__ import annotations

from typing import Callable

import flet as ft

from frosthaven_campaign_journal.state.placeholders import (
    ENTRY_RESOURCE_KEYS,
    MainScreenLocalState,
    entry_ref_matches_selected_week,
)
from frosthaven_campaign_journal.ui.views.main_shell_contracts import (
    MainShellViewActions,
    MainShellViewData,
)
from frosthaven_campaign_journal.ui.views.main_shell_shared import (
    CENTER_PANEL_PADDING,
    COLOR_CENTER_BG,
    COLOR_ERROR_BG,
    COLOR_ERROR_BORDER,
    COLOR_ERROR_TEXT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_WARNING_BG,
    COLOR_WARNING_BORDER,
    COLOR_WARNING_TEXT,
    build_badge,
    build_placeholder_card,
    build_status_banner,
    format_dt_short,
    format_duration,
    format_navigation_line,
    session_duration,
    sum_finished_sessions_duration,
    truncate,
)


def build_center_focus_panel(
    *,
    data: MainShellViewData,
    actions: MainShellViewActions,
) -> ft.Control:
    selected_week = _find_selected_week(data.state, data.weeks_for_selected_year)

    if data.viewer_entry is not None:
        primary_content = _build_focus_entry_mode(
            state=data.state,
            viewer_entry=data.viewer_entry,
            viewer_sessions=data.viewer_sessions,
            viewer_sessions_error_message=data.viewer_sessions_error_message,
            session_write_error_message=data.session_write_error_message,
            session_write_pending=data.session_write_pending,
            entry_write_error_message=data.entry_write_error_message,
            entry_write_pending=data.entry_write_pending,
            resource_write_error_message=data.resource_write_error_message,
            resource_write_pending=data.resource_write_pending,
            resource_draft_values=data.resource_draft_values,
            resource_draft_dirty=data.resource_draft_dirty,
            resource_draft_attached_to_viewer=data.resource_draft_attached_to_viewer,
            active_entry_ref=data.active_entry_ref,
            active_entry_label=data.active_entry_label,
            on_start_session=actions.on_start_session,
            on_stop_session=actions.on_stop_session,
            on_open_manual_create_session=actions.on_open_manual_create_session,
            on_open_manual_edit_session=actions.on_open_manual_edit_session,
            on_open_manual_delete_session=actions.on_open_manual_delete_session,
            on_open_create_entry_modal=actions.on_open_create_entry_modal,
            on_open_edit_entry_modal=actions.on_open_edit_entry_modal,
            on_open_delete_entry_confirm=actions.on_open_delete_entry_confirm,
            on_reorder_entry_up=actions.on_reorder_entry_up,
            on_reorder_entry_down=actions.on_reorder_entry_down,
            on_adjust_resource_draft_delta=actions.on_adjust_resource_draft_delta,
            on_save_resource_draft=actions.on_save_resource_draft,
            on_discard_resource_draft=actions.on_discard_resource_draft,
        )
    elif selected_week is not None:
        primary_content = _build_focus_week_mode(
            selected_week,
            week_write_error_message=data.week_write_error_message,
            week_write_pending=data.week_write_pending,
            entry_write_error_message=data.entry_write_error_message,
            entry_write_pending=data.entry_write_pending,
            on_open_week_notes_modal=actions.on_open_week_notes_modal,
            on_request_close_week=actions.on_request_close_week,
            on_request_reopen_week=actions.on_request_reopen_week,
            on_request_reclose_week=actions.on_request_reclose_week,
            on_open_create_entry_modal=actions.on_open_create_entry_modal,
        )
    else:
        primary_content = _build_focus_empty_mode(data.state)

    stacked_controls: list[ft.Control] = []
    if data.read_error_message:
        stacked_controls.append(
            build_status_banner(
                title="Error de lectura (Firestore)",
                body=data.read_error_message,
                background=COLOR_ERROR_BG,
                border_color=COLOR_ERROR_BORDER,
                foreground=COLOR_ERROR_TEXT,
            )
        )
    if data.read_warning_message:
        stacked_controls.append(
            build_status_banner(
                title="Advertencia de consistencia",
                body=data.read_warning_message,
                background=COLOR_WARNING_BG,
                border_color=COLOR_WARNING_BORDER,
                foreground=COLOR_WARNING_TEXT,
            )
        )
    stacked_controls.append(primary_content)

    return ft.Container(
        expand=True,
        bgcolor=COLOR_CENTER_BG,
        padding=ft.Padding.all(CENTER_PANEL_PADDING),
        content=ft.ListView(
            expand=True,
            spacing=12,
            padding=0,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            scroll=ft.ScrollMode.AUTO,
            controls=stacked_controls,
        ),
    )


def _build_focus_empty_mode(state: MainScreenLocalState) -> ft.Control:
    return ft.Column(
        spacing=10,
        controls=[
            ft.Text(
                "Sin week seleccionada",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT_PRIMARY,
            ),
            ft.Text(
                "Navega por las weeks del año visible y selecciona una entry para mostrarla en el visor.",
                size=14,
                color=COLOR_TEXT_MUTED,
            ),
            build_placeholder_card(
                title="Visor (sticky) vacío",
                body=(
                    "El visor se mantiene separado de la navegación. "
                    "Cuando selecciones una entry, seguirá visible aunque cambies de año o week."
                ),
                min_height=108,
            ),
            build_placeholder_card(
                title=(
                    f"Navegación actual: Año {state.selected_year}"
                    if state.selected_year is not None
                    else "Navegación actual: sin año disponible"
                ),
                body="No hay week seleccionada todavía.",
                min_height=74,
            ),
        ],
    )


def _build_focus_week_mode(
    week: object,
    *,
    week_write_error_message: str | None,
    week_write_pending: bool,
    entry_write_error_message: str | None,
    entry_write_pending: bool,
    on_open_week_notes_modal: Callable[[], None],
    on_request_close_week: Callable[[], None],
    on_request_reopen_week: Callable[[], None],
    on_request_reclose_week: Callable[[], None],
    on_open_create_entry_modal: Callable[[], None],
) -> ft.Control:
    badge_bg = "#EDEDED" if week.is_closed else "#D9F2D9"
    badge_fg = "#6A6A6A" if week.is_closed else "#237A3B"
    action_buttons: list[ft.Control] = [
        ft.FilledButton(
            "Nueva entry",
            on_click=lambda _e: on_open_create_entry_modal(),
            disabled=entry_write_pending,
            height=32,
        ),
        ft.OutlinedButton(
            "Editar notas",
            on_click=lambda _e: on_open_week_notes_modal(),
            disabled=week_write_pending,
            height=32,
        ),
    ]
    if week.is_closed:
        action_buttons.append(
            ft.FilledButton(
                "Reopen",
                on_click=lambda _e: on_request_reopen_week(),
                disabled=week_write_pending,
                height=32,
            )
        )
    else:
        action_buttons.extend(
            [
                ft.FilledButton(
                    "Close",
                    on_click=lambda _e: on_request_close_week(),
                    disabled=week_write_pending,
                    height=32,
                ),
                ft.OutlinedButton(
                    "Reclose",
                    on_click=lambda _e: on_request_reclose_week(),
                    disabled=week_write_pending,
                    height=32,
                ),
            ]
        )

    notes_controls: list[ft.Control] = [ft.Row(spacing=8, wrap=True, controls=action_buttons)]
    if week_write_pending:
        notes_controls.append(
            ft.Text(
                "Procesando acción de week…",
                size=12,
                color=COLOR_TEXT_MUTED,
                italic=True,
            )
        )
    if entry_write_pending:
        notes_controls.append(
            ft.Text(
                "Procesando acción de entry…",
                size=12,
                color=COLOR_TEXT_MUTED,
                italic=True,
            )
        )
    if week_write_error_message:
        notes_controls.append(
            ft.Container(
                padding=ft.Padding.all(8),
                bgcolor="#FFE7E7",
                border=ft.Border.all(1, "#D87A7A"),
                border_radius=6,
                content=ft.Text(
                    truncate(week_write_error_message, 220),
                    size=12,
                    color=COLOR_ERROR_TEXT,
                ),
            )
        )
    if entry_write_error_message:
        notes_controls.append(
            ft.Container(
                padding=ft.Padding.all(8),
                bgcolor="#FFE7E7",
                border=ft.Border.all(1, "#D87A7A"),
                border_radius=6,
                content=ft.Text(
                    truncate(entry_write_error_message, 220),
                    size=12,
                    color=COLOR_ERROR_TEXT,
                ),
            )
        )
    notes_controls.append(
        build_placeholder_card(
            title="Notas de la week",
            body=week.notes_preview or f"Sin notas en la week {week.week_number}.",
            min_height=110,
        )
    )

    return ft.Column(
        spacing=12,
        controls=[
            ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        f"Week {week.week_number}",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXT_PRIMARY,
                    ),
                    build_badge(week.status_label, badge_bg, badge_fg),
                ],
            ),
            ft.Container(
                padding=ft.Padding.all(12),
                bgcolor="#F6F6F6",
                border_radius=8,
                border=ft.Border.all(1, "#D6D6D6"),
                content=ft.Column(spacing=8, controls=notes_controls),
            ),
            build_placeholder_card(
                title="Sin entry en visor",
                body=(
                    "La week está seleccionada para navegación, pero el visor solo cambia al seleccionar una entry."
                ),
                min_height=90,
            ),
        ],
    )


def _build_focus_entry_mode(
    *,
    state: MainScreenLocalState,
    viewer_entry: object,
    viewer_sessions: list[object],
    viewer_sessions_error_message: str | None,
    session_write_error_message: str | None,
    session_write_pending: bool,
    entry_write_error_message: str | None,
    entry_write_pending: bool,
    resource_write_error_message: str | None,
    resource_write_pending: bool,
    resource_draft_values: dict[str, int] | None,
    resource_draft_dirty: bool,
    resource_draft_attached_to_viewer: bool,
    active_entry_ref: object | None,
    active_entry_label: str | None,
    on_start_session: Callable[[], None],
    on_stop_session: Callable[[], None],
    on_open_manual_create_session: Callable[[], None],
    on_open_manual_edit_session: Callable[[str], None],
    on_open_manual_delete_session: Callable[[str], None],
    on_open_create_entry_modal: Callable[[], None],
    on_open_edit_entry_modal: Callable[[], None],
    on_open_delete_entry_confirm: Callable[[], None],
    on_reorder_entry_up: Callable[[], None],
    on_reorder_entry_down: Callable[[], None],
    on_adjust_resource_draft_delta: Callable[[str, int], None],
    on_save_resource_draft: Callable[[], None],
    on_discard_resource_draft: Callable[[], None],
) -> ft.Control:
    viewer_matches_selected_week = entry_ref_matches_selected_week(state, viewer_entry.ref)
    active_here = active_entry_ref is not None and active_entry_ref == viewer_entry.ref

    context_lines = [
        (
            f"Viendo: {viewer_entry.label} · Week {viewer_entry.ref.week_number} · "
            f"Año {viewer_entry.ref.year_number}"
        ),
        format_navigation_line(state),
    ]
    if not viewer_matches_selected_week:
        context_lines.append(
            "Visor sticky: la entry visible no coincide con la week navegada actualmente."
        )

    if active_entry_ref is None:
        session_status_text = "Sin sesión activa real."
    elif active_here:
        session_status_text = f"Con sesión activa aquí: {active_entry_label or 'Entry activa'}."
    else:
        session_status_text = (
            f"Con sesión activa en otra entry: {active_entry_label or 'Entry activa'}."
        )

    detail_lines = [f"Tipo: {viewer_entry.entry_type}"]
    if viewer_entry.scenario_ref is not None:
        detail_lines.append(f"Scenario ref: {viewer_entry.scenario_ref}")
    if viewer_entry.order_index is not None:
        detail_lines.append(f"Order index: {viewer_entry.order_index}")
    if viewer_entry.resource_deltas:
        detail_lines.append(
            "resource_deltas: "
            + ", ".join(
                f"{k}={v}" for k, v in sorted(viewer_entry.resource_deltas.items(), key=lambda item: item[0])
            )
        )
    else:
        detail_lines.append("resource_deltas: sin cambios en esta entry")

    entry_detail_card = build_placeholder_card(
        title="Detalle de entry (Q5)",
        body="\n".join(detail_lines),
        min_height=120,
    )

    sessions_card = _build_sessions_card(
        viewer_sessions=viewer_sessions,
        viewer_sessions_error_message=viewer_sessions_error_message,
        session_write_error_message=session_write_error_message,
        session_write_pending=session_write_pending,
        session_status_text=session_status_text,
        on_start_session=on_start_session,
        on_stop_session=on_stop_session,
        on_open_manual_create_session=on_open_manual_create_session,
        on_open_manual_edit_session=on_open_manual_edit_session,
        on_open_manual_delete_session=on_open_manual_delete_session,
    )

    entry_actions_card = _build_entry_actions_card(
        entry_write_error_message=entry_write_error_message,
        entry_write_pending=entry_write_pending,
        on_open_create_entry_modal=on_open_create_entry_modal,
        on_open_edit_entry_modal=on_open_edit_entry_modal,
        on_open_delete_entry_confirm=on_open_delete_entry_confirm,
        on_reorder_entry_up=on_reorder_entry_up,
        on_reorder_entry_down=on_reorder_entry_down,
    )

    resources_card = _build_entry_resources_card(
        viewer_entry=viewer_entry,
        resource_draft_values=resource_draft_values,
        resource_draft_dirty=resource_draft_dirty,
        resource_draft_attached_to_viewer=resource_draft_attached_to_viewer,
        resource_write_error_message=resource_write_error_message,
        resource_write_pending=resource_write_pending,
        on_adjust_resource_draft_delta=on_adjust_resource_draft_delta,
        on_save_resource_draft=on_save_resource_draft,
        on_discard_resource_draft=on_discard_resource_draft,
    )

    return ft.Column(
        spacing=12,
        controls=[
            ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        f"Week {viewer_entry.ref.week_number} · {viewer_entry.label}",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXT_PRIMARY,
                    ),
                    build_badge(viewer_entry.entry_type, "#E7E0FF", "#4F46A5"),
                    build_badge(
                        "activo aquí" if active_here else "visor",
                        "#DFF4FF" if active_here else "#F0F0F0",
                        "#0E5E78" if active_here else "#666666",
                    ),
                ],
            ),
            build_placeholder_card(
                title="Contexto de visor / navegación",
                body="\n".join(context_lines),
                min_height=110,
            ),
            entry_detail_card,
            entry_actions_card,
            sessions_card,
            resources_card,
        ],
    )


def _build_entry_actions_card(
    *,
    entry_write_error_message: str | None,
    entry_write_pending: bool,
    on_open_create_entry_modal: Callable[[], None],
    on_open_edit_entry_modal: Callable[[], None],
    on_open_delete_entry_confirm: Callable[[], None],
    on_reorder_entry_up: Callable[[], None],
    on_reorder_entry_down: Callable[[], None],
) -> ft.Control:
    body_controls: list[ft.Control] = [
        ft.Text(
            "Crear usa la week seleccionada; editar/reordenar/borrar operan sobre la entry visible.",
            size=12,
            color=COLOR_TEXT_MUTED,
        ),
        ft.Row(
            spacing=8,
            wrap=True,
            controls=[
                ft.FilledButton(
                    "Nueva",
                    on_click=lambda _e: on_open_create_entry_modal(),
                    disabled=entry_write_pending,
                    height=32,
                ),
                ft.OutlinedButton(
                    "Editar",
                    on_click=lambda _e: on_open_edit_entry_modal(),
                    disabled=entry_write_pending,
                    height=32,
                ),
                ft.OutlinedButton(
                    "Borrar",
                    on_click=lambda _e: on_open_delete_entry_confirm(),
                    disabled=entry_write_pending,
                    height=32,
                ),
                ft.OutlinedButton(
                    "Subir",
                    on_click=lambda _e: on_reorder_entry_up(),
                    disabled=entry_write_pending,
                    height=32,
                ),
                ft.OutlinedButton(
                    "Bajar",
                    on_click=lambda _e: on_reorder_entry_down(),
                    disabled=entry_write_pending,
                    height=32,
                ),
            ],
        ),
    ]
    if entry_write_pending:
        body_controls.append(
            ft.Text(
                "Procesando acción de entry…",
                size=12,
                color=COLOR_TEXT_MUTED,
                italic=True,
            )
        )
    if entry_write_error_message:
        body_controls.append(
            ft.Container(
                padding=ft.Padding.all(8),
                bgcolor="#FFE7E7",
                border=ft.Border.all(1, "#D87A7A"),
                border_radius=6,
                content=ft.Text(
                    truncate(entry_write_error_message, 220),
                    size=12,
                    color=COLOR_ERROR_TEXT,
                ),
            )
        )
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border_radius=8,
        border=ft.Border.all(1, "#D6D6D6"),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    "Acciones de entry (#64)",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_TEXT_PRIMARY,
                ),
                ft.Container(
                    padding=ft.Padding.all(8),
                    bgcolor="#FFFFFF",
                    border_radius=6,
                    content=ft.Column(spacing=8, controls=body_controls),
                ),
            ],
        ),
    )


def _build_entry_resources_card(
    *,
    viewer_entry: object,
    resource_draft_values: dict[str, int] | None,
    resource_draft_dirty: bool,
    resource_draft_attached_to_viewer: bool,
    resource_write_error_message: str | None,
    resource_write_pending: bool,
    on_adjust_resource_draft_delta: Callable[[str, int], None],
    on_save_resource_draft: Callable[[], None],
    on_discard_resource_draft: Callable[[], None],
) -> ft.Control:
    effective_draft = (
        dict(resource_draft_values)
        if resource_draft_attached_to_viewer and resource_draft_values is not None
        else dict(viewer_entry.resource_deltas)
    )
    draft_controls_disabled = resource_write_pending or not resource_draft_attached_to_viewer

    rows: list[ft.Control] = []
    for resource_key in ENTRY_RESOURCE_KEYS:
        current_value = effective_draft.get(resource_key, 0)
        persisted_value = viewer_entry.resource_deltas.get(resource_key, 0)
        labels: list[ft.Control] = [
            ft.Text(
                resource_key,
                size=13,
                weight=ft.FontWeight.W_600,
                color=COLOR_TEXT_PRIMARY,
            ),
            ft.Text(
                f"Delta neto entry (edición): {current_value}",
                size=11,
                color=COLOR_TEXT_MUTED,
            ),
        ]
        if resource_draft_dirty and current_value != persisted_value:
            labels.append(
                ft.Text(
                    f"Guardado: {persisted_value}",
                    size=11,
                    color="#7D5700",
                )
            )
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
                        ft.Column(
                            expand=True,
                            spacing=2,
                            controls=labels,
                        ),
                        ft.Row(
                            spacing=6,
                            controls=[
                                ft.OutlinedButton(
                                    "-1",
                                    on_click=lambda _e, key=resource_key: on_adjust_resource_draft_delta(key, -1),
                                    disabled=draft_controls_disabled,
                                    height=32,
                                ),
                                ft.FilledButton(
                                    "+1",
                                    on_click=lambda _e, key=resource_key: on_adjust_resource_draft_delta(key, 1),
                                    disabled=draft_controls_disabled,
                                    height=32,
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )

    body_controls: list[ft.Control] = [
        ft.Text(
            "Los cambios se editan localmente y se persisten al pulsar Guardar.",
            size=12,
            color=COLOR_TEXT_MUTED,
        ),
        ft.Row(
            spacing=8,
            wrap=True,
            controls=[
                ft.FilledButton(
                    "Guardar recursos",
                    on_click=lambda _e: on_save_resource_draft(),
                    disabled=(
                        resource_write_pending
                        or not resource_draft_attached_to_viewer
                        or not resource_draft_dirty
                    ),
                    height=32,
                ),
                ft.OutlinedButton(
                    "Descartar cambios",
                    on_click=lambda _e: on_discard_resource_draft(),
                    disabled=(
                        resource_write_pending
                        or not resource_draft_attached_to_viewer
                        or not resource_draft_dirty
                    ),
                    height=32,
                ),
            ],
        ),
    ]
    if resource_draft_attached_to_viewer:
        body_controls.append(
            ft.Text(
                "Cambios sin guardar" if resource_draft_dirty else "Sin cambios locales pendientes",
                size=12,
                color="#7D5700" if resource_draft_dirty else COLOR_TEXT_MUTED,
                italic=resource_draft_dirty,
            )
        )
    else:
        body_controls.append(
            ft.Text(
                "Borrador de recursos no disponible para la entry visible (refresca y reintenta).",
                size=12,
                color=COLOR_WARNING_TEXT,
            )
        )
    body_controls.extend(rows)
    if resource_write_pending:
        body_controls.append(
            ft.Text(
                "Guardando cambios de recursos…",
                size=12,
                color=COLOR_TEXT_MUTED,
                italic=True,
            )
        )
    if resource_write_error_message:
        body_controls.append(
            ft.Container(
                padding=ft.Padding.all(8),
                bgcolor="#FFE7E7",
                border=ft.Border.all(1, "#D87A7A"),
                border_radius=6,
                content=ft.Text(
                    truncate(resource_write_error_message, 220),
                    size=12,
                    color=COLOR_ERROR_TEXT,
                ),
            )
        )
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border_radius=8,
        border=ft.Border.all(1, "#D6D6D6"),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    "Recursos de la entry (#64)",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_TEXT_PRIMARY,
                ),
                ft.Container(
                    padding=ft.Padding.all(8),
                    bgcolor="#FFFFFF",
                    border_radius=6,
                    content=ft.Column(spacing=8, controls=body_controls),
                ),
            ],
        ),
    )


def _build_sessions_card(
    *,
    viewer_sessions: list[object],
    viewer_sessions_error_message: str | None,
    session_write_error_message: str | None,
    session_write_pending: bool,
    session_status_text: str,
    on_start_session: Callable[[], None],
    on_stop_session: Callable[[], None],
    on_open_manual_create_session: Callable[[], None],
    on_open_manual_edit_session: Callable[[str], None],
    on_open_manual_delete_session: Callable[[str], None],
) -> ft.Control:
    total_duration = sum_finished_sessions_duration(viewer_sessions)
    total_text = format_duration(total_duration) if total_duration is not None else "0 min"
    has_active_session = any(session.ended_at_utc is None for session in viewer_sessions)
    body_controls: list[ft.Control] = [
        ft.Text(session_status_text, size=13, color=COLOR_TEXT_MUTED),
        ft.Text(f"Total jugado (Q8): {total_text}", size=13, color=COLOR_TEXT_MUTED),
        ft.Row(
            spacing=8,
            wrap=True,
            controls=[
                ft.FilledButton(
                    "Start",
                    on_click=lambda _e: on_start_session(),
                    disabled=session_write_pending,
                    height=32,
                ),
                ft.OutlinedButton(
                    "Stop",
                    on_click=lambda _e: on_stop_session(),
                    disabled=session_write_pending or not has_active_session,
                    height=32,
                ),
                ft.OutlinedButton(
                    "Nueva sesión",
                    on_click=lambda _e: on_open_manual_create_session(),
                    disabled=session_write_pending,
                    height=32,
                ),
            ],
        ),
    ]

    if session_write_pending:
        body_controls.append(
            ft.Text(
                "Procesando acción de sesión…",
                size=12,
                color=COLOR_TEXT_MUTED,
                italic=True,
            )
        )

    if session_write_error_message:
        body_controls.append(
            ft.Container(
                padding=ft.Padding.all(8),
                bgcolor="#FFE7E7",
                border=ft.Border.all(1, "#D87A7A"),
                border_radius=6,
                content=ft.Text(
                    truncate(session_write_error_message, 220),
                    size=12,
                    color=COLOR_ERROR_TEXT,
                ),
            )
        )

    if viewer_sessions_error_message:
        body_controls.append(
            ft.Container(
                padding=ft.Padding.all(8),
                bgcolor="#FFE7E7",
                border=ft.Border.all(1, "#D87A7A"),
                border_radius=6,
                content=ft.Text(
                    "Error local Q8: " + truncate(viewer_sessions_error_message, 220),
                    size=12,
                    color=COLOR_ERROR_TEXT,
                ),
            )
        )

    if not viewer_sessions:
        body_controls.append(
            ft.Text(
                "Sin sesiones para la entry visible.",
                size=12,
                color=COLOR_TEXT_MUTED,
                italic=True,
            )
        )
    else:
        rows: list[ft.Control] = []
        for index, session in enumerate(viewer_sessions[:8], start=1):
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
                            ft.Column(
                                expand=True,
                                spacing=2,
                                controls=[
                                    ft.Text(
                                        f"{index}. {_format_session_line(session)}",
                                        size=12,
                                        color=COLOR_TEXT_PRIMARY,
                                    ),
                                ],
                            ),
                            ft.Row(
                                spacing=4,
                                controls=[
                                    ft.OutlinedButton(
                                        "Editar",
                                        on_click=lambda _e, sid=session.session_id: on_open_manual_edit_session(sid),
                                        disabled=session_write_pending,
                                        height=30,
                                    ),
                                    ft.OutlinedButton(
                                        "Borrar",
                                        on_click=lambda _e, sid=session.session_id: on_open_manual_delete_session(sid),
                                        disabled=session_write_pending,
                                        height=30,
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )
        if len(viewer_sessions) > 8:
            rows.append(
                ft.Text(
                    f"… y {len(viewer_sessions) - 8} sesión(es) más",
                    size=11,
                    color=COLOR_TEXT_MUTED,
                )
            )
        body_controls.extend(rows)

    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border_radius=8,
        border=ft.Border.all(1, "#D6D6D6"),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    "Sesiones (#63)",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_TEXT_PRIMARY,
                ),
                ft.Container(
                    padding=ft.Padding.all(8),
                    bgcolor="#FFFFFF",
                    border_radius=6,
                    content=ft.Column(spacing=8, controls=body_controls),
                ),
            ],
        ),
    )


def _format_session_line(session: object) -> str:
    started = format_dt_short(session.started_at_utc)
    ended = format_dt_short(session.ended_at_utc)
    if session.ended_at_utc is None:
        return f"{session.session_id}: {started} → activa"
    duration = session_duration(session)
    duration_text = format_duration(duration) if duration is not None else "duración n/d"
    return f"{session.session_id}: {started} → {ended} · {duration_text}"


def _find_selected_week(
    state: MainScreenLocalState,
    weeks_for_selected_year: list[object],
) -> object | None:
    if state.selected_week is None:
        return None
    for week in weeks_for_selected_year:
        if week.week_number == state.selected_week:
            return week
    return None
