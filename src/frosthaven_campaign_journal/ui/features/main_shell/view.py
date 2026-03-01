from __future__ import annotations

from datetime import datetime, timedelta, timezone

import flet as ft

from frosthaven_campaign_journal.state.models import (
    ENTRY_RESOURCE_KEYS,
    EntrySummary,
    WeekSummary,
    entry_ref_matches_selected_week,
)
from frosthaven_campaign_journal.ui.features.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.features.main_shell.state import MainShellState

TOP_BAR_HEIGHT = 64
ENTRY_TABS_BAR_HEIGHT = 44
BOTTOM_BAR_HEIGHT = 96

COLOR_TOP_BAR_BG = "#F39A9A"
COLOR_TOP_NAV_BUTTON_BG = "#5F58C8"
COLOR_TOP_NAV_BUTTON_DISABLED_BG = "#8E88D8"
COLOR_WEEK_TILE_BG = "#F4A0A0"
COLOR_WEEK_TILE_CLOSED_BG = "#E6B7B7"
COLOR_WEEK_TILE_SELECTED_BORDER = "#4F46A5"
COLOR_WEEK_BLOCK_SUMMER_BG = "#F2ABAB"
COLOR_WEEK_BLOCK_WINTER_BG = "#E6B3C4"
COLOR_WEEK_BLOCK_BORDER = "#D98787"
COLOR_ENTRY_TABS_BG = "#EFEFEF"
COLOR_ENTRY_TAB_SELECTED_UNDERLINE = "#6D5BD6"
COLOR_CENTER_BG = "#E6E6E6"
COLOR_BOTTOM_BAR_BG = "#36B7E6"
COLOR_TEXT_PRIMARY = "#111111"
COLOR_TEXT_MUTED = "#555555"
COLOR_TEXT_DIMMED = "#7A6E6E"
COLOR_WHITE = "#FFFFFF"
COLOR_ERROR_TEXT = "#8A1F1F"


def build_main_shell_view(state: MainShellState) -> ft.Control:
    data = state.build_view_data()
    return ft.Pagelet(
        expand=True,
        appbar=ft.AppBar(
            toolbar_height=TOP_BAR_HEIGHT,
            automatically_imply_leading=False,
            leading_width=0,
            title_spacing=0,
            elevation=0,
            force_material_transparency=True,
            bgcolor=COLOR_TOP_BAR_BG,
            title=_build_top_temporal_bar(data, state),
        ),
        bottom_appbar=ft.BottomAppBar(
            height=BOTTOM_BAR_HEIGHT,
            padding=ft.Padding(left=16, top=12, right=16, bottom=12),
            elevation=0,
            bgcolor=COLOR_BOTTOM_BAR_BG,
            content=_build_status_bar(data, state),
        ),
        content=ft.Container(
            expand=True,
            bgcolor=COLOR_CENTER_BG,
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    _build_entry_tabs_bar(data, state),
                    ft.Container(expand=True, content=_build_center_panel(data, state)),
                ],
            ),
        ),
    )


