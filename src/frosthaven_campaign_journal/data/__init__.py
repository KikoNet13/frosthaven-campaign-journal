"""Data access helpers for Firestore and read-only app slices."""

from .firestore_client import (
    FirestoreConfigError,
    FirestoreReadError,
    build_firestore_client,
)
from .firestore_placeholder import describe_firestore_status
from .main_screen_reads import (
    ActiveEntryRead,
    ActiveSessionRead,
    CampaignMainRead,
    EntryRead,
    EntrySessionRead,
    MainScreenSnapshot,
    WeekRead,
    derive_year_from_week_cursor,
    load_main_screen_snapshot,
    read_entry_by_ref,
    read_q5_entries_for_selected_week,
    read_q8_sessions_for_entry,
)

__all__ = [
    "ActiveEntryRead",
    "ActiveSessionRead",
    "CampaignMainRead",
    "EntryRead",
    "EntrySessionRead",
    "FirestoreConfigError",
    "FirestoreReadError",
    "MainScreenSnapshot",
    "WeekRead",
    "build_firestore_client",
    "derive_year_from_week_cursor",
    "describe_firestore_status",
    "load_main_screen_snapshot",
    "read_entry_by_ref",
    "read_q5_entries_for_selected_week",
    "read_q8_sessions_for_entry",
]
