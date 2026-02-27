from __future__ import annotations

from dataclasses import dataclass, field

from frosthaven_campaign_journal.state.placeholders import EntryRef, MockEntry, MockWeek, ViewerSessionItem


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

