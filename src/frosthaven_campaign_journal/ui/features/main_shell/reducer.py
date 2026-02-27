from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field

from frosthaven_campaign_journal.ui.features.main_shell.intents import (
    AdjustResourceDraftDeltaPressed,
    AppStarted,
    DiscardResourceDraftPressed,
    MainShellIntent,
    ManualRefreshPressed,
    NextYearPressed,
    OpenEntryAddModalPressed,
    OpenEntryDeleteConfirmPressed,
    OpenEditEntryModalPressed,
    OpenExtendYearPlusOneConfirmPressed,
    OpenManualCreateSessionPressed,
    OpenManualDeleteSessionPressed,
    OpenManualEditSessionPressed,
    OpenWeekNotesModalPressed,
    PrevYearPressed,
    ReplayPendingContextIntent,
    ReorderEntryDownPressed,
    ReorderEntryUpPressed,
    RequestWeekClosePressed,
    RequestWeekReclosePressed,
    RequestWeekReopenPressed,
    ResourceDraftLeaveDialogCancelPressed,
    ResourceDraftLeaveDialogDiscardPressed,
    ResourceDraftLeaveDialogSavePressed,
    SaveResourceDraftPressed,
    SelectEntryPressed,
    SelectWeekPressed,
    StartSessionPressed,
    StopSessionPressed,
)
from frosthaven_campaign_journal.ui.features.main_shell.selectors import (
    clear_all_write_errors,
    discard_resource_draft_for_context_change,
    has_dirty_resource_draft_attached_to_viewer,
    normalize_resource_draft_values,
    selected_week_for_write,
    weeks_for_selected_year,
)
from frosthaven_campaign_journal.ui.features.main_shell.state import MainShellState


@dataclass(frozen=True)
class MainShellEffect:
    kind: str
    payload: dict[str, object] = field(default_factory=dict)


