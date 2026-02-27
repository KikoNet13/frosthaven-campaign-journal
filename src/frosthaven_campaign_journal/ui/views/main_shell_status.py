from __future__ import annotations

from typing import Callable

import flet as ft

from frosthaven_campaign_journal.state.placeholders import EntryRef
from frosthaven_campaign_journal.ui.views.main_shell_contracts import (
    MainShellViewActions,
    MainShellViewData,
)
from frosthaven_campaign_journal.ui.views.main_shell_shared import (
    COLOR_WHITE,
    entry_short_label,
    truncate,
)


def build_bottom_status_bar_content(
    *,
    data: MainShellViewData,
    actions: MainShellViewActions,
) -> ft.Control:
    active_text, active_detail_text = _active_status_texts(
        active_entry_ref=data.active_entry_ref,
        active_entry_label=data.active_entry_label,
        active_status_error_message=data.active_status_error_message,
        viewer_entry=data.viewer_entry,
    )
    viewer_text = (
        f"Viendo: {entry_short_label(data.viewer_entry)}"
        if data.viewer_entry is not None
        else "Sin entry en visor"
    )

    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Text(
                        "Totales (read-only)",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_WHITE,
                    ),
                    ft.Text(
                        _format_resource_totals(data.campaign_resource_totals),
                        size=12,
                        color="#EAF9FF",
                    ),
                ],
            ),
            ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        controls=[
                            ft.Text(
                                active_text,
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_WHITE,
                                text_align=ft.TextAlign.RIGHT,
                            ),
                            ft.Text(
                                active_detail_text or viewer_text,
                                size=12,
                                color="#EAF9FF",
                                text_align=ft.TextAlign.RIGHT,
                            ),
                            ft.Text(
                                f"{viewer_text} · env={data.env_name}",
                                size=11,
                                color="#DDF5FF",
                                text_align=ft.TextAlign.RIGHT,
                            ),
                        ],
                    ),
                    _build_refresh_button(actions.on_manual_refresh),
                ],
            ),
        ],
    )


def _build_refresh_button(on_click: Callable[[], None]) -> ft.Control:
    return ft.Container(
        padding=ft.Padding(left=10, top=8, right=10, bottom=8),
        bgcolor="#21A4D3",
        border_radius=8,
        border=ft.Border.all(1, "#BFEFFF"),
        on_click=lambda _e: on_click(),
        content=ft.Text(
            "Refresh",
            size=12,
            weight=ft.FontWeight.BOLD,
            color=COLOR_WHITE,
        ),
    )


def _active_status_texts(
    *,
    active_entry_ref: EntryRef | None,
    active_entry_label: str | None,
    active_status_error_message: str | None,
    viewer_entry: object | None,
) -> tuple[str, str]:
    if active_status_error_message:
        return (
            "Estado activo no disponible",
            truncate(active_status_error_message, 80),
        )

    if active_entry_ref is None:
        return ("Sin sesión activa", "")

    label = active_entry_label or f"Entry {active_entry_ref.entry_id}"
    if viewer_entry is not None and viewer_entry.ref == active_entry_ref:
        return (f"Con sesión activa: {label} · aquí", "")
    return (f"Con sesión activa: {label} · en otra entry", "")


def _format_resource_totals(resource_totals: dict[str, int] | None) -> str:
    if resource_totals is None:
        return "Totales no disponibles (Q1 no cargado)"
    if not resource_totals:
        return "Sin recursos materializados"

    items = sorted(resource_totals.items(), key=lambda item: item[0])
    visible = [f"{key}={value}" for key, value in items[:4]]
    suffix = " …" if len(items) > 4 else ""
    return " · ".join(visible) + suffix

