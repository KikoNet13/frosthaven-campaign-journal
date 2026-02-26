from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from google.api_core.exceptions import Aborted
from google.cloud import firestore

from frosthaven_campaign_journal.data.write_errors import (
    FirestoreConflictError,
    FirestoreTransitionInvalidError,
    FirestoreValidationError,
    FirestoreWriteError,
)


CAMPAIGN_ID = "01"
WEEKS_PER_YEAR = 20
WEEKS_PER_SEASON = 10
SEASON_TYPES = ("summer", "winter")


@dataclass(frozen=True)
class CampaignWriteResult:
    new_year_number: int
    created_week_start: int
    created_week_end: int
    week_cursor: int


def extend_years_plus_one(client: firestore.Client) -> CampaignWriteResult:
    campaign_doc_ref = _campaign_doc_ref(client)
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> CampaignWriteResult:
        campaign_snapshot = _get_doc_snapshot(txn, campaign_doc_ref)
        if not campaign_snapshot.exists:
            raise FirestoreTransitionInvalidError("La campaña ya no existe.")

        campaign_data = campaign_snapshot.to_dict() or {}
        week_cursor_raw = campaign_data.get("week_cursor")
        if isinstance(week_cursor_raw, bool) or not isinstance(week_cursor_raw, int) or week_cursor_raw <= 0:
            raise FirestoreValidationError("`campaign.week_cursor` debe ser un entero positivo.")

        years_state = _read_years_state(txn, client)
        if not years_state:
            raise FirestoreTransitionInvalidError(
                "La campaña no tiene años provisionados; no se puede extender +1 año."
            )
        last_year_number = max(years_state)
        new_year_number = last_year_number + 1

        weeks_state, max_existing_week_number = _read_all_weeks_state(txn, client)
        if max_existing_week_number is None:
            raise FirestoreTransitionInvalidError(
                "La campaña no tiene weeks provisionadas; no se puede extender +1 año."
            )

        created_week_start = max_existing_week_number + 1
        created_week_end = max_existing_week_number + WEEKS_PER_YEAR

        year_doc_ref = campaign_doc_ref.collection("years").document(str(new_year_number))
        year_snapshot = _get_doc_snapshot(txn, year_doc_ref)
        if year_snapshot.exists:
            raise FirestoreValidationError(
                f"Ya existe el año {new_year_number}; no se puede extender +1 año."
            )

        _validate_new_week_range_absent(
            weeks_state=weeks_state,
            created_week_start=created_week_start,
            created_week_end=created_week_end,
        )

        server_ts = firestore.SERVER_TIMESTAMP
        txn.set(
            year_doc_ref,
            {
                "year_number": new_year_number,
                "created_at_utc": server_ts,
                "updated_at_utc": server_ts,
            },
        )

        next_week_number = created_week_start
        for season_type in SEASON_TYPES:
            season_doc_ref = year_doc_ref.collection("seasons").document(season_type)
            txn.set(
                season_doc_ref,
                {
                    "season_type": season_type,
                    "created_at_utc": server_ts,
                    "updated_at_utc": server_ts,
                },
            )

            for _ in range(WEEKS_PER_SEASON):
                txn.set(
                    season_doc_ref.collection("weeks").document(str(next_week_number)),
                    {
                        "week_number": next_week_number,
                        "status": "open",
                        "notes": None,
                        "created_at_utc": server_ts,
                        "updated_at_utc": server_ts,
                    },
                )
                weeks_state[next_week_number] = "open"
                next_week_number += 1

        next_week_cursor = _first_open_week_number(weeks_state)
        if next_week_cursor is None:
            raise FirestoreValidationError(
                "La extensión dejaría 0 weeks abiertas, lo cual no está permitido."
            )

        txn.update(
            campaign_doc_ref,
            {
                "week_cursor": next_week_cursor,
                "updated_at_utc": server_ts,
            },
        )

        return CampaignWriteResult(
            new_year_number=new_year_number,
            created_week_start=created_week_start,
            created_week_end=created_week_end,
            week_cursor=next_week_cursor,
        )

    try:
        return _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover - defensive mapping
        _map_firestore_write_exception(exc)


