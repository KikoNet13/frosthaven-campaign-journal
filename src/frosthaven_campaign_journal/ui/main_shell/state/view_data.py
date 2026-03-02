from __future__ import annotations

from frosthaven_campaign_journal.ui.main_shell.model import (
    ConfirmationViewState,
    EntryFormViewState,
    MainShellViewData,
    SessionFormViewState,
    WeekNotesEditorViewState,
)


class MainShellViewDataMixin:
    def build_view_data(self) -> MainShellViewData:
        confirmation_view: ConfirmationViewState | None = None
        if self.confirmation_state.key is not None:
            confirmation_view = ConfirmationViewState(
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
        session_form_view: SessionFormViewState | None = None
        if self.session_form_state is not None:
            session_form_view = SessionFormViewState(
                mode=self.session_form_state.mode,
                session_id=self.session_form_state.session_id,
                started_date_local=self.session_form_state.started_date_local,
                started_time_local=self.session_form_state.started_time_local,
                ended_date_local=self.session_form_state.ended_date_local,
                ended_time_local=self.session_form_state.ended_time_local,
                active_without_end=self.session_form_state.active_without_end,
                error_message=self.session_form_state.error_message,
            )
        week_notes_view: WeekNotesEditorViewState | None = None
        if self.week_notes_editor_state is not None:
            week_notes_view = WeekNotesEditorViewState(
                notes_value=self.week_notes_editor_state.notes_value,
                error_message=self.week_notes_editor_state.error_message,
            )

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
            resource_draft_dirty=self.entry_panel_state.resource_draft_dirty and self._resource_draft_attached_to_viewer(),
            resource_draft_attached_to_viewer=self._resource_draft_attached_to_viewer(),
            active_entry_ref=self.read_state.active_entry_ref,
            active_entry_label=self.read_state.active_entry_label,
            active_status_error_message=self.read_state.active_status_error_message,
            campaign_resource_totals=self.read_state.campaign_resource_totals,
            read_status=self.read_state.status,
            read_error_message=self.read_state.error_message,
            read_warning_message=self.read_state.warning_message,
            env_name=self.env_name,
            info_message=self.info_message,
            confirmation=confirmation_view,
            entry_form=entry_form_view,
            session_form=session_form_view,
            week_notes_editor=week_notes_view,
        )
