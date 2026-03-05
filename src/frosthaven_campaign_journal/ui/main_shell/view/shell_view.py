from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.models import WeekSummary
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState
from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_BOTTOM_BAR_BG,
    COLOR_CENTER_BG,
    COLOR_TEXT_PRIMARY,
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

_FAB_MENU_TEXT_STYLE = ft.TextStyle(color=COLOR_TEXT_PRIMARY, size=15)
_FAB_MENU_ITEM_MIN_WIDTH = 228
_FAB_TRIGGER_SIZE = 56


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
        floating_action_button_location=ft.FloatingActionButtonLocation.END_DOCKED,
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


def _build_fab_menu_item(
    *,
    icon: ft.IconData,
    label: str,
    on_click,
    disabled: bool,
) -> ft.PopupMenuItem:
    return ft.PopupMenuItem(
        content=ft.Container(
            width=_FAB_MENU_ITEM_MIN_WIDTH,
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(icon, size=18, color=COLOR_TEXT_PRIMARY),
                    ft.Text(label, style=_FAB_MENU_TEXT_STYLE),
                ],
            ),
        ),
        label_text_style=_FAB_MENU_TEXT_STYLE,
        on_click=on_click,
        disabled=disabled,
    )


def _build_week_actions_fab(data: MainShellViewData, state: MainShellState) -> ft.Control | None:
    selected_week = _find_selected_week(data)
    if selected_week is None:
        return None

    write_pending = data.week_write_pending or data.entry_write_pending or data.campaign_write_pending
    menu_items: list[ft.PopupMenuItem] = [
        _build_fab_menu_item(
            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
            label="Crear entrada",
            on_click=state.on_open_entry_add_modal,
            disabled=data.entry_write_pending or data.campaign_write_pending,
        ),
    ]

    if selected_week.is_closed:
        menu_items.append(
            _build_fab_menu_item(
                icon=ft.Icons.LOCK_OPEN,
                label="Reabrir semana",
                on_click=state.on_request_week_reopen,
                disabled=write_pending,
            )
        )
    else:
        menu_items.extend(
            [
                _build_fab_menu_item(
                    icon=ft.Icons.LOCK,
                    label="Cerrar semana",
                    on_click=state.on_request_week_close,
                    disabled=write_pending,
                ),
                _build_fab_menu_item(
                    icon=ft.Icons.LOCK_RESET,
                    label="Recerrar semana",
                    on_click=state.on_request_week_reclose,
                    disabled=write_pending,
                ),
            ]
        )

    menu_items.append(
        _build_fab_menu_item(
            icon=ft.Icons.REFRESH,
            label="Refrescar",
            on_click=state.on_manual_refresh,
            disabled=data.campaign_write_pending,
        )
    )

    return ft.PopupMenuButton(
        content=ft.Container(
            width=_FAB_TRIGGER_SIZE,
            height=_FAB_TRIGGER_SIZE,
            alignment=ft.Alignment.CENTER,
            bgcolor=COLOR_TOP_NAV_BUTTON_BG,
            border=ft.Border.all(1.5, COLOR_WHITE),
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.32, ft.Colors.BLACK),
                offset=ft.Offset(0, 3),
            ),
            content=ft.Icon(ft.Icons.ADD, size=30, color=COLOR_WHITE),
        ),
        tooltip="Acciones de semana",
        shape=ft.RoundedRectangleBorder(radius=16),
        padding=0,
        size_constraints=ft.BoxConstraints(
            min_width=_FAB_TRIGGER_SIZE,
            min_height=_FAB_TRIGGER_SIZE,
        ),
        items=menu_items,
    )
