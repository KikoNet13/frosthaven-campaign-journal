from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Callable

import flet as ft

from frosthaven_campaign_journal.state.placeholders import (
    EntryRef,
    MainScreenLocalState,
    MockEntry,
    MockWeek,
    ViewerSessionItem,
)


TOP_BAR_HEIGHT = 64
ENTRY_TABS_BAR_HEIGHT = 44
BOTTOM_BAR_HEIGHT = 96
OUTER_PADDING = 0
CENTER_PANEL_PADDING = 16

COLOR_TOP_BAR_BG = "#F39A9A"
COLOR_TOP_NAV_BUTTON_BG = "#5F58C8"
COLOR_TOP_NAV_BUTTON_DISABLED_BG = "#8E88D8"
COLOR_WEEK_TILE_BG = "#F4A0A0"
COLOR_WEEK_TILE_CLOSED_BG = "#E6B7B7"
COLOR_WEEK_TILE_SELECTED_BORDER = "#4F46A5"
COLOR_ENTRY_TABS_BG = "#EFEFEF"
COLOR_ENTRY_TAB_SELECTED_UNDERLINE = "#6D5BD6"
COLOR_CENTER_BG = "#E6E6E6"
COLOR_BOTTOM_BAR_BG = "#36B7E6"
COLOR_TEXT_PRIMARY = "#111111"
COLOR_TEXT_MUTED = "#555555"
COLOR_TEXT_DIMMED = "#7A6E6E"
COLOR_WHITE = "#FFFFFF"
COLOR_ERROR_BG = "#FFE7E7"
COLOR_ERROR_BORDER = "#D87A7A"
COLOR_ERROR_TEXT = "#8A1F1F"
COLOR_WARNING_BG = "#FFF4D8"
COLOR_WARNING_BORDER = "#D0A55E"
COLOR_WARNING_TEXT = "#7D5700"
COLOR_WEEK_BLOCK_SUMMER_BG = "#F2ABAB"
COLOR_WEEK_BLOCK_WINTER_BG = "#E6B3C4"
COLOR_WEEK_BLOCK_BORDER = "#D98787"
ENTRY_RESOURCE_KEYS = ("lumber", "metal", "hide")


