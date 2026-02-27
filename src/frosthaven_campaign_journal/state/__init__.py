"""Local UI state placeholders for the bootstrap slice."""

from .placeholders import (
    ENTRY_RESOURCE_KEYS,
    EntryRef,
    MainScreenLocalState,
    MockEntry,
    MockMainScreenDataset,
    MockWeek,
    ViewerSessionItem,
    build_initial_main_screen_state,
    build_mock_entries_by_week,
    build_mock_main_screen_dataset,
    build_mock_weeks_by_year,
    build_mock_years,
    entry_ref_matches_selected_week,
)

__all__ = [
    "ENTRY_RESOURCE_KEYS",
    "EntryRef",
    "MainScreenLocalState",
    "MockEntry",
    "MockMainScreenDataset",
    "MockWeek",
    "ViewerSessionItem",
    "build_initial_main_screen_state",
    "build_mock_entries_by_week",
    "build_mock_main_screen_dataset",
    "build_mock_weeks_by_year",
    "build_mock_years",
    "entry_ref_matches_selected_week",
]
