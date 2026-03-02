from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.main_shell.state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.view.center_panel import build_center_panel
from frosthaven_campaign_journal.ui.main_shell.view.entries_bar import build_entry_tabs_bar
from frosthaven_campaign_journal.ui.main_shell.view.status_bar import build_status_bar
from frosthaven_campaign_journal.ui.main_shell.view.temporal_bar import build_top_temporal_bar
from frosthaven_campaign_journal.ui.main_shell.view.theme import (
    BOTTOM_BAR_HEIGHT,
    COLOR_BOTTOM_BAR_BG,
    COLOR_CENTER_BG,
    COLOR_TOP_BAR_BG,
    TOP_BAR_HEIGHT,
)


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
            title=build_top_temporal_bar(data, state),
        ),
        bottom_appbar=ft.BottomAppBar(
            height=BOTTOM_BAR_HEIGHT,
            padding=ft.Padding(left=16, top=12, right=16, bottom=12),
            elevation=0,
            bgcolor=COLOR_BOTTOM_BAR_BG,
            content=build_status_bar(data, state),
        ),
        content=ft.Container(
            expand=True,
            bgcolor=COLOR_CENTER_BG,
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    build_entry_tabs_bar(data, state),
                    ft.Container(expand=True, content=build_center_panel(data, state)),
                ],
            ),
        ),
    )