def build_main_shell_view(
    *,
    state: MainScreenLocalState,
    years: list[int],
    weeks_for_selected_year: list[MockWeek],
    entries_for_selected_week: list[MockEntry],
    viewer_entry: MockEntry | None,
    viewer_sessions: list[ViewerSessionItem],
    entries_panel_error_message: str | None,
    viewer_sessions_error_message: str | None,
    session_write_error_message: str | None,
    session_write_pending: bool,
    week_write_error_message: str | None,
    week_write_pending: bool,
    entry_write_error_message: str | None,
    entry_write_pending: bool,
    resource_write_error_message: str | None,
    resource_write_pending: bool,
    campaign_write_pending: bool,
    resource_draft_values: dict[str, int] | None,
    resource_draft_dirty: bool,
    resource_draft_attached_to_viewer: bool,
    active_entry_ref: EntryRef | None,
    active_entry_label: str | None,
    active_status_error_message: str | None,
    campaign_resource_totals: dict[str, int] | None,
    read_status: str,
    read_error_message: str | None,
    read_warning_message: str | None,
    viewport_width: int | float | None,
    viewport_height: int | float | None,
    env_name: str,
    on_prev_year: Callable[[], None],
    on_next_year: Callable[[], None],
    on_open_extend_year_plus_one_confirm: Callable[[], None],
    on_select_week: Callable[[int], None],
    on_select_entry: Callable[[EntryRef], None],
    on_manual_refresh: Callable[[], None],
    on_start_session: Callable[[], None],
    on_stop_session: Callable[[], None],
    on_open_manual_create_session: Callable[[], None],
    on_open_manual_edit_session: Callable[[str], None],
    on_open_manual_delete_session: Callable[[str], None],
    on_open_week_notes_modal: Callable[[], None],
    on_request_close_week: Callable[[], None],
    on_request_reopen_week: Callable[[], None],
    on_request_reclose_week: Callable[[], None],
    on_open_create_entry_modal: Callable[[], None],
    on_open_edit_entry_modal: Callable[[], None],
    on_open_delete_entry_confirm: Callable[[], None],
    on_reorder_entry_up: Callable[[], None],
    on_reorder_entry_down: Callable[[], None],
    on_adjust_resource_draft_delta: Callable[[str, int], None],
    on_save_resource_draft: Callable[[], None],
    on_discard_resource_draft: Callable[[], None],
) -> ft.Control:
    top_bar = _build_top_temporal_bar(
        state=state,
        years=years,
        weeks_for_selected_year=weeks_for_selected_year,
        read_status=read_status,
        read_error_message=read_error_message,
        campaign_write_pending=campaign_write_pending,
        on_prev_year=on_prev_year,
        on_next_year=on_next_year,
        on_open_extend_year_plus_one_confirm=on_open_extend_year_plus_one_confirm,
        on_select_week=on_select_week,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        embedded_in_appbar=True,
    )
    entry_tabs_bar = _build_entry_tabs_bar(
        state=state,
        entries_for_selected_week=entries_for_selected_week,
        viewer_entry=viewer_entry,
        entries_panel_error_message=entries_panel_error_message,
        on_select_entry=on_select_entry,
    )
    center_panel = _build_center_focus_panel(
        state=state,
        weeks_for_selected_year=weeks_for_selected_year,
        viewer_entry=viewer_entry,
        viewer_sessions=viewer_sessions,
        viewer_sessions_error_message=viewer_sessions_error_message,
        session_write_error_message=session_write_error_message,
        session_write_pending=session_write_pending,
        week_write_error_message=week_write_error_message,
        week_write_pending=week_write_pending,
        entry_write_error_message=entry_write_error_message,
        entry_write_pending=entry_write_pending,
        resource_write_error_message=resource_write_error_message,
        resource_write_pending=resource_write_pending,
        resource_draft_values=resource_draft_values,
        resource_draft_dirty=resource_draft_dirty,
        resource_draft_attached_to_viewer=resource_draft_attached_to_viewer,
        active_entry_ref=active_entry_ref,
        active_entry_label=active_entry_label,
        read_error_message=read_error_message,
        read_warning_message=read_warning_message,
        on_start_session=on_start_session,
        on_stop_session=on_stop_session,
        on_open_manual_create_session=on_open_manual_create_session,
        on_open_manual_edit_session=on_open_manual_edit_session,
        on_open_manual_delete_session=on_open_manual_delete_session,
        on_open_week_notes_modal=on_open_week_notes_modal,
        on_request_close_week=on_request_close_week,
        on_request_reopen_week=on_request_reopen_week,
        on_request_reclose_week=on_request_reclose_week,
        on_open_create_entry_modal=on_open_create_entry_modal,
        on_open_edit_entry_modal=on_open_edit_entry_modal,
        on_open_delete_entry_confirm=on_open_delete_entry_confirm,
        on_reorder_entry_up=on_reorder_entry_up,
        on_reorder_entry_down=on_reorder_entry_down,
        on_adjust_resource_draft_delta=on_adjust_resource_draft_delta,
        on_save_resource_draft=on_save_resource_draft,
        on_discard_resource_draft=on_discard_resource_draft,
    )
    bottom_bar_content = _build_bottom_status_bar_content(
        env_name=env_name,
        viewer_entry=viewer_entry,
        active_entry_ref=active_entry_ref,
        active_entry_label=active_entry_label,
        active_status_error_message=active_status_error_message,
        campaign_resource_totals=campaign_resource_totals,
        on_manual_refresh=on_manual_refresh,
    )
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
            title=top_bar,
        ),
        bottom_appbar=ft.BottomAppBar(
            height=BOTTOM_BAR_HEIGHT,
            padding=ft.Padding(left=16, top=12, right=16, bottom=12),
            elevation=0,
            bgcolor=COLOR_BOTTOM_BAR_BG,
            content=bottom_bar_content,
        ),
        content=ft.Container(
            expand=True,
            padding=OUTER_PADDING,
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    entry_tabs_bar,
                    ft.Container(expand=True, content=center_panel),
                ],
            ),
        ),
    )


