from __future__ import annotations

from dataclasses import dataclass

import flet as ft

from frosthaven_campaign_journal.models import EntryRef, EntrySummary, ViewerSessionItem, WeekSummary
from frosthaven_campaign_journal.ui.common.components import LabeledGroupBox
from frosthaven_campaign_journal.ui.common.resources import ResourceDeltaRow, iter_resource_ui_groups
from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_BOTTOM_BAR_BG,
    COLOR_DESTRUCTIVE_ICON,
    COLOR_DEFEAT_ICON,
    COLOR_ENTRY_TAB_SELECTED_UNDERLINE,
    COLOR_ERROR_TEXT,
    COLOR_PANEL_BG,
    COLOR_PANEL_BORDER,
    COLOR_PANEL_INNER_BORDER,
    COLOR_STATUS_GROUP_BG,
    COLOR_STATUS_GROUP_BORDER,
    COLOR_STATUS_LABEL_BG,
    COLOR_STATUS_LABEL_BORDER,
    COLOR_STATUS_LABEL_TEXT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_VICTORY_ICON,
    COLOR_WHITE,
)
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData, WeekEntryCardViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.view.center_helpers import (
    _build_card,
    _format_session_line,
)

WEEK_ENTRY_CARD_WIDTH = 540
MAX_SESSIONS_PREVIEW = 8


@dataclass(frozen=True)
class _EntryCardStatusTexts:
    sessions_status: str


def _build_focus_empty_mode(_data: MainShellViewData) -> ft.Control:
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=ft.Text(
            "Selecciona una semana.",
            size=18,
            color=COLOR_TEXT_MUTED,
            text_align=ft.TextAlign.CENTER,
        ),
    )


def _build_focus_week_mode(data: MainShellViewData, state: MainShellState, _week: WeekSummary) -> ft.Control:
    return _build_week_cards_lane(data, state)


def _build_week_cards_lane(data: MainShellViewData, state: MainShellState) -> ft.Control:
    if data.entries_panel_error_message:
        return _build_card(
            title="Entradas de la semana",
            body=f"Error Q5: {data.entries_panel_error_message}",
        )

    if not data.week_entry_cards:
        return _build_card(
            title="Entradas de la semana",
            body="Semana sin entradas. Usa el botón + para crear un escenario o un puesto fronterizo.",
        )

    card_count = len(data.week_entry_cards)
    wrappers: list[ft.Control] = []
    for card_index, card in enumerate(data.week_entry_cards):
        card_control = _build_week_entry_card(
            data,
            state,
            card,
            card_index=card_index,
            card_count=card_count,
        )
        if card_count <= 2:
            wrappers.append(ft.Container(expand=1, content=card_control))
        else:
            wrappers.append(ft.Container(width=WEEK_ENTRY_CARD_WIDTH, content=card_control))

    return ft.Container(
        expand=True,
        content=ft.Row(
            expand=True,
            spacing=12,
            wrap=False,
            scroll=ft.ScrollMode.AUTO,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=wrappers,
        ),
    )


def _build_week_entry_card(
    data: MainShellViewData,
    state: MainShellState,
    card: WeekEntryCardViewData,
    *,
    card_index: int,
    card_count: int,
) -> ft.Control:
    active_border_color = COLOR_ENTRY_TAB_SELECTED_UNDERLINE if card.is_active_session_owner else COLOR_PANEL_BORDER
    status_texts = _build_entry_card_status_texts(data, card)

    return ft.Container(
        expand=True,
        padding=ft.Padding.all(12),
        bgcolor=COLOR_BOTTOM_BAR_BG,
        border=ft.Border.all(2 if card.is_active_session_owner else 1, active_border_color),
        border_radius=10,
        content=ft.Column(
            expand=True,
            spacing=10,
            controls=[
                _build_entry_card_header(
                    data,
                    state,
                    card,
                    can_move_left=(card_index > 0),
                    can_move_right=(card_index < card_count - 1),
                ),
                ft.Container(
                    expand=True,
                    content=ft.ListView(
                        expand=True,
                        spacing=10,
                        padding=0,
                        controls=[
                            _build_entry_resources_card(data, state, card),
                            _build_entry_sessions_card(data, state, card, status_texts.sessions_status),
                        ],
                    ),
                ),
            ],
        ),
    )


