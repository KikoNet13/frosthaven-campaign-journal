from __future__ import annotations

from typing import Callable

import flet as ft

from frosthaven_campaign_journal.state.placeholders import EntryRef, entry_ref_matches_selected_week
from frosthaven_campaign_journal.ui.views.main_shell_contracts import (
    MainShellViewActions,
    MainShellViewData,
)
from frosthaven_campaign_journal.ui.views.main_shell_shared import (
    COLOR_ENTRY_TAB_SELECTED_UNDERLINE,
    COLOR_ENTRY_TABS_BG,
    COLOR_ERROR_TEXT,
    COLOR_TEXT_DIMMED,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_TOP_BAR_BG,
    COLOR_TOP_NAV_BUTTON_BG,
    COLOR_TOP_NAV_BUTTON_DISABLED_BG,
    COLOR_WEEK_BLOCK_BORDER,
    COLOR_WEEK_BLOCK_SUMMER_BG,
    COLOR_WEEK_BLOCK_WINTER_BG,
    COLOR_WEEK_TILE_BG,
    COLOR_WEEK_TILE_CLOSED_BG,
    COLOR_WEEK_TILE_SELECTED_BORDER,
    COLOR_WHITE,
    truncate,
)


def build_top_temporal_bar(
    *,
    data: MainShellViewData,
    actions: MainShellViewActions,
    embedded_in_appbar: bool = False,
) -> ft.Control:
    selected_year = data.state.selected_year
    has_valid_selected_year = selected_year is not None and selected_year in data.years
    if has_valid_selected_year:
        year_index = data.years.index(selected_year)
        has_prev_year = year_index > 0
        has_next_year = year_index < len(data.years) - 1
        is_last_year = year_index == len(data.years) - 1
        year_title = f"Año {selected_year}"
    else:
        has_prev_year = False
        has_next_year = False
        is_last_year = False
        year_title = "Año -"

    left_year_action = actions.on_prev_year if has_prev_year and not data.campaign_write_pending else None
    if not has_valid_selected_year:
        right_year_label = "?"
        right_year_action = None
    elif is_last_year:
        right_year_label = "+"
        right_year_action = (
            actions.on_open_extend_year_plus_one_confirm if not data.campaign_write_pending else None
        )
    else:
        right_year_label = "?"
        right_year_action = actions.on_next_year if has_next_year and not data.campaign_write_pending else None

    is_mobile_landscape_topbar = _is_mobile_landscape_topbar(
        viewport_width=data.viewport_width,
        viewport_height=data.viewport_height,
    )
    year_group_spacing = 8 if is_mobile_landscape_topbar else 12
    content_row_spacing = 8 if is_mobile_landscape_topbar else 16
    year_title_size = 24 if is_mobile_landscape_topbar else 32
    year_nav_button_size = 38 if is_mobile_landscape_topbar else 42
    year_nav_font_size = 18 if is_mobile_landscape_topbar else 20
    week_block_spacing = 6 if is_mobile_landscape_topbar else 8
    week_tile_gap = 4 if is_mobile_landscape_topbar else 6

    if data.read_status == "error" and not data.weeks_for_selected_year:
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
    elif not data.weeks_for_selected_year:
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
        summer_weeks, winter_weeks = _split_weeks_into_season_blocks(data.weeks_for_selected_year)
        season_blocks: list[ft.Control] = []
        if summer_weeks:
            season_blocks.append(
                _build_week_season_block(
                    weeks=summer_weeks,
                    selected_week=data.state.selected_week,
                    on_select_week=actions.on_select_week,
                    disabled=data.campaign_write_pending,
                    block_bgcolor=COLOR_WEEK_BLOCK_SUMMER_BG,
                    tile_spacing=week_tile_gap,
                )
            )
        if winter_weeks:
            season_blocks.append(
                _build_week_season_block(
                    weeks=winter_weeks,
                    selected_week=data.state.selected_week,
                    on_select_week=actions.on_select_week,
                    disabled=data.campaign_write_pending,
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

    tooltip = data.read_error_message if data.read_status == "error" else None

    year_group = ft.Row(
        spacing=year_group_spacing,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            _build_year_nav_button(
                "?",
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
    weeks_for_selected_year: list[object],
) -> tuple[list[object], list[object]]:
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
    weeks: list[object],
    selected_week: int | None,
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
            controls=[
                _build_week_tile(
                    week=week,
                    is_selected=(week.week_number == selected_week),
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
    size: int,
    font_size: int,
) -> ft.Control:
    enabled = on_click is not None
    return ft.Container(
        width=size,
        height=size,
        border_radius=8,
        bgcolor=COLOR_TOP_NAV_BUTTON_BG if enabled else COLOR_TOP_NAV_BUTTON_DISABLED_BG,
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
    week: object,
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


def build_entry_tabs_bar(*, data: MainShellViewData, actions: MainShellViewActions) -> ft.Control:
    if data.state.selected_week is None:
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
    elif data.entries_panel_error_message:
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    truncate(f"Error Q5: {data.entries_panel_error_message}", 140),
                    size=12,
                    color=COLOR_ERROR_TEXT,
                )
            ],
        )
    elif not data.entries_for_selected_week:
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    f"Week {data.state.selected_week} sin entries",
                    size=13,
                    color=COLOR_TEXT_MUTED,
                    italic=True,
                )
            ],
        )
    else:
        tab_selected_ref = (
            data.viewer_entry.ref if _viewer_matches_selected_week(data.state, data.viewer_entry) else None
        )
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=8,
            controls=[
                _build_entry_tab(
                    entry=entry,
                    is_selected=(tab_selected_ref == entry.ref),
                    on_select_entry=actions.on_select_entry,
                )
                for entry in data.entries_for_selected_week
            ],
        )

    return ft.Container(
        height=44,
        bgcolor=COLOR_ENTRY_TABS_BG,
        padding=ft.Padding(left=16, top=4, right=16, bottom=4),
        content=content,
    )


def _build_entry_tab(
    *,
    entry: object,
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


def _viewer_matches_selected_week(state: object, viewer_entry: object | None) -> bool:
    if viewer_entry is None:
        return False
    return entry_ref_matches_selected_week(state, viewer_entry.ref)