def reduce(state: MainShellState, intent: MainShellIntent) -> tuple[MainShellState, list[MainShellEffect]]:
    next_state = deepcopy(state)
    effects: list[MainShellEffect] = []

    if isinstance(intent, AppStarted):
        effects.append(
            MainShellEffect(
                kind="refresh_data",
                payload={
                    "selected_year_override": next_state.local_state.selected_year,
                    "reload_q5": False,
                    "reload_q8": False,
                },
            )
        )
        return next_state, effects

    if isinstance(intent, PrevYearPressed):
        return _queue_or_apply_context_intent(
            state=next_state,
            context_intent=intent,
            action_label="cambiar de aÃ±o",
            apply_fn=_apply_prev_year,
        )

    if isinstance(intent, NextYearPressed):
        return _queue_or_apply_context_intent(
            state=next_state,
            context_intent=intent,
            action_label="cambiar de aÃ±o",
            apply_fn=_apply_next_year,
        )

    if isinstance(intent, SelectWeekPressed):
        return _queue_or_apply_context_intent(
            state=next_state,
            context_intent=intent,
            action_label="cambiar de week",
            apply_fn=_apply_select_week,
        )

    if isinstance(intent, SelectEntryPressed):
        return _queue_or_apply_context_intent(
            state=next_state,
            context_intent=intent,
            action_label="cambiar de entry",
            apply_fn=_apply_select_entry,
        )

    if isinstance(intent, ManualRefreshPressed):
        return _queue_or_apply_context_intent(
            state=next_state,
            context_intent=intent,
            action_label="refrescar",
            apply_fn=_apply_manual_refresh,
        )

    if isinstance(intent, OpenExtendYearPlusOneConfirmPressed):
        if next_state.read_state.campaign_write_pending:
            return next_state, effects
        return _queue_or_apply_context_intent(
            state=next_state,
            context_intent=intent,
            action_label="extender +1 aÃ±o",
            apply_fn=_apply_open_extend_year_dialog,
        )

    if isinstance(intent, ResourceDraftLeaveDialogCancelPressed):
        next_state.workflow.resource_draft_leave_confirm_open = False
        next_state.workflow.pending_context_action_label = None
        next_state.workflow.pending_context_intent = None
        effects.append(MainShellEffect(kind="close_dialog"))
        return next_state, effects

    if isinstance(intent, ResourceDraftLeaveDialogDiscardPressed):
        next_state.workflow.resource_draft_leave_confirm_open = False
        effects.append(MainShellEffect(kind="close_dialog"))
        discard_resource_draft_for_context_change(next_state, show_notice=True)
        effects.append(MainShellEffect(kind="show_discard_notice_if_any"))
        effects.append(MainShellEffect(kind="replay_pending_context_intent"))
        return next_state, effects

    if isinstance(intent, ResourceDraftLeaveDialogSavePressed):
        next_state.workflow.resource_draft_leave_confirm_open = False
        effects.append(MainShellEffect(kind="close_dialog"))
        effects.append(MainShellEffect(kind="save_resource_draft_before_context_change"))
        effects.append(MainShellEffect(kind="replay_pending_context_intent"))
        return next_state, effects

    if isinstance(intent, ReplayPendingContextIntent):
        if next_state.workflow.pending_context_intent is None:
            return next_state, effects
        effects.append(MainShellEffect(kind="replay_pending_context_intent"))
        return next_state, effects

    if isinstance(intent, StartSessionPressed):
        effects.append(MainShellEffect(kind="run_begin_session"))
        return next_state, effects

    if isinstance(intent, StopSessionPressed):
        effects.append(MainShellEffect(kind="run_end_session"))
        return next_state, effects

    if isinstance(intent, OpenWeekNotesModalPressed):
        effects.append(MainShellEffect(kind="show_week_notes_dialog"))
        return next_state, effects

    if isinstance(intent, RequestWeekClosePressed):
        effects.append(MainShellEffect(kind="show_week_state_confirm_dialog", payload={"mode": "close"}))
        return next_state, effects

    if isinstance(intent, RequestWeekReopenPressed):
        effects.append(MainShellEffect(kind="show_week_state_confirm_dialog", payload={"mode": "reopen"}))
        return next_state, effects

    if isinstance(intent, RequestWeekReclosePressed):
        effects.append(MainShellEffect(kind="show_week_state_confirm_dialog", payload={"mode": "reclose"}))
        return next_state, effects

    if isinstance(intent, OpenEntryAddModalPressed):
        effects.append(MainShellEffect(kind="show_entry_form_dialog", payload={"mode": "create"}))
        return next_state, effects

    if isinstance(intent, OpenEditEntryModalPressed):
        effects.append(MainShellEffect(kind="show_entry_form_dialog", payload={"mode": "edit"}))
        return next_state, effects

    if isinstance(intent, OpenEntryDeleteConfirmPressed):
        effects.append(MainShellEffect(kind="show_entry_delete_confirm_dialog"))
        return next_state, effects

    if isinstance(intent, ReorderEntryUpPressed):
        effects.append(MainShellEffect(kind="run_reorder_entry", payload={"direction": "up"}))
        return next_state, effects

    if isinstance(intent, ReorderEntryDownPressed):
        effects.append(MainShellEffect(kind="run_reorder_entry", payload={"direction": "down"}))
        return next_state, effects

    if isinstance(intent, OpenManualCreateSessionPressed):
        effects.append(MainShellEffect(kind="show_session_form_dialog", payload={"mode": "create"}))
        return next_state, effects

    if isinstance(intent, OpenManualEditSessionPressed):
        effects.append(
            MainShellEffect(
                kind="show_session_form_dialog",
                payload={"mode": "edit", "session_id": intent.session_id},
            )
        )
        return next_state, effects

    if isinstance(intent, OpenManualDeleteSessionPressed):
        effects.append(
            MainShellEffect(
                kind="show_delete_session_confirm_dialog",
                payload={"session_id": intent.session_id},
            )
        )
        return next_state, effects

    if isinstance(intent, AdjustResourceDraftDeltaPressed):
        _apply_adjust_resource_draft_delta(next_state, intent.resource_key, intent.adjustment_delta)
        return next_state, effects

    if isinstance(intent, SaveResourceDraftPressed):
        if next_state.entry_panel_state.resource_draft_dirty:
            effects.append(MainShellEffect(kind="run_save_resource_draft"))
        return next_state, effects

    if isinstance(intent, DiscardResourceDraftPressed):
        _apply_discard_resource_draft(next_state)
        return next_state, effects

    return next_state, effects


def _queue_or_apply_context_intent(
    *,
    state: MainShellState,
    context_intent: MainShellIntent,
    action_label: str,
    apply_fn,
) -> tuple[MainShellState, list[MainShellEffect]]:
    effects: list[MainShellEffect] = []
    if has_dirty_resource_draft_attached_to_viewer(state):
        if state.workflow.resource_draft_leave_confirm_open:
            return state, effects
        state.workflow.pending_context_intent = context_intent
        state.workflow.pending_context_action_label = action_label
        state.workflow.resource_draft_leave_confirm_open = True
        effects.append(
            MainShellEffect(
                kind="show_resource_draft_leave_confirm_dialog",
                payload={"action_label": action_label},
            )
        )
        return state, effects
    return apply_fn(state, context_intent)


def _apply_prev_year(
    state: MainShellState,
    _intent: MainShellIntent,
) -> tuple[MainShellState, list[MainShellEffect]]:
    selected_year = state.local_state.selected_year
    years = state.read_state.years
    if selected_year is None or selected_year not in years:
        return state, []
    current_index = years.index(selected_year)
    if current_index <= 0:
        return state, []

    state.local_state.selected_year = years[current_index - 1]
    state.local_state.selected_week = None
    clear_all_write_errors(state)
    state.entry_panel_state.entries_for_selected_week = []
    state.entry_panel_state.entries_panel_error_message = None
    return state, [
        MainShellEffect(
            kind="refresh_data",
            payload={
                "selected_year_override": state.local_state.selected_year,
                "reload_q5": False,
                "reload_q8": False,
            },
        )
    ]


