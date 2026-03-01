from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Literal

import flet as ft

from frosthaven_campaign_journal.config import load_settings
from frosthaven_campaign_journal.data import (
    CampaignWriteResult,
    EntryRead,
    EntrySessionRead,
    EntryWriteResult,
    FirestoreConfigError,
    FirestoreConflictError,
    FirestoreReadError,
    FirestoreTransitionInvalidError,
    FirestoreValidationError,
    FirestoreWriteError,
    ResourceBulkWriteResult,
    WeekRead,
    WeekWriteResult,
    build_firestore_client,
    close_week,
    create_entry,
    delete_entry,
    extend_years_plus_one,
    load_main_screen_snapshot,
    manual_create_session,
    manual_delete_session,
    manual_update_session,
    read_entry_by_ref,
    read_q5_entries_for_selected_week,
    read_q8_sessions_for_entry,
    reclose_week,
    reorder_entry_within_week,
    reopen_week,
    replace_entry_resource_deltas,
    start_session,
    stop_session,
    update_entry,
    update_week_notes,
)
from frosthaven_campaign_journal.state.models import (
    ENTRY_RESOURCE_KEYS,
    EntryRef,
    MainScreenLocalState,
    EntrySummary,
    WeekSummary,
    ViewerSessionItem,
    build_initial_main_screen_state,
    entry_ref_matches_selected_week,
)
from frosthaven_campaign_journal.ui.features.main_shell.model import (
    ConfirmationViewState,
    EntryFormViewState,
    MainShellViewData,
    SessionFormViewState,
    WeekNotesEditorViewState,
)


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
    active_status_error_message: str | None = None
    campaign_write_pending: bool = False


@dataclass
class EntryPanelReadState:
    entries_for_selected_week: list[EntrySummary] = field(default_factory=list)
    entries_panel_error_message: str | None = None
    viewer_entry_snapshot: EntrySummary | None = None
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
class SessionFormState:
    mode: Literal["create", "edit"]
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


