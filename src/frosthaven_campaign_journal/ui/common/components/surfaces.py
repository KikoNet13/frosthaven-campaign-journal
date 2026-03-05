from __future__ import annotations

from enum import Enum
from typing import Sequence

import flet as ft

from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_BANNER_ERROR_BG,
    COLOR_BANNER_ERROR_BORDER,
    COLOR_BANNER_ERROR_TEXT,
    COLOR_BANNER_INFO_BG,
    COLOR_BANNER_INFO_BORDER,
    COLOR_BANNER_INFO_TEXT,
    COLOR_BANNER_WARNING_BG,
    COLOR_BANNER_WARNING_BORDER,
    COLOR_BANNER_WARNING_TEXT,
    COLOR_PANEL_BG,
    COLOR_PANEL_BORDER,
    COLOR_PANEL_INNER_BG,
    COLOR_PANEL_INNER_BORDER,
)


class BannerTone(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


def build_panel(
    *,
    controls: Sequence[ft.Control],
    spacing: int = 8,
    padding: int = 12,
) -> ft.Container:
    return ft.Container(
        padding=ft.Padding.all(padding),
        bgcolor=COLOR_PANEL_BG,
        border_radius=8,
        border=ft.Border.all(1, COLOR_PANEL_BORDER),
        content=ft.Column(
            spacing=spacing,
            controls=list(controls),
        ),
    )


def build_inner_surface(*, content: ft.Control, padding: int = 8) -> ft.Container:
    return ft.Container(
        padding=ft.Padding.all(padding),
        bgcolor=COLOR_PANEL_INNER_BG,
        border_radius=6,
        border=ft.Border.all(1, COLOR_PANEL_INNER_BORDER),
        content=content,
    )


def build_banner(*, title: str, body: str, tone: BannerTone) -> ft.Control:
    if tone == BannerTone.ERROR:
        background = COLOR_BANNER_ERROR_BG
        border = COLOR_BANNER_ERROR_BORDER
        foreground = COLOR_BANNER_ERROR_TEXT
    elif tone == BannerTone.WARNING:
        background = COLOR_BANNER_WARNING_BG
        border = COLOR_BANNER_WARNING_BORDER
        foreground = COLOR_BANNER_WARNING_TEXT
    else:
        background = COLOR_BANNER_INFO_BG
        border = COLOR_BANNER_INFO_BORDER
        foreground = COLOR_BANNER_INFO_TEXT

    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor=background,
        border=ft.Border.all(1, border),
        border_radius=8,
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=foreground),
                ft.Text(body, size=12, color=foreground),
            ],
        ),
    )
