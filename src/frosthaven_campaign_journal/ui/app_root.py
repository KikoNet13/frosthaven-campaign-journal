from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.features.main_shell.state import MainShellState
from frosthaven_campaign_journal.ui.features.main_shell.view import build_main_shell_view


def build_app_root(page: ft.Page) -> ft.Control:
    shell_state = MainShellState(page=page)
    shell_host = ft.Container(expand=True)
    safe_root = ft.SafeArea(expand=True, content=shell_host)
    root = ft.Container(expand=True, content=safe_root)

    def sync_root_height_to_viewport() -> None:
        viewport_height = getattr(page, "height", None)
        if not isinstance(viewport_height, (int, float)) or viewport_height <= 0:
            viewport_height = 900
        root.height = viewport_height

    def refresh() -> None:
        sync_root_height_to_viewport()
        shell_host.content = build_main_shell_view(
            data=shell_state.build_view_data(),
            actions=shell_state.build_actions(refresh),
        )
        page.update()

    page.on_media_change = lambda _e: refresh()
    shell_state.initialize()
    sync_root_height_to_viewport()
    shell_host.content = build_main_shell_view(
        data=shell_state.build_view_data(),
        actions=shell_state.build_actions(refresh),
    )
    return root
