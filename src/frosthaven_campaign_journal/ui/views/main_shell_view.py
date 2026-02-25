from __future__ import annotations

from typing import Callable

import flet as ft

from frosthaven_campaign_journal.state.placeholders import (
    EntryRef,
    MainScreenLocalState,
    MockEntry,
    MockWeek,
)


TOP_BAR_HEIGHT = 64
ENTRY_TABS_BAR_HEIGHT = 44
BOTTOM_BAR_HEIGHT = 96
OUTER_PADDING = 0
CENTER_PANEL_PADDING = 16

COLOR_TOP_BAR_BG = "#F39A9A"
COLOR_TOP_NAV_BUTTON_BG = "#5F58C8"
COLOR_TOP_NAV_BUTTON_DISABLED_BG = "#8E88D8"
COLOR_WEEK_TILE_BG = "#F4A0A0"
COLOR_WEEK_TILE_CLOSED_BG = "#E6B7B7"
COLOR_WEEK_TILE_SELECTED_BORDER = "#4F46A5"
COLOR_ENTRY_TABS_BG = "#EFEFEF"
COLOR_ENTRY_TAB_SELECTED_UNDERLINE = "#6D5BD6"
COLOR_CENTER_BG = "#E6E6E6"
COLOR_BOTTOM_BAR_BG = "#36B7E6"
COLOR_TEXT_PRIMARY = "#111111"
COLOR_TEXT_MUTED = "#555555"
COLOR_TEXT_DIMMED = "#7A6E6E"
COLOR_WHITE = "#FFFFFF"


def build_main_shell_view(
    *,
    state: MainScreenLocalState,
    years: list[int],
    weeks_for_selected_year: list[MockWeek],
    entries_for_selected_week: list[MockEntry],
    viewer_entry: MockEntry | None,
    active_entry_mock: MockEntry | None,
    env_name: str,
    on_prev_year: Callable[[], None],
    on_next_year: Callable[[], None],
    on_select_week: Callable[[int], None],
    on_select_entry: Callable[[EntryRef], None],
) -> ft.Control:
    return ft.Container(
        expand=True,
        padding=OUTER_PADDING,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                _build_top_temporal_bar(
                    state=state,
                    years=years,
                    weeks_for_selected_year=weeks_for_selected_year,
                    on_prev_year=on_prev_year,
                    on_next_year=on_next_year,
                    on_select_week=on_select_week,
                ),
                _build_entry_tabs_bar(
                    state=state,
                    entries_for_selected_week=entries_for_selected_week,
                    viewer_entry=viewer_entry,
                    on_select_entry=on_select_entry,
                ),
                _build_center_focus_panel(
                    state=state,
                    weeks_for_selected_year=weeks_for_selected_year,
                    viewer_entry=viewer_entry,
                    active_entry_mock=active_entry_mock,
                ),
                _build_bottom_status_bar(
                    env_name=env_name,
                    viewer_entry=viewer_entry,
                    active_entry_mock=active_entry_mock,
                ),
            ],
        ),
    )


def _build_top_temporal_bar(
    *,
    state: MainScreenLocalState,
    years: list[int],
    weeks_for_selected_year: list[MockWeek],
    on_prev_year: Callable[[], None],
    on_next_year: Callable[[], None],
    on_select_week: Callable[[int], None],
) -> ft.Control:
    has_prev_year = years.index(state.selected_year) > 0
    has_next_year = years.index(state.selected_year) < len(years) - 1

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
                        _build_year_nav_button("←", on_prev_year if has_prev_year else None),
                        ft.Text(
                            f"Año {state.selected_year}",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_TEXT_PRIMARY,
                        ),
                        _build_year_nav_button("→", on_next_year if has_next_year else None),
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
                                week=week,
                                is_selected=(week.week_number == state.selected_week),
                                on_select_week=on_select_week,
                            )
                            for week in weeks_for_selected_year
                        ],
                    ),
                ),
            ],
        ),
    )


def _build_year_nav_button(label: str, on_click: Callable[[], None] | None) -> ft.Control:
    enabled = on_click is not None
    return ft.Container(
        width=42,
        height=42,
        bgcolor=COLOR_TOP_NAV_BUTTON_BG if enabled else COLOR_TOP_NAV_BUTTON_DISABLED_BG,
        border_radius=999,
        alignment=ft.Alignment.CENTER,
        on_click=(lambda _e: on_click()) if on_click else None,
        content=ft.Text(
            label,
            size=20,
            weight=ft.FontWeight.BOLD,
            color=COLOR_WHITE if enabled else "#ECEBFF",
        ),
    )


