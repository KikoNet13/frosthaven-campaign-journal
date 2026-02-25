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
from .session_writes import (
    SessionWriteResult,
    manual_create_session,
    manual_delete_session,
    manual_update_session,
    start_session,
    stop_session,
)
from .week_writes import (
    WeekWriteResult,
    close_week,
    reopen_week,
    reclose_week,
    update_week_notes,
)
from .write_errors import (
    FirestoreConflictError,
    FirestoreTransitionInvalidError,
    FirestoreValidationError,
    FirestoreWriteError,
)

__all__ = [
    "ActiveEntryRead",
    "ActiveSessionRead",
    "CampaignMainRead",
    "EntryRead",
    "EntrySessionRead",
    "FirestoreConflictError",
    "FirestoreConfigError",
    "FirestoreReadError",
    "FirestoreTransitionInvalidError",
    "FirestoreValidationError",
    "FirestoreWriteError",
    "MainScreenSnapshot",
    "SessionWriteResult",
    "WeekRead",
    "WeekWriteResult",
    "build_firestore_client",
    "close_week",
    "derive_year_from_week_cursor",
    "describe_firestore_status",
    "load_main_screen_snapshot",
    "manual_create_session",
    "manual_delete_session",
    "manual_update_session",
    "read_entry_by_ref",
    "read_q5_entries_for_selected_week",
    "read_q8_sessions_for_entry",
    "reclose_week",
    "reopen_week",
    "start_session",
    "stop_session",
    "update_week_notes",
]
