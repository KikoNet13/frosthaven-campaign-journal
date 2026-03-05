from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.common.theme.colors import COLOR_RESOURCE_TOTAL_VALUE, COLOR_WHITE


@ft.control
class ResourceTotalRow(ft.Row):
    icon_src: str = ""
    label_es: str = ""
    total_text: str = "0"
    text_color: str = COLOR_WHITE
    value_color: str = COLOR_RESOURCE_TOTAL_VALUE
    icon_color: str | None = None
    icon_width: int = 20
    label_size: int = 12
    value_size: int = 12
    label_width: int = 136
    value_width: int = 44

    def _build_controls(self) -> list[ft.Control]:
        return [
            ft.Container(
                width=self.icon_width,
                alignment=ft.Alignment.CENTER_LEFT,
                content=ft.Image(
                    src=self.icon_src,
                    width=18,
                    height=18,
                    color=self.icon_color,
                    color_blend_mode=ft.BlendMode.SRC_IN if self.icon_color else None,
                ),
            ),
            ft.Container(
                width=self.label_width,
                alignment=ft.Alignment.CENTER_LEFT,
                content=ft.Text(
                    self.label_es,
                    size=self.label_size,
                    color=self.text_color,
                    no_wrap=True,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
            ),
            ft.Container(
                width=self.value_width,
                alignment=ft.Alignment.CENTER_RIGHT,
                content=ft.Text(
                    self.total_text,
                    size=self.value_size,
                    color=self.value_color,
                    weight=ft.FontWeight.W_700,
                    text_align=ft.TextAlign.RIGHT,
                    no_wrap=True,
                ),
            ),
        ]

    def init(self) -> None:
        super().init()
        self.spacing = 4
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.controls = self._build_controls()

    def before_update(self) -> None:
        self.spacing = 4
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.controls = self._build_controls()
