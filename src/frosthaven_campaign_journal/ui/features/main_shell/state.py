from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

import flet as ft

from frosthaven_campaign_journal.config import load_settings
from frosthaven_campaign_journal.state.placeholders import (
    ENTRY_RESOURCE_KEYS,
    EntryRef,
    MainScreenLocalState,
    MockEntry,
    MockWeek,
    ViewerSessionItem,
    build_initial_main_screen_state,
    build_mock_main_screen_dataset,
)
from frosthaven_campaign_journal.ui.features.main_shell.model import MainShellViewActions, MainShellViewData


@dataclass
class MainScreenReadState:
    status: str = "idle"
    error_message: str | None = None
    warning_message: str | None = None
    years: list[int] = field(default_factory=list)
    weeks_by_year: dict[int, list[MockWeek]] = field(default_factory=dict)
    campaign_resource_totals: dict[str, int] | None = None
    active_entry_ref: EntryRef | None = None
    active_entry_label: str | None = None
    active_status_error_message: str | None = None
    campaign_write_pending: bool = False


@dataclass
class EntryPanelReadState:
    entries_for_selected_week: list[MockEntry] = field(default_factory=list)
    entries_panel_error_message: str | None = None
    viewer_entry_snapshot: MockEntry | None = None
    viewer_sessions: list[ViewerSessionItem] = field(default_factory=list)
    viewer_sessions_error_message: str | None = None
    session_write_error_message: str | None = None
    session_write_pending: bool = False
    week_write_error_message: str | None = None
    week_write_pending: bool = False
    entry_write_error_message: str | None = None
    entry_write_pending: bool = False
    resource_write_error_message: str | None = None
    resource_write_pending: bool = False
    resource_draft_entry_ref: EntryRef | None = None
    resource_draft_values: dict[str, int] = field(default_factory=dict)
    resource_draft_dirty: bool = False
    resource_draft_discard_notice: str | None = None


