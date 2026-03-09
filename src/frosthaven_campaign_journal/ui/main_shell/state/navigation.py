from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.data import extend_years_plus_one, manual_delete_session
from frosthaven_campaign_journal.models import EntryRef


class MainShellNavigationMixin:
    def initialize(self) -> None:
        self._refresh_and_reload(
            selected_year_override=self.local_state.selected_year,
            reload_q5=False,
            reload_q8=False,
        )
        self.notify()

    # Navigation

    def on_prev_year(self, _event: ft.ControlEvent | None = None) -> None:
        if self.local_state.selected_year is None or self.local_state.selected_year not in self.read_state.years:
            return
        current_index = self.read_state.years.index(self.local_state.selected_year)
        if current_index <= 0:
            return
        target_year = self.read_state.years[current_index - 1]

        def _action() -> None:
            self.local_state.selected_year = target_year
            self.local_state.selected_week = None
            self.local_state.viewer_entry_ref = None
            self._clear_write_errors()
            self.entry_panel_state.entries_for_selected_week = []
            self.entry_panel_state.entries_panel_error_message = None
            self.entry_panel_state.viewer_entry_snapshot = None
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = None
            self.entry_panel_state.sessions_by_entry_ref = {}
            self.entry_panel_state.sessions_error_by_entry_ref = {}
            self._clear_form_modal_states()
            self._clear_resource_draft_state()
            self._refresh_and_reload(
                selected_year_override=self.local_state.selected_year,
                reload_q5=False,
                reload_q8=False,
            )

        self._run_or_confirm_resource_draft_before_context_change(_action, action_label="cambiar de año")

    def on_next_year(self, _event: ft.ControlEvent | None = None) -> None:
        if self.local_state.selected_year is None or self.local_state.selected_year not in self.read_state.years:
            return
        current_index = self.read_state.years.index(self.local_state.selected_year)
        if current_index >= len(self.read_state.years) - 1:
            return
        target_year = self.read_state.years[current_index + 1]

        def _action() -> None:
            self.local_state.selected_year = target_year
            self.local_state.selected_week = None
            self.local_state.viewer_entry_ref = None
            self._clear_write_errors()
            self.entry_panel_state.entries_for_selected_week = []
            self.entry_panel_state.entries_panel_error_message = None
            self.entry_panel_state.viewer_entry_snapshot = None
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = None
            self.entry_panel_state.sessions_by_entry_ref = {}
            self.entry_panel_state.sessions_error_by_entry_ref = {}
            self._clear_form_modal_states()
            self._clear_resource_draft_state()
            self._refresh_and_reload(
                selected_year_override=self.local_state.selected_year,
                reload_q5=False,
                reload_q8=False,
            )

        self._run_or_confirm_resource_draft_before_context_change(_action, action_label="cambiar de año")

    def on_select_week_click(self, event: ft.ControlEvent) -> None:
        week_number = event.control.data
        if isinstance(week_number, int) and not isinstance(week_number, bool):
            self.on_select_week(week_number)
            return
        if isinstance(week_number, str) and week_number.isdigit():
            self.on_select_week(int(week_number))

    def on_select_week(self, week_number: int) -> None:
        if self.local_state.selected_year is None:
            return
        if not any(week.week_number == week_number for week in self._weeks_for_selected_year()):
            return

        def _action() -> None:
            self.local_state.selected_week = week_number
            self.local_state.viewer_entry_ref = None
            self._clear_write_errors()
            self.entry_panel_state.viewer_entry_snapshot = None
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = None
            self._clear_form_modal_states()
            self._clear_resource_draft_state()
            self._load_entries_for_selected_week()

        self._run_or_confirm_resource_draft_before_context_change(_action, action_label="cambiar de semana")

    def on_select_entry_click(self, event: ft.ControlEvent) -> None:
        entry_ref = event.control.data
        if isinstance(entry_ref, EntryRef):
            self.on_select_entry(entry_ref)

    def on_select_entry(self, entry_ref: EntryRef) -> None:
        def _action() -> None:
            self.local_state.viewer_entry_ref = entry_ref
            self._clear_write_errors()
            self._clear_form_modal_states()
            self._load_viewer_entry_and_sessions()

        self._run_or_confirm_resource_draft_before_context_change(_action, action_label="cambiar de entrada")

    def on_manual_refresh(self, _event: ft.ControlEvent | None = None) -> None:
        def _action() -> None:
            self._clear_write_errors()
            self._refresh_and_reload(
                selected_year_override=self.local_state.selected_year,
                reload_q5=(self.local_state.selected_week is not None),
                reload_q8=False,
            )

        self._run_or_confirm_resource_draft_before_context_change(_action, action_label="refrescar")

    # Confirmations

    def on_open_extend_year_plus_one_confirm(self, _event: ft.ControlEvent | None = None) -> None:
        if not self.read_state.years:
            self._set_campaign_error("No hay años visibles para extender +1.")
            self.notify()
            return
        target_year = max(self.read_state.years) + 1
        self._set_confirmation(
            key="extend_year_plus_one",
            title="Extender campaña +1 año",
            body=f"Se creará el año {target_year} con 20 semanas abiertas. ¿Quieres continuar?",
            confirm_label="Crear año",
            payload=target_year,
        )
        self.notify()

    def on_confirm_pending_action(self, _event: ft.ControlEvent | None = None) -> None:
        key = self.confirmation_state.key
        payload = self.confirmation_state.payload
        if key is None:
            return

        self._clear_confirmation()

        if key == "discard_resource_draft_context_change":
            self._discard_resource_draft_for_context_change(show_notice=True)
            pending = self._take_pending_context_action()
            if pending is not None:
                pending()
            self.notify()
            return

        if key == "extend_year_plus_one":
            result = self._run_campaign_write(lambda client: extend_years_plus_one(client))
            if result is not None:
                self.local_state.selected_year = result.new_year_number
                self.local_state.selected_week = None
                self.local_state.viewer_entry_ref = None
                self.entry_panel_state.viewer_entry_snapshot = None
                self.entry_panel_state.viewer_sessions = []
                self.entry_panel_state.viewer_sessions_error_message = None
                self.entry_panel_state.sessions_by_entry_ref = {}
                self.entry_panel_state.sessions_error_by_entry_ref = {}
                self._clear_form_modal_states()
                self._clear_resource_draft_state()
                self._refresh_and_reload(
                    selected_year_override=result.new_year_number,
                    reload_q5=False,
                    reload_q8=False,
                )
                self._emit_info_toast(
                    f"Año {result.new_year_number} creado "
                    f"(semanas {result.created_week_start}-{result.created_week_end})."
                )
            self.notify()
            return

        if key in {"week_close", "week_reopen", "week_reclose"}:
            if isinstance(payload, tuple) and len(payload) == 2:
                year_number, week_number = payload
                if isinstance(year_number, int) and isinstance(week_number, int):
                    self._confirm_week_transition(transition_key=key, year_number=year_number, week_number=week_number)
            self.notify()
            return

        if key == "entry_delete" and isinstance(payload, EntryRef):
            self._confirm_delete_entry(payload)
            self.notify()
            return

        if key == "session_delete":
            if (
                isinstance(payload, tuple)
                and len(payload) == 2
                and isinstance(payload[0], EntryRef)
                and isinstance(payload[1], str)
            ):
                self._run_session_write(
                    lambda client, entry_ref: manual_delete_session(
                        client,
                        entry_ref=entry_ref,
                        session_id=payload[1],
                    ),
                    success_message="Sesión borrada.",
                    entry_ref=payload[0],
                )
            elif isinstance(payload, str):
                self._confirm_delete_session(payload)
            self.notify()
            return

        self.notify()

    def on_cancel_pending_action(self, _event: ft.ControlEvent | None = None) -> None:
        self._clear_confirmation()
        self._clear_pending_context_action()
        self.notify()
