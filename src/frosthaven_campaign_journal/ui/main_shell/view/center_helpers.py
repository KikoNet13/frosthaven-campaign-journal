from __future__ import annotations

from datetime import datetime, timedelta, timezone

import flet as ft

from frosthaven_campaign_journal.models import WeekSummary
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.view.theme import (
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
)


def _build_card(title: str, body: str) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.all(12),
        bgcolor="#F6F6F6",
        border_radius=8,
        border=ft.Border.all(1, "#D6D6D6"),
        content=ft.Column(
            spacing=6,
            controls=[
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                ft.Container(
                    padding=ft.Padding.all(8),
                    bgcolor="#FFFFFF",
                    border_radius=6,
                    content=ft.Text(body, size=13, color=COLOR_TEXT_MUTED),
                ),
            ],
        ),
    )


def _find_selected_week(data: MainShellViewData) -> WeekSummary | None:
    if data.state.selected_week is None:
        return None
    for week in data.weeks_for_selected_year:
        if week.week_number == data.state.selected_week:
            return week
    return None


def _format_navigation_line(data: MainShellViewData) -> str:
    if data.state.selected_year is None:
        return "Navegación actual: sin año seleccionado"
    if data.state.selected_week is None:
        return f"Navegación actual: Año {data.state.selected_year} · sin semana seleccionada"
    return f"Navegación actual: Año {data.state.selected_year} · Semana {data.state.selected_week}"


def _format_week_status_label(status_label: str) -> str:
    if status_label == "open":
        return "abierta"
    if status_label == "closed":
        return "cerrada"
    return status_label


def _sum_finished_sessions_duration(sessions: list[object]) -> timedelta | None:
    total = timedelta()
    has_finished = False
    for session in sessions:
        started = _as_datetime(getattr(session, "started_at_utc", None))
        ended = _as_datetime(getattr(session, "ended_at_utc", None))
        if started is None or ended is None or ended < started:
            continue
        total += ended - started
        has_finished = True
    return total if has_finished else None


def _as_datetime(value: object | None) -> datetime | None:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    return None


def _format_duration(duration: timedelta | None) -> str:
    if duration is None:
        return "0 min"
    total_seconds = int(duration.total_seconds())
    if total_seconds < 0:
        total_seconds = 0
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{hours}h {minutes:02d}m" if hours else f"{minutes} min"


def _format_session_line(session: object) -> str:
    session_id = getattr(session, "session_id", "n/d")
    started = _format_dt_short(getattr(session, "started_at_utc", None))
    ended_raw = getattr(session, "ended_at_utc", None)
    if ended_raw is None:
        return f"{session_id}: {started} -> activa"
    ended = _format_dt_short(ended_raw)
    duration = _session_duration(session)
    duration_text = _format_duration(duration) if duration is not None else "duración n/d"
    return f"{session_id}: {started} -> {ended} · {duration_text}"


def _session_duration(session: object) -> timedelta | None:
    started = _as_datetime(getattr(session, "started_at_utc", None))
    ended = _as_datetime(getattr(session, "ended_at_utc", None))
    if started is None or ended is None or ended < started:
        return None
    return ended - started


def _format_dt_short(value: object | None) -> str:
    dt = _as_datetime(value)
    if dt is None:
        return "n/d"
    return dt.astimezone().strftime("%Y-%m-%d %H:%M")
