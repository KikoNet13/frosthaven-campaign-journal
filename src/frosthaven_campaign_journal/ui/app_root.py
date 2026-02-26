from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone

import flet as ft

from frosthaven_campaign_journal.config import load_settings
from frosthaven_campaign_journal.data import (
    EntryWriteResult,
    EntryRead,
    EntrySessionRead,
    FirestoreConfigError,
    FirestoreConflictError,
    FirestoreReadError,
    FirestoreTransitionInvalidError,
    FirestoreValidationError,
    FirestoreWriteError,
    ResourceBulkWriteResult,
    ResourceWriteResult,
    WeekRead,
    WeekWriteResult,
    build_firestore_client,
    close_week,
    create_entry,
    delete_entry,
    derive_year_from_week_cursor,
    load_main_screen_snapshot,
    manual_create_session,
    manual_delete_session,
    manual_update_session,
    reopen_week,
    read_entry_by_ref,
    read_q5_entries_for_selected_week,
    read_q8_sessions_for_entry,
    replace_entry_resource_deltas,
    reorder_entry_within_week,
    reclose_week,
    start_session,
    stop_session,
    update_entry,
    update_week_notes,
)
from frosthaven_campaign_journal.state.placeholders import (
    EntryRef,
    MainScreenLocalState,
    MockEntry,
    MockWeek,
    ViewerSessionItem,
    build_initial_main_screen_state,
)
from frosthaven_campaign_journal.ui.views import build_main_shell_view


@dataclass
class MainScreenReadState:
    status: str = "idle"
    error_message: str | None = None
    warning_message: str | None = None
    years: list[int] = field(default_factory=list)
    weeks_by_year: dict[int, list[MockWeek]] = field(default_factory=dict)
    campaign_week_cursor: int | None = None
    campaign_resource_totals: dict[str, int] | None = None
    active_entry_ref: EntryRef | None = None
    active_entry_label: str | None = None
    active_status_error_message: str | None = None


@dataclass
class EntryPanelReadState:
    entries_for_selected_week: list[MockEntry] = field(default_factory=list)
    entries_panel_error_message: str | None = None
    viewer_entry_snapshot: MockEntry | None = None
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
    resource_draft_discard_notice: str | None = None