def _build_top_temporal_bar(
    *,
    state: MainScreenLocalState,
    years: list[int],
    weeks_for_selected_year: list[MockWeek],
    read_status: str,
    read_error_message: str | None,
    campaign_write_pending: bool,
    on_prev_year: Callable[[], None],
    on_next_year: Callable[[], None],
    on_open_extend_year_plus_one_confirm: Callable[[], None],
    on_select_week: Callable[[int], None],
    viewport_width: int | float | None,
    viewport_height: int | float | None,
    embedded_in_appbar: bool = False,
) -> ft.Control:
    selected_year = state.selected_year
    has_valid_selected_year = selected_year is not None and selected_year in years
    if has_valid_selected_year:
        year_index = years.index(selected_year)
        has_prev_year = year_index > 0
        has_next_year = year_index < len(years) - 1
        is_last_year = year_index == len(years) - 1
        year_title = f"Año {selected_year}"
    else:
        has_prev_year = False
        has_next_year = False
        is_last_year = False
        year_title = "Año -"

    left_year_action = on_prev_year if has_prev_year and not campaign_write_pending else None
    if not has_valid_selected_year:
        right_year_label = "→"
        right_year_action = None
    elif is_last_year:
        right_year_label = "+"
        right_year_action = (
            on_open_extend_year_plus_one_confirm if not campaign_write_pending else None
        )
    else:
        right_year_label = "→"
        right_year_action = on_next_year if has_next_year and not campaign_write_pending else None

    is_mobile_landscape_topbar = _is_mobile_landscape_topbar(
        viewport_width=viewport_width,
        viewport_height=viewport_height,
    )
    year_group_spacing = 8 if is_mobile_landscape_topbar else 12
    content_row_spacing = 8 if is_mobile_landscape_topbar else 16
    year_title_size = 24 if is_mobile_landscape_topbar else 32
    year_nav_button_size = 38 if is_mobile_landscape_topbar else 42
    year_nav_font_size = 18 if is_mobile_landscape_topbar else 20
    week_block_spacing = 6 if is_mobile_landscape_topbar else 8
    week_tile_gap = 4 if is_mobile_landscape_topbar else 6

    if read_status == "error" and not weeks_for_selected_year:
        week_strip_content: ft.Control = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Weeks no disponibles (error de lectura)",
                    size=13,
                    color=COLOR_ERROR_TEXT,
                    italic=True,
                ),
            ],
        )
    elif not weeks_for_selected_year:
        week_strip_content = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Sin weeks para el año visible",
                    size=13,
                    color=COLOR_TEXT_MUTED,
                    italic=True,
                ),
            ],
        )
    else:
        summer_weeks, winter_weeks = _split_weeks_into_season_blocks(weeks_for_selected_year)
        season_blocks: list[ft.Control] = []
        if summer_weeks:
            season_blocks.append(
                _build_week_season_block(
                    weeks=summer_weeks,
                    state=state,
                    on_select_week=on_select_week,
                    disabled=campaign_write_pending,
                    block_bgcolor=COLOR_WEEK_BLOCK_SUMMER_BG,
                    tile_spacing=week_tile_gap,
                )
            )
        if winter_weeks:
            season_blocks.append(
                _build_week_season_block(
                    weeks=winter_weeks,
                    state=state,
                    on_select_week=on_select_week,
                    disabled=campaign_write_pending,
                    block_bgcolor=COLOR_WEEK_BLOCK_WINTER_BG,
                    tile_spacing=week_tile_gap,
                )
            )

        week_strip_content = ft.Container(
            expand=True,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Row(
                spacing=week_block_spacing,
                wrap=False,
                scroll=ft.ScrollMode.AUTO,
                controls=season_blocks,
            ),
        )

    tooltip = read_error_message if read_status == "error" else None

    year_group = ft.Row(
        spacing=year_group_spacing,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            _build_year_nav_button(
                "←",
                left_year_action,
                size=year_nav_button_size,
                font_size=year_nav_font_size,
            ),
            ft.Text(
                year_title,
                size=year_title_size,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT_PRIMARY,
            ),
            _build_year_nav_button(
                right_year_label,
                right_year_action,
                size=year_nav_button_size,
                font_size=year_nav_font_size,
            ),
        ],
    )

    content = ft.Row(
        spacing=content_row_spacing,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            year_group,
            ft.Container(expand=True, content=week_strip_content),
        ],
    )

    if embedded_in_appbar:
        return ft.Container(
            padding=ft.Padding(left=12, top=10, right=12, bottom=10),
            tooltip=tooltip,
            content=content,
        )

    return ft.Container(
        height=TOP_BAR_HEIGHT,
        bgcolor=COLOR_TOP_BAR_BG,
        padding=ft.Padding(left=12, top=10, right=12, bottom=10),
        tooltip=tooltip,
        content=content,
    )


