from __future__ import annotations

from typing import Callable

import flet as ft
from flet.controls.base_control import skip_field

from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_DELTA_NEGATIVE,
    COLOR_DELTA_POSITIVE,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
)


ResourceDeltaClickHandler = Callable[[ft.ControlEvent], None]


@ft.control
class ResourceDeltaRow(ft.Row):
    resource_key: str = ""
    label_es: str = ""
    icon_src: str = ""
    delta_value: int = 0
    projected_total: int | None = None
    disabled: bool = False
    on_decrement_click: ResourceDeltaClickHandler | None = skip_field()
    on_increment_click: ResourceDeltaClickHandler | None = skip_field()

    def _handle_decrement(self, event: ft.ControlEvent) -> None:
        if self.on_decrement_click is not None:
            self.on_decrement_click(event)

    def _handle_increment(self, event: ft.ControlEvent) -> None:
        if self.on_increment_click is not None:
            self.on_increment_click(event)

    def _build_controls(self) -> list[ft.Control]:
        return [
            ft.Image(
                src=self.icon_src,
                width=24,
                height=24,
            ),
            ft.Row(
                expand=True,
                spacing=4,
                controls=[
                    ft.Text(
                        value=self.label_es,
                        size=13,
                        weight=ft.FontWeight.W_600,
                        color=COLOR_TEXT_PRIMARY,
                    ),
                    ft.Text(
                        value=_format_projected_total_text(self.projected_total),
                        size=12,
                        color=COLOR_TEXT_MUTED,
                        italic=True,
                    ),
                ],
            ),
            ft.IconButton(
                icon=ft.Icons.REMOVE,
                icon_size=16,
                tooltip="Restar 1",
                on_click=self._handle_decrement,
                disabled=self.disabled,
            ),
            ft.Text(
                value=_format_delta_text(self.delta_value),
                size=14,
                width=42,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.W_700,
                color=_delta_text_color(self.delta_value),
            ),
            ft.IconButton(
                icon=ft.Icons.ADD,
                icon_size=16,
                tooltip="Sumar 1",
                on_click=self._handle_increment,
                disabled=self.disabled,
            ),
        ]

    def init(self) -> None:
        super().init()
        self.alignment = ft.MainAxisAlignment.START
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 10
        self.controls = self._build_controls()

    def before_update(self) -> None:
        self.alignment = ft.MainAxisAlignment.START
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 10
        self.controls = self._build_controls()


def _format_delta_text(delta_value: int) -> str:
    if delta_value > 0:
        return f"+{delta_value}"
    return str(delta_value)


def _format_projected_total_text(projected_total: int | None) -> str:
    if projected_total is None:
        return "(Total: N/D)"
    return f"(Total: {projected_total})"


def _delta_text_color(delta_value: int) -> str:
    if delta_value > 0:
        return COLOR_DELTA_POSITIVE
    if delta_value < 0:
        return COLOR_DELTA_NEGATIVE
    return COLOR_TEXT_PRIMARY
