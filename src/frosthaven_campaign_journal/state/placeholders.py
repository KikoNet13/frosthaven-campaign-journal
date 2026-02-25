from __future__ import annotations

from dataclasses import dataclass, field
from typing import NamedTuple


@dataclass(frozen=True)
class EntryRef:
    year_number: int
    week_number: int
    entry_id: str


@dataclass(frozen=True)
class MockEntry:
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
class MockWeek:
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


class MockMainScreenDataset(NamedTuple):
    years: list[int]
    weeks_by_year: dict[int, list[MockWeek]]
    entries_by_week: dict[tuple[int, int], list[MockEntry]]


def build_mock_years() -> list[int]:
    return [1, 2, 3]


def build_mock_weeks_by_year() -> dict[int, list[MockWeek]]:
    years = build_mock_years()
    weeks_by_year: dict[int, list[MockWeek]] = {}

    for year_number in years:
        start_week = ((year_number - 1) * 20) + 1
        weeks: list[MockWeek] = []
        for offset in range(20):
            week_number = start_week + offset
            if year_number == 1:
                is_closed = True
            elif year_number == 2:
                is_closed = week_number <= 34
            else:
                is_closed = False

            weeks.append(
                MockWeek(
                    year_number=year_number,
                    week_number=week_number,
                    is_closed=is_closed,
                    status_label="closed" if is_closed else "open",
                    notes_preview=(
                        f"Notas mock de la week {week_number} (Año {year_number})."
                    ),
                )
            )
        weeks_by_year[year_number] = weeks

    return weeks_by_year


def build_mock_entries_by_week() -> dict[tuple[int, int], list[MockEntry]]:
    entries: dict[tuple[int, int], list[MockEntry]] = {}

    week35_entries = [
        MockEntry(
            ref=EntryRef(year_number=2, week_number=35, entry_id="w35-e1"),
            label="Escenario 51",
            entry_type="scenario",
            scenario_ref=51,
        ),
        MockEntry(
            ref=EntryRef(year_number=2, week_number=35, entry_id="w35-e2"),
            label="Escenario 42",
            entry_type="scenario",
            scenario_ref=42,
        ),
        MockEntry(
            ref=EntryRef(year_number=2, week_number=35, entry_id="w35-e3"),
            label="Puesto fronterizo",
            entry_type="outpost",
            scenario_ref=None,
        ),
    ]
    entries[(2, 35)] = week35_entries

    week36_entries = [
        MockEntry(
            ref=EntryRef(year_number=2, week_number=36, entry_id="w36-e1"),
            label="Escenario 51",
            entry_type="scenario",
            scenario_ref=51,
        ),
        MockEntry(
            ref=EntryRef(year_number=2, week_number=36, entry_id="w36-e2"),
            label="Escenario 42",
            entry_type="scenario",
            scenario_ref=42,
        ),
        MockEntry(
            ref=EntryRef(year_number=2, week_number=36, entry_id="w36-e3"),
            label="Puesto fronterizo",
            entry_type="outpost",
            scenario_ref=None,
        ),
    ]
    entries[(2, 36)] = week36_entries

    entries[(2, 34)] = [
        MockEntry(
            ref=EntryRef(year_number=2, week_number=34, entry_id="w34-e1"),
            label="Escenario 17",
            entry_type="scenario",
            scenario_ref=17,
        )
    ]

    return entries


def build_mock_main_screen_dataset() -> MockMainScreenDataset:
    years = build_mock_years()
    weeks_by_year = build_mock_weeks_by_year()
    entries_by_week = build_mock_entries_by_week()
    return MockMainScreenDataset(
        years=years,
        weeks_by_year=weeks_by_year,
        entries_by_week=entries_by_week,
    )


def build_initial_main_screen_state() -> MainScreenLocalState:
    return MainScreenLocalState(
        selected_year=None,
        selected_week=None,
        viewer_entry_ref=None,
    )
