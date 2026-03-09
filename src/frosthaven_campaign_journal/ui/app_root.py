from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_ACCENT_BG,
    COLOR_BANNER_INFO_BG,
    COLOR_BANNER_INFO_TEXT,
    COLOR_PANEL_INNER_BG,
    COLOR_TEXT_HEADING,
    COLOR_TEXT_PRIMARY,
    COLOR_WHITE,
)
from frosthaven_campaign_journal.ui.common.theme.layout import BOTTOM_BAR_HEIGHT
from frosthaven_campaign_journal.ui.main_shell import MainShellState, build_main_shell_view
from frosthaven_campaign_journal.ui.main_shell.view.center_forms import build_form_modal_overlay

_SNACKBAR_SIDE_MARGIN = 16
_SNACKBAR_BOTTOM_MARGIN = BOTTOM_BAR_HEIGHT + 24


def _close_overlay(overlay: ft.AlertDialog | ft.SnackBar | None) -> None:
    if overlay is None or not overlay.open:
        return
    overlay.open = False
    overlay.update()


def _build_dialog_button_style(*, filled: bool) -> ft.ButtonStyle:
    return ft.ButtonStyle(
        bgcolor=COLOR_ACCENT_BG if filled else None,
        color=COLOR_WHITE if filled else COLOR_ACCENT_BG,
        side=None if filled else ft.BorderSide(1.25, COLOR_ACCENT_BG),
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.Padding(left=16, top=12, right=16, bottom=12),
    )


@ft.component
def build_app_root(page: ft.Page) -> ft.Control:
    shell_state, _ = ft.use_state(MainShellState.create)
    active_toast = ft.use_ref(None)
    last_toast_event_id = ft.use_ref(None)
    active_confirmation = ft.use_ref(None)
    last_confirmation_event_id = ft.use_ref(None)

    def _sync_info_toast() -> None:
        toast = shell_state.toast_state
        if toast.event_id is None or not toast.message or toast.event_id == last_toast_event_id.current:
            return

        last_toast_event_id.current = toast.event_id
        _close_overlay(active_toast.current)

        def _on_dismiss(_event: ft.ControlEvent) -> None:
            if active_toast.current is snackbar:
                active_toast.current = None
            if shell_state.toast_state.event_id == toast.event_id:
                shell_state._clear_info_toast(event_id=toast.event_id)
                shell_state.notify()

        snackbar = ft.SnackBar(
            bgcolor=COLOR_BANNER_INFO_BG,
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.INFO_OUTLINE, color=COLOR_BANNER_INFO_TEXT, size=18),
                    ft.Text(toast.message, color=COLOR_BANNER_INFO_TEXT, expand=True),
                ],
            ),
            behavior=ft.SnackBarBehavior.FLOATING,
            show_close_icon=True,
            close_icon_color=COLOR_BANNER_INFO_TEXT,
            margin=ft.Margin(
                left=_SNACKBAR_SIDE_MARGIN,
                top=0,
                right=_SNACKBAR_SIDE_MARGIN,
                bottom=_SNACKBAR_BOTTOM_MARGIN,
            ),
            on_dismiss=_on_dismiss,
        )
        active_toast.current = snackbar
        page.show_dialog(snackbar)

    ft.use_effect(_sync_info_toast, dependencies=[shell_state.toast_state.event_id])

    def _sync_confirmation_dialog() -> None:
        confirmation = shell_state.confirmation_state
        if (
            confirmation.key is None
            or confirmation.event_id is None
            or confirmation.event_id == last_confirmation_event_id.current
        ):
            return

        last_confirmation_event_id.current = confirmation.event_id
        _close_overlay(active_confirmation.current)
        handled = {"value": False}

        def _handle_cancel(_event: ft.ControlEvent | None = None) -> None:
            handled["value"] = True
            _close_overlay(dialog)
            shell_state.on_cancel_pending_action()

        def _handle_confirm(_event: ft.ControlEvent | None = None) -> None:
            handled["value"] = True
            _close_overlay(dialog)
            shell_state.on_confirm_pending_action()

        def _on_dismiss(_event: ft.ControlEvent) -> None:
            if active_confirmation.current is dialog:
                active_confirmation.current = None
            if handled["value"]:
                return
            handled["value"] = True
            if (
                shell_state.confirmation_state.key == confirmation.key
                and shell_state.confirmation_state.event_id == confirmation.event_id
            ):
                shell_state.on_cancel_pending_action()

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor=COLOR_PANEL_INNER_BG,
            title=ft.Text(
                confirmation.title,
                size=18,
                weight=ft.FontWeight.W_600,
                color=COLOR_TEXT_HEADING,
            ),
            content=ft.Text(confirmation.body, size=14, color=COLOR_TEXT_PRIMARY),
            actions=[
                ft.OutlinedButton(
                    "Cancelar",
                    style=_build_dialog_button_style(filled=False),
                    on_click=_handle_cancel,
                ),
                ft.FilledButton(
                    confirmation.confirm_label,
                    style=_build_dialog_button_style(filled=True),
                    on_click=_handle_confirm,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=_on_dismiss,
        )
        active_confirmation.current = dialog
        page.show_dialog(dialog)

    ft.use_effect(_sync_confirmation_dialog, dependencies=[shell_state.confirmation_state.event_id])

    data = shell_state.build_view_data()
    stack_controls: list[ft.Control] = [build_main_shell_view(shell_state, data=data)]
    modal_overlay = build_form_modal_overlay(data, shell_state)
    if modal_overlay is not None:
        stack_controls.append(modal_overlay)

    return ft.Container(
        expand=True,
        content=ft.SafeArea(
            expand=True,
            content=ft.Stack(
                expand=True,
                controls=stack_controls,
            ),
        ),
    )
