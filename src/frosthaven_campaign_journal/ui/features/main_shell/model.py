from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from frosthaven_campaign_journal.state.models import (
    EntryRef,
    EntrySummary,
    MainScreenLocalState,
    ViewerSessionItem,
    WeekSummary,
)


@dataclass(frozen=True)
class MainShellViewData:
    state: MainScreenLocalState
    years: list[int]
    weeks_for_selected_year: list[WeekSummary]
    entries_for_selected_week: list[EntrySummary]
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
    active_status_error_message: str | None
    campaign_resource_totals: dict[str, int] | None
    read_status: str
    read_error_message: str | None
    read_warning_message: str | None
    env_name: str
    info_message: str | None
    confirmation: "ConfirmationViewState | None"
    entry_form: "EntryFormViewState | None"
    session_form: "SessionFormViewState | None"
    week_notes_editor: "WeekNotesEditorViewState | None"


@dataclass(frozen=True)
class ConfirmationViewState:
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
class SessionFormViewState:
    mode: Literal["create", "edit"]
    session_id: str | None
    started_date_local: str
    started_time_local: str
    ended_date_local: str
    ended_time_local: str
    active_without_end: bool
    error_message: str | None


@dataclass(frozen=True)
class WeekNotesEditorViewState:
    notes_value: str
    error_message: str | None
