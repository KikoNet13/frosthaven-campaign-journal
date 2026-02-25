from __future__ import annotations

from dataclasses import dataclass, field

import flet as ft

from frosthaven_campaign_journal.config import load_settings
from frosthaven_campaign_journal.data import (
    EntryRead,
    EntrySessionRead,
    FirestoreConfigError,
    FirestoreReadError,
    WeekRead,
    build_firestore_client,
    derive_year_from_week_cursor,
    load_main_screen_snapshot,
    read_entry_by_ref,
    read_q5_entries_for_selected_week,
    read_q8_sessions_for_entry,
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


def build_app_root(page: ft.Page) -> ft.Control:
    local_state = build_initial_main_screen_state()
    read_state = MainScreenReadState()
    entry_panel_state = EntryPanelReadState()

    shell_host = ft.Container(expand=True)
    root = ft.SafeArea(content=shell_host)

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
        shell_host.content = build_main_shell_view(
            state=local_state,
            years=read_state.years,
            weeks_for_selected_year=current_weeks_for_selected_year(),
            entries_for_selected_week=current_entries_for_selected_week(),
            viewer_entry=current_viewer_entry(),
            viewer_sessions=entry_panel_state.viewer_sessions,
            entries_panel_error_message=entry_panel_state.entries_panel_error_message,
            viewer_sessions_error_message=entry_panel_state.viewer_sessions_error_message,
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

    def load_viewer_entry_and_sessions() -> None:
        if local_state.viewer_entry_ref is None:
            entry_panel_state.viewer_entry_snapshot = None
            entry_panel_state.viewer_sessions = []
            entry_panel_state.viewer_sessions_error_message = None
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

        local_state.selected_year = read_state.years[current_index - 1]
        local_state.selected_week = None
        entry_panel_state.entries_for_selected_week = []
        entry_panel_state.entries_panel_error_message = None
        refresh_and_render(selected_year_override=local_state.selected_year, reload_q8=False)

    def handle_next_year() -> None:
        if local_state.selected_year is None or local_state.selected_year not in read_state.years:
            return
        current_index = read_state.years.index(local_state.selected_year)
        if current_index >= len(read_state.years) - 1:
            return

        local_state.selected_year = read_state.years[current_index + 1]
        local_state.selected_week = None
        entry_panel_state.entries_for_selected_week = []
        entry_panel_state.entries_panel_error_message = None
        refresh_and_render(selected_year_override=local_state.selected_year, reload_q8=False)

    def handle_select_week(week_number: int) -> None:
        if local_state.selected_year is None:
            return
        visible_weeks = current_weeks_for_selected_year()
        if not any(week.week_number == week_number for week in visible_weeks):
            return
        local_state.selected_week = week_number
        load_entries_for_selected_week()  # Q5 solo, el visor sticky no recarga Q8 por navegación
        render_shell()
        page.update()

    def handle_select_entry(entry_ref: EntryRef) -> None:
        local_state.viewer_entry_ref = entry_ref
        load_viewer_entry_and_sessions()  # Q8 sigue al visor sticky
        render_shell()
        page.update()

    def handle_manual_refresh() -> None:
        refresh_and_render(
            selected_year_override=local_state.selected_year,
            reload_q5=(local_state.selected_week is not None),
            reload_q8=(local_state.viewer_entry_ref is not None),
        )

    # Carga inicial: si falla, el shell se renderiza con error visible.
    load_readonly_snapshot(selected_year_override=local_state.selected_year)
    render_shell()
    return root


def _map_week_read_to_mock(week: WeekRead) -> MockWeek:
    is_closed = week.status == "closed"
    notes_preview = week.notes or f"Sin notas en la week {week.week_number}."
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