def _build_top_temporal_bar(data: MainShellViewData, state: MainShellState) -> ft.Control:
    selected_year = data.state.selected_year
    has_valid_selected_year = selected_year is not None and selected_year in data.years
    if has_valid_selected_year:
        year_index = data.years.index(selected_year)
        has_prev_year = year_index > 0
        has_next_year = year_index < len(data.years) - 1
        is_last_year = year_index == len(data.years) - 1
        year_title = f"AÃ±o {selected_year}"
    else:
        has_prev_year = False
        has_next_year = False
        is_last_year = False
        year_title = "AÃ±o -"

    left_year_action = state.on_prev_year if has_prev_year and not data.campaign_write_pending else None
    if not has_valid_selected_year:
        right_year_label = ">"
        right_year_action = None
    elif is_last_year:
        right_year_label = "+"
        right_year_action = (
            state.on_open_extend_year_plus_one_confirm if not data.campaign_write_pending else None
        )
    else:
        right_year_label = ">"
        right_year_action = state.on_next_year if has_next_year and not data.campaign_write_pending else None

    week_strip_content: ft.Control
    if data.read_status == "error" and not data.weeks_for_selected_year:
        week_strip_content = ft.Text(
            "Weeks no disponibles (error de lectura)",
            size=13,
            color=COLOR_ERROR_TEXT,
            italic=True,
        )
    elif not data.weeks_for_selected_year:
        week_strip_content = ft.Text(
            "Sin weeks para el aÃ±o visible",
            size=13,
            color=COLOR_TEXT_MUTED,
            italic=True,
        )
    else:
        summer_weeks, winter_weeks = _split_weeks_into_season_blocks(data.weeks_for_selected_year)
        season_blocks: list[ft.Control] = []
        if summer_weeks:
            season_blocks.append(
                _build_week_season_block(
                    weeks=summer_weeks,
                    selected_week=data.state.selected_week,
                    disabled=data.campaign_write_pending,
                    on_select_week_click=state.on_select_week_click,
                    block_bgcolor=COLOR_WEEK_BLOCK_SUMMER_BG,
                )
            )
        if winter_weeks:
            season_blocks.append(
                _build_week_season_block(
                    weeks=winter_weeks,
                    selected_week=data.state.selected_week,
                    disabled=data.campaign_write_pending,
                    on_select_week_click=state.on_select_week_click,
                    block_bgcolor=COLOR_WEEK_BLOCK_WINTER_BG,
                )
            )

        week_strip_content = ft.Row(
            spacing=8,
            wrap=False,
            scroll=ft.ScrollMode.AUTO,
            controls=season_blocks,
        )

    year_group = ft.Row(
        spacing=12,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            _build_year_nav_button("<", left_year_action),
            ft.Text(
                year_title,
                size=42,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT_PRIMARY,
            ),
            _build_year_nav_button(right_year_label, right_year_action),
        ],
    )

    return ft.Container(
        padding=ft.Padding(left=12, top=10, right=12, bottom=10),
        content=ft.Row(
            spacing=16,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                year_group,
                ft.Container(
                    expand=True,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    content=week_strip_content,
                ),
            ],
        ),
    )


def _split_weeks_into_season_blocks(weeks_for_selected_year: list[WeekSummary]) -> tuple[list[WeekSummary], list[WeekSummary]]:
    if not weeks_for_selected_year:
        return [], []
    if len(weeks_for_selected_year) <= 10:
        return weeks_for_selected_year, []
    return weeks_for_selected_year[:10], weeks_for_selected_year[10:]


def _build_week_season_block(
    *,
    weeks: list[WeekSummary],
    selected_week: int | None,
    disabled: bool,
    on_select_week_click: ft.OptionalEventCallable["ControlEvent"],
    block_bgcolor: str,
) -> ft.Control:
    return ft.Container(
        bgcolor=block_bgcolor,
        border=ft.Border.all(1, COLOR_WEEK_BLOCK_BORDER),
        border_radius=6,
        padding=ft.Padding(left=4, top=4, right=4, bottom=4),
        content=ft.Row(
            spacing=6,
            controls=[
                _build_week_tile(
                    week=week,
                    is_selected=week.week_number == selected_week,
                    disabled=disabled,
                    on_select_week_click=on_select_week_click,
                )
                for week in weeks
            ],
        ),
    )


def _build_year_nav_button(
    label: str,
    on_click: ft.OptionalEventCallable["ControlEvent"],
) -> ft.Control:
    enabled = on_click is not None
    return ft.Container(
        width=52,
        height=52,
        border_radius=999,
        bgcolor=COLOR_TOP_NAV_BUTTON_BG if enabled else COLOR_TOP_NAV_BUTTON_DISABLED_BG,
        alignment=ft.Alignment.CENTER,
        on_click=on_click,
        content=ft.Text(
            label,
            size=24,
            weight=ft.FontWeight.BOLD,
            color=COLOR_WHITE if enabled else "#ECEBFF",
        ),
    )


def _build_week_tile(
    *,
    week: WeekSummary,
    is_selected: bool,
    disabled: bool,
    on_select_week_click: ft.OptionalEventCallable["ControlEvent"],
) -> ft.Control:
    border = ft.Border.all(2, COLOR_WEEK_TILE_SELECTED_BORDER) if is_selected else None
    bgcolor = COLOR_WEEK_TILE_CLOSED_BG if week.is_closed else COLOR_WEEK_TILE_BG
    text_color = COLOR_TEXT_DIMMED if week.is_closed else COLOR_TEXT_PRIMARY
    return ft.Container(
        width=46,
        height=42,
        bgcolor=bgcolor,
        border=border,
        border_radius=2,
        alignment=ft.Alignment.CENTER,
        data=week.week_number,
        on_click=None if disabled else on_select_week_click,
        content=ft.Text(
            str(week.week_number),
            size=13,
            weight=ft.FontWeight.W_600,
            color=text_color,
        ),
    )


