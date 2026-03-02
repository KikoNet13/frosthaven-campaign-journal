from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.models import EntrySummary, entry_ref_matches_selected_week
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.view.theme import (
    COLOR_ENTRY_TAB_SELECTED_UNDERLINE,
    COLOR_ENTRY_TABS_BG,
    COLOR_ERROR_TEXT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
)


def build_entry_tabs_bar(data: MainShellViewData, state: MainShellState) -> ft.Control:
    content: ft.Control
    if data.state.selected_week is None:
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ft.Text("Selecciona una semana para ver entradas", size=13, color=COLOR_TEXT_MUTED, italic=True)],
        )
    elif data.entries_panel_error_message:
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ft.Text(f"Error Q5: {data.entries_panel_error_message}", size=12, color=COLOR_ERROR_TEXT)],
        )
    elif not data.entries_for_selected_week:
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ft.Text(f"Semana {data.state.selected_week} sin entradas", size=13, color=COLOR_TEXT_MUTED, italic=True)],
        )
    else:
        selected_ref = (
            data.viewer_entry.ref
            if data.viewer_entry is not None and entry_ref_matches_selected_week(data.state, data.viewer_entry.ref)
            else None
        )
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=8,
            controls=[
                _build_entry_tab(
                    entry=entry,
                    is_selected=selected_ref == entry.ref,
                    on_select_entry_click=state.on_select_entry_click,
                )
                for entry in data.entries_for_selected_week
            ],
        )

    return ft.Container(
        height=44,
        bgcolor=COLOR_ENTRY_TABS_BG,
        padding=ft.Padding(left=16, top=4, right=16, bottom=4),
        content=content,
    )


def _build_entry_tab(
    *,
    entry: EntrySummary,
    is_selected: bool,
    on_select_entry_click: ft.OptionalEventCallable["ControlEvent"],
) -> ft.Control:
    underline_color = COLOR_ENTRY_TAB_SELECTED_UNDERLINE if is_selected else "transparent"
    text_weight = ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL
    underline_width = max(36, min(180, len(entry.label) * 7))
    return ft.Container(
        data=entry.ref,
        on_click=on_select_entry_click,
        padding=ft.Padding(left=12, top=6, right=12, bottom=2),
        content=ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(entry.label, size=13, color=COLOR_TEXT_PRIMARY, weight=text_weight),
                ft.Container(width=underline_width, height=2, bgcolor=underline_color, border_radius=1),
            ],
        ),
    )
