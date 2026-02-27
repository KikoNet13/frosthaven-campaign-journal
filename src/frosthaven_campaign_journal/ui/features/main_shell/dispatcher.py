from __future__ import annotations

from collections import deque
from collections.abc import Callable

import flet as ft

from frosthaven_campaign_journal.ui.features.main_shell.effects import MainShellEffects
from frosthaven_campaign_journal.ui.features.main_shell.intents import MainShellIntent
from frosthaven_campaign_journal.ui.features.main_shell.reducer import reduce
from frosthaven_campaign_journal.ui.features.main_shell.state import MainShellState


class MainShellDispatcher:
    def __init__(
        self,
        *,
        page: ft.Page,
        state: MainShellState,
        effects: MainShellEffects,
        render: Callable[[MainShellState, Callable[[MainShellIntent], None]], None],
    ) -> None:
        self._page = page
        self._state = state
        self._effects = effects
        self._render = render

    @property
    def state(self) -> MainShellState:
        return self._state

    def dispatch(self, intent: MainShellIntent) -> None:
        queue: deque[MainShellIntent] = deque([intent])
        safety_counter = 0
        while queue:
            safety_counter += 1
            if safety_counter > 200:
                break

            current_intent = queue.popleft()
            self._state, effects = reduce(self._state, current_intent)
            self._render(self._state, self.dispatch)

            for effect in effects:
                self._effects.run(
                    effect=effect,
                    state=self._state,
                    dispatch=queue.append,
                )
                self._render(self._state, self.dispatch)

        self._page.update()

