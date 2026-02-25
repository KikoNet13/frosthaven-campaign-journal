from __future__ import annotations

from enum import Enum

import flet as ft


TOP_BAR_HEIGHT = 64
ENTRY_TABS_BAR_HEIGHT = 44
BOTTOM_BAR_HEIGHT = 96
OUTER_PADDING = 0
CENTER_PANEL_PADDING = 16

COLOR_TOP_BAR_BG = "#F39A9A"
COLOR_TOP_NAV_BUTTON_BG = "#5F58C8"
COLOR_WEEK_TILE_BG = "#F4A0A0"
COLOR_WEEK_TILE_CURRENT_BG = "#BFD7D0"
COLOR_WEEK_TILE_SELECTED_BORDER = "#4F46A5"
COLOR_ENTRY_TABS_BG = "#EFEFEF"
COLOR_ENTRY_TAB_SELECTED_UNDERLINE = "#6D5BD6"
COLOR_CENTER_BG = "#E6E6E6"
COLOR_BOTTOM_BAR_BG = "#36B7E6"
COLOR_TEXT_PRIMARY = "#111111"
COLOR_TEXT_MUTED = "#555555"
COLOR_WHITE = "#FFFFFF"


class ShellPreviewState(str, Enum):
    NO_SELECTION = "no_selection"
    WEEK_SELECTED = "week_selected"
    ENTRY_SELECTED = "entry_selected"


DEFAULT_SHELL_PREVIEW_STATE = ShellPreviewState.NO_SELECTION

_MOCK_WEEK_NUMBERS = list(range(21, 41))
_CURRENT_WEEK_NUMBER = 35
_WEEK_SELECTED_NUMBER = 35
_ENTRY_SELECTED_WEEK_NUMBER = 36


def build_main_shell_view(preview_state: ShellPreviewState, env_name: str) -> ft.Control:
    return ft.Container(
        expand=True,
        padding=OUTER_PADDING,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                _build_top_temporal_bar(preview_state),
                _build_entry_tabs_bar(preview_state),
                _build_center_focus_panel(preview_state),
                _build_bottom_status_bar(env_name),
            ],
        ),
    )


def _build_top_temporal_bar(preview_state: ShellPreviewState) -> ft.Control:
    selected_week_number = _selected_week_number(preview_state)

    return ft.Container(
        height=TOP_BAR_HEIGHT,
        bgcolor=COLOR_TOP_BAR_BG,
        padding=ft.Padding(left=12, top=10, right=12, bottom=10),
        content=ft.Row(
            spacing=16,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        _build_year_nav_button("←"),
                        ft.Text(
                            "Año 2",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_TEXT_PRIMARY,
                        ),
                        _build_year_nav_button("→"),
                    ],
                ),
                ft.Container(
                    expand=True,
                    content=ft.Row(
                        spacing=6,
                        wrap=False,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            _build_week_tile(
                                week_number=week_number,
                                is_current=(week_number == _CURRENT_WEEK_NUMBER),
                                is_selected=(week_number == selected_week_number),
                            )
                            for week_number in _MOCK_WEEK_NUMBERS
                        ],
                    ),
                ),
            ],
        ),
    )


def _build_year_nav_button(label: str) -> ft.Control:
    return ft.Container(
        width=42,
        height=42,
        bgcolor=COLOR_TOP_NAV_BUTTON_BG,
        border_radius=999,
        alignment=ft.Alignment.CENTER,
        content=ft.Text(
            label,
            size=20,
            weight=ft.FontWeight.BOLD,
            color=COLOR_WHITE,
        ),
    )


def _build_week_tile(week_number: int, is_current: bool, is_selected: bool) -> ft.Control:
    border = ft.border.all(2, COLOR_WEEK_TILE_SELECTED_BORDER) if is_selected else None
    bgcolor = COLOR_WEEK_TILE_CURRENT_BG if is_current else COLOR_WEEK_TILE_BG
    return ft.Container(
        width=46,
        height=42,
        bgcolor=bgcolor,
        border=border,
        border_radius=2,
        alignment=ft.Alignment.CENTER,
        content=ft.Text(
            str(week_number),
            size=13,
            weight=ft.FontWeight.W_600,
            color=COLOR_TEXT_PRIMARY,
        ),
    )


def _build_entry_tabs_bar(preview_state: ShellPreviewState) -> ft.Control:
    has_selected_week = preview_state in (
        ShellPreviewState.WEEK_SELECTED,
        ShellPreviewState.ENTRY_SELECTED,
    )
    has_selected_entry = preview_state == ShellPreviewState.ENTRY_SELECTED
    tabs = ["Escenario 51", "Escenario 42", "Puesto fronterizo"]

    return ft.Container(
        height=ENTRY_TABS_BAR_HEIGHT,
        bgcolor=COLOR_ENTRY_TABS_BG,
        padding=ft.Padding(left=16, top=4, right=16, bottom=4),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=8,
            controls=[
                _build_entry_tab(
                    label=label,
                    is_selected=has_selected_entry and index == 0,
                    is_dimmed=not has_selected_week,
                )
                for index, label in enumerate(tabs)
            ],
        ),
    )


