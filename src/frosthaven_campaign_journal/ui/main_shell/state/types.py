from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from frosthaven_campaign_journal.models import EntryRef, EntrySummary, ViewerSessionItem, WeekSummary


@dataclass
class MainScreenReadState:
    status: str = "idle"
    error_message: str | None = None
    warning_message: str | None = None
    years: list[int] = field(default_factory=list)
    weeks_by_year: dict[int, list[WeekSummary]] = field(default_factory=dict)
    campaign_resource_totals: dict[str, int] | None = None
    active_entry_ref: EntryRef | None = None
    active_entry_label: str | None = None
    active_session_started_at_utc: object | None = None
    active_status_error_message: str | None = None
    campaign_write_pending: bool = False


@dataclass
class EntryPanelReadState:
    entries_for_selected_week: list[EntrySummary] = field(default_factory=list)
    entries_panel_error_message: str | None = None
    sessions_by_entry_ref: dict[EntryRef, list[ViewerSessionItem]] = field(default_factory=dict)
    sessions_error_by_entry_ref: dict[EntryRef, str | None] = field(default_factory=dict)
    viewer_entry_snapshot: EntrySummary | None = None
    viewer_sessions: list[ViewerSessionItem] = field(default_factory=list)
    viewer_sessions_error_message: str | None = None
    session_write_error_message: str | None = None
    session_write_pending: bool = False
    session_write_error_by_entry_ref: dict[EntryRef, str | None] = field(default_factory=dict)
    session_write_pending_by_entry_ref: dict[EntryRef, bool] = field(default_factory=dict)
    week_write_error_message: str | None = None
    week_write_pending: bool = False
    entry_write_error_message: str | None = None
    entry_write_pending: bool = False
    resource_write_error_message: str | None = None
    resource_write_pending: bool = False
    resource_draft_entry_ref: EntryRef | None = None
    resource_draft_values: dict[str, int] = field(default_factory=dict)
    resource_draft_dirty: bool = False
    resource_draft_by_entry_ref: dict[EntryRef, dict[str, int]] = field(default_factory=dict)
    resource_draft_dirty_by_entry_ref: dict[EntryRef, bool] = field(default_factory=dict)
    resource_write_error_by_entry_ref: dict[EntryRef, str | None] = field(default_factory=dict)
    resource_write_pending_by_entry_ref: dict[EntryRef, bool] = field(default_factory=dict)


@dataclass
class ConfirmationState:
    key: str | None = None
    title: str = ""
    body: str = ""
    confirm_label: str = "Confirmar"
    payload: Any = None


@dataclass
class EntryFormState:
    mode: Literal["create", "edit"]
    entry_type: str
    scenario_ref_text: str
    error_message: str | None = None


@dataclass
class EntryNotesEditorState:
    entry_ref: EntryRef
    entry_label: str
    notes_value: str
    error_message: str | None = None


@dataclass
class SessionFormState:
    mode: Literal["create", "edit"]
    entry_ref: EntryRef
    session_id: str | None
    started_date_local: str
    started_time_local: str
    ended_date_local: str
    ended_time_local: str
    active_without_end: bool
    error_message: str | None = None


@dataclass
class WeekNotesEditorState:
    notes_value: str
    error_message: str | None = None