@ft.observable
@dataclass
class MainShellState:
    local_state: MainScreenLocalState = field(default_factory=build_initial_main_screen_state)
    read_state: MainScreenReadState = field(default_factory=MainScreenReadState)
    entry_panel_state: EntryPanelReadState = field(default_factory=EntryPanelReadState)
    env_name: str = field(default_factory=lambda: load_settings().env)
    confirmation_state: ConfirmationState = field(default_factory=ConfirmationState)
    entry_form_state: EntryFormState | None = None
    session_form_state: SessionFormState | None = None
    week_notes_editor_state: WeekNotesEditorState | None = None
    info_message: str | None = None
    _pending_context_action: Callable[[], None] | None = field(default=None, init=False, repr=False)
    _pending_context_action_label: str | None = field(default=None, init=False, repr=False)

    @classmethod
    def create(cls) -> MainShellState:
        state = cls()
        state.initialize()
        return state

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
            self._clear_write_errors()
            self.entry_panel_state.entries_for_selected_week = []
            self.entry_panel_state.entries_panel_error_message = None
            self._refresh_and_reload(
                selected_year_override=self.local_state.selected_year,
                reload_q5=False,
                reload_q8=False,
            )

        self._run_or_confirm_resource_draft_before_context_change(_action, action_label="cambiar de aÃ±o")

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
            self._clear_write_errors()
            self.entry_panel_state.entries_for_selected_week = []
            self.entry_panel_state.entries_panel_error_message = None
            self._refresh_and_reload(
                selected_year_override=self.local_state.selected_year,
                reload_q5=False,
                reload_q8=False,
            )

        self._run_or_confirm_resource_draft_before_context_change(_action, action_label="cambiar de aÃ±o")

    def on_select_week_click(self, event: ft.ControlEvent) -> None:
        week_number = event.control.data
        if isinstance(week_number, int):
            self.on_select_week(week_number)

    def on_select_week(self, week_number: int) -> None:
        if self.local_state.selected_year is None:
            return
        if not any(week.week_number == week_number for week in self._weeks_for_selected_year()):
            return

        def _action() -> None:
            self.local_state.selected_week = week_number
            self._clear_write_errors()
            self._load_entries_for_selected_week()

        self._run_or_confirm_resource_draft_before_context_change(_action, action_label="cambiar de week")

    def on_select_entry_click(self, event: ft.ControlEvent) -> None:
        entry_ref = event.control.data
        if isinstance(entry_ref, EntryRef):
            self.on_select_entry(entry_ref)

    def on_select_entry(self, entry_ref: EntryRef) -> None:
        def _action() -> None:
            self.local_state.viewer_entry_ref = entry_ref
            self._clear_write_errors()
            self._load_viewer_entry_and_sessions()

        self._run_or_confirm_resource_draft_before_context_change(_action, action_label="cambiar de entry")

    def on_manual_refresh(self, _event: ft.ControlEvent | None = None) -> None:
        def _action() -> None:
            self._clear_write_errors()
            self._refresh_and_reload(
                selected_year_override=self.local_state.selected_year,
                reload_q5=(self.local_state.selected_week is not None),
                reload_q8=(self.local_state.viewer_entry_ref is not None),
            )

        self._run_or_confirm_resource_draft_before_context_change(_action, action_label="refrescar")

    # Confirmations

    def on_open_extend_year_plus_one_confirm(self, _event: ft.ControlEvent | None = None) -> None:
        if not self.read_state.years:
            self._set_campaign_error("No hay aÃ±os visibles para extender +1.")
            self.notify()
            return
        target_year = max(self.read_state.years) + 1
        self._set_confirmation(
            key="extend_year_plus_one",
            title="Extender campaÃ±a +1 aÃ±o",
            body=f"Se crearÃ¡ el aÃ±o {target_year} con 20 weeks abiertas. Â¿Quieres continuar?",
            confirm_label="Crear aÃ±o",
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
                self._refresh_and_reload(
                    selected_year_override=result.new_year_number,
                    reload_q5=False,
                    reload_q8=(self.local_state.viewer_entry_ref is not None),
                )
                self.info_message = (
                    f"AÃ±o {result.new_year_number} creado "
                    f"(weeks {result.created_week_start}-{result.created_week_end})."
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

        if key == "session_delete" and isinstance(payload, str):
            self._confirm_delete_session(payload)
            self.notify()
            return

        self.notify()

    def on_cancel_pending_action(self, _event: ft.ControlEvent | None = None) -> None:
        self._clear_confirmation()
        self._clear_pending_context_action()
        self.notify()

    # Sessions

    def on_begin_session(self, _event: ft.ControlEvent | None = None) -> None:
        self.on_start_session(_event)

    def on_end_session(self, _event: ft.ControlEvent | None = None) -> None:
        self.on_stop_session(_event)

    def on_start_session(self, _event: ft.ControlEvent | None = None) -> None:
        self._run_session_write(
            lambda client, entry_ref: start_session(client, entry_ref=entry_ref),
            success_message="SesiÃ³n iniciada.",
        )

    def on_stop_session(self, _event: ft.ControlEvent | None = None) -> None:
        self._run_session_write(
            lambda client, entry_ref: stop_session(client, entry_ref=entry_ref),
            success_message="SesiÃ³n detenida.",
        )

    def on_open_manual_create_session(self, _event: ft.ControlEvent | None = None) -> None:
        if self.local_state.viewer_entry_ref is None:
            self._set_session_error("No hay entry en el visor para crear sesiÃ³n.")
            self.notify()
            return
        now_date, now_time = _to_local_strings(datetime.now(timezone.utc))
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
        session = _find_viewer_session_item(self.entry_panel_state.viewer_sessions, session_id)
        if session is None:
            self._set_session_error("La sesiÃ³n seleccionada ya no estÃ¡ visible en el visor.")
            self.notify()
            return

        started_date, started_time = _to_local_strings(session.started_at_utc)
        ended_date, ended_time = _to_local_strings(session.ended_at_utc)
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
        session = _find_viewer_session_item(self.entry_panel_state.viewer_sessions, session_id)
        if session is None:
            self._set_session_error("La sesiÃ³n seleccionada ya no estÃ¡ visible en el visor.")
            self.notify()
            return
        self._set_confirmation(
            key="session_delete",
            title="Borrar sesiÃ³n",
            body=f"Â¿Seguro que quieres borrar la sesiÃ³n '{session_id}'? Esta acciÃ³n es irreversible.",
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
            started_at_utc = _parse_local_datetime(
                form.started_date_local,
                form.started_time_local,
                field_label="Inicio",
            )
            if form.active_without_end:
                ended_at_utc = None
            else:
                ended_at_utc = _parse_optional_local_datetime(
                    form.ended_date_local,
                    form.ended_time_local,
                    field_label="Fin",
                )
                if ended_at_utc is None:
                    raise ValueError("Fin: rellena fecha y hora o marca 'SesiÃ³n activa'.")
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
                success_message="SesiÃ³n creada.",
            )
        else:
            if not form.session_id:
                form.error_message = "La sesiÃ³n objetivo no es vÃ¡lida."
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
                success_message="SesiÃ³n actualizada.",
            )
        if ok:
            self.session_form_state = None
        self.notify()

    # Week

    def on_open_week_notes_modal(self, _event: ft.ControlEvent | None = None) -> None:
        selected_week = self._find_selected_week_for_write()
        if selected_week is None:
            self._set_week_error("No hay week seleccionada para editar notas.")
            self.notify()
            return
        self.week_notes_editor_state = WeekNotesEditorState(
            notes_value=selected_week.notes_preview or "",
            error_message=None,
        )
        self.notify()

    def on_week_notes_change(self, event: ft.ControlEvent) -> None:
        if self.week_notes_editor_state is None:
            return
        self.week_notes_editor_state.notes_value = event.control.value or ""
        self.week_notes_editor_state.error_message = None
        self.notify()

    def on_cancel_week_notes_editor(self, _event: ft.ControlEvent | None = None) -> None:
        self.week_notes_editor_state = None
        self.notify()

    def on_submit_week_notes(self, _event: ft.ControlEvent | None = None) -> None:
        editor = self.week_notes_editor_state
        selected_week = self._find_selected_week_for_write()
        if editor is None:
            return
        if selected_week is None:
            editor.error_message = "No hay week seleccionada para guardar notas."
            self.notify()
            return
        result = self._run_week_write(
            lambda client: update_week_notes(
                client,
                year_number=selected_week.year_number,
                week_number=selected_week.week_number,
                notes=editor.notes_value,
            ),
            success_message="Notas de week actualizadas.",
        )
        if result is not None:
            self.week_notes_editor_state = None
        self.notify()

    def on_request_week_close(self, _event: ft.ControlEvent | None = None) -> None:
        selected_week = self._find_selected_week_for_write()
        if selected_week is None:
            self._set_week_error("No hay week seleccionada para cerrar.")
            self.notify()
            return
        self._set_confirmation(
            key="week_close",
            title="Cerrar week",
            body=f"La week {selected_week.week_number} pasarÃ¡ a closed. Â¿Quieres continuar?",
            confirm_label="Cerrar",
            payload=(selected_week.year_number, selected_week.week_number),
        )
        self.notify()

    def on_request_week_reopen(self, _event: ft.ControlEvent | None = None) -> None:
        selected_week = self._find_selected_week_for_write()
        if selected_week is None:
            self._set_week_error("No hay week seleccionada para reopen.")
            self.notify()
            return
        self._set_confirmation(
            key="week_reopen",
            title="Reopen week",
            body=f"La week {selected_week.week_number} pasarÃ¡ a open. Â¿Quieres continuar?",
            confirm_label="Reopen",
            payload=(selected_week.year_number, selected_week.week_number),
        )
        self.notify()

    def on_request_week_reclose(self, _event: ft.ControlEvent | None = None) -> None:
        selected_week = self._find_selected_week_for_write()
        if selected_week is None:
            self._set_week_error("No hay week seleccionada para reclose.")
            self.notify()
            return
        self._set_confirmation(
            key="week_reclose",
            title="Reclose week",
            body=f"La week {selected_week.week_number} se re-cerrarÃ¡. Â¿Quieres continuar?",
            confirm_label="Reclose",
            payload=(selected_week.year_number, selected_week.week_number),
        )
        self.notify()

    # Entry

    def on_open_entry_add_modal(self, _event: ft.ControlEvent | None = None) -> None:
        if self._get_selected_week_target_for_entry_create() is None:
            self._set_entry_error("No hay week seleccionada para crear entry.")
            self.notify()
            return
        self.entry_form_state = EntryFormState(
            mode="create",
            entry_type="scenario",
            scenario_ref_text="",
            error_message=None,
        )
        self.notify()

    def on_open_edit_entry_modal(self, _event: ft.ControlEvent | None = None) -> None:
        entry_ref = self._get_viewer_entry_ref_for_entry_write()
        viewer_entry = self.entry_panel_state.viewer_entry_snapshot
        if entry_ref is None or viewer_entry is None or viewer_entry.ref != entry_ref:
            self._set_entry_error("La entry visible no estÃ¡ cargada; refresca y reintenta.")
            self.notify()
            return
        self.entry_form_state = EntryFormState(
            mode="edit",
            entry_type=viewer_entry.entry_type,
            scenario_ref_text=(str(viewer_entry.scenario_ref) if viewer_entry.scenario_ref is not None else ""),
            error_message=None,
        )
        self.notify()

    def on_open_entry_delete_confirm(self, _event: ft.ControlEvent | None = None) -> None:
        entry_ref = self._get_viewer_entry_ref_for_entry_write()
        viewer_entry = self.entry_panel_state.viewer_entry_snapshot
        if entry_ref is None or viewer_entry is None or viewer_entry.ref != entry_ref:
            self._set_entry_error("No hay entry vÃ¡lida en el visor para borrar.")
            self.notify()
            return
        self._set_confirmation(
            key="entry_delete",
            title="Borrar entry",
            body=f"Â¿Seguro que quieres borrar '{viewer_entry.label}'? Esta acciÃ³n es irreversible.",
            confirm_label="Borrar",
            payload=entry_ref,
        )
        self.notify()

    def on_reorder_entry_up(self, _event: ft.ControlEvent | None = None) -> None:
        entry_ref = self._get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            self._set_entry_error("No hay entry en el visor para reordenar.")
            self.notify()
            return
        self._run_entry_write(
            lambda client: reorder_entry_within_week(client, entry_ref=entry_ref, direction="up"),
            reload_q5=entry_ref_matches_selected_week(self.local_state, entry_ref),
            reload_q8=True,
            success_message="Entry movida hacia arriba.",
        )
        self.notify()

    def on_reorder_entry_down(self, _event: ft.ControlEvent | None = None) -> None:
        entry_ref = self._get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            self._set_entry_error("No hay entry en el visor para reordenar.")
            self.notify()
            return
        self._run_entry_write(
            lambda client: reorder_entry_within_week(client, entry_ref=entry_ref, direction="down"),
            reload_q5=entry_ref_matches_selected_week(self.local_state, entry_ref),
            reload_q8=True,
            success_message="Entry movida hacia abajo.",
        )
        self.notify()

    def on_entry_form_set_type(self, event: ft.ControlEvent) -> None:
        form = self.entry_form_state
        if form is None:
            return
        form.entry_type = (event.control.value or "").strip()
        form.error_message = None
        self.notify()

    def on_entry_form_set_scenario_ref(self, event: ft.ControlEvent) -> None:
        form = self.entry_form_state
        if form is None:
            return
        form.scenario_ref_text = event.control.value or ""
        form.error_message = None
        self.notify()

    def on_cancel_entry_form(self, _event: ft.ControlEvent | None = None) -> None:
        self.entry_form_state = None
        self.notify()

    def on_submit_entry_form(self, _event: ft.ControlEvent | None = None) -> None:
        form = self.entry_form_state
        if form is None:
            return
        try:
            entry_type, scenario_ref = _parse_entry_form_values(
                entry_type_value=form.entry_type,
                scenario_ref_value=form.scenario_ref_text,
            )
        except ValueError as exc:
            form.error_message = str(exc)
            self.notify()
            return

        if form.mode == "create":
            create_target = self._get_selected_week_target_for_entry_create()
            if create_target is None:
                form.error_message = "No hay week seleccionada para crear una entry."
                self.notify()
                return
            year_number, week_number = create_target

            def _select_created_entry(result: EntryWriteResult) -> None:
                if result.entry_ref is not None:
                    self._discard_resource_draft_for_context_change(show_notice=False)
                    self.local_state.viewer_entry_ref = result.entry_ref

            result = self._run_entry_write(
                lambda client: create_entry(
                    client,
                    year_number=year_number,
                    week_number=week_number,
                    entry_type=entry_type,
                    scenario_ref=scenario_ref,
                ),
                reload_q5=True,
                reload_q8=True,
                before_refresh=_select_created_entry,
                success_message="Entry creada.",
            )
            if result is not None:
                self.entry_form_state = None
            self.notify()
            return

        entry_ref = self._get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            form.error_message = "No hay entry en el visor para editar."
            self.notify()
            return
        result = self._run_entry_write(
            lambda client: update_entry(
                client,
                entry_ref=entry_ref,
                entry_type=entry_type,
                scenario_ref=scenario_ref,
            ),
            reload_q5=entry_ref_matches_selected_week(self.local_state, entry_ref),
            reload_q8=True,
            success_message="Entry actualizada.",
        )
        if result is not None:
            self.entry_form_state = None
        self.notify()

    # Resources

    def on_adjust_resource_draft_delta(self, resource_key: str, adjustment_delta: int) -> None:
        entry_ref = self._get_viewer_entry_ref_for_resource_write()
        if entry_ref is None:
            self._set_resource_error("No hay entry en el visor para ajustar recursos.")
            self.notify()
            return
        if self.entry_panel_state.resource_draft_entry_ref != entry_ref:
            self._set_resource_error(
                "El borrador de recursos no coincide con la entry visible; refresca y reintenta."
            )
            self.notify()
            return
        if resource_key not in ENTRY_RESOURCE_KEYS:
            self._set_resource_error(f"Recurso no soportado: '{resource_key}'.")
            self.notify()
            return
        if isinstance(adjustment_delta, bool) or not isinstance(adjustment_delta, int) or adjustment_delta == 0:
            self._set_resource_error("El ajuste de recurso debe ser entero distinto de 0.")
            self.notify()
            return

        current_value = self.entry_panel_state.resource_draft_values.get(resource_key, 0)
        next_value = current_value + adjustment_delta
        if next_value == 0:
            self.entry_panel_state.resource_draft_values.pop(resource_key, None)
        else:
            self.entry_panel_state.resource_draft_values[resource_key] = next_value
        self.entry_panel_state.resource_draft_dirty = True
        self.entry_panel_state.resource_write_error_message = None
        self.notify()

    def on_adjust_resource_draft_delta_click(self, event: ft.ControlEvent) -> None:
        payload = event.control.data
        if (
            isinstance(payload, tuple)
            and len(payload) == 2
            and isinstance(payload[0], str)
            and isinstance(payload[1], int)
        ):
            self.on_adjust_resource_draft_delta(payload[0], payload[1])

    def on_save_resource_draft(self, _event: ft.ControlEvent | None = None) -> None:
        entry_ref = self._get_viewer_entry_ref_for_resource_write()
        if entry_ref is None:
            self._set_resource_error("No hay entry en el visor para guardar recursos.")
            self.notify()
            return
        if self.entry_panel_state.resource_draft_entry_ref != entry_ref:
            self._set_resource_error(
                "El borrador de recursos no coincide con la entry visible; refresca y reintenta."
            )
            self.notify()
            return
        if not self.entry_panel_state.resource_draft_dirty:
            return

        target_resource_deltas = self._normalize_resource_draft_values(self.entry_panel_state.resource_draft_values)
        result = self._run_resource_write(
            lambda client: replace_entry_resource_deltas(
                client,
                entry_ref=entry_ref,
                target_resource_deltas=target_resource_deltas,
            ),
            success_message="Recursos guardados.",
        )
        if result is not None:
            self.entry_panel_state.resource_draft_dirty = False
        self.notify()

    def on_discard_resource_draft(self, _event: ft.ControlEvent | None = None) -> None:
        viewer_entry = self.entry_panel_state.viewer_entry_snapshot
        entry_ref = self._get_viewer_entry_ref_for_resource_write()
        if viewer_entry is None or entry_ref is None or viewer_entry.ref != entry_ref:
            self._clear_resource_draft_state()
            self.entry_panel_state.resource_write_error_message = None
            self.notify()
            return
        self.entry_panel_state.resource_draft_entry_ref = viewer_entry.ref
        self.entry_panel_state.resource_draft_values = self._normalize_resource_draft_values(viewer_entry.resource_deltas)
        self.entry_panel_state.resource_draft_dirty = False
        self.entry_panel_state.resource_write_error_message = None
        self.info_message = "Cambios de recursos descartados."
        self.notify()

    # View Data

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

    # Internals

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
        if reload_q8:
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
            _map_week_read_to_summary(week)
            for week in snapshot.weeks_for_selected_year
        ]

        self.local_state.selected_year = snapshot.effective_year
        visible_week_numbers = {
            week.week_number for week in self.read_state.weeks_by_year[snapshot.effective_year]
        }
        if self.local_state.selected_week is not None and self.local_state.selected_week not in visible_week_numbers:
            self.local_state.selected_week = None

        if snapshot.active_entry is None:
            self.read_state.active_entry_ref = None
            self.read_state.active_entry_label = None
        else:
            self.read_state.active_entry_ref = snapshot.active_entry.entry_ref
            self.read_state.active_entry_label = snapshot.active_entry.label
        self.read_state.active_status_error_message = snapshot.active_status_error_message
        return True

    def _load_entries_for_selected_week(self) -> None:
        if self.local_state.selected_year is None or self.local_state.selected_week is None:
            self.entry_panel_state.entries_for_selected_week = []
            self.entry_panel_state.entries_panel_error_message = None
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
            return

        self.entry_panel_state.entries_for_selected_week = [_map_entry_read_to_summary(entry) for entry in entries]
        self.entry_panel_state.entries_panel_error_message = None

        if self.local_state.viewer_entry_ref is None:
            return
        if not entry_ref_matches_selected_week(self.local_state, self.local_state.viewer_entry_ref):
            return

        updated_entry = _find_entry_in_list(
            self.entry_panel_state.entries_for_selected_week,
            self.local_state.viewer_entry_ref,
        )
        if updated_entry is not None:
            self.entry_panel_state.viewer_entry_snapshot = updated_entry
            self._sync_resource_draft_from_viewer_snapshot()

    def _load_viewer_entry_and_sessions(self) -> None:
        if self.local_state.viewer_entry_ref is None:
            self.entry_panel_state.viewer_entry_snapshot = None
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = None
            self._clear_resource_draft_state()
            return
        try:
            client = self._build_client()
            viewer_entry_read = read_entry_by_ref(client, self.local_state.viewer_entry_ref)
        except (FirestoreConfigError, FirestoreReadError) as exc:
            self.entry_panel_state.viewer_sessions_error_message = str(exc)
            self.entry_panel_state.viewer_sessions = []
            if (
                self.entry_panel_state.viewer_entry_snapshot is not None
                and self.entry_panel_state.viewer_entry_snapshot.ref != self.local_state.viewer_entry_ref
            ):
                self.entry_panel_state.viewer_entry_snapshot = None
            return

        self.entry_panel_state.viewer_entry_snapshot = _map_entry_read_to_summary(viewer_entry_read)
        self._sync_resource_draft_from_viewer_snapshot()

        try:
            sessions = read_q8_sessions_for_entry(client, entry_ref=self.local_state.viewer_entry_ref)
        except FirestoreReadError as exc:
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = str(exc)
            return

        self.entry_panel_state.viewer_sessions = [
            _map_session_read_to_viewer_session(session)
            for session in sessions
        ]
        self.entry_panel_state.viewer_sessions_error_message = None

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
        if self._has_dirty_resource_draft_attached_to_viewer():
            self._queue_pending_context_action(action, action_label=action_label)
            self._set_confirmation(
                key="discard_resource_draft_context_change",
                title="Cambios de recursos sin guardar",
                body=(
                    "Hay cambios de recursos sin guardar. "
                    f"Si continÃºas para {action_label}, se descartarÃ¡n."
                ),
                confirm_label="Descartar y continuar",
                payload=action_label,
            )
            self.notify()
            return
        action()
        self.notify()

    def _normalize_resource_draft_values(self, raw_map: dict[str, int] | None) -> dict[str, int]:
        if not isinstance(raw_map, dict):
            return {}
        normalized: dict[str, int] = {}
        for key in ENTRY_RESOURCE_KEYS:
            value = raw_map.get(key)
            if isinstance(value, bool) or not isinstance(value, int):
                continue
            if value == 0:
                continue
            normalized[key] = value
        return normalized

    def _clear_resource_draft_state(self) -> None:
        self.entry_panel_state.resource_draft_entry_ref = None
        self.entry_panel_state.resource_draft_values = {}
        self.entry_panel_state.resource_draft_dirty = False

    def _resource_draft_attached_to_viewer(self) -> bool:
        return (
            self.local_state.viewer_entry_ref is not None
            and self.entry_panel_state.resource_draft_entry_ref == self.local_state.viewer_entry_ref
        )

    def _has_dirty_resource_draft_attached_to_viewer(self) -> bool:
        return self._resource_draft_attached_to_viewer() and self.entry_panel_state.resource_draft_dirty

    def _sync_resource_draft_from_viewer_snapshot(self) -> None:
        viewer_entry = self.entry_panel_state.viewer_entry_snapshot
        if viewer_entry is None:
            return
        normalized_viewer_deltas = self._normalize_resource_draft_values(viewer_entry.resource_deltas)
        if self.entry_panel_state.resource_draft_entry_ref != viewer_entry.ref:
            self.entry_panel_state.resource_draft_entry_ref = viewer_entry.ref
            self.entry_panel_state.resource_draft_values = normalized_viewer_deltas
            self.entry_panel_state.resource_draft_dirty = False
            return
        if not self.entry_panel_state.resource_draft_dirty:
            self.entry_panel_state.resource_draft_values = normalized_viewer_deltas

    def _discard_resource_draft_for_context_change(self, *, show_notice: bool) -> None:
        had_dirty = self.entry_panel_state.resource_draft_dirty
        self._clear_resource_draft_state()
        self.entry_panel_state.resource_write_error_message = None
        if show_notice and had_dirty:
            self.info_message = "Cambios de recursos sin guardar descartados al cambiar de contexto."

    def _clear_write_errors(self) -> None:
        self.entry_panel_state.session_write_error_message = None
        self.entry_panel_state.week_write_error_message = None
        self.entry_panel_state.entry_write_error_message = None
        self.entry_panel_state.resource_write_error_message = None

    def _set_campaign_error(self, message: str) -> None:
        self.read_state.warning_message = message

    def _set_session_error(self, message: str) -> None:
        self.entry_panel_state.session_write_error_message = message

    def _set_week_error(self, message: str) -> None:
        self.entry_panel_state.week_write_error_message = message

    def _set_entry_error(self, message: str) -> None:
        self.entry_panel_state.entry_write_error_message = message

    def _set_resource_error(self, message: str) -> None:
        self.entry_panel_state.resource_write_error_message = message

    def _handle_write_exception(self, *, domain: str, exc: Exception) -> None:
        message = str(exc)
        if isinstance(exc, (FirestoreConfigError, FirestoreReadError)):
            self.read_state.status = "error"
            self.read_state.error_message = message
            return

        if isinstance(exc, FirestoreConflictError):
            self.read_state.warning_message = message

        if domain == "session":
            self._set_session_error(message)
        elif domain == "week":
            self._set_week_error(message)
        elif domain == "entry":
            self._set_entry_error(message)
        elif domain == "resource":
            self._set_resource_error(message)
        elif domain == "campaign":
            self._set_campaign_error(message)

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
                reload_q8=(self.local_state.viewer_entry_ref is not None),
            )
            if result.auto_stopped_session_id:
                self.info_message = (
                    f"Week actualizada. Se auto-cerrÃ³ la sesiÃ³n {result.auto_stopped_session_id}."
                )
            else:
                self.info_message = success_message
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
    ) -> bool:
        entry_ref = self.local_state.viewer_entry_ref
        if entry_ref is None:
            self._set_session_error("No hay entry en el visor para gestionar sesiones.")
            return False

        self.entry_panel_state.session_write_pending = True
        self.entry_panel_state.session_write_error_message = None
        self.notify()
        try:
            client = self._build_client()
            action(client, entry_ref)
            self._refresh_and_reload(
                selected_year_override=self.local_state.selected_year,
                reload_q5=False,
                reload_q8=True,
            )
            self.info_message = success_message
            return True
        except (
            FirestoreConfigError,
            FirestoreReadError,
            FirestoreConflictError,
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreWriteError,
        ) as exc:
            self._handle_write_exception(domain="session", exc=exc)
            return False
        finally:
            self.entry_panel_state.session_write_pending = False

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
                self.info_message = (
                    f"Entry actualizada. Se auto-cerrÃ³ la sesiÃ³n {result.auto_stopped_session_id}."
                )
            else:
                self.info_message = success_message
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
    ) -> ResourceBulkWriteResult | None:
        self.entry_panel_state.resource_write_pending = True
        self.entry_panel_state.resource_write_error_message = None
        self.notify()
        try:
            client = self._build_client()
            result = action(client)
            self._refresh_and_reload(
                selected_year_override=self.local_state.selected_year,
                reload_q5=(self.local_state.selected_week is not None),
                reload_q8=(self.local_state.viewer_entry_ref is not None),
            )
            self.info_message = success_message
            return result
        except (
            FirestoreConfigError,
            FirestoreReadError,
            FirestoreConflictError,
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreWriteError,
        ) as exc:
            self._handle_write_exception(domain="resource", exc=exc)
            return None
        finally:
            self.entry_panel_state.resource_write_pending = False

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
                success_message="Week cerrada.",
            )
        elif transition_key == "week_reopen":
            self._run_week_write(
                lambda client: reopen_week(client, year_number=year_number, week_number=week_number),
                success_message="Week reabierta.",
            )
        elif transition_key == "week_reclose":
            self._run_week_write(
                lambda client: reclose_week(client, year_number=year_number, week_number=week_number),
                success_message="Week re-cerrada.",
            )

    def _confirm_delete_entry(self, entry_ref: EntryRef) -> None:
        reload_q5 = entry_ref_matches_selected_week(self.local_state, entry_ref)

        def _clear_viewer_after_delete(_result: EntryWriteResult) -> None:
            self.local_state.viewer_entry_ref = None
            self.entry_panel_state.viewer_entry_snapshot = None
            self.entry_panel_state.viewer_sessions = []
            self.entry_panel_state.viewer_sessions_error_message = None
            self._clear_resource_draft_state()

        self._run_entry_write(
            lambda client: delete_entry(client, entry_ref=entry_ref),
            reload_q5=reload_q5,
            reload_q8=False,
            before_refresh=_clear_viewer_after_delete,
            success_message="Entry borrada.",
        )

    def _confirm_delete_session(self, session_id: str) -> None:
        self._run_session_write(
            lambda client, entry_ref: manual_delete_session(
                client,
                entry_ref=entry_ref,
                session_id=session_id,
            ),
            success_message="SesiÃ³n borrada.",
        )


