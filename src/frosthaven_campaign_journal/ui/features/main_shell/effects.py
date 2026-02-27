from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timezone

import flet as ft

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
    reopen_week,
    reorder_entry_within_week,
    replace_entry_resource_deltas,
    start_session,
    stop_session,
    update_entry,
    update_week_notes,
)
from frosthaven_campaign_journal.state.placeholders import EntryRef, MockEntry, MockWeek, ViewerSessionItem
from frosthaven_campaign_journal.ui.features.main_shell import dialogs
from frosthaven_campaign_journal.ui.features.main_shell.intents import (
    MainShellIntent,
    ResourceDraftLeaveDialogCancelPressed,
    ResourceDraftLeaveDialogDiscardPressed,
    ResourceDraftLeaveDialogSavePressed,
)
from frosthaven_campaign_journal.ui.features.main_shell.reducer import MainShellEffect
from frosthaven_campaign_journal.ui.features.main_shell.selectors import (
    clear_all_write_errors,
    clear_resource_draft_state,
    discard_resource_draft_for_context_change,
    entry_belongs_to_selected_week,
    selected_week_for_write,
    selected_week_target_for_entry_create,
    sync_resource_draft_from_viewer_snapshot,
    viewer_entry_ref_for_entry_write,
    viewer_entry_ref_for_resource_write,
    viewer_matches_week,
)
from frosthaven_campaign_journal.ui.features.main_shell.state import MainShellState


