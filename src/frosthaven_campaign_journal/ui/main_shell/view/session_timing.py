from __future__ import annotations

import asyncio
from concurrent.futures import Future
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
    return SessionDurationText(
        started_at_utc=started_at_utc,
        ended_at_utc=ended_at_utc,
        size=size,
        weight=weight,
        color=color,
        text_align=text_align,
    )


@ft.control(isolated=True)
class SessionDurationText(ft.Text):
    started_at_utc: object | None = None
    ended_at_utc: object | None = None

    def init(self) -> None:
        super().init()
        self.no_wrap = True
        self._ticker_future: Future[None] | None = None
        self._ticker_running = False
        self._display_value = format_session_duration_hms(
            started_at_utc=self.started_at_utc,
            ended_at_utc=self.ended_at_utc,
        )
        self._apply_display_value()

    def did_mount(self) -> None:
        super().did_mount()
        self._sync_ticker()

    def before_update(self) -> None:
        self.no_wrap = True
        self._display_value = format_session_duration_hms(
            started_at_utc=self.started_at_utc,
            ended_at_utc=self.ended_at_utc,
        )
        self._apply_display_value()
        self._sync_ticker()

    def will_unmount(self) -> None:
        self._stop_ticker()
        super().will_unmount()

    def _migrate_state(self, other: ft.BaseControl) -> None:
        super()._migrate_state(other)
        if isinstance(other, SessionDurationText):
            other._stop_ticker()
        self._ticker_future = None
        self._ticker_running = False

    def _apply_display_value(self) -> None:
        self.value = self._display_value

    def _is_live_session(self) -> bool:
        return (
            coerce_datetime(self.started_at_utc) is not None
            and coerce_datetime(self.ended_at_utc) is None
        )

    def _sync_ticker(self) -> None:
        if not self._is_attached_to_page() or not self._is_live_session():
            self._stop_ticker()
            return
        if self._ticker_future is not None and not self._ticker_future.done():
            return
        self._ticker_running = True
        self._ticker_future = self.page.run_task(self._run_ticker)

    def _stop_ticker(self) -> None:
        self._ticker_running = False
        if self._ticker_future is not None and not self._ticker_future.done():
            self._ticker_future.cancel()
        self._ticker_future = None

    async def _run_ticker(self) -> None:
        try:
            while self._ticker_running and self._is_live_session():
                await asyncio.sleep(1)
                next_value = format_session_duration_hms(
                    started_at_utc=self.started_at_utc,
                    ended_at_utc=self.ended_at_utc,
                )
                if self._display_value != next_value:
                    self._display_value = next_value
                    self._apply_display_value()
                    self.update()
        except asyncio.CancelledError:
            pass
        except RuntimeError:
            self._stop_ticker()

    def _is_attached_to_page(self) -> bool:
        try:
            self.page
        except RuntimeError:
            return False
        return True
