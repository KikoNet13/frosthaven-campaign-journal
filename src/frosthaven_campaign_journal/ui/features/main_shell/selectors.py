from __future__ import annotations

from frosthaven_campaign_journal.state.placeholders import (
    ENTRY_RESOURCE_KEYS,
    EntryRef,
    MockEntry,
    MockWeek,
    entry_ref_matches_selected_week,
)
from frosthaven_campaign_journal.ui.features.main_shell.state import MainShellState


def weeks_for_selected_year(state: MainShellState) -> list[MockWeek]:
    selected_year = state.local_state.selected_year
    if selected_year is None:
        return []
    return state.read_state.weeks_by_year.get(selected_year, [])


def entries_for_selected_week(state: MainShellState) -> list[MockEntry]:
    if state.local_state.selected_week is None:
        return []
    return state.entry_panel_state.entries_for_selected_week


def viewer_entry(state: MainShellState) -> MockEntry | None:
    return state.entry_panel_state.viewer_entry_snapshot


def resource_draft_attached_to_viewer(state: MainShellState) -> bool:
    return (
        state.local_state.viewer_entry_ref is not None
        and state.entry_panel_state.resource_draft_entry_ref == state.local_state.viewer_entry_ref
    )


def has_dirty_resource_draft_attached_to_viewer(state: MainShellState) -> bool:
    return state.entry_panel_state.resource_draft_dirty and resource_draft_attached_to_viewer(state)


def clear_all_write_errors(state: MainShellState) -> None:
    state.entry_panel_state.session_write_error_message = None
    state.entry_panel_state.week_write_error_message = None
    state.entry_panel_state.entry_write_error_message = None
    state.entry_panel_state.resource_write_error_message = None


def normalize_resource_draft_values(raw_map: dict[str, int] | None) -> dict[str, int]:
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


def clear_resource_draft_state(state: MainShellState) -> None:
    state.entry_panel_state.resource_draft_entry_ref = None
    state.entry_panel_state.resource_draft_values = {}
    state.entry_panel_state.resource_draft_dirty = False
    state.entry_panel_state.resource_draft_discard_notice = None


def discard_resource_draft_for_context_change(state: MainShellState, *, show_notice: bool) -> None:
    viewer = viewer_entry(state)
    if viewer is None:
        clear_resource_draft_state(state)
        return

    state.entry_panel_state.resource_draft_entry_ref = viewer.ref
    state.entry_panel_state.resource_draft_values = normalize_resource_draft_values(viewer.resource_deltas)
    state.entry_panel_state.resource_draft_dirty = False
    if show_notice:
        state.entry_panel_state.resource_draft_discard_notice = (
            "Cambios locales de recursos descartados por cambio de contexto."
        )
    else:
        state.entry_panel_state.resource_draft_discard_notice = None
    state.entry_panel_state.resource_write_error_message = None


def sync_resource_draft_from_viewer_snapshot(state: MainShellState) -> None:
    viewer = viewer_entry(state)
    if viewer is None:
        clear_resource_draft_state(state)
        return
    normalized = normalize_resource_draft_values(viewer.resource_deltas)
    state.entry_panel_state.resource_draft_entry_ref = viewer.ref
    state.entry_panel_state.resource_draft_values = normalized
    state.entry_panel_state.resource_draft_dirty = False
    state.entry_panel_state.resource_draft_discard_notice = None
    state.entry_panel_state.resource_write_error_message = None


def selected_week_for_write(state: MainShellState) -> MockWeek | None:
    selected_week_number = state.local_state.selected_week
    if selected_week_number is None:
        return None
    for week in weeks_for_selected_year(state):
        if week.week_number == selected_week_number:
            return week
    return None


def viewer_matches_week(state: MainShellState, year_number: int, week_number: int) -> bool:
    entry_ref = state.local_state.viewer_entry_ref
    return (
        entry_ref is not None
        and entry_ref.year_number == year_number
        and entry_ref.week_number == week_number
    )


def selected_week_target_for_entry_create(state: MainShellState) -> tuple[int, int] | None:
    target_week = selected_week_for_write(state)
    if (
        state.local_state.selected_year is None
        or state.local_state.selected_week is None
        or target_week is None
    ):
        return None
    return state.local_state.selected_year, state.local_state.selected_week


def viewer_entry_ref_for_entry_write(state: MainShellState) -> EntryRef | None:
    return state.local_state.viewer_entry_ref


def viewer_entry_ref_for_resource_write(state: MainShellState) -> EntryRef | None:
    return state.local_state.viewer_entry_ref


def entry_belongs_to_selected_week(state: MainShellState, entry_ref: EntryRef) -> bool:
    return entry_ref_matches_selected_week(state.local_state, entry_ref)

