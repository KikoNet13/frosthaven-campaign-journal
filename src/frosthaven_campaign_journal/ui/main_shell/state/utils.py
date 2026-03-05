from __future__ import annotations

from datetime import datetime, timezone

from frosthaven_campaign_journal.data import EntryRead, EntrySessionRead, WeekRead
from frosthaven_campaign_journal.models import EntryRef, EntrySummary, ViewerSessionItem, WeekSummary


def map_week_read_to_summary(week: WeekRead) -> WeekSummary:
    is_closed = week.status == "closed"
    return WeekSummary(
        year_number=week.year_number,
        week_number=week.week_number,
        is_closed=is_closed,
        status_label=week.status,
    )


def map_entry_read_to_summary(entry: EntryRead) -> EntrySummary:
    return EntrySummary(
        ref=entry.ref,
        label=entry.label,
        entry_type=entry.entry_type,
        scenario_ref=entry.scenario_ref,
        notes=entry.notes,
        scenario_outcome=entry.scenario_outcome,
        order_index=entry.order_index,
        resource_deltas=dict(entry.resource_deltas),
        created_at_utc=entry.created_at_utc,
        updated_at_utc=entry.updated_at_utc,
    )


def map_session_read_to_viewer_session(session: EntrySessionRead) -> ViewerSessionItem:
    return ViewerSessionItem(
        session_id=session.session_id,
        started_at_utc=session.started_at_utc,
        ended_at_utc=session.ended_at_utc,
        created_at_utc=session.created_at_utc,
        updated_at_utc=session.updated_at_utc,
    )


def find_entry_in_list(entries: list[EntrySummary], entry_ref: EntryRef) -> EntrySummary | None:
    for entry in entries:
        if entry.ref == entry_ref:
            return entry
    return None


def find_viewer_session_item(
    sessions: list[ViewerSessionItem],
    session_id: str,
) -> ViewerSessionItem | None:
    for session in sessions:
        if session.session_id == session_id:
            return session
    return None


def to_local_strings(value: object | None) -> tuple[str, str]:
    if isinstance(value, datetime):
        local = value.astimezone()
        return local.strftime("%Y-%m-%d"), local.strftime("%H:%M")
    return "", ""


def parse_local_datetime(date_value: str, time_value: str, *, field_label: str) -> datetime:
    date_value = date_value.strip()
    time_value = time_value.strip()
    if not date_value or not time_value:
        raise ValueError(f"{field_label}: fecha y hora son obligatorias (YYYY-MM-DD y HH:MM).")
    try:
        naive = datetime.strptime(f"{date_value} {time_value}", "%Y-%m-%d %H:%M")
    except ValueError as exc:
        raise ValueError(f"{field_label}: formato inválido, usa YYYY-MM-DD y HH:MM.") from exc
    local_tz = datetime.now().astimezone().tzinfo or timezone.utc
    aware_local = naive.replace(tzinfo=local_tz)
    return aware_local.astimezone(timezone.utc)


def parse_optional_local_datetime(
    date_value: str,
    time_value: str,
    *,
    field_label: str,
) -> datetime | None:
    date_value = date_value.strip()
    time_value = time_value.strip()
    if not date_value and not time_value:
        return None
    return parse_local_datetime(date_value, time_value, field_label=field_label)


def parse_entry_form_values(*, entry_type_value: str, scenario_ref_value: str) -> tuple[str, int | None]:
    entry_type = (entry_type_value or "").strip().lower()
    if entry_type not in {"scenario", "outpost"}:
        raise ValueError("Tipo de entrada inválido. Usa 'scenario' o 'outpost'.")
    raw_scenario = (scenario_ref_value or "").strip()
    if entry_type == "scenario":
        if not raw_scenario:
            raise ValueError("La referencia de escenario es obligatoria para entradas de tipo scenario.")
        try:
            scenario_ref = int(raw_scenario)
        except ValueError as exc:
            raise ValueError("La referencia de escenario debe ser un entero positivo.") from exc
        if scenario_ref <= 0:
            raise ValueError("La referencia de escenario debe ser un entero positivo.")
        return entry_type, scenario_ref

    if raw_scenario:
        raise ValueError("La referencia de escenario debe quedar vacía para entradas de tipo outpost.")
    return entry_type, None
