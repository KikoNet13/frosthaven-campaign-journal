from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from frosthaven_campaign_journal.state.placeholders import (
    EntryRef,
    MainScreenLocalState,
    MockEntry,
    MockWeek,
    ViewerSessionItem,
)


@dataclass(frozen=True)
class MainShellViewData:
    state: MainScreenLocalState
    years: list[int]
    weeks_for_selected_year: list[MockWeek]
    entries_for_selected_week: list[MockEntry]
    viewer_entry: MockEntry | None
    viewer_sessions: list[ViewerSessionItem]
    entries_panel_error_message: str | None
    viewer_sessions_error_message: str | None
    session_write_error_message: str | None
    session_write_pending: bool
    week_write_error_message: str | None
    week_write_pending: bool
    entry_write_error_message: str | None
    entry_write_pending: bool
    resource_write_error_message: str | None
    resource_write_pending: bool
    campaign_write_pending: bool
    resource_draft_values: dict[str, int] | None
    resource_draft_dirty: bool
    resource_draft_attached_to_viewer: bool
    active_entry_ref: EntryRef | None
    active_entry_label: str | None
    active_status_error_message: str | None
    campaign_resource_totals: dict[str, int] | None
    read_status: str
    read_error_message: str | None
    read_warning_message: str | None
    viewport_width: int | float | None
    viewport_height: int | float | None
    env_name: str


@dataclass(frozen=True)
class MainShellViewActions:
    on_prev_year: Callable[[], None]
    on_next_year: Callable[[], None]
    on_open_extend_year_plus_one_confirm: Callable[[], None]
    on_select_week: Callable[[int], None]
    on_select_entry: Callable[[EntryRef], None]
    on_manual_refresh: Callable[[], None]
    on_begin_session: Callable[[], None]
    on_end_session: Callable[[], None]
    on_open_manual_create_session: Callable[[], None]
    on_open_manual_edit_session: Callable[[str], None]
    on_open_manual_delete_session: Callable[[str], None]
    on_open_week_notes_modal: Callable[[], None]
    on_request_week_close: Callable[[], None]
    on_request_week_reopen: Callable[[], None]
    on_request_week_reclose: Callable[[], None]
    on_open_entry_add_modal: Callable[[], None]
    on_open_edit_entry_modal: Callable[[], None]
    on_open_entry_delete_confirm: Callable[[], None]
    on_reorder_entry_up: Callable[[], None]
    on_reorder_entry_down: Callable[[], None]
    on_adjust_resource_draft_delta: Callable[[str, int], None]
    on_save_resource_draft: Callable[[], None]
    on_discard_resource_draft: Callable[[], None]


