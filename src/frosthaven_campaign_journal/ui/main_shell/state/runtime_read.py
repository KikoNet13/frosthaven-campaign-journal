from __future__ import annotations

from typing import Any, Callable

from frosthaven_campaign_journal.config import load_settings
from frosthaven_campaign_journal.data import (
    FirestoreConfigError,
    FirestoreReadError,
    build_firestore_client,
    load_main_screen_snapshot,
    read_entry_by_ref,
    read_q5_entries_for_selected_week,
    read_q8_sessions_for_entry,
)
from frosthaven_campaign_journal.models import EntryRef, WeekSummary, entry_ref_matches_selected_week
from frosthaven_campaign_journal.ui.main_shell.state.types import ConfirmationState
from frosthaven_campaign_journal.ui.main_shell.state.utils import (
    find_entry_in_list,
    map_entry_read_to_summary,
    map_session_read_to_viewer_session,
    map_week_read_to_summary,
)


class MainShellRuntimeReadMixin:
    def _build_client(self):
        settings = load_settings()
        return build_firestore_client(settings)

    def _refresh_and_reload(
        self,
        *,
        selected_year_override: int | None,
        reload_q5: bool,
        reload_q8: bool,
    ) -> None:
        self._load_readonly_snapshot(selected_year_override=selected_year_override)
        if reload_q5:
            self._load_entries_for_selected_week()
        elif reload_q8:
            self._load_viewer_entry_and_sessions()

    def _load_readonly_snapshot(self, *, selected_year_override: int | None) -> bool:
        try:
            client = self._build_client()
            snapshot = load_main_screen_snapshot(
                client,
                selected_year=selected_year_override,
                viewer_entry_ref=self.local_state.viewer_entry_ref,
            )
        except (FirestoreConfigError, FirestoreReadError) as exc:
            self.read_state.status = "error"
            self.read_state.error_message = str(exc)
            self.read_state.warning_message = None
            self.read_state.years = []
            self.read_state.weeks_by_year = {}
            return False

        self.read_state.status = "ready"
        self.read_state.error_message = None
        self.read_state.years = snapshot.years
        self.read_state.campaign_resource_totals = snapshot.campaign_main.resource_totals
        self.read_state.weeks_by_year[snapshot.effective_year] = [
            map_week_read_to_summary(week)
            for week in snapshot.weeks_for_selected_year
        ]

        self.local_state.selected_year = snapshot.effective_year
        visible_week_numbers = {
            week.week_number for week in self.read_state.weeks_by_year[snapshot.effective_year]
        }
        if self.local_state.selected_week is not None and self.local_state.selected_week not in visible_week_numbers:
            self.local_state.selected_week = None
            self.local_state.viewer_entry_ref = None
            self.entry_panel_state.viewer_entry_snapshot = None
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = None
            self.entry_panel_state.sessions_by_entry_ref = {}
            self.entry_panel_state.sessions_error_by_entry_ref = {}
            self.entry_notes_editor_state = None
            self._clear_resource_draft_state()

        if snapshot.active_entry is None:
            self.read_state.active_entry_ref = None
            self.read_state.active_entry_label = None
        else:
            self.read_state.active_entry_ref = snapshot.active_entry.entry_ref
            self.read_state.active_entry_label = snapshot.active_entry.label
        self.read_state.active_session_started_at_utc = (
            snapshot.active_session.started_at_utc if snapshot.active_session is not None else None
        )
        self.read_state.active_status_error_message = snapshot.active_status_error_message
        return True

    def _load_entries_for_selected_week(self) -> None:
        if self.local_state.selected_year is None or self.local_state.selected_week is None:
            self.entry_panel_state.entries_for_selected_week = []
            self.entry_panel_state.entries_panel_error_message = None
            self.entry_panel_state.sessions_by_entry_ref = {}
            self.entry_panel_state.sessions_error_by_entry_ref = {}
            return

        try:
            client = self._build_client()
            entries = read_q5_entries_for_selected_week(
                client,
                year_number=self.local_state.selected_year,
                week_number=self.local_state.selected_week,
            )
        except (FirestoreConfigError, FirestoreReadError) as exc:
            self.entry_panel_state.entries_for_selected_week = []
            self.entry_panel_state.entries_panel_error_message = str(exc)
            self.entry_panel_state.sessions_by_entry_ref = {}
            self.entry_panel_state.sessions_error_by_entry_ref = {}
            return

        mapped_entries = [map_entry_read_to_summary(entry) for entry in entries]
        self.entry_panel_state.entries_for_selected_week = mapped_entries
        self.entry_panel_state.entries_panel_error_message = None

        sessions_by_entry_ref: dict[EntryRef, list[Any]] = {}
        sessions_error_by_entry_ref: dict[EntryRef, str | None] = {}
        for entry in mapped_entries:
            try:
                entry_sessions = read_q8_sessions_for_entry(client, entry_ref=entry.ref)
            except FirestoreReadError as exc:
                sessions_by_entry_ref[entry.ref] = []
                sessions_error_by_entry_ref[entry.ref] = str(exc)
                continue
            sessions_by_entry_ref[entry.ref] = [
                map_session_read_to_viewer_session(session)
                for session in entry_sessions
            ]
            sessions_error_by_entry_ref[entry.ref] = None

        self.entry_panel_state.sessions_by_entry_ref = sessions_by_entry_ref
        self.entry_panel_state.sessions_error_by_entry_ref = sessions_error_by_entry_ref

        self._sync_resource_draft_from_entries()

        valid_refs = {entry.ref for entry in mapped_entries}
        for stale_ref in list(self.entry_panel_state.session_write_pending_by_entry_ref):
            if stale_ref not in valid_refs:
                self.entry_panel_state.session_write_pending_by_entry_ref.pop(stale_ref, None)
                self.entry_panel_state.session_write_error_by_entry_ref.pop(stale_ref, None)
        for stale_ref in list(self.entry_panel_state.resource_write_pending_by_entry_ref):
            if stale_ref not in valid_refs:
                self.entry_panel_state.resource_write_pending_by_entry_ref.pop(stale_ref, None)
                self.entry_panel_state.resource_write_error_by_entry_ref.pop(stale_ref, None)

        if self.local_state.viewer_entry_ref is None:
            self.entry_panel_state.viewer_entry_snapshot = None
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = None
            return

        if not entry_ref_matches_selected_week(self.local_state, self.local_state.viewer_entry_ref):
            self.entry_panel_state.viewer_entry_snapshot = None
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = None
            return

        updated_entry = find_entry_in_list(mapped_entries, self.local_state.viewer_entry_ref)
        if updated_entry is None:
            self.entry_panel_state.viewer_entry_snapshot = None
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = None
            return

        self.entry_panel_state.viewer_entry_snapshot = updated_entry
        self.entry_panel_state.viewer_sessions = list(
            self.entry_panel_state.sessions_by_entry_ref.get(updated_entry.ref, [])
        )
        self.entry_panel_state.viewer_sessions_error_message = (
            self.entry_panel_state.sessions_error_by_entry_ref.get(updated_entry.ref)
        )

    def _load_viewer_entry_and_sessions(self) -> None:
        if self.local_state.viewer_entry_ref is None:
            self.entry_panel_state.viewer_entry_snapshot = None
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = None
            return

        entry_ref = self.local_state.viewer_entry_ref
        try:
            client = self._build_client()
            viewer_entry_read = read_entry_by_ref(client, entry_ref)
            entry_summary = map_entry_read_to_summary(viewer_entry_read)
        except (FirestoreConfigError, FirestoreReadError) as exc:
            self.entry_panel_state.viewer_sessions_error_message = str(exc)
            self.entry_panel_state.viewer_sessions = []
            if (
                self.entry_panel_state.viewer_entry_snapshot is not None
                and self.entry_panel_state.viewer_entry_snapshot.ref != entry_ref
            ):
                self.entry_panel_state.viewer_entry_snapshot = None
            return

        self.entry_panel_state.viewer_entry_snapshot = entry_summary
        self._sync_resource_draft_from_entry_snapshot(entry_summary)

        try:
            sessions = read_q8_sessions_for_entry(client, entry_ref=entry_ref)
        except FirestoreReadError as exc:
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = str(exc)
            self.entry_panel_state.sessions_by_entry_ref[entry_ref] = []
            self.entry_panel_state.sessions_error_by_entry_ref[entry_ref] = str(exc)
            return

        viewer_sessions = [
            map_session_read_to_viewer_session(session)
            for session in sessions
        ]
        self.entry_panel_state.viewer_sessions = viewer_sessions
        self.entry_panel_state.viewer_sessions_error_message = None
        self.entry_panel_state.sessions_by_entry_ref[entry_ref] = viewer_sessions
        self.entry_panel_state.sessions_error_by_entry_ref[entry_ref] = None

    def _find_selected_week_for_write(self) -> WeekSummary | None:
        if self.local_state.selected_year is None or self.local_state.selected_week is None:
            return None
        for week in self._weeks_for_selected_year():
            if week.week_number == self.local_state.selected_week:
                return week
        return None

    def _get_selected_week_target_for_entry_create(self) -> tuple[int, int] | None:
        selected_week = self._find_selected_week_for_write()
        if selected_week is None:
            return None
        return selected_week.year_number, selected_week.week_number

    def _get_viewer_entry_ref_for_entry_write(self) -> EntryRef | None:
        return self.local_state.viewer_entry_ref

    def _get_viewer_entry_ref_for_resource_write(self) -> EntryRef | None:
        return self.local_state.viewer_entry_ref

    def _weeks_for_selected_year(self) -> list[WeekSummary]:
        if self.local_state.selected_year is None:
            return []
        return self.read_state.weeks_by_year.get(self.local_state.selected_year, [])

    def _set_confirmation(
        self,
        *,
        key: str,
        title: str,
        body: str,
        confirm_label: str,
        payload: Any,
    ) -> None:
        self.confirmation_state.key = key
        self.confirmation_state.title = title
        self.confirmation_state.body = body
        self.confirmation_state.confirm_label = confirm_label
        self.confirmation_state.payload = payload

    def _clear_confirmation(self) -> None:
        self.confirmation_state = ConfirmationState()

    def _queue_pending_context_action(self, action: Callable[[], None], *, action_label: str) -> None:
        self._pending_context_action = action
        self._pending_context_action_label = action_label

    def _take_pending_context_action(self) -> Callable[[], None] | None:
        action = self._pending_context_action
        self._pending_context_action = None
        self._pending_context_action_label = None
        return action

    def _clear_pending_context_action(self) -> None:
        self._pending_context_action = None
        self._pending_context_action_label = None

    def _run_or_confirm_resource_draft_before_context_change(
        self,
        action: Callable[[], None],
        *,
        action_label: str,
    ) -> None:
        if self._has_any_dirty_resource_draft():
            self._queue_pending_context_action(action, action_label=action_label)
            self._set_confirmation(
                key="discard_resource_draft_context_change",
                title="Cambios de recursos sin guardar",
                body=(
                    "Hay cambios de recursos sin guardar en la semana visible. "
                    f"Si continúas para {action_label}, se descartarán."
                ),
                confirm_label="Descartar y continuar",
                payload=action_label,
            )
            self.notify()
            return
        action()
        self.notify()