def _build_entry_tabs_bar(data: MainShellViewData, state: MainShellState) -> ft.Control:
    content: ft.Control
    if data.state.selected_week is None:
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ft.Text("Selecciona una week para ver entries", size=13, color=COLOR_TEXT_MUTED, italic=True)],
        )
    elif data.entries_panel_error_message:
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ft.Text(f"Error Q5: {data.entries_panel_error_message}", size=12, color=COLOR_ERROR_TEXT)],
        )
    elif not data.entries_for_selected_week:
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ft.Text(f"Week {data.state.selected_week} sin entries", size=13, color=COLOR_TEXT_MUTED, italic=True)],
        )
    else:
        selected_ref = (
            data.viewer_entry.ref
            if data.viewer_entry is not None and entry_ref_matches_selected_week(data.state, data.viewer_entry.ref)
            else None
        )
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=8,
            controls=[
                _build_entry_tab(
                    entry=entry,
                    is_selected=selected_ref == entry.ref,
                    on_select_entry_click=state.on_select_entry_click,
                )
                for entry in data.entries_for_selected_week
            ],
        )

    return ft.Container(
        height=ENTRY_TABS_BAR_HEIGHT,
        bgcolor=COLOR_ENTRY_TABS_BG,
        padding=ft.Padding(left=16, top=4, right=16, bottom=4),
        content=content,
    )


def _build_entry_tab(
    *,
    entry: EntrySummary,
    is_selected: bool,
    on_select_entry_click: ft.OptionalEventCallable["ControlEvent"],
) -> ft.Control:
    underline_color = COLOR_ENTRY_TAB_SELECTED_UNDERLINE if is_selected else "transparent"
    text_weight = ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL
    underline_width = max(36, min(180, len(entry.label) * 7))
    return ft.Container(
        data=entry.ref,
        on_click=on_select_entry_click,
        padding=ft.Padding(left=12, top=6, right=12, bottom=2),
        content=ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(entry.label, size=13, color=COLOR_TEXT_PRIMARY, weight=text_weight),
                ft.Container(width=underline_width, height=2, bgcolor=underline_color, border_radius=1),
            ],
        ),
    )


def _build_center_panel(data: MainShellViewData, state: MainShellState) -> ft.Control:
    controls: list[ft.Control] = []

    if data.read_error_message:
        controls.append(_build_banner("Error de lectura", data.read_error_message, "#FFE7E7", "#D87A7A", "#8A1F1F"))
    if data.read_warning_message:
        controls.append(
            _build_banner("Advertencia", data.read_warning_message, "#FFF4D8", "#D0A55E", "#7D5700")
        )
    if data.info_message:
        controls.append(_build_banner("Info", data.info_message, "#E8F4FF", "#90C4E8", "#0E5E78"))
    if data.confirmation is not None:
        controls.append(_build_confirmation_card(data, state))
    if data.week_notes_editor is not None:
        controls.append(_build_week_notes_editor(data, state))
    if data.entry_form is not None:
        controls.append(_build_entry_form_editor(data, state))
    if data.session_form is not None:
        controls.append(_build_session_form_editor(data, state))

    selected_week = _find_selected_week(data)
    if data.viewer_entry is not None:
        controls.append(_build_focus_entry_mode(data, state))
    elif selected_week is not None:
        controls.append(_build_focus_week_mode(data, state, selected_week))
    else:
        controls.append(_build_focus_empty_mode(data))

    return ft.Container(
        expand=True,
        bgcolor=COLOR_CENTER_BG,
        padding=ft.Padding.all(16),
        content=ft.ListView(
            expand=True,
            spacing=12,
            padding=0,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            scroll=ft.ScrollMode.AUTO,
            controls=controls,
        ),
    )


def _build_banner(title: str, body: str, background: str, border_color: str, foreground: str) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor=background,
        border=ft.Border.all(1, border_color),
        border_radius=8,
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=foreground),
                ft.Text(body, size=12, color=foreground),
            ],
        ),
    )


