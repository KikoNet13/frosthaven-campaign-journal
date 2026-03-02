from __future__ import annotations

from typing import Any, Callable

from frosthaven_campaign_journal.config import load_settings
from frosthaven_campaign_journal.data import (
    CampaignWriteResult,
    EntryWriteResult,
    FirestoreConfigError,
    FirestoreConflictError,
    FirestoreReadError,
    FirestoreTransitionInvalidError,
    FirestoreValidationError,
    FirestoreWriteError,
    ResourceBulkWriteResult,
    WeekWriteResult,
    build_firestore_client,
    close_week,
    delete_entry,
    load_main_screen_snapshot,
    manual_delete_session,
    read_entry_by_ref,
    read_q5_entries_for_selected_week,
    read_q8_sessions_for_entry,
    reclose_week,
    reopen_week,
)
from frosthaven_campaign_journal.models import (
    ENTRY_RESOURCE_KEYS,
    EntryRef,
    WeekSummary,
    entry_ref_matches_selected_week,
)
from frosthaven_campaign_journal.ui.main_shell.state.types import ConfirmationState
from frosthaven_campaign_journal.ui.main_shell.state.utils import (
    find_entry_in_list,
    map_entry_read_to_summary,
    map_session_read_to_viewer_session,
    map_week_read_to_summary,
)

class MainShellRuntimeSupportMixin:
    def _normalize_resource_draft_values(self, raw_map: dict[str, int] | None) -> dict[str, int]:
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

    def _clear_resource_draft_state(self) -> None:
        self.entry_panel_state.resource_draft_entry_ref = None
        self.entry_panel_state.resource_draft_values = {}
        self.entry_panel_state.resource_draft_dirty = False

    def _resource_draft_attached_to_viewer(self) -> bool:
        return (
            self.local_state.viewer_entry_ref is not None
            and self.entry_panel_state.resource_draft_entry_ref == self.local_state.viewer_entry_ref
        )

    def _has_dirty_resource_draft_attached_to_viewer(self) -> bool:
        return self._resource_draft_attached_to_viewer() and self.entry_panel_state.resource_draft_dirty

    def _sync_resource_draft_from_viewer_snapshot(self) -> None:
        viewer_entry = self.entry_panel_state.viewer_entry_snapshot
        if viewer_entry is None:
            return
        normalized_viewer_deltas = self._normalize_resource_draft_values(viewer_entry.resource_deltas)
        if self.entry_panel_state.resource_draft_entry_ref != viewer_entry.ref:
            self.entry_panel_state.resource_draft_entry_ref = viewer_entry.ref
            self.entry_panel_state.resource_draft_values = normalized_viewer_deltas
            self.entry_panel_state.resource_draft_dirty = False
            return
        if not self.entry_panel_state.resource_draft_dirty:
            self.entry_panel_state.resource_draft_values = normalized_viewer_deltas

    def _discard_resource_draft_for_context_change(self, *, show_notice: bool) -> None:
        had_dirty = self.entry_panel_state.resource_draft_dirty
        self._clear_resource_draft_state()
        self.entry_panel_state.resource_write_error_message = None
        if show_notice and had_dirty:
            self.info_message = "Cambios de recursos sin guardar descartados al cambiar de contexto."

    def _clear_write_errors(self) -> None:
        self.entry_panel_state.session_write_error_message = None
        self.entry_panel_state.week_write_error_message = None
        self.entry_panel_state.entry_write_error_message = None
        self.entry_panel_state.resource_write_error_message = None

    def _set_campaign_error(self, message: str) -> None:
        self.read_state.warning_message = message

    def _set_session_error(self, message: str) -> None:
        self.entry_panel_state.session_write_error_message = message

    def _set_week_error(self, message: str) -> None:
        self.entry_panel_state.week_write_error_message = message

    def _set_entry_error(self, message: str) -> None:
        self.entry_panel_state.entry_write_error_message = message

    def _set_resource_error(self, message: str) -> None:
        self.entry_panel_state.resource_write_error_message = message

    def _handle_write_exception(self, *, domain: str, exc: Exception) -> None:
        message = str(exc)
        if isinstance(exc, (FirestoreConfigError, FirestoreReadError)):
            self.read_state.status = "error"
            self.read_state.error_message = message
            return

        if isinstance(exc, FirestoreConflictError):
            self.read_state.warning_message = message

        if domain == "session":
            self._set_session_error(message)
        elif domain == "week":
            self._set_week_error(message)
        elif domain == "entry":
            self._set_entry_error(message)
        elif domain == "resource":
            self._set_resource_error(message)
        elif domain == "campaign":
            self._set_campaign_error(message)

