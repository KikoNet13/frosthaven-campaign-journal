from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState


def build_entry_tabs_bar(_data: MainShellViewData, _state: MainShellState) -> ft.Control:
    """Legacy placeholder kept for compatibility after moving entries selection to the center viewer."""
    return ft.Container(visible=False, height=0)
