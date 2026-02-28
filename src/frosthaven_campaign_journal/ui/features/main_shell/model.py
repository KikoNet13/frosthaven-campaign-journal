from __future__ import annotations

from dataclasses import dataclass

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
    env_name: str
