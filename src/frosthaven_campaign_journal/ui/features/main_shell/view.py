from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.features.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.features.main_shell.state import MainShellState

TOP_BAR_HEIGHT = 64
BOTTOM_BAR_HEIGHT = 96


@ft.component
def build_main_shell_view(state: MainShellState) -> ft.Control:
    data = state.build_view_data()
    return ft.Pagelet(
        expand=True,
        appbar=ft.AppBar(
            toolbar_height=TOP_BAR_HEIGHT,
            automatically_imply_leading=False,
            leading_width=0,
            title_spacing=0,
            elevation=0,
            force_material_transparency=True,
            bgcolor="#F39A9A",
            title=_build_top_bar(data, state),
        ),
        bottom_appbar=ft.BottomAppBar(
            height=BOTTOM_BAR_HEIGHT,
            padding=ft.Padding(left=16, top=12, right=16, bottom=12),
            elevation=0,
            bgcolor="#36B7E6",
            content=_build_status_bar(data, state),
        ),
        content=ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    _build_week_tabs(data, state),
                    ft.Container(expand=True, padding=16, content=_build_center(data, state)),
                ],
            ),
        ),
    )


def _build_top_bar(data: MainShellViewData, state: MainShellState) -> ft.Control:
    year_label = f"Año {data.state.selected_year}" if data.state.selected_year else "Sin año"
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                spacing=8,
                controls=[
                    ft.FilledButton("←", on_click=state.on_prev_year),
                    ft.Text(year_label, size=18, weight=ft.FontWeight.BOLD),
                    ft.FilledButton("→", on_click=state.on_next_year),
                ],
            ),
            ft.Row(
                controls=[
                    ft.TextButton("Actualizar", on_click=state.on_manual_refresh),
                    ft.Text(f"env: {data.env_name}", size=12),
                ]
            ),
        ],
    )


def _build_week_tabs(data: MainShellViewData, state: MainShellState) -> ft.Control:
    chips: list[ft.Control] = []
    for week in data.weeks_for_selected_year:
        selected = week.week_number == data.state.selected_week
        chips.append(
            ft.OutlinedButton(
                f"W{week.week_number}",
                data=week.week_number,
                on_click=state.on_select_week_click,
                style=ft.ButtonStyle(
                    bgcolor="#F4A0A0" if selected else "#EFEFEF",
                    side=ft.BorderSide(2, "#4F46A5" if selected else "#CCCCCC"),
                ),
            )
        )
    return ft.Container(
        height=44,
        bgcolor="#EFEFEF",
        padding=ft.Padding(left=12, top=6, right=12, bottom=6),
        content=ft.Row(scroll=ft.ScrollMode.AUTO, spacing=8, controls=chips),
    )


def _build_center(data: MainShellViewData, state: MainShellState) -> ft.Control:
    return ft.ResponsiveRow(
        controls=[
            ft.Container(col={"xs": 12, "md": 4}, content=_build_entries(data, state)),
            ft.Container(col={"xs": 12, "md": 8}, content=_build_viewer(data, state)),
        ]
    )


def _build_entries(data: MainShellViewData, state: MainShellState) -> ft.Control:
    controls: list[ft.Control] = [ft.Text("Entries", size=16, weight=ft.FontWeight.BOLD)]
    for entry in data.entries_for_selected_week:
        controls.append(
            ft.ListTile(
                title=ft.Text(entry.label),
                subtitle=ft.Text(f"Week {entry.ref.week_number}"),
                data=entry.ref,
                on_click=state.on_select_entry_click,
            )
        )
    if not data.entries_for_selected_week:
        controls.append(ft.Text("Sin entries para esta week."))
    return ft.Card(content=ft.Container(padding=12, content=ft.Column(controls=controls)))


def _build_viewer(data: MainShellViewData, state: MainShellState) -> ft.Control:
    viewer = data.viewer_entry
    title = viewer.label if viewer else "Sin entry seleccionada"
    draft = data.resource_draft_values or {}
    resources = ft.Row(
        controls=[
            _resource_control("lumber", draft.get("lumber", 0), state),
            _resource_control("metal", draft.get("metal", 0), state),
            _resource_control("hide", draft.get("hide", 0), state),
        ]
    )
    return ft.Card(
        content=ft.Container(
            padding=12,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                    resources,
                    ft.Row(
                        controls=[
                            ft.OutlinedButton("Descartar", on_click=state.on_discard_resource_draft),
                            ft.FilledButton("Guardar", on_click=state.on_save_resource_draft),
                        ]
                    ),
                ],
            ),
        )
    )


def _resource_control(key: str, value: int, state: MainShellState) -> ft.Control:
    return ft.Row(
        spacing=4,
        controls=[
            ft.IconButton(
                icon=ft.Icons.REMOVE,
                data=(key, -1),
                on_click=state.on_adjust_resource_draft_delta_click,
            ),
            ft.Text(f"{key}: {value}"),
            ft.IconButton(
                icon=ft.Icons.ADD,
                data=(key, 1),
                on_click=state.on_adjust_resource_draft_delta_click,
            ),
        ],
    )


def _build_status_bar(data: MainShellViewData, state: MainShellState) -> ft.Control:
    msg = data.read_warning_message or data.read_error_message or "Listo"
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Text(msg, color="#111111"),
            ft.TextButton("+ Año", on_click=state.on_open_extend_year_plus_one_confirm),
        ],
    )
