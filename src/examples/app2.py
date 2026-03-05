import flet as ft


@ft.component
def Counter(value: int):

    def inc():
        value += 1

    def dec():
        value -= 1

    return ft.Row(
        controls=[
            ft.IconButton(ft.Icons.REMOVE, on_click=dec),
            ft.Text(
                value=f"{value}",
                color=(ft.Colors.ERROR if value > 10 else ft.Colors.PRIMARY),
            ),
            ft.IconButton(ft.Icons.ADD, on_click=inc),
        ],
    )


@ft.observable
class AppExampleStates:
    value1: int = 0
    value2: int = 0
    value3: int = 0
    value4: int = 0


@ft.component
def AppExample():

    state, _ = ft.use_state(AppExampleStates())

    return ft.Column(
        controls=[
            Counter(state.value1),
            Counter(state.value2),
            Counter(state.value3),
            Counter(state.value4),
        ]
    )
