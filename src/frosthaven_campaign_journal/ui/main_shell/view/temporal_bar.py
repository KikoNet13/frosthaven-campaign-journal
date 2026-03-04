from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.models import WeekSummary
from frosthaven_campaign_journal.ui.common.components import LabeledGroupBox
from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_ERROR_TEXT,
    COLOR_SEASON_LABEL_BG,
    COLOR_SEASON_LABEL_BORDER,
    COLOR_SEASON_LABEL_TEXT,
    COLOR_TOP_BAR_TEXT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_TOP_NAV_BUTTON_BG,
    COLOR_TOP_NAV_BUTTON_DISABLED_BG,
    COLOR_TOP_NAV_BUTTON_TEXT_DISABLED,
    COLOR_WEEK_BLOCK_BORDER,
    COLOR_WEEK_BLOCK_SUMMER_BG,
    COLOR_WEEK_BLOCK_WINTER_BG,
    COLOR_WEEK_TILE_BG,
    COLOR_WEEK_TILE_CLOSED_BG,
    COLOR_WEEK_TILE_CLOSED_TEXT,
    COLOR_WEEK_TILE_SELECTED_BG,
    COLOR_WEEK_TILE_SELECTED_BORDER,
    COLOR_WHITE,
)
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState


def build_top_temporal_bar(data: MainShellViewData, state: MainShellState) -> ft.Control:
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

    left_year_action = state.on_prev_year if has_prev_year and not data.campaign_write_pending else None
    if not has_valid_selected_year:
        right_year_label = ">"
        right_year_action = None
    elif is_last_year:
        right_year_label = "+ Año"
        right_year_action = (
            state.on_open_extend_year_plus_one_confirm if not data.campaign_write_pending else None
        )
    else:
        right_year_label = ">"
        right_year_action = state.on_next_year if has_next_year and not data.campaign_write_pending else None

    week_strip_content: ft.Control
    if data.read_status == "error" and not data.weeks_for_selected_year:
        week_strip_content = ft.Text(
            "Semanas no disponibles (error de lectura)",
            size=13,
            color=COLOR_ERROR_TEXT,
            italic=True,
        )
    elif not data.weeks_for_selected_year:
        week_strip_content = ft.Text(
            "Sin semanas para el año visible",
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
                    season_label="Verano",
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
                    season_label="Invierno",
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
                color=COLOR_TOP_BAR_TEXT,
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
                    clip_behavior=ft.ClipBehavior.NONE,
                    content=week_strip_content,
                ),
            ],
        ),
    )


def _split_weeks_into_season_blocks(
    weeks_for_selected_year: list[WeekSummary],
) -> tuple[list[WeekSummary], list[WeekSummary]]:
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
    season_label: str,
) -> ft.Control:
    return LabeledGroupBox(
        label=season_label,
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
        bgcolor=block_bgcolor,
        border_color=COLOR_WEEK_BLOCK_BORDER,
        label_bgcolor=COLOR_SEASON_LABEL_BG,
        label_border_color=COLOR_SEASON_LABEL_BORDER,
        label_text_color=COLOR_SEASON_LABEL_TEXT,
        padding=ft.Padding(left=4, top=8, right=4, bottom=4),
    )


def _build_year_nav_button(
    label: str,
    on_click: ft.OptionalEventCallable["ControlEvent"],
) -> ft.Control:
    enabled = on_click is not None
    is_extended_label = label == "+ Año"
    return ft.Container(
        width=88 if is_extended_label else 52,
        height=40 if is_extended_label else 52,
        border_radius=999,
        bgcolor=COLOR_TOP_NAV_BUTTON_BG if enabled else COLOR_TOP_NAV_BUTTON_DISABLED_BG,
        alignment=ft.Alignment.CENTER,
        on_click=on_click,
        content=ft.Text(
            label,
            size=16 if is_extended_label else 24,
            weight=ft.FontWeight.BOLD,
            color=COLOR_WHITE if enabled else COLOR_TOP_NAV_BUTTON_TEXT_DISABLED,
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
    if is_selected:
        bgcolor = COLOR_WEEK_TILE_SELECTED_BG
    else:
        bgcolor = COLOR_WEEK_TILE_CLOSED_BG if week.is_closed else COLOR_WEEK_TILE_BG
    text_color = COLOR_WEEK_TILE_CLOSED_TEXT if week.is_closed else COLOR_TEXT_PRIMARY
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
