from __future__ import annotations

from frosthaven_campaign_journal.data import (
    FirestoreConfigError,
    FirestoreConflictError,
    FirestoreReadError,
)
from frosthaven_campaign_journal.models import ENTRY_RESOURCE_KEYS, EntryRef, EntrySummary
from frosthaven_campaign_journal.ui.main_shell.state.types import ToastState


class MainShellRuntimeSupportMixin:
    def _clear_form_modal_states(self) -> None:
        self.entry_form_state = None
        self.entry_notes_editor_state = None
        self.session_form_state = None

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

    def _resource_draft_for_entry(self, entry_ref: EntryRef) -> dict[str, int]:
        current = self.entry_panel_state.resource_draft_by_entry_ref.get(entry_ref)
        if current is None:
            current = {}
            self.entry_panel_state.resource_draft_by_entry_ref[entry_ref] = current
        return current

    def _is_resource_draft_dirty(self, entry_ref: EntryRef) -> bool:
        return bool(self.entry_panel_state.resource_draft_dirty_by_entry_ref.get(entry_ref, False))

    def _set_resource_draft_for_entry(self, entry_ref: EntryRef, values: dict[str, int], *, dirty: bool) -> None:
        self.entry_panel_state.resource_draft_by_entry_ref[entry_ref] = dict(values)
        self.entry_panel_state.resource_draft_dirty_by_entry_ref[entry_ref] = dirty

    def _clear_resource_draft_for_entry(self, entry_ref: EntryRef) -> None:
        self.entry_panel_state.resource_draft_by_entry_ref.pop(entry_ref, None)
        self.entry_panel_state.resource_draft_dirty_by_entry_ref.pop(entry_ref, None)
        self.entry_panel_state.resource_write_error_by_entry_ref.pop(entry_ref, None)
        self.entry_panel_state.resource_write_pending_by_entry_ref.pop(entry_ref, None)
        if self.entry_panel_state.resource_draft_entry_ref == entry_ref:
            self.entry_panel_state.resource_draft_entry_ref = None
            self.entry_panel_state.resource_draft_values = {}
            self.entry_panel_state.resource_draft_dirty = False

    def _clear_resource_draft_state(self) -> None:
        self.entry_panel_state.resource_draft_entry_ref = None
        self.entry_panel_state.resource_draft_values = {}
        self.entry_panel_state.resource_draft_dirty = False
        self.entry_panel_state.resource_draft_by_entry_ref = {}
        self.entry_panel_state.resource_draft_dirty_by_entry_ref = {}
        self.entry_panel_state.resource_write_error_by_entry_ref = {}
        self.entry_panel_state.resource_write_pending_by_entry_ref = {}

    def _resource_draft_attached_to_viewer(self) -> bool:
        return (
            self.local_state.viewer_entry_ref is not None
            and self.entry_panel_state.resource_draft_entry_ref == self.local_state.viewer_entry_ref
        )

    def _has_dirty_resource_draft_attached_to_viewer(self) -> bool:
        return self._resource_draft_attached_to_viewer() and self.entry_panel_state.resource_draft_dirty

    def _has_any_dirty_resource_draft(self) -> bool:
        if self.entry_panel_state.resource_draft_dirty:
            return True
        return any(self.entry_panel_state.resource_draft_dirty_by_entry_ref.values())

    def _sync_resource_draft_from_entry_snapshot(self, entry: EntrySummary) -> None:
        normalized_deltas = self._normalize_resource_draft_values(entry.resource_deltas)
        if not self._is_resource_draft_dirty(entry.ref):
            self._set_resource_draft_for_entry(entry.ref, normalized_deltas, dirty=False)

        if self.entry_panel_state.resource_draft_entry_ref == entry.ref:
            if not self.entry_panel_state.resource_draft_dirty:
                self.entry_panel_state.resource_draft_values = dict(normalized_deltas)
                self.entry_panel_state.resource_draft_dirty = False
        elif self.entry_panel_state.resource_draft_entry_ref is None:
            self.entry_panel_state.resource_draft_entry_ref = entry.ref
            self.entry_panel_state.resource_draft_values = dict(normalized_deltas)
            self.entry_panel_state.resource_draft_dirty = False

    def _sync_resource_draft_from_entries(self) -> None:
        valid_refs = {entry.ref for entry in self.entry_panel_state.entries_for_selected_week}
        for stale_ref in list(self.entry_panel_state.resource_draft_by_entry_ref.keys()):
            if stale_ref not in valid_refs:
                self._clear_resource_draft_for_entry(stale_ref)
        for entry in self.entry_panel_state.entries_for_selected_week:
            self._sync_resource_draft_from_entry_snapshot(entry)

    def _emit_info_toast(self, message: str) -> None:
        self.toast_state = ToastState(message=message, event_id=self._next_ui_event_id())

    def _clear_info_toast(self, *, event_id: int | None = None) -> None:
        if event_id is not None and self.toast_state.event_id != event_id:
            return
        self.toast_state = ToastState()

    def _discard_resource_draft_for_context_change(self, *, show_notice: bool) -> None:
        had_dirty = self._has_any_dirty_resource_draft()
        self._clear_resource_draft_state()
        self.entry_panel_state.resource_write_error_message = None
        if show_notice and had_dirty:
            self._emit_info_toast("Cambios de recursos sin guardar descartados al cambiar de contexto.")

    def _clear_write_errors(self) -> None:
        self.entry_panel_state.session_write_error_message = None
        self.entry_panel_state.week_write_error_message = None
        self.entry_panel_state.entry_write_error_message = None
        self.entry_panel_state.resource_write_error_message = None
        self.entry_panel_state.session_write_error_by_entry_ref = {}
        self.entry_panel_state.resource_write_error_by_entry_ref = {}

    def _set_campaign_error(self, message: str) -> None:
        self.read_state.warning_message = message

    def _set_session_error(self, message: str, *, entry_ref: EntryRef | None = None) -> None:
        self.entry_panel_state.session_write_error_message = message
        if entry_ref is not None:
            self.entry_panel_state.session_write_error_by_entry_ref[entry_ref] = message

    def _set_week_error(self, message: str) -> None:
        self.entry_panel_state.week_write_error_message = message

    def _set_entry_error(self, message: str) -> None:
        self.entry_panel_state.entry_write_error_message = message

    def _set_resource_error(self, message: str, *, entry_ref: EntryRef | None = None) -> None:
        self.entry_panel_state.resource_write_error_message = message
        if entry_ref is not None:
            self.entry_panel_state.resource_write_error_by_entry_ref[entry_ref] = message

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