def _build_confirmation_card(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.confirmation is not None
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#FFF4D8",
        border=ft.Border.all(1, "#D0A55E"),
        border_radius=8,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(data.confirmation.title, size=15, weight=ft.FontWeight.BOLD, color="#7D5700"),
                ft.Text(data.confirmation.body, size=13, color="#7D5700"),
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.TextButton("Cancelar", on_click=state.on_cancel_pending_action),
                        ft.FilledButton(data.confirmation.confirm_label, on_click=state.on_confirm_pending_action),
                    ],
                ),
            ],
        ),
    )


def _build_week_notes_editor(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.week_notes_editor is not None
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border=ft.Border.all(1, "#D6D6D6"),
        border_radius=8,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text("Editar notas de week", size=14, weight=ft.FontWeight.BOLD),
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
        ),
    )


def _build_entry_form_editor(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.entry_form is not None
    is_scenario = data.entry_form.entry_type == "scenario"
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border=ft.Border.all(1, "#D6D6D6"),
        border_radius=8,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    "Crear entry" if data.entry_form.mode == "create" else "Editar entry",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Dropdown(
                    value=data.entry_form.entry_type,
                    options=[
                        ft.dropdown.Option("scenario"),
                        ft.dropdown.Option("outpost"),
                    ],
                    on_change=state.on_entry_form_set_type,
                ),
                ft.TextField(
                    label="Scenario ref",
                    value=data.entry_form.scenario_ref_text,
                    on_change=state.on_entry_form_set_scenario_ref,
                    disabled=not is_scenario,
                    hint_text="Entero positivo" if is_scenario else "No aplica para outpost",
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
        ),
    )


def _build_session_form_editor(data: MainShellViewData, state: MainShellState) -> ft.Control:
    assert data.session_form is not None
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border=ft.Border.all(1, "#D6D6D6"),
        border_radius=8,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    "Crear sesiÃ³n manual" if data.session_form.mode == "create" else "Editar sesiÃ³n",
                    size=14,
                    weight=ft.FontWeight.BOLD,
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
                    label="SesiÃ³n activa (sin fin)",
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
        ),
    )


def _build_focus_empty_mode(data: MainShellViewData) -> ft.Control:
    return _build_card(
        title="Sin week seleccionada",
        body=(
            "Navega por las weeks del aÃ±o visible y selecciona una entry para mostrarla en el visor.\n"
            + _format_navigation_line(data)
        ),
    )


def _build_focus_week_mode(data: MainShellViewData, state: MainShellState, week: WeekSummary) -> ft.Control:
    action_buttons: list[ft.Control] = [
        ft.FilledButton("Nueva entry", on_click=state.on_open_entry_add_modal, disabled=data.entry_write_pending, height=32),
        ft.OutlinedButton("Editar notas", on_click=state.on_open_week_notes_modal, disabled=data.week_write_pending, height=32),
    ]
    if week.is_closed:
        action_buttons.append(
            ft.FilledButton("Reopen", on_click=state.on_request_week_reopen, disabled=data.week_write_pending, height=32)
        )
    else:
        action_buttons.extend(
            [
                ft.FilledButton("Close", on_click=state.on_request_week_close, disabled=data.week_write_pending, height=32),
                ft.OutlinedButton("Reclose", on_click=state.on_request_week_reclose, disabled=data.week_write_pending, height=32),
            ]
        )

    body_lines = [f"Estado: {week.status_label}", f"Notas: {week.notes_preview or 'Sin notas'}"]
    if data.week_write_error_message:
        body_lines.append(f"Error week: {data.week_write_error_message}")
    if data.entry_write_error_message:
        body_lines.append(f"Error entry: {data.entry_write_error_message}")
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border=ft.Border.all(1, "#D6D6D6"),
        border_radius=8,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(f"Week {week.week_number}", size=22, weight=ft.FontWeight.BOLD),
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
        f"Viendo: {viewer_entry.label} Â· Week {viewer_entry.ref.week_number} Â· AÃ±o {viewer_entry.ref.year_number}",
        _format_navigation_line(data),
    ]
    if not viewer_matches_selected_week:
        context_lines.append("Visor sticky: la entry visible no coincide con la week navegada.")

    detail_lines = [f"Tipo: {viewer_entry.entry_type}"]
    if viewer_entry.scenario_ref is not None:
        detail_lines.append(f"Scenario ref: {viewer_entry.scenario_ref}")
    if viewer_entry.order_index is not None:
        detail_lines.append(f"Order index: {viewer_entry.order_index}")
    if viewer_entry.resource_deltas:
        detail_lines.append(
            "resource_deltas: "
            + ", ".join(f"{k}={v}" for k, v in sorted(viewer_entry.resource_deltas.items(), key=lambda item: item[0]))
        )
    else:
        detail_lines.append("resource_deltas: sin cambios")

    return ft.Column(
        spacing=12,
        controls=[
            _build_card(
                title=f"Week {viewer_entry.ref.week_number} Â· {viewer_entry.label}",
                body="\n".join(context_lines),
            ),
            _build_card(
                title="Detalle entry",
                body="\n".join(detail_lines),
            ),
            _build_entry_actions_card(data, state),
            _build_sessions_card(data, state, active_here=active_here),
            _build_resources_card(data, state),
        ],
    )


