from __future__ import annotations

import flet as ft


@ft.control(isolated=True)
class LabeledGroupBox(ft.Stack):
    label: str = ""
    content: ft.Control | None = None
    bgcolor: str = ""
    border_color: str = ""
    label_bgcolor: str = ""
    label_border_color: str = ""
    label_text_color: str = ""
    width: int | None = None
    padding: ft.Padding | None = None
    border_radius: int = 6
    label_left: int = 10
    label_top: int = 0
    label_text_size: int = 10
    label_text_weight: ft.FontWeight = ft.FontWeight.W_600
    label_overlap: int = 6

    def _resolved_padding(self) -> ft.Padding:
        return self.padding or ft.Padding(left=8, top=8, right=8, bottom=6)

    def _build_controls(self) -> list[ft.Control]:
        label_text = ft.Text(
            self.label,
            size=self.label_text_size,
            weight=self.label_text_weight,
            color=self.label_text_color,
            no_wrap=True,
        )
        base_container = ft.Container(
            width=self.width,
            margin=ft.Margin(top=max(0, self.label_overlap), right=0, bottom=0, left=0),
            padding=self._resolved_padding(),
            bgcolor=self.bgcolor,
            border=ft.Border.all(1, self.border_color),
            border_radius=self.border_radius,
            content=self.content,
        )
        label_container = ft.Container(
            padding=ft.Padding(left=8, top=1, right=8, bottom=1),
            margin=ft.Margin(
                left=self.label_left,
                top=max(0, self.label_top),
                right=0,
                bottom=0,
            ),
            bgcolor=self.label_bgcolor,
            border=ft.Border.all(1, self.label_border_color),
            border_radius=999,
            content=label_text,
        )
        return [base_container, label_container]

    def init(self) -> None:
        super().init()
        self.alignment = ft.Alignment(-1, -1)
        self.clip_behavior = ft.ClipBehavior.NONE
        self.controls = self._build_controls()

    def before_update(self) -> None:
        self.alignment = ft.Alignment(-1, -1)
        self.clip_behavior = ft.ClipBehavior.NONE
        self.controls = self._build_controls()
