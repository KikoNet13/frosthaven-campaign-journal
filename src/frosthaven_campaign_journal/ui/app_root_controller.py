from __future__ import annotations

from collections.abc import Callable

import flet as ft

from frosthaven_campaign_journal.config import load_settings
from frosthaven_campaign_journal.data import build_firestore_client
from frosthaven_campaign_journal.ui.features.main_shell.contracts import (
    MainShellViewActions,
    MainShellViewData,
)
from frosthaven_campaign_journal.ui.features.main_shell.dispatcher import MainShellDispatcher
from frosthaven_campaign_journal.ui.features.main_shell.effects import MainShellEffects
from frosthaven_campaign_journal.ui.features.main_shell.intents import (
    AdjustResourceDraftDeltaPressed,
    AppStarted,
    DiscardResourceDraftPressed,
    MainShellIntent,
    ManualRefreshPressed,
    NextYearPressed,
    OpenEntryAddModalPressed,
    OpenEntryDeleteConfirmPressed,
    OpenEditEntryModalPressed,
    OpenExtendYearPlusOneConfirmPressed,
    OpenManualCreateSessionPressed,
    OpenManualDeleteSessionPressed,
    OpenManualEditSessionPressed,
    OpenWeekNotesModalPressed,
    PrevYearPressed,
    ReorderEntryDownPressed,
    ReorderEntryUpPressed,
    RequestWeekClosePressed,
    RequestWeekReclosePressed,
    RequestWeekReopenPressed,
    SaveResourceDraftPressed,
    SelectEntryPressed,
    SelectWeekPressed,
    StartSessionPressed,
    StopSessionPressed,
    ViewportChanged,
)
from frosthaven_campaign_journal.ui.features.main_shell.screen import build_main_shell_screen
from frosthaven_campaign_journal.ui.features.main_shell.selectors import (
    entries_for_selected_week,
    resource_draft_attached_to_viewer,
    viewer_entry,
    weeks_for_selected_year,
)
from frosthaven_campaign_journal.ui.features.main_shell.state import MainShellState


def build_app_root_controller(page: ft.Page) -> ft.Control:
    return AppRootController(page).build()


