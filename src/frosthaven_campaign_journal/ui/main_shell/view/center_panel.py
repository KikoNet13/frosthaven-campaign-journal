from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.common.components.surfaces import BannerTone, build_banner
from frosthaven_campaign_journal.ui.common.theme.colors import COLOR_CENTER_BG
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.view.center_focus import (
    _build_focus_empty_mode,
    _build_focus_week_mode,
)
from frosthaven_campaign_journal.ui.main_shell.view.center_forms import (
    _build_entry_form_editor,
    _build_entry_notes_editor,
    _build_session_form_editor,
)
from frosthaven_campaign_journal.ui.main_shell.view.center_helpers import _find_selected_week


def build_center_panel(data: MainShellViewData, state: MainShellState) -> ft.Control:
    top_controls: list[ft.Control] = []

    if data.read_error_message:
        top_controls.append(build_banner(title="Error de lectura", body=data.read_error_message, tone=BannerTone.ERROR))
    if data.read_warning_message:
        top_controls.append(build_banner(title="Advertencia", body=data.read_warning_message, tone=BannerTone.WARNING))
    if data.week_write_error_message:
        top_controls.append(build_banner(title="Error de semana", body=data.week_write_error_message, tone=BannerTone.ERROR))
    if data.entry_write_error_message:
        top_controls.append(build_banner(title="Error de entrada", body=data.entry_write_error_message, tone=BannerTone.ERROR))

    if data.entry_form is not None:
        top_controls.append(_build_entry_form_editor(data, state))
    if data.entry_notes_editor is not None:
        top_controls.append(_build_entry_notes_editor(data, state))
    if data.session_form is not None:
        top_controls.append(_build_session_form_editor(data, state))

    selected_week = _find_selected_week(data)
    focus_control = (
        _build_focus_week_mode(data, state, selected_week)
        if selected_week is not None
        else _build_focus_empty_mode(data)
    )

    return ft.Container(
        expand=True,
        bgcolor=COLOR_CENTER_BG,
        padding=ft.Padding.all(16),
        content=ft.Column(
            expand=True,
            spacing=12,
            controls=[
                *top_controls,
                ft.Container(
                    expand=True,
                    content=focus_control,
                ),
            ],
        ),
    )