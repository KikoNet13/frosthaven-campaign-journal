from __future__ import annotations

from datetime import datetime, timedelta, timezone

import flet as ft

from frosthaven_campaign_journal.state.placeholders import MainScreenLocalState, MockEntry


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
COLOR_ERROR_BG = "#FFE7E7"
COLOR_ERROR_BORDER = "#D87A7A"
COLOR_ERROR_TEXT = "#8A1F1F"
COLOR_WARNING_BG = "#FFF4D8"
COLOR_WARNING_BORDER = "#D0A55E"
COLOR_WARNING_TEXT = "#7D5700"
COLOR_WEEK_BLOCK_SUMMER_BG = "#F2ABAB"
COLOR_WEEK_BLOCK_WINTER_BG = "#E6B3C4"
COLOR_WEEK_BLOCK_BORDER = "#D98787"


def build_badge(label: str, background: str, foreground: str) -> ft.Control:
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


def build_status_banner(
    *,
    title: str,
    body: str,
    background: str,
    border_color: str,
    foreground: str,
) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor=background,
        border=ft.Border.all(1, border_color),
        border_radius=8,
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=foreground),
                ft.Text(body, size=12, color=foreground),
            ],
        ),
    )


def build_placeholder_card(title: str, body: str, min_height: int) -> ft.Control:
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


def entry_short_label(entry: MockEntry) -> str:
    return f"Week {entry.ref.week_number} / {entry.label}"


def format_navigation_line(state: MainScreenLocalState) -> str:
    if state.selected_year is None:
        return "Navegación actual: sin año seleccionado"
    if state.selected_week is None:
        return f"Navegación actual: Año {state.selected_year} · sin week seleccionada"
    return f"Navegación actual: Año {state.selected_year} · Week {state.selected_week}"


def sum_finished_sessions_duration(sessions: list[object]) -> timedelta | None:
    total = timedelta()
    has_finished = False
    for session in sessions:
        started = as_datetime(getattr(session, "started_at_utc", None))
        ended = as_datetime(getattr(session, "ended_at_utc", None))
        if started is None or ended is None:
            continue
        if ended < started:
            continue
        total += ended - started
        has_finished = True
    return total if has_finished else None


def session_duration(session: object) -> timedelta | None:
    started = as_datetime(getattr(session, "started_at_utc", None))
    ended = as_datetime(getattr(session, "ended_at_utc", None))
    if started is None or ended is None:
        return None
    if ended < started:
        return None
    return ended - started


def as_datetime(value: object | None) -> datetime | None:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    return None


def format_dt_short(value: object | None) -> str:
    dt = as_datetime(value)
    if dt is None:
        return "n/d"
    return dt.astimezone().strftime("%Y-%m-%d %H:%M")


def format_duration(duration: timedelta | None) -> str:
    if duration is None:
        return "0 min"
    total_seconds = int(duration.total_seconds())
    if total_seconds < 0:
        total_seconds = 0
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{hours}h {minutes:02d}m" if hours else f"{minutes} min"


def truncate(value: str, max_length: int) -> str:
    if len(value) <= max_length:
        return value
    if max_length <= 1:
        return value[:max_length]
    return value[: max_length - 1].rstrip() + "…"