class MainShellEffects:
    def __init__(
        self,
        *,
        page: ft.Page,
        build_client: Callable[[], object],
    ) -> None:
        self._page = page
        self._build_client = build_client
        self._active_dialog: ft.AlertDialog | None = None

    def run(
        self,
        *,
        effect: MainShellEffect,
        state: MainShellState,
        dispatch: Callable[[MainShellIntent], None],
    ) -> None:
        kind = effect.kind
        payload = effect.payload

        if kind == "refresh_data":
            self._refresh_and_reload(
                state,
                selected_year_override=payload.get("selected_year_override"),
                reload_q5=bool(payload.get("reload_q5")),
                reload_q8=bool(payload.get("reload_q8")),
            )
            return
        if kind == "load_entries_for_selected_week":
            self._load_entries_for_selected_week(state)
            return
        if kind == "load_viewer_entry_and_sessions":
            self._load_viewer_entry_and_sessions(state)
            return
        if kind == "show_resource_draft_leave_confirm_dialog":
            self._show_resource_draft_leave_confirm_dialog(
                state=state,
                action_label=str(payload.get("action_label") or "cambiar de contexto"),
                dispatch=dispatch,
            )
            return
        if kind == "close_dialog":
            self._close_dialog()
            return
        if kind == "show_discard_notice_if_any":
            if state.entry_panel_state.resource_draft_discard_notice:
                self._show_snack_info(state.entry_panel_state.resource_draft_discard_notice)
            return
        if kind == "replay_pending_context_intent":
            pending = state.workflow.pending_context_intent
            state.workflow.pending_context_intent = None
            state.workflow.pending_context_action_label = None
            if pending is not None:
                dispatch(pending)
            return
        if kind == "save_resource_draft_before_context_change":
            result = self._run_resource_draft_save(state)
            if result is None:
                state.workflow.pending_context_intent = None
                state.workflow.pending_context_action_label = None
            return
        if kind == "run_begin_session":
            self._run_session_write(
                state,
                lambda client, entry_ref: start_session(client, entry_ref=entry_ref),
            )
            return
        if kind == "run_end_session":
            self._run_session_write(
                state,
                lambda client, entry_ref: stop_session(client, entry_ref=entry_ref),
            )
            return
        if kind == "show_week_notes_dialog":
            self._show_week_notes_dialog(state)
            return
        if kind == "show_week_state_confirm_dialog":
            self._show_week_state_confirm_dialog(state, mode=str(payload.get("mode") or ""))
            return
        if kind == "show_extend_year_plus_one_confirm_dialog":
            self._show_extend_year_plus_one_confirm_dialog(state)
            return
        if kind == "show_entry_form_dialog":
            self._show_entry_form_dialog(state, mode=str(payload.get("mode") or ""))
            return
        if kind == "show_entry_delete_confirm_dialog":
            self._show_entry_delete_confirm_dialog(state)
            return
        if kind == "run_reorder_entry":
            direction = str(payload.get("direction") or "")
            if direction in {"up", "down"}:
                self._run_reorder_entry(state, direction=direction)
            return
        if kind == "show_session_form_dialog":
            session_id = payload.get("session_id")
            self._show_session_form_dialog(
                state=state,
                mode=str(payload.get("mode") or ""),
                session_id=(str(session_id) if isinstance(session_id, str) else None),
            )
            return
        if kind == "show_delete_session_confirm_dialog":
            session_id = payload.get("session_id")
            if isinstance(session_id, str):
                self._show_delete_session_confirm_dialog(state, session_id=session_id)
            return
        if kind == "run_save_resource_draft":
            self._run_resource_draft_save(state)
            return

    def _refresh_and_reload(
        self,
        state: MainShellState,
        *,
        selected_year_override: int | None,
        reload_q5: bool,
        reload_q8: bool,
    ) -> None:
        self._load_readonly_snapshot(state, selected_year_override=selected_year_override)
        if reload_q5:
            self._load_entries_for_selected_week(state)
        if reload_q8:
            self._load_viewer_entry_and_sessions(state)

    def _load_readonly_snapshot(
        self,
        state: MainShellState,
        *,
        selected_year_override: int | None,
    ) -> bool:
        try:
            client = self._build_client()
            snapshot = load_main_screen_snapshot(
                client,
                selected_year=selected_year_override,
                viewer_entry_ref=state.local_state.viewer_entry_ref,
            )
        except (FirestoreConfigError, FirestoreReadError) as exc:
            state.read_state.status = "error"
            state.read_state.error_message = str(exc)
            state.read_state.warning_message = None
            return False

        state.read_state.status = "ready"
        state.read_state.error_message = None
        state.read_state.years = snapshot.years
        state.read_state.campaign_resource_totals = snapshot.campaign_main.resource_totals
        state.read_state.weeks_by_year[snapshot.effective_year] = [
            _map_week_read_to_mock(week)
            for week in snapshot.weeks_for_selected_year
        ]

        state.local_state.selected_year = snapshot.effective_year
        visible_week_numbers = {
            week.week_number
            for week in state.read_state.weeks_by_year[snapshot.effective_year]
        }
        if (
            state.local_state.selected_week is not None
            and state.local_state.selected_week not in visible_week_numbers
        ):
            state.local_state.selected_week = None
        state.read_state.warning_message = None

        if snapshot.active_entry is None:
            state.read_state.active_entry_ref = None
            state.read_state.active_entry_label = None
        else:
            state.read_state.active_entry_ref = snapshot.active_entry.entry_ref
            state.read_state.active_entry_label = snapshot.active_entry.label
        state.read_state.active_status_error_message = snapshot.active_status_error_message
        return True

    def _load_entries_for_selected_week(self, state: MainShellState) -> None:
        if state.local_state.selected_year is None or state.local_state.selected_week is None:
            state.entry_panel_state.entries_for_selected_week = []
            state.entry_panel_state.entries_panel_error_message = None
            return

        try:
            client = self._build_client()
            entries = read_q5_entries_for_selected_week(
                client,
                year_number=state.local_state.selected_year,
                week_number=state.local_state.selected_week,
            )
        except (FirestoreConfigError, FirestoreReadError) as exc:
            state.entry_panel_state.entries_for_selected_week = []
            state.entry_panel_state.entries_panel_error_message = str(exc)
            return

        state.entry_panel_state.entries_for_selected_week = [
            _map_entry_read_to_mock(entry)
            for entry in entries
        ]
        state.entry_panel_state.entries_panel_error_message = None

        if state.local_state.viewer_entry_ref is None:
            return
        if not entry_belongs_to_selected_week(state, state.local_state.viewer_entry_ref):
            return

        updated_entry = _find_entry_in_list(
            state.entry_panel_state.entries_for_selected_week,
            state.local_state.viewer_entry_ref,
        )
        if updated_entry is not None:
            state.entry_panel_state.viewer_entry_snapshot = updated_entry
            sync_resource_draft_from_viewer_snapshot(state)

    def _load_viewer_entry_and_sessions(self, state: MainShellState) -> None:
        if state.local_state.viewer_entry_ref is None:
            state.entry_panel_state.viewer_entry_snapshot = None
            state.entry_panel_state.viewer_sessions = []
            state.entry_panel_state.viewer_sessions_error_message = None
            clear_resource_draft_state(state)
            return

        try:
            client = self._build_client()
            viewer_entry_read = read_entry_by_ref(client, state.local_state.viewer_entry_ref)
        except (FirestoreConfigError, FirestoreReadError) as exc:
            state.entry_panel_state.viewer_sessions_error_message = str(exc)
            state.entry_panel_state.viewer_sessions = []
            if (
                state.entry_panel_state.viewer_entry_snapshot is not None
                and state.entry_panel_state.viewer_entry_snapshot.ref != state.local_state.viewer_entry_ref
            ):
                state.entry_panel_state.viewer_entry_snapshot = None
            return

        state.entry_panel_state.viewer_entry_snapshot = _map_entry_read_to_mock(viewer_entry_read)
        sync_resource_draft_from_viewer_snapshot(state)

        try:
            sessions = read_q8_sessions_for_entry(
                client,
                entry_ref=state.local_state.viewer_entry_ref,
            )
        except FirestoreReadError as exc:
            state.entry_panel_state.viewer_sessions = []
            state.entry_panel_state.viewer_sessions_error_message = str(exc)
            return

        state.entry_panel_state.viewer_sessions = [
            _map_session_read_to_viewer_session(session)
            for session in sessions
        ]
        state.entry_panel_state.viewer_sessions_error_message = None

    def _run_campaign_write(
        self,
        state: MainShellState,
        action,
    ) -> CampaignWriteResult | None:
        state.read_state.campaign_write_pending = True
        result: CampaignWriteResult | None = None
        success = True
        try:
            client = self._build_client()
            result = action(client)
        except FirestoreConflictError as exc:
            self._show_snack_error(str(exc))
            success = False
        except (
            FirestoreConfigError,
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreReadError,
            FirestoreWriteError,
        ) as exc:
            self._show_snack_error(str(exc))
            success = False
        finally:
            state.read_state.campaign_write_pending = False

        if not success:
            return None
        return result

    def _run_week_write(self, state: MainShellState, action) -> WeekWriteResult | None:
        target_week = selected_week_for_write(state)
        if (
            state.local_state.selected_year is None
            or state.local_state.selected_week is None
            or target_week is None
        ):
            state.entry_panel_state.week_write_error_message = (
                "No hay week seleccionada para ejecutar la acciÃ³n."
            )
            return None

        year_number = state.local_state.selected_year
        week_number = state.local_state.selected_week
        state.entry_panel_state.week_write_pending = True
        state.entry_panel_state.week_write_error_message = None
        result: WeekWriteResult | None = None
        success = True
        try:
            client = self._build_client()
            result = action(client, year_number, week_number)
        except FirestoreConflictError as exc:
            state.entry_panel_state.week_write_error_message = str(exc)
            success = False
        except (
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreReadError,
            FirestoreWriteError,
        ) as exc:
            state.entry_panel_state.week_write_error_message = str(exc)
            success = False
        finally:
            state.entry_panel_state.week_write_pending = False

        if not success:
            return None

        self._refresh_and_reload(
            state,
            selected_year_override=state.local_state.selected_year,
            reload_q5=False,
            reload_q8=viewer_matches_week(state, year_number, week_number),
        )
        return result

    def _run_session_write(self, state: MainShellState, action) -> bool:
        if state.local_state.viewer_entry_ref is None:
            state.entry_panel_state.session_write_error_message = (
                "No hay entry en el visor para ejecutar la acciÃ³n de sesiÃ³n."
            )
            return False

        state.entry_panel_state.session_write_pending = True
        state.entry_panel_state.session_write_error_message = None
        success = True
        try:
            client = self._build_client()
            action(client, state.local_state.viewer_entry_ref)
        except FirestoreConflictError as exc:
            state.entry_panel_state.session_write_error_message = str(exc)
            success = False
        except (FirestoreTransitionInvalidError, FirestoreValidationError, FirestoreReadError) as exc:
            state.entry_panel_state.session_write_error_message = str(exc)
            success = False
        finally:
            state.entry_panel_state.session_write_pending = False

        if not success:
            return False

        self._refresh_and_reload(
            state,
            selected_year_override=state.local_state.selected_year,
            reload_q5=False,
            reload_q8=(state.local_state.viewer_entry_ref is not None),
        )
        return True

    def _run_entry_write(
        self,
        state: MainShellState,
        action,
        *,
        reload_q5: bool,
        reload_q8: bool,
        before_refresh=None,
    ) -> EntryWriteResult | None:
        state.entry_panel_state.entry_write_pending = True
        state.entry_panel_state.entry_write_error_message = None
        result: EntryWriteResult | None = None
        success = True
        try:
            client = self._build_client()
            result = action(client)
        except FirestoreConflictError as exc:
            state.entry_panel_state.entry_write_error_message = str(exc)
            success = False
        except (
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreReadError,
            FirestoreWriteError,
        ) as exc:
            state.entry_panel_state.entry_write_error_message = str(exc)
            success = False
        finally:
            state.entry_panel_state.entry_write_pending = False

        if not success:
            return None

        if before_refresh is not None and result is not None:
            before_refresh(result)

        self._refresh_and_reload(
            state,
            selected_year_override=state.local_state.selected_year,
            reload_q5=reload_q5,
            reload_q8=reload_q8,
        )
        return result

    def _run_resource_draft_save(self, state: MainShellState) -> ResourceBulkWriteResult | None:
        entry_ref = viewer_entry_ref_for_resource_write(state)
        if entry_ref is None:
            state.entry_panel_state.resource_write_error_message = (
                "No hay entry en el visor para guardar recursos."
            )
            return None
        if state.entry_panel_state.resource_draft_entry_ref != entry_ref:
            state.entry_panel_state.resource_write_error_message = (
                "El borrador de recursos no coincide con la entry visible; refresca y reintenta."
            )
            return None

        reload_q5 = entry_belongs_to_selected_week(state, entry_ref)
        target_resource_deltas = dict(state.entry_panel_state.resource_draft_values)

        state.entry_panel_state.resource_write_pending = True
        state.entry_panel_state.resource_write_error_message = None
        result: ResourceBulkWriteResult | None = None
        success = True
        try:
            client = self._build_client()
            result = replace_entry_resource_deltas(
                client,
                entry_ref=entry_ref,
                target_resource_deltas=target_resource_deltas,
            )
        except FirestoreConflictError as exc:
            state.entry_panel_state.resource_write_error_message = str(exc)
            success = False
        except (
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreReadError,
            FirestoreWriteError,
        ) as exc:
            state.entry_panel_state.resource_write_error_message = str(exc)
            success = False
        finally:
            state.entry_panel_state.resource_write_pending = False

        if not success:
            return None

        state.entry_panel_state.resource_draft_dirty = False
        state.entry_panel_state.resource_draft_discard_notice = None
        if result is not None and result.no_op:
            return result

        self._refresh_and_reload(
            state,
            selected_year_override=state.local_state.selected_year,
            reload_q5=reload_q5,
            reload_q8=(state.local_state.viewer_entry_ref is not None),
        )
        return result

    def _run_reorder_entry(self, state: MainShellState, *, direction: str) -> None:
        entry_ref = viewer_entry_ref_for_entry_write(state)
        if entry_ref is None:
            state.entry_panel_state.entry_write_error_message = "No hay entry en el visor para reordenar."
            return
        self._run_entry_write(
            state,
            lambda client: reorder_entry_within_week(
                client,
                entry_ref=entry_ref,
                direction=direction,
            ),
            reload_q5=entry_belongs_to_selected_week(state, entry_ref),
            reload_q8=True,
        )

    def _show_week_notes_dialog(self, state: MainShellState) -> None:
        target_week = selected_week_for_write(state)
        if target_week is None:
            state.entry_panel_state.week_write_error_message = "No hay week seleccionada para editar notas."
            return

        notes_field = ft.TextField(
            label=f"Notas week {target_week.week_number}",
            multiline=True,
            min_lines=4,
            max_lines=10,
            value=target_week.notes_preview or "",
            autofocus=True,
            expand=True,
        )

        def _submit(_e) -> None:
            notes_value = (notes_field.value or "").strip()
            self._close_dialog()
            self._run_week_write(
                state,
                lambda client, year_number, week_number: update_week_notes(
                    client,
                    year_number=year_number,
                    week_number=week_number,
                    notes=notes_value,
                ),
            )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar notas de week"),
            content=ft.Container(width=520, content=notes_field),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _e: self._close_dialog()),
                ft.FilledButton("Guardar", on_click=_submit),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._open_dialog(dialog)

    def _show_week_state_confirm_dialog(self, state: MainShellState, *, mode: str) -> None:
        target_week = selected_week_for_write(state)
        if target_week is None:
            label = "cerrar"
            if mode == "reopen":
                label = "reabrir"
            elif mode == "reclose":
                label = "re-cerrar"
            state.entry_panel_state.week_write_error_message = f"No hay week seleccionada para {label}."
            return

        if mode == "close":
            title = "Cerrar week"
            body = (
                f"Â¿Seguro que quieres cerrar la week {target_week.week_number}? "
                "Si hay una sesiÃ³n activa en esta week se auto-cerrarÃ¡."
            )
            confirm_label = "Cerrar"
            action = lambda client, year_number, week_number: close_week(
                client,
                year_number=year_number,
                week_number=week_number,
            )
        elif mode == "reopen":
            title = "Reabrir week"
            body = f"Â¿Seguro que quieres reabrir la week {target_week.week_number}?"
            confirm_label = "Reabrir"
            action = lambda client, year_number, week_number: reopen_week(
                client,
                year_number=year_number,
                week_number=week_number,
            )
        else:
            title = "Re-cerrar week"
            body = (
                f"Â¿Seguro que quieres re-cerrar la week {target_week.week_number}? "
                "Si hay una sesiÃ³n activa en esta week se auto-cerrarÃ¡."
            )
            confirm_label = "Re-cerrar"
            action = lambda client, year_number, week_number: reclose_week(
                client,
                year_number=year_number,
                week_number=week_number,
            )

        def _confirm(_e) -> None:
            self._close_dialog()
            result = self._run_week_write(state, action)
            if result is None:
                return
            if result.auto_stopped_session_id:
                self._show_snack_info(
                    f"Week actualizada. Se auto-cerrÃ³ la sesiÃ³n {result.auto_stopped_session_id}."
                )

        self._open_dialog(
            dialogs.build_confirm_dialog(
                title=title,
                body=body,
                confirm_label=confirm_label,
                on_confirm=_confirm,
                on_cancel=lambda _e: self._close_dialog(),
            )
        )

    def _get_extend_year_plus_one_target(self, state: MainShellState) -> tuple[int, int] | None:
        if not state.read_state.years:
            self._show_snack_error("No hay aÃ±os provisionados en la campaÃ±a.")
            return None
        selected_year = state.local_state.selected_year
        if selected_year is None or selected_year not in state.read_state.years:
            self._show_snack_error("No hay un aÃ±o vÃ¡lido seleccionado para extender la campaÃ±a.")
            return None
        last_year = max(state.read_state.years)
        if selected_year != last_year:
            self._show_snack_error("Solo se puede extender +1 aÃ±o desde el Ãºltimo aÃ±o provisionado.")
            return None
        return selected_year, (last_year + 1)

    def _show_extend_year_plus_one_confirm_dialog(self, state: MainShellState) -> None:
        target = self._get_extend_year_plus_one_target(state)
        if target is None:
            return
        current_year, next_year_number = target

        def _confirm(_e) -> None:
            self._close_dialog()
            result = self._run_campaign_write(state, lambda client: extend_years_plus_one(client))
            if result is None:
                return

            state.local_state.selected_year = result.new_year_number
            state.local_state.selected_week = None
            clear_all_write_errors(state)
            state.entry_panel_state.entries_for_selected_week = []
            state.entry_panel_state.entries_panel_error_message = None
            self._refresh_and_reload(
                state,
                selected_year_override=result.new_year_number,
                reload_q5=False,
                reload_q8=(state.local_state.viewer_entry_ref is not None),
            )
            self._show_snack_info(
                f"AÃ±o {result.new_year_number} aÃ±adido correctamente "
                f"(weeks {result.created_week_start}-{result.created_week_end})."
            )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Extender campaÃ±a (+1 aÃ±o)"),
            content=ft.Text(
                (
                    f"Vas a extender la campaÃ±a desde AÃ±o {current_year} a AÃ±o {next_year_number}.\n\n"
                    "Se aÃ±adirÃ¡ exactamente 1 aÃ±o completo (20 weeks) con confirmaciÃ³n explÃ­cita."
                )
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _e: self._close_dialog()),
                ft.FilledButton(
                    "Extender",
                    on_click=_confirm,
                    disabled=state.read_state.campaign_write_pending,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._open_dialog(dialog)

    def _show_resource_draft_leave_confirm_dialog(
        self,
        *,
        state: MainShellState,
        action_label: str,
        dispatch: Callable[[MainShellIntent], None],
    ) -> None:
        self._open_dialog(
            dialogs.build_resource_draft_leave_confirm_dialog(
                action_label=action_label,
                on_cancel=lambda _e: dispatch(ResourceDraftLeaveDialogCancelPressed()),
                on_discard=lambda _e: dispatch(ResourceDraftLeaveDialogDiscardPressed()),
                on_save=lambda _e: dispatch(ResourceDraftLeaveDialogSavePressed()),
                save_disabled=state.entry_panel_state.resource_write_pending,
            )
        )

    def _open_dialog(self, dialog: ft.AlertDialog) -> None:
        if self._active_dialog is not None:
            try:
                self._active_dialog.open = False
                self._active_dialog.update()
            except Exception:
                pass
            self._active_dialog = None
        self._page.show_dialog(dialog)
        self._active_dialog = dialog

    def _close_dialog(self) -> None:
        if self._active_dialog is None:
            return
        dialog = self._active_dialog
        self._active_dialog = None
        try:
            dialog.open = False
            dialog.update()
        except Exception:
            pass

    def _show_snack_error(self, message: str) -> None:
        self._page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor="#8A1F1F",
            open=True,
        )

    def _show_snack_info(self, message: str) -> None:
        self._page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            open=True,
        )

    def _show_entry_form_dialog(self, state: MainShellState, *, mode: str) -> None:
        if mode == "create":
            create_target = selected_week_target_for_entry_create(state)
            if create_target is None:
                state.entry_panel_state.entry_write_error_message = "No hay week seleccionada para crear una entry."
                return
            year_number, week_number = create_target
        else:
            year_number = None
            week_number = None

        entry_to_edit = state.entry_panel_state.viewer_entry_snapshot
        if mode == "edit":
            entry_ref = viewer_entry_ref_for_entry_write(state)
            if entry_ref is None:
                state.entry_panel_state.entry_write_error_message = "No hay entry en el visor para editar."
                return
            if entry_to_edit is None or entry_to_edit.ref != entry_ref:
                state.entry_panel_state.entry_write_error_message = (
                    "La entry visible no estÃ¡ cargada; refresca y reintenta."
                )
                return

        entry_type_field = ft.Dropdown(
            label="Tipo de entry",
            width=220,
            dense=True,
            value=(entry_to_edit.entry_type if entry_to_edit is not None else "scenario"),
            options=[
                ft.dropdown.Option("scenario"),
                ft.dropdown.Option("outpost"),
            ],
        )
        scenario_ref_field = ft.TextField(
            label="Scenario ref",
            hint_text="Entero positivo",
            width=180,
            dense=True,
            value=(
                str(entry_to_edit.scenario_ref)
                if entry_to_edit is not None and entry_to_edit.scenario_ref is not None
                else ""
            ),
        )
        dialog_error = ft.Text("", color="#8A1F1F", size=12, visible=False)

        def _apply_entry_type(_e=None) -> None:
            is_scenario = entry_type_field.value == "scenario"
            scenario_ref_field.disabled = not is_scenario
            scenario_ref_field.hint_text = "Entero positivo" if is_scenario else "No aplica para outpost"

        def _submit(_e) -> None:
            try:
                entry_type, scenario_ref = _parse_entry_form_values(
                    entry_type_value=entry_type_field.value,
                    scenario_ref_value=scenario_ref_field.value,
                )
            except ValueError as exc:
                dialog_error.value = str(exc)
                dialog_error.visible = True
                return

            if mode == "create":
                self._close_dialog()

                def _select_created_entry(result: EntryWriteResult) -> None:
                    if result.entry_ref is not None:
                        discard_resource_draft_for_context_change(state, show_notice=False)
                        state.local_state.viewer_entry_ref = result.entry_ref

                self._run_entry_write(
                    state,
                    lambda client: create_entry(
                        client,
                        year_number=year_number,  # type: ignore[arg-type]
                        week_number=week_number,  # type: ignore[arg-type]
                        entry_type=entry_type,
                        scenario_ref=scenario_ref,
                    ),
                    reload_q5=True,
                    reload_q8=True,
                    before_refresh=_select_created_entry,
                )
                return

            entry_ref = viewer_entry_ref_for_entry_write(state)
            if entry_ref is None:
                dialog_error.value = "No hay entry en el visor para editar."
                dialog_error.visible = True
                return

            self._close_dialog()
            self._run_entry_write(
                state,
                lambda client: update_entry(
                    client,
                    entry_ref=entry_ref,
                    entry_type=entry_type,
                    scenario_ref=scenario_ref,
                ),
                reload_q5=entry_belongs_to_selected_week(state, entry_ref),
                reload_q8=True,
            )

        title = "Crear entry" if mode == "create" else "Editar entry"
        submit_label = "Crear" if mode == "create" else "Guardar"
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Container(
                width=420,
                content=ft.Column(
                    tight=True,
                    spacing=8,
                    controls=[
                        entry_type_field,
                        scenario_ref_field,
                        dialog_error,
                    ],
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _e: self._close_dialog()),
                ft.FilledButton(submit_label, on_click=_submit),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._open_dialog(dialog)
        _apply_entry_type()

    def _show_entry_delete_confirm_dialog(self, state: MainShellState) -> None:
        entry_ref = viewer_entry_ref_for_entry_write(state)
        viewer_entry = state.entry_panel_state.viewer_entry_snapshot
        if entry_ref is None or viewer_entry is None or viewer_entry.ref != entry_ref:
            state.entry_panel_state.entry_write_error_message = "No hay entry en el visor para borrar."
            return
        entry_label = viewer_entry.label

        def _confirm(_e) -> None:
            self._close_dialog()

            def _clear_viewer_after_delete(_result: EntryWriteResult) -> None:
                state.local_state.viewer_entry_ref = None
                state.entry_panel_state.viewer_entry_snapshot = None
                state.entry_panel_state.viewer_sessions = []
                state.entry_panel_state.viewer_sessions_error_message = None
                clear_resource_draft_state(state)

            result = self._run_entry_write(
                state,
                lambda client: delete_entry(client, entry_ref=entry_ref),
                reload_q5=entry_belongs_to_selected_week(state, entry_ref),
                reload_q8=False,
                before_refresh=_clear_viewer_after_delete,
            )
            if result is not None and result.auto_stopped_session_id:
                self._show_snack_info(
                    f"Entry borrada. Se auto-cerrÃ³ la sesiÃ³n {result.auto_stopped_session_id}."
                )

        self._open_dialog(
            dialogs.build_confirm_dialog(
                title="Borrar entry",
                body=f"Â¿Seguro que quieres borrar la entry `{entry_label}`? Esta acciÃ³n es irreversible.",
                confirm_label="Borrar",
                on_confirm=_confirm,
                on_cancel=lambda _e: self._close_dialog(),
            )
        )

    def _show_session_form_dialog(
        self,
        *,
        state: MainShellState,
        mode: str,
        session_id: str | None,
    ) -> None:
        if state.local_state.viewer_entry_ref is None:
            state.entry_panel_state.session_write_error_message = (
                "No hay entry en el visor para gestionar sesiones."
            )
            return

        session_to_edit = None
        if mode == "edit":
            if not session_id:
                state.entry_panel_state.session_write_error_message = (
                    "La sesiÃ³n seleccionada ya no estÃ¡ visible en el visor."
                )
                return
            session_to_edit = _find_viewer_session_item(state.entry_panel_state.viewer_sessions, session_id)
            if session_to_edit is None:
                state.entry_panel_state.session_write_error_message = (
                    "La sesiÃ³n seleccionada ya no estÃ¡ visible en el visor."
                )
                return

        started_date_default, started_time_default = _to_local_strings(
            session_to_edit.started_at_utc if session_to_edit else None
        )
        ended_date_default, ended_time_default = _to_local_strings(
            session_to_edit.ended_at_utc if session_to_edit else None
        )
        active_default = bool(session_to_edit and session_to_edit.ended_at_utc is None)

        started_date_field = ft.TextField(label="Inicio (fecha local)", hint_text="YYYY-MM-DD", value=started_date_default, dense=True, width=180)
        started_time_field = ft.TextField(label="Inicio (hora local)", hint_text="HH:MM", value=started_time_default, dense=True, width=140)
        ended_date_field = ft.TextField(label="Fin (fecha local)", hint_text="YYYY-MM-DD", value=ended_date_default, dense=True, width=180)
        ended_time_field = ft.TextField(label="Fin (hora local)", hint_text="HH:MM", value=ended_time_default, dense=True, width=140)
        active_checkbox = ft.Checkbox(label="SesiÃ³n activa (sin fin)", value=active_default if mode == "edit" else False)
        dialog_error = ft.Text("", color="#8A1F1F", size=12, visible=False)

        def _apply_active_checkbox(_e=None) -> None:
            disable_end = bool(active_checkbox.value)
            ended_date_field.disabled = disable_end
            ended_time_field.disabled = disable_end

        def _submit(_e) -> None:
            try:
                started_at_utc = _parse_local_datetime(
                    started_date_field.value or "",
                    started_time_field.value or "",
                    field_label="Inicio",
                )
                if active_checkbox.value:
                    ended_at_utc = None
                else:
                    ended_at_utc = _parse_optional_local_datetime(
                        ended_date_field.value or "",
                        ended_time_field.value or "",
                        field_label="Fin",
                    )
                    if ended_at_utc is None:
                        raise ValueError("Fin: rellena fecha y hora o marca 'SesiÃ³n activa (sin fin)'.")
            except ValueError as exc:
                dialog_error.value = str(exc)
                dialog_error.visible = True
                return

            self._close_dialog()
            if mode == "create":
                self._run_session_write(
                    state,
                    lambda client, entry_ref: manual_create_session(
                        client,
                        entry_ref=entry_ref,
                        started_at_utc=started_at_utc,
                        ended_at_utc=ended_at_utc,
                    ),
                )
            elif session_to_edit is not None:
                self._run_session_write(
                    state,
                    lambda client, entry_ref: manual_update_session(
                        client,
                        entry_ref=entry_ref,
                        session_id=session_to_edit.session_id,
                        started_at_utc=started_at_utc,
                        ended_at_utc=ended_at_utc,
                    ),
                )

        title = "Crear sesiÃ³n manual" if mode == "create" else "Editar sesiÃ³n"
        submit_label = "Crear" if mode == "create" else "Guardar"
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Container(
                width=420,
                content=ft.Column(
                    tight=True,
                    spacing=8,
                    controls=[
                        ft.Row([started_date_field, started_time_field], spacing=8),
                        ft.Row([ended_date_field, ended_time_field], spacing=8),
                        active_checkbox,
                        dialog_error,
                    ],
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _e: self._close_dialog()),
                ft.FilledButton(submit_label, on_click=_submit),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._open_dialog(dialog)
        _apply_active_checkbox()

    def _show_delete_session_confirm_dialog(self, state: MainShellState, *, session_id: str) -> None:
        session = _find_viewer_session_item(state.entry_panel_state.viewer_sessions, session_id)
        if session is None:
            state.entry_panel_state.session_write_error_message = (
                "La sesiÃ³n seleccionada ya no estÃ¡ visible en el visor."
            )
            return

        def _confirm(_e) -> None:
            self._close_dialog()
            self._run_session_write(
                state,
                lambda client, entry_ref: manual_delete_session(
                    client,
                    entry_ref=entry_ref,
                    session_id=session_id,
                ),
            )

        self._open_dialog(
            dialogs.build_confirm_dialog(
                title="Borrar sesiÃ³n",
                body=f"Â¿Seguro que quieres borrar la sesiÃ³n `{session_id}`? Esta acciÃ³n es irreversible.",
                confirm_label="Borrar",
                on_confirm=_confirm,
                on_cancel=lambda _e: self._close_dialog(),
            )
        )


def _map_week_read_to_mock(week: WeekRead) -> MockWeek:
    is_closed = week.status == "closed"
    notes_preview = week.notes or ""
    return MockWeek(
        year_number=week.year_number,
        week_number=week.week_number,
        is_closed=is_closed,
        status_label=week.status,
        notes_preview=notes_preview,
    )


def _map_entry_read_to_mock(entry: EntryRead) -> MockEntry:
    return MockEntry(
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


def _find_entry_in_list(entries: list[MockEntry], entry_ref: EntryRef) -> MockEntry | None:
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
    if not isinstance(value, datetime):
        return "", ""
    dt = value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
    local_dt = dt.astimezone()
    return local_dt.strftime("%Y-%m-%d"), local_dt.strftime("%H:%M")


def _parse_local_datetime(date_value: str, time_value: str, *, field_label: str) -> datetime:
    date_clean = date_value.strip()
    time_clean = time_value.strip()
    if not date_clean or not time_clean:
        raise ValueError(f"{field_label}: fecha y hora son obligatorias.")
    try:
        naive = datetime.strptime(f"{date_clean} {time_clean}", "%Y-%m-%d %H:%M")
    except ValueError as exc:
        raise ValueError(f"{field_label}: usa formato YYYY-MM-DD y HH:MM.") from exc
    local_tz = datetime.now().astimezone().tzinfo
    if local_tz is None:
        raise ValueError("No se pudo resolver la zona horaria local.")
    local_dt = naive.replace(tzinfo=local_tz)
    return local_dt.astimezone(timezone.utc)


def _parse_optional_local_datetime(
    date_value: str,
    time_value: str,
    *,
    field_label: str,
) -> datetime | None:
    if not date_value.strip() and not time_value.strip():
        return None
    return _parse_local_datetime(date_value, time_value, field_label=field_label)


def _parse_entry_form_values(
    *,
    entry_type_value: str | None,
    scenario_ref_value: str | None,
) -> tuple[str, int | None]:
    entry_type = (entry_type_value or "").strip()
    if entry_type not in {"scenario", "outpost"}:
        raise ValueError("Tipo de entry invÃ¡lido. Usa `scenario` o `outpost`.")

    if entry_type == "outpost":
        return "outpost", None

    scenario_ref_raw = (scenario_ref_value or "").strip()
    if not scenario_ref_raw:
        raise ValueError("Scenario ref: es obligatorio para entries de tipo `scenario`.")
    try:
        scenario_ref = int(scenario_ref_raw)
    except ValueError as exc:
        raise ValueError("Scenario ref: debe ser un entero positivo.") from exc
    if scenario_ref <= 0:
        raise ValueError("Scenario ref: debe ser un entero positivo.")
    return "scenario", scenario_ref