def _build_entry_actions_card(data: MainShellViewData, state: MainShellState) -> ft.Control:
    info_lines: list[str] = ["Crear usa la week seleccionada; editar/reordenar/borrar operan sobre la entry visible."]
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
                ft.Text("Acciones de entry", size=14, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
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
        session_status_text = "Sin sesiÃ³n activa real."
    elif active_here:
        session_status_text = f"Con sesiÃ³n activa aquÃ­: {data.active_entry_label or 'Entry activa'}."
    else:
        session_status_text = f"Con sesiÃ³n activa en otra entry: {data.active_entry_label or 'Entry activa'}."

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
        rows.append(ft.Text(f"â€¦ y {len(data.viewer_sessions) - 8} sesiÃ³n(es) mÃ¡s", size=11, color=COLOR_TEXT_MUTED))

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
                        ft.FilledButton("Start", on_click=state.on_begin_session, disabled=data.session_write_pending, height=32),
                        ft.OutlinedButton(
                            "Stop",
                            on_click=state.on_end_session,
                            disabled=data.session_write_pending or not has_active_session,
                            height=32,
                        ),
                        ft.OutlinedButton(
                            "Nueva sesiÃ³n",
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
            ft.Text(f"Delta neto entry (ediciÃ³n): {current_value}", size=11, color=COLOR_TEXT_MUTED),
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
                                    height=32,
                                ),
                                ft.FilledButton(
                                    "+1",
                                    data=(resource_key, 1),
                                    on_click=state.on_adjust_resource_draft_delta_click,
                                    disabled=draft_controls_disabled,
                                    height=32,
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )

    header_lines = ["Los cambios se editan localmente y se persisten al pulsar Guardar."]
    if data.resource_write_error_message:
        header_lines.append(f"Error: {data.resource_write_error_message}")
    elif data.resource_draft_attached_to_viewer:
        header_lines.append("Cambios sin guardar" if data.resource_draft_dirty else "Sin cambios locales pendientes")
    else:
        header_lines.append("Borrador no disponible para la entry visible.")

    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border_radius=8,
        border=ft.Border.all(1, "#D6D6D6"),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text("Recursos de la entry", size=14, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                ft.Text("\n".join(header_lines), size=12, color=COLOR_TEXT_MUTED),
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


def _build_card(title: str, body: str) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border_radius=8,
        border=ft.Border.all(1, "#D6D6D6"),
        content=ft.Column(
            spacing=6,
            controls=[
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                ft.Container(
                    padding=ft.Padding.all(8),
                    bgcolor="#FFFFFF",
                    border_radius=6,
                    content=ft.Text(body, size=13, color=COLOR_TEXT_MUTED),
                ),
            ],
        ),
    )


def _build_status_bar(data: MainShellViewData, state: MainShellState) -> ft.Control:
    active_text, active_detail_text = _active_status_texts(data)
    viewer_text = (
        f"Viendo: {data.viewer_entry.label} (W{data.viewer_entry.ref.week_number})"
        if data.viewer_entry is not None
        else "Sin entry en visor"
    )
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Text("Totales (read-only)", size=16, weight=ft.FontWeight.BOLD, color=COLOR_WHITE),
                    ft.Text(_format_resource_totals(data.campaign_resource_totals), size=12, color="#EAF9FF"),
                ],
            ),
            ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        controls=[
                            ft.Text(active_text, size=13, weight=ft.FontWeight.BOLD, color=COLOR_WHITE, text_align=ft.TextAlign.RIGHT),
                            ft.Text(active_detail_text or viewer_text, size=12, color="#EAF9FF", text_align=ft.TextAlign.RIGHT),
                            ft.Text(f"{viewer_text} Â· env={data.env_name}", size=11, color="#DDF5FF", text_align=ft.TextAlign.RIGHT),
                        ],
                    ),
                    ft.Column(
                        spacing=6,
                        controls=[
                            ft.OutlinedButton("Actualizar", on_click=state.on_manual_refresh),
                            ft.FilledButton("+ AÃ±o", on_click=state.on_open_extend_year_plus_one_confirm),
                        ],
                    ),
                ],
            ),
        ],
    )


