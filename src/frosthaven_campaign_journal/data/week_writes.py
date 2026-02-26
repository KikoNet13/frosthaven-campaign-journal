from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from google.api_core.exceptions import Aborted
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from frosthaven_campaign_journal.data.write_errors import (
    FirestoreConflictError,
    FirestoreTransitionInvalidError,
    FirestoreValidationError,
    FirestoreWriteError,
)


CAMPAIGN_ID = "01"
WEEKS_PER_YEAR = 20
SEASON_TYPES = ("summer", "winter")


@dataclass(frozen=True)
class WeekWriteResult:
    week_number: int
    new_status: str | None = None
    week_cursor: int | None = None
    auto_stopped_session_id: str | None = None


def update_week_notes(
    client: firestore.Client,
    *,
    year_number: int,
    week_number: int,
    notes: str,
) -> WeekWriteResult:
    if not isinstance(notes, str):
        raise FirestoreValidationError("Las notas de week deben ser texto.")

    week_doc_ref = _week_doc_ref(client, year_number=year_number, week_number=week_number)
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> None:
        snapshot = _get_doc_snapshot(txn, week_doc_ref)
        if not snapshot.exists:
            raise FirestoreTransitionInvalidError("La week ya no existe.")
        txn.update(
            week_doc_ref,
            {
                "notes": notes,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )

    try:
        _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover - defensive mapping
        _map_firestore_write_exception(exc)

    return WeekWriteResult(week_number=week_number)


def close_week(
    client: firestore.Client,
    *,
    year_number: int,
    week_number: int,
) -> WeekWriteResult:
    return _close_like_week_operation(
        client,
        year_number=year_number,
        week_number=week_number,
        operation_label="cerrar",
    )


def reclose_week(
    client: firestore.Client,
    *,
    year_number: int,
    week_number: int,
) -> WeekWriteResult:
    return _close_like_week_operation(
        client,
        year_number=year_number,
        week_number=week_number,
        operation_label="re-cerrar",
    )


def reopen_week(
    client: firestore.Client,
    *,
    year_number: int,
    week_number: int,
) -> WeekWriteResult:
    week_doc_ref = _week_doc_ref(client, year_number=year_number, week_number=week_number)
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> WeekWriteResult:
        target_snapshot = _get_doc_snapshot(txn, week_doc_ref)
        if not target_snapshot.exists:
            raise FirestoreTransitionInvalidError("La week ya no existe.")

        target_data = target_snapshot.to_dict() or {}
        current_status = target_data.get("status")
        if current_status not in {"open", "closed"}:
            raise FirestoreValidationError(
                f"Estado de week no soportado: {current_status!r}."
            )
        if current_status != "closed":
            raise FirestoreTransitionInvalidError(
                "La week no está cerrada; no se puede reabrir."
            )

        weeks_state = _read_all_weeks_state(txn, client)
        if week_number not in weeks_state:
            raise FirestoreTransitionInvalidError("La week ya no existe en la estructura temporal.")
        weeks_state[week_number] = "open"

        next_cursor = _first_open_week_number(weeks_state)
        if next_cursor is None:
            raise FirestoreValidationError(
                "La operación dejaría 0 weeks abiertas, lo cual no está permitido."
            )

        txn.update(
            week_doc_ref,
            {
                "status": "open",
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )
        return WeekWriteResult(
            week_number=week_number,
            new_status="open",
            week_cursor=next_cursor,
        )

    try:
        return _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover - defensive mapping
        _map_firestore_write_exception(exc)


def _close_like_week_operation(
    client: firestore.Client,
    *,
    year_number: int,
    week_number: int,
    operation_label: str,
) -> WeekWriteResult:
    week_doc_ref = _week_doc_ref(client, year_number=year_number, week_number=week_number)
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> WeekWriteResult:
        target_snapshot = _get_doc_snapshot(txn, week_doc_ref)
        if not target_snapshot.exists:
            raise FirestoreTransitionInvalidError("La week ya no existe.")

        target_data = target_snapshot.to_dict() or {}
        current_status = target_data.get("status")
        if current_status not in {"open", "closed"}:
            raise FirestoreValidationError(
                f"Estado de week no soportado: {current_status!r}."
            )
        if current_status != "open":
            raise FirestoreTransitionInvalidError(
                f"La week no está abierta; no se puede {operation_label}."
            )

        weeks_state = _read_all_weeks_state(txn, client)
        if week_number not in weeks_state:
            raise FirestoreTransitionInvalidError("La week ya no existe en la estructura temporal.")
        weeks_state[week_number] = "closed"

        next_cursor = _first_open_week_number(weeks_state)
        if next_cursor is None:
            raise FirestoreValidationError(
                "La operación dejaría 0 weeks abiertas, lo cual no está permitido."
            )

        auto_stopped_session_id: str | None = None
        active_session_snapshot = _read_active_session(txn, client)
        if active_session_snapshot is not None:
            active_year, active_week = _week_owner_from_session_ref(active_session_snapshot.reference)
            if active_year == year_number and active_week == week_number:
                txn.update(
                    active_session_snapshot.reference,
                    {
                        "ended_at_utc": firestore.SERVER_TIMESTAMP,
                        "updated_at_utc": firestore.SERVER_TIMESTAMP,
                    },
                )
                auto_stopped_session_id = active_session_snapshot.id

        txn.update(
            week_doc_ref,
            {
                "status": "closed",
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )
        return WeekWriteResult(
            week_number=week_number,
            new_status="closed",
            week_cursor=next_cursor,
            auto_stopped_session_id=auto_stopped_session_id,
        )

    try:
        return _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover - defensive mapping
        _map_firestore_write_exception(exc)


def _campaign_doc_ref(client: firestore.Client) -> Any:
    return client.collection("campaigns").document(CAMPAIGN_ID)


def _week_doc_ref(client: firestore.Client, *, year_number: int, week_number: int) -> Any:
    season_type = _resolve_season_type_for_week(year_number=year_number, week_number=week_number)
    return (
        _campaign_doc_ref(client)
        .collection("years")
        .document(str(year_number))
        .collection("seasons")
        .document(season_type)
        .collection("weeks")
        .document(str(week_number))
    )


def _resolve_season_type_for_week(*, year_number: int, week_number: int) -> str:
    local_week = week_number - ((year_number - 1) * WEEKS_PER_YEAR)
    if not 1 <= local_week <= WEEKS_PER_YEAR:
        raise FirestoreValidationError(
            f"Week {week_number} no pertenece al año {year_number} según el template temporal MVP."
        )
    return "summer" if local_week <= 10 else "winter"


def _read_all_weeks_state(txn: firestore.Transaction, client: firestore.Client) -> dict[int, str]:
    years_query = _campaign_doc_ref(client).collection("years").order_by("year_number")
    year_snaps = list(years_query.stream(transaction=txn))
    weeks_state: dict[int, str] = {}
    for year_snap in year_snaps:
        try:
            year_number = int(year_snap.id)
        except ValueError as exc:
            raise FirestoreValidationError(f"ID de año inválido: {year_snap.id!r}.") from exc

        year_doc_ref = year_snap.reference
        for season_type in SEASON_TYPES:
            weeks_query = (
                year_doc_ref.collection("seasons")
                .document(season_type)
                .collection("weeks")
                .order_by("week_number")
            )
            for week_snap in weeks_query.stream(transaction=txn):
                data = week_snap.to_dict() or {}
                week_number_raw = data.get("week_number")
                status = data.get("status")
                if not isinstance(week_number_raw, int):
                    raise FirestoreValidationError(
                        f"Week inválida en {week_snap.reference.path}: `week_number` no es entero."
                    )
                if status not in {"open", "closed"}:
                    raise FirestoreValidationError(
                        f"Week inválida en {week_snap.reference.path}: estado no soportado {status!r}."
                    )
                expected_year = ((week_number_raw - 1) // WEEKS_PER_YEAR) + 1
                if expected_year != year_number:
                    raise FirestoreValidationError(
                        f"Inconsistencia temporal: week {week_number_raw} no pertenece al año {year_number}."
                    )
                weeks_state[week_number_raw] = status
    return weeks_state


def _first_open_week_number(weeks_state: dict[int, str]) -> int | None:
    open_weeks = [week_number for week_number, status in weeks_state.items() if status == "open"]
    if not open_weeks:
        return None
    return min(open_weeks)


def _read_active_session(txn: firestore.Transaction, client: firestore.Client) -> Any | None:
    query = (
        client.collection_group("sessions")
        .where(filter=FieldFilter("ended_at_utc", "==", None))
        .limit(1)
    )
    snaps = list(query.stream(transaction=txn))
    return snaps[0] if snaps else None


def _week_owner_from_session_ref(session_doc_ref: Any) -> tuple[int, int]:
    try:
        entry_doc_ref = session_doc_ref.parent.parent
        week_doc_ref = entry_doc_ref.parent.parent
        year_doc_ref = week_doc_ref.parent.parent.parent.parent
    except Exception as exc:  # pragma: no cover - defensive
        raise FirestoreConflictError(
            "No se pudo resolver la week owner de la sesión activa."
        ) from exc

    try:
        return int(year_doc_ref.id), int(week_doc_ref.id)
    except ValueError as exc:  # pragma: no cover - defensive
        raise FirestoreConflictError("No se pudo resolver year/week numéricos desde la sesión activa.") from exc


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