def _build_week_tile(
    *,
    week: MockWeek,
    is_selected: bool,
    on_select_week: Callable[[int], None],
) -> ft.Control:
    border = ft.Border.all(2, COLOR_WEEK_TILE_SELECTED_BORDER) if is_selected else None
    bgcolor = COLOR_WEEK_TILE_CLOSED_BG if week.is_closed else COLOR_WEEK_TILE_BG
    text_color = COLOR_TEXT_DIMMED if week.is_closed else COLOR_TEXT_PRIMARY

    return ft.Container(
        width=46,
        height=42,
        bgcolor=bgcolor,
        border=border,
        border_radius=2,
        alignment=ft.Alignment.CENTER,
        on_click=lambda _e, week_number=week.week_number: on_select_week(week_number),
        content=ft.Text(
            str(week.week_number),
            size=13,
            weight=ft.FontWeight.W_600,
            color=text_color,
        ),
    )


def _build_entry_tabs_bar(
    *,
    state: MainScreenLocalState,
    entries_for_selected_week: list[MockEntry],
    viewer_entry: MockEntry | None,
    on_select_entry: Callable[[EntryRef], None],
) -> ft.Control:
    if state.selected_week is None:
        content: ft.Control = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Selecciona una week para ver entries",
                    size=13,
                    color=COLOR_TEXT_MUTED,
                    italic=True,
                )
            ],
        )
    elif not entries_for_selected_week:
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    f"Week {state.selected_week} sin entries (mock)",
                    size=13,
                    color=COLOR_TEXT_MUTED,
                    italic=True,
                )
            ],
        )
    else:
        tab_selected_ref = (
            viewer_entry.ref if _viewer_matches_selected_week(state, viewer_entry) else None
        )
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=8,
            controls=[
                _build_entry_tab(
                    entry=entry,
                    is_selected=(tab_selected_ref == entry.ref),
                    on_select_entry=on_select_entry,
                )
                for entry in entries_for_selected_week
            ],
        )

    return ft.Container(
        height=ENTRY_TABS_BAR_HEIGHT,
        bgcolor=COLOR_ENTRY_TABS_BG,
        padding=ft.Padding(left=16, top=4, right=16, bottom=4),
        content=content,
    )


def _build_entry_tab(
    *,
    entry: MockEntry,
    is_selected: bool,
    on_select_entry: Callable[[EntryRef], None],
) -> ft.Control:
    underline_color = COLOR_ENTRY_TAB_SELECTED_UNDERLINE if is_selected else "transparent"
    text_weight = ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL
    underline_width = max(36, min(120, len(entry.label) * 7))

    return ft.Container(
        padding=ft.Padding(left=12, top=6, right=12, bottom=2),
        on_click=lambda _e, ref=entry.ref: on_select_entry(ref),
        content=ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    entry.label,
                    size=13,
                    color=COLOR_TEXT_PRIMARY,
                    weight=text_weight,
                ),
                ft.Container(
                    width=underline_width,
                    height=2,
                    bgcolor=underline_color,
                    border_radius=1,
                ),
            ],
        ),
    )


def _build_center_focus_panel(
    *,
    state: MainScreenLocalState,
    weeks_for_selected_year: list[MockWeek],
    viewer_entry: MockEntry | None,
    active_entry_mock: MockEntry | None,
) -> ft.Control:
    selected_week = _find_selected_week(state, weeks_for_selected_year)

    if viewer_entry is not None:
        content = _build_focus_entry_mode(
            state=state,
            viewer_entry=viewer_entry,
            active_entry_mock=active_entry_mock,
        )
    elif selected_week is not None:
        content = _build_focus_week_mode(selected_week)
    else:
        content = _build_focus_empty_mode(state)

    return ft.Container(
        expand=True,
        bgcolor=COLOR_CENTER_BG,
        padding=ft.Padding.all(CENTER_PANEL_PADDING),
        content=content,
    )


def _build_focus_empty_mode(state: MainScreenLocalState) -> ft.Control:
    return ft.Column(
        spacing=10,
        controls=[
            ft.Text(
                "Sin week seleccionada",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT_PRIMARY,
            ),
            ft.Text(
                "Navega por las weeks del año visible y selecciona una entry para mostrarla en el visor.",
                size=14,
                color=COLOR_TEXT_MUTED,
            ),
            _build_placeholder_card(
                title="Visor (sticky) vacío",
                body=(
                    "En #53 el visor se mantiene separado de la navegación. "
                    "Cuando selecciones una entry, seguirá visible aunque cambies de year/week."
                ),
                min_height=108,
            ),
            _build_placeholder_card(
                title=f"Navegación actual (mock): Año {state.selected_year}",
                body="No hay week seleccionada todavía.",
                min_height=74,
            ),
        ],
    )


def _build_focus_week_mode(week: MockWeek) -> ft.Control:
    badge_bg = "#EDEDED" if week.is_closed else "#D9F2D9"
    badge_fg = "#6A6A6A" if week.is_closed else "#237A3B"

    return ft.Column(
        spacing=12,
        controls=[
            ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        f"Week {week.week_number}",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXT_PRIMARY,
                    ),
                    _build_badge(week.status_label, badge_bg, badge_fg),
                ],
            ),
            _build_placeholder_card(
                title="Notas de la week (mock)",
                body=week.notes_preview,
                min_height=110,
            ),
            _build_placeholder_card(
                title="Sin entry en visor",
                body=(
                    "La week está seleccionada para navegación, pero el visor solo cambia al seleccionar una entry."
                ),
                min_height=90,
            ),
        ],
    )


