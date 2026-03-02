from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.view.center_focus import (
    _build_focus_empty_mode,
    _build_focus_entry_mode,
    _build_focus_week_mode,
)
from frosthaven_campaign_journal.ui.main_shell.view.center_forms import (
    _build_banner,
    _build_confirmation_card,
    _build_entry_form_editor,
    _build_session_form_editor,
    _build_week_notes_editor,
)
from frosthaven_campaign_journal.ui.main_shell.view.center_helpers import _find_selected_week
from frosthaven_campaign_journal.ui.main_shell.view.theme import COLOR_CENTER_BG


def build_center_panel(data: MainShellViewData, state: MainShellState) -> ft.Control:
    controls: list[ft.Control] = []

    if data.read_error_message:
        controls.append(_build_banner("Error de lectura", data.read_error_message, "#FFE7E7", "#D87A7A", "#8A1F1F"))
    if data.read_warning_message:
        controls.append(
            _build_banner("Advertencia", data.read_warning_message, "#FFF4D8", "#D0A55E", "#7D5700")
        )
    if data.info_message:
        controls.append(_build_banner("Información", data.info_message, "#E8F4FF", "#90C4E8", "#0E5E78"))
    if data.confirmation is not None:
        controls.append(_build_confirmation_card(data, state))
    if data.week_notes_editor is not None:
        controls.append(_build_week_notes_editor(data, state))
    if data.entry_form is not None:
        controls.append(_build_entry_form_editor(data, state))
    if data.session_form is not None:
        controls.append(_build_session_form_editor(data, state))

    selected_week = _find_selected_week(data)
    if data.viewer_entry is not None:
        controls.append(_build_focus_entry_mode(data, state))
    elif selected_week is not None:
        controls.append(_build_focus_week_mode(data, state, selected_week))
    else:
        controls.append(_build_focus_empty_mode(data))

    return ft.Container(
        expand=True,
        bgcolor=COLOR_CENTER_BG,
        padding=ft.Padding.all(16),
        content=ft.ListView(
            expand=True,
            spacing=12,
            padding=0,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            scroll=ft.ScrollMode.AUTO,
            controls=controls,
        ),
    )
