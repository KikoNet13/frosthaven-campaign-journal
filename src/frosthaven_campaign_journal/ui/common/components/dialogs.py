from __future__ import annotations

from collections.abc import Sequence

import flet as ft

from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_ACCENT_BG,
    COLOR_PANEL_BG,
    COLOR_PANEL_BORDER,
    COLOR_TEXT_HEADING,
    COLOR_WHITE,
)

_MODAL_WIDTH = 560
_MODAL_BACKDROP = ft.Colors.with_opacity(0.42, ft.Colors.BLACK)


def build_dialog_button_style(*, filled: bool) -> ft.ButtonStyle:
    return ft.ButtonStyle(
        bgcolor=COLOR_ACCENT_BG if filled else None,
        color=COLOR_WHITE if filled else COLOR_ACCENT_BG,
        side=None if filled else ft.BorderSide(1.25, COLOR_ACCENT_BG),
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.Padding(left=16, top=12, right=16, bottom=12),
    )


def build_modal_dialog_shell(
    *,
    body: ft.Control,
    actions: Sequence[ft.Control],
    title: str | None = None,
    width: int = _MODAL_WIDTH,
    height: int | None = None,
    body_expand: bool = False,
) -> ft.Control:
    controls: list[ft.Control] = []
    if title:
        controls.append(
            ft.Text(
                title,
                size=18,
                weight=ft.FontWeight.W_600,
                color=COLOR_TEXT_HEADING,
            )
        )
    controls.append(ft.Container(expand=body_expand, content=body))
    if actions:
        controls.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                spacing=8,
                controls=list(actions),
            )
        )

    return ft.Container(
        expand=True,
        bgcolor=_MODAL_BACKDROP,
        alignment=ft.Alignment.CENTER,
        padding=ft.Padding.all(24),
        content=ft.Container(
            width=width,
            height=height,
            padding=ft.Padding.all(16),
            bgcolor=COLOR_PANEL_BG,
            border_radius=12,
            border=ft.Border.all(1, COLOR_PANEL_BORDER),
            content=ft.Column(
                expand=body_expand,
                spacing=12,
                controls=controls,
            ),
        ),
    )