def _is_mobile_landscape_topbar(
    *,
    viewport_width: int | float | None,
    viewport_height: int | float | None,
) -> bool:
    if not isinstance(viewport_width, (int, float)) or not isinstance(viewport_height, (int, float)):
        return False
    if viewport_width <= 0 or viewport_height <= 0:
        return False
    return viewport_width > viewport_height and viewport_width <= 700


def _split_weeks_into_season_blocks(
    weeks_for_selected_year: list[MockWeek],
) -> tuple[list[MockWeek], list[MockWeek]]:
    if not weeks_for_selected_year:
        return [], []
    if len(weeks_for_selected_year) <= 10:
        return weeks_for_selected_year, []
    if len(weeks_for_selected_year) >= 20:
        return weeks_for_selected_year[:10], weeks_for_selected_year[10:]
    split_index = min(10, (len(weeks_for_selected_year) + 1) // 2)
    return weeks_for_selected_year[:split_index], weeks_for_selected_year[split_index:]


def _build_week_season_block(
    *,
    weeks: list[MockWeek],
    state: MainScreenLocalState,
    on_select_week: Callable[[int], None],
    disabled: bool,
    block_bgcolor: str,
    tile_spacing: int,
) -> ft.Control:
    return ft.Container(
        bgcolor=block_bgcolor,
        border=ft.Border.all(1, COLOR_WEEK_BLOCK_BORDER),
        border_radius=6,
        padding=ft.Padding(left=4, top=4, right=4, bottom=4),
        content=ft.Row(
            spacing=tile_spacing,
            wrap=False,
            controls=[
                _build_week_tile(
                    week=week,
                    is_selected=(week.week_number == state.selected_week),
                    on_select_week=on_select_week,
                    disabled=disabled,
                )
                for week in weeks
            ],
        ),
    )


def _build_year_nav_button(
    label: str,
    on_click: Callable[[], None] | None,
    *,
    size: int = 42,
    font_size: int = 20,
) -> ft.Control:
    enabled = on_click is not None
    return ft.Container(
        width=size,
        height=size,
        bgcolor=COLOR_TOP_NAV_BUTTON_BG if enabled else COLOR_TOP_NAV_BUTTON_DISABLED_BG,
        border_radius=999,
        alignment=ft.Alignment.CENTER,
        on_click=(lambda _e: on_click()) if on_click else None,
        content=ft.Text(
            label,
            size=font_size,
            weight=ft.FontWeight.BOLD,
            color=COLOR_WHITE if enabled else "#ECEBFF",
        ),
    )


def _build_week_tile(
    *,
    week: MockWeek,
    is_selected: bool,
    on_select_week: Callable[[int], None],
    disabled: bool = False,
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
        on_click=(
            None if disabled else (lambda _e, week_number=week.week_number: on_select_week(week_number))
        ),
        content=ft.Text(
            str(week.week_number),
            size=13,
            weight=ft.FontWeight.W_600,
            color=text_color,
        ),
    )


def _build_entry_tabs_bar(
    *,
    state: MainScreenLocalState,
    entries_for_selected_week: list[MockEntry],
    viewer_entry: MockEntry | None,
    entries_panel_error_message: str | None,
    on_select_entry: Callable[[EntryRef], None],
) -> ft.Control:
    if state.selected_week is None:
        content: ft.Control = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Selecciona una week para ver entries",
                    size=13,
                    color=COLOR_TEXT_MUTED,
                    italic=True,
                )
            ],
        )
    elif entries_panel_error_message:
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    _truncate(f"Error Q5: {entries_panel_error_message}", 140),
                    size=12,
                    color=COLOR_ERROR_TEXT,
                )
            ],
        )
    elif not entries_for_selected_week:
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    f"Week {state.selected_week} sin entries",
                    size=13,
                    color=COLOR_TEXT_MUTED,
                    italic=True,
                )
            ],
        )
    else:
        tab_selected_ref = (
            viewer_entry.ref if _viewer_matches_selected_week(state, viewer_entry) else None
        )
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=8,
            controls=[
                _build_entry_tab(
                    entry=entry,
                    is_selected=(tab_selected_ref == entry.ref),
                    on_select_entry=on_select_entry,
                )
                for entry in entries_for_selected_week
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
    entry: MockEntry,
    is_selected: bool,
    on_select_entry: Callable[[EntryRef], None],
) -> ft.Control:
    underline_color = COLOR_ENTRY_TAB_SELECTED_UNDERLINE if is_selected else "transparent"
    text_weight = ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL
    underline_width = max(36, min(140, len(entry.label) * 7))

    return ft.Container(
        padding=ft.Padding(left=12, top=6, right=12, bottom=2),
        on_click=lambda _e, ref=entry.ref: on_select_entry(ref),
        content=ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    entry.label,
                    size=13,
                    color=COLOR_TEXT_PRIMARY,
                    weight=text_weight,
                ),
                ft.Container(
                    width=underline_width,
                    height=2,
                    bgcolor=underline_color,
                    border_radius=1,
                ),
            ],
        ),
    )


