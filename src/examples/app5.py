from __future__ import annotations

from dataclasses import dataclass

import flet as ft

if __package__:
    from .counter import Counter
else:
    from counter import Counter


@ft.observable
@dataclass
class AppExampleState:
    value1: int = 0
    value2: int = 0
    value3: int = 0
    value4: int = 0

    def inc(self, field_name: str) -> None:
        setattr(self, field_name, int(getattr(self, field_name)) + 1)

    def dec(self, field_name: str) -> None:
        setattr(self, field_name, int(getattr(self, field_name)) - 1)

@ft.component
def AppExample():
    state, _ = ft.use_state(AppExampleState)

    return ft.Column(
        controls=[
            ft.Text(value="App 5 - Reusable Counter Control"),
            Counter(
                label="Counter 1",
                value=state.value1,
                on_increment_click=lambda _: state.inc("value1"),
                on_decrement_click=lambda _: state.dec("value1"),
            ),
            Counter(
                label="Counter 2",
                value=state.value2,
                on_increment_click=lambda _: state.inc("value2"),
                on_decrement_click=lambda _: state.dec("value2"),
            ),
            Counter(
                label="Counter 3",
                value=state.value3,
                on_increment_click=lambda _: state.inc("value3"),
                on_decrement_click=lambda _: state.dec("value3"),
            ),
            Counter(
                label="Counter 4",
                value=state.value4,
                on_increment_click=lambda _: state.inc("value4"),
                on_decrement_click=lambda _: state.dec("value4"),
            ),
            ft.Divider(),
            ft.Text(
                value=(
                    f"Snapshot -> value1={state.value1}, value2={state.value2}, "
                    f"value3={state.value3}, value4={state.value4}"
                )
            ),
        ]
    )


def main(page: ft.Page) -> None:
    page.title = "App 5 - Control Reusable"
    page.padding = 16
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.render(AppExample)


if __name__ == "__main__":
    ft.run(main)