class AppRootController:
    def __init__(self, page: ft.Page) -> None:
        self._page = page
        self._state = MainShellState()
        self._shell_host = ft.Container(expand=True)
        self._safe_root = ft.SafeArea(expand=True, content=self._shell_host)
        self._root = ft.Container(expand=True, content=self._safe_root)
        self._effects = MainShellEffects(page=page, build_client=self._build_client)
        self._dispatcher = MainShellDispatcher(
            page=page,
            state=self._state,
            effects=self._effects,
            render=self._render_shell,
        )

    def build(self) -> ft.Control:
        self._page.on_media_change = lambda _e: self._dispatcher.dispatch(ViewportChanged())
        self._sync_root_height_to_viewport()
        self._dispatcher.dispatch(AppStarted())
        return self._root

    def _build_client(self):
        settings = load_settings()
        return build_firestore_client(settings)

    def _sync_root_height_to_viewport(self) -> None:
        viewport_height = getattr(self._page, "height", None)
        if not isinstance(viewport_height, (int, float)) or viewport_height <= 0:
            viewport_height = 900
        self._root.height = viewport_height

    def _render_shell(
        self,
        state: MainShellState,
        dispatch: Callable[[MainShellIntent], None],
    ) -> None:
        self._sync_root_height_to_viewport()

        data = MainShellViewData(
            state=state.local_state,
            years=state.read_state.years,
            weeks_for_selected_year=weeks_for_selected_year(state),
            entries_for_selected_week=entries_for_selected_week(state),
            viewer_entry=viewer_entry(state),
            viewer_sessions=state.entry_panel_state.viewer_sessions,
            entries_panel_error_message=state.entry_panel_state.entries_panel_error_message,
            viewer_sessions_error_message=state.entry_panel_state.viewer_sessions_error_message,
            session_write_error_message=state.entry_panel_state.session_write_error_message,
            session_write_pending=state.entry_panel_state.session_write_pending,
            week_write_error_message=state.entry_panel_state.week_write_error_message,
            week_write_pending=state.entry_panel_state.week_write_pending,
            entry_write_error_message=state.entry_panel_state.entry_write_error_message,
            entry_write_pending=state.entry_panel_state.entry_write_pending,
            resource_write_error_message=state.entry_panel_state.resource_write_error_message,
            resource_write_pending=state.entry_panel_state.resource_write_pending,
            campaign_write_pending=state.read_state.campaign_write_pending,
            resource_draft_values=(
                dict(state.entry_panel_state.resource_draft_values)
                if resource_draft_attached_to_viewer(state)
                else None
            ),
            resource_draft_dirty=(
                state.entry_panel_state.resource_draft_dirty
                and resource_draft_attached_to_viewer(state)
            ),
            resource_draft_attached_to_viewer=resource_draft_attached_to_viewer(state),
            active_entry_ref=state.read_state.active_entry_ref,
            active_entry_label=state.read_state.active_entry_label,
            active_status_error_message=state.read_state.active_status_error_message,
            campaign_resource_totals=state.read_state.campaign_resource_totals,
            read_status=state.read_state.status,
            read_error_message=state.read_state.error_message,
            read_warning_message=state.read_state.warning_message,
            viewport_width=getattr(self._page, "width", None),
            viewport_height=getattr(self._page, "height", None),
            env_name=load_settings().env,
        )
        actions = MainShellViewActions(
            on_prev_year=lambda: dispatch(PrevYearPressed()),
            on_next_year=lambda: dispatch(NextYearPressed()),
            on_open_extend_year_plus_one_confirm=lambda: dispatch(OpenExtendYearPlusOneConfirmPressed()),
            on_select_week=lambda week_number: dispatch(SelectWeekPressed(week_number=week_number)),
            on_select_entry=lambda entry_ref: dispatch(SelectEntryPressed(entry_ref=entry_ref)),
            on_manual_refresh=lambda: dispatch(ManualRefreshPressed()),
            on_begin_session=lambda: dispatch(StartSessionPressed()),
            on_end_session=lambda: dispatch(StopSessionPressed()),
            on_open_manual_create_session=lambda: dispatch(OpenManualCreateSessionPressed()),
            on_open_manual_edit_session=lambda session_id: dispatch(
                OpenManualEditSessionPressed(session_id=session_id)
            ),
            on_open_manual_delete_session=lambda session_id: dispatch(
                OpenManualDeleteSessionPressed(session_id=session_id)
            ),
            on_open_week_notes_modal=lambda: dispatch(OpenWeekNotesModalPressed()),
            on_request_week_close=lambda: dispatch(RequestWeekClosePressed()),
            on_request_week_reopen=lambda: dispatch(RequestWeekReopenPressed()),
            on_request_week_reclose=lambda: dispatch(RequestWeekReclosePressed()),
            on_open_entry_add_modal=lambda: dispatch(OpenEntryAddModalPressed()),
            on_open_edit_entry_modal=lambda: dispatch(OpenEditEntryModalPressed()),
            on_open_entry_delete_confirm=lambda: dispatch(OpenEntryDeleteConfirmPressed()),
            on_reorder_entry_up=lambda: dispatch(ReorderEntryUpPressed()),
            on_reorder_entry_down=lambda: dispatch(ReorderEntryDownPressed()),
            on_adjust_resource_draft_delta=lambda key, delta: dispatch(
                AdjustResourceDraftDeltaPressed(resource_key=key, adjustment_delta=delta)
            ),
            on_save_resource_draft=lambda: dispatch(SaveResourceDraftPressed()),
            on_discard_resource_draft=lambda: dispatch(DiscardResourceDraftPressed()),
        )
        self._shell_host.content = build_main_shell_screen(data=data, actions=actions)