def _build_entry_card_header(
    data: MainShellViewData,
    state: MainShellState,
    card: WeekEntryCardViewData,
    *,
    can_move_left: bool,
    can_move_right: bool,
) -> ft.Control:
    entry = card.entry
    outcome_icon = _build_entry_outcome_icon(entry)
    title_controls: list[ft.Control] = [ft.Text(entry.label, size=18, weight=ft.FontWeight.BOLD, color=COLOR_WHITE)]
    if outcome_icon is not None:
        title_controls.append(outcome_icon)

    action_buttons: list[ft.Control] = [
        ft.IconButton(
            icon=ft.Icons.EDIT_NOTE,
            icon_size=18,
            icon_color=COLOR_WHITE,
            tooltip="Editar notas",
            data=entry.ref,
            on_click=state.on_open_entry_notes_editor_click,
            disabled=card.entry_write_pending,
        ),
    ]
    if card.resource_draft_dirty:
        action_buttons.extend(
            [
                ft.IconButton(
                    icon=ft.Icons.SAVE_OUTLINED,
                    icon_size=18,
                    icon_color=COLOR_WHITE,
                    tooltip="Guardar recursos",
                    on_click=lambda _event, entry_ref=entry.ref: state.on_save_resource_draft_for_entry(entry_ref),
                    disabled=card.resource_write_pending,
                ),
                ft.IconButton(
                    icon=ft.Icons.DO_NOT_DISTURB_ALT_OUTLINED,
                    icon_size=18,
                    icon_color=COLOR_WHITE,
                    tooltip="No guardar cambios de recursos",
                    on_click=lambda _event, entry_ref=entry.ref: state.on_discard_resource_draft_for_entry(entry_ref),
                    disabled=card.resource_write_pending,
                ),
            ]
        )

    action_buttons.append(
        ft.PopupMenuButton(
            icon=ft.Icons.MORE_HORIZ,
            icon_color=COLOR_WHITE,
            tooltip="Más acciones",
            items=[
                ft.PopupMenuItem(
                    icon=ft.Icons.ARROW_BACK,
                    text="Mover a la izquierda",
                    on_click=(
                        lambda _event, entry_ref=entry.ref: state.on_reorder_entry_left_for_entry(entry_ref)
                    ),
                    disabled=card.entry_write_pending or not can_move_left,
                ),
                ft.PopupMenuItem(
                    icon=ft.Icons.ARROW_FORWARD,
                    text="Mover a la derecha",
                    on_click=(
                        lambda _event, entry_ref=entry.ref: state.on_reorder_entry_right_for_entry(entry_ref)
                    ),
                    disabled=card.entry_write_pending or not can_move_right,
                ),
                ft.PopupMenuItem(
                    on_click=(
                        lambda _event, entry_ref=entry.ref: state.on_open_entry_delete_confirm_for_entry(entry_ref)
                    ),
                    disabled=card.entry_write_pending,
                    content=ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.DELETE_OUTLINE, size=18, color=COLOR_DESTRUCTIVE_ICON),
                            ft.Text("Eliminar entrada", color=COLOR_DESTRUCTIVE_ICON),
                        ],
                    ),
                ),
            ],
        )
    )

    return ft.Column(
        spacing=6,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        expand=True,
                        spacing=2,
                        controls=[
                            ft.Row(spacing=6, wrap=True, controls=title_controls),
                        ],
                    ),
                    ft.Row(spacing=2, controls=action_buttons),
                ],
            ),
        ],
    )


