from __future__ import annotations

import asyncio
from datetime import datetime, timezone

import flet as ft


def coerce_datetime(value: object | None) -> datetime | None:
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def format_session_duration_hms(
    *,
    started_at_utc: object | None,
    ended_at_utc: object | None = None,
    now: datetime | None = None,
) -> str:
    started = coerce_datetime(started_at_utc)
    if started is None:
        return "00:00:00"

    resolved_now = now or datetime.now(timezone.utc)
    if resolved_now.tzinfo is None:
        resolved_now = resolved_now.replace(tzinfo=timezone.utc)
    ended = coerce_datetime(ended_at_utc) or resolved_now
    if ended < started:
        ended = started

    total_seconds = int((ended - started).total_seconds())
    hours, remainder = divmod(max(0, total_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def format_session_summary_date(started_at_utc: object | None) -> str:
    started = coerce_datetime(started_at_utc)
    if started is None:
        return "n/d"
    return started.astimezone().strftime("%d/%m/%y")


def format_session_summary_range(
    *,
    started_at_utc: object | None,
    ended_at_utc: object | None = None,
) -> str:
    started = coerce_datetime(started_at_utc)
    if started is None:
        return "n/d"

    started_text = started.astimezone().strftime("%H:%M")
    ended = coerce_datetime(ended_at_utc)
    if ended is None:
        return f"{started_text} - activa"
    return f"{started_text} - {ended.astimezone().strftime('%H:%M')}"


def build_active_session_subtitle(*, entry_label: str | None, week_number: int | None) -> str:
    base_label = entry_label or "Entrada activa"
    if week_number is None:
        return base_label
    return f"{base_label} · Semana {week_number}"


def build_session_duration_text(
    *,
    started_at_utc: object | None,
    ended_at_utc: object | None = None,
    size: int,
    weight: ft.FontWeight = ft.FontWeight.W_700,
    color: str,
    text_align: ft.TextAlign = ft.TextAlign.LEFT,
) -> ft.Control:
    try:
        return SessionDurationText(
            started_at_utc=started_at_utc,
            ended_at_utc=ended_at_utc,
            size=size,
            weight=weight,
            color=color,
            text_align=text_align,
        )
    except RuntimeError:
        return ft.Text(
            value=format_session_duration_hms(
                started_at_utc=started_at_utc,
                ended_at_utc=ended_at_utc,
            ),
            size=size,
            weight=weight,
            color=color,
            text_align=text_align,
            no_wrap=True,
        )


@ft.component
def SessionDurationText(
    *,
    started_at_utc: object | None,
    ended_at_utc: object | None = None,
    size: int,
    weight: ft.FontWeight = ft.FontWeight.W_700,
    color: str,
    text_align: ft.TextAlign = ft.TextAlign.LEFT,
) -> ft.Control:
    tick, set_tick = ft.use_state(0)

    def _setup():
        if coerce_datetime(started_at_utc) is None or coerce_datetime(ended_at_utc) is not None:
            return None

        async def _tick() -> None:
            while True:
                await asyncio.sleep(1)
                set_tick(lambda current: current + 1)

        task = ft.context.page.run_task(_tick)

        def _cleanup() -> None:
            task.cancel()

        return _cleanup

    ft.use_effect(_setup, dependencies=[started_at_utc, ended_at_utc])
    _ = tick

    return ft.Text(
        value=format_session_duration_hms(
            started_at_utc=started_at_utc,
            ended_at_utc=ended_at_utc,
        ),
        size=size,
        weight=weight,
        color=color,
        text_align=text_align,
        no_wrap=True,
    )
