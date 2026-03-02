from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.state import MainShellState
from frosthaven_campaign_journal.ui.main_shell.view.theme import COLOR_WHITE


def build_status_bar(data: MainShellViewData, state: MainShellState) -> ft.Control:
    active_text, active_detail_text = _active_status_texts(data)
    viewer_text = (
        f"Viendo: {data.viewer_entry.label} (S{data.viewer_entry.ref.week_number})"
        if data.viewer_entry is not None
        else "Sin entrada en visor"
    )
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Text("Totales (solo lectura)", size=16, weight=ft.FontWeight.BOLD, color=COLOR_WHITE),
                    ft.Text(_format_resource_totals(data.campaign_resource_totals), size=12, color="#EAF9FF"),
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
                            ft.Text(active_text, size=13, weight=ft.FontWeight.BOLD, color=COLOR_WHITE, text_align=ft.TextAlign.RIGHT),
                            ft.Text(active_detail_text or viewer_text, size=12, color="#EAF9FF", text_align=ft.TextAlign.RIGHT),
                            ft.Text(f"{viewer_text} · env={data.env_name}", size=11, color="#DDF5FF", text_align=ft.TextAlign.RIGHT),
                        ],
                    ),
                    ft.Column(
                        spacing=6,
                        controls=[
                            ft.OutlinedButton("Actualizar", on_click=state.on_manual_refresh),
                        ],
                    ),
                ],
            ),
        ],
    )


def _active_status_texts(data: MainShellViewData) -> tuple[str, str]:
    if data.active_status_error_message:
        return ("Estado activo no disponible", data.active_status_error_message)
    if data.active_entry_ref is None:
        return ("Sin sesión activa", "")
    label = data.active_entry_label or f"Entrada {data.active_entry_ref.entry_id}"
    if data.viewer_entry is not None and data.viewer_entry.ref == data.active_entry_ref:
        return (f"Con sesión activa: {label} · aquí", "")
    return (f"Con sesión activa: {label} · en otra entrada", "")


def _format_resource_totals(resource_totals: dict[str, int] | None) -> str:
    if resource_totals is None:
        return "Totales no disponibles (Q1 no cargado)"
    if not resource_totals:
        return "Sin recursos materializados"
    items = sorted(resource_totals.items(), key=lambda item: item[0])
    visible = [f"{key}={value}" for key, value in items[:4]]
    suffix = " ..." if len(items) > 4 else ""
    return " · ".join(visible) + suffix
