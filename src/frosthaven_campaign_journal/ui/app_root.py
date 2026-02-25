from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.config import load_settings
from frosthaven_campaign_journal.ui.views import (
    DEFAULT_SHELL_PREVIEW_STATE,
    build_main_shell_view,
)


def build_app_root() -> ft.Control:
    settings = load_settings()
    return ft.SafeArea(
        content=build_main_shell_view(
            preview_state=DEFAULT_SHELL_PREVIEW_STATE,
            env_name=settings.env,
        ),
        expand=True,
    )
