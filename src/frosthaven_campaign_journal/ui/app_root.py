from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.features.main_shell.state import MainShellState
from frosthaven_campaign_journal.ui.features.main_shell.view import build_main_shell_view


@ft.component
def build_app_root(page: ft.Page) -> ft.Control:
    shell_state, _ = ft.use_state(MainShellState.create)

    return ft.Container(
        expand=True,
        content=ft.SafeArea(
            expand=True,
            content=build_main_shell_view(shell_state),
        ),
    )
