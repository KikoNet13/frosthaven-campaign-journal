from __future__ import annotations

from dataclasses import dataclass

from frosthaven_campaign_journal.state.placeholders import EntryRef


@dataclass(frozen=True)
class AppStarted:
    pass


@dataclass(frozen=True)
class ViewportChanged:
    pass


@dataclass(frozen=True)
class PrevYearPressed:
    pass


@dataclass(frozen=True)
class NextYearPressed:
    pass


@dataclass(frozen=True)
class SelectWeekPressed:
    week_number: int


@dataclass(frozen=True)
class SelectEntryPressed:
    entry_ref: EntryRef


@dataclass(frozen=True)
class ManualRefreshPressed:
    pass


@dataclass(frozen=True)
class StartSessionPressed:
    pass


@dataclass(frozen=True)
class StopSessionPressed:
    pass


@dataclass(frozen=True)
class OpenManualCreateSessionPressed:
    pass


@dataclass(frozen=True)
class OpenManualEditSessionPressed:
    session_id: str


@dataclass(frozen=True)
class OpenManualDeleteSessionPressed:
    session_id: str


@dataclass(frozen=True)
class OpenWeekNotesModalPressed:
    pass


@dataclass(frozen=True)
class RequestWeekClosePressed:
    pass


@dataclass(frozen=True)
class RequestWeekReopenPressed:
    pass


@dataclass(frozen=True)
class RequestWeekReclosePressed:
    pass


@dataclass(frozen=True)
class OpenEntryAddModalPressed:
    pass


@dataclass(frozen=True)
class OpenEditEntryModalPressed:
    pass


@dataclass(frozen=True)
class OpenEntryDeleteConfirmPressed:
    pass


@dataclass(frozen=True)
class ReorderEntryUpPressed:
    pass


@dataclass(frozen=True)
class ReorderEntryDownPressed:
    pass


@dataclass(frozen=True)
class AdjustResourceDraftDeltaPressed:
    resource_key: str
    adjustment_delta: int


@dataclass(frozen=True)
class SaveResourceDraftPressed:
    pass


@dataclass(frozen=True)
class DiscardResourceDraftPressed:
    pass


@dataclass(frozen=True)
class OpenExtendYearPlusOneConfirmPressed:
    pass


@dataclass(frozen=True)
class ResourceDraftLeaveDialogSavePressed:
    pass


@dataclass(frozen=True)
class ResourceDraftLeaveDialogDiscardPressed:
    pass


@dataclass(frozen=True)
class ResourceDraftLeaveDialogCancelPressed:
    pass


@dataclass(frozen=True)
class ReplayPendingContextIntent:
    pass


MainShellIntent = (
    AppStarted
    | ViewportChanged
    | PrevYearPressed
    | NextYearPressed
    | SelectWeekPressed
    | SelectEntryPressed
    | ManualRefreshPressed
    | StartSessionPressed
    | StopSessionPressed
    | OpenManualCreateSessionPressed
    | OpenManualEditSessionPressed
    | OpenManualDeleteSessionPressed
    | OpenWeekNotesModalPressed
    | RequestWeekClosePressed
    | RequestWeekReopenPressed
    | RequestWeekReclosePressed
    | OpenEntryAddModalPressed
    | OpenEditEntryModalPressed
    | OpenEntryDeleteConfirmPressed
    | ReorderEntryUpPressed
    | ReorderEntryDownPressed
    | AdjustResourceDraftDeltaPressed
    | SaveResourceDraftPressed
    | DiscardResourceDraftPressed
    | OpenExtendYearPlusOneConfirmPressed
    | ResourceDraftLeaveDialogSavePressed
    | ResourceDraftLeaveDialogDiscardPressed
    | ResourceDraftLeaveDialogCancelPressed
    | ReplayPendingContextIntent
)


