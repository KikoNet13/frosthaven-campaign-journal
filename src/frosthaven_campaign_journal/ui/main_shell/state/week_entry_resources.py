from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.data import (
    EntryWriteResult,
    create_entry,
    reorder_entry_within_week,
    replace_entry_resource_deltas,
    update_entry,
    update_entry_notes,
)
from frosthaven_campaign_journal.models import ENTRY_RESOURCE_KEYS, EntryRef, entry_ref_matches_selected_week
from frosthaven_campaign_journal.ui.main_shell.state.types import (
    EntryFormState,
    EntryNotesEditorState,
)
from frosthaven_campaign_journal.ui.main_shell.state.utils import (
    find_entry_in_list,
    parse_entry_form_values,
)


class MainShellWeekEntryResourceActionsMixin:
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
        if entry_ref is None:
            self._set_entry_error("No hay entrada en foco para editar.")
            self.notify()
            return
        self.on_open_edit_entry_modal_for_entry(entry_ref)

    def on_open_edit_entry_modal_for_entry(self, entry_ref: EntryRef) -> None:
        selected_entry = find_entry_in_list(self.entry_panel_state.entries_for_selected_week, entry_ref)
        if selected_entry is None:
            self._set_entry_error("La entrada seleccionada no está disponible; refresca y reintenta.")
            self.notify()
            return
        self.local_state.viewer_entry_ref = entry_ref
        self.entry_form_state = EntryFormState(
            mode="edit",
            entry_type=selected_entry.entry_type,
            scenario_ref_text=(str(selected_entry.scenario_ref) if selected_entry.scenario_ref is not None else ""),
            error_message=None,
        )
        self.notify()

    def on_open_edit_entry_modal_click(self, event: ft.ControlEvent) -> None:
        entry_ref = event.control.data
        if isinstance(entry_ref, EntryRef):
            self.on_open_edit_entry_modal_for_entry(entry_ref)

    def on_open_entry_delete_confirm(self, _event: ft.ControlEvent | None = None) -> None:
        entry_ref = self._get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            self._set_entry_error("No hay entrada en foco para borrar.")
            self.notify()
            return
        self._open_entry_delete_confirm_for_ref(entry_ref)

    def _open_entry_delete_confirm_for_ref(
        self,
        entry_ref: EntryRef,
        *,
        fallback_label: str | None = None,
    ) -> None:
        selected_entry = find_entry_in_list(self.entry_panel_state.entries_for_selected_week, entry_ref)
        label = selected_entry.label if selected_entry is not None else (fallback_label or f"Entrada {entry_ref.entry_id}")
        self._set_confirmation(
            key="entry_delete",
            title="Borrar entrada",
            body=f"¿Seguro que quieres borrar '{label}'? Esta acción es irreversible.",
            confirm_label="Borrar",
            payload=entry_ref,
        )
        self.notify()

    def on_open_entry_delete_confirm_click(self, event: ft.ControlEvent) -> None:
        entry_ref = event.control.data
        if isinstance(entry_ref, EntryRef):
            self._open_entry_delete_confirm_for_ref(entry_ref)

    def on_open_entry_delete_confirm_for_entry(self, entry_ref: EntryRef) -> None:
        self._open_entry_delete_confirm_for_ref(entry_ref)

    def on_reorder_entry_up(self, _event: ft.ControlEvent | None = None) -> None:
        entry_ref = self._get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            self._set_entry_error("No hay entrada en foco para reordenar.")
            self.notify()
            return
        self._reorder_entry_by_ref(entry_ref, direction="up")
        self.notify()

    def on_reorder_entry_down(self, _event: ft.ControlEvent | None = None) -> None:
        entry_ref = self._get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            self._set_entry_error("No hay entrada en foco para reordenar.")
            self.notify()
            return
        self._reorder_entry_by_ref(entry_ref, direction="down")
        self.notify()

    def _reorder_entry_by_ref(self, entry_ref: EntryRef, *, direction: str) -> None:
        self._run_entry_write(
            lambda client: reorder_entry_within_week(client, entry_ref=entry_ref, direction=direction),
            reload_q5=entry_ref_matches_selected_week(self.local_state, entry_ref),
            reload_q8=False,
            success_message="Entrada reordenada.",
        )

    def on_reorder_entry_up_click(self, event: ft.ControlEvent) -> None:
        entry_ref = event.control.data
        if isinstance(entry_ref, EntryRef):
            self._reorder_entry_by_ref(entry_ref, direction="up")
            self.notify()

    def on_reorder_entry_down_click(self, event: ft.ControlEvent) -> None:
        entry_ref = event.control.data
        if isinstance(entry_ref, EntryRef):
            self._reorder_entry_by_ref(entry_ref, direction="down")
            self.notify()

    def on_reorder_entry_left_for_entry(self, entry_ref: EntryRef) -> None:
        self._reorder_entry_by_ref(entry_ref, direction="up")
        self.notify()

    def on_reorder_entry_right_for_entry(self, entry_ref: EntryRef) -> None:
        self._reorder_entry_by_ref(entry_ref, direction="down")
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
                reload_q8=False,
                before_refresh=_select_created_entry,
                success_message="Entrada creada.",
            )
            if result is not None:
                self.entry_form_state = None
            self.notify()
            return

        entry_ref = self._get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            form.error_message = "No hay entrada en foco para editar."
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
            reload_q8=False,
            success_message="Entrada actualizada.",
        )
        if result is not None:
            self.entry_form_state = None
        self.notify()

    # Entry notes

    def on_open_entry_notes_editor(self, entry_ref: EntryRef) -> None:
        selected_entry = find_entry_in_list(self.entry_panel_state.entries_for_selected_week, entry_ref)
        if selected_entry is None:
            self._set_entry_error("No hay entrada cargada para editar notas.")
            self.notify()
            return
        self.local_state.viewer_entry_ref = entry_ref
        self.entry_notes_editor_state = EntryNotesEditorState(
            entry_ref=entry_ref,
            entry_label=selected_entry.label,
            notes_value=selected_entry.notes or "",
            error_message=None,
        )
        self.notify()

    def on_open_entry_notes_editor_click(self, event: ft.ControlEvent) -> None:
        entry_ref = event.control.data
        if isinstance(entry_ref, EntryRef):
            self.on_open_entry_notes_editor(entry_ref)

    def on_entry_notes_change(self, event: ft.ControlEvent) -> None:
        editor = self.entry_notes_editor_state
        if editor is None:
            return
        editor.notes_value = event.control.value or ""
        editor.error_message = None
        self.notify()

    def on_cancel_entry_notes_editor(self, _event: ft.ControlEvent | None = None) -> None:
        self.entry_notes_editor_state = None
        self.notify()

    def on_submit_entry_notes(self, _event: ft.ControlEvent | None = None) -> None:
        editor = self.entry_notes_editor_state
        if editor is None:
            return

        result = self._run_entry_write(
            lambda client: update_entry_notes(
                client,
                entry_ref=editor.entry_ref,
                notes=editor.notes_value,
            ),
            reload_q5=entry_ref_matches_selected_week(self.local_state, editor.entry_ref),
            reload_q8=False,
            success_message="Notas de entrada actualizadas.",
        )
        if result is not None:
            self.entry_notes_editor_state = None
        elif self.entry_panel_state.entry_write_error_message:
            editor.error_message = self.entry_panel_state.entry_write_error_message
        self.notify()

    # Resources

    def on_adjust_resource_draft_delta(self, resource_key: str, adjustment_delta: int) -> None:
        entry_ref = self._get_viewer_entry_ref_for_resource_write()
        if entry_ref is None:
            self._set_resource_error("No hay entrada en foco para ajustar recursos.")
            self.notify()
            return
        self.on_adjust_resource_draft_delta_for_entry(entry_ref, resource_key, adjustment_delta)

    def on_adjust_resource_draft_delta_for_entry(
        self,
        entry_ref: EntryRef,
        resource_key: str,
        adjustment_delta: int,
    ) -> None:
        if resource_key not in ENTRY_RESOURCE_KEYS:
            self._set_resource_error(f"Recurso no soportado: '{resource_key}'.", entry_ref=entry_ref)
            self.notify()
            return
        if isinstance(adjustment_delta, bool) or not isinstance(adjustment_delta, int) or adjustment_delta == 0:
            self._set_resource_error("El ajuste de recurso debe ser entero distinto de 0.", entry_ref=entry_ref)
            self.notify()
            return

        draft_map = self._resource_draft_for_entry(entry_ref)
        current_value = draft_map.get(resource_key, 0)
        next_value = current_value + adjustment_delta
        if next_value == 0:
            draft_map.pop(resource_key, None)
        else:
            draft_map[resource_key] = next_value
        self.entry_panel_state.resource_draft_dirty_by_entry_ref[entry_ref] = True
        self.entry_panel_state.resource_write_error_by_entry_ref[entry_ref] = None

        if self.local_state.viewer_entry_ref == entry_ref:
            self.entry_panel_state.resource_draft_entry_ref = entry_ref
            self.entry_panel_state.resource_draft_values = dict(draft_map)
            self.entry_panel_state.resource_draft_dirty = True
            self.entry_panel_state.resource_write_error_message = None

        self.notify()

    def on_adjust_resource_draft_delta_click(self, event: ft.ControlEvent) -> None:
        payload = event.control.data
        if (
            isinstance(payload, tuple)
            and len(payload) == 3
            and isinstance(payload[0], EntryRef)
            and isinstance(payload[1], str)
            and isinstance(payload[2], int)
        ):
            self.on_adjust_resource_draft_delta_for_entry(payload[0], payload[1], payload[2])
            return
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
            self._set_resource_error("No hay entrada en foco para guardar recursos.")
            self.notify()
            return
        self.on_save_resource_draft_for_entry(entry_ref)

    def on_save_resource_draft_for_entry(self, entry_ref: EntryRef) -> None:
        draft_map = self._resource_draft_for_entry(entry_ref)
        if not self._is_resource_draft_dirty(entry_ref):
            return

        target_resource_deltas = self._normalize_resource_draft_values(draft_map)
        result = self._run_resource_write(
            lambda client: replace_entry_resource_deltas(
                client,
                entry_ref=entry_ref,
                target_resource_deltas=target_resource_deltas,
            ),
            success_message="Recursos guardados.",
            entry_ref=entry_ref,
        )
        if result is not None:
            self.entry_panel_state.resource_draft_dirty_by_entry_ref[entry_ref] = False
            if self.local_state.viewer_entry_ref == entry_ref:
                self.entry_panel_state.resource_draft_entry_ref = entry_ref
                self.entry_panel_state.resource_draft_values = dict(target_resource_deltas)
                self.entry_panel_state.resource_draft_dirty = False
        self.notify()

    def on_discard_resource_draft(self, _event: ft.ControlEvent | None = None) -> None:
        entry_ref = self._get_viewer_entry_ref_for_resource_write()
        if entry_ref is None:
            self._set_resource_error("No hay entrada en foco para descartar recursos.")
            self.notify()
            return
        self.on_discard_resource_draft_for_entry(entry_ref)

    def on_discard_resource_draft_for_entry(self, entry_ref: EntryRef) -> None:
        entry = find_entry_in_list(self.entry_panel_state.entries_for_selected_week, entry_ref)
        if entry is None:
            self._clear_resource_draft_for_entry(entry_ref)
            self.notify()
            return
        normalized = self._normalize_resource_draft_values(entry.resource_deltas)
        self._set_resource_draft_for_entry(entry_ref, normalized, dirty=False)
        self.entry_panel_state.resource_write_error_by_entry_ref[entry_ref] = None
        if self.local_state.viewer_entry_ref == entry_ref:
            self.entry_panel_state.resource_draft_entry_ref = entry_ref
            self.entry_panel_state.resource_draft_values = dict(normalized)
            self.entry_panel_state.resource_draft_dirty = False
            self.entry_panel_state.resource_write_error_message = None
        self._emit_info_toast("Cambios de recursos descartados.")
        self.notify()