def _build_center_focus_panel(
    *,
    state: MainScreenLocalState,
    weeks_for_selected_year: list[MockWeek],
    viewer_entry: MockEntry | None,
    viewer_sessions: list[ViewerSessionItem],
    viewer_sessions_error_message: str | None,
    session_write_error_message: str | None,
    session_write_pending: bool,
    week_write_error_message: str | None,
    week_write_pending: bool,
    entry_write_error_message: str | None,
    entry_write_pending: bool,
    resource_write_error_message: str | None,
    resource_write_pending: bool,
    resource_draft_values: dict[str, int] | None,
    resource_draft_dirty: bool,
    resource_draft_attached_to_viewer: bool,
    active_entry_ref: EntryRef | None,
    active_entry_label: str | None,
    read_error_message: str | None,
    read_warning_message: str | None,
    on_start_session: Callable[[], None],
    on_stop_session: Callable[[], None],
    on_open_manual_create_session: Callable[[], None],
    on_open_manual_edit_session: Callable[[str], None],
    on_open_manual_delete_session: Callable[[str], None],
    on_open_week_notes_modal: Callable[[], None],
    on_request_close_week: Callable[[], None],
    on_request_reopen_week: Callable[[], None],
    on_request_reclose_week: Callable[[], None],
    on_open_create_entry_modal: Callable[[], None],
    on_open_edit_entry_modal: Callable[[], None],
    on_open_delete_entry_confirm: Callable[[], None],
    on_reorder_entry_up: Callable[[], None],
    on_reorder_entry_down: Callable[[], None],
    on_adjust_resource_draft_delta: Callable[[str, int], None],
    on_save_resource_draft: Callable[[], None],
    on_discard_resource_draft: Callable[[], None],
) -> ft.Control:
    selected_week = _find_selected_week(state, weeks_for_selected_year)

    if viewer_entry is not None:
        primary_content = _build_focus_entry_mode(
            state=state,
            viewer_entry=viewer_entry,
            viewer_sessions=viewer_sessions,
            viewer_sessions_error_message=viewer_sessions_error_message,
            session_write_error_message=session_write_error_message,
            session_write_pending=session_write_pending,
            entry_write_error_message=entry_write_error_message,
            entry_write_pending=entry_write_pending,
            resource_write_error_message=resource_write_error_message,
            resource_write_pending=resource_write_pending,
            resource_draft_values=resource_draft_values,
            resource_draft_dirty=resource_draft_dirty,
            resource_draft_attached_to_viewer=resource_draft_attached_to_viewer,
            active_entry_ref=active_entry_ref,
            active_entry_label=active_entry_label,
            on_start_session=on_start_session,
            on_stop_session=on_stop_session,
            on_open_manual_create_session=on_open_manual_create_session,
            on_open_manual_edit_session=on_open_manual_edit_session,
            on_open_manual_delete_session=on_open_manual_delete_session,
            on_open_create_entry_modal=on_open_create_entry_modal,
            on_open_edit_entry_modal=on_open_edit_entry_modal,
            on_open_delete_entry_confirm=on_open_delete_entry_confirm,
            on_reorder_entry_up=on_reorder_entry_up,
            on_reorder_entry_down=on_reorder_entry_down,
            on_adjust_resource_draft_delta=on_adjust_resource_draft_delta,
            on_save_resource_draft=on_save_resource_draft,
            on_discard_resource_draft=on_discard_resource_draft,
        )
    elif selected_week is not None:
        primary_content = _build_focus_week_mode(
            selected_week,
            week_write_error_message=week_write_error_message,
            week_write_pending=week_write_pending,
            entry_write_error_message=entry_write_error_message,
            entry_write_pending=entry_write_pending,
            on_open_week_notes_modal=on_open_week_notes_modal,
            on_request_close_week=on_request_close_week,
            on_request_reopen_week=on_request_reopen_week,
            on_request_reclose_week=on_request_reclose_week,
            on_open_create_entry_modal=on_open_create_entry_modal,
        )
    else:
        primary_content = _build_focus_empty_mode(state)

    stacked_controls: list[ft.Control] = []
    if read_error_message:
        stacked_controls.append(
            _build_status_banner(
                title="Error de lectura (Firestore)",
                body=read_error_message,
                background=COLOR_ERROR_BG,
                border_color=COLOR_ERROR_BORDER,
                foreground=COLOR_ERROR_TEXT,
            )
        )
    if read_warning_message:
        stacked_controls.append(
            _build_status_banner(
                title="Advertencia de consistencia",
                body=read_warning_message,
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
            _build_placeholder_card(
                title="Visor (sticky) vacío",
                body=(
                    "El visor se mantiene separado de la navegación. "
                    "Cuando selecciones una entry, seguirá visible aunque cambies de año o week."
                ),
                min_height=108,
            ),
            _build_placeholder_card(
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
    week: MockWeek,
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
        )
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

    notes_controls: list[ft.Control] = [
        ft.Row(spacing=8, wrap=True, controls=action_buttons)
    ]
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
                    _truncate(week_write_error_message, 220),
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
                    _truncate(entry_write_error_message, 220),
                    size=12,
                    color=COLOR_ERROR_TEXT,
                ),
            )
        )
    notes_controls.append(
        _build_placeholder_card(
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
                    _build_badge(week.status_label, badge_bg, badge_fg),
                ],
            ),
            ft.Container(
                padding=ft.Padding.all(12),
                bgcolor="#F6F6F6",
                border_radius=8,
                border=ft.Border.all(1, "#D6D6D6"),
                content=ft.Column(spacing=8, controls=notes_controls),
            ),
            _build_placeholder_card(
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
    viewer_entry: MockEntry,
    viewer_sessions: list[ViewerSessionItem],
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
    active_entry_ref: EntryRef | None,
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
    viewer_matches_selected_week = _entry_ref_matches_selected_week(state, viewer_entry.ref)
    active_here = active_entry_ref is not None and active_entry_ref == viewer_entry.ref

    context_lines = [
        (
            f"Viendo: {viewer_entry.label} · Week {viewer_entry.ref.week_number} · "
            f"Año {viewer_entry.ref.year_number}"
        ),
        _format_navigation_line(state),
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

    entry_detail_card = _build_placeholder_card(
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
                    _build_badge(viewer_entry.entry_type, "#E7E0FF", "#4F46A5"),
                    _build_badge(
                        "activo aquí" if active_here else "visor",
                        "#DFF4FF" if active_here else "#F0F0F0",
                        "#0E5E78" if active_here else "#666666",
                    ),
                ],
            ),
            _build_placeholder_card(
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
                    _truncate(entry_write_error_message, 220),
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
    viewer_entry: MockEntry,
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
    body_controls.extend(
        [
        *rows,
        ]
    )
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
                    _truncate(resource_write_error_message, 220),
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
    viewer_sessions: list[ViewerSessionItem],
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
    total_duration = _sum_finished_sessions_duration(viewer_sessions)
    total_text = _format_duration(total_duration) if total_duration is not None else "0 min"
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
                    disabled=session_write_pending,
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
                    _truncate(session_write_error_message, 220),
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
                    "Error local Q8: " + _truncate(viewer_sessions_error_message, 220),
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
                                    ft.Text(
                                        "Activa" if session.ended_at_utc is None else "Histórica",
                                        size=11,
                                        color=COLOR_TEXT_MUTED,
                                    ),
                                ],
                            ),
                            ft.Row(
                                spacing=4,
                                controls=[
                                    ft.TextButton(
                                        "Editar",
                                        on_click=lambda _e, sid=session.session_id: on_open_manual_edit_session(sid),
                                        disabled=session_write_pending,
                                    ),
                                    ft.TextButton(
                                        "Borrar",
                                        on_click=lambda _e, sid=session.session_id: on_open_manual_delete_session(sid),
                                        disabled=session_write_pending,
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )
        body_controls.extend(rows)
        if len(viewer_sessions) > 8:
            body_controls.append(
                ft.Text(
                    f"… y {len(viewer_sessions) - 8} sesión(es) más",
                    size=11,
                    color=COLOR_TEXT_MUTED,
                )
            )
    if has_active_session:
        body_controls.append(
            ft.Text(
                "Hay una sesión activa en la lista (ended_at_utc = null).",
                size=11,
                color=COLOR_TEXT_MUTED,
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
                    "Bloque de sesión (Q8 + acciones #62)",
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


def _format_session_line(session: ViewerSessionItem) -> str:
    started = _format_dt_short(session.started_at_utc)
    ended = _format_dt_short(session.ended_at_utc)
    if session.ended_at_utc is None:
        return f"{session.session_id}: {started} → activa"
    duration = _session_duration(session)
    duration_text = _format_duration(duration) if duration is not None else "duración n/d"
    return f"{session.session_id}: {started} → {ended} · {duration_text}"


def _build_bottom_status_bar(
    *,
    env_name: str,
    viewer_entry: MockEntry | None,
    active_entry_ref: EntryRef | None,
    active_entry_label: str | None,
    active_status_error_message: str | None,
    campaign_resource_totals: dict[str, int] | None,
    on_manual_refresh: Callable[[], None],
) -> ft.Control:
    return ft.Container(
        height=BOTTOM_BAR_HEIGHT,
        bgcolor=COLOR_BOTTOM_BAR_BG,
        padding=ft.Padding(left=16, top=12, right=16, bottom=12),
        content=_build_bottom_status_bar_content(
            env_name=env_name,
            viewer_entry=viewer_entry,
            active_entry_ref=active_entry_ref,
            active_entry_label=active_entry_label,
            active_status_error_message=active_status_error_message,
            campaign_resource_totals=campaign_resource_totals,
            on_manual_refresh=on_manual_refresh,
        ),
    )


def _build_bottom_status_bar_content(
    *,
    env_name: str,
    viewer_entry: MockEntry | None,
    active_entry_ref: EntryRef | None,
    active_entry_label: str | None,
    active_status_error_message: str | None,
    campaign_resource_totals: dict[str, int] | None,
    on_manual_refresh: Callable[[], None],
) -> ft.Control:
    active_text, active_detail_text = _active_status_texts(
        active_entry_ref=active_entry_ref,
        active_entry_label=active_entry_label,
        active_status_error_message=active_status_error_message,
        viewer_entry=viewer_entry,
    )
    viewer_text = (
        f"Viendo: {_entry_short_label(viewer_entry)}"
        if viewer_entry is not None
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
                    ft.Text(
                        "Totales (read-only)",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_WHITE,
                    ),
                    ft.Text(
                        _format_resource_totals(campaign_resource_totals),
                        size=12,
                        color="#EAF9FF",
                    ),
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
                            ft.Text(
                                active_text,
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_WHITE,
                                text_align=ft.TextAlign.RIGHT,
                            ),
                            ft.Text(
                                active_detail_text or viewer_text,
                                size=12,
                                color="#EAF9FF",
                                text_align=ft.TextAlign.RIGHT,
                            ),
                            ft.Text(
                                f"{viewer_text} · env={env_name}",
                                size=11,
                                color="#DDF5FF",
                                text_align=ft.TextAlign.RIGHT,
                            ),
                        ],
                    ),
                    _build_refresh_button(on_manual_refresh),
                ],
            ),
        ],
    )


