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
from .entry_writes import (
    EntryWriteResult,
    create_entry,
    delete_entry,
    reorder_entry_within_week,
    update_entry,
)
from .resource_writes import (
    ResourceBulkWriteResult,
    ResourceWriteResult,
    adjust_resource_delta,
    replace_entry_resource_deltas,
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
    "EntryWriteResult",
    "EntryRead",
    "EntrySessionRead",
    "FirestoreConflictError",
    "FirestoreConfigError",
    "FirestoreReadError",
    "FirestoreTransitionInvalidError",
    "FirestoreValidationError",
    "FirestoreWriteError",
    "MainScreenSnapshot",
    "ResourceBulkWriteResult",
    "ResourceWriteResult",
    "SessionWriteResult",
    "WeekRead",
    "WeekWriteResult",
    "adjust_resource_delta",
    "build_firestore_client",
    "close_week",
    "create_entry",
    "delete_entry",
    "derive_year_from_week_cursor",
    "describe_firestore_status",
    "load_main_screen_snapshot",
    "manual_create_session",
    "manual_delete_session",
    "manual_update_session",
    "read_entry_by_ref",
    "read_q5_entries_for_selected_week",
    "read_q8_sessions_for_entry",
    "reorder_entry_within_week",
    "reclose_week",
    "replace_entry_resource_deltas",
    "reopen_week",
    "start_session",
    "stop_session",
    "update_entry",
    "update_week_notes",
]
