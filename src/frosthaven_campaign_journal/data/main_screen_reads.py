from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from frosthaven_campaign_journal.data.firestore_client import FirestoreReadError
from frosthaven_campaign_journal.state.placeholders import EntryRef


CAMPAIGN_ID = "01"
WEEKS_PER_YEAR = 20


@dataclass(frozen=True)
class CampaignMainRead:
    resource_totals: dict[str, int]
    updated_at_utc: Any | None


@dataclass(frozen=True)
class WeekRead:
    year_number: int
    week_number: int
    status: str
    notes: str | None


@dataclass(frozen=True)
class EntryRead:
    ref: EntryRef
    label: str
    entry_type: str
    scenario_ref: int | None
    order_index: int
    resource_deltas: dict[str, int]
    created_at_utc: Any | None
    updated_at_utc: Any | None


@dataclass(frozen=True)
class EntrySessionRead:
    session_id: str
    started_at_utc: Any | None
    ended_at_utc: Any | None
    created_at_utc: Any | None
    updated_at_utc: Any | None


@dataclass(frozen=True)
class ActiveSessionRead:
    session_ref: Any
    session_id: str
    started_at_utc: Any | None
    ended_at_utc: Any | None


@dataclass(frozen=True)
class ActiveEntryRead:
    entry_ref: EntryRef
    label: str
    entry_type: str
    scenario_ref: int | None


@dataclass(frozen=True)
class MainScreenSnapshot:
    campaign_main: CampaignMainRead
    years: list[int]
    effective_year: int
    weeks_for_selected_year: list[WeekRead]
    active_session: ActiveSessionRead | None
    active_entry: ActiveEntryRead | None
    active_status_error_message: str | None


def read_q1_campaign_main(client: firestore.Client) -> CampaignMainRead:
    try:
        snapshot = client.collection("campaigns").document(CAMPAIGN_ID).get()
    except Exception as exc:
        raise FirestoreReadError(f"Error leyendo Q1 (`campaigns/{CAMPAIGN_ID}`): {exc}") from exc

    if not snapshot.exists:
        raise FirestoreReadError(f"No existe el documento de campaña `campaigns/{CAMPAIGN_ID}`.")

    data = snapshot.to_dict() or {}

    resource_totals_raw = data.get("resource_totals") or {}
    if not isinstance(resource_totals_raw, dict):
        raise FirestoreReadError("Q1 inválido: `resource_totals` debe ser un mapa.")

    resource_totals: dict[str, int] = {}
    for key, value in resource_totals_raw.items():
        if not isinstance(key, str):
            raise FirestoreReadError("Q1 inválido: `resource_totals` contiene una clave no string.")
        if isinstance(value, bool) or not isinstance(value, int):
            raise FirestoreReadError(
                f"Q1 inválido: `resource_totals[{key}]` debe ser entero, recibido {type(value).__name__}."
            )
        resource_totals[key] = value

    return CampaignMainRead(
        resource_totals=resource_totals,
        updated_at_utc=data.get("updated_at_utc"),
    )


def read_q2_years_list(client: firestore.Client) -> list[int]:
    years: list[int] = []
    try:
        query = (
            client.collection("campaigns")
            .document(CAMPAIGN_ID)
            .collection("years")
            .order_by("year_number")
        )
        for snapshot in query.stream():
            data = snapshot.to_dict() or {}
            year_number = data.get("year_number")
            if year_number is None:
                try:
                    year_number = int(snapshot.id)
                except ValueError as exc:
                    raise FirestoreReadError(
                        f"Q2 inválido: year `{snapshot.id}` sin `year_number` parseable."
                    ) from exc
            if not isinstance(year_number, int) or year_number <= 0:
                raise FirestoreReadError(
                    f"Q2 inválido: `year_number` no válido en doc `{snapshot.id}`."
                )
            years.append(year_number)
    except FirestoreReadError:
        raise
    except Exception as exc:
        raise FirestoreReadError(f"Error leyendo Q2 (`years_list`): {exc}") from exc

    return years


def read_q3_q4_weeks_for_year(client: firestore.Client, year_number: int) -> list[WeekRead]:
    weeks = [
        *list(_read_weeks_for_season(client, year_number, "summer")),
        *list(_read_weeks_for_season(client, year_number, "winter")),
    ]
    return sorted(weeks, key=lambda week: week.week_number)