def _map_week_read_to_summary(week: WeekRead) -> WeekSummary:
    is_closed = week.status == "closed"
    notes_preview = week.notes or ""
    return WeekSummary(
        year_number=week.year_number,
        week_number=week.week_number,
        is_closed=is_closed,
        status_label=week.status,
        notes_preview=notes_preview,
    )


def _map_entry_read_to_summary(entry: EntryRead) -> EntrySummary:
    return EntrySummary(
        ref=entry.ref,
        label=entry.label,
        entry_type=entry.entry_type,
        scenario_ref=entry.scenario_ref,
        order_index=entry.order_index,
        resource_deltas=dict(entry.resource_deltas),
        created_at_utc=entry.created_at_utc,
        updated_at_utc=entry.updated_at_utc,
    )


def _map_session_read_to_viewer_session(session: EntrySessionRead) -> ViewerSessionItem:
    return ViewerSessionItem(
        session_id=session.session_id,
        started_at_utc=session.started_at_utc,
        ended_at_utc=session.ended_at_utc,
        created_at_utc=session.created_at_utc,
        updated_at_utc=session.updated_at_utc,
    )


def _find_entry_in_list(entries: list[EntrySummary], entry_ref: EntryRef) -> EntrySummary | None:
    for entry in entries:
        if entry.ref == entry_ref:
            return entry
    return None


