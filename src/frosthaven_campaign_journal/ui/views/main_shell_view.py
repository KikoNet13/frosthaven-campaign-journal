from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.views.main_shell_contracts import (
    MainShellViewActions,
    MainShellViewData,
)
from frosthaven_campaign_journal.ui.views.main_shell_focus import build_center_focus_panel
from frosthaven_campaign_journal.ui.views.main_shell_shared import (
    BOTTOM_BAR_HEIGHT,
    COLOR_BOTTOM_BAR_BG,
    COLOR_TOP_BAR_BG,
    OUTER_PADDING,
    TOP_BAR_HEIGHT,
)
from frosthaven_campaign_journal.ui.views.main_shell_status import build_bottom_status_bar_content
from frosthaven_campaign_journal.ui.views.main_shell_temporal import (
    build_entry_tabs_bar,
    build_top_temporal_bar,
)


def build_main_shell_view(*, data: MainShellViewData, actions: MainShellViewActions) -> ft.Control:
    top_bar = build_top_temporal_bar(
        data=data,
        actions=actions,
        embedded_in_appbar=True,
    )
    entry_tabs_bar = build_entry_tabs_bar(data=data, actions=actions)
    center_panel = build_center_focus_panel(data=data, actions=actions)
    bottom_bar_content = build_bottom_status_bar_content(data=data, actions=actions)

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