def _build_refresh_button(on_click: Callable[[], None]) -> ft.Control:
    return ft.Container(
        padding=ft.Padding(left=10, top=8, right=10, bottom=8),
        bgcolor="#21A4D3",
        border_radius=8,
        border=ft.Border.all(1, "#BFEFFF"),
        on_click=lambda _e: on_click(),
        content=ft.Text(
            "Refresh",
            size=12,
            weight=ft.FontWeight.BOLD,
            color=COLOR_WHITE,
        ),
    )


def _active_status_texts(
    *,
    active_entry_ref: EntryRef | None,
    active_entry_label: str | None,
    active_status_error_message: str | None,
    viewer_entry: MockEntry | None,
) -> tuple[str, str]:
    if active_status_error_message:
        return (
            "Estado activo no disponible",
            _truncate(active_status_error_message, 80),
        )

    if active_entry_ref is None:
        return ("Sin sesión activa", "")

    label = active_entry_label or f"Entry {active_entry_ref.entry_id}"
    if viewer_entry is not None and viewer_entry.ref == active_entry_ref:
        return (f"Con sesión activa: {label} · aquí", "")
    return (f"Con sesión activa: {label} · en otra entry", "")


def _format_resource_totals(resource_totals: dict[str, int] | None) -> str:
    if resource_totals is None:
        return "Totales no disponibles (Q1 no cargado)"
    if not resource_totals:
        return "Sin recursos materializados"

    items = sorted(resource_totals.items(), key=lambda item: item[0])
    visible = [f"{key}={value}" for key, value in items[:4]]
    suffix = " …" if len(items) > 4 else ""
    return " · ".join(visible) + suffix