def _build_entry_tab(label: str, is_selected: bool, is_dimmed: bool) -> ft.Control:
    underline_color = COLOR_ENTRY_TAB_SELECTED_UNDERLINE if is_selected else "transparent"
    text_color = COLOR_TEXT_MUTED if is_dimmed else COLOR_TEXT_PRIMARY
    text_weight = ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL
    underline_width = max(36, min(110, len(label) * 7))

    return ft.Container(
        padding=ft.Padding(left=12, top=6, right=12, bottom=2),
        content=ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(label, size=13, color=text_color, weight=text_weight),
                ft.Container(
                    width=underline_width,
                    height=2,
                    bgcolor=underline_color,
                    border_radius=1,
                ),
            ],
        ),
    )


def _build_center_focus_panel(preview_state: ShellPreviewState) -> ft.Control:
    return ft.Container(
        expand=True,
        bgcolor=COLOR_CENTER_BG,
        padding=ft.Padding.all(CENTER_PANEL_PADDING),
        content=_build_focus_placeholder(preview_state),
    )


def _build_focus_placeholder(preview_state: ShellPreviewState) -> ft.Control:
    if preview_state == ShellPreviewState.NO_SELECTION:
        return ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    "Sin week seleccionada",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_TEXT_PRIMARY,
                ),
                ft.Text(
                    "El panel central mostrará el foco de week o entry en los siguientes slices.",
                    size=14,
                    color=COLOR_TEXT_MUTED,
                ),
            ],
        )

    if preview_state == ShellPreviewState.WEEK_SELECTED:
        return ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            f"Week {_WEEK_SELECTED_NUMBER}",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_TEXT_PRIMARY,
                        ),
                        _build_badge("open", "#D9F2D9", "#237A3B"),
                    ],
                ),
                _build_placeholder_card(
                    title="Notas de la week (placeholder)",
                    body=(
                        "Aquí se mostrarán status y notes de la week seleccionada "
                        "cuando se conecten estado real y lecturas."
                    ),
                    min_height=120,
                ),
                _build_placeholder_card(
                    title="Sin entry seleccionada",
                    body=(
                        "Los tabs de entry están visibles, pero el detalle de entry "
                        "se activará cuando se seleccione una entry (#53/#54)."
                    ),
                    min_height=100,
                ),
            ],
        )

    return ft.Column(
        spacing=12,
        controls=[
            ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Week 36 · Escenario 51",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXT_PRIMARY,
                    ),
                    _build_badge("entry", "#E7E0FF", "#4F46A5"),
                ],
            ),
            _build_placeholder_card(
                title="Detalle de entry (placeholder)",
                body=(
                    "Tipo, referencia de escenario y datos de entry se conectarán "
                    "en los siguientes slices read-only."
                ),
                min_height=110,
            ),
            _build_placeholder_card(
                title="Sesión activa / historial (placeholder)",
                body=(
                    "El bloque de sesión irá aquí (start/stop real fuera de #52, "
                    "datos reales en #54+)."
                ),
                min_height=90,
            ),
            _build_placeholder_card(
                title="Recursos de la entry (placeholder)",
                body="Resumen y edición de recursos se conectan en la ola de recursos.",
                min_height=80,
            ),
        ],
    )


def _build_badge(label: str, background: str, foreground: str) -> ft.Control:
    return ft.Container(
        padding=ft.Padding(left=8, top=4, right=8, bottom=4),
        bgcolor=background,
        border_radius=999,
        content=ft.Text(
            label,
            size=12,
            color=foreground,
            weight=ft.FontWeight.W_500,
        ),
    )


def _build_placeholder_card(title: str, body: str, min_height: int) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border_radius=8,
        border=ft.border.all(1, "#D6D6D6"),
        content=ft.Column(
            spacing=6,
            controls=[
                ft.Text(
                    title,
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_TEXT_PRIMARY,
                ),
                ft.Container(
                    height=min_height,
                    padding=ft.Padding.all(8),
                    bgcolor="#FFFFFF",
                    border_radius=6,
                    content=ft.Text(body, size=13, color=COLOR_TEXT_MUTED),
                ),
            ],
        ),
    )


def _build_bottom_status_bar(env_name: str) -> ft.Control:
    return ft.Container(
        height=BOTTOM_BAR_HEIGHT,
        bgcolor=COLOR_BOTTOM_BAR_BG,
        padding=ft.Padding(left=16, top=12, right=16, bottom=12),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            "Totales (placeholder)",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_WHITE,
                        ),
                        ft.Text(
                            "Los totales reales se conectarán con lecturas read-only.",
                            size=12,
                            color="#EAF9FF",
                        ),
                    ],
                ),
                ft.Column(
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.Text(
                            "Activo global (placeholder)",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_WHITE,
                        ),
                        ft.Text(
                            f"Sin sesión activa · env={env_name}",
                            size=12,
                            color="#EAF9FF",
                        ),
                    ],
                ),
            ],
        ),
    )


def _selected_week_number(preview_state: ShellPreviewState) -> int | None:
    if preview_state == ShellPreviewState.WEEK_SELECTED:
        return _WEEK_SELECTED_NUMBER
    if preview_state == ShellPreviewState.ENTRY_SELECTED:
        return _ENTRY_SELECTED_WEEK_NUMBER
    return None