def _find_viewer_session_item(
    sessions: list[ViewerSessionItem],
    session_id: str,
) -> ViewerSessionItem | None:
    for session in sessions:
        if session.session_id == session_id:
            return session
    return None


def _to_local_strings(value: object | None) -> tuple[str, str]:
    if isinstance(value, datetime):
        local = value.astimezone()
        return local.strftime("%Y-%m-%d"), local.strftime("%H:%M")
    return "", ""


def _parse_local_datetime(date_value: str, time_value: str, *, field_label: str) -> datetime:
    date_value = date_value.strip()
    time_value = time_value.strip()
    if not date_value or not time_value:
        raise ValueError(f"{field_label}: fecha y hora son obligatorias (YYYY-MM-DD y HH:MM).")
    try:
        naive = datetime.strptime(f"{date_value} {time_value}", "%Y-%m-%d %H:%M")
    except ValueError as exc:
        raise ValueError(f"{field_label}: formato invÃ¡lido, usa YYYY-MM-DD y HH:MM.") from exc
    local_tz = datetime.now().astimezone().tzinfo or timezone.utc
    aware_local = naive.replace(tzinfo=local_tz)
    return aware_local.astimezone(timezone.utc)


def _parse_optional_local_datetime(
    date_value: str,
    time_value: str,
    *,
    field_label: str,
) -> datetime | None:
    date_value = date_value.strip()
    time_value = time_value.strip()
    if not date_value and not time_value:
        return None
    return _parse_local_datetime(date_value, time_value, field_label=field_label)


def _parse_entry_form_values(*, entry_type_value: str, scenario_ref_value: str) -> tuple[str, int | None]:
    entry_type = (entry_type_value or "").strip().lower()
    if entry_type not in {"scenario", "outpost"}:
        raise ValueError("Entry type invÃ¡lido. Usa 'scenario' o 'outpost'.")
    raw_scenario = (scenario_ref_value or "").strip()
    if entry_type == "scenario":
        if not raw_scenario:
            raise ValueError("Scenario ref es obligatorio para entries de tipo scenario.")
        try:
            scenario_ref = int(raw_scenario)
        except ValueError as exc:
            raise ValueError("Scenario ref debe ser un entero positivo.") from exc
        if scenario_ref <= 0:
            raise ValueError("Scenario ref debe ser un entero positivo.")
        return entry_type, scenario_ref

    if raw_scenario:
        raise ValueError("Scenario ref debe quedar vacÃ­o para entries de tipo outpost.")
    return entry_type, None

