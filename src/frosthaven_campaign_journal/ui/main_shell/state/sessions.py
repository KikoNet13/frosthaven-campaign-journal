from __future__ import annotations

from datetime import datetime, timezone

import flet as ft

from frosthaven_campaign_journal.data import (
    EntryWriteResult,
    create_entry,
    extend_years_plus_one,
    manual_create_session,
    manual_update_session,
    reorder_entry_within_week,
    replace_entry_resource_deltas,
    start_session,
    stop_session,
    update_entry,
    update_week_notes,
)
from frosthaven_campaign_journal.models import ENTRY_RESOURCE_KEYS, EntryRef, entry_ref_matches_selected_week
from frosthaven_campaign_journal.ui.main_shell.state.types import (
    EntryFormState,
    SessionFormState,
    WeekNotesEditorState,
)
from frosthaven_campaign_journal.ui.main_shell.state.utils import (
    find_viewer_session_item,
    parse_entry_form_values,
    parse_local_datetime,
    parse_optional_local_datetime,
    to_local_strings,
)

class MainShellSessionActionsMixin:
    def on_begin_session(self, _event: ft.ControlEvent | None = None) -> None:
        self.on_start_session(_event)

    def on_end_session(self, _event: ft.ControlEvent | None = None) -> None:
        self.on_stop_session(_event)

    def on_start_session(self, _event: ft.ControlEvent | None = None) -> None:
        self._run_session_write(
            lambda client, entry_ref: start_session(client, entry_ref=entry_ref),
            success_message="Sesión iniciada.",
        )

    def on_stop_session(self, _event: ft.ControlEvent | None = None) -> None:
        self._run_session_write(
            lambda client, entry_ref: stop_session(client, entry_ref=entry_ref),
            success_message="Sesión detenida.",
        )

    def on_open_manual_create_session(self, _event: ft.ControlEvent | None = None) -> None:
        if self.local_state.viewer_entry_ref is None:
            self._set_session_error("No hay entrada en el visor para crear sesión.")
            self.notify()
            return
        now_date, now_time = to_local_strings(datetime.now(timezone.utc))
        self.session_form_state = SessionFormState(
            mode="create",
            session_id=None,
            started_date_local=now_date,
            started_time_local=now_time,
            ended_date_local="",
            ended_time_local="",
            active_without_end=False,
            error_message=None,
        )
        self.notify()

    def on_open_manual_edit_session(self, session_id: str) -> None:
        session = find_viewer_session_item(self.entry_panel_state.viewer_sessions, session_id)
        if session is None:
            self._set_session_error("La sesión seleccionada ya no está visible en el visor.")
            self.notify()
            return

        started_date, started_time = to_local_strings(session.started_at_utc)
        ended_date, ended_time = to_local_strings(session.ended_at_utc)
        is_active = session.ended_at_utc is None
        self.session_form_state = SessionFormState(
            mode="edit",
            session_id=session.session_id,
            started_date_local=started_date,
            started_time_local=started_time,
            ended_date_local="" if is_active else ended_date,
            ended_time_local="" if is_active else ended_time,
            active_without_end=is_active,
            error_message=None,
        )
        self.notify()

    def on_open_manual_edit_session_click(self, event: ft.ControlEvent) -> None:
        session_id = event.control.data
        if isinstance(session_id, str):
            self.on_open_manual_edit_session(session_id)

    def on_open_manual_delete_session(self, session_id: str) -> None:
        session = find_viewer_session_item(self.entry_panel_state.viewer_sessions, session_id)
        if session is None:
            self._set_session_error("La sesión seleccionada ya no está visible en el visor.")
            self.notify()
            return
        self._set_confirmation(
            key="session_delete",
            title="Borrar sesión",
            body=f"¿Seguro que quieres borrar la sesión '{session_id}'? Esta acción es irreversible.",
            confirm_label="Borrar",
            payload=session_id,
        )
        self.notify()

    def on_open_manual_delete_session_click(self, event: ft.ControlEvent) -> None:
        session_id = event.control.data
        if isinstance(session_id, str):
            self.on_open_manual_delete_session(session_id)

    def on_session_form_set_started_date(self, event: ft.ControlEvent) -> None:
        if self.session_form_state is None:
            return
        self.session_form_state.started_date_local = event.control.value or ""
        self.session_form_state.error_message = None
        self.notify()

    def on_session_form_set_started_time(self, event: ft.ControlEvent) -> None:
        if self.session_form_state is None:
            return
        self.session_form_state.started_time_local = event.control.value or ""
        self.session_form_state.error_message = None
        self.notify()

    def on_session_form_set_ended_date(self, event: ft.ControlEvent) -> None:
        if self.session_form_state is None:
            return
        self.session_form_state.ended_date_local = event.control.value or ""
        self.session_form_state.error_message = None
        self.notify()

    def on_session_form_set_ended_time(self, event: ft.ControlEvent) -> None:
        if self.session_form_state is None:
            return
        self.session_form_state.ended_time_local = event.control.value or ""
        self.session_form_state.error_message = None
        self.notify()

    def on_session_form_toggle_active(self, event: ft.ControlEvent) -> None:
        if self.session_form_state is None:
            return
        self.session_form_state.active_without_end = bool(event.control.value)
        self.session_form_state.error_message = None
        self.notify()

    def on_cancel_session_form(self, _event: ft.ControlEvent | None = None) -> None:
        self.session_form_state = None
        self.notify()

    def on_submit_session_form(self, _event: ft.ControlEvent | None = None) -> None:
        form = self.session_form_state
        if form is None:
            return
        try:
            started_at_utc = parse_local_datetime(
                form.started_date_local,
                form.started_time_local,
                field_label="Inicio",
            )
            if form.active_without_end:
                ended_at_utc = None
            else:
                ended_at_utc = parse_optional_local_datetime(
                    form.ended_date_local,
                    form.ended_time_local,
                    field_label="Fin",
                )
                if ended_at_utc is None:
                    raise ValueError("Fin: rellena fecha y hora o marca 'Sesión activa'.")
        except ValueError as exc:
            form.error_message = str(exc)
            self.notify()
            return

        if form.mode == "create":
            ok = self._run_session_write(
                lambda client, entry_ref: manual_create_session(
                    client,
                    entry_ref=entry_ref,
                    started_at_utc=started_at_utc,
                    ended_at_utc=ended_at_utc,
                ),
                success_message="Sesión creada.",
            )
        else:
            if not form.session_id:
                form.error_message = "La sesión objetivo no es válida."
                self.notify()
                return
            ok = self._run_session_write(
                lambda client, entry_ref: manual_update_session(
                    client,
                    entry_ref=entry_ref,
                    session_id=form.session_id,
                    started_at_utc=started_at_utc,
                    ended_at_utc=ended_at_utc,
                ),
                success_message="Sesión actualizada.",
            )
        if ok:
            self.session_form_state = None
        self.notify()

    # Week