def _build_entry_resources_card(
    data: MainShellViewData,
    state: MainShellState,
    card: WeekEntryCardViewData,
) -> ft.Control:
    draft_controls_disabled = card.resource_write_pending
    campaign_resource_totals = data.campaign_resource_totals

    group_cards_by_key: dict[str, ft.Control] = {}
    for group in iter_resource_ui_groups():
        column_controls: list[ft.Control] = []
        for group_column in group.columns:
            resource_rows: list[ft.Control] = []
            for item in group_column:
                current_delta = card.resource_draft_values.get(item.key, 0)
                projected_total = (
                    None
                    if campaign_resource_totals is None
                    else campaign_resource_totals.get(item.key, 0) + current_delta
                )
                resource_rows.append(
                    ResourceDeltaRow(
                        resource_key=item.key,
                        label_es=item.label_es,
                        icon_src=item.icon_src,
                        delta_value=current_delta,
                        projected_total=projected_total,
                        disabled=draft_controls_disabled,
                        on_decrement_click=(
                            lambda _event, entry_ref=card.entry.ref, key=item.key: state.on_adjust_resource_draft_delta_for_entry(
                                entry_ref,
                                key,
                                -1,
                            )
                        ),
                        on_increment_click=(
                            lambda _event, entry_ref=card.entry.ref, key=item.key: state.on_adjust_resource_draft_delta_for_entry(
                                entry_ref,
                                key,
                                1,
                            )
                        ),
                    )
                )
            column_controls.append(ft.Column(spacing=6, expand=True, controls=resource_rows))

        group_content: ft.Control
        if len(column_controls) == 1:
            group_content = column_controls[0]
        else:
            group_content = ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=column_controls,
            )

        group_cards_by_key[group.key] = LabeledGroupBox(
            label=group.label_es,
            content=group_content,
            bgcolor=COLOR_STATUS_GROUP_BG,
            border_color=COLOR_STATUS_GROUP_BORDER,
            label_bgcolor=COLOR_STATUS_LABEL_BG,
            label_border_color=COLOR_STATUS_LABEL_BORDER,
            label_text_color=COLOR_STATUS_LABEL_TEXT,
            padding=ft.Padding(left=8, top=10, right=8, bottom=8),
        )

    layout_rows: list[ft.Control] = []

    if card.resource_write_error_message:
        layout_rows.append(ft.Text(card.resource_write_error_message, size=12, color=COLOR_ERROR_TEXT))

    first_row_boxes: list[ft.Control] = []
    for group_key in ("others", "materials"):
        group_box = group_cards_by_key.get(group_key)
        if group_box is not None:
            first_row_boxes.append(ft.Container(expand=1, content=group_box))

    if first_row_boxes:
        layout_rows.append(
            ft.Row(
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=first_row_boxes,
            )
        )

    plants_box = group_cards_by_key.get("plants")
    if plants_box is not None:
        layout_rows.append(plants_box)

    return ft.Column(
        spacing=8,
        controls=layout_rows,
    )