@dataclass
class MainShellState:
    page: ft.Page
    local_state: MainScreenLocalState = field(default_factory=build_initial_main_screen_state)
    read_state: MainScreenReadState = field(default_factory=MainScreenReadState)
    entry_panel_state: EntryPanelReadState = field(default_factory=EntryPanelReadState)
    _entries_by_week: dict[tuple[int, int], list[MockEntry]] = field(default_factory=dict)

    def initialize(self) -> None:
        dataset = build_mock_main_screen_dataset()
        self.read_state.years = dataset.years
        self.read_state.weeks_by_year = dataset.weeks_by_year
        self._entries_by_week = dataset.entries_by_week
        if dataset.years:
            self.local_state.selected_year = dataset.years[0]
            weeks = dataset.weeks_by_year.get(dataset.years[0], [])
            self.local_state.selected_week = weeks[0].week_number if weeks else None
        self._refresh_entries_for_week()
        self.read_state.status = "ready"

    def on_prev_year(self) -> None:
        self._move_year(-1)

    def on_next_year(self) -> None:
        self._move_year(1)

    def on_open_extend_year_plus_one_confirm(self) -> None:
        self.read_state.warning_message = "Extensión de año pendiente en MVP."

    def on_select_week(self, week_number: int) -> None:
        self.local_state.selected_week = week_number
        self.local_state.viewer_entry_ref = None
        self._refresh_entries_for_week()

    def on_select_entry(self, entry_ref: EntryRef) -> None:
        self.local_state.viewer_entry_ref = entry_ref
        self.entry_panel_state.viewer_entry_snapshot = self._find_entry(entry_ref)
        self._sync_resource_draft_from_viewer()

    def on_manual_refresh(self) -> None:
        self._refresh_entries_for_week()

    def on_begin_session(self) -> None:
        self.read_state.warning_message = "Control de sesiones en modo placeholder."

    def on_end_session(self) -> None:
        self.read_state.warning_message = "Control de sesiones en modo placeholder."

    def on_open_manual_create_session(self) -> None:
        self.read_state.warning_message = "Acción no disponible en este slice."

    def on_open_manual_edit_session(self, _session_id: str) -> None:
        self.read_state.warning_message = "Acción no disponible en este slice."

    def on_open_manual_delete_session(self, _session_id: str) -> None:
        self.read_state.warning_message = "Acción no disponible en este slice."

    def on_open_week_notes_modal(self) -> None:
        self.read_state.warning_message = "Acción no disponible en este slice."

    def on_request_week_close(self) -> None:
        self.read_state.warning_message = "Acción no disponible en este slice."

    def on_request_week_reopen(self) -> None:
        self.read_state.warning_message = "Acción no disponible en este slice."

    def on_request_week_reclose(self) -> None:
        self.read_state.warning_message = "Acción no disponible en este slice."

    def on_open_entry_add_modal(self) -> None:
        self.read_state.warning_message = "Acción no disponible en este slice."

    def on_open_edit_entry_modal(self) -> None:
        self.read_state.warning_message = "Acción no disponible en este slice."

    def on_open_entry_delete_confirm(self) -> None:
        self.read_state.warning_message = "Acción no disponible en este slice."

    def on_reorder_entry_up(self) -> None:
        self.read_state.warning_message = "Acción no disponible en este slice."

    def on_reorder_entry_down(self) -> None:
        self.read_state.warning_message = "Acción no disponible en este slice."

    def on_adjust_resource_draft_delta(self, resource_key: str, adjustment_delta: int) -> None:
        if resource_key not in ENTRY_RESOURCE_KEYS:
            return
        current = self.entry_panel_state.resource_draft_values.get(resource_key, 0)
        updated = current + adjustment_delta
        if updated == 0:
            self.entry_panel_state.resource_draft_values.pop(resource_key, None)
        else:
            self.entry_panel_state.resource_draft_values[resource_key] = updated
        self.entry_panel_state.resource_draft_dirty = True

    def on_save_resource_draft(self) -> None:
        self.entry_panel_state.resource_draft_dirty = False

    def on_discard_resource_draft(self) -> None:
        self._sync_resource_draft_from_viewer()

    def build_view_data(self) -> MainShellViewData:
        return MainShellViewData(
            state=self.local_state,
            years=self.read_state.years,
            weeks_for_selected_year=self._weeks_for_selected_year(),
            entries_for_selected_week=self.entry_panel_state.entries_for_selected_week,
            viewer_entry=self.entry_panel_state.viewer_entry_snapshot,
            viewer_sessions=self.entry_panel_state.viewer_sessions,
            entries_panel_error_message=self.entry_panel_state.entries_panel_error_message,
            viewer_sessions_error_message=self.entry_panel_state.viewer_sessions_error_message,
            session_write_error_message=self.entry_panel_state.session_write_error_message,
            session_write_pending=self.entry_panel_state.session_write_pending,
            week_write_error_message=self.entry_panel_state.week_write_error_message,
            week_write_pending=self.entry_panel_state.week_write_pending,
            entry_write_error_message=self.entry_panel_state.entry_write_error_message,
            entry_write_pending=self.entry_panel_state.entry_write_pending,
            resource_write_error_message=self.entry_panel_state.resource_write_error_message,
            resource_write_pending=self.entry_panel_state.resource_write_pending,
            campaign_write_pending=self.read_state.campaign_write_pending,
            resource_draft_values=(
                dict(self.entry_panel_state.resource_draft_values)
                if self._resource_draft_attached_to_viewer()
                else None
            ),
            resource_draft_dirty=self.entry_panel_state.resource_draft_dirty,
            resource_draft_attached_to_viewer=self._resource_draft_attached_to_viewer(),
            active_entry_ref=self.read_state.active_entry_ref,
            active_entry_label=self.read_state.active_entry_label,
            active_status_error_message=self.read_state.active_status_error_message,
            campaign_resource_totals=self.read_state.campaign_resource_totals,
            read_status=self.read_state.status,
            read_error_message=self.read_state.error_message,
            read_warning_message=self.read_state.warning_message,
            viewport_width=getattr(self.page, "width", None),
            viewport_height=getattr(self.page, "height", None),
            env_name=load_settings().env,
        )

    def build_actions(self, refresh: Callable[[], None]) -> MainShellViewActions:
        return MainShellViewActions(
            on_prev_year=lambda: self._run_and_refresh(self.on_prev_year, refresh),
            on_next_year=lambda: self._run_and_refresh(self.on_next_year, refresh),
            on_open_extend_year_plus_one_confirm=lambda: self._run_and_refresh(
                self.on_open_extend_year_plus_one_confirm, refresh
            ),
            on_select_week=lambda week_number: self._run_and_refresh(lambda: self.on_select_week(week_number), refresh),
            on_select_entry=lambda entry_ref: self._run_and_refresh(lambda: self.on_select_entry(entry_ref), refresh),
            on_manual_refresh=lambda: self._run_and_refresh(self.on_manual_refresh, refresh),
            on_begin_session=lambda: self._run_and_refresh(self.on_begin_session, refresh),
            on_end_session=lambda: self._run_and_refresh(self.on_end_session, refresh),
            on_open_manual_create_session=lambda: self._run_and_refresh(self.on_open_manual_create_session, refresh),
            on_open_manual_edit_session=lambda session_id: self._run_and_refresh(
                lambda: self.on_open_manual_edit_session(session_id), refresh
            ),
            on_open_manual_delete_session=lambda session_id: self._run_and_refresh(
                lambda: self.on_open_manual_delete_session(session_id), refresh
            ),
            on_open_week_notes_modal=lambda: self._run_and_refresh(self.on_open_week_notes_modal, refresh),
            on_request_week_close=lambda: self._run_and_refresh(self.on_request_week_close, refresh),
            on_request_week_reopen=lambda: self._run_and_refresh(self.on_request_week_reopen, refresh),
            on_request_week_reclose=lambda: self._run_and_refresh(self.on_request_week_reclose, refresh),
            on_open_entry_add_modal=lambda: self._run_and_refresh(self.on_open_entry_add_modal, refresh),
            on_open_edit_entry_modal=lambda: self._run_and_refresh(self.on_open_edit_entry_modal, refresh),
            on_open_entry_delete_confirm=lambda: self._run_and_refresh(self.on_open_entry_delete_confirm, refresh),
            on_reorder_entry_up=lambda: self._run_and_refresh(self.on_reorder_entry_up, refresh),
            on_reorder_entry_down=lambda: self._run_and_refresh(self.on_reorder_entry_down, refresh),
            on_adjust_resource_draft_delta=lambda key, delta: self._run_and_refresh(
                lambda: self.on_adjust_resource_draft_delta(key, delta), refresh
            ),
            on_save_resource_draft=lambda: self._run_and_refresh(self.on_save_resource_draft, refresh),
            on_discard_resource_draft=lambda: self._run_and_refresh(self.on_discard_resource_draft, refresh),
        )

    def _run_and_refresh(self, operation: Callable[[], None], refresh: Callable[[], None]) -> None:
        operation()
        refresh()

    def _move_year(self, delta: int) -> None:
        if not self.read_state.years:
            return
        current = self.local_state.selected_year
        if current not in self.read_state.years:
            current = self.read_state.years[0]
        index = self.read_state.years.index(current)
        target_index = max(0, min(len(self.read_state.years) - 1, index + delta))
        self.local_state.selected_year = self.read_state.years[target_index]
        weeks = self._weeks_for_selected_year()
        self.local_state.selected_week = weeks[0].week_number if weeks else None
        self.local_state.viewer_entry_ref = None
        self._refresh_entries_for_week()

    def _weeks_for_selected_year(self) -> list[MockWeek]:
        if self.local_state.selected_year is None:
            return []
        return self.read_state.weeks_by_year.get(self.local_state.selected_year, [])

    def _refresh_entries_for_week(self) -> None:
        if self.local_state.selected_year is None or self.local_state.selected_week is None:
            self.entry_panel_state.entries_for_selected_week = []
            self.entry_panel_state.viewer_entry_snapshot = None
            return
        entries = self._entries_by_week.get((self.local_state.selected_year, self.local_state.selected_week), [])
        self.entry_panel_state.entries_for_selected_week = entries
        if entries:
            self.local_state.viewer_entry_ref = entries[0].ref
            self.entry_panel_state.viewer_entry_snapshot = entries[0]
            self._sync_resource_draft_from_viewer()
        else:
            self.local_state.viewer_entry_ref = None
            self.entry_panel_state.viewer_entry_snapshot = None
            self.entry_panel_state.resource_draft_entry_ref = None
            self.entry_panel_state.resource_draft_values = {}
            self.entry_panel_state.resource_draft_dirty = False

    def _find_entry(self, entry_ref: EntryRef) -> MockEntry | None:
        for entry in self.entry_panel_state.entries_for_selected_week:
            if entry.ref == entry_ref:
                return entry
        return None

    def _sync_resource_draft_from_viewer(self) -> None:
        viewer = self.entry_panel_state.viewer_entry_snapshot
        if viewer is None:
            self.entry_panel_state.resource_draft_entry_ref = None
            self.entry_panel_state.resource_draft_values = {}
            self.entry_panel_state.resource_draft_dirty = False
            return
        self.entry_panel_state.resource_draft_entry_ref = viewer.ref
        self.entry_panel_state.resource_draft_values = dict(viewer.resource_deltas)
        self.entry_panel_state.resource_draft_dirty = False

    def _resource_draft_attached_to_viewer(self) -> bool:
        return (
            self.local_state.viewer_entry_ref is not None
            and self.entry_panel_state.resource_draft_entry_ref == self.local_state.viewer_entry_ref
        )
