from __future__ import annotations

from dataclasses import dataclass, field

import flet as ft

from frosthaven_campaign_journal.config import load_settings
from frosthaven_campaign_journal.data import (
    FirestoreConfigError,
    FirestoreReadError,
    WeekRead,
    build_firestore_client,
    derive_year_from_week_cursor,
    load_main_screen_snapshot,
)
from frosthaven_campaign_journal.state.placeholders import (
    EntryRef,
    MainScreenLocalState,
    MockEntry,
    MockWeek,
    build_initial_main_screen_state,
    build_mock_main_screen_dataset,
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


def build_app_root(page: ft.Page) -> ft.Control:
    mock_dataset = build_mock_main_screen_dataset()
    mock_entry_index = {
        entry.ref: entry
        for entries in mock_dataset.entries_by_week.values()
        for entry in entries
    }
    local_state = build_initial_main_screen_state()
    read_state = MainScreenReadState()

    shell_host = ft.Container(expand=True)
    root = ft.SafeArea(content=shell_host)

    def current_weeks_for_selected_year() -> list[MockWeek]:
        if local_state.selected_year is None:
            return []
        return read_state.weeks_by_year.get(local_state.selected_year, [])

    def current_entries_for_selected_week() -> list[MockEntry]:
        if local_state.selected_year is None or local_state.selected_week is None:
            return []
        return mock_dataset.entries_by_week.get(
            (local_state.selected_year, local_state.selected_week),
            [],
        )

    def current_viewer_entry() -> MockEntry | None:
        if local_state.viewer_entry_ref is None:
            return None
        return mock_entry_index.get(local_state.viewer_entry_ref)

    def render_shell() -> None:
        shell_host.content = build_main_shell_view(
            state=local_state,
            years=read_state.years,
            weeks_for_selected_year=current_weeks_for_selected_year(),
            entries_for_selected_week=current_entries_for_selected_week(),
            viewer_entry=current_viewer_entry(),
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

    def load_readonly_snapshot(*, selected_year_override: int | None) -> bool:
        try:
            settings = load_settings()
            client = build_firestore_client(settings)
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

    def refresh_and_render(*, selected_year_override: int | None) -> None:
        load_readonly_snapshot(selected_year_override=selected_year_override)
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
        refresh_and_render(selected_year_override=local_state.selected_year)

    def handle_next_year() -> None:
        if local_state.selected_year is None or local_state.selected_year not in read_state.years:
            return
        current_index = read_state.years.index(local_state.selected_year)
        if current_index >= len(read_state.years) - 1:
            return

        local_state.selected_year = read_state.years[current_index + 1]
        local_state.selected_week = None
        refresh_and_render(selected_year_override=local_state.selected_year)

    def handle_select_week(week_number: int) -> None:
        if local_state.selected_year is None:
            return
        visible_weeks = current_weeks_for_selected_year()
        if not any(week.week_number == week_number for week in visible_weeks):
            return
        local_state.selected_week = week_number
        render_shell()
        page.update()

    def handle_select_entry(entry_ref: EntryRef) -> None:
        local_state.viewer_entry_ref = entry_ref
        render_shell()
        page.update()

    def handle_manual_refresh() -> None:
        refresh_and_render(selected_year_override=local_state.selected_year)

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
