from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
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
from frosthaven_campaign_journal.state.models import EntryRef


CAMPAIGN_ID = "01"
WEEKS_PER_YEAR = 20


@dataclass(frozen=True)
class SessionWriteResult:
    session_id: str | None = None


def start_session(
    client: firestore.Client,
    *,
    entry_ref: EntryRef,
) -> SessionWriteResult:
    target_entry_ref = _entry_doc_ref(client, entry_ref)
    target_sessions_ref = target_entry_ref.collection("sessions")
    transaction = client.transaction()
    created_session_id = target_sessions_ref.document().id

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> None:
        active = _read_active_session(txn, client)
        if active is not None:
            active_entry_ref = _entry_ref_from_session_ref(active.reference)
            if active_entry_ref == entry_ref:
                raise FirestoreTransitionInvalidError(
                    "La entry del visor ya tiene una sesión activa."
                )
            txn.update(
                active.reference,
                {
                    "ended_at_utc": firestore.SERVER_TIMESTAMP,
                    "updated_at_utc": firestore.SERVER_TIMESTAMP,
                },
            )

        txn.set(
            target_sessions_ref.document(created_session_id),
            {
                "started_at_utc": firestore.SERVER_TIMESTAMP,
                "ended_at_utc": None,
                "created_at_utc": firestore.SERVER_TIMESTAMP,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )

    try:
        _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover - protective mapping
        _map_firestore_write_exception(exc)
    return SessionWriteResult(session_id=created_session_id)


def stop_session(
    client: firestore.Client,
    *,
    entry_ref: EntryRef,
) -> SessionWriteResult:
    entry_doc_ref = _entry_doc_ref(client, entry_ref)
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> str:
        active = _read_active_session_for_entry(txn, entry_doc_ref)
        if active is None:
            raise FirestoreTransitionInvalidError(
                "No hay sesión activa en la entry visible para detener."
            )
        txn.update(
            active.reference,
            {
                "ended_at_utc": firestore.SERVER_TIMESTAMP,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )
        return active.id

    try:
        stopped_id = _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover - protective mapping
        _map_firestore_write_exception(exc)
    return SessionWriteResult(session_id=stopped_id)


def manual_create_session(
    client: firestore.Client,
    *,
    entry_ref: EntryRef,
    started_at_utc: datetime,
    ended_at_utc: datetime | None,
) -> SessionWriteResult:
    _validate_manual_session_times(started_at_utc, ended_at_utc)

    entry_doc_ref = _entry_doc_ref(client, entry_ref)
    sessions_ref = entry_doc_ref.collection("sessions")
    transaction = client.transaction()
    created_session_id = sessions_ref.document().id

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> None:
        if ended_at_utc is None:
            active = _read_active_session(txn, client)
            if active is not None:
                raise FirestoreValidationError(
                    "Ya existe una sesión activa global. Cierra la sesión activa antes de crear otra activa."
                )

        txn.set(
            sessions_ref.document(created_session_id),
            {
                "started_at_utc": started_at_utc,
                "ended_at_utc": ended_at_utc,
                "created_at_utc": firestore.SERVER_TIMESTAMP,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )

    try:
        _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover - protective mapping
        _map_firestore_write_exception(exc)
    return SessionWriteResult(session_id=created_session_id)


def manual_update_session(
    client: firestore.Client,
    *,
    entry_ref: EntryRef,
    session_id: str,
    started_at_utc: datetime,
    ended_at_utc: datetime | None,
) -> SessionWriteResult:
    _validate_manual_session_times(started_at_utc, ended_at_utc)

    session_doc_ref = _entry_doc_ref(client, entry_ref).collection("sessions").document(session_id)
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> None:
        snapshot = _get_doc_snapshot(txn, session_doc_ref)
        if not snapshot.exists:
            raise FirestoreTransitionInvalidError("La sesión ya no existe.")

        if ended_at_utc is None:
            active = _read_active_session(txn, client)
            if active is not None and active.reference.path != session_doc_ref.path:
                raise FirestoreValidationError(
                    "No se puede dejar esta sesión activa porque ya existe otra sesión activa global."
                )

        txn.update(
            session_doc_ref,
            {
                "started_at_utc": started_at_utc,
                "ended_at_utc": ended_at_utc,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )

    try:
        _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover - protective mapping
        _map_firestore_write_exception(exc)
    return SessionWriteResult(session_id=session_id)


def manual_delete_session(
    client: firestore.Client,
    *,
    entry_ref: EntryRef,
    session_id: str,
) -> SessionWriteResult:
    session_doc_ref = _entry_doc_ref(client, entry_ref).collection("sessions").document(session_id)
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> None:
        snapshot = _get_doc_snapshot(txn, session_doc_ref)
        if not snapshot.exists:
            raise FirestoreTransitionInvalidError("La sesión ya no existe.")
        txn.delete(session_doc_ref)

    try:
        _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover - protective mapping
        _map_firestore_write_exception(exc)
    return SessionWriteResult(session_id=session_id)


def _validate_manual_session_times(started_at_utc: datetime, ended_at_utc: datetime | None) -> None:
    if started_at_utc.tzinfo is None:
        raise FirestoreValidationError("`started_at_utc` debe incluir zona horaria (UTC).")
    if ended_at_utc is not None and ended_at_utc.tzinfo is None:
        raise FirestoreValidationError("`ended_at_utc` debe incluir zona horaria (UTC).")
    if ended_at_utc is not None and ended_at_utc < started_at_utc:
        raise FirestoreValidationError("`ended_at_utc` no puede ser anterior a `started_at_utc`.")


def _entry_doc_ref(client: firestore.Client, entry_ref: EntryRef) -> Any:
    season_type = _resolve_season_type_for_week(
        year_number=entry_ref.year_number,
        week_number=entry_ref.week_number,
    )
    return (
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


def _resolve_season_type_for_week(*, year_number: int, week_number: int) -> str:
    local_week = week_number - ((year_number - 1) * WEEKS_PER_YEAR)
    if not 1 <= local_week <= WEEKS_PER_YEAR:
        raise FirestoreValidationError(
            f"Week {week_number} no pertenece al año {year_number} según el template temporal MVP."
        )
    return "summer" if local_week <= 10 else "winter"


def _read_active_session(txn: firestore.Transaction, client: firestore.Client) -> Any | None:
    query = (
        client.collection_group("sessions")
        .where(filter=FieldFilter("ended_at_utc", "==", None))
        .limit(1)
    )
    snapshots = list(query.stream(transaction=txn))
    if not snapshots:
        return None
    return snapshots[0]


def _read_active_session_for_entry(txn: firestore.Transaction, entry_doc_ref: Any) -> Any | None:
    query = (
        entry_doc_ref.collection("sessions")
        .where(filter=FieldFilter("ended_at_utc", "==", None))
        .limit(1)
    )
    snapshots = list(query.stream(transaction=txn))
    if not snapshots:
        return None
    return snapshots[0]


def _entry_ref_from_session_ref(session_doc_ref: Any) -> EntryRef:
    try:
        entry_doc_ref = session_doc_ref.parent.parent
        week_doc_ref = entry_doc_ref.parent.parent
        year_doc_ref = week_doc_ref.parent.parent.parent.parent
    except Exception as exc:  # pragma: no cover - defensive
        raise FirestoreConflictError(
            "No se pudo resolver la entry owner de la sesión activa."
        ) from exc

    return EntryRef(
        year_number=int(year_doc_ref.id),
        week_number=int(week_doc_ref.id),
        entry_id=entry_doc_ref.id,
    )


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
