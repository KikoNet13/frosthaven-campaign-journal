from __future__ import annotations

from typing import Callable

import flet as ft
from flet.controls.base_control import skip_field


CounterClickHandler = Callable[[ft.ControlEvent], None]


@ft.control
class Counter(ft.Row):
    label: str = "Counter"
    value: int = 0
    on_increment_click: CounterClickHandler | None = skip_field()
    on_decrement_click: CounterClickHandler | None = skip_field()
    _label_text: ft.Text | None = skip_field()
    _value_text: ft.Text | None = skip_field()

    def _handle_increment(self, e: ft.ControlEvent) -> None:
        if self.on_increment_click:
            self.on_increment_click(e)

    def _handle_decrement(self, e: ft.ControlEvent) -> None:
        if self.on_decrement_click:
            self.on_decrement_click(e)

    def init(self) -> None:
        self.alignment = ft.MainAxisAlignment.START
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 8
        self._label_text = ft.Text(self.label, width=90)
        self._value_text = ft.Text(
            value=str(self.value),
            width=40,
            text_align=ft.TextAlign.CENTER,
            color=(ft.Colors.ERROR if self.value > 10 else ft.Colors.PRIMARY),
        )
        self.controls = [
            self._label_text,
            ft.IconButton(ft.Icons.REMOVE_CIRCLE, on_click=self._handle_decrement),
            self._value_text,
            ft.IconButton(ft.Icons.ADD_CIRCLE, on_click=self._handle_increment),
        ]

    def before_update(self) -> None:
        if self._label_text:
            self._label_text.value = self.label
        if self._value_text:
            self._value_text.value = str(self.value)
            self._value_text.color = (
                ft.Colors.ERROR if self.value > 10 else ft.Colors.PRIMARY
            )
