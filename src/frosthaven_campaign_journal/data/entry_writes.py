from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from google.api_core.exceptions import Aborted
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from frosthaven_campaign_journal.data.write_errors import (
    FirestoreConflictError,
    FirestoreTransitionInvalidError,
    FirestoreValidationError,
    FirestoreWriteError,
)
from frosthaven_campaign_journal.models import EntryRef


CAMPAIGN_ID = "01"
WEEKS_PER_YEAR = 20


@dataclass(frozen=True)
class EntryWriteResult:
    entry_ref: EntryRef | None = None
    auto_stopped_session_id: str | None = None


def create_entry(
    client: firestore.Client,
    *,
    year_number: int,
    week_number: int,
    entry_type: str,
    scenario_ref: int | None,
) -> EntryWriteResult:
    normalized_type, normalized_scenario_ref = _normalize_entry_fields(
        entry_type=entry_type,
        scenario_ref=scenario_ref,
    )
    entries_ref = _entries_collection_ref(client, year_number=year_number, week_number=week_number)
    transaction = client.transaction()
    created_entry_id = entries_ref.document().id

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> None:
        week_snapshot = _get_doc_snapshot(
            txn,
            _week_doc_ref(client, year_number=year_number, week_number=week_number),
        )
        if not week_snapshot.exists:
            raise FirestoreTransitionInvalidError("La week ya no existe.")
        existing = _read_entries_for_week(txn, entries_ref)
        _normalize_entries_order_if_needed(txn, existing)
        next_order = len(existing) + 1
        txn.set(
            entries_ref.document(created_entry_id),
            {
                "type": normalized_type,
                "scenario_ref": normalized_scenario_ref,
                "notes": "",
                "scenario_outcome": None,
                "order_index": next_order,
                "resource_deltas": {},
                "created_at_utc": firestore.SERVER_TIMESTAMP,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )

    try:
        _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover - defensive mapping
        _map_firestore_write_exception(exc)

    return EntryWriteResult(
        entry_ref=EntryRef(year_number=year_number, week_number=week_number, entry_id=created_entry_id)
    )


def update_entry(
    client: firestore.Client,
    *,
    entry_ref: EntryRef,
    entry_type: str,
    scenario_ref: int | None,
) -> EntryWriteResult:
    normalized_type, normalized_scenario_ref = _normalize_entry_fields(
        entry_type=entry_type,
        scenario_ref=scenario_ref,
    )
    entry_doc_ref = _entry_doc_ref(client, entry_ref)
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> None:
        snapshot = _get_doc_snapshot(txn, entry_doc_ref)
        if not snapshot.exists:
            raise FirestoreTransitionInvalidError("La entry ya no existe.")
        txn.update(
            entry_doc_ref,
            {
                "type": normalized_type,
                "scenario_ref": normalized_scenario_ref,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )

    try:
        _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover
        _map_firestore_write_exception(exc)

    return EntryWriteResult(entry_ref=entry_ref)


def update_entry_notes(
    client: firestore.Client,
    *,
    entry_ref: EntryRef,
    notes: str,
) -> EntryWriteResult:
    if not isinstance(notes, str):
        raise FirestoreValidationError("`notes` debe ser string.")

    entry_doc_ref = _entry_doc_ref(client, entry_ref)
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> None:
        snapshot = _get_doc_snapshot(txn, entry_doc_ref)
        if not snapshot.exists:
            raise FirestoreTransitionInvalidError("La entry ya no existe.")
        txn.update(
            entry_doc_ref,
            {
                "notes": notes,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )

    try:
        _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover
        _map_firestore_write_exception(exc)

    return EntryWriteResult(entry_ref=entry_ref)


def delete_entry(
    client: firestore.Client,
    *,
    entry_ref: EntryRef,
) -> EntryWriteResult:
    entry_doc_ref = _entry_doc_ref(client, entry_ref)
    entries_ref = entry_doc_ref.parent
    campaign_doc_ref = _campaign_doc_ref(client)
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> EntryWriteResult:
        entry_snapshot = _get_doc_snapshot(txn, entry_doc_ref)
        if not entry_snapshot.exists:
            raise FirestoreTransitionInvalidError("La entry ya no existe.")

        entry_data = entry_snapshot.to_dict() or {}
        resource_deltas = _parse_resource_map(
            entry_data.get("resource_deltas") or {},
            field_label="resource_deltas",
        )

        auto_stopped_session_id: str | None = None
        sessions_query = entry_doc_ref.collection("sessions")
        session_snaps = list(sessions_query.stream(transaction=txn))
        for session_snap in session_snaps:
            session_data = session_snap.to_dict() or {}
            if session_data.get("ended_at_utc") is None and auto_stopped_session_id is None:
                auto_stopped_session_id = session_snap.id

        next_resource_totals: dict[str, int] | None = None

        if resource_deltas:
            campaign_snapshot = _get_doc_snapshot(txn, campaign_doc_ref)
            if not campaign_snapshot.exists:
                raise FirestoreConflictError("La campaña ya no existe. Pulsa Refresh y reintenta.")
            campaign_data = campaign_snapshot.to_dict() or {}
            resource_totals = _parse_resource_map(
                campaign_data.get("resource_totals") or {},
                field_label="campaign.resource_totals",
            )
            for key, delta in resource_deltas.items():
                base_total = resource_totals.get(key)
                if base_total is None:
                    raise FirestoreConflictError(
                        "Se detectó inconsistencia de recursos (total ausente). Pulsa Refresh y reintenta."
                    )
                next_total = base_total - delta
                if next_total < 0:
                    raise FirestoreConflictError(
                        "Se detectó inconsistencia de recursos (total negativo al borrar). Pulsa Refresh y reintenta."
                    )
                resource_totals[key] = next_total

            next_resource_totals = resource_totals

        # En transacciones Firestore, todas las lecturas deben ocurrir antes de la primera escritura.
        existing = _read_entries_for_week(txn, entries_ref)
        _normalize_entries_order_if_needed(txn, existing)

        for session_snap in session_snaps:
            txn.delete(session_snap.reference)

        if next_resource_totals is not None:
            txn.update(
                campaign_doc_ref,
                {
                    "resource_totals": next_resource_totals,
                    "updated_at_utc": firestore.SERVER_TIMESTAMP,
                },
            )
        remaining = [item for item in existing if item["snapshot"].reference.path != entry_doc_ref.path]

        txn.delete(entry_doc_ref)
        for index, item in enumerate(remaining, start=1):
            if item["order_index"] != index:
                txn.update(
                    item["snapshot"].reference,
                    {
                        "order_index": index,
                        "updated_at_utc": firestore.SERVER_TIMESTAMP,
                    },
                )

        return EntryWriteResult(entry_ref=entry_ref, auto_stopped_session_id=auto_stopped_session_id)

    try:
        return _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover
        _map_firestore_write_exception(exc)


def reorder_entry_within_week(
    client: firestore.Client,
    *,
    entry_ref: EntryRef,
    direction: Literal["up", "down"],
) -> EntryWriteResult:
    if direction not in {"up", "down"}:
        raise FirestoreValidationError("Dirección de reorder no soportada.")

    entries_ref = _entries_collection_ref(
        client,
        year_number=entry_ref.year_number,
        week_number=entry_ref.week_number,
    )
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> None:
        entries = _read_entries_for_week(txn, entries_ref)
        _normalize_entries_order_if_needed(txn, entries)

        ordered_snaps = [item["snapshot"] for item in sorted(entries, key=lambda item: item["order_index"])]
        current_index = next(
            (i for i, snap in enumerate(ordered_snaps) if snap.id == entry_ref.entry_id),
            None,
        )
        if current_index is None:
            raise FirestoreTransitionInvalidError("La entry ya no existe en la week visible.")

        if direction == "up":
            if current_index == 0:
                raise FirestoreTransitionInvalidError("La entry ya está en la primera posición.")
            new_index = current_index - 1
        else:
            if current_index == len(ordered_snaps) - 1:
                raise FirestoreTransitionInvalidError("La entry ya está en la última posición.")
            new_index = current_index + 1

        entry_snap = ordered_snaps.pop(current_index)
        ordered_snaps.insert(new_index, entry_snap)

        for idx, snap in enumerate(ordered_snaps, start=1):
            current_order_raw = (snap.to_dict() or {}).get("order_index")
            if current_order_raw != idx:
                txn.update(
                    snap.reference,
                    {
                        "order_index": idx,
                        "updated_at_utc": firestore.SERVER_TIMESTAMP,
                    },
                )

    try:
        _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover
        _map_firestore_write_exception(exc)

    return EntryWriteResult(entry_ref=entry_ref)


def _normalize_entry_fields(*, entry_type: str, scenario_ref: int | None) -> tuple[str, int | None]:
    if entry_type not in {"scenario", "outpost"}:
        raise FirestoreValidationError("`type` de entry no soportado.")
    if entry_type == "scenario":
        if isinstance(scenario_ref, bool) or not isinstance(scenario_ref, int) or scenario_ref <= 0:
            raise FirestoreValidationError("`scenario_ref` debe ser entero positivo para entries de tipo scenario.")
        return entry_type, scenario_ref
    if scenario_ref not in {None, ""}:
        # tolerate UI passing 0/""
        if scenario_ref is not None:
            raise FirestoreValidationError("`scenario_ref` debe estar vacío para entries de tipo outpost.")
    return entry_type, None


def _campaign_doc_ref(client: firestore.Client) -> Any:
    return client.collection("campaigns").document(CAMPAIGN_ID)


def _entries_collection_ref(client: firestore.Client, *, year_number: int, week_number: int) -> Any:
    return _week_doc_ref(client, year_number=year_number, week_number=week_number).collection("entries")


def _entry_doc_ref(client: firestore.Client, entry_ref: EntryRef) -> Any:
    return _entries_collection_ref(
        client,
        year_number=entry_ref.year_number,
        week_number=entry_ref.week_number,
    ).document(entry_ref.entry_id)


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


def _read_entries_for_week(txn: firestore.Transaction, entries_ref: Any) -> list[dict[str, Any]]:
    query = entries_ref.order_by("order_index")
    snapshots = list(query.stream(transaction=txn))
    result: list[dict[str, Any]] = []
    for snap in snapshots:
        data = snap.to_dict() or {}
        order_index = data.get("order_index")
        if isinstance(order_index, bool) or not isinstance(order_index, int) or order_index <= 0:
            raise FirestoreValidationError(
                f"Entry inválida en {snap.reference.path}: `order_index` debe ser entero positivo."
            )
        result.append({"snapshot": snap, "order_index": order_index})
    return result


def _normalize_entries_order_if_needed(txn: firestore.Transaction, entries: list[dict[str, Any]]) -> None:
    if not entries:
        return
    ordered = sorted(entries, key=lambda item: item["order_index"])
    expected = 1
    changed = False
    for item in ordered:
        if item["order_index"] != expected:
            changed = True
            break
        expected += 1
    if not changed:
        return
    for index, item in enumerate(ordered, start=1):
        txn.update(
            item["snapshot"].reference,
            {
                "order_index": index,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )
        item["order_index"] = index


def _parse_resource_map(raw_map: Any, *, field_label: str) -> dict[str, int]:
    if not isinstance(raw_map, dict):
        raise FirestoreValidationError(f"`{field_label}` debe ser un mapa.")
    parsed: dict[str, int] = {}
    for key, value in raw_map.items():
        if not isinstance(key, str):
            raise FirestoreValidationError(f"`{field_label}` contiene una clave no string.")
        if isinstance(value, bool) or not isinstance(value, int):
            raise FirestoreValidationError(f"`{field_label}[{key}]` debe ser entero.")
        parsed[key] = value
    return parsed


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
