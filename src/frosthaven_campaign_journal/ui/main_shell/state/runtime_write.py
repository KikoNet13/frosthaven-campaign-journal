from __future__ import annotations

from typing import Any, Callable

from frosthaven_campaign_journal.data import (
    CampaignWriteResult,
    EntryWriteResult,
    FirestoreConfigError,
    FirestoreConflictError,
    FirestoreReadError,
    FirestoreTransitionInvalidError,
    FirestoreValidationError,
    FirestoreWriteError,
    ResourceBulkWriteResult,
    WeekWriteResult,
    close_week,
    delete_entry,
    manual_delete_session,
    reclose_week,
    reopen_week,
)
from frosthaven_campaign_journal.models import EntryRef, entry_ref_matches_selected_week


class MainShellRuntimeWriteMixin:
    def _run_campaign_write(
        self,
        action: Callable[[Any], CampaignWriteResult],
    ) -> CampaignWriteResult | None:
        self.read_state.campaign_write_pending = True
        self.read_state.warning_message = None
        self.notify()
        try:
            client = self._build_client()
            return action(client)
        except (
            FirestoreConfigError,
            FirestoreReadError,
            FirestoreConflictError,
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreWriteError,
        ) as exc:
            self._handle_write_exception(domain="campaign", exc=exc)
            return None
        finally:
            self.read_state.campaign_write_pending = False

    def _run_week_write(
        self,
        action: Callable[[Any], WeekWriteResult],
        *,
        success_message: str,
    ) -> WeekWriteResult | None:
        self.entry_panel_state.week_write_pending = True
        self.entry_panel_state.week_write_error_message = None
        self.notify()
        try:
            client = self._build_client()
            result = action(client)
            self._refresh_and_reload(
                selected_year_override=self.local_state.selected_year,
                reload_q5=(self.local_state.selected_week is not None),
                reload_q8=False,
            )
            if result.auto_stopped_session_id:
                self._emit_info_toast(
                    f"Semana actualizada. Se auto-cerró la sesión {result.auto_stopped_session_id}."
                )
            else:
                self._emit_info_toast(success_message)
            return result
        except (
            FirestoreConfigError,
            FirestoreReadError,
            FirestoreConflictError,
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreWriteError,
        ) as exc:
            self._handle_write_exception(domain="week", exc=exc)
            return None
        finally:
            self.entry_panel_state.week_write_pending = False

    def _run_session_write(
        self,
        action: Callable[[Any, EntryRef], Any],
        *,
        success_message: str,
        entry_ref: EntryRef | None = None,
    ) -> bool:
        effective_ref = entry_ref or self.local_state.viewer_entry_ref
        if effective_ref is None:
            self._set_session_error("No hay entrada disponible para gestionar sesiones.")
            return False

        self.entry_panel_state.session_write_pending = True
        self.entry_panel_state.session_write_error_message = None
        self.entry_panel_state.session_write_pending_by_entry_ref[effective_ref] = True
        self.entry_panel_state.session_write_error_by_entry_ref[effective_ref] = None
        self.notify()
        try:
            client = self._build_client()
            action(client, effective_ref)
            self._refresh_and_reload(
                selected_year_override=self.local_state.selected_year,
                reload_q5=(self.local_state.selected_week is not None),
                reload_q8=False,
            )
            self._emit_info_toast(success_message)
            return True
        except (
            FirestoreConfigError,
            FirestoreReadError,
            FirestoreConflictError,
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreWriteError,
        ) as exc:
            self._set_session_error(str(exc), entry_ref=effective_ref)
            self._handle_write_exception(domain="session", exc=exc)
            return False
        finally:
            self.entry_panel_state.session_write_pending = False
            self.entry_panel_state.session_write_pending_by_entry_ref[effective_ref] = False

    def _run_entry_write(
        self,
        action: Callable[[Any], EntryWriteResult],
        *,
        reload_q5: bool,
        reload_q8: bool,
        before_refresh: Callable[[EntryWriteResult], None] | None = None,
        success_message: str,
    ) -> EntryWriteResult | None:
        self.entry_panel_state.entry_write_pending = True
        self.entry_panel_state.entry_write_error_message = None
        self.notify()
        try:
            client = self._build_client()
            result = action(client)
            if before_refresh is not None:
                before_refresh(result)
            self._refresh_and_reload(
                selected_year_override=self.local_state.selected_year,
                reload_q5=reload_q5,
                reload_q8=reload_q8,
            )
            if result.auto_stopped_session_id:
                self._emit_info_toast(
                    f"Entrada actualizada. Se auto-cerró la sesión {result.auto_stopped_session_id}."
                )
            else:
                self._emit_info_toast(success_message)
            return result
        except (
            FirestoreConfigError,
            FirestoreReadError,
            FirestoreConflictError,
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreWriteError,
        ) as exc:
            self._handle_write_exception(domain="entry", exc=exc)
            return None
        finally:
            self.entry_panel_state.entry_write_pending = False

    def _run_resource_write(
        self,
        action: Callable[[Any], ResourceBulkWriteResult],
        *,
        success_message: str,
        entry_ref: EntryRef | None = None,
    ) -> ResourceBulkWriteResult | None:
        effective_ref = entry_ref or self.local_state.viewer_entry_ref
        self.entry_panel_state.resource_write_pending = True
        self.entry_panel_state.resource_write_error_message = None
        if effective_ref is not None:
            self.entry_panel_state.resource_write_pending_by_entry_ref[effective_ref] = True
            self.entry_panel_state.resource_write_error_by_entry_ref[effective_ref] = None
        self.notify()
        try:
            client = self._build_client()
            result = action(client)
            self._refresh_and_reload(
                selected_year_override=self.local_state.selected_year,
                reload_q5=(self.local_state.selected_week is not None),
                reload_q8=False,
            )
            self._emit_info_toast(success_message)
            return result
        except (
            FirestoreConfigError,
            FirestoreReadError,
            FirestoreConflictError,
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreWriteError,
        ) as exc:
            self._set_resource_error(str(exc), entry_ref=effective_ref)
            self._handle_write_exception(domain="resource", exc=exc)
            return None
        finally:
            self.entry_panel_state.resource_write_pending = False
            if effective_ref is not None:
                self.entry_panel_state.resource_write_pending_by_entry_ref[effective_ref] = False

    def _confirm_week_transition(
        self,
        *,
        transition_key: str,
        year_number: int,
        week_number: int,
    ) -> None:
        if transition_key == "week_close":
            self._run_week_write(
                lambda client: close_week(client, year_number=year_number, week_number=week_number),
                success_message="Semana cerrada.",
            )
        elif transition_key == "week_reopen":
            self._run_week_write(
                lambda client: reopen_week(client, year_number=year_number, week_number=week_number),
                success_message="Semana reabierta.",
            )
        elif transition_key == "week_reclose":
            self._run_week_write(
                lambda client: reclose_week(client, year_number=year_number, week_number=week_number),
                success_message="Semana recerrada.",
            )

    def _confirm_delete_entry(self, entry_ref: EntryRef) -> None:
        reload_q5 = entry_ref_matches_selected_week(self.local_state, entry_ref)

        def _clear_after_delete(_result: EntryWriteResult) -> None:
            self._clear_form_modal_states()
            self.entry_panel_state.viewer_entry_snapshot = None
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = None
            self.entry_panel_state.sessions_by_entry_ref.pop(entry_ref, None)
            self.entry_panel_state.sessions_error_by_entry_ref.pop(entry_ref, None)
            self._clear_resource_draft_for_entry(entry_ref)
            if self.local_state.viewer_entry_ref == entry_ref:
                self.local_state.viewer_entry_ref = None

        self._run_entry_write(
            lambda client: delete_entry(client, entry_ref=entry_ref),
            reload_q5=reload_q5,
            reload_q8=False,
            before_refresh=_clear_after_delete,
            success_message="Entrada borrada.",
        )

    def _confirm_delete_session(self, session_id: str) -> None:
        self._run_session_write(
            lambda client, entry_ref: manual_delete_session(
                client,
                entry_ref=entry_ref,
                session_id=session_id,
            ),
            success_message="Sesión borrada.",
        )