def build_app_root(page: ft.Page) -> ft.Control:
    local_state = build_initial_main_screen_state()
    read_state = MainScreenReadState()
    entry_panel_state = EntryPanelReadState()

    shell_host = ft.Container(expand=True)
    safe_root = ft.SafeArea(expand=True, content=shell_host)
    root = ft.Container(expand=True, content=safe_root)
    active_dialog: ft.AlertDialog | None = None
    pending_resource_draft_context_action: Callable[[], None] | None = None
    pending_resource_draft_context_action_label: str | None = None
    resource_draft_leave_confirm_dialog_open = False

    def _sync_root_height_to_viewport() -> None:
        viewport_height = getattr(page, "height", None)
        if not isinstance(viewport_height, (int, float)) or viewport_height <= 0:
            viewport_height = 900
        root.height = viewport_height

    def current_weeks_for_selected_year() -> list[MockWeek]:
        if local_state.selected_year is None:
            return []
        return read_state.weeks_by_year.get(local_state.selected_year, [])

    def current_entries_for_selected_week() -> list[MockEntry]:
        if local_state.selected_week is None:
            return []
        return entry_panel_state.entries_for_selected_week

    def current_viewer_entry() -> MockEntry | None:
        return entry_panel_state.viewer_entry_snapshot

    def render_shell() -> None:
        _sync_root_height_to_viewport()
        shell_host.content = build_main_shell_view(
            state=local_state,
            years=read_state.years,
            weeks_for_selected_year=current_weeks_for_selected_year(),
            entries_for_selected_week=current_entries_for_selected_week(),
            viewer_entry=current_viewer_entry(),
            viewer_sessions=entry_panel_state.viewer_sessions,
            entries_panel_error_message=entry_panel_state.entries_panel_error_message,
            viewer_sessions_error_message=entry_panel_state.viewer_sessions_error_message,
            session_write_error_message=entry_panel_state.session_write_error_message,
            session_write_pending=entry_panel_state.session_write_pending,
            week_write_error_message=entry_panel_state.week_write_error_message,
            week_write_pending=entry_panel_state.week_write_pending,
            entry_write_error_message=entry_panel_state.entry_write_error_message,
            entry_write_pending=entry_panel_state.entry_write_pending,
            resource_write_error_message=entry_panel_state.resource_write_error_message,
            resource_write_pending=entry_panel_state.resource_write_pending,
            resource_draft_values=(
                dict(entry_panel_state.resource_draft_values)
                if _resource_draft_attached_to_viewer()
                else None
            ),
            resource_draft_dirty=entry_panel_state.resource_draft_dirty and _resource_draft_attached_to_viewer(),
            resource_draft_attached_to_viewer=_resource_draft_attached_to_viewer(),
            active_entry_ref=read_state.active_entry_ref,
            active_entry_label=read_state.active_entry_label,
            active_status_error_message=read_state.active_status_error_message,
            campaign_resource_totals=read_state.campaign_resource_totals,
            read_status=read_state.status,
            read_error_message=read_state.error_message,
            read_warning_message=read_state.warning_message,
            env_name=load_settings().env,
            on_prev_year=handle_prev_year,
            on_next_year=handle_next_year,
            on_select_week=handle_select_week,
            on_select_entry=handle_select_entry,
            on_manual_refresh=handle_manual_refresh,
            on_start_session=handle_start_session,
            on_stop_session=handle_stop_session,
            on_open_manual_create_session=handle_open_create_session_modal,
            on_open_manual_edit_session=handle_open_edit_session_modal,
            on_open_manual_delete_session=handle_open_delete_session_confirm,
            on_open_week_notes_modal=handle_open_week_notes_modal,
            on_request_close_week=handle_request_close_week,
            on_request_reopen_week=handle_request_reopen_week,
            on_request_reclose_week=handle_request_reclose_week,
            on_open_create_entry_modal=handle_open_create_entry_modal,
            on_open_edit_entry_modal=handle_open_edit_entry_modal,
            on_open_delete_entry_confirm=handle_open_delete_entry_confirm,
            on_reorder_entry_up=handle_reorder_entry_up,
            on_reorder_entry_down=handle_reorder_entry_down,
            on_adjust_resource_draft_delta=handle_adjust_resource_draft_delta,
            on_save_resource_draft=handle_save_resource_draft,
            on_discard_resource_draft=handle_discard_resource_draft,
        )

    def _build_client():
        settings = load_settings()
        return build_firestore_client(settings)

    def load_readonly_snapshot(*, selected_year_override: int | None) -> bool:
        try:
            client = _build_client()
            snapshot = load_main_screen_snapshot(
                client,
                selected_year=selected_year_override,
                viewer_entry_ref=local_state.viewer_entry_ref,
            )
        except (FirestoreConfigError, FirestoreReadError) as exc:
            read_state.status = "error"
            read_state.error_message = str(exc)
            read_state.warning_message = None
            return False

        read_state.status = "ready"
        read_state.error_message = None
        read_state.years = snapshot.years
        read_state.campaign_week_cursor = snapshot.campaign_main.week_cursor
        read_state.campaign_resource_totals = snapshot.campaign_main.resource_totals
        read_state.weeks_by_year[snapshot.effective_year] = [
            _map_week_read_to_mock(week)
            for week in snapshot.weeks_for_selected_year
        ]

        local_state.selected_year = snapshot.effective_year

        visible_week_numbers = {
            week.week_number for week in read_state.weeks_by_year[snapshot.effective_year]
        }
        if local_state.selected_week is not None and local_state.selected_week not in visible_week_numbers:
            local_state.selected_week = None

        derived_year = derive_year_from_week_cursor(snapshot.campaign_main.week_cursor)
        if derived_year not in snapshot.years:
            read_state.warning_message = (
                "Advertencia: `week_cursor` apunta a un año no provisionado. "
                f"Se usa Año {snapshot.effective_year} como fallback de navegación."
            )
        else:
            read_state.warning_message = None

        if snapshot.active_entry is None:
            read_state.active_entry_ref = None
            read_state.active_entry_label = None
        else:
            read_state.active_entry_ref = snapshot.active_entry.entry_ref
            read_state.active_entry_label = snapshot.active_entry.label
        read_state.active_status_error_message = snapshot.active_status_error_message

        return True

    def load_entries_for_selected_week() -> None:
        if local_state.selected_year is None or local_state.selected_week is None:
            entry_panel_state.entries_for_selected_week = []
            entry_panel_state.entries_panel_error_message = None
            return

        try:
            client = _build_client()
            entries = read_q5_entries_for_selected_week(
                client,
                year_number=local_state.selected_year,
                week_number=local_state.selected_week,
            )
        except (FirestoreConfigError, FirestoreReadError) as exc:
            entry_panel_state.entries_for_selected_week = []
            entry_panel_state.entries_panel_error_message = str(exc)
            return

        entry_panel_state.entries_for_selected_week = [_map_entry_read_to_mock(entry) for entry in entries]
        entry_panel_state.entries_panel_error_message = None

        # Reconciliar snapshot del visor si la entry visible pertenece a la week cargada.
        if local_state.viewer_entry_ref is None:
            return

        if not _entry_ref_matches_selected_week(local_state, local_state.viewer_entry_ref):
            return

        updated_entry = _find_entry_in_list(
            entry_panel_state.entries_for_selected_week,
            local_state.viewer_entry_ref,
        )
        if updated_entry is not None:
            entry_panel_state.viewer_entry_snapshot = updated_entry
            _sync_resource_draft_from_viewer_snapshot()

    def load_viewer_entry_and_sessions() -> None:
        if local_state.viewer_entry_ref is None:
            entry_panel_state.viewer_entry_snapshot = None
            entry_panel_state.viewer_sessions = []
            entry_panel_state.viewer_sessions_error_message = None
            _clear_resource_draft_state()
            return

        try:
            client = _build_client()
            viewer_entry_read = read_entry_by_ref(client, local_state.viewer_entry_ref)
        except (FirestoreConfigError, FirestoreReadError) as exc:
            entry_panel_state.viewer_sessions_error_message = str(exc)
            entry_panel_state.viewer_sessions = []
            if (
                entry_panel_state.viewer_entry_snapshot is not None
                and entry_panel_state.viewer_entry_snapshot.ref != local_state.viewer_entry_ref
            ):
                entry_panel_state.viewer_entry_snapshot = None
            return

        entry_panel_state.viewer_entry_snapshot = _map_entry_read_to_mock(viewer_entry_read)
        _sync_resource_draft_from_viewer_snapshot()

        try:
            sessions = read_q8_sessions_for_entry(client, entry_ref=local_state.viewer_entry_ref)
        except FirestoreReadError as exc:
            entry_panel_state.viewer_sessions = []
            entry_panel_state.viewer_sessions_error_message = str(exc)
            return

        entry_panel_state.viewer_sessions = [
            _map_session_read_to_viewer_session(session) for session in sessions
        ]
        entry_panel_state.viewer_sessions_error_message = None

    def refresh_and_render(
        *,
        selected_year_override: int | None,
        reload_q5: bool = False,
        reload_q8: bool = False,
    ) -> None:
        load_readonly_snapshot(selected_year_override=selected_year_override)
        if reload_q5:
            load_entries_for_selected_week()
        if reload_q8:
            load_viewer_entry_and_sessions()
        render_shell()
        page.update()

    def handle_prev_year() -> None:
        if local_state.selected_year is None or local_state.selected_year not in read_state.years:
            return
        current_index = read_state.years.index(local_state.selected_year)
        if current_index <= 0:
            return
        target_year = read_state.years[current_index - 1]

        def _continue() -> None:
            local_state.selected_year = target_year
            local_state.selected_week = None
            _clear_session_write_error()
            _clear_week_write_error()
            _clear_entry_write_error()
            _clear_resource_write_error()
            entry_panel_state.entries_for_selected_week = []
            entry_panel_state.entries_panel_error_message = None
            refresh_and_render(selected_year_override=local_state.selected_year, reload_q8=False)

        _run_or_confirm_resource_draft_before_context_change(
            _continue,
            action_label="cambiar de año",
        )

    def handle_next_year() -> None:
        if local_state.selected_year is None or local_state.selected_year not in read_state.years:
            return
        current_index = read_state.years.index(local_state.selected_year)
        if current_index >= len(read_state.years) - 1:
            return
        target_year = read_state.years[current_index + 1]

        def _continue() -> None:
            local_state.selected_year = target_year
            local_state.selected_week = None
            _clear_session_write_error()
            _clear_week_write_error()
            _clear_entry_write_error()
            _clear_resource_write_error()
            entry_panel_state.entries_for_selected_week = []
            entry_panel_state.entries_panel_error_message = None
            refresh_and_render(selected_year_override=local_state.selected_year, reload_q8=False)

        _run_or_confirm_resource_draft_before_context_change(
            _continue,
            action_label="cambiar de año",
        )

    def handle_select_week(week_number: int) -> None:
        if local_state.selected_year is None:
            return
        visible_weeks = current_weeks_for_selected_year()
        if not any(week.week_number == week_number for week in visible_weeks):
            return

        def _continue() -> None:
            local_state.selected_week = week_number
            _clear_session_write_error()
            _clear_week_write_error()
            _clear_entry_write_error()
            _clear_resource_write_error()
            load_entries_for_selected_week()  # Q5 solo, el visor sticky no recarga Q8 por navegación
            render_shell()
            page.update()

        _run_or_confirm_resource_draft_before_context_change(
            _continue,
            action_label="cambiar de week",
        )

    def handle_select_entry(entry_ref: EntryRef) -> None:
        def _continue() -> None:
            local_state.viewer_entry_ref = entry_ref
            _clear_session_write_error()
            _clear_week_write_error()
            _clear_entry_write_error()
            _clear_resource_write_error()
            load_viewer_entry_and_sessions()  # Q8 sigue al visor sticky
            render_shell()
            page.update()

        _run_or_confirm_resource_draft_before_context_change(
            _continue,
            action_label="cambiar de entry",
        )

    def handle_manual_refresh() -> None:
        def _continue() -> None:
            _clear_session_write_error()
            _clear_week_write_error()
            _clear_entry_write_error()
            _clear_resource_write_error()
            refresh_and_render(
                selected_year_override=local_state.selected_year,
                reload_q5=(local_state.selected_week is not None),
                reload_q8=(local_state.viewer_entry_ref is not None),
            )

        _run_or_confirm_resource_draft_before_context_change(
            _continue,
            action_label="refrescar",
        )

    def _clear_session_write_error() -> None:
        entry_panel_state.session_write_error_message = None

    def _set_session_write_error(message: str) -> None:
        entry_panel_state.session_write_error_message = message

    def _clear_week_write_error() -> None:
        entry_panel_state.week_write_error_message = None

    def _set_week_write_error(message: str) -> None:
        entry_panel_state.week_write_error_message = message

    def _clear_entry_write_error() -> None:
        entry_panel_state.entry_write_error_message = None

    def _set_entry_write_error(message: str) -> None:
        entry_panel_state.entry_write_error_message = message

    def _clear_resource_write_error() -> None:
        entry_panel_state.resource_write_error_message = None

    def _set_resource_write_error(message: str) -> None:
        entry_panel_state.resource_write_error_message = message

    def _normalize_resource_draft_values(raw_map: dict[str, int] | None) -> dict[str, int]:
        if not isinstance(raw_map, dict):
            return {}
        normalized: dict[str, int] = {}
        for key in ("lumber", "metal", "hide"):
            value = raw_map.get(key)
            if isinstance(value, bool) or not isinstance(value, int):
                continue
            if value == 0:
                continue
            normalized[key] = value
        return normalized

    def _clear_resource_draft_state() -> None:
        entry_panel_state.resource_draft_entry_ref = None
        entry_panel_state.resource_draft_values = {}
        entry_panel_state.resource_draft_dirty = False
        entry_panel_state.resource_draft_discard_notice = None

    def _resource_draft_attached_to_viewer() -> bool:
        return (
            local_state.viewer_entry_ref is not None
            and entry_panel_state.resource_draft_entry_ref == local_state.viewer_entry_ref
        )

    def _has_dirty_resource_draft_attached_to_viewer() -> bool:
        return _resource_draft_attached_to_viewer() and entry_panel_state.resource_draft_dirty

    def _sync_resource_draft_from_viewer_snapshot() -> None:
        viewer_entry = entry_panel_state.viewer_entry_snapshot
        if viewer_entry is None:
            return

        normalized_viewer_deltas = _normalize_resource_draft_values(viewer_entry.resource_deltas)
        if entry_panel_state.resource_draft_entry_ref != viewer_entry.ref:
            entry_panel_state.resource_draft_entry_ref = viewer_entry.ref
            entry_panel_state.resource_draft_values = normalized_viewer_deltas
            entry_panel_state.resource_draft_dirty = False
            entry_panel_state.resource_draft_discard_notice = None
            return

        if not entry_panel_state.resource_draft_dirty:
            entry_panel_state.resource_draft_values = normalized_viewer_deltas

    def _discard_resource_draft_for_context_change(*, show_notice: bool) -> None:
        had_dirty = entry_panel_state.resource_draft_dirty
        _clear_resource_draft_state()
        _clear_resource_write_error()
        if show_notice and had_dirty:
            entry_panel_state.resource_draft_discard_notice = (
                "Cambios de recursos sin guardar descartados al cambiar de contexto."
            )
            _show_snack_info(entry_panel_state.resource_draft_discard_notice, update_page=False)

    def _auto_discard_resource_draft_on_context_change() -> None:
        _discard_resource_draft_for_context_change(show_notice=True)

    def _clear_pending_resource_draft_context_action() -> None:
        nonlocal pending_resource_draft_context_action
        nonlocal pending_resource_draft_context_action_label
        pending_resource_draft_context_action = None
        pending_resource_draft_context_action_label = None

    def _queue_resource_draft_context_action(
        action: Callable[[], None],
        *,
        action_label: str | None,
    ) -> None:
        nonlocal pending_resource_draft_context_action
        nonlocal pending_resource_draft_context_action_label
        pending_resource_draft_context_action = action
        pending_resource_draft_context_action_label = action_label

    def _take_pending_resource_draft_context_action() -> Callable[[], None] | None:
        nonlocal pending_resource_draft_context_action
        nonlocal pending_resource_draft_context_action_label
        action = pending_resource_draft_context_action
        pending_resource_draft_context_action = None
        pending_resource_draft_context_action_label = None
        return action

    def _close_resource_draft_leave_confirm_dialog(*, clear_pending_action: bool) -> None:
        nonlocal resource_draft_leave_confirm_dialog_open
        resource_draft_leave_confirm_dialog_open = False
        _close_dialog()
        if clear_pending_action:
            _clear_pending_resource_draft_context_action()

    def _run_pending_resource_draft_context_action() -> None:
        pending_action = _take_pending_resource_draft_context_action()
        if pending_action is None:
            return
        pending_action()

    def _open_resource_draft_leave_confirm_dialog() -> None:
        nonlocal resource_draft_leave_confirm_dialog_open
        if resource_draft_leave_confirm_dialog_open:
            return
        resource_draft_leave_confirm_dialog_open = True

        if pending_resource_draft_context_action_label:
            body_text = (
                "Hay cambios de recursos sin guardar en la entry visible. "
                f"¿Qué quieres hacer antes de {pending_resource_draft_context_action_label}?"
            )
        else:
            body_text = (
                "Hay cambios de recursos sin guardar en la entry visible. "
                "¿Qué quieres hacer antes de continuar?"
            )

        def _handle_cancel(_e) -> None:
            _close_resource_draft_leave_confirm_dialog(clear_pending_action=True)

        def _handle_discard(_e) -> None:
            _close_resource_draft_leave_confirm_dialog(clear_pending_action=False)
            _discard_resource_draft_for_context_change(show_notice=False)
            _run_pending_resource_draft_context_action()

        def _handle_save(_e) -> None:
            _close_resource_draft_leave_confirm_dialog(clear_pending_action=False)
            result = _run_resource_draft_save()
            if result is None:
                _clear_pending_resource_draft_context_action()
                return
            _run_pending_resource_draft_context_action()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Cambios de recursos sin guardar"),
            content=ft.Text(body_text),
            actions=[
                ft.TextButton("Cancelar", on_click=_handle_cancel),
                ft.OutlinedButton(
                    "Descartar",
                    on_click=_handle_discard,
                    disabled=entry_panel_state.resource_write_pending,
                ),
                ft.FilledButton(
                    "Guardar",
                    on_click=_handle_save,
                    disabled=entry_panel_state.resource_write_pending,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        _open_dialog(dialog)

    def _run_or_confirm_resource_draft_before_context_change(
        action: Callable[[], None],
        *,
        action_label: str | None,
    ) -> None:
        if not _has_dirty_resource_draft_attached_to_viewer():
            action()
            return
        if resource_draft_leave_confirm_dialog_open:
            return
        _queue_resource_draft_context_action(action, action_label=action_label)
        _open_resource_draft_leave_confirm_dialog()

    def _get_selected_week_for_write() -> MockWeek | None:
        if local_state.selected_week is None:
            return None
        for week in current_weeks_for_selected_year():
            if week.week_number == local_state.selected_week:
                return week
        return None

    def _viewer_matches_week(year_number: int, week_number: int) -> bool:
        return (
            local_state.viewer_entry_ref is not None
            and local_state.viewer_entry_ref.year_number == year_number
            and local_state.viewer_entry_ref.week_number == week_number
        )

    def _get_selected_week_target_for_entry_create() -> tuple[int, int] | None:
        target_week = _get_selected_week_for_write()
        if local_state.selected_year is None or local_state.selected_week is None or target_week is None:
            return None
        return local_state.selected_year, local_state.selected_week

    def _get_viewer_entry_ref_for_entry_write() -> EntryRef | None:
        return local_state.viewer_entry_ref

    def _get_viewer_entry_ref_for_resource_write() -> EntryRef | None:
        return local_state.viewer_entry_ref

    def _run_week_write(action) -> WeekWriteResult | None:
        target_week = _get_selected_week_for_write()
        if local_state.selected_year is None or local_state.selected_week is None or target_week is None:
            _set_week_write_error("No hay week seleccionada para ejecutar la acción.")
            render_shell()
            page.update()
            return None

        year_number = local_state.selected_year
        week_number = local_state.selected_week

        entry_panel_state.week_write_pending = True
        _clear_week_write_error()
        render_shell()
        page.update()

        result: WeekWriteResult | None = None
        success = True
        try:
            client = _build_client()
            result = action(client, year_number, week_number)
        except FirestoreConflictError as exc:
            _set_week_write_error(str(exc))
            success = False
        except (
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreReadError,
            FirestoreWriteError,
        ) as exc:
            _set_week_write_error(str(exc))
            success = False
        finally:
            entry_panel_state.week_write_pending = False

        if not success:
            render_shell()
            page.update()
            return None

        refresh_and_render(
            selected_year_override=local_state.selected_year,
            reload_q5=False,
            reload_q8=_viewer_matches_week(year_number, week_number),
        )
        return result

    def _run_session_write(action) -> bool:
        if local_state.viewer_entry_ref is None:
            _set_session_write_error("No hay entry en el visor para ejecutar la acción de sesión.")
            render_shell()
            page.update()
            return False

        entry_panel_state.session_write_pending = True
        _clear_session_write_error()
        render_shell()
        page.update()
        success = True

        try:
            client = _build_client()
            action(client, local_state.viewer_entry_ref)
        except FirestoreConflictError as exc:
            _set_session_write_error(str(exc))
            success = False
        except (FirestoreTransitionInvalidError, FirestoreValidationError, FirestoreReadError) as exc:
            _set_session_write_error(str(exc))
            success = False
        finally:
            entry_panel_state.session_write_pending = False

        if not success:
            render_shell()
            page.update()
            return False

        refresh_and_render(
            selected_year_override=local_state.selected_year,
            reload_q5=False,
            reload_q8=(local_state.viewer_entry_ref is not None),
        )
        return True

    def _run_entry_write(
        action,
        *,
        reload_q5: bool,
        reload_q8: bool,
        before_refresh=None,
    ) -> EntryWriteResult | None:
        entry_panel_state.entry_write_pending = True
        _clear_entry_write_error()
        render_shell()
        page.update()

        result: EntryWriteResult | None = None
        success = True
        try:
            client = _build_client()
            result = action(client)
        except FirestoreConflictError as exc:
            _set_entry_write_error(str(exc))
            success = False
        except (
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreReadError,
            FirestoreWriteError,
        ) as exc:
            _set_entry_write_error(str(exc))
            success = False
        finally:
            entry_panel_state.entry_write_pending = False

        if not success:
            render_shell()
            page.update()
            return None

        if before_refresh is not None and result is not None:
            before_refresh(result)

        refresh_and_render(
            selected_year_override=local_state.selected_year,
            reload_q5=reload_q5,
            reload_q8=reload_q8,
        )
        return result

    def _run_resource_write(action) -> ResourceWriteResult | None:
        entry_ref = _get_viewer_entry_ref_for_resource_write()
        if entry_ref is None:
            _set_resource_write_error("No hay entry en el visor para ajustar recursos.")
            render_shell()
            page.update()
            return None

        reload_q5 = _entry_ref_matches_selected_week(local_state, entry_ref)

        entry_panel_state.resource_write_pending = True
        _clear_resource_write_error()
        render_shell()
        page.update()

        result: ResourceWriteResult | None = None
        success = True
        try:
            client = _build_client()
            result = action(client, entry_ref)
        except FirestoreConflictError as exc:
            _set_resource_write_error(str(exc))
            success = False
        except (
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreReadError,
            FirestoreWriteError,
        ) as exc:
            _set_resource_write_error(str(exc))
            success = False
        finally:
            entry_panel_state.resource_write_pending = False

        if not success:
            render_shell()
            page.update()
            return None

        refresh_and_render(
            selected_year_override=local_state.selected_year,
            reload_q5=reload_q5,
            reload_q8=(local_state.viewer_entry_ref is not None),
        )
        return result

    def _run_resource_draft_save() -> ResourceBulkWriteResult | None:
        entry_ref = _get_viewer_entry_ref_for_resource_write()
        if entry_ref is None:
            _set_resource_write_error("No hay entry en el visor para guardar recursos.")
            render_shell()
            page.update()
            return None

        if entry_panel_state.resource_draft_entry_ref != entry_ref:
            _set_resource_write_error(
                "El borrador de recursos no coincide con la entry visible; refresca y reintenta."
            )
            render_shell()
            page.update()
            return None

        reload_q5 = _entry_ref_matches_selected_week(local_state, entry_ref)
        target_resource_deltas = dict(entry_panel_state.resource_draft_values)

        entry_panel_state.resource_write_pending = True
        _clear_resource_write_error()
        render_shell()
        page.update()

        result: ResourceBulkWriteResult | None = None
        success = True
        try:
            client = _build_client()
            result = replace_entry_resource_deltas(
                client,
                entry_ref=entry_ref,
                target_resource_deltas=target_resource_deltas,
            )
        except FirestoreConflictError as exc:
            _set_resource_write_error(str(exc))
            success = False
        except (
            FirestoreTransitionInvalidError,
            FirestoreValidationError,
            FirestoreReadError,
            FirestoreWriteError,
        ) as exc:
            _set_resource_write_error(str(exc))
            success = False
        finally:
            entry_panel_state.resource_write_pending = False

        if not success:
            render_shell()
            page.update()
            return None

        entry_panel_state.resource_draft_dirty = False
        entry_panel_state.resource_draft_discard_notice = None

        if result is not None and result.no_op:
            render_shell()
            page.update()
            return result

        refresh_and_render(
            selected_year_override=local_state.selected_year,
            reload_q5=reload_q5,
            reload_q8=(local_state.viewer_entry_ref is not None),
        )
        return result

    def handle_start_session() -> None:
        _run_session_write(lambda client, entry_ref: start_session(client, entry_ref=entry_ref))

    def handle_stop_session() -> None:
        _run_session_write(lambda client, entry_ref: stop_session(client, entry_ref=entry_ref))

    def _show_week_notes_modal() -> None:
        target_week = _get_selected_week_for_write()
        if target_week is None:
            _set_week_write_error("No hay week seleccionada para editar notas.")
            render_shell()
            page.update()
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
            _close_dialog()
            _run_week_write(
                lambda client, year_number, week_number: update_week_notes(
                    client,
                    year_number=year_number,
                    week_number=week_number,
                    notes=notes_value,
                )
            )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar notas de week"),
            content=ft.Container(width=520, content=notes_field),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _e: _close_dialog()),
                ft.FilledButton("Guardar", on_click=_submit),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        _open_dialog(dialog)

    def _show_week_state_confirm_dialog(
        *,
        title: str,
        body: str,
        confirm_label: str,
        action,
    ) -> None:
        def _confirm(_e) -> None:
            _close_dialog()
            result = _run_week_write(action)
            if result is None:
                return
            if result.auto_stopped_session_id:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(
                        f"Week actualizada. Se auto-cerró la sesión {result.auto_stopped_session_id}."
                    ),
                    open=True,
                )
                page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(body),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _e: _close_dialog()),
                ft.FilledButton(confirm_label, on_click=_confirm),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        _open_dialog(dialog)

    def handle_open_week_notes_modal() -> None:
        _show_week_notes_modal()

    def handle_request_close_week() -> None:
        target_week = _get_selected_week_for_write()
        if target_week is None:
            _set_week_write_error("No hay week seleccionada para cerrar.")
            render_shell()
            page.update()
            return
        _show_week_state_confirm_dialog(
            title="Cerrar week",
            body=(
                f"¿Seguro que quieres cerrar la week {target_week.week_number}? "
                "Si hay una sesión activa en esta week se auto-cerrará."
            ),
            confirm_label="Cerrar",
            action=lambda client, year_number, week_number: close_week(
                client,
                year_number=year_number,
                week_number=week_number,
            ),
        )

    def handle_request_reopen_week() -> None:
        target_week = _get_selected_week_for_write()
        if target_week is None:
            _set_week_write_error("No hay week seleccionada para reabrir.")
            render_shell()
            page.update()
            return
        _show_week_state_confirm_dialog(
            title="Reabrir week",
            body=f"¿Seguro que quieres reabrir la week {target_week.week_number}?",
            confirm_label="Reabrir",
            action=lambda client, year_number, week_number: reopen_week(
                client,
                year_number=year_number,
                week_number=week_number,
            ),
        )

    def handle_request_reclose_week() -> None:
        target_week = _get_selected_week_for_write()
        if target_week is None:
            _set_week_write_error("No hay week seleccionada para re-cerrar.")
            render_shell()
            page.update()
            return
        _show_week_state_confirm_dialog(
            title="Re-cerrar week",
            body=(
                f"¿Seguro que quieres re-cerrar la week {target_week.week_number}? "
                "Si hay una sesión activa en esta week se auto-cerrará."
            ),
            confirm_label="Re-cerrar",
            action=lambda client, year_number, week_number: reclose_week(
                client,
                year_number=year_number,
                week_number=week_number,
            ),
        )

    def _open_dialog(dialog: ft.AlertDialog) -> None:
        nonlocal active_dialog
        if active_dialog is not None:
            try:
                active_dialog.open = False
                active_dialog.update()
            except Exception:
                pass
            active_dialog = None
        page.show_dialog(dialog)
        active_dialog = dialog

    def _close_dialog() -> None:
        nonlocal active_dialog
        if active_dialog is None:
            return
        dialog = active_dialog
        active_dialog = None
        try:
            dialog.open = False
            dialog.update()
        except Exception:
            page.update()

    def _show_snack_error(message: str) -> None:
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor="#8A1F1F",
            open=True,
        )
        page.update()

    def _show_snack_info(message: str, *, update_page: bool = True) -> None:
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            open=True,
        )
        if update_page:
            page.update()

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
            raise ValueError("Tipo de entry inválido. Usa `scenario` o `outpost`.")

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

    def _show_entry_form_dialog(
        *,
        mode: str,
        entry_to_edit: MockEntry | None = None,
    ) -> None:
        if mode == "create" and _get_selected_week_target_for_entry_create() is None:
            _set_entry_write_error("No hay week seleccionada para crear una entry.")
            render_shell()
            page.update()
            return

        if mode == "edit":
            entry_ref = _get_viewer_entry_ref_for_entry_write()
            if entry_ref is None:
                _set_entry_write_error("No hay entry en el visor para editar.")
                render_shell()
                page.update()
                return
            if entry_to_edit is None or entry_to_edit.ref != entry_ref:
                _set_entry_write_error("La entry visible no está cargada; refresca y reintenta.")
                render_shell()
                page.update()
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
            if not is_scenario:
                scenario_ref_field.hint_text = "No aplica para outpost"
            else:
                scenario_ref_field.hint_text = "Entero positivo"
            page.update()

        entry_type_field.on_change = _apply_entry_type

        def _submit(_e) -> None:
            try:
                entry_type, scenario_ref = _parse_entry_form_values(
                    entry_type_value=entry_type_field.value,
                    scenario_ref_value=scenario_ref_field.value,
                )
            except ValueError as exc:
                dialog_error.value = str(exc)
                dialog_error.visible = True
                page.update()
                return

            if mode == "create":
                create_target = _get_selected_week_target_for_entry_create()
                if create_target is None:
                    dialog_error.value = "No hay week seleccionada para crear una entry."
                    dialog_error.visible = True
                    page.update()
                    return
                year_number, week_number = create_target
                _close_dialog()

                def _select_created_entry(result: EntryWriteResult) -> None:
                    if result.entry_ref is not None:
                        _auto_discard_resource_draft_on_context_change()
                        local_state.viewer_entry_ref = result.entry_ref

                _run_entry_write(
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
                )
                return

            entry_ref = _get_viewer_entry_ref_for_entry_write()
            if entry_ref is None:
                dialog_error.value = "No hay entry en el visor para editar."
                dialog_error.visible = True
                page.update()
                return

            reload_q5 = _entry_ref_matches_selected_week(local_state, entry_ref)
            _close_dialog()
            _run_entry_write(
                lambda client: update_entry(
                    client,
                    entry_ref=entry_ref,
                    entry_type=entry_type,
                    scenario_ref=scenario_ref,
                ),
                reload_q5=reload_q5,
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
                ft.TextButton("Cancelar", on_click=lambda _e: _close_dialog()),
                ft.FilledButton(submit_label, on_click=_submit),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        _open_dialog(dialog)
        _apply_entry_type()

    def handle_open_create_entry_modal() -> None:
        _show_entry_form_dialog(mode="create")

    def handle_open_edit_entry_modal() -> None:
        viewer_entry = entry_panel_state.viewer_entry_snapshot
        entry_ref = _get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            _set_entry_write_error("No hay entry en el visor para editar.")
            render_shell()
            page.update()
            return
        if viewer_entry is None or viewer_entry.ref != entry_ref:
            _set_entry_write_error("La entry visible no está cargada; refresca y reintenta.")
            render_shell()
            page.update()
            return
        _show_entry_form_dialog(mode="edit", entry_to_edit=viewer_entry)

    def handle_open_delete_entry_confirm() -> None:
        entry_ref = _get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            _set_entry_write_error("No hay entry en el visor para borrar.")
            render_shell()
            page.update()
            return

        viewer_entry = entry_panel_state.viewer_entry_snapshot
        if viewer_entry is None or viewer_entry.ref != entry_ref:
            _set_entry_write_error("La entry visible no está cargada; refresca y reintenta.")
            render_shell()
            page.update()
            return

        entry_label = viewer_entry.label
        reload_q5 = _entry_ref_matches_selected_week(local_state, entry_ref)

        def _confirm(_e) -> None:
            _close_dialog()

            def _clear_viewer_after_delete(_result: EntryWriteResult) -> None:
                local_state.viewer_entry_ref = None
                entry_panel_state.viewer_entry_snapshot = None
                entry_panel_state.viewer_sessions = []
                entry_panel_state.viewer_sessions_error_message = None
                _clear_resource_draft_state()

            result = _run_entry_write(
                lambda client: delete_entry(client, entry_ref=entry_ref),
                reload_q5=reload_q5,
                reload_q8=False,
                before_refresh=_clear_viewer_after_delete,
            )
            if result is None:
                return
            if result.auto_stopped_session_id:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(
                        f"Entry borrada. Se auto-cerró la sesión {result.auto_stopped_session_id}."
                    ),
                    open=True,
                )
                page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Borrar entry"),
            content=ft.Text(
                f"¿Seguro que quieres borrar la entry `{entry_label}`? Esta acción es irreversible."
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _e: _close_dialog()),
                ft.FilledButton("Borrar", on_click=_confirm),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        _open_dialog(dialog)

    def handle_reorder_entry_up() -> None:
        entry_ref = _get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            _set_entry_write_error("No hay entry en el visor para reordenar.")
            render_shell()
            page.update()
            return
        _run_entry_write(
            lambda client: reorder_entry_within_week(
                client,
                entry_ref=entry_ref,
                direction="up",
            ),
            reload_q5=_entry_ref_matches_selected_week(local_state, entry_ref),
            reload_q8=True,
        )

    def handle_reorder_entry_down() -> None:
        entry_ref = _get_viewer_entry_ref_for_entry_write()
        if entry_ref is None:
            _set_entry_write_error("No hay entry en el visor para reordenar.")
            render_shell()
            page.update()
            return
        _run_entry_write(
            lambda client: reorder_entry_within_week(
                client,
                entry_ref=entry_ref,
                direction="down",
            ),
            reload_q5=_entry_ref_matches_selected_week(local_state, entry_ref),
            reload_q8=True,
        )

    def handle_adjust_resource_draft_delta(resource_key: str, adjustment_delta: int) -> None:
        entry_ref = _get_viewer_entry_ref_for_resource_write()
        if entry_ref is None:
            _set_resource_write_error("No hay entry en el visor para ajustar recursos.")
            render_shell()
            page.update()
            return
        if entry_panel_state.resource_draft_entry_ref != entry_ref:
            _set_resource_write_error(
                "El borrador de recursos no coincide con la entry visible; refresca y reintenta."
            )
            render_shell()
            page.update()
            return
        if resource_key not in {"lumber", "metal", "hide"}:
            _set_resource_write_error(f"Recurso no soportado: {resource_key!r}.")
            render_shell()
            page.update()
            return
        if isinstance(adjustment_delta, bool) or not isinstance(adjustment_delta, int) or adjustment_delta == 0:
            _set_resource_write_error("El ajuste de recurso debe ser entero distinto de 0.")
            render_shell()
            page.update()
            return

        current_value = entry_panel_state.resource_draft_values.get(resource_key, 0)
        next_value = current_value + adjustment_delta
        if next_value == 0:
            entry_panel_state.resource_draft_values.pop(resource_key, None)
        else:
            entry_panel_state.resource_draft_values[resource_key] = next_value

        entry_panel_state.resource_draft_dirty = True
        entry_panel_state.resource_draft_discard_notice = None
        _clear_resource_write_error()
        render_shell()
        page.update()

    def handle_save_resource_draft() -> None:
        entry_ref = _get_viewer_entry_ref_for_resource_write()
        if entry_ref is None:
            _set_resource_write_error("No hay entry en el visor para guardar recursos.")
            render_shell()
            page.update()
            return
        if entry_panel_state.resource_draft_entry_ref != entry_ref:
            _set_resource_write_error(
                "El borrador de recursos no coincide con la entry visible; refresca y reintenta."
            )
            render_shell()
            page.update()
            return
        if not entry_panel_state.resource_draft_dirty:
            return
        _run_resource_draft_save()

    def handle_discard_resource_draft() -> None:
        _clear_pending_resource_draft_context_action()
        viewer_entry = entry_panel_state.viewer_entry_snapshot
        entry_ref = _get_viewer_entry_ref_for_resource_write()
        if viewer_entry is None or entry_ref is None or viewer_entry.ref != entry_ref:
            _clear_resource_draft_state()
            _clear_resource_write_error()
            render_shell()
            page.update()
            return

        entry_panel_state.resource_draft_entry_ref = viewer_entry.ref
        entry_panel_state.resource_draft_values = _normalize_resource_draft_values(
            viewer_entry.resource_deltas
        )
        entry_panel_state.resource_draft_dirty = False
        entry_panel_state.resource_draft_discard_notice = None
        _clear_resource_write_error()
        render_shell()
        page.update()

    def _show_session_form_dialog(
        *,
        mode: str,
        session_to_edit: ViewerSessionItem | None = None,
    ) -> None:
        if local_state.viewer_entry_ref is None:
            _set_session_write_error("No hay entry en el visor para gestionar sesiones.")
            render_shell()
            page.update()
            return

        started_date_default, started_time_default = _to_local_strings(
            session_to_edit.started_at_utc if session_to_edit else None
        )
        ended_date_default, ended_time_default = _to_local_strings(
            session_to_edit.ended_at_utc if session_to_edit else None
        )
        active_default = bool(session_to_edit and session_to_edit.ended_at_utc is None)

        started_date_field = ft.TextField(
            label="Inicio (fecha local)",
            hint_text="YYYY-MM-DD",
            value=started_date_default,
            dense=True,
            width=180,
        )
        started_time_field = ft.TextField(
            label="Inicio (hora local)",
            hint_text="HH:MM",
            value=started_time_default,
            dense=True,
            width=140,
        )
        ended_date_field = ft.TextField(
            label="Fin (fecha local)",
            hint_text="YYYY-MM-DD",
            value=ended_date_default,
            dense=True,
            width=180,
        )
        ended_time_field = ft.TextField(
            label="Fin (hora local)",
            hint_text="HH:MM",
            value=ended_time_default,
            dense=True,
            width=140,
        )
        active_checkbox = ft.Checkbox(
            label="Sesión activa (sin fin)",
            value=active_default if mode == "edit" else False,
        )
        dialog_error = ft.Text("", color="#8A1F1F", size=12, visible=False)

        def _apply_active_checkbox(_e=None) -> None:
            disable_end = bool(active_checkbox.value)
            ended_date_field.disabled = disable_end
            ended_time_field.disabled = disable_end
            page.update()

        active_checkbox.on_change = _apply_active_checkbox

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
                        raise ValueError(
                            "Fin: rellena fecha y hora o marca 'Sesión activa (sin fin)'."
                        )
            except ValueError as exc:
                dialog_error.value = str(exc)
                dialog_error.visible = True
                page.update()
                return

            _close_dialog()
            if mode == "create":
                _run_session_write(
                    lambda client, entry_ref: manual_create_session(
                        client,
                        entry_ref=entry_ref,
                        started_at_utc=started_at_utc,
                        ended_at_utc=ended_at_utc,
                    )
                )
            elif mode == "edit" and session_to_edit is not None:
                _run_session_write(
                    lambda client, entry_ref: manual_update_session(
                        client,
                        entry_ref=entry_ref,
                        session_id=session_to_edit.session_id,
                        started_at_utc=started_at_utc,
                        ended_at_utc=ended_at_utc,
                    )
                )

        title = "Crear sesión manual" if mode == "create" else "Editar sesión"
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
                ft.TextButton("Cancelar", on_click=lambda _e: _close_dialog()),
                ft.FilledButton(submit_label, on_click=_submit),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        _open_dialog(dialog)
        _apply_active_checkbox()

    def handle_open_create_session_modal() -> None:
        _show_session_form_dialog(mode="create")

    def handle_open_edit_session_modal(session_id: str) -> None:
        session = _find_viewer_session_item(entry_panel_state.viewer_sessions, session_id)
        if session is None:
            _set_session_write_error("La sesión seleccionada ya no está visible en el visor.")
            render_shell()
            page.update()
            return
        _show_session_form_dialog(mode="edit", session_to_edit=session)

    def handle_open_delete_session_confirm(session_id: str) -> None:
        session = _find_viewer_session_item(entry_panel_state.viewer_sessions, session_id)
        if session is None:
            _set_session_write_error("La sesión seleccionada ya no está visible en el visor.")
            render_shell()
            page.update()
            return

        def _confirm(_e) -> None:
            _close_dialog()
            _run_session_write(
                lambda client, entry_ref: manual_delete_session(
                    client,
                    entry_ref=entry_ref,
                    session_id=session_id,
                )
            )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Borrar sesión"),
            content=ft.Text(
                f"¿Seguro que quieres borrar la sesión `{session_id}`? Esta acción es irreversible."
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _e: _close_dialog()),
                ft.FilledButton("Borrar", on_click=_confirm),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        _open_dialog(dialog)

    def _handle_media_change(_e) -> None:
        _sync_root_height_to_viewport()
        page.update()

    page.on_media_change = _handle_media_change

    # Carga inicial: si falla, el shell se renderiza con error visible.
    _sync_root_height_to_viewport()
    load_readonly_snapshot(selected_year_override=local_state.selected_year)
    render_shell()
    return root


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


def _entry_ref_matches_selected_week(state: MainScreenLocalState, entry_ref: EntryRef) -> bool:
    return (
        state.selected_year is not None
        and state.selected_week is not None
        and entry_ref.year_number == state.selected_year
        and entry_ref.week_number == state.selected_week
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