def _build_entry_sessions_card(
    data: MainShellViewData,
    state: MainShellState,
    card: WeekEntryCardViewData,
    status_line: str,
) -> ft.Control:
    has_active_session = any(session.ended_at_utc is None for session in card.sessions)

    rows: list[ft.Control] = []
    for session in card.sessions[:MAX_SESSIONS_PREVIEW]:
        rows.append(_build_session_row(state, card.entry.ref, session, card.session_write_pending))

    if len(card.sessions) > MAX_SESSIONS_PREVIEW:
        rows.append(
            ft.Text(
                f"… y {len(card.sessions) - MAX_SESSIONS_PREVIEW} sesión(es) más",
                size=11,
                color=COLOR_TEXT_MUTED,
            )
        )

    if card.sessions_error_message:
        rows.insert(0, ft.Text(f"Error Q8: {card.sessions_error_message}", size=12, color=COLOR_ERROR_TEXT))

    controls: list[ft.Control] = [
        ft.Text(status_line, size=12, color=COLOR_TEXT_MUTED),
        ft.Text(f"Total jugado (Q8): {card.sessions_total_text}", size=12, color=COLOR_TEXT_MUTED),
        ft.Row(
            spacing=8,
            wrap=True,
            controls=[
                ft.FilledButton(
                    "Iniciar",
                    on_click=lambda _event, entry_ref=card.entry.ref: state.on_start_session_for_entry(entry_ref),
                    disabled=card.session_write_pending,
                    height=32,
                ),
                ft.OutlinedButton(
                    "Detener",
                    on_click=lambda _event, entry_ref=card.entry.ref: state.on_stop_session_for_entry(entry_ref),
                    disabled=card.session_write_pending or not has_active_session,
                    height=32,
                ),
                ft.OutlinedButton(
                    "Nueva sesión",
                    on_click=(
                        lambda _event, entry_ref=card.entry.ref: state.on_open_manual_create_session_for_entry(entry_ref)
                    ),
                    disabled=card.session_write_pending,
                    height=32,
                ),
            ],
        ),
    ]

    controls.extend(rows)

    return LabeledGroupBox(
        label="Sesiones",
        content=ft.Column(spacing=8, controls=controls),
        bgcolor=COLOR_STATUS_GROUP_BG,
        border_color=COLOR_STATUS_GROUP_BORDER,
        label_bgcolor=COLOR_STATUS_LABEL_BG,
        label_border_color=COLOR_STATUS_LABEL_BORDER,
        label_text_color=COLOR_STATUS_LABEL_TEXT,
        padding=ft.Padding.all(12),
    )


def _build_session_row(
    state: MainShellState,
    entry_ref: EntryRef,
    session: ViewerSessionItem,
    is_pending: bool,
) -> ft.Control:
    return ft.Container(
        padding=ft.Padding(left=8, top=6, right=8, bottom=6),
        bgcolor=COLOR_PANEL_BG,
        border=ft.Border.all(1, COLOR_PANEL_INNER_BORDER),
        border_radius=6,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(_format_session_line(session), size=12, color=COLOR_TEXT_PRIMARY),
                ft.Row(
                    spacing=4,
                    controls=[
                        ft.OutlinedButton(
                            "Editar",
                            on_click=(
                                lambda _event, ref=entry_ref, session_id=session.session_id: state.on_open_manual_edit_session_for_entry(
                                    ref,
                                    session_id,
                                )
                            ),
                            disabled=is_pending,
                            height=30,
                        ),
                        ft.OutlinedButton(
                            "Borrar",
                            on_click=(
                                lambda _event, ref=entry_ref, session_id=session.session_id: state.on_open_manual_delete_session_for_entry(
                                    ref,
                                    session_id,
                                )
                            ),
                            disabled=is_pending,
                            height=30,
                        ),
                    ],
                ),
            ],
        ),
    )


def _build_entry_outcome_icon(entry: EntrySummary) -> ft.Control | None:
    if entry.entry_type != "scenario":
        return None
    if entry.scenario_outcome == "victory":
        return ft.Icon(ft.Icons.CHECK_CIRCLE, size=18, color=COLOR_VICTORY_ICON, tooltip="Victoria")
    if entry.scenario_outcome == "defeat":
        return ft.Icon(ft.Icons.CANCEL, size=18, color=COLOR_DEFEAT_ICON, tooltip="Derrota")
    return None


def _build_entry_card_status_texts(
    data: MainShellViewData,
    card: WeekEntryCardViewData,
) -> _EntryCardStatusTexts:
    if data.active_entry_ref is None:
        sessions_status = "Sin sesión activa real."
    elif card.is_active_session_owner:
        sessions_status = f"Con sesión activa aquí: {data.active_entry_label or card.entry.label}."
    else:
        sessions_status = f"Con sesión activa en otra entrada: {data.active_entry_label or 'Entrada activa'}."

    return _EntryCardStatusTexts(
        sessions_status=sessions_status,
    )