def _apply_next_year(
    state: MainShellState,
    _intent: MainShellIntent,
) -> tuple[MainShellState, list[MainShellEffect]]:
    selected_year = state.local_state.selected_year
    years = state.read_state.years
    if selected_year is None or selected_year not in years:
        return state, []
    current_index = years.index(selected_year)
    if current_index >= len(years) - 1:
        return state, []

    state.local_state.selected_year = years[current_index + 1]
    state.local_state.selected_week = None
    clear_all_write_errors(state)
    state.entry_panel_state.entries_for_selected_week = []
    state.entry_panel_state.entries_panel_error_message = None
    return state, [
        MainShellEffect(
            kind="refresh_data",
            payload={
                "selected_year_override": state.local_state.selected_year,
                "reload_q5": False,
                "reload_q8": False,
            },
        )
    ]


def _apply_select_week(
    state: MainShellState,
    context_intent: MainShellIntent,
) -> tuple[MainShellState, list[MainShellEffect]]:
    if not isinstance(context_intent, SelectWeekPressed):
        return state, []
    week_number = context_intent.week_number
    if state.local_state.selected_year is None:
        return state, []
    if not any(week.week_number == week_number for week in weeks_for_selected_year(state)):
        return state, []
    state.local_state.selected_week = week_number
    clear_all_write_errors(state)
    return state, [MainShellEffect(kind="load_entries_for_selected_week")]


def _apply_select_entry(
    state: MainShellState,
    context_intent: MainShellIntent,
) -> tuple[MainShellState, list[MainShellEffect]]:
    if not isinstance(context_intent, SelectEntryPressed):
        return state, []
    state.local_state.viewer_entry_ref = context_intent.entry_ref
    clear_all_write_errors(state)
    return state, [MainShellEffect(kind="load_viewer_entry_and_sessions")]


def _apply_manual_refresh(
    state: MainShellState,
    _intent: MainShellIntent,
) -> tuple[MainShellState, list[MainShellEffect]]:
    clear_all_write_errors(state)
    return state, [
        MainShellEffect(
            kind="refresh_data",
            payload={
                "selected_year_override": state.local_state.selected_year,
                "reload_q5": state.local_state.selected_week is not None,
                "reload_q8": state.local_state.viewer_entry_ref is not None,
            },
        )
    ]


def _apply_open_extend_year_dialog(
    state: MainShellState,
    _intent: MainShellIntent,
) -> tuple[MainShellState, list[MainShellEffect]]:
    return state, [MainShellEffect(kind="show_extend_year_plus_one_confirm_dialog")]


def _apply_adjust_resource_draft_delta(
    state: MainShellState,
    resource_key: str,
    adjustment_delta: int,
) -> None:
    entry_ref = state.local_state.viewer_entry_ref
    if entry_ref is None:
        state.entry_panel_state.resource_write_error_message = (
            "No hay entry en el visor para ajustar recursos."
        )
        return
    if state.entry_panel_state.resource_draft_entry_ref != entry_ref:
        state.entry_panel_state.resource_write_error_message = (
            "El borrador de recursos no coincide con la entry visible; refresca y reintenta."
        )
        return
    if resource_key not in {"lumber", "metal", "hide"}:
        state.entry_panel_state.resource_write_error_message = f"Recurso no soportado: {resource_key!r}."
        return
    if isinstance(adjustment_delta, bool) or not isinstance(adjustment_delta, int) or adjustment_delta == 0:
        state.entry_panel_state.resource_write_error_message = (
            "El ajuste de recurso debe ser entero distinto de 0."
        )
        return

    current_value = state.entry_panel_state.resource_draft_values.get(resource_key, 0)
    next_value = current_value + adjustment_delta
    if next_value == 0:
        state.entry_panel_state.resource_draft_values.pop(resource_key, None)
    else:
        state.entry_panel_state.resource_draft_values[resource_key] = next_value

    state.entry_panel_state.resource_draft_dirty = True
    state.entry_panel_state.resource_draft_discard_notice = None
    state.entry_panel_state.resource_write_error_message = None


def _apply_discard_resource_draft(state: MainShellState) -> None:
    state.workflow.pending_context_intent = None
    state.workflow.pending_context_action_label = None

    viewer = state.entry_panel_state.viewer_entry_snapshot
    entry_ref = state.local_state.viewer_entry_ref
    if viewer is None or entry_ref is None or viewer.ref != entry_ref:
        state.entry_panel_state.resource_draft_entry_ref = None
        state.entry_panel_state.resource_draft_values = {}
        state.entry_panel_state.resource_draft_dirty = False
        state.entry_panel_state.resource_draft_discard_notice = None
        state.entry_panel_state.resource_write_error_message = None
        return

    state.entry_panel_state.resource_draft_entry_ref = viewer.ref
    state.entry_panel_state.resource_draft_values = normalize_resource_draft_values(
        viewer.resource_deltas
    )
    state.entry_panel_state.resource_draft_dirty = False
    state.entry_panel_state.resource_draft_discard_notice = None
    state.entry_panel_state.resource_write_error_message = None