def _active_status_texts(data: MainShellViewData) -> tuple[str, str]:
    if data.active_status_error_message:
        return ("Estado activo no disponible", data.active_status_error_message)
    if data.active_entry_ref is None:
        return ("Sin sesiÃ³n activa", "")
    label = data.active_entry_label or f"Entry {data.active_entry_ref.entry_id}"
    if data.viewer_entry is not None and data.viewer_entry.ref == data.active_entry_ref:
        return (f"Con sesiÃ³n activa: {label} Â· aquÃ­", "")
    return (f"Con sesiÃ³n activa: {label} Â· en otra entry", "")


def _format_resource_totals(resource_totals: dict[str, int] | None) -> str:
    if resource_totals is None:
        return "Totales no disponibles (Q1 no cargado)"
    if not resource_totals:
        return "Sin recursos materializados"
    items = sorted(resource_totals.items(), key=lambda item: item[0])
    visible = [f"{key}={value}" for key, value in items[:4]]
    suffix = " ..." if len(items) > 4 else ""
    return " Â· ".join(visible) + suffix


def _find_selected_week(data: MainShellViewData) -> WeekSummary | None:
    if data.state.selected_week is None:
        return None
    for week in data.weeks_for_selected_year:
        if week.week_number == data.state.selected_week:
            return week
    return None


def _format_navigation_line(data: MainShellViewData) -> str:
    if data.state.selected_year is None:
        return "NavegaciÃ³n actual: sin aÃ±o seleccionado"
    if data.state.selected_week is None:
        return f"NavegaciÃ³n actual: AÃ±o {data.state.selected_year} Â· sin week seleccionada"
    return f"NavegaciÃ³n actual: AÃ±o {data.state.selected_year} Â· Week {data.state.selected_week}"


def _sum_finished_sessions_duration(sessions: list[object]) -> timedelta | None:
    total = timedelta()
    has_finished = False
    for session in sessions:
        started = _as_datetime(getattr(session, "started_at_utc", None))
        ended = _as_datetime(getattr(session, "ended_at_utc", None))
        if started is None or ended is None or ended < started:
            continue
        total += ended - started
        has_finished = True
    return total if has_finished else None


def _as_datetime(value: object | None) -> datetime | None:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    return None


def _format_duration(duration: timedelta | None) -> str:
    if duration is None:
        return "0 min"
    total_seconds = int(duration.total_seconds())
    if total_seconds < 0:
        total_seconds = 0
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{hours}h {minutes:02d}m" if hours else f"{minutes} min"


def _format_session_line(session: object) -> str:
    session_id = getattr(session, "session_id", "n/d")
    started = _format_dt_short(getattr(session, "started_at_utc", None))
    ended_raw = getattr(session, "ended_at_utc", None)
    if ended_raw is None:
        return f"{session_id}: {started} -> activa"
    ended = _format_dt_short(ended_raw)
    duration = _session_duration(session)
    duration_text = _format_duration(duration) if duration is not None else "duraciÃ³n n/d"
    return f"{session_id}: {started} -> {ended} Â· {duration_text}"


def _session_duration(session: object) -> timedelta | None:
    started = _as_datetime(getattr(session, "started_at_utc", None))
    ended = _as_datetime(getattr(session, "ended_at_utc", None))
    if started is None or ended is None or ended < started:
        return None
    return ended - started


def _format_dt_short(value: object | None) -> str:
    dt = _as_datetime(value)
    if dt is None:
        return "n/d"
    return dt.astimezone().strftime("%Y-%m-%d %H:%M")

