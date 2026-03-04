import flet as ft


@ft.observable
class CounterState:
    count: int = 0

    def inc(self):
        self.count += 1

    def dec(self):
        self.count -= 1


@ft.component
def Counter(state: CounterState):

    # state, _ = ft.use_state(CounterState())

    return ft.Row(
        controls=[
            ft.IconButton(ft.Icons.REMOVE, on_click=state.dec),
            ft.Text(
                value=f"{state.count}",
                color=(ft.Colors.ERROR if state.count > 10 else ft.Colors.PRIMARY),
            ),
            ft.IconButton(ft.Icons.ADD, on_click=state.inc),
        ],
    )


@ft.observable
class AppExampleStates:
    counters_states = [CounterState() for _ in range(4)]


@ft.component
def AppExample():

    state, _ = ft.use_state(AppExampleStates())

    return ft.Column(
        [Counter(counter_state) for counter_state in state.counters_states]
    )
