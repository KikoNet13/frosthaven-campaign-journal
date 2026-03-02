from __future__ import annotations

from dataclasses import dataclass, field


ENTRY_RESOURCE_KEYS = ("lumber", "metal", "hide")


@dataclass(frozen=True)
class EntryRef:
    year_number: int
    week_number: int
    entry_id: str


@dataclass(frozen=True)
class EntrySummary:
    ref: EntryRef
    label: str
    entry_type: str
    scenario_ref: int | None = None
    order_index: int | None = None
    resource_deltas: dict[str, int] = field(default_factory=dict)
    created_at_utc: object | None = None
    updated_at_utc: object | None = None


@dataclass(frozen=True)
class ViewerSessionItem:
    session_id: str
    started_at_utc: object | None
    ended_at_utc: object | None
    created_at_utc: object | None = None
    updated_at_utc: object | None = None


@dataclass(frozen=True)
class WeekSummary:
    year_number: int
    week_number: int
    is_closed: bool
    status_label: str
    notes_preview: str


@dataclass
class MainScreenLocalState:
    selected_year: int | None
    selected_week: int | None
    viewer_entry_ref: EntryRef | None


def entry_ref_matches_selected_week(state: MainScreenLocalState, entry_ref: EntryRef) -> bool:
    return (
        state.selected_year is not None
        and state.selected_week is not None
        and entry_ref.year_number == state.selected_year
        and entry_ref.week_number == state.selected_week
    )


def build_initial_main_screen_state() -> MainScreenLocalState:
    return MainScreenLocalState(
        selected_year=None,
        selected_week=None,
        viewer_entry_ref=None,
    )