def _build_badge(label: str, background: str, foreground: str) -> ft.Control:
    return ft.Container(
        padding=ft.Padding(left=8, top=4, right=8, bottom=4),
        bgcolor=background,
        border_radius=999,
        content=ft.Text(
            label,
            size=12,
            color=foreground,
            weight=ft.FontWeight.W_500,
        ),
    )


def _build_status_banner(
    *,
    title: str,
    body: str,
    background: str,
    border_color: str,
    foreground: str,
) -> ft.Control:
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


def _build_placeholder_card(title: str, body: str, min_height: int) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border_radius=8,
        border=ft.Border.all(1, "#D6D6D6"),
        content=ft.Column(
            spacing=6,
            controls=[
                ft.Text(
                    title,
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_TEXT_PRIMARY,
                ),
                ft.Container(
                    height=min_height,
                    padding=ft.Padding.all(8),
                    bgcolor="#FFFFFF",
                    border_radius=6,
                    content=ft.Text(body, size=13, color=COLOR_TEXT_MUTED),
                ),
            ],
        ),
    )


def _find_selected_week(
    state: MainScreenLocalState,
    weeks_for_selected_year: list[MockWeek],
) -> MockWeek | None:
    if state.selected_week is None:
        return None
    for week in weeks_for_selected_year:
        if week.week_number == state.selected_week:
            return week
    return None


