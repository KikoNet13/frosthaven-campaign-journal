from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.config import load_settings
from frosthaven_campaign_journal.ui.views.bootstrap_view import build_bootstrap_view


def build_app_root() -> ft.Control:
    settings = load_settings()
    return ft.SafeArea(
        content=build_bootstrap_view(env_name=settings.env),
        expand=True,
    )
