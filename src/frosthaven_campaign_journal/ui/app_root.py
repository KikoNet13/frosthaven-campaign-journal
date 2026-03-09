from __future__ import annotations

import asyncio
from concurrent.futures import Future
from typing import Callable

import flet as ft

from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_BANNER_INFO_BG,
    COLOR_BANNER_INFO_TEXT,
)
from frosthaven_campaign_journal.ui.common.theme.layout import BOTTOM_BAR_HEIGHT
from frosthaven_campaign_journal.ui.main_shell import MainShellState, build_main_shell_view
from frosthaven_campaign_journal.ui.main_shell.view.modal_overlay import (
    build_main_shell_modal_overlay,
)

_SNACKBAR_SIDE_MARGIN = 16
_SNACKBAR_BOTTOM_MARGIN = BOTTOM_BAR_HEIGHT + 24


def _close_overlay(overlay: ft.SnackBar | None) -> None:
    if overlay is None or not overlay.open:
        return
    overlay.open = False
    overlay.update()


@ft.component
def build_app_root(page: ft.Page) -> ft.Control:
    shell_state, _ = ft.use_state(MainShellState.create)
    _live_session_tick, set_live_session_tick = ft.use_state(0)
    active_toast = ft.use_ref(None)
    last_toast_event_id = ft.use_ref(None)
    active_session_ticker = ft.use_ref(None)

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

    def _sync_live_session_ticker() -> Callable[[], None] | None:
        current_future: Future[None] | None = active_session_ticker.current
        if current_future is not None and not current_future.done():
            current_future.cancel()
        active_session_ticker.current = None

        if shell_state.read_state.active_session_started_at_utc is None:
            return None

        async def _run_live_session_ticker() -> None:
            try:
                while shell_state.read_state.active_session_started_at_utc is not None:
                    await asyncio.sleep(1)
                    set_live_session_tick(lambda current: current + 1)
            except asyncio.CancelledError:
                pass

        future = page.run_task(_run_live_session_ticker)
        active_session_ticker.current = future

        def _cleanup_live_session_ticker() -> None:
            cleanup_future: Future[None] | None = active_session_ticker.current
            if cleanup_future is not None and not cleanup_future.done():
                cleanup_future.cancel()
            active_session_ticker.current = None

        return _cleanup_live_session_ticker

    ft.use_effect(
        _sync_live_session_ticker,
        dependencies=[shell_state.read_state.active_session_started_at_utc],
    )

    data = shell_state.build_view_data()
    stack_controls: list[ft.Control] = [build_main_shell_view(shell_state, data=data)]
    modal_overlay = build_main_shell_modal_overlay(data, shell_state)
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
