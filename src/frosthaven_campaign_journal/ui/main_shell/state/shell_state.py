from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import flet as ft

from frosthaven_campaign_journal.config import load_settings
from frosthaven_campaign_journal.models import (
    MainScreenLocalState,
    build_initial_main_screen_state,
)
from frosthaven_campaign_journal.ui.main_shell.state.navigation import MainShellNavigationMixin
from frosthaven_campaign_journal.ui.main_shell.state.runtime_read import MainShellRuntimeReadMixin
from frosthaven_campaign_journal.ui.main_shell.state.runtime_support import MainShellRuntimeSupportMixin
from frosthaven_campaign_journal.ui.main_shell.state.runtime_write import MainShellRuntimeWriteMixin
from frosthaven_campaign_journal.ui.main_shell.state.sessions import MainShellSessionActionsMixin
from frosthaven_campaign_journal.ui.main_shell.state.view_data import MainShellViewDataMixin
from frosthaven_campaign_journal.ui.main_shell.state.week_entry_resources import (
    MainShellWeekEntryResourceActionsMixin,
)
from frosthaven_campaign_journal.ui.main_shell.state.types import (
    ConfirmationState,
    EntryFormState,
    EntryNotesEditorState,
    EntryPanelReadState,
    MainScreenReadState,
    SessionFormState,
)


@ft.observable
@dataclass
class MainShellState(
    MainShellNavigationMixin,
    MainShellSessionActionsMixin,
    MainShellWeekEntryResourceActionsMixin,
    MainShellViewDataMixin,
    MainShellRuntimeReadMixin,
    MainShellRuntimeSupportMixin,
    MainShellRuntimeWriteMixin,
):
    local_state: MainScreenLocalState = field(default_factory=build_initial_main_screen_state)
    read_state: MainScreenReadState = field(default_factory=MainScreenReadState)
    entry_panel_state: EntryPanelReadState = field(default_factory=EntryPanelReadState)
    env_name: str = field(default_factory=lambda: load_settings().env)
    confirmation_state: ConfirmationState = field(default_factory=ConfirmationState)
    entry_form_state: EntryFormState | None = None
    entry_notes_editor_state: EntryNotesEditorState | None = None
    session_form_state: SessionFormState | None = None
    info_message: str | None = None
    _pending_context_action: Callable[[], None] | None = field(default=None, init=False, repr=False)
    _pending_context_action_label: str | None = field(default=None, init=False, repr=False)

    @classmethod
    def create(cls) -> MainShellState:
        state = cls()
        state.initialize()
        return state
