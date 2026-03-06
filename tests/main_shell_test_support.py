from __future__ import annotations

import sys
from dataclasses import dataclass, field
from types import ModuleType


def install_data_stub() -> None:
    if "frosthaven_campaign_journal.data" in sys.modules:
        return

    data_stub = ModuleType("frosthaven_campaign_journal.data")

    class FirestoreConfigError(Exception):
        pass

    class FirestoreReadError(Exception):
        pass

    class FirestoreConflictError(Exception):
        pass

    class FirestoreTransitionInvalidError(Exception):
        pass

    class FirestoreValidationError(Exception):
        pass

    class FirestoreWriteError(Exception):
        pass

    @dataclass
    class CampaignWriteResult:
        new_year_number: int = 0
        created_week_start: int = 0
        created_week_end: int = 0

    @dataclass
    class WeekWriteResult:
        auto_stopped_session_id: str | None = None

    @dataclass
    class EntryWriteResult:
        entry_ref: object | None = None
        auto_stopped_session_id: str | None = None

    @dataclass
    class ResourceBulkWriteResult:
        pass

    @dataclass
    class WeekRead:
        year_number: int = 0
        week_number: int = 0
        status: str = "open"

    @dataclass
    class EntryRead:
        ref: object | None = None
        label: str = ""
        entry_type: str = "scenario"
        scenario_ref: int | None = None
        notes: str | None = None
        scenario_outcome: str | None = None
        order_index: int = 0
        resource_deltas: dict[str, int] = field(default_factory=dict)
        created_at_utc: object | None = None
        updated_at_utc: object | None = None

    @dataclass
    class EntrySessionRead:
        session_id: str = ""
        started_at_utc: object | None = None
        ended_at_utc: object | None = None
        created_at_utc: object | None = None
        updated_at_utc: object | None = None

    def _unexpected(*_args, **_kwargs):
        raise AssertionError("Unexpected call into frosthaven_campaign_journal.data stub")

    for name, value in {
        "FirestoreConfigError": FirestoreConfigError,
        "FirestoreReadError": FirestoreReadError,
        "FirestoreConflictError": FirestoreConflictError,
        "FirestoreTransitionInvalidError": FirestoreTransitionInvalidError,
        "FirestoreValidationError": FirestoreValidationError,
        "FirestoreWriteError": FirestoreWriteError,
        "CampaignWriteResult": CampaignWriteResult,
        "WeekWriteResult": WeekWriteResult,
        "EntryWriteResult": EntryWriteResult,
        "ResourceBulkWriteResult": ResourceBulkWriteResult,
        "WeekRead": WeekRead,
        "EntryRead": EntryRead,
        "EntrySessionRead": EntrySessionRead,
        "build_firestore_client": _unexpected,
        "load_main_screen_snapshot": _unexpected,
        "read_entry_by_ref": _unexpected,
        "read_q5_entries_for_selected_week": _unexpected,
        "read_q8_sessions_for_entry": _unexpected,
        "extend_years_plus_one": _unexpected,
        "manual_delete_session": _unexpected,
        "close_week": _unexpected,
        "delete_entry": _unexpected,
        "reclose_week": _unexpected,
        "reopen_week": _unexpected,
        "manual_create_session": _unexpected,
        "manual_update_session": _unexpected,
        "start_session": _unexpected,
        "stop_session": _unexpected,
        "create_entry": _unexpected,
        "reorder_entry_within_week": _unexpected,
        "replace_entry_resource_deltas": _unexpected,
        "update_entry": _unexpected,
        "update_entry_notes": _unexpected,
    }.items():
        setattr(data_stub, name, value)

    sys.modules["frosthaven_campaign_journal.data"] = data_stub