def _viewer_matches_selected_week(
    state: MainScreenLocalState,
    viewer_entry: MockEntry | None,
) -> bool:
    if viewer_entry is None:
        return False
    return _entry_ref_matches_selected_week(state, viewer_entry.ref)


def _entry_ref_matches_selected_week(
    state: MainScreenLocalState,
    entry_ref: EntryRef,
) -> bool:
    return (
        state.selected_year is not None
        and state.selected_week is not None
        and entry_ref.year_number == state.selected_year
        and entry_ref.week_number == state.selected_week
    )


def _entry_short_label(entry: MockEntry) -> str:
    return f"{entry.label} (W{entry.ref.week_number})"


def _format_navigation_line(state: MainScreenLocalState) -> str:
    if state.selected_year is None:
        return "Navegación actual: sin año visible"
    if state.selected_week is None:
        return f"Navegación actual: Año {state.selected_year} · sin week seleccionada"
    return f"Navegación actual: Año {state.selected_year} · Week {state.selected_week}"


def _sum_finished_sessions_duration(sessions: list[ViewerSessionItem]) -> timedelta | None:
    total = timedelta(0)
    has_any = False
    for session in sessions:
        duration = _session_duration(session)
        if duration is None:
            continue
        has_any = True
        total += duration
    return total if has_any else timedelta(0)


def _session_duration(session: ViewerSessionItem) -> timedelta | None:
    started = _as_datetime(session.started_at_utc)
    ended = _as_datetime(session.ended_at_utc)
    if started is None or ended is None:
        return None
    if ended < started:
        return None
    return ended - started


def _as_datetime(value: object | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    return None


def _format_dt_short(value: object | None) -> str:
    dt_value = _as_datetime(value)
    if dt_value is None:
        return "n/d"
    return dt_value.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%MZ")


def _format_duration(duration: timedelta) -> str:
    total_seconds = int(duration.total_seconds())
    hours, rem = divmod(total_seconds, 3600)
    minutes, _seconds = divmod(rem, 60)
    if hours > 0:
        return f"{hours} h {minutes} min"
    return f"{minutes} min"


def _truncate(value: str, max_length: int) -> str:
    if len(value) <= max_length:
        return value
    return value[: max_length - 1] + "…"