def _build_focus_entry_mode(
    *,
    state: MainScreenLocalState,
    viewer_entry: MockEntry,
    active_entry_mock: MockEntry | None,
) -> ft.Control:
    viewer_matches_selected_week = _entry_ref_matches_selected_week(state, viewer_entry.ref)
    active_here = active_entry_mock is not None and active_entry_mock.ref == viewer_entry.ref

    context_lines = [
        f"Viendo: {viewer_entry.label} · Week {viewer_entry.ref.week_number} · Año {viewer_entry.ref.year_number}",
        (
            f"Navegación actual: Año {state.selected_year}"
            + (
                f" · Week {state.selected_week}"
                if state.selected_week is not None
                else " · sin week seleccionada"
            )
        ),
    ]
    if not viewer_matches_selected_week:
        context_lines.append(
            "Visor sticky: la entry visible no coincide con la week navegada actualmente."
        )

    session_mock_text = (
        "Con sesión activa (mock) en esta entry."
        if active_here
        else "Sin sesión activa (mock) en esta entry."
    )

    return ft.Column(
        spacing=12,
        controls=[
            ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        f"Week {viewer_entry.ref.week_number} · {viewer_entry.label}",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXT_PRIMARY,
                    ),
                    _build_badge(viewer_entry.entry_type, "#E7E0FF", "#4F46A5"),
                    _build_badge(
                        "activo aquí (mock)" if active_here else "visor (mock)",
                        "#DFF4FF" if active_here else "#F0F0F0",
                        "#0E5E78" if active_here else "#666666",
                    ),
                ],
            ),
            _build_placeholder_card(
                title="Contexto de visor / navegación",
                body="\n".join(context_lines),
                min_height=110,
            ),
            _build_placeholder_card(
                title="Detalle de entry (mock)",
                body=(
                    f"Tipo: {viewer_entry.entry_type}\n"
                    + (
                        f"Scenario ref: {viewer_entry.scenario_ref}\n"
                        if viewer_entry.scenario_ref
                        else ""
                    )
                    + "Datos reales y sincronización llegarán en #54+."
                ),
                min_height=96,
            ),
            _build_placeholder_card(
                title="Bloque de sesión (mock)",
                body=(
                    f"{session_mock_text}\n"
                    "Start/Stop reales y sesiones persistidas quedan fuera de #53."
                ),
                min_height=84,
            ),
            _build_placeholder_card(
                title="Recursos de la entry (mock)",
                body="Placeholder visual de recursos. Sin datos reales ni mutaciones.",
                min_height=72,
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
        border=ft.Border.all(1, "#D6D6D6"),
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


def _build_bottom_status_bar(
    *,
    env_name: str,
    viewer_entry: MockEntry | None,
    active_entry_mock: MockEntry | None,
) -> ft.Control:
    active_text = _active_mock_status_text(active_entry_mock, viewer_entry)
    viewer_text = (
        f"Viendo: {_entry_short_label(viewer_entry)}"
        if viewer_entry is not None
        else "Sin entry en visor"
    )

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
                            "Se conectarán con Q1 y reglas de recursos en #54+.",
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
                            active_text,
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_WHITE,
                            text_align=ft.TextAlign.RIGHT,
                        ),
                        ft.Text(
                            viewer_text,
                            size=12,
                            color="#EAF9FF",
                            text_align=ft.TextAlign.RIGHT,
                        ),
                        ft.Text(
                            f"env={env_name}",
                            size=11,
                            color="#DDF5FF",
                            text_align=ft.TextAlign.RIGHT,
                        ),
                    ],
                ),
            ],
        ),
    )


def _active_mock_status_text(
    active_entry_mock: MockEntry | None,
    viewer_entry: MockEntry | None,
) -> str:
    if active_entry_mock is None:
        return "Sin sesión activa (mock)"

    base = f"Con sesión activa (mock): {_entry_short_label(active_entry_mock)}"
    if viewer_entry is not None and viewer_entry.ref == active_entry_mock.ref:
        return f"{base} · aquí"
    return f"{base} · en otra entry"


def _entry_short_label(entry: MockEntry) -> str:
    return f"{entry.label} (W{entry.ref.week_number})"


def _find_selected_week(
    state: MainScreenLocalState,
    weeks_for_selected_year: list[MockWeek],
) -> MockWeek | None:
    if state.selected_week is None:
        return None
    for week in weeks_for_selected_year:
        if week.week_number == state.selected_week:
            return week
    return None


def _viewer_matches_selected_week(
    state: MainScreenLocalState,
    viewer_entry: MockEntry | None,
) -> bool:
    if viewer_entry is None:
        return False
    return _entry_ref_matches_selected_week(state, viewer_entry.ref)


def _entry_ref_matches_selected_week(
    state: MainScreenLocalState,
    entry_ref: EntryRef,
) -> bool:
    return (
        state.selected_week is not None
        and entry_ref.year_number == state.selected_year
        and entry_ref.week_number == state.selected_week
    )
