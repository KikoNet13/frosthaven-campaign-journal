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
    MainScreenSnapshot,
    WeekRead,
    derive_year_from_week_cursor,
    load_main_screen_snapshot,
)

__all__ = [
    "ActiveEntryRead",
    "ActiveSessionRead",
    "CampaignMainRead",
    "FirestoreConfigError",
    "FirestoreReadError",
    "MainScreenSnapshot",
    "WeekRead",
    "build_firestore_client",
    "derive_year_from_week_cursor",
    "describe_firestore_status",
    "load_main_screen_snapshot",
]
