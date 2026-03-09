from __future__ import annotations

from datetime import datetime, timedelta, timezone

from frosthaven_campaign_journal.models import EntryRef, EntrySummary, ViewerSessionItem
from frosthaven_campaign_journal.ui.main_shell.model import (
    ConfirmationDialogViewState,
    EntryFormViewState,
    EntryNotesEditorViewState,
    MainShellViewData,
    SessionFormViewState,
    WeekEntryCardViewData,
)


class MainShellViewDataMixin:
    def build_view_data(self) -> MainShellViewData:
        confirmation_view: ConfirmationDialogViewState | None = None
        if self.confirmation_state.key is not None:
            confirmation_view = ConfirmationDialogViewState(
                key=self.confirmation_state.key,
                title=self.confirmation_state.title,
                body=self.confirmation_state.body,
                confirm_label=self.confirmation_state.confirm_label,
            )
        entry_form_view: EntryFormViewState | None = None
        if self.entry_form_state is not None:
            entry_form_view = EntryFormViewState(
                mode=self.entry_form_state.mode,
                entry_type=self.entry_form_state.entry_type,
                scenario_ref_text=self.entry_form_state.scenario_ref_text,
                error_message=self.entry_form_state.error_message,
            )
        entry_notes_view: EntryNotesEditorViewState | None = None
        if self.entry_notes_editor_state is not None:
            entry_notes_view = EntryNotesEditorViewState(
                entry_ref=self.entry_notes_editor_state.entry_ref,
                entry_label=self.entry_notes_editor_state.entry_label,
                notes_value=self.entry_notes_editor_state.notes_value,
                error_message=self.entry_notes_editor_state.error_message,
            )
        session_form_view: SessionFormViewState | None = None
        if self.session_form_state is not None:
            session_form_view = SessionFormViewState(
                mode=self.session_form_state.mode,
                entry_ref=self.session_form_state.entry_ref,
                session_id=self.session_form_state.session_id,
                started_date_local=self.session_form_state.started_date_local,
                started_time_local=self.session_form_state.started_time_local,
                ended_date_local=self.session_form_state.ended_date_local,
                ended_time_local=self.session_form_state.ended_time_local,
                active_without_end=self.session_form_state.active_without_end,
                error_message=self.session_form_state.error_message,
            )
        week_entry_cards = [
            _build_week_entry_card_view_data(
                entry=entry,
                sessions=self.entry_panel_state.sessions_by_entry_ref.get(entry.ref, []),
                sessions_error=self.entry_panel_state.sessions_error_by_entry_ref.get(entry.ref),
                resource_draft=self.entry_panel_state.resource_draft_by_entry_ref.get(
                    entry.ref,
                    self._normalize_resource_draft_values(entry.resource_deltas),
                ),
                resource_draft_dirty=self.entry_panel_state.resource_draft_dirty_by_entry_ref.get(entry.ref, False),
                resource_write_error=self.entry_panel_state.resource_write_error_by_entry_ref.get(entry.ref),
                resource_write_pending=self.entry_panel_state.resource_write_pending_by_entry_ref.get(entry.ref, False),
                session_write_pending=self.entry_panel_state.session_write_pending_by_entry_ref.get(entry.ref, False),
                active_entry_ref=self.read_state.active_entry_ref,
                entry_write_pending=self.entry_panel_state.entry_write_pending,
            )
            for entry in self.entry_panel_state.entries_for_selected_week
        ]

        return MainShellViewData(
            state=self.local_state,
            years=self.read_state.years,
            weeks_for_selected_year=self._weeks_for_selected_year(),
            entries_for_selected_week=self.entry_panel_state.entries_for_selected_week,
            week_entry_cards=week_entry_cards,
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
            resource_draft_dirty=self.entry_panel_state.resource_draft_dirty and self._resource_draft_attached_to_viewer(),
            resource_draft_attached_to_viewer=self._resource_draft_attached_to_viewer(),
            active_entry_ref=self.read_state.active_entry_ref,
            active_entry_label=self.read_state.active_entry_label,
            active_session_started_at_utc=self.read_state.active_session_started_at_utc,
            active_status_error_message=self.read_state.active_status_error_message,
            campaign_resource_totals=self.read_state.campaign_resource_totals,
            read_status=self.read_state.status,
            read_error_message=self.read_state.error_message,
            read_warning_message=self.read_state.warning_message,
            env_name=self.env_name,
            confirmation_dialog=confirmation_view,
            entry_form=entry_form_view,
            entry_notes_editor=entry_notes_view,
            session_form=session_form_view,
        )


def _build_week_entry_card_view_data(
    *,
    entry: EntrySummary,
    sessions: list[ViewerSessionItem],
    sessions_error: str | None,
    resource_draft: dict[str, int],
    resource_draft_dirty: bool,
    resource_write_error: str | None,
    resource_write_pending: bool,
    session_write_pending: bool,
    active_entry_ref: EntryRef | None,
    entry_write_pending: bool,
) -> WeekEntryCardViewData:
    return WeekEntryCardViewData(
        entry=entry,
        resource_draft_values=dict(resource_draft),
        resource_draft_dirty=resource_draft_dirty,
        resource_write_error_message=resource_write_error,
        resource_write_pending=resource_write_pending,
        sessions=list(sessions),
        sessions_total_text=_format_sessions_total_text(sessions),
        sessions_error_message=sessions_error,
        session_write_pending=session_write_pending,
        entry_write_pending=entry_write_pending,
        is_active_session_owner=(active_entry_ref == entry.ref),
    )


def _format_sessions_total_text(sessions: list[ViewerSessionItem]) -> str:
    total = timedelta()
    has_finished = False
    for session in sessions:
        started = _as_datetime(session.started_at_utc)
        ended = _as_datetime(session.ended_at_utc)
        if started is None or ended is None or ended < started:
            continue
        total += ended - started
        has_finished = True
    if not has_finished:
        return "0 min"
    total_seconds = int(total.total_seconds())
    if total_seconds < 0:
        total_seconds = 0
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{hours}h {minutes:02d}m" if hours else f"{minutes} min"


def _as_datetime(value: object | None) -> datetime | None:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    return None
