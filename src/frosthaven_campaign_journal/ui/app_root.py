from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.config import load_settings
from frosthaven_campaign_journal.state.placeholders import (
    EntryRef,
    MockEntry,
    build_initial_main_screen_state,
    build_mock_main_screen_dataset,
)
from frosthaven_campaign_journal.ui.views import (
    build_main_shell_view,
)


def build_app_root(page: ft.Page) -> ft.Control:
    settings = load_settings()
    dataset = build_mock_main_screen_dataset()
    state = build_initial_main_screen_state(dataset.active_entry_ref_mock)

    entry_index = _build_entry_index(dataset.entries_by_week)
    root = ft.SafeArea(content=ft.Container(), expand=True)

    def weeks_for_selected_year() -> list:
        return dataset.weeks_by_year.get(state.selected_year, [])

    def entries_for_selected_week() -> list[MockEntry]:
        if state.selected_week is None:
            return []
        return dataset.entries_by_week.get((state.selected_year, state.selected_week), [])

    def resolve_entry(entry_ref: EntryRef | None) -> MockEntry | None:
        if entry_ref is None:
            return None
        return entry_index.get((entry_ref.year_number, entry_ref.week_number, entry_ref.entry_id))

    def rerender() -> None:
        root.content = build_main_shell_view(
            state=state,
            years=dataset.years,
            weeks_for_selected_year=weeks_for_selected_year(),
            entries_for_selected_week=entries_for_selected_week(),
            viewer_entry=resolve_entry(state.viewer_entry_ref),
            active_entry_mock=resolve_entry(state.active_entry_ref_mock),
            env_name=settings.env,
            on_prev_year=handle_prev_year,
            on_next_year=handle_next_year,
            on_select_week=handle_select_week,
            on_select_entry=handle_select_entry,
        )

    def commit_ui_state() -> None:
        rerender()
        page.update()

    def handle_prev_year() -> None:
        current_index = dataset.years.index(state.selected_year)
        if current_index == 0:
            return
        state.selected_year = dataset.years[current_index - 1]
        state.selected_week = None
        commit_ui_state()

    def handle_next_year() -> None:
        current_index = dataset.years.index(state.selected_year)
        if current_index >= len(dataset.years) - 1:
            return
        state.selected_year = dataset.years[current_index + 1]
        state.selected_week = None
        commit_ui_state()

    def handle_select_week(week_number: int) -> None:
        if not any(week.week_number == week_number for week in weeks_for_selected_year()):
            return
        state.selected_week = week_number
        commit_ui_state()

    def handle_select_entry(entry_ref: EntryRef) -> None:
        if state.selected_week is None:
            return
        week_entries = entries_for_selected_week()
        if not any(entry.ref == entry_ref for entry in week_entries):
            return
        state.viewer_entry_ref = entry_ref
        commit_ui_state()

    rerender()
    return root


def _build_entry_index(
    entries_by_week: dict[tuple[int, int], list[MockEntry]],
) -> dict[tuple[int, int, str], MockEntry]:
    index: dict[tuple[int, int, str], MockEntry] = {}
    for entries in entries_by_week.values():
        for entry in entries:
            key = (
                entry.ref.year_number,
                entry.ref.week_number,
                entry.ref.entry_id,
            )
            index[key] = entry
    return index
