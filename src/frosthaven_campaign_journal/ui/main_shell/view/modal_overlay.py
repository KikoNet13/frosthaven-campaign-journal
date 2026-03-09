from __future__ import annotations

from dataclasses import dataclass

import flet as ft

from frosthaven_campaign_journal.ui.common.components.dialogs import (
    build_dialog_button_style,
    build_modal_dialog_shell,
)
from frosthaven_campaign_journal.ui.common.theme.colors import COLOR_TEXT_PRIMARY
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.view.center_forms import (
    build_entry_form_dialog_body,
    build_entry_notes_dialog_body,
    build_session_form_dialog_body,
)

_NOTES_DIALOG_HEIGHT = 320


@dataclass
class _DialogDefinition:
    body: ft.Control
    actions: list[ft.Control]
    title: str | None = None
    height: int | None = None
    body_expand: bool = False


def build_main_shell_modal_overlay(data: MainShellViewData, state: MainShellState) -> ft.Control | None:
    dialog = _build_confirmation_dialog(data, state)
    if dialog is None:
        dialog = _build_entry_form_dialog(data, state)
    if dialog is None:
        dialog = _build_entry_notes_dialog(data, state)
    if dialog is None:
        dialog = _build_session_form_dialog(data, state)
    if dialog is None:
        return None
    return build_modal_dialog_shell(
        title=dialog.title,
        body=dialog.body,
        actions=dialog.actions,
        height=dialog.height,
        body_expand=dialog.body_expand,
    )


def _build_confirmation_dialog(data: MainShellViewData, state: MainShellState) -> _DialogDefinition | None:
    if data.confirmation_dialog is None:
        return None
    return _DialogDefinition(
        title=data.confirmation_dialog.title,
        body=ft.Text(data.confirmation_dialog.body, size=14, color=COLOR_TEXT_PRIMARY),
        actions=[
            _build_dialog_button("Cancelar", filled=False, on_click=state.on_cancel_pending_action),
            _build_dialog_button(
                data.confirmation_dialog.confirm_label,
                filled=True,
                on_click=state.on_confirm_pending_action,
            ),
        ],
    )


def _build_entry_form_dialog(data: MainShellViewData, state: MainShellState) -> _DialogDefinition | None:
    if data.entry_form is None:
        return None
    return _DialogDefinition(
        title="Crear entrada" if data.entry_form.mode == "create" else "Editar entrada",
        body=build_entry_form_dialog_body(data, state),
        actions=[
            _build_dialog_button("Cancelar", filled=False, on_click=state.on_cancel_entry_form),
            _build_dialog_button("Guardar", filled=True, on_click=state.on_submit_entry_form),
        ],
    )


def _build_entry_notes_dialog(data: MainShellViewData, state: MainShellState) -> _DialogDefinition | None:
    if data.entry_notes_editor is None:
        return None
    return _DialogDefinition(
        body=build_entry_notes_dialog_body(data, state),
        actions=[
            _build_dialog_button("Cancelar", filled=False, on_click=state.on_cancel_entry_notes_editor),
            _build_dialog_button("Guardar", filled=True, on_click=state.on_submit_entry_notes),
        ],
        height=_NOTES_DIALOG_HEIGHT,
        body_expand=True,
    )


def _build_session_form_dialog(data: MainShellViewData, state: MainShellState) -> _DialogDefinition | None:
    if data.session_form is None:
        return None
    return _DialogDefinition(
        title="Crear sesión manual" if data.session_form.mode == "create" else "Editar sesión",
        body=build_session_form_dialog_body(data, state),
        actions=[
            _build_dialog_button("Cancelar", filled=False, on_click=state.on_cancel_session_form),
            _build_dialog_button("Guardar", filled=True, on_click=state.on_submit_session_form),
        ],
    )


def _build_dialog_button(label: str, *, filled: bool, on_click) -> ft.Control:
    button_cls = ft.FilledButton if filled else ft.OutlinedButton
    return button_cls(
        label,
        style=build_dialog_button_style(filled=filled),
        on_click=on_click,
    )