def _read_weeks_for_season(
    client: firestore.Client,
    year_number: int,
    season_type: str,
) -> list[WeekRead]:
    weeks: list[WeekRead] = []
    try:
        query = (
            client.collection("campaigns")
            .document(CAMPAIGN_ID)
            .collection("years")
            .document(str(year_number))
            .collection("seasons")
            .document(season_type)
            .collection("weeks")
            .order_by("week_number")
        )
        for snapshot in query.stream():
            data = snapshot.to_dict() or {}
            week_number = data.get("week_number")
            if not isinstance(week_number, int) or week_number <= 0:
                try:
                    week_number = int(snapshot.id)
                except Exception as exc:
                    raise FirestoreReadError(
                        f"Q3/Q4 inválido: `week_number` no válido en `{snapshot.reference.path}`."
                    ) from exc

            status = data.get("status")
            if status not in {"open", "closed"}:
                raise FirestoreReadError(
                    f"Q3/Q4 inválido: `status` no válido en `{snapshot.reference.path}`."
                )

            notes = data.get("notes")
            if notes is not None and not isinstance(notes, str):
                raise FirestoreReadError(
                    f"Q3/Q4 inválido: `notes` debe ser string/null en `{snapshot.reference.path}`."
                )

            weeks.append(
                WeekRead(
                    year_number=year_number,
                    week_number=week_number,
                    status=status,
                    notes=notes,
                )
            )
    except FirestoreReadError:
        raise
    except Exception as exc:
        raise FirestoreReadError(
            f"Error leyendo weeks de `{season_type}` para año {year_number}: {exc}"
        ) from exc

    return weeks


def read_q6_active_session_global(client: firestore.Client) -> ActiveSessionRead | None:
    try:
        query = (
            client.collection_group("sessions")
            .where(filter=FieldFilter("ended_at_utc", "==", None))
            .limit(1)
        )
        snapshots = list(query.stream())
    except Exception as exc:
        raise FirestoreReadError(f"Error leyendo Q6 (`active_session_global`): {exc}") from exc

    if not snapshots:
        return None

    snapshot = snapshots[0]
    data = snapshot.to_dict() or {}
    return ActiveSessionRead(
        session_ref=snapshot.reference,
        session_id=snapshot.id,
        started_at_utc=data.get("started_at_utc"),
        ended_at_utc=data.get("ended_at_utc"),
    )


def read_q5_entries_for_selected_week(
    client: firestore.Client,
    *,
    year_number: int,
    week_number: int,
) -> list[EntryRead]:
    season_type = _resolve_season_type_for_week(year_number=year_number, week_number=week_number)
    entries: list[EntryRead] = []
    try:
        query = (
            client.collection("campaigns")
            .document(CAMPAIGN_ID)
            .collection("years")
            .document(str(year_number))
            .collection("seasons")
            .document(season_type)
            .collection("weeks")
            .document(str(week_number))
            .collection("entries")
            .order_by("order_index")
        )
        for snapshot in query.stream():
            entries.append(_map_entry_snapshot(snapshot, year_number=year_number, week_number=week_number))
    except FirestoreReadError:
        raise
    except Exception as exc:
        raise FirestoreReadError(
            f"Error leyendo Q5 (`entries_selected_week`) para week {week_number} (año {year_number}): {exc}"
        ) from exc

    return sorted(
        entries,
        key=lambda entry: (
            entry.order_index,
            _sortable_dt_asc(entry.created_at_utc),
            entry.ref.entry_id,
        ),
    )


def read_entry_by_ref(client: firestore.Client, entry_ref: EntryRef) -> EntryRead:
    season_type = _resolve_season_type_for_week(
        year_number=entry_ref.year_number,
        week_number=entry_ref.week_number,
    )
    entry_doc_ref = (
        client.collection("campaigns")
        .document(CAMPAIGN_ID)
        .collection("years")
        .document(str(entry_ref.year_number))
        .collection("seasons")
        .document(season_type)
        .collection("weeks")
        .document(str(entry_ref.week_number))
        .collection("entries")
        .document(entry_ref.entry_id)
    )
    try:
        snapshot = entry_doc_ref.get()
    except Exception as exc:
        raise FirestoreReadError(
            f"Error leyendo entry del visor (`{entry_doc_ref.path}`): {exc}"
        ) from exc
    if not snapshot.exists:
        raise FirestoreReadError(f"La entry del visor ya no existe: `{entry_doc_ref.path}`.")
    return _map_entry_snapshot(
        snapshot,
        year_number=entry_ref.year_number,
        week_number=entry_ref.week_number,
    )


