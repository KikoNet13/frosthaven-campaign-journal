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

class MainShellWeekEntryResourceActionsMixin:
    def on_open_week_notes_modal(self, _event: ft.ControlEvent | None = None) -> None:
        selected_week = self._find_selected_week_for_write()
        if selected_week is None:
            self._set_week_error("No hay semana seleccionada para editar notas.")
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
            editor.error_message = "No hay semana seleccionada para guardar notas."
            self.notify()
            return
        result = self._run_week_write(
            lambda client: update_week_notes(
                client,
                year_number=selected_week.year_number,
                week_number=selected_week.week_number,
                notes=editor.notes_value,
            ),
            success_message="Notas de semana actualizadas.",
        )
        if result is not None:
            self.week_notes_editor_state = None
        self.notify()

    def on_request_week_close(self, _event: ft.ControlEvent | None = None) -> None:
        selected_week = self._find_selected_week_for_write()
        if selected_week is None:
            self._set_week_error("No hay semana seleccionada para cerrar.")
            self.notify()
            return
        self._set_confirmation(
            key="week_close",
            title="Cerrar semana",
            body=f"La semana {selected_week.week_number} pasará a cerrada. ¿Quieres continuar?",
            confirm_label="Cerrar",
            payload=(selected_week.year_number, selected_week.week_number),
        )
        self.notify()

    def on_request_week_reopen(self, _event: ft.ControlEvent | None = None) -> None:
        selected_week = self._find_selected_week_for_write()
        if selected_week is None:
            self._set_week_error("No hay semana seleccionada para reabrir.")
            self.notify()
            return
        self._set_confirmation(
            key="week_reopen",
            title="Reabrir semana",
            body=f"La semana {selected_week.week_number} pasará a abierta. ¿Quieres continuar?",
            confirm_label="Reabrir",
            payload=(selected_week.year_number, selected_week.week_number),
        )
        self.notify()

    def on_request_week_reclose(self, _event: ft.ControlEvent | None = None) -> None:
        selected_week = self._find_selected_week_for_write()
        if selected_week is None:
            self._set_week_error("No hay semana seleccionada para recerrar.")
            self.notify()
            return
        self._set_confirmation(
            key="week_reclose",
            title="Recerrar semana",
            body=f"La semana {selected_week.week_number} se recerrará. ¿Quieres continuar?",
            confirm_label="Recerrar",
            payload=(selected_week.year_number, selected_week.week_number),
        )
        self.notify()

    # Entry

    def on_open_entry_add_modal(self, _event: ft.ControlEvent | None = None) -> None:
        if self._get_selected_week_target_for_entry_create() is None:
            self._set_entry_error("No hay semana seleccionada para crear una entrada.")
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
            self._set_entry_error("La entrada visible no está cargada; refresca y reintenta.")
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
            self._set_entry_error("No hay entrada válida en el visor para borrar.")
            self.notify()
            return
        self._set_confirmation(
            key="entry_delete",
            title="Borrar entrada",
            body=f"¿Seguro que quieres borrar '{viewer_entry.label}'? Esta acción es irreversible.",
            confirm_label="Borrar",
            payload=entry_ref,
        )
        self.notify()

    def on_reorder_entry_up(self, _event: ft.ControlEvent | None = None) -> None:
        entry_ref = self._get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            self._set_entry_error("No hay entrada en el visor para reordenar.")
            self.notify()
            return
        self._run_entry_write(
            lambda client: reorder_entry_within_week(client, entry_ref=entry_ref, direction="up"),
            reload_q5=entry_ref_matches_selected_week(self.local_state, entry_ref),
            reload_q8=True,
            success_message="Entrada movida hacia arriba.",
        )
        self.notify()

    def on_reorder_entry_down(self, _event: ft.ControlEvent | None = None) -> None:
        entry_ref = self._get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            self._set_entry_error("No hay entrada en el visor para reordenar.")
            self.notify()
            return
        self._run_entry_write(
            lambda client: reorder_entry_within_week(client, entry_ref=entry_ref, direction="down"),
            reload_q5=entry_ref_matches_selected_week(self.local_state, entry_ref),
            reload_q8=True,
            success_message="Entrada movida hacia abajo.",
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
            entry_type, scenario_ref = parse_entry_form_values(
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
                form.error_message = "No hay semana seleccionada para crear una entrada."
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
                success_message="Entrada creada.",
            )
            if result is not None:
                self.entry_form_state = None
            self.notify()
            return

        entry_ref = self._get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            form.error_message = "No hay entrada en el visor para editar."
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
            success_message="Entrada actualizada.",
        )
        if result is not None:
            self.entry_form_state = None
        self.notify()

    # Resources

    def on_adjust_resource_draft_delta(self, resource_key: str, adjustment_delta: int) -> None:
        entry_ref = self._get_viewer_entry_ref_for_resource_write()
        if entry_ref is None:
            self._set_resource_error("No hay entrada en el visor para ajustar recursos.")
            self.notify()
            return
        if self.entry_panel_state.resource_draft_entry_ref != entry_ref:
            self._set_resource_error(
                "El borrador de recursos no coincide con la entrada visible; refresca y reintenta."
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
            self._set_resource_error("No hay entrada en el visor para guardar recursos.")
            self.notify()
            return
        if self.entry_panel_state.resource_draft_entry_ref != entry_ref:
            self._set_resource_error(
                "El borrador de recursos no coincide con la entrada visible; refresca y reintenta."
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
