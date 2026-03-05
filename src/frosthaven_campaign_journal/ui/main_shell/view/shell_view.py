from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.models import WeekSummary
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState
from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_BOTTOM_BAR_BG,
    COLOR_CENTER_BG,
    COLOR_TOP_NAV_BUTTON_BG,
    COLOR_TOP_BAR_BG,
    COLOR_WHITE,
)
from frosthaven_campaign_journal.ui.common.theme.layout import (
    BOTTOM_BAR_HEIGHT,
    TOP_BAR_HEIGHT,
)
from frosthaven_campaign_journal.ui.main_shell.view.center_panel import build_center_panel
from frosthaven_campaign_journal.ui.main_shell.view.status_bar import build_status_bar
from frosthaven_campaign_journal.ui.main_shell.view.temporal_bar import build_top_temporal_bar


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
            force_material_transparency=False,
            bgcolor=COLOR_TOP_BAR_BG,
            title=build_top_temporal_bar(data, state),
        ),
        bottom_appbar=ft.BottomAppBar(
            height=BOTTOM_BAR_HEIGHT,
            padding=ft.Padding(left=12, top=8, right=12, bottom=8),
            elevation=0,
            bgcolor=COLOR_BOTTOM_BAR_BG,
            content=build_status_bar(data),
        ),
        floating_action_button=_build_week_actions_fab(data, state),
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
        content=ft.Container(
            expand=True,
            bgcolor=COLOR_CENTER_BG,
            content=build_center_panel(data, state),
        ),
    )


def _find_selected_week(data: MainShellViewData) -> WeekSummary | None:
    if data.state.selected_week is None:
        return None
    for week in data.weeks_for_selected_year:
        if week.week_number == data.state.selected_week:
            return week
    return None


def _build_week_actions_fab(data: MainShellViewData, state: MainShellState) -> ft.Control | None:
    selected_week = _find_selected_week(data)
    if selected_week is None:
        return None

    write_pending = data.week_write_pending or data.entry_write_pending or data.campaign_write_pending
    menu_items: list[ft.PopupMenuItem] = [
        ft.PopupMenuItem(
            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
            content="Crear entrada",
            on_click=state.on_open_entry_add_modal,
            disabled=data.entry_write_pending or data.campaign_write_pending,
        ),
    ]

    if selected_week.is_closed:
        menu_items.append(
            ft.PopupMenuItem(
                icon=ft.Icons.LOCK_OPEN,
                content="Reabrir semana",
                on_click=state.on_request_week_reopen,
                disabled=write_pending,
            )
        )
    else:
        menu_items.extend(
            [
                ft.PopupMenuItem(
                    icon=ft.Icons.LOCK,
                    content="Cerrar semana",
                    on_click=state.on_request_week_close,
                    disabled=write_pending,
                ),
                ft.PopupMenuItem(
                    icon=ft.Icons.LOCK_RESET,
                    content="Recerrar semana",
                    on_click=state.on_request_week_reclose,
                    disabled=write_pending,
                ),
            ]
        )

    menu_items.append(
        ft.PopupMenuItem(
            icon=ft.Icons.REFRESH,
            content="Refrescar",
            on_click=state.on_manual_refresh,
            disabled=data.campaign_write_pending,
        )
    )

    return ft.PopupMenuButton(
        icon=ft.Icons.ADD,
        icon_size=26,
        icon_color=COLOR_WHITE,
        tooltip="Acciones de semana",
        bgcolor=COLOR_TOP_NAV_BUTTON_BG,
        shape=ft.CircleBorder(),
        padding=14,
        items=menu_items,
    )