def read_q8_sessions_for_entry(
    client: firestore.Client,
    *,
    entry_ref: EntryRef,
) -> list[EntrySessionRead]:
    season_type = _resolve_season_type_for_week(
        year_number=entry_ref.year_number,
        week_number=entry_ref.week_number,
    )
    sessions: list[EntrySessionRead] = []
    try:
        query = (
            client.collection("campaigns")
            .document(CAMPAIGN_ID)
            .collection("years")
            .document(str(entry_ref.year_number))
            .collection("seasons")
            .document(season_type)
            .collection("weeks")
            .document(str(entry_ref.week_number))
            .collection("entries")
            .document(entry_ref.entry_id)
            .collection("sessions")
            .order_by("started_at_utc", direction=firestore.Query.DESCENDING)
        )
        for snapshot in query.stream():
            data = snapshot.to_dict() or {}
            sessions.append(
                EntrySessionRead(
                    session_id=snapshot.id,
                    started_at_utc=data.get("started_at_utc"),
                    ended_at_utc=data.get("ended_at_utc"),
                    created_at_utc=data.get("created_at_utc"),
                    updated_at_utc=data.get("updated_at_utc"),
                )
            )
    except Exception as exc:
        raise FirestoreReadError(
            f"Error leyendo Q8 (`sessions_selected_entry_combined`) para `{entry_ref.entry_id}`: {exc}"
        ) from exc

    return sorted(
        sessions,
        key=lambda session: (
            0 if session.ended_at_utc is None else 1,
            _sortable_dt_desc(session.started_at_utc),
            _sortable_dt_desc(session.updated_at_utc),
            session.session_id,
        ),
    )


def read_q7_active_entry_doc_if_needed(
    client: firestore.Client,
    active_session: ActiveSessionRead | None,
    viewer_entry_ref: EntryRef | None,
) -> ActiveEntryRead | None:
    if active_session is None:
        return None

    entry_doc_ref = active_session.session_ref.parent.parent
    if entry_doc_ref is None:
        raise FirestoreReadError("Q7 inválido: no se pudo resolver la Entry owner desde la sesión activa.")

    active_entry_ref = _entry_ref_from_entry_doc_ref(entry_doc_ref)

    # Q7 es condicional; en #54 lo usamos siempre para label del activo.
    # Mantenemos el parámetro para alineación con #16 y facilitar #54+.
    _ = viewer_entry_ref

    try:
        entry_snapshot = entry_doc_ref.get()
    except Exception as exc:
        raise FirestoreReadError(f"Error leyendo Q7 (`active_entry_doc_if_needed`): {exc}") from exc

    if not entry_snapshot.exists:
        raise FirestoreReadError("Q7 inválido: la Entry owner de la sesión activa no existe.")

    data = entry_snapshot.to_dict() or {}
    entry_type_raw = data.get("type")
    entry_type = str(entry_type_raw) if entry_type_raw is not None else ""

    scenario_ref_raw = data.get("scenario_ref")
    scenario_ref: int | None
    if scenario_ref_raw is None:
        scenario_ref = None
    elif isinstance(scenario_ref_raw, bool) or not isinstance(scenario_ref_raw, int):
        raise FirestoreReadError("Q7 inválido: `scenario_ref` debe ser entero o null.")
    else:
        scenario_ref = scenario_ref_raw

    label = _build_entry_label(entry_type=entry_type, scenario_ref=scenario_ref, entry_id=entry_doc_ref.id)
    return ActiveEntryRead(
        entry_ref=active_entry_ref,
        label=label,
        entry_type=entry_type,
        scenario_ref=scenario_ref,
    )


def load_main_screen_snapshot(
    client: firestore.Client,
    *,
    selected_year: int | None,
    viewer_entry_ref: EntryRef | None,
) -> MainScreenSnapshot:
    campaign_main = read_q1_campaign_main(client)
    years = read_q2_years_list(client)
    if not years:
        raise FirestoreReadError("Q2 inválido: no hay años provisionados en la campaña.")

    if selected_year is not None and selected_year in years:
        effective_year = selected_year
        weeks_for_selected_year = read_q3_q4_weeks_for_year(client, effective_year)
    else:
        effective_year = years[0]
        weeks_for_selected_year: list[WeekRead] | None = None
        first_year_weeks: list[WeekRead] | None = None

        for idx, year_number in enumerate(years):
            year_weeks = read_q3_q4_weeks_for_year(client, year_number)
            if idx == 0:
                first_year_weeks = year_weeks
            if any(week.status == "open" for week in year_weeks):
                effective_year = year_number
                weeks_for_selected_year = year_weeks
                break

        if weeks_for_selected_year is None:
            weeks_for_selected_year = first_year_weeks or []

    active_session: ActiveSessionRead | None = None
    active_entry: ActiveEntryRead | None = None
    active_status_error_message: str | None = None
    try:
        active_session = read_q6_active_session_global(client)
        active_entry = read_q7_active_entry_doc_if_needed(
            client,
            active_session=active_session,
            viewer_entry_ref=viewer_entry_ref,
        )
    except FirestoreReadError as exc:
        active_status_error_message = str(exc)

    return MainScreenSnapshot(
        campaign_main=campaign_main,
        years=years,
        effective_year=effective_year,
        weeks_for_selected_year=weeks_for_selected_year,
        active_session=active_session,
        active_entry=active_entry,
        active_status_error_message=active_status_error_message,
    )


