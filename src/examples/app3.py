import flet as ft
from dataclasses import dataclass


@ft.observable
@dataclass
class AppExampleState:
    value1: int = 0
    value2: int = 0
    value3: int = 0
    value4: int = 0


@ft.component
def Counter(label: str, app_state: AppExampleState, field_name: str):
    def inc(_=None):
        current = int(getattr(app_state, field_name))
        setattr(app_state, field_name, current + 1)

    def dec(_=None):
        current = int(getattr(app_state, field_name))
        setattr(app_state, field_name, current - 1)

    value = int(getattr(app_state, field_name))

    return ft.Row(
        controls=[
            ft.Text(label, width=90),
            ft.IconButton(ft.Icons.REMOVE, on_click=dec),
            ft.Text(
                value=f"{value}",
                width=40,
                text_align=ft.TextAlign.CENTER,
                color=(ft.Colors.ERROR if value > 10 else ft.Colors.PRIMARY),
            ),
            ft.IconButton(ft.Icons.ADD, on_click=inc),
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


@ft.component
def AppExample():
    state, _ = ft.use_state(AppExampleState())

    return ft.Column(
        controls=[
            ft.Text(value="General (4 counters)"),
            Counter("Counter 1", state, "value1"),
            Counter("Counter 2", state, "value2"),
            Counter("Counter 3", state, "value3"),
            Counter("Counter 4", state, "value4"),
        ]
    )
