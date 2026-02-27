from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.app_root_controller import AppRootController


def build_app_root(page: ft.Page) -> ft.Control:
    return AppRootController(page).build()