def _resolve_season_type_for_week(*, year_number: int, week_number: int) -> str:
    local_week = week_number - ((year_number - 1) * WEEKS_PER_YEAR)
    if not 1 <= local_week <= WEEKS_PER_YEAR:
        raise FirestoreReadError(
            f"Week {week_number} no pertenece al año {year_number} según el template temporal MVP."
        )
    return "summer" if local_week <= 10 else "winter"


def _map_entry_snapshot(snapshot: Any, *, year_number: int, week_number: int) -> EntryRead:
    data = snapshot.to_dict() or {}
    entry_type = data.get("type")
    if not isinstance(entry_type, str) or not entry_type:
        raise FirestoreReadError(f"Q5/Q7 inválido: `type` no válido en `{snapshot.reference.path}`.")

    order_index = data.get("order_index")
    if isinstance(order_index, bool) or not isinstance(order_index, int) or order_index <= 0:
        raise FirestoreReadError(
            f"Q5/Q7 inválido: `order_index` no válido en `{snapshot.reference.path}`."
        )

    scenario_ref_raw = data.get("scenario_ref")
    scenario_ref: int | None
    if scenario_ref_raw is None:
        scenario_ref = None
    elif isinstance(scenario_ref_raw, bool) or not isinstance(scenario_ref_raw, int):
        raise FirestoreReadError(
            f"Q5/Q7 inválido: `scenario_ref` no válido en `{snapshot.reference.path}`."
        )
    else:
        scenario_ref = scenario_ref_raw

    resource_deltas_raw = data.get("resource_deltas") or {}
    if not isinstance(resource_deltas_raw, dict):
        raise FirestoreReadError(
            f"Q5/Q7 inválido: `resource_deltas` debe ser mapa en `{snapshot.reference.path}`."
        )
    resource_deltas: dict[str, int] = {}
    for key, value in resource_deltas_raw.items():
        if not isinstance(key, str):
            raise FirestoreReadError(
                f"Q5/Q7 inválido: clave de `resource_deltas` no string en `{snapshot.reference.path}`."
            )
        if isinstance(value, bool) or not isinstance(value, int):
            raise FirestoreReadError(
                f"Q5/Q7 inválido: `resource_deltas[{key}]` no entero en `{snapshot.reference.path}`."
            )
        resource_deltas[key] = value

    return EntryRead(
        ref=EntryRef(year_number=year_number, week_number=week_number, entry_id=snapshot.id),
        label=_build_entry_label(entry_type=entry_type, scenario_ref=scenario_ref, entry_id=snapshot.id),
        entry_type=entry_type,
        scenario_ref=scenario_ref,
        order_index=order_index,
        resource_deltas=resource_deltas,
        created_at_utc=data.get("created_at_utc"),
        updated_at_utc=data.get("updated_at_utc"),
    )


def _entry_ref_from_entry_doc_ref(entry_doc_ref: Any) -> EntryRef:
    try:
        week_doc_ref = entry_doc_ref.parent.parent
        season_doc_ref = week_doc_ref.parent.parent
        year_doc_ref = season_doc_ref.parent.parent
    except Exception as exc:
        raise FirestoreReadError("Q7 inválido: no se pudo reconstruir la jerarquía de la Entry activa.") from exc

    if week_doc_ref is None or year_doc_ref is None:
        raise FirestoreReadError("Q7 inválido: jerarquía incompleta al resolver la Entry activa.")

    try:
        year_number = int(year_doc_ref.id)
        week_number = int(week_doc_ref.id)
    except ValueError as exc:
        raise FirestoreReadError("Q7 inválido: IDs de year/week no parseables en la ruta de la Entry activa.") from exc

    return EntryRef(
        year_number=year_number,
        week_number=week_number,
        entry_id=entry_doc_ref.id,
    )


def _build_entry_label(*, entry_type: str, scenario_ref: int | None, entry_id: str) -> str:
    if entry_type == "scenario" and scenario_ref is not None:
        return f"Escenario {scenario_ref}"
    if entry_type == "outpost":
        return "Puesto fronterizo"
    return f"Entry {entry_id}"


def _sortable_dt_asc(value: Any | None) -> tuple[int, datetime]:
    if value is None:
        return (1, datetime.min.replace(tzinfo=timezone.utc))
    return (0, value)


def _sortable_dt_desc(value: Any | None) -> tuple[int, float]:
    if value is None:
        return (1, 0.0)
    try:
        ts = value.timestamp()
    except Exception:
        return (1, 0.0)
    return (0, -ts)