def _read_years_state(txn: firestore.Transaction, client: firestore.Client) -> set[int]:
    years_query = _campaign_doc_ref(client).collection("years").order_by("year_number")
    year_snaps = list(years_query.stream(transaction=txn))
    year_numbers: set[int] = set()
    for year_snap in year_snaps:
        data = year_snap.to_dict() or {}
        year_number = data.get("year_number")
        if year_number is None:
            try:
                year_number = int(year_snap.id)
            except ValueError as exc:
                raise FirestoreValidationError(
                    f"Year inválido: `{year_snap.reference.path}` sin `year_number` parseable."
                ) from exc
        if isinstance(year_number, bool) or not isinstance(year_number, int) or year_number <= 0:
            raise FirestoreValidationError(
                f"Year inválido en `{year_snap.reference.path}`: `year_number` no válido."
            )
        if year_number in year_numbers:
            raise FirestoreValidationError(f"Hay años duplicados con `year_number={year_number}`.")
        year_numbers.add(year_number)
    return year_numbers


def _read_all_weeks_state(
    txn: firestore.Transaction,
    client: firestore.Client,
) -> tuple[dict[int, str], int | None]:
    years_query = _campaign_doc_ref(client).collection("years").order_by("year_number")
    year_snaps = list(years_query.stream(transaction=txn))
    weeks_state: dict[int, str] = {}
    max_week_number: int | None = None

    for year_snap in year_snaps:
        data = year_snap.to_dict() or {}
        year_number = data.get("year_number")
        if year_number is None:
            try:
                year_number = int(year_snap.id)
            except ValueError as exc:
                raise FirestoreValidationError(f"ID de año inválido: {year_snap.id!r}.") from exc
        if isinstance(year_number, bool) or not isinstance(year_number, int) or year_number <= 0:
            raise FirestoreValidationError(
                f"Year inválido en `{year_snap.reference.path}`: `year_number` no válido."
            )

        year_doc_ref = year_snap.reference
        for season_type in SEASON_TYPES:
            weeks_query = (
                year_doc_ref.collection("seasons")
                .document(season_type)
                .collection("weeks")
                .order_by("week_number")
            )
            for week_snap in weeks_query.stream(transaction=txn):
                week_data = week_snap.to_dict() or {}
                week_number = week_data.get("week_number")
                status = week_data.get("status")
                if isinstance(week_number, bool) or not isinstance(week_number, int) or week_number <= 0:
                    raise FirestoreValidationError(
                        f"Week inválida en {week_snap.reference.path}: `week_number` no es entero positivo."
                    )
                if status not in {"open", "closed"}:
                    raise FirestoreValidationError(
                        f"Week inválida en {week_snap.reference.path}: estado no soportado {status!r}."
                    )
                expected_year = ((week_number - 1) // WEEKS_PER_YEAR) + 1
                if expected_year != year_number:
                    raise FirestoreValidationError(
                        f"Inconsistencia temporal: week {week_number} no pertenece al año {year_number}."
                    )
                if week_number in weeks_state:
                    raise FirestoreValidationError(
                        f"Duplicado temporal: week {week_number} repetida en la estructura."
                    )
                weeks_state[week_number] = status
                if max_week_number is None or week_number > max_week_number:
                    max_week_number = week_number

    return weeks_state, max_week_number


def _validate_new_week_range_absent(
    *,
    weeks_state: dict[int, str],
    created_week_start: int,
    created_week_end: int,
) -> None:
    for week_number in range(created_week_start, created_week_end + 1):
        if week_number in weeks_state:
            raise FirestoreValidationError(
                f"La extensión +1 año duplicaría la week {week_number}."
            )


def _first_open_week_number(weeks_state: dict[int, str]) -> int | None:
    open_weeks = [week_number for week_number, status in weeks_state.items() if status == "open"]
    if not open_weeks:
        return None
    return min(open_weeks)


def _campaign_doc_ref(client: firestore.Client) -> Any:
    return client.collection("campaigns").document(CAMPAIGN_ID)


def _get_doc_snapshot(txn: firestore.Transaction, doc_ref: Any) -> Any:
    snapshot_or_iter = txn.get(doc_ref)
    if hasattr(snapshot_or_iter, "exists"):
        return snapshot_or_iter
    snapshots = list(snapshot_or_iter)
    if not snapshots:
        raise FirestoreTransitionInvalidError("El documento ya no existe.")
    return snapshots[0]


def _map_firestore_write_exception(exc: Exception) -> None:
    if isinstance(exc, FirestoreWriteError):
        raise exc
    if isinstance(exc, Aborted):
        raise FirestoreConflictError(
            "La operación de escritura entró en conflicto. Pulsa Refresh y reintenta."
        ) from exc
    raise FirestoreWriteError(f"Error de escritura en Firestore: {exc}") from exc
