from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from frosthaven_campaign_journal.models import (
    EntryRef,
    EntrySummary,
    MainScreenLocalState,
    ViewerSessionItem,
    WeekSummary,
)


@dataclass(frozen=True)
class WeekEntryCardViewData:
    entry: EntrySummary
    resource_draft_values: dict[str, int]
    resource_draft_dirty: bool
    resource_write_error_message: str | None
    resource_write_pending: bool
    sessions: list[ViewerSessionItem]
    sessions_total_text: str
    sessions_error_message: str | None
    session_write_pending: bool
    entry_write_pending: bool
    is_active_session_owner: bool


@dataclass(frozen=True)
class MainShellViewData:
    state: MainScreenLocalState
    years: list[int]
    weeks_for_selected_year: list[WeekSummary]
    entries_for_selected_week: list[EntrySummary]
    week_entry_cards: list[WeekEntryCardViewData]
    viewer_entry: EntrySummary | None
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
    active_session_started_at_utc: object | None
    active_status_error_message: str | None
    campaign_resource_totals: dict[str, int] | None
    read_status: str
    read_error_message: str | None
    read_warning_message: str | None
    env_name: str
    confirmation_dialog: "ConfirmationDialogViewState | None"
    entry_form: "EntryFormViewState | None"
    entry_notes_editor: "EntryNotesEditorViewState | None"
    session_form: "SessionFormViewState | None"


@dataclass(frozen=True)
class ConfirmationDialogViewState:
    key: str
    title: str
    body: str
    confirm_label: str


@dataclass(frozen=True)
class EntryFormViewState:
    mode: Literal["create", "edit"]
    entry_type: str
    scenario_ref_text: str
    error_message: str | None


@dataclass(frozen=True)
class EntryNotesEditorViewState:
    entry_ref: EntryRef
    entry_label: str
    notes_value: str
    error_message: str | None


@dataclass(frozen=True)
class SessionFormViewState:
    mode: Literal["create", "edit"]
    entry_ref: EntryRef
    session_id: str | None
    started_date_local: str
    started_time_local: str
    ended_date_local: str
    ended_time_local: str
    active_without_end: bool
    error_message: str | None
